"""History-conditioned, game-independent online action-effect model.

All training labels come from *charged, previously observed* native SDK actions.
No game IDs, objects, hidden dynamics, oracle frames, rewards as proxy labels or
source-code-dependant interface mechanics.  All legal actions remain selectable.
"""
from __future__ import annotations
import math
from collections import Counter, deque
import numpy as np
from reference_policy import AuditedCrossLevelCore
from effect_prior import click_features, OnlineEffectPredictor, _sigmoid

MODES=('temporal_nohistory','temporal_history','temporal_corrupt')
N_BASE=27
N_EXTRA=18


def _group(action):
    action=int(action)
    if action<0 or action>=4102:raise ValueError(action)
    return action if action<6 else 6


def history_features(history, action, mode):
    """Never use future info, source-specific features or absolute past coords.

    Distinguish the previous action's type, its effect magnitude, a repeated
    action, a transition in control type, and the two-step change history.
    Ablation eliminates all history; falsification reverses the observed
    action/effect categories, preserving all marginal update counts.
    """
    v=np.zeros(N_EXTRA,dtype=np.float64)
    if mode=='temporal_nohistory' or not history:return v
    prev=history[-1]
    grp,delta,prev_action,run=prev
    curr=_group(action)
    bucket=0 if delta==0 else (1 if delta<=3 else 2)
    prior_bucket=0
    if len(history)>=2:
        prior=history[-2][1]
        prior_bucket=0 if prior==0 else (1 if prior<=3 else 2)
    if mode=='temporal_corrupt':
        # Current-action-derived placebo: no information about the actual
        # preceding native action or its visual outcome. Unlike a fixed
        # permutation of the true history, this cannot be inverted to recover
        # historical information. It remains a learned feature control.
        grp=(curr+3)%7
        bucket=(curr+1)%3
        prior_bucket=(curr+2)%3
    v[0:7]=0.
    v[grp]=1.
    v[7+bucket]=1.
    v[10+prior_bucket]=1. if len(history)>=2 else 0.
    if mode!='temporal_corrupt':
        v[13]=float(int(prev_action)==int(action))
        v[14]=float(curr==grp)
        v[15]=min(1.,float(run)/4.)
        v[16]=min(1.,math.log1p(delta)/math.log1p(4096.))
    v[17]=1. if len(history)>=2 else 0.
    return v


def temporal_features(frame,action,history,mode):
    return np.concatenate((click_features(frame,int(action)),
                           history_features(history,action,mode)))


class TemporalLogit(OnlineEffectPredictor):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.weights=np.zeros(N_BASE+N_EXTRA,dtype=np.float64)
        self.adagrad=np.full(N_BASE+N_EXTRA,0.2,dtype=np.float64)
    def train_features(self,x,observed,level):
        x=np.asarray(x,np.float64)
        assert x.shape==(N_BASE+N_EXTRA,)
        p=self.predict_features(x)
        y=float(observed)
        self.logloss+=float(-y*np.log(max(p,1e-9))-(1-y)*np.log(max(1-p,1e-9)))
        self.squared_error+=(p-y)**2
        self.predictions.append((int(level),round(p,8),int(y)))
        self.by_level[(int(level),'positive' if y else 'negative')]+=1
        gradient=(p-y)*x+self.reg*self.weights
        self.adagrad+=gradient**2
        self.weights-=self.lr*gradient/(np.sqrt(self.adagrad)+.1)
        np.clip(self.weights,-6,6,out=self.weights)
        self.n+=1
        return p


class TemporalEffectCore(AuditedCrossLevelCore):
    """N093 frozen Level 1, untouched native Bellman updates, soft L2+ ranking.

    Native rewards advance only via core.observe. Each prediction is computed
    from observation history available *before* the charged SDK action.
    """
    def __init__(self,*args,mode='temporal_history',**kwargs):
        if mode not in MODES:raise ValueError(mode)
        super().__init__(*args,mode='local',**kwargs)
        self.temporal_mode=mode
        self.predictor=TemporalLogit()
        self.recent=deque(maxlen=2)
        self._feature_at_action=None
        self.temporal_qualified=0
        self.temporal_choice_diff=0
        self.temporal_exposure=Counter()
        self.temporal_delta_log=[]
        self.temporal_last_action=None
        self.temporal_run=0

    def _memory_bonus(self,frame,a,mode):
        _,local,desc,past_n,current_n=super()._memory_bonus(frame,a,'local')
        x=temporal_features(frame,int(a),self.recent,self.temporal_mode)
        p=self.predictor.predict_features(x)
        confidence=min(1.,self.predictor.n/24.)
        # Same effect-prior amplitude and local evidence as the existing
        # successful soft_plus_local controller: isolates history features.
        bonus=.045*(p-.5)*2.*confidence
        return float(bonus),float(local),desc,past_n,current_n

    def choose(self,f,legal):
        # Same feature generator for all modes.  Use the exact context present
        # when this action was selected, never recompute after observing it.
        a=int(super().choose(f,legal))
        x=temporal_features(f,a,self.recent,self.temporal_mode)
        pred=self.predictor.predict_features(x)
        self._feature_at_action=x
        if self.action_diag:
            self.action_diag[-1]['prequential_p_substantial']=float(pred)
            self.action_diag[-1]['temporal_mode']=self.temporal_mode
            self.action_diag[-1]['history_len']=len(self.recent)
            self.action_diag[-1]['online_fit_count']=self.predictor.n
        if self.level>=1:
            self.temporal_exposure['l2plus_choices']+=1
            self.temporal_choice_diff+=int(self.action_diag[-1]['chosen']!=self.action_diag[-1]['baseline_argmax'])
        return a

    def observe(self,f,legal,completed,terminal=False):
        pending=self.pending
        if pending is not None:
            _,a,before_level,oldf=pending
            nxt=np.asarray(f,np.uint8)
            delta=int(np.count_nonzero(oldf!=nxt))
            reward=int(completed)>int(before_level)
            if not reward and not terminal:
                assert self._feature_at_action is not None
                p=self.predictor.train_features(self._feature_at_action,int(delta>=4),int(before_level)+1)
                self.temporal_exposure['prequential_predictions']+=1
                if int(before_level)>=1:
                    self.temporal_exposure['prequential_level2plus']+=1
                self.temporal_delta_log.append([int(before_level)+1,float(p),int(delta>=4),delta])
            if reward or terminal:
                self.recent.clear();self.temporal_run=0;self.temporal_last_action=None
            else:
                self.temporal_run=(self.temporal_run+1) if int(a)==self.temporal_last_action else 1
                self.temporal_last_action=int(a)
                self.recent.append((_group(a),delta,int(a),self.temporal_run))
            self._feature_at_action=None
        return super().observe(f,legal,completed,terminal=terminal)

    def report(self):
        d=super().report()
        d.update({'temporal_mode':self.temporal_mode,'temporal_predictor':self.predictor.report(),
                  'history_decision_count':self.temporal_choice_diff,
                  'history_action_counts':dict(self.temporal_exposure)})
        return d