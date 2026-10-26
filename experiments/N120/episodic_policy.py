"""N093 PUCT plus *observational* Q(s,h,a) prior on Level3 only.
No simulated successors: the frozen selector has no leaf-search tree. Native
reward remains the ONLY Bellman reward. All unobserved actions remain legal.
"""
from __future__ import annotations
from collections import deque,Counter
from pathlib import Path
import numpy as np
import torch
from reference_policy import AuditedCrossLevelCore
from episodic_features import state_features,candidate_features
from value_model import EpisodicValueNet

MODES=('value_mc','value_td','value_shuffle','value_hard','value_state_only','value_td_online')

class EpisodicPUCTCore(AuditedCrossLevelCore):
    def __init__(self,*args,mode='value_td',model_dir=None,**kwargs):
        if mode not in MODES:raise ValueError(mode)
        super().__init__(*args,mode='local',**kwargs)
        self.value_mode=mode
        checkpoint='model_'+('mc' if mode=='value_mc' else 'shuffled' if mode=='value_shuffle' else 'td')+'.pt'
        entry=torch.load(str(Path(model_dir)/checkpoint),map_location='cpu',weights_only=True)
        self.episodic_net=EpisodicValueNet().eval()
        self.episodic_net.load_state_dict(entry['model'])
        self.history=deque(maxlen=2)
        self.online_level=[]
        self.online_updates=0
        self.counter=Counter()
        self.value_choice_diff=0
        self.max_p_value=0.
        self.model_training_families=tuple(entry['train_families'])
        self._last_features=None
        self.value_diag=[]

    def start_level(self,completed,frame):
        if getattr(self,'level',-1)!=int(completed):
            self.history.clear()
            self.online_level.clear()
        return super().start_level(completed,frame)

    def _values(self,f,acts):
        st=state_features(f,list(self.history),self.since_reset,self.level+1)
        aa=np.stack([candidate_features(f,int(a)) for a in acts]).astype(np.float32)
        ss=np.broadcast_to(st,(len(acts),len(st))).copy()
        with torch.inference_mode():
            v,q=self.episodic_net(torch.from_numpy(ss),torch.from_numpy(aa))
        return st,aa,v.detach().numpy(),q.detach().numpy()

    def choose(self,f,legal):
        f=np.asarray(f,np.uint8)
        # No change whatsoever to Level1 B1 or Level2 local-effect controller.
        if self.level < 2:
            a=int(super().choose(f,legal))
            self._last_features=(state_features(f,list(self.history),self.since_reset-1,self.level+1),candidate_features(f,a))
            return a
        if self.value_mode=='value_state_only':
            # V(s,h) cannot select among actions, because it is invariant across
            # candidate actions at a fixed observation. Genuine null ablation.
            a=int(super().choose(f,legal))
            self._last_features=(state_features(f,list(self.history),self.since_reset-1,self.level+1),candidate_features(f,a))
            self.counter['state_only_no_action_rerank']+=1
            return a
        s=self.node(f,legal);nd=self.nodes[s]
        acts=np.asarray(nd['actions'],dtype=np.int64)
        p=self.puct_probabilities(nd,acts)
        visits=self.puct_state_actions.setdefault(s,{})
        n=np.array([visits.get(int(a),0) for a in acts],dtype=np.float64)
        q,base=self._array_scores(nd,acts,p,n,self.puct_c)
        score=base.copy()
        # Same bounded local-effect ranking as our proven 15-level candidate.
        cutoff=max(48,min(96,int(len(acts)*.15)))
        top=np.argsort(-base,kind='stable')[:min(cutoff,len(acts))]
        tested=np.flatnonzero(n>0)
        near=tested[base[tested]>=base.max()-.045] if len(tested) else tested
        candidate_indices=np.unique(np.concatenate((top,near)))
        if len(candidate_indices)>200:
            candidate_indices=candidate_indices[np.argsort(-base[candidate_indices])[:200]]
        for j in candidate_indices:
            a=int(acts[j]);_,local,_,_,_=self._memory_bonus(f,a,'local')
            score[j]+=local
        frozen_local_action=int(acts[np.argmax(score)])
        st,actfeat,vhat,qhat=self._values(f,acts)
        qhat=np.nan_to_num(qhat,nan=0.0,posinf=0.0,neginf=0.0)
        qhat=np.clip(qhat,0,1)
        untried=n==0
        if self.value_mode=='value_hard':
            # Unsafe direct replacement requested as a falsification control.
            score[untried]+=(qhat[untried]-q[untried])
            self.counter['hard_q_initializations']+=int(untried.sum())
        else:
            # Conservative value prior: preserve nonzero exploration chance
            # and avoid letting near-zero OOD Q completely eliminate actions.
            # Bounded, centered residual on the optimistic Q initialization.
            if np.any(untried):
                values=qhat[untried]
                scale=max(.02,float(np.std(values)))
                score[untried]+=.045*np.clip((values-float(np.mean(values)))/scale,-2.,2.)
        idx=int(np.argmax(score));a=int(acts[idx])
        self.value_choice_diff+=int(a!=frozen_local_action)
        self.max_p_value=max(self.max_p_value,float(qhat[idx]))
        self.counter['value_actions']+=1
        self._last_features=(st,actfeat[idx])
        diag={'level':self.level+1,'mode':self.value_mode,'chosen':a,
              'baseline_argmax':frozen_local_action,'q':float(q[idx]),
              'prior':float(p[idx]),'visits_pre':int(n[idx]),
              'predicted_return':float(qhat[idx]),'state_value':float(vhat[idx]),
              'base_q_optimism':float(q[idx]),'score':float(score[idx]),
              'value_changed_action':bool(a!=frozen_local_action),
              'candidate_count':len(acts),'observed_value_train_only':True}
        self._stage(nd,s,a,f,diag)
        return a

    def _reward_online_update(self):
        if not self.online_level:return
        assert all(r in (0,1) for _,_,r in self.online_level)
        # Only after a *native* level win. No current/future reward leak.
        samples=self.online_level
        if not samples[-1][2]:return
        S=np.stack([entry[0] for entry in samples]).astype(np.float32)
        A=np.stack([entry[1] for entry in samples]).astype(np.float32)
        T=np.array([.985**(len(samples)-1-i) for i in range(len(samples))],np.float32)
        optimizer=torch.optim.AdamW(self.episodic_net.parameters(),lr=.0004,weight_decay=.01)
        self.episodic_net.train()
        for _ in range(2):
            pv,pq=self.episodic_net(torch.from_numpy(S),torch.from_numpy(A))
            y=torch.from_numpy(T)
            loss=(pq-y).square().mean()+.3*(pv-y).square().mean()
            optimizer.zero_grad();loss.backward();optimizer.step()
            self.online_updates+=1
        self.episodic_net.eval()

    def observe(self,f,legal,completed,terminal=False):
        pend=self.pending
        if pend is not None:
            _,a,prev_level,old=pend
            delta=int(np.count_nonzero(np.asarray(f,np.uint8)!=old))
            rewarded=int(completed)>prev_level
            if self._last_features is not None:
                state,action=self._last_features
                self.online_level.append((state,action,int(rewarded)))
            if rewarded and self.value_mode=='value_td_online':
                self._reward_online_update()
            if rewarded or terminal:
                self.history.clear();self.online_level.clear()
            else:self.history.append((int(a),delta))
        return super().observe(f,legal,completed,terminal=terminal)

    def report(self):
        rep=super().report()
        rep.update({'episodic_value_mode':self.value_mode,'level3_value_decision_changes':int(self.value_choice_diff),
                    'online_update_batches':int(self.online_updates),
                    'value_actions':int(self.counter['value_actions']),
                    'state_only_null_actions':int(self.counter['state_only_no_action_rerank']),
                    'unsafe_hard_q_initializations':int(self.counter['hard_q_initializations'])})
        return rep