"""N102: observation-only, empirically estimated action-effect signatures.

The mask is NOT a physics oracle. An unknown entry is not False. Every
True/False label follows an *executed legal action* and compares the public
before/after frames. A visually silent action may have altered latent state,
so optional invalidation replaces older measurements with UNKNOWN. Even the
full measurement history is not a sufficient POMDP state in general.

State key: Hash(public frame including level, sorted legal actions + tri-state
empirical effect signature). NO rolling action string or privileged simulator
state is read, no reset action is generated.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import blake2b
import numpy as np
from n101_rta import Action, Observation
from n101_bellman_fixed import BellmanRTAFix

UNKNOWN=-1
NO_CHANGE=0
CHANGED=1


class AffordanceLedger:
    def __init__(self, invalidate_on_silent=True):
        self._table: dict[str,dict[str,int]]={}
        self.invalidate_on_silent=bool(invalidate_on_silent)
        self.paid_probes=0
        self.invalidation_events=0
        self.status_changes=[]

    def mask(self, obs:Observation)->tuple[tuple[str,int],...]:
        known=self._table.get(obs.frame_hash,{})
        return tuple((a.key(),known.get(a.key(),UNKNOWN)) for a in sorted(obs.actions,key=lambda a:a.key()))

    def state_key(self,obs:Observation)->str:
        # action names may contain punctuation: serialize length-prefixed tokens
        # rather than trusting string joining not to collide.
        v=self.mask(obs)
        digest=blake2b(digest_size=16)
        digest.update(obs.frame_hash.encode('ascii'))
        for action,condition in v:
            b=action.encode('utf-8')
            digest.update(len(b).to_bytes(4,'big'))
            digest.update(b)
            digest.update(bytes([condition+1]))
        return digest.hexdigest()

    def record(self,before:Observation,action:Action,after:Observation)->dict:
        if action.key() not in {a.key() for a in before.actions}:
            raise ValueError('Only actually executed, currently legal actions may update mask')
        before_visual=before.frame_hash
        old_key=self.state_key(before)
        before_mask=self.mask(before)
        delta=int(np.count_nonzero(before.frame0 != after.frame0))
        change=CHANGED if delta>0 else NO_CHANGE
        source=self._table.setdefault(before_visual,{})
        # An action can be silent yet update hidden engine state. Its effects
        # on *other* actions are now stale, never magically set to True.
        stale=0
        if self.invalidate_on_silent and delta==0 and before_visual==after.frame_hash:
            for candidate in list(source):
                if candidate!=action.key() and source[candidate]!=UNKNOWN:
                    source[candidate]=UNKNOWN
                    stale+=1
        prev=source.get(action.key(),UNKNOWN)
        source[action.key()]=change
        self.paid_probes+=1
        self.invalidation_events+=int(stale>0)
        new_key=self.state_key(after)
        event={'action':action.key(),'changed_pixels':delta,
               'before_visual':before_visual,'after_visual':after.frame_hash,
               'source_key_before':old_key,'destination_key_after':new_key,
               'mask_before':list(before_mask),'mask_after':list(self.mask(after)),
               'mask_entry_before':prev,'mask_entry_after':change,
               'other_entries_invalidated':stale,'paid_native_action':True}
        self.status_changes.append(event)
        return event


class AffordanceRTA(BellmanRTAFix):
    def __init__(self, heuristic, *, invalidate_on_silent=True,**kwargs):
        super().__init__(heuristic,**kwargs)
        self.affordances=AffordanceLedger(invalidate_on_silent=invalidate_on_silent)
        self.affordance_events=[]

    def _key(self,obs:Observation)->str:
        return self.affordances.state_key(obs)

    def _record_transition(self,after:Observation)->None:
        if self.pending is not None:
            source,before,before_h,action,decision=self.pending
            self.affordance_events.append(self.affordances.record(before,action,after))
        super()._record_transition(after)

    def summary(self):
        result=super().summary()
        result.update(affordance_probes=self.affordances.paid_probes,
                      affordance_invalidation_events=self.affordances.invalidation_events,
                      distinct_effect_signatures=len(self.nodes))
        return result
