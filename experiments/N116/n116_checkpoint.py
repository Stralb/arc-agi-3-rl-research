"""N116: reward-provenance, false-positive-controlled event checkpointing.

Uses only public frames, action outcomes and the known N106 parser. The native
reward is never replaced by intrinsic reward, and GAME_OVER cannot be reset.
A checkpoint only resets visit-count exploration (not Q, not the environment)
after the same event occurs on two rewarded levels and nowhere in earlier
unrewarded transitions. Every false-negative abstains to the original policy.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable
import numpy as np
from n106_odsl import infer_local_operations


def effect_signatures(before: np.ndarray, after: np.ndarray) -> set[tuple]:
    """N106 local operation signatures, no object-id or absolute coordinates.

    May characterize incidental animation, so a signature is *not* itself proof
    of terminal relevance or causal progress.
    """
    if before.shape != (64,64) or after.shape!=(64,64):
        raise ValueError('expected SDK 64x64 palette frames')
    ops, scene = infer_local_operations(before,after, return_scene=True)
    return {(p.kind, int(scene.objects[p.object_id].color),
             tuple(scene.objects[p.object_id].signature),
             int(p.dx),int(p.dy),None if p.color is None else int(p.color))
            for p in ops}

@dataclass
class CheckpointMonitor:
    """Learn candidate events online, assign native reward *only* to native win."""
    positives: dict[int,set] = field(default_factory=dict)
    negatives: Counter = field(default_factory=Counter)
    negative_steps: Counter = field(default_factory=Counter)
    licensed: set = field(default_factory=set)
    candidate_hits: Counter = field(default_factory=Counter)
    rewarded_events: list = field(default_factory=list)
    checkpoints: int = 0
    parsed: int = 0

    def observe(self,before,after_frame_stack,level_before,level_after):
        if not after_frame_stack:
            raise ValueError('missing actual public SDK observation stack')
        outgoing=np.asarray(after_frame_stack[-1],np.uint8)
        rewarded=int(level_after)>int(level_before)
        if rewarded:
            # the last frame is the new level; do NOT parse a level transition
            if len(after_frame_stack)<2:
                source_event=set()   # abstain without an in-level terminal frame
            else:
                final_pre_advance=np.asarray(after_frame_stack[-2],np.uint8)
                source_event=effect_signatures(np.asarray(before,np.uint8),final_pre_advance)
            self.positives[int(level_before)+1]=source_event
            self.rewarded_events.append({'level':int(level_before)+1,'signature_count':len(source_event)})
            # A rule must work on >=2 independently rewarded levels, and have
            # zero false-positive nonreward appearances during observed data.
            positive_levels=tuple(sorted(self.positives))
            if len(positive_levels)>=2:
                intersection=set.intersection(*(self.positives[k] for k in positive_levels))
                self.licensed={s for s in intersection if self.negatives[s]==0}
            return {'reward':True,'license_count':len(self.licensed),'checkpoint':False,
                    'candidate_count':len(source_event)}
        hits=effect_signatures(np.asarray(before,np.uint8),outgoing)
        self.parsed+=1
        if int(level_before)<2:
            self.negative_steps[int(level_before)+1]+=1
            self.negatives.update(hits)
        if int(level_before)>=2:
            for s in hits:
                if s in self.positives.get(1,set()):
                    self.candidate_hits['L1_raw']+=1
                if s in self.positives.get(2,set()):
                    self.candidate_hits['L2_raw']+=1
            if self.licensed.intersection(hits):
                self.checkpoints+=1
                return {'reward':False,'checkpoint':True,'license_count':len(self.licensed),
                        'candidate_count':len(hits)}
        return {'reward':False,'checkpoint':False,'license_count':len(self.licensed),
                'candidate_count':len(hits)}