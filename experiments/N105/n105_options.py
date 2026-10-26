"""N105: observed, charged, bounded options atop the untouched N093 B1 Bellman core.

Only Level-1 on-policy source actions are used to synthesize initial options.
The strict arm uses exactly those options. The open arm admits Level-2
B1-generated legal action candidates, explicitly marking this as a distinct
hypothesis. Each option consists of one SDK action repeated until the first
zero-pixel-delta step, visual-cycle detection, a native level transition, a
legal-action change, or the fixed action cap. Each atomic step is charged and
is observed by the original B1 Bellman model; option-level reward is only
native level advancement. No oracle, reset, SDK cloning, engine state, game ID
features, or trajectory hindsight enters acting code.

Option backups use the semi-Markov Bellman target:
    Q(s,o) = mean[R + gamma**duration * max_o' Q(s',o')]
This does not make partial-observation visual states Markov; it is an empirical
semi-Markov backup over the selected visible endpoint abstraction.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter, defaultdict, deque
from hashlib import blake2b
import numpy as np

GAMMA = 0.985


def frame_hash(frame):
    return blake2b(np.asarray(frame,np.uint8).tobytes(),digest_size=12).hexdigest()


def state_key(frame,legal):
    return blake2b(np.asarray(frame,np.uint8).tobytes()+np.asarray(legal,np.uint8).tobytes(),digest_size=16).hexdigest()


@dataclass(frozen=True)
class SourceBlock:
    action: int
    length: int
    visible: int
    silent: int
    block_index: int


def synthesize_blocks(trajectory):
    """Parse exact contiguous Level-1 actions; no Level-2 outcome leakage."""
    blocks=[]
    for row in trajectory:
        a=int(row['action'])
        if blocks and blocks[-1]['action']==a:
            b=blocks[-1]; b['length']+=1
            b['visible']+=int(row['changed']>0);b['silent']+=int(row['changed']==0)
        else:
            blocks.append({'action':a,'length':1,'visible':int(row['changed']>0),
                           'silent':int(row['changed']==0),'block_index':len(blocks)})
    return [SourceBlock(**d) for d in blocks]


class EndpointBellman:
    """Semi-Markov empirical Bellman graph, with reward on native level events."""
    def __init__(self,gamma=GAMMA,enable_backups=True):
        self.gamma=float(gamma)
        self.enable_backups=bool(enable_backups)
        self.q=defaultdict(dict)
        self.counts=defaultdict(Counter)
        self.transitions=defaultdict(Counter)
        self.parents=defaultdict(set)
        self.updates=0
        self.changed_backups=0
        self.action_changes=0

    def register(self,s,opts):
        for a in opts:
            self.q[s].setdefault(int(a),1.0)
        return self.q[s]

    def value(self,s):
        q=self.q.get(s)
        return max(q.values()) if q else 1.0

    def backup(self,s,a):
        h=self.transitions[(s,int(a))]
        if not h:return 0.0
        total=sum(h.values())
        updated=0.0
        for (sp,r,end,d),n in h.items():
            updated+=n*(r if end else r+(self.gamma**d)*self.value(sp))
        updated/=total
        old=self.q[s][int(a)]
        self.q[s][int(a)]=updated
        self.updates+=1
        if abs(old-updated)>1e-8:self.changed_backups+=1
        return abs(old-updated)

    def observe_option(self,s,a,sp,reward,end,duration,next_actions):
        if duration<1:raise ValueError('Option requires at least one charged action')
        self.register(s,[a])
        if not end:self.register(sp,next_actions)
        if not end:self.parents[sp].add((s,int(a)))
        self.counts[s][int(a)]+=1
        self.transitions[(s,int(a))][(sp,float(reward),bool(end),int(duration))]+=1
        if not self.enable_backups:return 0.0
        changed=self.backup(s,a)
        if changed>1e-8:
            queue=deque([s]);n=0
            while queue and n<128:
                target=queue.popleft()
                for ps,pa in sorted(self.parents[target]):
                    old_v=self.value(ps)
                    if self.backup(ps,pa)>1e-8 and abs(self.value(ps)-old_v)>1e-7:
                        queue.append(ps)
                    n+=1
                    if n>=128:break
        return changed


class MacroOptionController:
    def __init__(self,core,variant='source_only',max_option_steps=12,level_budget=200,enable_backups=True):
        if variant not in ('source_only','open','open_novel'):
            raise ValueError('Expected source_only, open or open_novel')
        self.core=core
        self.variant=variant
        self.max_option_steps=int(max_option_steps)
        self.level_budget=int(level_budget)
        self.source_steps=[];self.blocks=[];self.source_order=[];self.option_info={}
        self.bellman=EndpointBellman(enable_backups=enable_backups)
        self.active=None
        self.level2_actions=0
        self.option_count=0
        self.stop_reasons=Counter()
        self.traces=[]
        self.learned_options=0
        self.open_option_choices=0
        self.source_option_choices=0

    def record_source(self,a,pre,post,reward):
        if self.core.level not in (0,1):raise AssertionError('source is Level 1 only')
        self.source_steps.append({'action':int(a),'changed':int(np.count_nonzero(pre!=post)),
                                  'native_reward':bool(reward)})
        if reward:
            self.blocks=synthesize_blocks(self.source_steps)
            # Preserve source order, collapse duplicate controls; no hand-coded game feature.
            for b in self.blocks:
                if b.action not in self.source_order:self.source_order.append(b.action)
                info=self.option_info.setdefault(b.action,{'length':0,'visible':0,'silent':0})
                info['length']+=b.length;info['visible']+=b.visible;info['silent']+=b.silent

    def _legal_option(self,a,legal):
        return bool(legal[5] if a>=6 else legal[(1,2,3,4,5,7)[int(a)]-1])

    def _new_action_candidates(self,frame,legal):
        if self.variant not in ('open','open_novel'):return []
        # The B1 candidate grammar and the frozen pretrained prior are reused;
        # this produces NEW Level-2 controls, not source demonstrations.
        s=self.core.node(frame,legal)
        nd=self.core.nodes[s]
        actions=np.asarray(nd['actions'],dtype=int)
        if not len(actions):return []
        p=self.core.puct_probabilities(nd,actions)
        q=np.array([nd['q'][int(x)] for x in actions],dtype=float)
        n=self.core.puct_state_actions.get(s,{})
        scores=q+0.10*p/(1.+np.asarray([n.get(int(x),0) for x in actions]))
        order=np.argsort(-scores,kind='stable')
        # Two possibilities: the original naive top-two (often source actions),
        # or a controlled vocabulary-coverage variant requiring genuinely
        # different B1-proposed controls at the same observed endpoint.
        if self.variant=='open_novel':
            return [int(actions[i]) for i in order if int(actions[i]) not in self.source_order][:2]
        return [int(actions[i]) for i in order[:2]]

    def candidates(self,frame,legal):
        source=[a for a in self.source_order if self._legal_option(a,legal)]
        novel=[a for a in self._new_action_candidates(frame,legal) if self._legal_option(a,legal)]
        # Preserve options previously introduced by native observations.
        opts=list(dict.fromkeys(source+novel))
        return opts

    def _stage_b1(self,a,frame,legal):
        s=self.core.node(frame,legal)
        nd=self.core.nodes[s]
        if a not in nd['q']:
            nd['actions'].append(int(a));nd['q'][int(a)]=1.0
            nd.pop('prior',None)
        nd['visits']+=1
        self.core.pending=(s,int(a),int(self.core.level),np.asarray(frame,np.uint8).copy())
        self.core.sdk_actions+=1;self.core.since_reset+=1
        if nd['visits']%80==0:self.core._expand(s)
        visit=self.core.puct_state_actions.setdefault(s,{})
        visit[a]=visit.get(a,0)+1

    def select(self,frame,legal):
        if self.level2_actions>=self.level_budget:return None,'level_cap'
        frame=np.asarray(frame,np.uint8)
        legal=np.asarray(legal,bool)
        if self.active is not None:
            a=self.active['action']
            if self._legal_option(a,legal):
                self._stage_b1(a,frame,legal)
                return a,'continue'
            self._finish(frame,legal,False,'action_became_illegal')
        opts=self.candidates(frame,legal)
        if not opts:return None,'no_source_options_or_legal_actions'
        s=state_key(frame,legal)
        q=self.bellman.register(s,opts)
        # Q first, optimistic exploration among options; source-order tie break
        # is independent of future Level-2 outcomes.
        score=[]
        for idx,a in enumerate(opts):
            n=self.bellman.counts[s][a]
            src=a in self.source_order
            source_bonus=(0.006/(idx+1) if src else 0.)
            exploration=0.012/(1+n)
            score.append(float(q[a])+source_bonus+exploration)
        action=int(opts[int(np.argmax(score))])
        self.active=dict(action=action,start=s,steps=0,changed=0,silent=0,
                         seen={frame_hash(frame)},source=(action in self.source_order))
        self.option_count+=1
        if action in self.source_order:self.source_option_choices+=1
        else:self.open_option_choices+=1;self.learned_options+=1
        self._stage_b1(action,frame,legal)
        return action,'option_start'

    def _finish(self,frame,legal,reward,why,terminal=False):
        o=self.active
        if o is None:return
        end=bool(terminal or reward)
        sp=state_key(frame,legal) if not end else 'TERMINAL'
        possible=self.candidates(frame,legal) if not end else []
        self.bellman.observe_option(o['start'],o['action'],sp,
                                    1.0 if reward else 0.0,end,o['steps'],possible)
        self.stop_reasons[why]+=1
        self.traces.append(dict(source=bool(o['source']),action=int(o['action']),
                                duration=o['steps'],visible=o['changed'],silent=o['silent'],
                                why=why,level_reward=bool(reward),
                                source_start=o['start'],target=sp))
        self.active=None

    def observe(self,pre,post,legal,completed_before,completed_after,terminal=False):
        if completed_before==0:
            # An outgoing terminal image is supplied in the runner, not the next Level frame.
            self.record_source(self._last_source_action,pre,post,
                               completed_after>completed_before)
            return
        if self.active is None:return
        if completed_before>=2:
            self._finish(post,legal,False,'higher_level',terminal=True);return
        self.level2_actions+=1
        o=self.active
        o['steps']+=1
        reward=completed_after>completed_before
        if not reward:
            delta=int(np.count_nonzero(np.asarray(pre,np.uint8)!=np.asarray(post,np.uint8)))
            o['changed']+=int(delta>0);o['silent']+=int(delta==0)
            key=frame_hash(post)
            cycled=key in o['seen']
            o['seen'].add(key)
        else:delta=-1;cycled=False
        why=('native_reward' if reward else
             'native_terminal' if terminal else
             'zero_delta' if delta==0 else
             'visual_cycle' if cycled else
             'option_step_cap' if o['steps']>=self.max_option_steps else
             'level_budget' if self.level2_actions>=self.level_budget else
             None)
        if why:self._finish(post,legal,reward,why,terminal=terminal)

    def set_last_source_action(self,a):
        self._last_source_action=int(a)

    def stats(self):
        return dict(variant=self.variant,backups_enabled=self.bellman.enable_backups,source_blocks=[vars(b) for b in self.blocks],
                    source_options=self.source_order,options_executed=self.option_count,
                    option_durations=[t['duration'] for t in self.traces],
                    macro_actions=sum(t['duration'] for t in self.traces),
                    multi_step_options=sum(t['duration']>1 for t in self.traces),
                    stop_reasons=dict(self.stop_reasons),level2_actions=self.level2_actions,
                    source_option_choices=self.source_option_choices,
                    open_option_choices=self.open_option_choices,
                    bellman_updates=self.bellman.updates,
                    bellman_changed_backups=self.bellman.changed_backups,
                    option_traces=self.traces)
