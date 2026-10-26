"""N113 candidate selector: Level-3-only ablations of frozen N093 PUCT.

No game-ID dispatch, no baked action coordinates, no oracle or environment source.
This module imports the frozen portable RL agent only from user-supplied source root.
"""
from __future__ import annotations
from collections import Counter
import numpy as np

GAMMA = 0.985


def boost_action_probs(probs, actions, inherited, factor=10.0):
    """Renormalize observed PUCT priors over the same legal candidates."""
    p=np.asarray(probs,dtype=np.float64).copy()
    a=np.asarray(actions,dtype=np.int64)
    if len(p)!=len(a) or not len(p):raise ValueError('action/probability size mismatch')
    if factor < 1 or not np.isfinite(factor):raise ValueError('invalid boost factor')
    if not np.all(np.isfinite(p)) or np.any(p<0) or p.sum()<=0:raise ValueError('invalid probabilities')
    if inherited:
        p[np.isin(a,list(inherited))]*=factor
    return p/p.sum()


def topk_mask(probs,k):
    p=np.asarray(probs,dtype=np.float64)
    if len(p)==0 or k<1:raise ValueError('empty priors or invalid k')
    order=np.argsort(-p,kind='stable')
    out=np.zeros(len(p),dtype=bool)
    out[order[:min(k,len(p))]]=True
    return out


def delta_shaping(old_gap,new_gap,scale=.5,extent=64):
    """Requested observed gap-reduction reward; never confused with SDK reward."""
    if old_gap is None or new_gap is None:return 0.
    if not (np.isfinite(old_gap) and np.isfinite(new_gap)):return 0.
    old=np.clip(float(old_gap),0,extent)
    new=np.clip(float(new_gap),0,extent)
    return float(scale*(old-new)/extent)


class _StatsMixin:
    """Initializer + methods mixed into N093 Core at runtime by build_core_class."""
    def __init__(self,*args,prune_top_k=0,inherit_boost=1.,shape_scale=0.,**kwargs):
        super().__init__(*args,**kwargs)
        self.prune_top_k=int(prune_top_k)
        self.inherit_boost=float(inherit_boost)
        self.shape_scale=float(shape_scale)
        if self.prune_top_k<0 or self.inherit_boost<1 or self.shape_scale<0:
            raise ValueError('invalid N113 setting')
        self.inherited_actions=set()
        self.goal_ast=None
        self.n113_stats=Counter()
        self.n113_first_l3=None
        self.n113_coverage=[]
        self._shaping_bonus=0.

    def configure_level3(self,l2_winning_actions,goal_ast):
        # Only factual, executed, pre-reward Level-2 actions: no oracle replay.
        self.inherited_actions={int(x) for x in l2_winning_actions}
        self.goal_ast=goal_ast
        self.n113_stats['inherited_distinct']=len(self.inherited_actions)

    def node(self,f,legal):
        key=super().node(f,legal)
        if self.level==2 and self.inherit_boost>1. and self.inherited_actions:
            nd=self.nodes[key]
            for action in sorted(self.inherited_actions):
                legal_index=5 if action>=6 else (0,1,2,3,4,6)[action]
                if bool(legal[legal_index]) and action not in nd['q']:
                    # Actual native Level-2 actions remain SDK-legal controls;
                    # expose them to the SAME Q/PUCT selector, no forced replay.
                    nd['actions'].append(action)
                    nd['q'][action]=1.
                    self.n113_stats['inherited_candidates_admitted']+=1
        return key

    def puct_probabilities(self,nd,acts):
        p=super().puct_probabilities(nd,acts)
        if self.level==2 and self.inherit_boost>1. and self.inherited_actions:
            self.n113_stats['prior_boost_calls']+=1
            self.n113_stats['prior_boost_candidate_matches']+=int(np.isin(acts,list(self.inherited_actions)).sum())
            p=boost_action_probs(p,acts,self.inherited_actions,self.inherit_boost)
        return p

    def choose(self,f,legal):
        # Critical: Levels 1 and 2 use frozen N093 exactly, with no new randomness.
        if self.level<2 or self.prune_top_k==0:
            action=super().choose(f,legal)
            if self.level==2:
                self.n113_stats['level3_actions']+=1
                if self.n113_first_l3 is None:self.n113_first_l3=int(action)
            return action
        f=np.asarray(f,np.uint8);legal=np.asarray(legal,bool)
        s=self.node(f,legal);nd=self.nodes[s]
        nd['visits']+=1
        acts=np.asarray(nd['actions'],dtype=np.int64)
        q=np.asarray([nd['q'][int(a)] for a in acts],dtype=np.float64)
        p=self.puct_probabilities(nd,acts)
        keep=topk_mask(p,self.prune_top_k)
        visits=self.puct_state_actions.setdefault(s,{})
        n=np.asarray([visits.get(int(a),0) for a in acts],dtype=np.float64)
        score=q+self.puct_c*p/(1.+n)
        score[~keep]=-np.inf
        i=int(np.argmax(score));a=int(acts[i])
        self.n113_stats['topk_calls']+=1
        self.n113_stats['topk_rejected_candidates']+=len(acts)-int(keep.sum())
        self.n113_stats['topk_q_masked_better']+=int(np.max(q[~keep])>np.max(q[keep])) if (~keep).any() else 0
        if visits.get(a,0)>0:self.puct_revisits+=1
        visits[a]=visits.get(a,0)+1
        self.puct_choices+=1
        self.pending=(s,a,int(self.level),f.copy())
        self.since_reset+=1;self.sdk_actions+=1
        if nd['visits']%80==0:self._expand(s)
        self.n113_stats['level3_actions']+=1
        if self.n113_first_l3 is None:self.n113_first_l3=a
        return a

    def observe(self,f,legal,completed,terminal=False):
        self._shaping_bonus=0.
        if self.level==2 and self.pending is not None and self.shape_scale>0 and self.goal_ast is not None:
            try:
                from n097.anchor import find_pair
                old=self.pending[3]
                oldpair=find_pair(old,self.goal_ast,self.mask)
                newpair=find_pair(np.asarray(f,np.uint8),self.goal_ast,self.mask)
                if oldpair is not None and newpair is not None and int(completed)==self.level:
                    self._shaping_bonus=delta_shaping(oldpair['gap'],newpair['gap'],self.shape_scale)
                    self.n113_stats['shape_eligible']+=1
                    if abs(self._shaping_bonus)>1e-10:self.n113_stats['shape_nonzero']+=1
                    if newpair['gap']<oldpair['gap']:self.n113_stats['shape_gap_reduced']+=1
                else:
                    self.n113_stats['shape_unavailable']+=1
            except (ValueError,TypeError,KeyError):
                self.n113_stats['shape_unavailable']+=1
        ret=super().observe(f,legal,completed,terminal=terminal)
        self._shaping_bonus=0.
        return ret

    def _observe_q(self,s,a,ns,r,terminal):
        native_r=float(r)
        shaped=native_r+self._shaping_bonus
        if abs(self._shaping_bonus)>1e-10:
            self.n113_stats['shape_total_abs_x100000']+=int(round(abs(self._shaping_bonus)*100000))
        return super()._observe_q(s,a,ns,shaped,terminal)


def build_core_class(frozen_cls):
    return type('N113AmplifiedCore',(_StatsMixin,frozen_cls),{})
