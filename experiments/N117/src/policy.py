"""Action-selection ablations atop the immutable N093 source.

Only selects from N093 legal/candidate actions.  No game identity, privileged
lookahead, source semantics, or pseudo native rewards.  B1 Q backups untouched.
"""
from __future__ import annotations
from collections import Counter,deque
from dataclasses import dataclass
import numpy as np
from submission import PretrainedPUCTCore

MODES = ('baseline','transfer','local','combined','curiosity','curiosity_no_risk','pixel_novelty','random_novelty','skill','local_any_pixel','local_shuffled')


class AuditedCrossLevelCore(PretrainedPUCTCore):
    def __init__(self, *args, mode='baseline', **kwargs):
        if mode not in MODES: raise ValueError(mode)
        super().__init__(*args,**kwargs)
        self.mode=mode
        self.action_diag=[]
        self.final_records=[]
        self.level_stats=Counter()
        self.effect_history=deque(maxlen=4)
        self.history_by_action=Counter()
        self.action_outcomes=Counter()
        self.visible_changes=Counter()
        self.visible_totals=Counter()
        self.skill_remaining=0
        self.skill_action=None
        self.skill_used=0
        self.skill_stops=Counter()
        self.option_attempts=0
        self.policy_changed_vs_frozen=0
        self.risk_avoidances=0

    def start_level(self,completed,frame):
        if getattr(self,'level',-1)!=completed:
            if hasattr(self,'effect_history'):
                self.effect_history.clear()
                self.visible_changes.clear()
                self.visible_totals.clear()
                self.skill_remaining=0
                self.skill_action=None
        return super().start_level(completed,frame)

    @staticmethod
    def _array_scores(nd,acts,p,n,c):
        q=np.asarray([nd['q'][int(a)] for a in acts],dtype=np.float64)
        return q,q+c*p/(1+n)

    def _stat(self,frame,a):
        desc=self.beliefs.describe(frame,int(a))
        historic=self.beliefs.past.get(desc)
        current=self.beliefs.current.get(desc)
        hy=historic.yes if historic is not None else 0
        hn=historic.no if historic is not None else 0
        cy=current.yes if current is not None else 0
        cn=current.no if current is not None else 0
        return desc,hy,hn,cy,cn

    def _memory_bonus(self,frame,a,mode):
        desc,hy,hn,cy,cn=self._stat(frame,a)
        past_n=hy+hn; current_n=cy+cn
        pt=(hy+1)/(past_n+2)
        pc=(cy+1)/(current_n+2)
        confidence_past=min(1.0,past_n/3.)
        confidence_current=min(1.0,current_n/3.)
        transfer=0.07*(pt-.5)*confidence_past
        local=0.09*(pc-.5)*confidence_current
        if mode=='local_any_pixel':
            any_n=self.visible_totals[desc]
            any_yes=self.visible_changes[desc]
            rate=(any_yes+1)/(any_n+2)
            return 0.,0.09*(rate-.5)*min(1.0,any_n/3.),desc,past_n,any_n
        if mode=='local_shuffled':
            # Deliberately break descriptor-to-outcome attribution as a control.
            # For primitive controls, use the next different primitive's data.
            surrogate=((int(a)+1)%6 if int(a)<6 else int(a))
            wrong=self.beliefs.describe(frame,surrogate)
            ev=self.beliefs.current.get(wrong)
            ny,nno=(ev.yes,ev.no) if ev is not None else (0,0)
            wrong_n=ny+nno
            rate=(ny+1)/(wrong_n+2)
            return 0.,0.09*(rate-.5)*min(1.0,wrong_n/3.),wrong,past_n,wrong_n
        if mode=='transfer': return transfer,0.,desc,past_n,current_n
        if mode=='local': return 0.,local,desc,past_n,current_n
        if mode in ('combined','skill'):
            return transfer,local,desc,past_n,current_n
        if mode in ('curiosity','curiosity_no_risk'):
            # How uncertain is the effect class? No proxy reward is fed to Q.
            n=past_n*.25+current_n
            uncertainty=1.0/(1.0+n/2.)
            # Preserve stronger effect evidence and do not penalize silent actions.
            novelty=0.015*uncertainty
            risk=0.0
            if mode=='curiosity':
                # Repeated, empirically silent *descriptor* after limited retries.
                recent_same_silent=sum(int(d==desc and not delta) for d,delta in self.effect_history)
                risk=0.025*max(0,recent_same_silent-1)
            return novelty-risk,0.,desc,past_n,current_n
        if mode=='pixel_novelty':
            # Objective is class-level changed-pixel frequency, not a native reward.
            rate=(cy+1)/(current_n+2)
            return 0.025*(rate-.5),0.,desc,past_n,current_n
        if mode=='random_novelty':
            # Selection-only random exploration, seeded separately by same policy RNG.
            return float(self.rng.uniform(0,.023)),0.,desc,past_n,current_n
        return 0.,0.,desc,past_n,current_n

    def _stage(self,nd,s,a,frame,diagnostic):
        # Exactly the same accounting and PUCT-state updates as N093.
        nd['visits']+=1
        visits=self.puct_state_actions.setdefault(s,{})
        if visits.get(a,0)>0:self.puct_revisits+=1
        visits[a]=visits.get(a,0)+1
        self.puct_choices+=1
        self.pending=(s,a,int(self.level),frame.copy())
        self.since_reset+=1
        self.sdk_actions+=1
        if nd['visits']%80==0:self._expand(s)
        self.action_diag.append(diagnostic)
        return a

    def choose(self,f,legal):
        f=np.asarray(f,np.uint8);legal=np.asarray(legal,bool)
        if self.level<1 or not self.puct_enabled:
            # Retain byte-for-byte B1 behavior on Level 1.
            a=super().choose(f,legal)
            self.action_diag.append({'level':self.level+1,'mode':'frozen_L1','chosen':int(a)})
            return a
        s=self.node(f,legal);nd=self.nodes[s]
        acts=np.asarray(nd['actions'],dtype=np.int64)
        p=self.puct_probabilities(nd,acts)
        visits=self.puct_state_actions.setdefault(s,{})
        n=np.array([visits.get(int(a),0) for a in acts],dtype=np.float64)
        q,base=self._array_scores(nd,acts,p,n,self.puct_c)
        base_i=int(np.argmax(base));base_action=int(acts[base_i]);base_score=float(base[base_i])
        # Frozen baseline direct path: no candidate priors or stochasticity changed.
        if self.mode=='baseline':
            i=base_i
            chosen=int(acts[i])
            diag={'level':self.level+1,'mode':self.mode,'chosen':chosen,
                  'baseline_argmax':base_action,'candidate_count':len(acts),
                  'q':float(q[i]),'prior':float(p[i]),'puct_bonus':float(base[i]-q[i]),
                  'combined':float(base[i]),'visits_pre':int(n[i]),'memory_bonus':0.,
                  'past_n':0,'current_n':0,'prior_rank':int(np.argsort(-p).tolist().index(i))+1,
                  'untried_count':int((n==0).sum()),'q_untried_optimism':float((q[n==0]==1).mean()) if (n==0).any() else 0}
            return self._stage(nd,s,chosen,f,diag)
        if self.mode=='skill' and self.skill_remaining>0:
            action=int(self.skill_action)
            if action in nd['q'] and self._legal_encoded(action,legal):
                j=int(np.flatnonzero(acts==action)[0]);self.skill_remaining-=1;self.skill_used+=1
                diag={'level':self.level+1,'mode':self.mode,'driver':'observed_event_skill',
                      'chosen':action,'baseline_argmax':base_action,'candidate_count':len(acts),
                      'q':float(q[j]),'prior':float(p[j]),'puct_bonus':float(base[j]-q[j]),
                      'combined':float(base[j]),'visits_pre':int(n[j]),'memory_bonus':0.,
                      'past_n':0,'current_n':0,'skill_remaining':int(self.skill_remaining)}
                return self._stage(nd,s,action,f,diag)
            self.skill_stops['illegal_or_absent']+=1
            self.skill_remaining=0;self.skill_action=None
        # N093 already generates the observable candidate menu. Re-rank the
        # best 48 baseline options, plus previously tried options with only a
        # modest Q penalty. No absolute clicked coordinates are transferred.
        cutoff=max(48,min(96,int(len(acts)*.15)))
        top=np.argsort(-base,kind='stable')[:min(cutoff,len(acts))]
        tested=np.flatnonzero(n>0)
        near=tested[base[tested]>=base_score-.045] if len(tested) else tested
        candidate_indices=np.unique(np.concatenate((top,near)))
        if len(candidate_indices)>200:
            candidate_indices=candidate_indices[np.argsort(-base[candidate_indices])[:200]]
        scores=base.copy()
        # unexamined actions retain frozen base scores, no fabricated evidence.
        extras={}
        for j in candidate_indices:
            a=int(acts[j]);b1,b2,desc,past_n,current_n=self._memory_bonus(f,a,self.mode)
            scores[j]+=b1+b2
            extras[j]=(float(b1+b2),past_n,current_n,desc)
        i=int(np.argmax(scores))
        action=int(acts[i])
        bonus,past_n,current_n,desc=extras.get(i,(0.,0,0,None))
        self.policy_changed_vs_frozen+=int(action!=base_action)
        if self.mode=='curiosity' and action!=base_action and bonus<0:self.risk_avoidances+=1
        # event-conditioned short skill: only after prior repeated positive
        # *action effect*, then confirm the first Level2 step changed frame.
        if self.mode=='skill' and self.skill_remaining==0:
            desc,hy,hn,cy,cn=self._stat(f,action)
            if hy>=2 and hy/(hy+hn)>.75:
                self.skill_action=action
                self.option_attempts+=1
                # The first action must be observed before committing repetition.
        diag={'level':self.level+1,'mode':self.mode,'driver':'adjusted_score',
              'chosen':action,'baseline_argmax':base_action,'candidate_count':len(acts),
              'q':float(q[i]),'prior':float(p[i]),'puct_bonus':float(base[i]-q[i]),
              'combined':float(scores[i]),'visits_pre':int(n[i]),'memory_bonus':float(bonus),
              'past_n':past_n,'current_n':current_n,
              'untried_count':int((n==0).sum()),
              'base_gap':float(base_score-base[i]),'shortlist':int(len(candidate_indices))}
        return self._stage(nd,s,action,f,diag)

    @staticmethod
    def _legal_encoded(a,legal):
        return (0<=a<6 and bool(legal[[0,1,2,3,4,6][a]])) or (6<=a<4102 and bool(legal[5]))

    def observe(self,f,legal,completed,terminal=False):
        old_pending=self.pending
        if old_pending is not None:
            _,a,before_level,old_frame=old_pending
            next_image=np.asarray(f,np.uint8)
            delta=int(np.count_nonzero(old_frame!=next_image))
            desc=self.beliefs.describe(old_frame,a)
            if self.level>=1:
                self.effect_history.append((desc,delta>0))
                self.visible_totals[desc]+=1
                self.visible_changes[desc]+=int(delta>0)
                self.action_outcomes[(self.level+1, 'changed' if delta else 'silent')]+=1
                # Skill proposal is from Level 1 recurrent effect evidence.
                if self.mode=='skill' and self.skill_action==a:
                    if terminal or int(completed)>before_level or not delta:
                        self.skill_remaining=0;self.skill_action=None
                        self.skill_stops['terminal_or_no_delta']+=1
                    elif self.skill_remaining==0 and self.action_diag[-1].get('driver')!='observed_event_skill':
                        self.skill_remaining=2
                    elif self.action_diag[-1].get('driver')=='observed_event_skill' and self.skill_remaining==0:
                        self.skill_action=None
                        self.skill_stops['max_two_repeats']+=1
            if self.action_diag:
                self.action_diag[-1]['visual_delta']=delta
                self.action_diag[-1]['native_reward']=int(completed>before_level)
                self.action_diag[-1]['native_terminal']=bool(terminal)
        return super().observe(f,legal,completed,terminal=terminal)

    def report(self):
        return {'mode':self.mode,'changed_vs_frozen_state_choice':self.policy_changed_vs_frozen,
                'skill_actions':self.skill_used,'skill_attempts':self.option_attempts,
                'skill_stops':dict(self.skill_stops),'risk_rejections':self.risk_avoidances,
                'effect_actions':{str(k):v for k,v in self.action_outcomes.items()},
                'level_choices':dict(Counter(d.get('level') for d in self.action_diag)),
                'bellman_updates':self.num_updates}
