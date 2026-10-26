"""Bounded zero-native-call MCTS over a learned, non-oracle forward model."""
from dataclasses import dataclass,field
from collections import Counter
import numpy as np
from n112_forward import EmpiricalForward


@dataclass
class GoalContrast:
    """Histogram of an *observed* Level-1 terminal transition, not a causal goal."""
    counts:np.ndarray
    raw_changes:int

    @classmethod
    def from_native(cls,pre_reward,outgoing_l1):
        a=np.asarray(pre_reward,dtype=np.uint8);b=np.asarray(outgoing_l1,dtype=np.uint8)
        if a.shape!=(64,64) or b.shape!=(64,64):raise ValueError('bad public frame')
        where=a!=b
        h=np.bincount((a[where].astype(np.int64)*16+b[where]).ravel(),minlength=256).astype(float)
        return cls(h,int(where.sum()))

    def score(self,before,after)->float:
        a=np.asarray(before,np.uint8);b=np.asarray(after,np.uint8)
        w=a!=b
        if not self.raw_changes or not w.any():return 0.
        h=np.bincount((a[w].astype(np.int64)*16+b[w]).ravel(),minlength=256).astype(float)
        dot=float(h@self.counts)
        similarity=dot/max(1e-10,float(np.linalg.norm(h)*np.linalg.norm(self.counts)))
        ratio=min(int(w.sum()),self.raw_changes)/max(int(w.sum()),self.raw_changes)
        return float(similarity*np.sqrt(ratio))

@dataclass
class Node:
    frame:np.ndarray
    visits:int=0
    edge_visits:dict=field(default_factory=dict)
    edge_values:dict=field(default_factory=dict)
    children:dict=field(default_factory=dict)


class ModelMCTS:
    """UCT/PUCT MCTS; *all* children are predicted; no environment reference.

    The rollout action vocabulary is the legal, root-observed B1 candidate set.
    Future legalities are not assumed known; the result is a proposal only.
    """
    def __init__(self, model:EmpiricalForward, iterations=256,depth=3,c=.9,
                 minimum_action_confidence=.72, minimum_goal_score=.35):
        self.model=model;self.iterations=int(iterations);self.depth=int(depth)
        self.c=float(c);self.minimum_action_confidence=float(minimum_action_confidence)
        self.minimum_goal_score=float(minimum_goal_score)

    def search(self,root_frame,actions,priors,goal:GoalContrast):
        actions=tuple(dict.fromkeys(int(a) for a in actions))
        if not actions:raise ValueError('Need legal root candidate actions')
        priors=np.asarray(priors,float)
        if len(priors)!=len(actions):raise ValueError('Prior/action mismatch')
        priors=np.maximum(0.,priors);priors=priors/max(1e-12,priors.sum())
        root=Node(np.asarray(root_frame,np.uint8).copy())
        calls=0; predictions=0; confidences=[]; strongest=(0.,[],[])
        n_sim=max(1,self.iterations)
        for _ in range(n_sim):
            cur=root;nodes=[];trail=[];lastframe=root.frame;confs=[]
            for depth in range(self.depth):
                cur.visits+=1
                q=[]
                for a,p in zip(actions,priors):
                    n=cur.edge_visits.get(a,0)
                    mean=cur.edge_values.get(a,0.)/n if n else 0.
                    q.append(mean+self.c*p*np.sqrt(cur.visits)/(1+n))
                i=int(np.argmax(q));a=actions[i]
                nodes.append((cur,a));trail.append(a)
                if a not in cur.children:
                    nxt=self.model.predict(cur.frame,a);calls+=1
                    confs.append(nxt.confidence)
                    confidences.append(nxt.confidence)
                    nxtnode=Node(nxt.frame)
                    cur.children[a]=nxtnode
                    cur=nxtnode
                    break
                cur=cur.children[a]
                confs.append(1.) # visited node's confidence is checked via proposals below
            value=goal.score(root.frame,cur.frame)
            # Safety: penalise unknown model transitions and zero-change hallucinations.
            value*=float(min(confs)) if confs else 0.
            value-=.003*len(trail)
            if value>strongest[0]:strongest=(float(value),list(trail),list(confs))
            for node,a in nodes:
                node.edge_visits[a]=node.edge_visits.get(a,0)+1
                node.edge_values[a]=node.edge_values.get(a,0.)+value
            predictions+=1
        # Exhaustively re-evaluate saved root branch in MODEL only for safety.
        path=strongest[1];frame=root.frame.copy();steps=[];max_score=0.
        for a in path:
            pred=self.model.predict(frame,a);calls+=1
            step={'action':a,'confidence':pred.confidence,'predicted_change':pred.changed,
                  'expected_frame':pred.frame}
            steps.append(step);frame=pred.frame
            max_score=max(max_score,goal.score(root.frame,frame))
        trusted=bool(path and max_score>=self.minimum_goal_score and
                     all(s['confidence']>=self.minimum_action_confidence and s['predicted_change']>0 for s in steps))
        return {'proposed_actions':path,'trusted':trusted,'score':max_score,
                'rollouts':predictions,'model_calls':calls,'expanded_nodes':count_nodes(root),
                'steps':steps,'confidence_stats':{
                    'mean':float(np.mean(confidences)) if confidences else 0.,
                    'min':float(np.min(confidences)) if confidences else 0.}}


def count_nodes(n):
    return 1+sum(count_nodes(c) for c in n.children.values())
