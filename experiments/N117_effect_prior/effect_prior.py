"""N117 / effect-prior experiment. Online observed-effect predictions, NO oracle.

The only supervised target is whether a *charged* native action changes public
pixels, or produces a sustained substantial change.  Predictions are never
external rewards. All actions remain available in the soft branches.

This module is game-agnostic: no game identifiers, game sources, absolute
winning paths, future states, or external model training are used by the actor.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import math
import numpy as np
from reference_policy import AuditedCrossLevelCore

MODES = ('soft_any', 'soft_substantial', 'soft_plus_local', 'soft_persistent',
         'hard_substantial', 'repeat_silence', 'soft_shuffled')


def _sigmoid(z):
    return 1. / (1. + np.exp(-np.clip(z, -20., 20.)))


def click_features(frame: np.ndarray, action: int) -> np.ndarray:
    """Palette-invariant, fixed-dimensional action context, from public pixels.

    No component labels, object identities, grid-specific target coordinates,
    decoded source code or hardcoded UI rules.  A clicked action is distinguished
    by local contrast and color-frequency role, not its raw color number.
    """
    f=np.asarray(frame,dtype=np.uint8)
    if f.shape!=(64,64):raise ValueError('64x64 SDK frame required')
    a=int(action)
    v=np.zeros(27,dtype=np.float64)
    v[0]=1.
    if a<6:
        if a<0:raise ValueError(a)
        v[1+a]=1.
        return v
    if a>=4102:raise ValueError(a)
    y,x=divmod(a-6,64)
    v[7]=1.
    v[8]=(x-31.5)/31.5;v[9]=(y-31.5)/31.5
    v[10]=(min(x,63-x)/31.5);v[11]=(min(y,63-y)/31.5)
    v[12]=((x-31.5)**2+(y-31.5)**2)/(2*31.5**2)
    counts=np.bincount(f.ravel(),minlength=256)
    pixel=int(f[y,x]);volume=int(counts[pixel]);mode=int(np.argmax(counts))
    v[13]=float(pixel==mode)
    v[14]=float(volume/4096.)
    v[15]=min(1.,math.log2(volume+1)/12.)
    v[16]=float(volume<=16)
    v[17]=float(volume<=128)
    # Local edge/texture is positional context only, not an object parser.
    y0=max(0,y-2);y1=min(64,y+3);x0=max(0,x-2);x1=min(64,x+3)
    local=f[y0:y1,x0:x1]
    v[18]=float(np.count_nonzero(local!=pixel)/len(local.ravel()))
    v[19]=float(len(np.unique(local))-1)/24.
    v[20]=float(f[max(0,y-1),x]!=pixel)
    v[21]=float(f[min(63,y+1),x]!=pixel)
    v[22]=float(f[y,max(0,x-1)]!=pixel)
    v[23]=float(f[y,min(63,x+1)]!=pixel)
    v[24]=float(y<8 or x<8 or y>=56 or x>=56)
    v[25]=float(16<=x<48 and 16<=y<48)
    v[26]=float((volume>4096//2) and (v[18]<.2))
    return v


class OnlineEffectPredictor:
    """Regularized online logistic model. Exposes confidence/uncertainty.

    Only observed transitions update weights.  Online one-step predictions are
    tracked before training on that observation. Initial predictions 0.5.
    """
    def __init__(self,lr=.18,regularization=.006):
        self.weights=np.zeros(27,dtype=np.float64)
        self.adagrad=np.full(27,0.2,dtype=np.float64)
        self.n=0
        self.lr=float(lr)
        self.reg=float(regularization)
        self.logloss=0.
        self.squared_error=0.
        self.predictions=[]
        self.by_level=Counter()

    def predict_features(self,x):
        return float(_sigmoid(float(np.dot(self.weights,x))))

    def predict(self,f,a):
        return self.predict_features(click_features(f,a))

    def update(self,f,a,changed,level):
        x=click_features(f,a)
        p=self.predict_features(x)
        y=float(bool(changed))
        self.logloss+=float(-y*np.log(max(p,1e-9))-(1-y)*np.log(max(1-p,1e-9)))
        self.squared_error+=(p-y)**2
        self.predictions.append((int(level),round(p,8),int(y),int(a)))
        self.by_level[(int(level),'positive' if y else 'negative')]+=1
        gradient=(p-y)*x+self.reg*self.weights
        self.adagrad+=gradient**2
        self.weights-=self.lr*gradient/(np.sqrt(self.adagrad)+.1)
        self.weights=np.clip(self.weights,-6,6)
        self.n+=1
        return p

    def report(self):
        n=max(1,self.n)
        return {'updates':self.n,'mean_log_loss':round(self.logloss/n,5),
                'brier':round(self.squared_error/n,5),
                'observed_by_level':{str(k):v for k,v in self.by_level.items()}}


class SoftEffectCore(AuditedCrossLevelCore):
    """Frozen L1 and frozen Bellman backups; only L2+ action reranking changes.

    Under hard_substantial, actions are masked only in the experimental hard
    ablation (never in recommended soft branches), with explicit rescue fallback.
    """
    def __init__(self,*args,mode='soft_any',**kwargs):
        if mode not in MODES:raise ValueError(mode)
        super().__init__(*args,mode='local',**kwargs)
        self.mode=mode
        self.predictor=OnlineEffectPredictor()
        self.decisions=0
        self.low_probability_choices=0
        self.hard_exclusions=0
        self.hard_rescues=0
        self.silent_by_exact=defaultdict(lambda:[0,0])
        self.last_predict=None
        self.prev_persistent=None
        self.durable_training=0
        self.changed_choices=0

    def _repeat_data(self, f,a):
        key=(hashlib.blake2s(f.tobytes(),digest_size=10).digest(),int(a))
        silent,total=self.silent_by_exact[key]
        return key,silent,total

    def _memory_bonus(self,frame,a,mode):
        x=click_features(frame,int(a))
        p=self.predictor.predict_features(x)
        confidence=min(1.,self.predictor.n/24.)
        # All modes preserve nonzero probability of actions with low predictions;
        # bonus is to *action score*, never an invented environmental reward.
        effect_bonus=.105*(p-.5)*2.*confidence
        desc,hy,hn,cy,cn=self._stat(frame,a)
        local_n=cy+cn
        local_b=.09*((cy+1)/(local_n+2)-.5)*min(1.,local_n/3.)
        if mode=='soft_any' or mode=='soft_substantial' or mode=='soft_persistent':
            bonus=effect_bonus
        elif mode=='soft_plus_local':
            # Effect probability augments the empirically validated local bonus.
            bonus=local_b+.045*(p-.5)*2.*confidence
        elif mode=='repeat_silence':
            _,silent,total=self._repeat_data(frame,a)
            bonus=local_b-.025*min(2.,silent)*min(1.,total/2.)
        elif mode=='hard_substantial':
            # The full native candidate set remains legal. Hard-masking may
            # force this candidate out of the shortlist, as a negative control.
            bonus=effect_bonus
            if self.predictor.n>=8 and p<.5:
                bonus-=2.
                self.hard_exclusions+=1
        elif mode=='soft_shuffled':
            # A falsification control: action features from next action slot.
            wrong=(int(a)+1)%6 if int(a)<6 else 6+(((int(a)-6)+1057)%4096)
            pseudo=self.predictor.predict(frame,wrong)
            bonus=.105*(pseudo-.5)*2.*confidence
        else:raise ValueError(mode)
        return float(bonus),0.,desc,hy+hn,local_n

    def _hard_choose(self,f,legal):
        """True mask of every N093 candidate, not merely a reranked shortlist.

        Never mask SDK legality: this is a *predictive* policy ablation.
        If the predictor rejects everything, the frozen PUCT winner is used.
        """
        f=np.asarray(f,np.uint8);legal=np.asarray(legal,bool)
        if self.level<1 or not self.puct_enabled:
            return super().choose(f,legal)
        s=self.node(f,legal);nd=self.nodes[s]
        acts=np.asarray(nd['actions'],dtype=np.int64)
        prior=self.puct_probabilities(nd,acts)
        visits=self.puct_state_actions.setdefault(s,{})
        n=np.asarray([visits.get(int(a),0) for a in acts],dtype=np.float64)
        q,base=self._array_scores(nd,acts,prior,n,self.puct_c)
        pred=np.asarray([self.predictor.predict(f,int(a)) for a in acts])
        masked=(pred<.5) if self.predictor.n>=8 else np.zeros(len(acts),dtype=bool)
        self.hard_exclusions+=int(masked.sum())
        scores=base.copy();scores[masked]=-np.inf
        if not np.isfinite(scores).any():
            self.hard_rescues+=1
            scores=base.copy()
        i=int(np.argmax(scores));chosen=int(acts[i]);base_i=int(np.argmax(base))
        self.policy_changed_vs_frozen+=int(chosen!=int(acts[base_i]))
        diag={'level':self.level+1,'mode':self.mode,'chosen':chosen,
              'baseline_argmax':int(acts[base_i]),'candidate_count':len(acts),
              'q':float(q[i]),'prior':float(prior[i]),'puct_bonus':float(base[i]-q[i]),
              'combined':float(scores[i]),'visits_pre':int(n[i]),
              'memory_bonus':0.,'hard_masked':int(masked.sum()),
              'untried_count':int((n==0).sum())}
        return self._stage(nd,s,chosen,f,diag)

    def choose(self,f,legal):
        a=self._hard_choose(f,legal) if self.mode=='hard_substantial' else super().choose(f,legal)
        self.last_predict=(self.level,int(a),float(self.predictor.predict(f,a)),np.asarray(f,np.uint8).copy())
        if self.action_diag:
            self.action_diag[-1]['p_frame_change']=self.last_predict[2]
            self.action_diag[-1]['predictor_updates']=self.predictor.n
        if self.level>=1:
            self.decisions+=1
            self.changed_choices+=int(self.action_diag[-1].get('chosen')!=self.action_diag[-1].get('baseline_argmax'))
            self.low_probability_choices+=int(self.last_predict[2]<.5)
        return a

    def observe(self,f,legal,completed,terminal=False):
        pending=self.pending
        nextf=np.asarray(f,np.uint8)
        if pending is not None:
            _,action,before_level,oldf=pending
            reward=int(completed)>int(before_level)
            delta=int(np.count_nonzero(oldf!=nextf))
            if self.mode=='soft_persistent':
                if self.prev_persistent is not None:
                    old,act,after,lev=self.prev_persistent
                    # Check whether at least 70% of the changed pixel values
                    # survive a further real SDK step within the same level.
                    if int(before_level)==lev and not reward and not terminal:
                        changed=old!=after
                        stable=(nextf[changed]==after[changed]).mean() if changed.any() else 0.
                        durable=bool(changed.sum()>=4 and stable>=.7)
                        self.predictor.update(old,act,durable,lev+1)
                        self.durable_training+=1
                self.prev_persistent=None
                if not reward and not terminal:
                    self.prev_persistent=(oldf.copy(),int(action),nextf.copy(),int(before_level))
            else:
                if not reward and not terminal:
                    positive= (delta>0) if self.mode=='soft_any' else (delta>=4)
                    self.predictor.update(oldf,int(action),positive,int(before_level)+1)
            if self.level>=1 and not reward and not terminal:
                key,silent,total=self._repeat_data(oldf,action)
                self.silent_by_exact[key]=[silent+int(delta==0),total+1]
        return super().observe(f,legal,completed,terminal=terminal)

    def report(self):
        r=super().report()
        r.update({'predictor':self.predictor.report(),'low_probability_chosen':self.low_probability_choices,
                  'hard_mask_exclusions':self.hard_exclusions,'hard_mask_rescues':self.hard_rescues,
                  'altered_choices':self.changed_choices,'durable_trained':self.durable_training})
        return r
