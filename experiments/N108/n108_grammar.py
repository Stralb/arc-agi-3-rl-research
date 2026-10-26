"""N108 native-observation-only, two-action UI grammar learner.

A candidate is *not* a palette until supported by observed interactions.
Only charged SDK actions supply transitions. Neither this module nor the
controller consults game source, hidden engine state, or a shadow rollout.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import blake2b
from typing import Optional
import numpy as np
from n106_odsl import Operation, parse_scene, infer_exact_operations, render_operation


def frame_hash(frame):
    return blake2b(np.asarray(frame,np.uint8).tobytes(), digest_size=12).hexdigest()


def click(x, y):
    x,y=int(x),int(y)
    if not (0<=x<64 and 0<=y<64):raise ValueError('click must be in native 64x64 frame')
    return 6+64*y+x


def decode_click(action):
    if action<6:raise ValueError('not an ACTION6 coordinate')
    v=int(action)-6
    return v%64, v//64


def obj_click(obj,kind='on_object'):
    points=obj.holes if kind=='inside_hole' else obj.pixels
    if not points:return None
    cy,cx=obj.centroid[1],obj.centroid[0]
    y,x=min(points,key=lambda p:((p[0]-cy)**2+(p[1]-cx)**2,p[0],p[1]))
    return click(x,y)


def zone(obj):
    x,y=obj.centroid
    borders={'top':y,'bottom':63-y,'left':x,'right':63-x}
    return min(borders,key=lambda k:(borders[k],k))


def is_peripheral(obj):
    x,y=obj.centroid
    return (2 <= obj.area <= 32 and min(x,63-x,y,63-y)<=13)


def ui_identity(obj):
    x0,y0,x1,y1=obj.bbox
    return (obj.kind,int(obj.area),x1-x0+1,y1-y0+1,len(obj.holes),zone(obj))


def ui_candidates(scene):
    """Rank *possible* interface glyphs, not asserted action controls."""
    all_candidates=[o for o in scene.objects if is_peripheral(o)]
    if len(all_candidates)<2:return []
    # A toolbar hypothesis needs two spatially related small elements.
    clustered=[]
    for o in all_candidates:
        if any(p.id!=o.id and abs(p.centroid[0]-o.centroid[0])+abs(p.centroid[1]-o.centroid[1])<=20
               for p in all_candidates):
            clustered.append(o)
    return sorted(clustered,key=lambda o:(min(o.centroid[0],63-o.centroid[0],
                                           o.centroid[1],63-o.centroid[1]),
                                          o.area,o.id))


def canvas_candidates(scene,interfaces):
    ui_ids={o.id for o in interfaces}
    candidates=[o for o in scene.objects if o.id not in ui_ids and o.area>=4 and
                10<=o.centroid[0]<=53 and 10<=o.centroid[1]<=53 and
                o.area<1500]
    return sorted(candidates,key=lambda o:(abs(o.centroid[0]-31.5)+abs(o.centroid[1]-31.5),-o.area,o.id))


@dataclass(frozen=True)
class Probe:
    ui_identity:tuple
    ui_anchor:tuple
    target_anchor:tuple
    target_signature:tuple
    target_color:int
    ui_color:int


def discover_probes(frame,max_pairs=4):
    s=parse_scene(frame,max_objects=100)
    ui=ui_candidates(s)
    targets=canvas_candidates(s,ui)
    if not ui or not targets:return []
    probes=[]
    # At most two distinct UI candidates and two distinct targets, to spend <=8 clicks.
    for u,t in [(u,t) for u in ui[:2] for t in targets[:2]]:
        ua=obj_click(u)
        ta=obj_click(t, 'inside_hole' if t.holes else 'on_object')
        if ua is None or ta is None or ua==ta:continue
        probes.append(Probe(ui_identity(u),decode_click(ua),decode_click(ta),
                            t.signature,t.color,u.color))
    return probes[:max_pairs]


def near_anchor_object(frame,anchor,signature,color,*,hole=False):
    """Track within the *same* episode only. Not used for cross-level compilation."""
    s=parse_scene(frame,max_objects=120)
    options=[o for o in s.objects if o.signature==signature and o.color==color]
    if not options:return None
    px,py=anchor
    return min(options,key=lambda o:((o.centroid[0]-px)**2+(o.centroid[1]-py)**2,o.id))


def ui_is_locally_stable(before,after,anchor,margin=3,max_external=6):
    """Palette-selection click may highlight UI but should not alter the canvas."""
    a=np.asarray(before,np.uint8);b=np.asarray(after,np.uint8)
    if a.shape!=(64,64) or b.shape!=(64,64):return False
    x,y=anchor
    outside=a!=b
    outside[max(0,y-margin):min(64,y+margin+1),max(0,x-margin):min(64,x+margin+1)]=False
    return int(outside.sum())<=max_external


@dataclass(frozen=True)
class GrammarRule:
    ui_role:tuple
    operation_kind:str
    target_kind:str
    click_role:str
    effect:tuple
    target_color_relation:str
    ui_color_relation:str


@dataclass(frozen=True)
class CompiledPair:
    ui_action:int
    canvas_action:int
    operation:Operation
    rule:GrammarRule


class ActionGrammar:
    """Sequence-effect correlation, with strict repetition/uniqueness gates.

    Even a 'trusted' rule is a reproducible *association*, not evidence that
    the UI click was necessary; a without-UI counterfactual is unavailable.
    """
    def __init__(self,min_support=2):
        self.min_support=int(min_support)
        self.examples=defaultdict(set)
        self.contradictions=Counter()
        self.effect_families=defaultdict(set)
        self.attempts=0
        self.local_ui_clicks=0
        self.pairs_completed=0
        self.unique_primitives=0
        self.failures=Counter()
        self.compiles=Counter()
        self.rule_details=[]
    def _relation(self,scene,ui,op):
        if op.kind=='Translate':return ('translation','any')
        if op.color==ui.color:return ('same_as_ui','target_color')
        if op.color==scene.background:return ('background','background')
        return ('unsupported','unsupported')
    def observe_pair(self,ui_before,after_ui,before_canvas,after_canvas,
                     ui_action,canvas_action,*,level_advanced=False):
        self.attempts+=1
        if not ui_is_locally_stable(ui_before,after_ui,decode_click(ui_action)):
            self.failures['ui_click_changed_canvas']+=1
            return None,'ui_click_changed_canvas'
        self.local_ui_clicks+=1
        if level_advanced:
            self.failures['reward_animation_confounds_visual_effect']+=1
            return None,'reward_animation_confounds_visual_effect'
        self.pairs_completed+=1
        ui_scene=parse_scene(ui_before,max_objects=100)
        ux,uy=decode_click(ui_action)
        ui=[o for o in ui_scene.objects if (uy,ux) in o.pixels and is_peripheral(o)]
        if len(ui)!=1:
            self.failures['ui_object_ambiguous']+=1
            return None,'ui_object_ambiguous'
        ui=ui[0]
        src=parse_scene(before_canvas,max_objects=100)
        tx,ty=decode_click(canvas_action)
        targets=[o for o in src.objects if (ty,tx) in o.pixels or (ty,tx) in o.holes]
        if len(targets)!=1:
            self.failures['canvas_object_ambiguous']+=1
            return None,'canvas_object_ambiguous'
        target=targets[0]
        family=(ui_identity(ui),target.kind,'inside_hole' if (ty,tx) in target.holes else 'on_object')
        ops,status=infer_exact_operations(before_canvas,after_canvas)
        if status!='unique' or len(ops)!=1 or ops[0].object_id!=target.id:
            self.contradictions[family]+=1
            self.failures[f'not_target_unique_primitive:{status}']+=1
            return None,'not_target_unique_primitive'
        op=ops[0]
        self.unique_primitives+=1
        color_rel,ui_rel=self._relation(src,ui,op)
        if color_rel=='unsupported':
            self.contradictions[family]+=1
            self.failures['unsupported_color_relation']+=1
            return None,'unsupported_color_relation'
        effect=(int(op.dx),int(op.dy)) if op.kind=='Translate' else (color_rel,)
        rule=GrammarRule(family[0],op.kind,target.kind,family[2],effect,color_rel,ui_rel)
        self.examples[rule].add(frame_hash(before_canvas))
        self.effect_families[family].add(rule)
        self.rule_details.append(dict(kind=rule.operation_kind,role=repr(rule.ui_role),
                                      effect=repr(rule.effect),source_hash=frame_hash(before_canvas)))
        return rule,'observed_pair_primitive'
    def trusted(self):
        return tuple(sorted((r for r,states in self.examples.items()
                             if len(states)>=self.min_support and
                             len(self.effect_families[(r.ui_role,r.target_kind,r.click_role)])==1 and
                             not self.contradictions[(r.ui_role,r.target_kind,r.click_role)]),
                            key=repr))
    def compile(self,frame,op,legal):
        legal=np.asarray(legal,bool)
        if legal.shape!=(7,) or not legal[5]:
            self.compiles['ACTION6_unavailable']+=1
            return None,'ACTION6_unavailable'
        s=parse_scene(frame,max_objects=100)
        if op.object_id>=len(s.objects):return None,'missing_target'
        target=s.object(op.object_id)
        try:
            intended=render_operation(s,op)
        except (ValueError,IndexError):
            return None,'invalid_desired_transform'
        if np.array_equal(intended,s.frame):return None,'no_effect'
        plans=[]
        for r in self.trusted():
            if r.operation_kind!=op.kind or r.target_kind!=target.kind:continue
            if r.operation_kind=='Translate':
                if r.effect!=(op.dx,op.dy):continue
            elif r.target_color_relation=='same_as_ui':
                pass
            elif r.target_color_relation=='background' and op.color!=s.background:
                continue
            else:
                continue
            ui=[u for u in ui_candidates(s) if ui_identity(u)==r.ui_role and
                (r.operation_kind=='Translate' or r.target_color_relation!='same_as_ui' or u.color==op.color)]
            if len(ui)!=1:continue
            u=ui[0]
            if r.click_role=='inside_hole' and not target.holes:continue
            ta=obj_click(target,r.click_role)
            ua=obj_click(u)
            if ta is None or ua is None or ta==ua:continue
            plans.append(CompiledPair(ua,ta,op,r))
        unique={(p.ui_action,p.canvas_action):p for p in plans}
        if len(unique)!=1:
            why='no_unique_grammatical_sequence' if unique else 'no_grounded_sequence'
            self.compiles[why]+=1
            return None,why
        self.compiles['licensed']+=1
        return next(iter(unique.values())),'licensed_observed_pair'
    def stats(self):
        return dict(calibration_pairs=self.attempts,locally_stable_ui_clicks=self.local_ui_clicks,
                    completed_pairs=self.pairs_completed,unique_target_primitives=self.unique_primitives,
                    candidate_rules=len(self.examples),trusted_rules=len(self.trusted()),
                    rule_supports={repr(k):len(v) for k,v in self.examples.items()},
                    calibration_failures=dict(self.failures),compiler=dict(self.compiles))
