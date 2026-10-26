"""N112: causal, action-conditional empirical forward dynamics.

The model is FIT on executed native (before, action, after) pairs only. It
never calls an environment and never uses the level's answer as a teacher.
A transition memory is used rather than claiming a CNN trained on a handful
of sparse Level-1 observations has learned general physics.
"""
from dataclasses import dataclass
from collections import defaultdict
import hashlib
import numpy as np

SHAPE=(64,64)

def state_action_key(frame,action):
    return (hashlib.blake2b(np.asarray(frame,np.uint8).tobytes(),digest_size=12).digest(),int(action))


def kind(action:int)->int:
    return 6 if int(action)>=6 else int(action)


def xy(action:int)->tuple[int,int]:
    return ((int(action)-6)%64,(int(action)-6)//64) if action>=6 else (-1,-1)


@dataclass
class Prediction:
    frame:np.ndarray
    confidence:float
    changed:int
    source_index:int
    reason:str


class EmpiricalForward:
    """Finite Level-1 transition-buffer model, with click-relative deltas.

    This is deliberately *not* a privileged simulator. Nearest-neighbour
    retrieval is a learned, imperfect dynamics hypothesis. Unknown actions
    return identity with zero confidence, not fabricated scene changes.
    """
    def __init__(self, min_confidence=.58, max_records=400):
        self.min_confidence=float(min_confidence)
        self.max_records=int(max_records)
        self.records=[]
        self.by_kind=defaultdict(list)
        self.conflicted_pairs=set()

    def fit(self,frames,actions,next_frames, terminal_flags=None):
        self.records=[];self.by_kind=defaultdict(list); self.conflicted_pairs=set()
        outcomes=defaultdict(set)
        if terminal_flags is None:terminal_flags=np.zeros(len(actions),dtype=bool)
        for s,a,t,terminal in zip(frames,actions,next_frames,terminal_flags):
            if terminal:continue  # outgoing frame is a level-transition animation
            s=np.asarray(s,np.uint8);t=np.asarray(t,np.uint8)
            if s.shape!=SHAPE or t.shape!=SHAPE:raise ValueError('Public frames must be 64x64')
            ac=int(a)
            key=state_action_key(s,ac)
            outcomes[key].add(hashlib.blake2b(t.tobytes(),digest_size=12).digest())
            delta=np.where(s!=t)
            ys=delta[0].astype(np.int16);xs=delta[1].astype(np.int16)
            if len(xs)>1024:continue # never replay broad/cinematic transitions
            old=s[ys,xs].copy(); new=t[ys,xs].copy()
            r={'before':s.copy(),'action':ac,'pair_key':key,'xy':xy(ac),'ys':ys,'xs':xs,
               'old':old,'new':new,'thumb':s[::8,::8].copy()}
            self.records.append(r);self.by_kind[kind(ac)].append(len(self.records)-1)
        self.conflicted_pairs={key for key,variants in outcomes.items() if len(variants)>1}
        # Fixed deterministic memory budget: no test-time selection by reward.
        if len(self.records)>self.max_records:
            subset=np.linspace(0,len(self.records)-1,self.max_records,dtype=int)
            old=self.records
            self.records=[old[int(i)] for i in subset]
            self.by_kind=defaultdict(list)
            for j,r in enumerate(self.records):self.by_kind[kind(r['action'])].append(j)
        return self

    def predict(self,frame:np.ndarray,action:int)->Prediction:
        f=np.asarray(frame,np.uint8)
        if f.shape!=SHAPE:raise ValueError('Expected 64x64 public native frame')
        act=int(action); kk=kind(act); candidates=self.by_kind.get(kk,[])
        if state_action_key(f,act) in self.conflicted_pairs:
            return Prediction(f.copy(),0.,0,-1,'ambiguous_exact_transition')
        if not candidates:
            return Prediction(f.copy(),0.,0,-1,'unseen_action')
        best=-1.;choice=None;indexes=None
        thumb=f[::8,::8]
        xx,yy=xy(act)
        for i in candidates:
            r=self.records[i]
            if r['pair_key'] in self.conflicted_pairs:continue
            x0,y0=r['xy'];xs=r['xs'];ys=r['ys']
            if kk==6:
                if x0<0:continue
                dx=xx-x0;dy=yy-y0
                tx=xs+dx;ty=ys+dy
            else:
                tx=xs;ty=ys
            if len(tx) and ((tx<0).any() or (tx>=64).any() or (ty<0).any() or (ty>=64).any()):continue
            local=float(np.mean(f[ty,tx]==r['old'])) if len(tx) else 1.
            coarse=float(np.mean(thumb==r['thumb']))
            # Click effects do not automatically move with the cursor:
            # a source delta far from the source click is not safely portable.
            if kk==6 and len(xs)>0 and np.percentile(np.maximum(abs(xs-x0),abs(ys-y0)),90)>16:
                continue
            score=.72*local+.28*coarse
            if kk!=6 and int(r['action'])!=act:continue
            if score>best:
                best=score;choice=i;indexes=(ty,tx)
        if choice is None or best<self.min_confidence:
            return Prediction(f.copy(),max(0.,best),0,-1,'low_match')
        r=self.records[choice];g=f.copy();ty,tx=indexes
        if len(tx):g[ty,tx]=r['new']
        return Prediction(g,float(best),int(np.count_nonzero(g!=f)),choice,'empirical_delta')


def frame_metrics(true_next, predicted, before):
    t=np.asarray(true_next)!=np.asarray(before)
    p=np.asarray(predicted)!=np.asarray(before)
    tp=int(np.count_nonzero(t&p)); fn=int(np.count_nonzero(t&~p));fp=int(np.count_nonzero(p&~t))
    return dict(tp=tp,fp=fp,fn=fn,correct=int(np.count_nonzero(np.asarray(true_next)==np.asarray(predicted))),total=int(np.asarray(before).size), changed_true=int(np.count_nonzero(t)))


def score_metrics(rows):
    sums={k:sum(r[k] for r in rows) for k in ['tp','fp','fn','correct','total','changed_true']}
    prec=sums['tp']/max(1,sums['tp']+sums['fp']);rec=sums['tp']/max(1,sums['tp']+sums['fn'])
    return {**sums,'pixel_accuracy':sums['correct']/max(1,sums['total']),
            'changed_pixel_precision':prec,'changed_pixel_recall':rec,
            'changed_pixel_f1':2*prec*rec/max(1e-12,prec+rec)}
