"""N107: five object-centric options with native-reward SMDP learning.

Only a compiler grounded by N106's native *observed* effects can emit actions.
The architecture deliberately separates unsupported plans from executed options:
invalid proposals have duration zero and are NOT native transitions, so they do
not get a fictitious environment reward. Frozen B1 is an explicit bootstrap.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter, defaultdict
from typing import Optional
import math
import numpy as np
from n106_odsl import NativeCompiler, Operation, parse_scene, render_operation
from n106_executor import GuardedExecutor

OPTIONS = (
    'Fill_Hollow_With_Border_Color',
    'Recolor_Small_Outlier_To_Majority',
    'Translate_To_Nearest_Same_Color',
    'Translate_Toward_Row_Alignment',
    'Recolor_Small_Outlier_To_Background',
)

@dataclass(frozen=True)
class Proposal:
    name: str
    operation: Operation


def abstract_key(frame):
    """Coordinate- and palette-name-invariant *coarse* object features.

    Deliberately not guaranteed sufficient or Markov. Persistent option-global
    values additionally transfer when object counts/shapes change.
    """
    scene = parse_scene(frame, max_objects=97)
    objs = [o for o in scene.objects if o.area >= 2]
    if len(scene.objects) >= 97:
        return ('fragmented',)
    color_groups = Counter(o.color for o in objs)
    bin_count = lambda n: min(int(n), 5)
    return ('objects', bin_count(len(objs)),
            bin_count(sum(bool(o.holes) for o in objs)),
            bin_count(sum(o.kind == 'solid' for o in objs)),
            bin_count(sum(o.kind == 'line' for o in objs)),
            bin_count(sum(v > 1 for v in color_groups.values())),
            bin_count(len(set(o.shape_key for o in objs))))


def _renderable(scene, op):
    try:
        return not np.array_equal(render_operation(scene, op),scene.frame)
    except (ValueError, IndexError):
        return False


def generate_proposals(frame):
    """One deterministic candidate per option: *desired* changes, not actions."""
    s=parse_scene(frame, max_objects=97)
    if len(s.objects)>=97:return []
    objs=[o for o in s.objects if o.area>=2]
    if not objs:return []
    output=[]
    def put(name,op):
        if _renderable(s,op):output.append(Proposal(name,op))

    rings=sorted((o for o in objs if o.holes),key=lambda o:(-len(o.holes),-o.area,o.id))
    for ring in rings:
        op=Operation('FloodFill',ring.id,color=ring.color)
        if _renderable(s,op):
            put(OPTIONS[0],op);break

    foreground_colors=Counter()
    for o in objs:foreground_colors[o.color]+=o.area
    majority=sorted(foreground_colors.items(),key=lambda x:(-x[1],x[0]))[0][0]
    candidates=sorted((o for o in objs if o.color!=majority),key=lambda o:(o.area,o.id))
    if candidates and candidates[0].area < sum(o.area for o in objs)/2:
        put(OPTIONS[1],Operation('Recolor',candidates[0].id,color=majority))

    same=[]
    for o in objs:
        for other in objs:
            if o.id==other.id or o.color!=other.color:continue
            dx=other.centroid[0]-o.centroid[0]
            dy=other.centroid[1]-o.centroid[1]
            dist=abs(dx)+abs(dy)
            if dist<=0:continue
            # Translate toward adjacency, not into an overlapping same-colour
            # object. Bound the objective to one 8-step licensed option.
            if abs(dy)>abs(dx):
                gap=(other.bbox[1]-1-o.bbox[3] if dy>0 else
                     other.bbox[3]+1-o.bbox[1])
                step=(0,int(np.clip(gap,-8,8)))
            else:
                gap=(other.bbox[0]-1-o.bbox[2] if dx>0 else
                     other.bbox[2]+1-o.bbox[0])
                step=(int(np.clip(gap,-8,8)),0)
            if step==(0,0):continue
            op=Operation('Translate',o.id,dx=step[0],dy=step[1])
            if _renderable(s,op):same.append((dist,o.id,other.id,op))
    if same:
        put(OPTIONS[2],min(same,key=lambda p:(p[0],p[1],p[2]))[3])

    row=[]
    for o in objs:
        for other in objs:
            if o.id==other.id:continue
            dy=other.centroid[1]-o.centroid[1]
            if abs(dy)<0.6:continue
            # The macro objective is the new object's row, not a one-step
            # greedy gradient. N106 may compile up to eight *charged* moves.
            step=int(np.clip(round(dy),-8,8))
            if not step:continue
            op=Operation('Translate',o.id,dy=step)
            if _renderable(s,op):row.append((abs(dy),o.area,o.id,other.id,op))
    if row:
        # Object *role*, not numeric colour or component traversal order.
        # Prefer moving the smaller object to align with the larger anchor.
        put(OPTIONS[3],min(row,key=lambda p:(p[0],p[1],p[2],p[3]))[4])

    small=sorted((o for o in objs if o.area<=2 and len(objs)>1),key=lambda o:(o.area,o.id))
    if small:
        put(OPTIONS[4],Operation('Recolor',small[0].id,color=s.background))
    return output


class MetaQ:
    """SMDP Q-learning. Real SDK rewards only; gamma^duration bootstrapping.

    Global option Q (level persistent) backs up coarse state-option Q for
    transfer. State signatures alone cannot guarantee semantic equivalence.
    No Q update is made for ungroundable options, since they execute no action.
    """
    def __init__(self,gamma=0.985,alpha=0.45,initial=0.5,puct_c=0.10):
        if not 0<gamma<=1 or not 0<alpha<=1:raise ValueError('invalid gamma or alpha')
        self.gamma=float(gamma);self.alpha=float(alpha)
        self.initial=float(initial);self.puct_c=float(puct_c)
        self.global_q={o:self.initial for o in OPTIONS}
        self.state_q={}
        self.state_visits=Counter()
        self.invalid=Counter()
        self.updates=[]
        self.level_start_snapshots=[]
    def q(self,state,opt):
        return self.state_q.get((state,opt),self.global_q[opt])
    def choose(self,state,grounded):
        names=sorted(set(grounded))
        if not names:return None
        # NOTE: Frozen N093 actor predicts native clicks, not abstract options.
        # Uniform option prior is honest, rather than misusing neural logits.
        return max(names,key=lambda o:(self.q(state,o)+self.puct_c/len(names)/
                                (1+self.state_visits[(state,o)]+self.invalid[(state,o)]),-OPTIONS.index(o)))
    def reject(self,state,opt,reason):
        if opt not in OPTIONS:raise ValueError(opt)
        self.invalid[(state,opt)]+=1
        # Rejection is not an MDP/SMDP transition, so never alter environment Q.
    def update(self,state,opt,rewards,next_state,done):
        if opt not in OPTIONS:raise ValueError(opt)
        tau=len(rewards)
        if tau<1:raise ValueError('duration-zero rejected options cannot be SMDP updates')
        if not all(float(r) in (0.,1.) for r in rewards):
            raise ValueError('only binary native reward permitted')
        ret=sum((self.gamma**i)*float(r) for i,r in enumerate(rewards))
        if not done:
            if next_state is None:raise ValueError('nonterminal transition needs next state')
            ret+=(self.gamma**tau)*max(self.q(next_state,o) for o in OPTIONS)
        old=self.q(state,opt)
        new=old+self.alpha*(ret-old)
        self.state_q[(state,opt)]=new
        oldglobal=self.global_q[opt]
        self.global_q[opt]=oldglobal+self.alpha*(ret-oldglobal)
        self.state_visits[(state,opt)]+=1
        rec=dict(state=repr(state),option=opt,duration=tau,rewards=list(map(float,rewards)),
                 terminal=bool(done),return_target=float(ret),q_before=old,q_after=float(new),
                 global_before=oldglobal,global_after=float(self.global_q[opt]))
        self.updates.append(rec)
        return rec
    def level_transition(self,level):
        self.level_start_snapshots.append(dict(level=int(level),global_q=self.global_q.copy(),
                                               local_entries=len(self.state_q)))
    def stats(self):
        return dict(option_updates=len(self.updates),rewarded_option_updates=sum(
                        x['terminal'] and any(r>0 for r in x['rewards']) for x in self.updates),
                    meta_global_q=self.global_q.copy(),meta_entries=len(self.state_q),
                    rejected_options=sum(self.invalid.values()),
                    max_option_duration=max((x['duration'] for x in self.updates),default=0),
                    level_snapshots=self.level_start_snapshots)


class N107Controller:
    """Option-first controller, grounded by N106; B1 bootstrap/fallback.

    Native option steps still update B1's empirical Q with the *real* reward.
    Separate meta-Q is preserved when B1 clears pixel nodes on level change.
    """
    def __init__(self,core,model:Optional[NativeCompiler]=None,level_budget=200,max_macro=8):
        self.core=core;self.model=model if model is not None else NativeCompiler(min_support=2)
        self.meta=MetaQ()
        self.executor=GuardedExecutor(self.model,max_clicks=max_macro)
        self.budget=int(level_budget)
        self.level=-1;self.used=0;self.tau_rewards=[]
        self.option_origin=None;self.active_option=None
        self.waiting_mode=None;self.last_before=None;self.last_action=None
        self.fallbacks=0;self.compiled_calls=0;self.proposals=0
        self.compile_rejections=Counter();self.rewards=0;self.frame_mismatches=0
    def initialize(self,completed,frame):
        self.level=int(completed)
        self.core.start_level(self.level,np.asarray(frame,np.uint8))
        self.meta.level_transition(self.level)
    def _stage_core(self,frame,legal,action):
        """Stage an externally selected legal action into unmodified B1 Bellman."""
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
    def _finish_macro(self,after,done):
        if self.active_option is None:return
        next_state=None if done else abstract_key(after)
        self.meta.update(self.option_origin,self.active_option,self.tau_rewards,next_state,done)
        self.active_option=None;self.option_origin=None;self.tau_rewards=[]
    def choose(self,frame,legal):
        if self.waiting_mode is not None:raise RuntimeError('observe the previous native action first')
        if self.used>=self.budget:return None,'level_action_cap'
        frame=np.asarray(frame,np.uint8);legal=np.asarray(legal,bool)
        if legal.shape!=(7,):raise ValueError('native legal vector must have 7 entries')
        state=abstract_key(frame)
        action=None;mode='fallback'
        if self.active_option is not None:
            action,why=self.executor.next_action(frame)
            if action is None:
                self.compile_rejections[why]+=1
                self.executor.cancel('partial_option_stopped') if self.executor.steps else None
                self._finish_macro(frame,done=False)
        if action is None:
            # Identical result, much cheaper: when the strict N106 compiler has
            # no trusted native effects, NO option can be grounded. Do not
            # repeatedly parse and compile five known-unexecutable operations.
            proposals=generate_proposals(frame) if self.model.trusted() else []
            self.proposals+=len(proposals)
            # Consider all applicable five options, but require compiler success.
            # When not grounded, never issue guessed clicks.
            grounded=[]
            for proposal in proposals:
                plan,why=self.model.compile(frame,proposal.operation,legal,max_steps=self.executor.max_clicks)
                if plan is None:
                    self.compile_rejections[why]+=1
                    self.meta.reject(state,proposal.name,why)
                elif 0<len(plan)<=min(self.executor.max_clicks,self.budget-self.used):
                    grounded.append(proposal)
            chosen=self.meta.choose(state,[p.name for p in grounded])
            if chosen is not None:
                proposal=next(p for p in grounded if p.name==chosen)
                good,reason=self.executor.propose(frame,proposal.operation,legal)
                if good:
                    action,why=self.executor.next_action(frame)
                    if action is not None:
                        self.active_option=proposal.name
                        self.option_origin=state
                        self.tau_rewards=[]
                        mode='option'
                if action is None:
                    self.compile_rejections[reason if not good else why]+=1
        else:mode='option'
        if action is None:
            action=int(self.core.choose(frame,legal));self.fallbacks+=1;mode='fallback'
        else:
            slot=(1,2,3,4,5,7)[action] if action<6 else 6
            if not bool(legal[slot-1]):raise AssertionError('compiler emitted illegal native action')
            self._stage_core(frame,legal,action)
            self.compiled_calls+=1
        self.waiting_mode=mode;self.last_before=frame.copy();self.last_action=int(action)
        return int(action),mode
    def observe(self,frame,legal,completed,*,outgoing_frame=None,terminal=False):
        if self.waiting_mode is None:raise RuntimeError('no native action pending')
        completed=int(completed);old_level=self.level
        if completed<old_level or completed>old_level+1:raise ValueError('unexpected level change')
        reward=float(completed>old_level)
        post=np.asarray(frame,np.uint8)
        outgoing=np.asarray(outgoing_frame if outgoing_frame is not None else frame,np.uint8)
        if old_level==0 and self.waiting_mode=='fallback' and not reward:
            # Strict N106 contradictions are monotone within an episode:
            # once a native control has an inconsistent or non-primitive
            # observation, this exact compiler can never trust that control.
            # Skipping later redundant attempts preserves trusted() exactly.
            action_key = self.last_action if self.last_action < 6 else 6
            if not self.model.contradictions[action_key]:
                self.model.observe(self.last_before,outgoing,self.last_action)
        if self.waiting_mode=='option':
            self.tau_rewards.append(reward)
            right,why=self.executor.observe(outgoing,native_level_reward=bool(reward))
            if not right and not reward:self.frame_mismatches+=1
            if not self.executor.steps or reward or terminal:
                if terminal and self.executor.steps:self.executor.cancel('terminal')
                self._finish_macro(post,done=bool(reward or terminal))
        self.core.observe(post,np.asarray(legal,bool),completed,terminal=bool(terminal))
        self.used+=1
        if reward:
            self.rewards+=1
            self.level=completed
            self.used=0
            if self.active_option is not None:
                # Reward is authoritative, but should have been finalized above.
                self._finish_macro(post,done=True)
            self.executor.cancel('level_transition') if self.executor.steps else None
            self.meta.level_transition(self.level)
        if terminal and self.active_option is not None:self._finish_macro(post,done=True)
        self.last_action=None;self.last_before=None;self.waiting_mode=None
        return reward
    def stats(self):
        return dict(level=self.level,used_in_current_level=self.used,
                    native_option_actions=self.compiled_calls,native_fallback_actions=self.fallbacks,
                    proposals=self.proposals,compile_rejections=dict(self.compile_rejections),
                    postcondition_mismatches=self.frame_mismatches,native_rewards=self.rewards,
                    **self.meta.stats())
