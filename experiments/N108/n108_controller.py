"""N108: charged Level-1 UI probes + sequence-grounded N107 SMDP option control.

No simulator lookahead, hidden state, game-specific dispatch, or oracle. Frozen
B1/PUCT runs when runtime interface grammar is not adequately supported.
"""
from __future__ import annotations
from collections import Counter
import numpy as np
from n106_odsl import parse_scene, render_operation, Operation
from n107_smdp import generate_proposals, abstract_key, MetaQ
from n108_grammar import (ActionGrammar,discover_probes,decode_click,obj_click,
                          ui_candidates,ui_identity,near_anchor_object,
                          ui_is_locally_stable)

class N108Controller:
    def __init__(self,core,level_budget=200,max_calibration_calls=8,min_support=2):
        self.core=core;self.meta=MetaQ();self.grammar=ActionGrammar(min_support=min_support)
        self.budget=int(level_budget)
        self.max_calibration_calls=min(int(max_calibration_calls),int(level_budget))
        self.level=-1;self.used=0
        self.initialized=False
        self.pending=None;self.last_before=None;self.last_action=None
        self.probes=[];self.probe_cursor=0;self.active_probe=None;self.pair_ui_after=None
        self.calibration_charged=0;self.calibration_aborts=Counter();self.pairs_probed=0
        self.option=None;self.option_origin=None;self.option_rewards=[]
        self.option_before=None;self.option_stage=0;self.target_signature=None
        self.option_calls=0;self.option_updates=0;self.rewarded_option_updates=0
        self.postcondition_mismatches=0;self.fallback_calls=0;self.rewards=0
        self.rejections=Counter()
        self.level2_licensed=0;self.level2_executed=0;self.level2_option_updates=0
        self.initial_level1_legal_click=False
    def initialize(self,completed,frame,legal):
        self.level=int(completed)
        self.core.start_level(self.level,np.asarray(frame,np.uint8))
        self.meta.level_transition(self.level)
        self.initial_level1_legal_click=bool(np.asarray(legal,bool)[5])
        if self.level==0 and self.initial_level1_legal_click:
            self.probes=discover_probes(frame,max_pairs=self.max_calibration_calls//2)
        self.initialized=True
    def _stage_core(self,frame,legal,action):
        core=self.core
        state=core.node(frame,legal);nd=core.nodes[state]
        if action not in nd['q']:
            nd['actions'].append(int(action));nd['q'][int(action)]=1.0
            nd.pop('prior',None)
        nd['visits']+=1
        core.pending=(state,int(action),int(self.level),np.asarray(frame,np.uint8).copy())
        core.sdk_actions+=1;core.since_reset+=1
        if nd['visits']%80==0:core._expand(state)
        visits=core.puct_state_actions.setdefault(state,{})
        visits[int(action)]=visits.get(int(action),0)+1
    def _legal(self,action,legal):
        ix=(1,2,3,4,5,7)[action]-1 if action<6 else 5
        return bool(np.asarray(legal,bool)[ix])
    def _calibration_choice(self,frame,legal):
        if not bool(legal[5]):return None
        if self.active_probe is not None and self.pair_ui_after is not None:
            p=self.active_probe['spec']
            o=near_anchor_object(frame,p.target_anchor,p.target_signature,p.target_color)
            if o is None:
                self.calibration_aborts['target_no_longer_visible']+=1
                self.active_probe=None;self.pair_ui_after=None
                return None
            action=obj_click(o,'inside_hole' if o.holes else 'on_object')
            if action is None or not self._legal(action,legal):
                self.calibration_aborts['target_click_unavailable']+=1
                self.active_probe=None;self.pair_ui_after=None
                return None
            self.active_probe['before_canvas']=frame.copy()
            self.active_probe['canvas_action']=action
            return int(action),'calibration_canvas'
        while self.probe_cursor<len(self.probes):
            p=self.probes[self.probe_cursor]
            self.probe_cursor+=1
            scene=parse_scene(frame,max_objects=100)
            x,y=p.ui_anchor
            possible=[o for o in ui_candidates(scene) if ui_identity(o)==p.ui_identity]
            if not possible:
                self.calibration_aborts['ui_no_longer_visible']+=1
                continue
            o=min(possible,key=lambda o:((o.centroid[0]-x)**2+(o.centroid[1]-y)**2,o.id))
            action=obj_click(o)
            if action is None or not self._legal(action,legal):
                self.calibration_aborts['ui_click_unavailable']+=1
                continue
            self.active_probe=dict(spec=p,before_ui=frame.copy(),ui_action=action)
            return int(action),'calibration_ui'
        return None
    def _resolve_option_target(self,frame):
        if self.option is None:return None
        src=parse_scene(self.option_before,max_objects=100)
        try:old=src.object(self.option.operation.object_id)
        except (IndexError, ValueError):return None
        scene=parse_scene(frame,max_objects=100)
        targets=[o for o in scene.objects if set(o.pixels)==set(old.pixels) and o.color==old.color]
        if len(targets)!=1:return None
        op=self.option.operation
        new=Operation(op.kind,targets[0].id,dx=op.dx,dy=op.dy,color=op.color)
        return new
    def _option_choice(self,frame,legal):
        if not bool(legal[5]):return None
        if self.option is not None and self.option_stage==1:
            op=self._resolve_option_target(frame)
            if op is None:
                self._finish_option(frame,False)
                self.rejections['option_target_moved_after_ui']+=1
                return None
            self.option_observed_ui=frame.copy()
            self.option_current_op=op
            target=parse_scene(frame,max_objects=100).object(op.object_id)
            action=obj_click(target,self.option.rule.click_role)
            if action is None or not self._legal(action,legal):
                self._finish_option(frame,False)
                self.rejections['option_canvas_unavailable']+=1
                return None
            if action!=self.option.canvas_action:
                self._finish_option(frame,False)
                self.rejections['option_canvas_relocalized']+=1
                return None
            return int(action),'option_canvas'
        if self.option is not None:return None
        if not self.grammar.trusted():return None
        state=abstract_key(frame)
        grounded=[]
        for p in generate_proposals(frame):
            plan,reason=self.grammar.compile(frame,p.operation,legal)
            if plan is None:
                self.rejections[reason]+=1
                continue
            grounded.append((p,plan))
        chosen=self.meta.choose(state,[p.name for p,_ in grounded])
        if chosen is None:return None
        p,plan=next((p,plan) for p,plan in grounded if p.name==chosen)
        self.option=plan;self.option_name=p.name;self.option_origin=state
        self.option_rewards=[];self.option_stage=0;self.option_before=frame.copy()
        if self.level>=1:self.level2_licensed+=1
        return int(plan.ui_action),'option_ui'
    def _finish_option(self,frame,done):
        if self.option is None:return
        if self.option_rewards:
            next_state=None if done else abstract_key(frame)
            info=self.meta.update(self.option_origin,self.option_name,self.option_rewards,next_state,done)
            self.option_updates+=1
            if self.level>=1:self.level2_option_updates+=1
            if any(r>0 for r in self.option_rewards):self.rewarded_option_updates+=1
        self.option=None;self.option_origin=None;self.option_rewards=[];self.option_stage=0
        self.option_before=None
    def choose(self,frame,legal):
        if not self.initialized:raise RuntimeError('initialize first')
        if self.pending is not None:raise RuntimeError('observe previous action first')
        if self.used>=self.budget:return None,'level_action_cap'
        frame=np.asarray(frame,np.uint8);legal=np.asarray(legal,bool)
        if legal.shape!=(7,) or not legal.any():return None,'no_legal_actions'
        selected=None
        if self.level==0 and self.calibration_charged<self.max_calibration_calls:
            selected=self._calibration_choice(frame,legal)
        if selected is None:
            selected=self._option_choice(frame,legal)
        if selected is None:
            action=int(self.core.choose(frame,legal));mode='fallback';self.fallback_calls+=1
        else:
            action,mode=selected
            self._stage_core(frame,legal,action)
            if mode.startswith('calibration'):self.calibration_charged+=1
            if mode.startswith('option'):
                self.option_calls+=1
                if self.level>=1:self.level2_executed+=1
        if not self._legal(action,legal):raise AssertionError('issued illegal native action')
        self.pending=mode;self.last_before=frame.copy();self.last_action=action
        return action,mode
    def observe(self,frame,legal,completed,*,outgoing_frame=None,terminal=False):
        if self.pending is None:raise RuntimeError('missing pending native action')
        level_old=self.level
        completed=int(completed)
        if completed<level_old or completed>level_old+1:raise ValueError('invalid level transition')
        reward=float(completed>level_old)
        current=np.asarray(frame,np.uint8)
        outgoing=np.asarray(outgoing_frame if outgoing_frame is not None else current,np.uint8)
        mode=self.pending
        if mode=='calibration_ui':
            if self.active_probe is not None:
                self.active_probe['after_ui']=outgoing.copy()
                if reward or terminal:
                    self.calibration_aborts['ui_click_advanced_level']+=1
                    self.active_probe=None;self.pair_ui_after=None
                elif not ui_is_locally_stable(self.active_probe['before_ui'],outgoing,
                                              decode_click(self.last_action)):
                    self.calibration_aborts['ui_click_changed_canvas']+=1
                    self.active_probe=None;self.pair_ui_after=None
                else:self.pair_ui_after=outgoing.copy()
        elif mode=='calibration_canvas':
            if self.active_probe is not None:
                b=self.active_probe
                self.grammar.observe_pair(b['before_ui'],b['after_ui'],b['before_canvas'],outgoing,
                                          b['ui_action'],b['canvas_action'],level_advanced=bool(reward))
                self.pairs_probed+=1
            self.active_probe=None;self.pair_ui_after=None
        elif mode.startswith('option') and self.option is not None:
            self.option_rewards.append(reward)
            if mode=='option_ui':
                if reward or terminal:
                    self._finish_option(current,True)
                elif not ui_is_locally_stable(self.option_before,outgoing,decode_click(self.last_action)):
                    self.rejections['ui_postcondition_failed']+=1
                    self.postcondition_mismatches+=1
                    self._finish_option(current,False)
                else:self.option_stage=1
            else:
                if not reward:
                    try:
                        pred=render_operation(parse_scene(self.option_observed_ui,max_objects=100),self.option_current_op)
                        correct=np.array_equal(pred,outgoing)
                    except (ValueError,IndexError):correct=False
                    if not correct:self.postcondition_mismatches+=1
                self._finish_option(current,bool(reward or terminal))
        self.core.observe(current,np.asarray(legal,bool),completed,terminal=bool(terminal))
        self.used+=1
        if reward:
            self.rewards+=1;self.level=completed;self.used=0
            self.active_probe=None;self.pair_ui_after=None
            if self.option is not None:self._finish_option(current,True)
            self.meta.level_transition(self.level)
        if terminal and self.option is not None:self._finish_option(current,True)
        self.pending=None;self.last_before=None;self.last_action=None
        return reward
    def stats(self):
        return dict(level=self.level,used_current_level=self.used,
                    calibration_charged=self.calibration_charged,pairs_probed=self.pairs_probed,
                    probes_planned=len(self.probes),calibration_aborts=dict(self.calibration_aborts),
                    native_option_actions=self.option_calls,level2_licensed=self.level2_licensed,
                    level2_option_actions=self.level2_executed,option_updates=self.option_updates,
                    level2_option_updates=self.level2_option_updates,
                    rewarded_option_updates=self.rewarded_option_updates,
                    fallback_actions=self.fallback_calls,native_rewards=self.rewards,
                    postcondition_mismatches=self.postcondition_mismatches,
                    compile_rejections=dict(self.rejections),grammar=self.grammar.stats(),
                    meta=self.meta.stats())
