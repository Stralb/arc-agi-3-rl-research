"""N111 whole-grid transformation DSL and exact bounded BFS synthesizer.

All operations run on 2-D uint8 observed arrays. They do NOT emit legal native
SDK actions; there is deliberately no direct-pixel-write action in this DSL.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque, Counter
from typing import Iterable
import hashlib
import numpy as np
from scipy.ndimage import binary_fill_holes

@dataclass(frozen=True)
class Op:
    name: str
    args: tuple[int, ...] = ()

    def as_dict(self) -> dict:
        return {'name': self.name, 'args': list(self.args)}


def check_grid(grid: np.ndarray) -> np.ndarray:
    x = np.asarray(grid)
    if x.ndim != 2 or x.dtype.kind not in 'ui' or not 1 <= x.shape[0] <= 128 or not 1 <= x.shape[1] <= 128:
        raise ValueError('expected bounded 2-D integer grid')
    return np.asarray(x, dtype=np.uint8)


def border_background(x: np.ndarray) -> int:
    """Background = modal border colour, with smallest value breaking ties."""
    border = np.concatenate([x[0], x[-1], x[1:-1, 0], x[1:-1, -1]])
    vals, counts = np.unique(border, return_counts=True)
    return int(vals[np.argmax(counts)])


def fill_enclosed_background(x: np.ndarray, replacement: int) -> np.ndarray:
    """Fill modal-background holes; scipy uses a C-level flood-fill implementation."""
    x = check_grid(x)
    bg = border_background(x)
    if replacement == bg:
        return x.copy()
    bgmask = (x == bg)
    enclosed = bgmask & binary_fill_holes(~bgmask)
    if not enclosed.any():
        return x.copy()
    out = x.copy()
    out[enclosed] = replacement
    return out


def gravity(x: np.ndarray, direction: int) -> np.ndarray:
    """Pack nonbackground cells along an axis without changing relative order."""
    x=check_grid(x)
    if direction not in (0,1,2,3):raise ValueError('invalid gravity direction')
    bg=border_background(x)
    h,w=x.shape
    out=np.full_like(x,bg)
    mask=x!=bg
    if direction<=1:
        yy,xx=np.nonzero(mask)
        rank=np.cumsum(mask,axis=0)[yy,xx]-1
        if direction==1:
            rank=rank+(h-np.sum(mask,axis=0)[xx])
        out[rank,xx]=x[yy,xx]
    else:
        yy,xx=np.nonzero(mask)
        rank=np.cumsum(mask,axis=1)[yy,xx]-1
        if direction==3:
            rank=rank+(w-np.sum(mask,axis=1)[yy])
        out[yy,rank]=x[yy,xx]
    return out


def apply_op(grid:np.ndarray, op:Op) -> np.ndarray:
    x=check_grid(grid)
    if op.name=='Rotate90':
        k=op.args[0]
        if k not in (1,2,3): raise ValueError('rotate k must be 1..3')
        return np.rot90(x,k).copy()
    if op.name=='Reflect':
        if op.args not in ((0,), (1,)):raise ValueError('reflect axis must be 0/1')
        return np.flip(x,axis=op.args[0]).copy()
    if op.name=='ColorMap':
        if len(op.args)!=2:raise ValueError('ColorMap(c1,c2)')
        a,b=op.args
        if not 0<=a<=255 or not 0<=b<=255:raise ValueError('bad colour')
        return np.where(x==a,b,x).astype(np.uint8)
    if op.name=='FloodFill_Background':
        if len(op.args)!=1:raise ValueError('replacement required')
        return fill_enclosed_background(x,op.args[0])
    if op.name=='Gravity_Shift_Pixels':
        return gravity(x,op.args[0])
    raise ValueError(f'unknown op: {op.name}')


def apply_program(x:np.ndarray, ops:Iterable[Op]) -> np.ndarray:
    for op in ops:x=apply_op(x,op)
    return check_grid(x)


def op_vocabulary(source:np.ndarray,target:np.ndarray) -> list[Op]:
    """Freeze operations from Level-1 source and target palettes only.

    True BFS over these fixed operations. No target-pixel action oracle.
    """
    x=check_grid(source);y=check_grid(target)
    present=sorted(set(np.unique(x).tolist()) | set(np.unique(y).tolist()))
    ops=[Op('Rotate90',(k,)) for k in (1,2,3)] + [Op('Reflect',(a,)) for a in (0,1)]
    ops += [Op('Gravity_Shift_Pixels',(d,)) for d in (0,1,2,3)]
    ops += [Op('FloodFill_Background',(color,)) for color in present]
    ops += [Op('ColorMap',(a,b)) for a in present for b in present if a!=b]
    return ops


def _digest(arr:np.ndarray) -> bytes:
    return hashlib.blake2b(arr.tobytes(order='C'),digest_size=16).digest()


def hamming(x:np.ndarray,y:np.ndarray) -> int:
    if x.shape!=y.shape:return int(max(x.size,y.size))
    return int(np.count_nonzero(x!=y))


def synthesize(source:np.ndarray,target:np.ndarray,*,max_depth:int=3,max_states:int=5000) -> dict:
    """Exact shortest-path BFS, bounded by expanded unique states.

    If truncated, failure means 'not found under budget', never 'impossible'.
    Depth bound and every cost are program operations, not SDK calls.
    """
    x=check_grid(source);y=check_grid(target)
    if x.shape!=y.shape:raise ValueError('target shape differs; this vocabulary preserves shape for square grids')
    if not 0<=max_depth<=4 or max_states<1:raise ValueError('invalid bounds')
    ops=op_vocabulary(x,y)
    if np.array_equal(x,y):
        return {'matched':True,'trivial_identity':True,'program':[],'best_distance':0,
                'identity_distance':0,'explored_states':1,'candidate_expansions':0,'exhausted':True,
                'hit_state_cap':False,'vocabulary_size':len(ops),'max_depth':max_depth,'max_states':max_states}
    visited={_digest(x)}
    q=deque([(x,())]); expanded=0; candidates=0
    best=hamming(x,y);bestprog=()
    found=None; hit=False
    while q:
        if expanded>=max_states:
            hit=True;break
        grid, prog=q.popleft()
        expanded+=1
        if len(prog)>=max_depth:continue
        for oi,op in enumerate(ops):
            cand=apply_op(grid,op)
            candidates+=1
            if np.array_equal(cand,grid):continue
            key=_digest(cand)
            if key in visited:continue
            visited.add(key)
            candidate_prog=(*prog,oi)
            score=hamming(cand,y)
            if score<best:
                best=score;bestprog=candidate_prog
            if score==0:
                found=candidate_prog;break
            if len(candidate_prog)<max_depth:q.append((cand,candidate_prog))
        if found is not None:break
    result={'matched':found is not None,'trivial_identity':False,
            'program':[ops[i].as_dict() for i in found] if found is not None else [],
            'best_program':[ops[i].as_dict() for i in bestprog],
            'best_distance':best,'identity_distance':hamming(x,y),
            'explored_states':expanded,'unique_states':len(visited),
            'candidate_expansions':candidates,'exhausted':found is None and not hit,
            'hit_state_cap':hit,'vocabulary_size':len(ops),
            'max_depth':max_depth,'max_states':max_states}
    if found is not None:assert np.array_equal(apply_program(x,[ops[i] for i in found]),y)
    return result


def pixel_diff_commands(current:np.ndarray,target:np.ndarray) -> list[tuple[int,int,int]]:
    """Desired (x,y,colour) writes only; NOT a native SDK action compiler.

    A GameAction ACTION6 is a click, not a 'set pixel to this colour' command.
    A notebook must not execute these commands as if their effects were known.
    """
    a=check_grid(current);b=check_grid(target)
    if a.shape!=b.shape:raise ValueError('shape mismatch')
    yy,xx=np.where(a!=b)
    return [(int(x),int(y),int(b[y,x])) for y,x in zip(yy,xx)]
