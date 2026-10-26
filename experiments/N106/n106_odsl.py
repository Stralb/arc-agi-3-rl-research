"""N106 observable object parser, exact inverse graphics and evidence-gated action compiler.

Observation only. No engine code, game-name dispatch, shadow/oracle steps or
unverified action labels. Emitting a desired pixel transform IS NOT the same as
knowing a native control that produces it. Compilation abstains by default.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict, deque, Counter
from typing import Optional, Tuple
import numpy as np
from scipy import ndimage as ndi

CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=np.uint8)


@dataclass(frozen=True)
class Object:
    id: int
    color: int
    pixels: Tuple[Tuple[int,int], ...]  # y,x pairs, not original source positions
    bbox: Tuple[int,int,int,int]        # x0,y0,x1,y1 inclusive
    centroid: Tuple[float,float]
    area: int
    holes: Tuple[Tuple[int,int],...]
    kind: str
    touches_border: bool

    @property
    def shape_key(self):
        x0,y0,_,_ = self.bbox
        return tuple((y-y0,x-x0) for y,x in self.pixels)

    @property
    def signature(self):
        x0,y0,x1,y1 = self.bbox
        return (self.kind, self.area, x1-x0+1,y1-y0+1,len(self.holes))


@dataclass(frozen=True)
class Scene:
    frame: np.ndarray
    background: int
    objects: Tuple[Object,...]
    adjacency: Tuple[Tuple[int,int],...]
    containment: Tuple[Tuple[int,int], ...]
    palette: Tuple[int,...]

    def object(self, identity):
        return self.objects[int(identity)]


def _valid_frame(frame):
    arr=np.asarray(frame,dtype=np.uint8)
    if arr.ndim != 2 or arr.shape != (64,64):
        raise ValueError('N106 currently accepts native 64x64 palette frames only')
    return arr


def parse_scene(frame, *, min_area=1, max_objects=1024):
    """Four-connected monochrome components with topology and relational graph.

    Background is the modal palette value (an approximation, not game truth).
    Hollow means a same-colour component bounds an interior pixel region.
    """
    f=_valid_frame(frame)
    hist=np.bincount(f.ravel(), minlength=256)
    background=int(np.argmax(hist))
    palette=tuple(map(int,np.flatnonzero(hist)))
    objects=[]
    for c in palette:
        if c==background:continue
        mask=f==c
        label,n=ndi.label(mask,structure=CROSS)
        slices=ndi.find_objects(label)
        for j,sl in enumerate(slices,1):
            if sl is None:continue
            ys,xs=sl
            local=label[sl]==j
            dy,dx=np.nonzero(local)
            if len(dx)<min_area:continue
            xy=tuple(sorted((int(y+ys.start),int(x+xs.start)) for y,x in zip(dy,dx)))
            x0,y0,x1,y1=min(x for _,x in xy),min(y for y,_ in xy),max(x for _,x in xy),max(y for y,_ in xy)
            filled=ndi.binary_fill_holes(local)
            holes=tuple(sorted((int(y+ys.start),int(x+xs.start)) for y,x in zip(*np.nonzero(filled & ~local))))
            w=x1-x0+1;h=y1-y0+1
            if holes:kind='hollow'
            elif w==1 or h==1:kind='line'
            elif len(xy)==w*h:kind='solid'
            else:kind='irregular'
            o=Object(len(objects),int(c),xy,(x0,y0,x1,y1),
                     (float(np.mean([x for _,x in xy])),float(np.mean([y for y,_ in xy]))),
                     len(xy),holes,kind,
                     (x0==0 or y0==0 or x1==63 or y1==63))
            objects.append(o)
            if len(objects)>=max_objects:break
        if len(objects)>=max_objects:break
    # Relational edges by adjacent pixels (8-neighbour bounding is prefilter).
    adjacent=[];containing=[]
    for i,a in enumerate(objects):
        ax0,ay0,ax1,ay1=a.bbox;aset=set(a.pixels)
        for j in range(i+1,len(objects)):
            b=objects[j];bx0,by0,bx1,by1=b.bbox
            if ax0-1<=bx1 and bx0-1<=ax1 and ay0-1<=by1 and by0-1<=ay1:
                if any((y+dy,x+dx) in aset for y,x in b.pixels for dy,dx in ((-1,0),(0,-1),(1,0),(0,1))):
                    adjacent.append((i,j))
            if a.holes and set(b.pixels).issubset(set(a.holes)):containing.append((i,j))
            if b.holes and aset.issubset(set(b.holes)):containing.append((j,i))
    return Scene(f.copy(),background,tuple(objects),tuple(adjacent),tuple(containing),palette)


@dataclass(frozen=True)
class Operation:
    kind: str
    object_id: int
    dx: int=0
    dy: int=0
    color: Optional[int]=None
    def __post_init__(self):
        if self.kind not in ('Translate','Recolor','FloodFill'):
            raise ValueError(f'Unsupported operation {self.kind}; scale is not supported')
        if self.kind=='Translate' and self.dx==self.dy==0:
            raise ValueError('Zero translation is not a meaningful primitive')
        if self.kind!='Translate' and (self.color is None or not 0<=self.color<=15):
            raise ValueError('Recolor and FloodFill require a native palette colour 0..15')


def render_operation(scene,op):
    """Pure desired-image renderer, NOT native simulator or proof of executability."""
    o=scene.object(op.object_id); f=scene.frame.copy()
    source=set(o.pixels)
    if op.kind=='Translate':
        tgt=set((y+op.dy,x+op.dx) for y,x in source)
        if any(not (0<=y<64 and 0<=x<64) for y,x in tgt):raise ValueError('translation leaves canvas')
        if any((y,x) not in source and int(f[y,x])!=scene.background for y,x in tgt):
            raise ValueError('translation occludes existing nonbackground objects')
        for y,x in source:f[y,x]=scene.background
        for y,x in tgt:f[y,x]=o.color
    elif op.kind=='Recolor':
        if op.color==o.color:raise ValueError('no-op recolouring')
        for y,x in source:f[y,x]=op.color
    elif op.kind=='FloodFill':
        if not o.holes:raise ValueError('target has no enclosed interior')
        if any(int(f[y,x])!=scene.background for y,x in o.holes):
            raise ValueError('interior is not empty background; fill would overwrite another object')
        for y,x in o.holes:f[y,x]=op.color
    return f


def _shiftshape(pixels,base):
    x0,y0,_,_=base
    return tuple((y-y0,x-x0) for y,x in pixels)


def infer_exact_operations(before,after,max_candidates=8):
    """Recover unique *observed visual effect* from exact before/after frames.

    Diagnostic extraction can use AFTER; acting compiler cannot. If multiple
    objects or operations explain an image, return ambiguity rather than invent
    a causal interpretation. Animation/multielement changes typically abstain.
    """
    f=_valid_frame(before);aft=_valid_frame(after)
    if np.array_equal(f,aft):return [],'silent'
    before_scene=parse_scene(f); after_scene=parse_scene(aft)
    changed=f!=aft
    solutions=[]
    # Candidates are only components touching the observed changed region.
    objects=[o for o in before_scene.objects if any(changed[y,x] for y,x in o.pixels) or
             (o.holes and any(changed[y,x] for y,x in o.holes))]
    if len(objects)>max_candidates:
        return [],'too_many_components'
    # Pre-index after components by palette, area, normalized outline.
    post_lookup=defaultdict(list)
    for post in after_scene.objects:
        post_lookup[(post.color,post.area,post.shape_key)].append(post)
    for o in objects:
        old=set(o.pixels)
        # Exact recolour requires only this single component to change.
        vals={int(aft[y,x]) for y,x in o.pixels}
        if len(vals)==1:
            c=next(iter(vals))
            if c!=o.color:
                op=Operation('Recolor',o.id,color=c)
                if np.array_equal(render_operation(before_scene,op),aft):solutions.append(op)
        if o.holes:
            vals={int(aft[y,x]) for y,x in o.holes}
            if len(vals)==1:
                c=next(iter(vals))
                if any(int(f[y,x])!=c for y,x in o.holes):
                    op=Operation('FloodFill',o.id,color=c)
                    try:trial=render_operation(before_scene,op)
                    except ValueError:trial=None
                    if trial is not None and np.array_equal(trial,aft):solutions.append(op)
        for p in post_lookup.get((o.color,o.area,o.shape_key),[]):
            dx=p.bbox[0]-o.bbox[0];dy=p.bbox[1]-o.bbox[1]
            if dx==dy==0 or abs(dx)>12 or abs(dy)>12:continue
            op=Operation('Translate',o.id,dx=dx,dy=dy)
            try:trial=render_operation(before_scene,op)
            except ValueError:continue
            if np.array_equal(trial,aft):solutions.append(op)
    distinct=list(dict.fromkeys(solutions))
    return distinct,'unique' if len(distinct)==1 else ('ambiguous' if distinct else 'not_single_primitive')


@dataclass(frozen=True)
class NativeRule:
    # No game IDs or original absolute ACTION6 click coordinates stored.
    action: int           # internal B1 action id (0..5; >=6 means current-object click)
    kind: str
    dx: int=0
    dy: int=0
    color_relation: str=''
    shape_role: str=''
    shape_signature: tuple=()  # source shape geometry, never source position
    click_role: str=''     # object or enclosed interior
    click_offset: Tuple[int,int]=(0,0)  # x,y within object bbox; no absolute replay


def _relation_colour(scene,op):
    o=scene.object(op.object_id)
    if op.color==scene.background:return 'background'
    if op.color==o.color:return 'same'
    if len(scene.palette)>1:
        # Other colours are not transferable from a single source example.
        return f'literal:{op.color}'
    return f'literal:{op.color}'


def make_native_rule(before,op,action):
    """One level-1 observation of action -> exact transform (hypothesis only)."""
    scene=parse_scene(before);o=scene.object(op.object_id)
    action=int(action)
    if action>=6:
        x=(action-6)%64;y=(action-6)//64
        if (y,x) in set(o.pixels):role='on_object'
        elif (y,x) in set(o.holes):role='inside_hole'
        else:return None
        action=6  # never record historical click position
    else:role='key'
    offset=(x-o.bbox[0],y-o.bbox[1]) if role!='key' else (0,0)
    return NativeRule(action=action,kind=op.kind,dx=op.dx,dy=op.dy,
                      color_relation='' if op.kind=='Translate' else _relation_colour(scene,op),
                      shape_role=o.kind,shape_signature=o.signature,click_role=role,
                      click_offset=offset)


class NativeCompiler:
    """Strict, observed-effect compiler. All emitted action requests must be verified.

    A rule is reliable only when it appeared in >=min_support distinct *visual*
    source states, and the same native control was never seen contradicting it
    in matching states. This is an engineering safety guard, not causality proof.
    """
    def __init__(self,min_support=2):
        self.min_support=int(min_support)
        self.evidence=defaultdict(set)
        self.contradictions=Counter()
        self.action_effects=defaultdict(set)
        self.failures=Counter()

    def observe(self,before,after,action):
        ops,status=infer_exact_operations(before,after)
        signature=(int(action) if int(action)<6 else 6)
        if status!='unique':
            self.contradictions[signature]+=1
            return status
        rule=make_native_rule(before,ops[0],action)
        if rule is None:
            self.contradictions[signature]+=1
            return 'unclickable_target'
        # Distinct preobservations only (identical runs do not increase support).
        import hashlib
        state_digest=hashlib.blake2b(_valid_frame(before).tobytes(),digest_size=12).hexdigest()
        self.evidence[rule].add(state_digest)
        self.action_effects[signature].add(rule)
        return status

    def trusted(self):
        # A conservative compiler abstains if control's observed effects vary;
        # controls that routinely do nothing can't be treated as pure primitives.
        rules=[]
        for rule,examples in self.evidence.items():
            identity=rule.action
            if len(examples)>=self.min_support and len(self.action_effects[identity])==1 and self.contradictions[identity]==0:
                rules.append(rule)
        return tuple(sorted(rules,key=lambda r:(r.kind,r.action,r.dx,r.dy,r.color_relation,r.shape_role)))

    @staticmethod
    def _click(o,role,offset=(0,0)):
        # Exact observed *within-object* click offset, not an invented centroid.
        # New shapes or moved objects still require native postcondition proof.
        x=o.bbox[0]+int(offset[0]);y=o.bbox[1]+int(offset[1])
        if not 0<=x<64 or not 0<=y<64:return None
        if role=='on_object' and (y,x) in o.pixels:return int(6+y*64+x)
        if role=='inside_hole' and (y,x) in o.holes:return int(6+y*64+x)
        return None

    def _resolve_action(self,rule,scene,op,legal):
        obj=scene.object(op.object_id)
        if obj.kind!=rule.shape_role:return None
        if rule.kind!=op.kind:return None
        if rule.action<6:
            # A directional key is global; it contains no object identity.
            # Refuse if the observed geometry admits indistinguishable targets
            # or differs from the calibrated source shape.
            if obj.signature != rule.shape_signature:return None
            if sum(other.signature==rule.shape_signature for other in scene.objects)!=1:
                return None
            action=rule.action
        else:
            action=self._click(obj,rule.click_role,rule.click_offset)
            if action is None:return None
        slot=int((1,2,3,4,5,7)[action]) if action<6 else 6
        if not bool(legal[slot-1]):return None
        return action

    def compile(self,frame,op,legal,max_steps=8):
        scene=parse_scene(frame);legal=np.asarray(legal,bool)
        if legal.shape!=(7,):raise ValueError('Legal action vector has seven entries')
        trusted=self.trusted()
        if not trusted:return None,'no_reliable_action_model'
        if op.kind in ('Recolor','FloodFill'):
            relation=_relation_colour(scene,op)
            matches=[]
            for rule in trusted:
                if rule.kind!=op.kind or rule.color_relation!=relation:continue
                a=self._resolve_action(rule,scene,op,legal)
                if a is not None:matches.append(a)
            matches=list(dict.fromkeys(matches))
            if len(matches)!=1:return None,'no_unique_grounded_native_action'
            return [matches[0]],'compiled_observed_primitive'
        # bounded shortest translation path in observed per-click directions
        moves=[]
        for rule in trusted:
            if rule.kind!='Translate':continue
            a=self._resolve_action(rule,scene,op,legal)
            if a is not None:moves.append((rule.dx,rule.dy,a))
        if not moves:return None,'no_grounded_translation_action'
        queue=deque([(0,0,())]);seen={(0,0)};goal=(op.dx,op.dy);solutions=[]
        for _ in range(max_steps):
            if not queue:break
            nextq=deque()
            while queue:
                x,y,seq=queue.popleft()
                for dx,dy,a in moves:
                    pos=(x+dx,y+dy);path=seq+(a,)
                    if pos==goal:solutions.append(path)
                    elif pos not in seen and abs(pos[0])<=16 and abs(pos[1])<=16:
                        seen.add(pos);nextq.append((pos[0],pos[1],path))
            if solutions:break
            queue=nextq
        unique={tuple(s) for s in solutions}
        if len(unique)!=1:return None,'no_unique_grounded_translation_path'
        return list(next(iter(unique))),'compiled_observed_translation'


def verify_step(scene_before,actual_after,expected_op):
    """On-policy postcondition guard: fail closed when SDK differs from DSL image."""
    try:expected=render_operation(scene_before,expected_op)
    except ValueError:return False
    return bool(np.array_equal(expected,_valid_frame(actual_after)))


def infer_local_operations(before,after,min_area=4,return_scene=False):
    """Higher-recall diagnostic: identify isolated object effects amid other changes.

    NOT a native inverse model. Only accepts unambiguous same-shape matching,
    exact local pixel postconditions, and a movement bound. It may still match
    incidental animation; it is explicitly unsuitable as a goal oracle.
    """
    b=_valid_frame(before);a=_valid_frame(after)
    if np.array_equal(b,a):return ([],None) if return_scene else []
    bs=parse_scene(b,min_area=min_area);ds=parse_scene(a,min_area=min_area)
    bb=defaultdict(list);dd=defaultdict(list)
    for o in bs.objects:bb[(o.color,o.area,o.shape_key)].append(o)
    for o in ds.objects:dd[(o.color,o.area,o.shape_key)].append(o)
    out=[]
    for o in bs.objects:
        src=set(o.pixels)
        # A uniformly recoloured source component; other pixels may also change.
        vals={int(a[y,x]) for y,x in src}
        if len(vals)==1:
            c=next(iter(vals))
            if c!=o.color:out.append(Operation('Recolor',o.id,color=c))
        # Interior fill without destroying any other pre-existing object.
        if o.holes and all(int(b[y,x])==bs.background for y,x in o.holes):
            vals={int(a[y,x]) for y,x in o.holes}
            if len(vals)==1:
                c=next(iter(vals))
                if c!=bs.background:
                    out.append(Operation('FloodFill',o.id,color=c))
        shape=(o.color,o.area,o.shape_key)
        if len(bb[shape])!=1 or len(dd.get(shape,[]))!=1:continue
        p=dd[shape][0]
        dx=p.bbox[0]-o.bbox[0];dy=p.bbox[1]-o.bbox[1]
        if dx==dy==0 or max(abs(dx),abs(dy))>12:continue
        target=set(p.pixels)
        # The surviving object is unchanged in colour and shape. Moved-away
        # pixels must reveal the current modal background, with no occlusions.
        if any(int(a[y,x])!=bs.background for y,x in src-target):continue
        if any(int(a[y,x])!=o.color for y,x in target):continue
        if any(int(b[y,x])!=bs.background for y,x in target-src):continue
        out.append(Operation('Translate',o.id,dx=dx,dy=dy))
    uniq=list(dict.fromkeys(out))
    return (uniq,bs) if return_scene else uniq


@dataclass(frozen=True)
class ContextRule:
    """Exact observed object geometry plus native transform; no game identifier."""
    native: NativeRule
    shape: Tuple[int,int,int,int,int]


class ContextualCompiler:
    """Observational context gate, contrasted against global-action gating.

    Different geometries may have different effects for the same button. A
    directional native action is nevertheless allowed only when ONE object in
    the current scene has the learned shape signature, and calibration data
    show zero contradictions in matching source contexts. No forward engine
    calls are made during planning. Closed-world confidence is NOT claimed.
    """
    def __init__(self,min_support=2):
        self.min_support=int(min_support)
        self.rules={}
        self.stats={}

    @staticmethod
    def _matching_target(scene, rule, action):
        o=[x for x in scene.objects if x.signature==rule.shape]
        if rule.native.action==6:
            x=(int(action)-6)%64;y=(int(action)-6)//64
            if action<6:return None
            if rule.native.click_role=='on_object':o=[z for z in o if (y,x) in z.pixels]
            elif rule.native.click_role=='inside_hole':o=[z for z in o if (y,x) in z.holes]
            else:return None
        return o[0] if len(o)==1 else None

    def fit(self,rows):
        """Rows are recorded Level-1 (before,after,action), never future Level-2."""
        rows=list(rows)
        candidates={}
        for before,after,action in rows:
            ops,status=infer_exact_operations(before,after)
            if status!='unique':continue
            native=make_native_rule(before,ops[0],action)
            if native is None:continue
            shape=parse_scene(before).object(ops[0].object_id).signature
            rule=ContextRule(native,shape)
            candidates[rule]=None
        self.rules={};self.stats={}
        import hashlib
        for rule in candidates:
            tested={};ambiguous=0
            for before,after,action in rows:
                if (int(action) if int(action)<6 else 6)!=rule.native.action:continue
                scene=parse_scene(before)
                target=self._matching_target(scene,rule,action)
                if target is None:
                    if any(z.signature==rule.shape for z in scene.objects):ambiguous+=1
                    continue
                color=None
                if rule.native.kind in ('Recolor','FloodFill'):
                    rel=rule.native.color_relation
                    if rel=='background':color=scene.background
                    elif rel.startswith('literal:'):color=int(rel.split(':')[1])
                    else:continue
                op=Operation(rule.native.kind,target.id,dx=rule.native.dx,
                             dy=rule.native.dy,color=color)
                try:pred=render_operation(scene,op)
                except ValueError:continue
                digest=hashlib.blake2b(np.asarray(before,np.uint8).tobytes(),digest_size=12).hexdigest()
                is_match=bool(np.array_equal(pred,after))
                # If identical state/action has distinct results, use the
                # worst case; do not count repeated traces as new evidence.
                tested[digest]=tested.get(digest,True) and is_match
            correct=sum(tested.values());wrong=len(tested)-correct
            detail={'observed_distinct':len(tested),'positive':correct,'negative':wrong,'ambiguous':ambiguous}
            self.stats[rule]=detail
            if correct>=self.min_support and wrong==0:
                self.rules[rule]=detail
        return self

    def compile(self,frame,op,legal,max_steps=8):
        scene=parse_scene(frame)
        if op.kind=='Translate':
            # Direct one-step only in this proof-of-grounding implementation.
            # Multi-step composition remains covered by NativeCompiler.
            matches=[]
            for rule in self.rules:
                n=rule.native
                if n.kind!=op.kind or (n.dx,n.dy)!=(op.dx,op.dy):continue
                if scene.object(op.object_id).signature!=rule.shape:continue
                if sum(o.signature==rule.shape for o in scene.objects)!=1:continue
                if n.action>=6:continue
                if bool(legal[(1,2,3,4,5,7)[n.action]-1]):matches.append(n.action)
        else:
            matches=[]
            relation=_relation_colour(scene,op)
            for rule in self.rules:
                n=rule.native
                if n.kind!=op.kind or n.color_relation!=relation:continue
                if scene.object(op.object_id).signature!=rule.shape:continue
                if n.action<6:
                    if sum(o.signature==rule.shape for o in scene.objects)!=1:continue
                    if bool(legal[(1,2,3,4,5,7)[n.action]-1]):matches.append(n.action)
                else:
                    action=NativeCompiler._click(scene.object(op.object_id),n.click_role,n.click_offset)
                    if action is not None and bool(legal[5]):matches.append(action)
        matches=list(dict.fromkeys(matches))
        return ([matches[0]],'context_grounded') if len(matches)==1 else (None,'no_verified_unique_context')
