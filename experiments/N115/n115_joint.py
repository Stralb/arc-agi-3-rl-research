"""N115: legal, charged two-action options on top of *unmodified* frozen N093.

All options consist of two native actions. Both actions are performed through
SDK.step by the caller; there are no shadow transitions, reset queries, hidden
state reads, environment-dependent dispatch, privileged goal frames or pseudo
SDK rewards. This module does not import any privileged simulator search.

The base B1 engine receives and updates EVERY atomic transition. Separately,
SMDP values are learned at option boundaries, gamma**duration, from native
level advances only. Invalid second actions abort the pending option; they do
not invent an environment transition or fake a reward.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
import numpy as np

GAMMA = 0.985


def action_is_legal(a,legal):
    v=np.asarray(legal,bool)
    a=int(a)
    return (a>=6 and a<4102 and len(v)>5 and bool(v[5])) or (
        0<=a<6 and len(v)>6 and bool(v[(0,1,2,3,4,6)[a]]))


@dataclass
class ActivePair:
    start_key: str
    start_level: int
    first: int
    second: int
    steps: int=0
    reward: float=0.0
    first_effect: bool=False


class JointOptionController:
    """Chooses atomic or precommitted two-step actions, never simulates the SDK."""
    def __init__(self,core,mode='mixed',every=5,max_pairs_per_level=34,
                 gamma=GAMMA,optimistic=1.0,enable_pair_backups=True):
        if mode not in ('mixed','cross','repeat','atomic','adaptive'):
            raise ValueError('unknown N115 mode')
        self.core=core
        self.mode=mode
        self.every=int(every)
        self.max_pairs_per_level=int(max_pairs_per_level)
        self.gamma=float(gamma)
        self.optimistic=float(optimistic)
        self.enable_pair_backups=bool(enable_pair_backups)
        if self.every<1 or self.max_pairs_per_level<0 or not 0<gamma<=1:
            raise ValueError('invalid controller settings')
        self.q=defaultdict(dict)
        self.visits=Counter()
        self.global_visits=Counter()
        self.smdp_updates=0
        self.smdp_value_changes=0
        self.invalid_pair_penalties=0
        self.pairs_started=0
        self.pairs_finished=0
        self.pairs_aborted=0
        self.pairs_rewarded=0
        self.pairs_cross=0
        self.pairs_repeat=0
        self.charged_pair_actions=0
        self.b1_atomic_actions=0
        self.unsafe_action_avoided=0
        self.last_level=int(core.level)
        self.local_step=0
        self.recent_silent=0
        self.active=None
        self.last_driver='baseline'
        self.execution_log=[]
        self.selected_pairs=[]

    def _new_level(self):
        if self.last_level!=int(self.core.level):
            self.last_level=int(self.core.level)
            self.local_step=0
            self.recent_silent=0
            if self.active is not None:
                self.active=None
            self.q.clear();self.visits.clear();self.global_visits.clear()
            self.pairs_started=0

    def _frozen_puct_menu(self,f,legal):
        """Only frozen B1 candidate grammar and frozen pretrained prior."""
        s=self.core.node(f,legal)
        nd=self.core.nodes[s]
        acts=np.asarray(nd['actions'],np.int64)
        probs=self.core.puct_probabilities(nd,acts)
        values=np.asarray([nd['q'][int(a)] for a in acts],float)
        counts=self.core.puct_state_actions.get(s,{})
        counts=np.asarray([counts.get(int(a),0) for a in acts],float)
        score=values+self.core.puct_c*probs/(1.+counts)
        order=np.argsort(-score,kind='stable')
        chosen=[int(acts[i]) for i in order[:min(8,len(order))]]
        lookup={int(a):(float(probs[i]),float(values[i])) for i,a in enumerate(acts)}
        return s, chosen, lookup

    def _pick_pair(self,f,legal):
        s,menu,lookup=self._frozen_puct_menu(f,legal)
        if not menu:return None
        # Candidate count <= 8*8; pair selection does NOT roll out hypothetical
        # actions and can never see successor screenshots at selection time.
        choices=[]
        for a in menu[:6]:
            for b in menu:
                if self.mode=='repeat' and a!=b:continue
                if self.mode=='cross' and a==b:continue
                if not action_is_legal(a,legal) or not action_is_legal(b,legal):continue
                pair=(a,b)
                pa,qa=lookup[a];pb,qb=lookup[b]
                prior=np.sqrt(pa*pb)
                oldq=(self.q[s].get(pair,self.optimistic) if self.enable_pair_backups
                      else self.optimistic)
                tried=self.visits[(s,a,b)]
                global_count=self.global_visits[pair]
                # B1 Q-value encourages promising first actions; pessimistic
                # empirical bigrams decay from the optimistic initializer.
                # Global visits limit exhausting the same pair on new frames.
                score=(oldq+.10*(qa-self.optimistic)+.20*prior/(1+tried)
                       +.06/(1+global_count))
                choices.append((score,a,b))
        if not choices:return None
        _,a,b=max(choices,key=lambda t:(t[0],-t[1],-t[2]))
        return s,int(a),int(b)

    def _stage_committed(self,action,frame,legal):
        """Stage one chosen action using N093's existing native update API."""
        a=int(action)
        if not action_is_legal(a,legal):
            self.unsafe_action_avoided+=1
            raise RuntimeError('Attempt to stage an SDK-illegal action')
        s=self.core.node(frame,legal)
        nd=self.core.nodes[s]
        if a not in nd['q']:
            nd['actions'].append(a)
            nd['q'][a]=1.0
            nd.pop('prior',None)
        nd['visits']+=1
        counts=self.core.puct_state_actions.setdefault(s,{})
        if counts.get(a,0)>0:self.core.puct_revisits+=1
        counts[a]=counts.get(a,0)+1
        self.core.puct_choices+=1
        self.core.pending=(s,a,int(self.core.level),np.asarray(frame,np.uint8).copy())
        self.core.since_reset+=1
        self.core.sdk_actions+=1
        if nd['visits']%80==0:self.core._expand(s)
        return a

    def _abort_invalid_second(self):
        # The first step was already charged; do not execute an illegal second
        # step. The penalty affects only the internal pair preference, not the
        # native SDK reward stream or B1's reward-driven Bellman learner.
        pair=self.active
        if pair is None:return
        self.pairs_aborted+=1
        self.invalid_pair_penalties+=1
        k=(pair.start_key,pair.first,pair.second)
        self.visits[k]+=1
        self.global_visits[(pair.first,pair.second)]+=1
        if self.enable_pair_backups:
            previous=self.q[pair.start_key].get((pair.first,pair.second),self.optimistic)
            updated=previous+(-0.05-previous)/self.visits[k]
            self.q[pair.start_key][(pair.first,pair.second)]=updated
            self.smdp_updates+=1
            self.smdp_value_changes+=int(abs(updated-previous)>1e-12)
        self.active=None

    def _adaptive_second(self,frame,legal,first):
        # Optional ablation: second click is selected from the legal menu
        # *after* the first real SDK observation. No uncharged simulation.
        _,menu,_=self._frozen_puct_menu(frame,legal)
        if not menu:return None
        for a in menu:
            if a!=first and action_is_legal(a,legal):return a
        return menu[0] if action_is_legal(menu[0],legal) else None

    def choose(self,frame,legal,remaining):
        self._new_level()
        f=np.asarray(frame,np.uint8)
        if self.active is not None:
            if self.mode=='adaptive' and self.active.steps==1:
                refreshed=self._adaptive_second(f,legal,self.active.first)
                if refreshed is not None:self.active.second=int(refreshed)
            if (self.core.level!=self.active.start_level or not action_is_legal(self.active.second,legal)
                    or remaining<=0):
                self._abort_invalid_second()
            else:
                a=self._stage_committed(self.active.second,f,legal)
                self.last_driver='bigram_second'
                self.charged_pair_actions+=1
                self.local_step+=1
                return a
        should_pair=(self.mode!='atomic' and int(self.core.level)>=1 and remaining>=2 and
                     self.pairs_started<self.max_pairs_per_level and
                     (self.local_step%self.every==0 or self.recent_silent>=2))
        if should_pair:
            pair=self._pick_pair(f,legal)
            if pair is not None:
                s,a,b=pair
                self.active=ActivePair(s,int(self.core.level),a,b)
                self.pairs_started+=1
                if a==b:self.pairs_repeat+=1
                else:self.pairs_cross+=1
                self.selected_pairs.append((int(self.core.level)+1,a,b))
                result=self._stage_committed(a,f,legal)
                self.last_driver='bigram_first'
                self.charged_pair_actions+=1
                self.local_step+=1
                return result
        a=int(self.core.choose(f,legal))
        self.last_driver='frozen_N093'
        self.b1_atomic_actions+=1
        self.local_step+=1
        return a

    def observe(self,before,after,legal,completed,terminal=False):
        if self.core.pending is None:
            raise RuntimeError('Missing frozen B1 pending native action')
        before=np.asarray(before,np.uint8)
        after=np.asarray(after,np.uint8)
        old_level=int(self.core.level)
        reward=float(int(completed)>old_level)
        driver=self.last_driver
        if driver=='bigram_first' and self.active is not None:
            self.active.steps+=1
            self.active.reward+=reward
            self.active.first_effect=bool(np.any(before!=after))
        elif driver=='bigram_second' and self.active is not None:
            self.active.steps+=1
            self.active.reward+=(self.gamma**(self.active.steps-1))*reward
        self.core.observe(after,legal,completed,terminal=terminal)
        if before.shape==after.shape and not np.any(before!=after):self.recent_silent+=1
        else:self.recent_silent=0
        self.execution_log.append({'source':driver,'level':old_level+1,
                                   'reward':int(reward>0),'change':int(np.count_nonzero(before!=after))})
        pair=self.active
        if pair is None:return
        if pair.steps>=2 or reward>0 or terminal or int(completed)!=pair.start_level:
            duration=pair.steps
            if duration<=0:raise AssertionError('zero-duration option')
            term=bool(terminal or reward>0 or int(completed)!=pair.start_level)
            next_value=self.optimistic
            if not term:
                sp=self.core.node(after,legal)
                next_value=self.core._value(sp)
            old=self.q[pair.start_key].get((pair.first,pair.second),self.optimistic)
            target=pair.reward+(0.0 if term else self.gamma**duration*next_value)
            key=(pair.start_key,pair.first,pair.second)
            self.visits[key]+=1
            new=old+(target-old)/self.visits[key]
            self.global_visits[(pair.first,pair.second)]+=1
            if self.enable_pair_backups:
                self.q[pair.start_key][(pair.first,pair.second)]=new
                self.smdp_updates+=1
                if abs(new-old)>1.e-12:self.smdp_value_changes+=1
            self.pairs_finished+=1
            if pair.reward>0:self.pairs_rewarded+=1
            self.active=None

    def report(self):
        return {'mode':self.mode,'pair_backups_enabled':self.enable_pair_backups,
                'invalid_pair_penalties':self.invalid_pair_penalties,
                'pairs_started':self.pairs_finished+self.pairs_aborted+int(self.active is not None),
                'pairs_finished':self.pairs_finished,'pairs_aborted':self.pairs_aborted,
                'pairs_rewarded':self.pairs_rewarded,'pairs_repeat':self.pairs_repeat,
                'pairs_cross':self.pairs_cross,'charged_pair_actions':self.charged_pair_actions,
                'baseline_atomic_actions':self.b1_atomic_actions,'smdp_updates':self.smdp_updates,
                'smdp_value_changes':self.smdp_value_changes,'illegal_second_avoided':self.unsafe_action_avoided,
                'selected_pairs':self.selected_pairs}
