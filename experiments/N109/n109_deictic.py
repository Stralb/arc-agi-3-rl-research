"""N109: image-observable deictic click anchoring, no abstract action inference.

Strictly replay-based experiment. A closest visible component is an *anchor
hypothesis*, NOT evidence that the component causes the action's effects.
References only observations available at decision time.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import Counter
from typing import Optional
import math
import numpy as np
from n106_odsl import parse_scene


@dataclass(frozen=True)
class Signature:
    color: int
    area: int
    aspect_n: int
    aspect_d: int
    kind: str


@dataclass(frozen=True)
class Anchor:
    action: int
    signature: Signature
    dx: float
    dy: float
    original_x: int
    original_y: int
    distance: float
    source_matches: int
    clicked_component: bool


@dataclass(frozen=True)
class Token:
    action: int
    anchor: Optional[Anchor] = None
    source_sha: str = ''


def sig_of(o):
    x0,y0,x1,y1=o.bbox
    w=x1-x0+1;h=y1-y0+1
    d=math.gcd(w,h)
    return Signature(int(o.color),int(o.area),int(w//d),int(h//d),str(o.kind))


def index_for_click(action):
    if action<6 or action>=6+64*64:raise ValueError('not a native click index')
    return (int((action-6)%64),int((action-6)//64))


def action_for_click(x,y):
    if not (0<=x<64 and 0<=y<64):raise ValueError('off-screen click')
    return 6+int(y)*64+int(x)


def encode(frame, action, *, source_sha=''):
    """Learn anchor only from the *pre-click* current observation.

    Tie-breaking must abstain; object order or position is not an invariant.
    Key-action tokens stay key actions. No outcome or future frame is accessed.
    """
    a=int(action)
    if a<6:return Token(a,None,source_sha)
    x,y=index_for_click(a)
    scene=parse_scene(frame)
    if not scene.objects:return Token(a,None,source_sha)
    ranked=sorted(((math.hypot(x-o.centroid[0],y-o.centroid[1]),o) for o in scene.objects), key=lambda v:v[0])
    if len(ranked)>1 and abs(ranked[1][0]-ranked[0][0])<1e-8:
        return Token(a,None,source_sha)
    d,obj=ranked[0]
    sg=sig_of(obj)
    candidates=sum(sig_of(o)==sg for o in scene.objects)
    return Token(a,Anchor(a,sg,float(x-obj.centroid[0]),float(y-obj.centroid[1]),
                     x,y,float(d),candidates,(y,x) in set(obj.pixels)),source_sha)


def resolve(token, frame, *, mode='deictic', legal=None):
    """Return (encoded native action, status). No SDK calls and no fallback.

    mode='absolute' is the precommitted direct-click playback control.
    """
    a=int(token.action)
    if a<6:
        if legal is not None and not _legal(a,legal):return None,'illegal_key'
        return a,'key_replay'
    if mode=='absolute':
        if legal is not None and not _legal(a,legal):return None,'illegal_click'
        return a,'absolute_click'
    if mode!='deictic':raise ValueError('unsupported mode')
    if token.anchor is None:return None,'no_unambiguous_source_anchor'
    scene=parse_scene(frame)
    matched=[o for o in scene.objects if sig_of(o)==token.anchor.signature]
    if not matched:return None,'unmatched_level2_signature'
    if len(matched)!=1:return None,'ambiguous_level2_signature'
    obj=matched[0]
    # Python round uses bankers' ties; source click is integral after adding its
    # own exact centroid-relative residual. For integer translation this remains
    # exact (within floating point). Other geometric scale changes abstain.
    xx=int(round(obj.centroid[0]+token.anchor.dx))
    yy=int(round(obj.centroid[1]+token.anchor.dy))
    if not (0<=xx<64 and 0<=yy<64):return None,'translated_offscreen'
    action=action_for_click(xx,yy)
    if legal is not None and not _legal(action,legal):return None,'illegal_click'
    return action,'deictic_click'


def _legal(action,legal):
    v=np.asarray(legal,dtype=bool)
    if v.shape!=(7,):raise ValueError('native legal vector must have seven entries')
    index=(1,2,3,4,5,7)[action] if action<6 else 6
    return bool(v[index-1])


def summary(tokens):
    out=Counter()
    for t in tokens:
        if t.action<6:out['non_coordinate']+=1
        else:
            out['coordinate_clicks']+=1
            if t.anchor is None:out['unanchored_source_clicks']+=1
            else:
                out['anchored_source_clicks']+=1
                if t.anchor.source_matches>1:out['ambiguous_signature_at_source']+=1
                if t.anchor.clicked_component:out['clicked_component']+=1
                else:out['closest_centroid_not_clicked_component']+=1
    return dict(out)


def export_token(t):
    return {'action':t.action,'anchor':None if t.anchor is None else {
        **asdict(t.anchor),'signature':asdict(t.anchor.signature)
    },'source_sha':t.source_sha}
