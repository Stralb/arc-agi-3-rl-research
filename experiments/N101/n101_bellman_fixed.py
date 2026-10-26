"""N101 RTA code repair: stable visual state, complete-action Bellman backups.

This is an online *observed-graph* LRTA*-like search diagnostic. A frame hash
is NOT a guaranteed Markov state when silent latent prerequisites exist.
The controller does not use reset, game IDs, oracle actions or environment code.
"""
from __future__ import annotations
from collections import defaultdict, deque
from math import inf, isfinite
import numpy as np
from n101_rta import ZeroResetRTA, Action, Observation, Edge


class BellmanRTAFix(ZeroResetRTA):
    def __init__(self, heuristic, *, configuration=None, action_prior_gains=None,
                 enable_backups=True, max_propagations=256):
        super().__init__(heuristic, configuration=configuration,
                         action_prior_gains=action_prior_gains)
        self.enable_backups = enable_backups
        self.max_propagations = max_propagations
        self.legal_at: dict[str, set[str]] = {}
        self.predecessors: dict[str, set[str]] = defaultdict(set)
        self.terminal_nodes: set[str] = set()
        self.ambiguous_nodes: set[str] = set()
        self.backup_events: list[dict] = []
        self.backup_diagnostics = dict(incomplete=0, aliased=0, fixed_point=0,
                                       backup_calls=0, propagation_truncated=0)

    def _key(self, obs: Observation) -> str:
        # A stable visible-state identifier (no rolling action-history digest).
        # Repeat visits now share the same Bellman value. If history-dependent
        # outcomes are observed we flag the aliased node and withhold its update.
        return obs.frame_hash

    def observe(self, obs: Observation) -> None:
        super().observe(obs)
        key = self._key(obs)
        legal = {a.key() for a in obs.actions if a.name.upper() != 'RESET'}
        previously = self.legal_at.get(key)
        if previously is not None and previously != legal:
            self.ambiguous_nodes.add(key)
        self.legal_at[key] = legal
        # The recovered base incorrectly zeroes h for GAME_OVER even when
        # level_completed did not increase. A failed terminal is not a goal.
        if obs.state.upper() == 'GAME_OVER' and (
            self.level2_base_completed is None or
            obs.levels_completed <= self.level2_base_completed):
            self.h_learned[key] = self._eval_h(obs)
        if ((self.level2_base_completed is not None and
             obs.levels_completed > self.level2_base_completed) or
                obs.state.upper() == 'WIN'):
            self.terminal_nodes.add(key)
            self.h_learned[key] = 0.0

    def _bellman_candidate(self, key: str):
        """1-step Bellman target only when *every* legal action is observed.

        T(s) = min_a (1 + V(observed successor)). Self loops are included.
        If differing outcomes share one visible (s,a), the graph is not a
        deterministic fully observed transition system; abstain from backup.
        """
        if key in self.terminal_nodes or key in self.ambiguous_nodes:
            return None
        legal = self.legal_at.get(key)
        if not legal or any(not self.graph[key].get(a) for a in legal):
            return None
        q=[]
        for a in sorted(legal):
            destinations={e.destination for e in self.graph[key][a]}
            if len(destinations)!=1:
                self.ambiguous_nodes.add(key)
                return None
            dest=next(iter(destinations))
            q.append(1.0+self.h_learned[dest])
        return min(q)

    def _backup_closure(self, source: str):
        """Monotone LRTA update followed by bounded predecessor propagation.

        Standard LRTA learning step: V(s) <- max(V(s), T(s)) with unit action
        costs. Preconditions: stable deterministic observed transitions, and
        all legal actions for s observed. h0 admissibility is *not* verified.
        """
        if not self.enable_backups:
            return
        queue=deque([source]); queued={source}; visited=set(); n=0
        while queue and n < self.max_propagations:
            s=queue.popleft(); queued.discard(s); n+=1
            if s in visited:
                continue
            visited.add(s)
            self.backup_diagnostics['backup_calls']+=1
            target=self._bellman_candidate(s)
            if target is None:
                if s in self.ambiguous_nodes:
                    self.backup_diagnostics['aliased']+=1
                else:
                    self.backup_diagnostics['incomplete']+=1
                continue
            old=self.h_learned[s]
            new=max(old, target)
            if new>old+1e-9:
                self.h_learned[s]=new
                self.backup_events.append({'state':s,'before':old,'target':target,
                                           'after':new,'source':source,
                                           'all_legal_known':True})
                for predecessor in sorted(self.predecessors[s]):
                    if predecessor not in queued and predecessor not in visited:
                        queue.append(predecessor);queued.add(predecessor)
            else:
                self.backup_diagnostics['fixed_point']+=1
        if queue:
            self.backup_diagnostics['propagation_truncated']+=1

    def _record_transition(self, after: Observation) -> None:
        if self.pending is None:
            return
        source_key,before,before_h,action,decision=self.pending
        dest_key=self._key(after)
        changed=int(np.count_nonzero(before.frame0 != after.frame0))
        delta=after.levels_completed-before.levels_completed
        if delta<0 or delta>1:
            raise ValueError('Unexpected native level change')
        same_frame=before.frame_hash==after.frame_hash
        event='ADVANCE' if delta else ('FRAME_CHANGE' if changed else 'SILENT')
        self.history.append((action.key(),event))
        after_h=0.0 if delta or after.state.upper()=='WIN' else self._eval_h(after)
        edge=Edge(source_key,dest_key,action,before_h,after_h,changed,delta,
                  same_frame,source_key==dest_key)
        previous={e.destination for e in self.graph[source_key][action.key()]}
        self.graph[source_key][action.key()].append(edge)
        self.predecessors[dest_key].add(source_key)
        self.action_stats[action.key()].add(before_h-after_h, changed)
        self.nodes.setdefault(dest_key, {'h':after_h,'frame_hash':after.frame_hash})
        self.h_learned.setdefault(dest_key, after_h)
        if previous and dest_key not in previous:
            self.ambiguous_nodes.add(source_key)
        if same_frame and not delta:
            self.last_noop_on_frame.add((before.frame_hash,action.key()))
        self.last_action_key=action.key()
        if delta or after.state.upper()=='WIN':
            self.terminal_nodes.add(dest_key)
            self.h_learned[dest_key]=0.0
        prev_update_count=len(self.backup_events)
        self._backup_closure(source_key)
        self.event_log.append({'native_action':self.native_actions,
           'level2_action':self.level2_actions,
           'before':source_key,'after':dest_key,'action':action.to_dict(),
           'h_before':before_h,'h_after':after_h,
           'V_origin_after':self.h_learned[source_key],
           'V_destination_after':self.h_learned[dest_key],
           'new_backup_events':len(self.backup_events)-prev_update_count,
           'changed_pixels':changed,'self_loop_observed':same_frame,
           'level_advance':delta,'chosen_reason':decision.get('reason'),
           'scores':decision.get('scores')})
        self.pending=None

    def decide(self, obs: Observation) -> Action:
        if self.pending is not None or self.last_observation is not obs:
            self.observe(obs)
        if obs.state.upper() in ('WIN','GAME_OVER') or (
            self.level2_base_completed is not None and
            obs.levels_completed > self.level2_base_completed):
            raise RuntimeError('Level-2 terminal')
        if self.level2_start is None:
            raise RuntimeError('Level-2-only controller')
        if self.level2_actions>=self.config.episode_limit:
            raise RuntimeError('No-reset action budget reached')
        key=self.last_key
        v=self.h_learned[key]
        candidates=[];scores={};reasons={}
        for rank,a in enumerate(obs.actions):
            if a.name.upper()=='RESET':
                continue
            ak=a.key()
            past=self.graph[key].get(ak, ())
            attempts=self.context_attempts[(key,ak)]
            if past:
                succ={e.destination for e in past}
                # For non-Markov screens use a conservative upper Q bound.
                q=1.0+max(self.h_learned[s] for s in succ)
                reasons[ak]='known_successor_aliased' if len(succ)>1 else 'known_successor_V'
            else:
                stats=self.action_stats[ak]
                gain=max(0.0,self.prior.get(ak,0.0),
                          self.config.known_positive_gain_weight*max(0.0,stats.mean_gain))
                # Learned V(s), not raw h(s), drives estimated actions too.
                q=max(1.0,1.0+max(0.0,v-gain)-self.config.unseen_action_bonus)
                if stats.effect_count and not stats.success_count:
                    q-=self.config.effect_without_progress_bonus
                reasons[ak]='untried_optimistic_V'
                bonus=self._silent_repeat_bonus(obs.frame_hash,a)
                if bonus:
                    q-=bonus
                    reasons[ak]='silent_repeat_intervention'
            q+=self.config.retry_penalty*attempts
            scores[ak]=q
            candidates.append((q,rank,a))
        if not candidates:
            raise RuntimeError('No non-reset actions')
        _,_,chosen=min(candidates)
        self.context_attempts[(key,chosen.key())]+=1
        self.native_actions+=1;self.level2_actions+=1
        why=reasons[chosen.key()]
        decision={'reason':why,'scores':scores,'rank':1,
                  'value_current':v,'value_source':'learned_Bellman' if self.enable_backups else 'raw_no_backup'}
        self.pending=(key,obs,self._eval_h(obs),chosen,decision)
        self.last_decision=decision
        return chosen

    def summary(self):
        s=super().summary()
        s.update({'algorithm':'N101_Bellman_repaired_observed_graph',
                  'backup_enabled':self.enable_backups,
                  'backup_increases':len(self.backup_events),
                  'aliased_visible_nodes':len(self.ambiguous_nodes),
                  'backup_diagnostics':dict(self.backup_diagnostics)})
        return s
