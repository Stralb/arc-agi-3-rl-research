"""N119: observation-only native reward eligibility and measured state-return risk.

Uses the complete legal action interface and N093 Bellman updates unchanged.
Only adds bounded Level-2+ action selection bonuses; no phantom native reward,
shadow simulator, privileged frame, static game ID, or native action reset.

The credit term is explicitly associative, not established causal credit.
The recurrence term penalizes observed returns to recent states, NOT all
visually-silent actions. It never hard-masks a legal control.
"""
from __future__ import annotations
from collections import Counter, deque
import hashlib
import math
import numpy as np
from effect_prior import SoftEffectCore

MODES=('delayed_credit','state_return_risk','credit_plus_risk','attribution_placebo')


def frame_digest(f):
    return hashlib.blake2s(np.asarray(f,np.uint8).tobytes(),digest_size=12).digest()


def reward_eligibility(history, reward=True, decay=0.65, maximum=6):
    """Distribute *observed* native level reward over last <=6 descriptor events.

    Returns selection-only retrospective associations, never a Q reward.
    Observations in history are assumed to be in chronological order.
    """
    if not reward:return {}
    out=Counter()
    for i,(desc,visual_delta) in enumerate(reversed(tuple(history)[-maximum:])):
        # Small visual effects may be latent control operations, so do not
        # filter out or upweight actions based on immediate pixel magnitude.
        out[desc] += decay**i
    return {key:min(1.0,float(val)) for key,val in out.items()}


class DelayedCreditCore(SoftEffectCore):
    """Unmodified frozen Level 1 and level-advancement-only Bellman learner."""
    def __init__(self,*args,mode='credit_plus_risk',**kwargs):
        if mode not in MODES:raise ValueError(mode)
        super().__init__(*args,mode='soft_plus_local',**kwargs)
        self.mode=mode
        self.credit=Counter()
        self.recent_actions=deque(maxlen=6)
        self.recent_frames=deque(maxlen=14)
        self.cycle_effects=Counter()
        self.cycle_counts=Counter()
        self.cycle_total=0
        self.cycle_activations=0
        self.reward_associations=0
        self.extra_choice_count=0
        self.last_choice_extra=0.
        self.credit_probes=Counter()
        self.cycle_log=[]

    def start_level(self,completed,frame):
        old_level=getattr(self,'level',-1)
        if old_level!=completed:
            if old_level>=0 and int(completed)>old_level:
                for k in list(self.credit):
                    self.credit[k]*=.70
                    if self.credit[k]<1.e-4:del self.credit[k]
            elif old_level>=0 and int(completed)<old_level:
                self.credit.clear()
            self.recent_actions.clear()
            self.recent_frames.clear()
            self.cycle_effects.clear()
            self.cycle_counts.clear()
            self.recent_frames.append(frame_digest(frame))
        return super().start_level(completed,frame)

    def _return_penalty(self,frame,desc):
        n=int(self.cycle_counts[desc])
        if n<2:return 0.
        repeats=int(self.cycle_effects[desc])
        # Beta regularization; avoid using guessed physical counterfactuals.
        p=(repeats+1)/(n+2)
        familiarity=sum(z==frame_digest(frame) for z in self.recent_frames)
        # Penalize documented recurrent loops more aggressively when currently
        # stuck in a seen state, but never suppress low-p actions entirely.
        amplification=(1.0 if familiarity>=2 else .50)
        return -.09*max(0.,p-.25)*min(1.,n/4.)*amplification

    def _memory_bonus(self,frame,a,mode):
        # Controlled copy of the proven 15-level N117 soft-plus-local policy.
        soft,local,desc,past_n,current_n=super()._memory_bonus(frame,a,'soft_plus_local')
        credit=0.;risk=0.
        if mode in ('delayed_credit','credit_plus_risk','attribution_placebo'):
            lookup=desc
            if mode=='attribution_placebo':
                # Deterministic treatment-control permutation, no future data.
                a=int(a)
                surrogate=((a+1)%6 if a<6 else 6+((a-6+1097)%4096))
                lookup=self.beliefs.describe(frame,surrogate)
            credit=.055*min(1.,float(self.credit[lookup]))
        if mode in ('state_return_risk','credit_plus_risk','attribution_placebo'):
            lookup=desc
            if mode=='attribution_placebo':
                a=int(a)
                surrogate=((a+1)%6 if a<6 else 6+((a-6+1097)%4096))
                lookup=self.beliefs.describe(frame,surrogate)
            risk=self._return_penalty(frame,lookup)
        return float(soft+credit+risk),float(local),desc,past_n,current_n

    def choose(self,f,legal):
        a=int(super().choose(f,legal))
        if self.level>=1:
            desc=self.beliefs.describe(np.asarray(f,np.uint8),a)
            c=.055*min(1.,float(self.credit[desc])) if 'credit' in self.mode or self.mode=='attribution_placebo' else 0.
            r=self._return_penalty(f,desc) if 'risk' in self.mode or self.mode=='attribution_placebo' else 0.
            self.action_diag[-1]['reward_association_bonus']=float(c)
            self.action_diag[-1]['measured_recurrence_penalty']=float(r)
            self.action_diag[-1]['cycle_samples']=int(self.cycle_counts[desc])
            self.action_diag[-1]['credit_evidence']=float(self.credit[desc])
            self.extra_choice_count+=int(a!=self.action_diag[-1].get('baseline_argmax'))
            self.last_choice_extra=c+r
        return a

    def observe(self,f,legal,completed,terminal=False):
        pending=self.pending
        if pending is not None:
            _,a,before_level,oldf=pending
            desc=self.beliefs.describe(oldf,int(a))
            new_level=int(completed)
            rew=new_level>int(before_level)
            delta=int(np.count_nonzero(np.asarray(f,np.uint8)!=oldf))
            # Last-action history contains no future transitions. The native
            # reward event arrives only AFTER executing the charged action.
            self.recent_actions.append((desc,delta))
            if rew:
                credits=reward_eligibility(self.recent_actions,True)
                for k,value in credits.items():
                    self.credit[k]+=value
                self.reward_associations+=len(credits)
            elif not terminal:
                after=frame_digest(f);before=frame_digest(oldf)
                # Important: nonzero-change return to a recently observed
                # frame, excludes immediate visually silent action. This is a
                # different mechanism from N117's no-op predictor.
                revisit=int(after!=before and after in self.recent_frames)
                self.cycle_counts[desc]+=1
                self.cycle_effects[desc]+=revisit
                self.cycle_total+=revisit
                if revisit:self.cycle_activations+=1
                self.cycle_log.append((int(before_level)+1,int(a),int(revisit),delta))
                self.recent_frames.append(after)
        return super().observe(f,legal,completed,terminal=terminal)

    def report(self):
        r=super().report()
        r.update({'n119_mode':self.mode,
                  'reward_associated_descriptors':int(self.reward_associations),
                  'known_return_to_prior_frame_events':int(self.cycle_total),
                  'candidate_choice_changes_vs_frozen':int(self.extra_choice_count),
                  'credit_descriptors':len(self.credit),
                  'recurrence_descriptor_support':len(self.cycle_counts)})
        return r