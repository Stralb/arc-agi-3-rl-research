#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="$ROOT/artifacts/e012_scheduler"
PRIMARY_DEVICE="${1:-cpu}"
PARALLELISM="${2:-${SLURM_CPUS_PER_TASK:-1}}"
EXPECTED=60
mkdir -p "$STATE/task_locks" "$STATE/failures" "$ROOT/logs" "$ROOT/results/runs"

log() { echo "[$(date '+%F %T')] job=${SLURM_JOB_ID:-local} host=$(hostname) $*"; }

if [[ -f "$STATE/COMPLETE" ]]; then
  log "E012 already complete"
  exit 0
fi

run_initialization() {
  exec 9>"$STATE/init.lock"
  if flock -n 9; then
    if [[ ! -f "$STATE/init.done" ]]; then
      log "running one-time unit tests + preflight + ARC smoke"
      python3 -m unittest discover -s tests -v || { echo "unit tests failed" > "$STATE/FATAL"; return 1; }
      python3 scripts/preflight.py || { echo "preflight failed" > "$STATE/FATAL"; return 1; }
      python3 scripts/smoke.py || { echo "smoke failed" > "$STATE/FATAL"; return 1; }
      touch "$STATE/init.done"
      log "initialization complete"
    fi
    flock -u 9
  fi
  exec 9>&-

  while [[ ! -f "$STATE/init.done" ]]; do
    [[ -f "$STATE/FATAL" ]] && { cat "$STATE/FATAL"; return 1; }
    sleep 2
  done
}

result_count() {
  find "$ROOT/results/runs" -maxdepth 1 -type f -name '*.json' 2>/dev/null | wc -l
}

run_lane() {
  local lane="$1" device="$2"
  log "lane=$lane device=$device START"
  while true; do
    [[ -f "$STATE/FATAL" ]] && return 1
    local n
    n=$(result_count)
    if (( n >= EXPECTED )); then
      log "lane=$lane sees all $EXPECTED tasks complete"
      return 0
    fi

    local claimed=0
    for idx in $(seq 0 $((EXPECTED - 1))); do
      local lock="$STATE/task_locks/task_${idx}.lock"
      exec {fd}>"$lock"
      if flock -n "$fd"; then
        # tournament itself checks the deterministic output path and skips if done.
        claimed=1
        log "lane=$lane claim task=$idx device=$device"
        if python3 -m arc_e012.tournament --task-index "$idx" --device "$device"; then
          rm -f "$STATE/failures/task_${idx}.count"
        else
          local fails=0 f="$STATE/failures/task_${idx}.count"
          [[ -f "$f" ]] && fails=$(cat "$f" 2>/dev/null || echo 0)
          fails=$((fails + 1))
          echo "$fails" > "$f"
          log "lane=$lane task=$idx FAILED attempt=$fails"
          if (( fails >= 3 )); then
            echo "task=$idx failed $fails times; last job ${SLURM_JOB_ID:-unknown}" > "$STATE/FATAL"
          fi
        fi
        flock -u "$fd"
      fi
      eval "exec ${fd}>&-"
      (( claimed == 1 )) && break
    done
    (( claimed == 0 )) && sleep 1
  done
}

finalize_once() {
  [[ $(result_count) -eq EXPECTED ]] || return 0
  exec 8>"$STATE/finalize.lock"
  if flock -n 8; then
    if [[ ! -f "$STATE/COMPLETE" ]]; then
      log "aggregating E012"
      python3 -m arc_e012.aggregate || { echo "aggregation failed" > "$STATE/FATAL"; return 1; }
      python3 -m arc_e012.report || { echo "report failed" > "$STATE/FATAL"; return 1; }
      touch "$STATE/COMPLETE"
      log "E012 COMPLETE"

      if command -v squeue >/dev/null 2>&1 && command -v scancel >/dev/null 2>&1; then
        squeue -h -u "$USER" -o '%A %j' | awk '$2 ~ /^e012_/ {print $1}' | while read -r jid; do
          [[ -z "$jid" || "$jid" == "${SLURM_JOB_ID:-}" ]] && continue
          scancel "$jid" 2>/dev/null || true
        done
      fi
    fi
    flock -u 8
  fi
  exec 8>&-
}

run_initialization

# Avoid nested BLAS/OpenMP oversubscription: parallelism comes from independent ARC trials.
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export TORCH_NUM_THREADS=1

if (( PARALLELISM < 1 )); then PARALLELISM=1; fi

pids=()
if [[ "$PRIMARY_DEVICE" == "auto" ]] && python3 - <<'PY' >/dev/null 2>&1
import torch
raise SystemExit(0 if torch.cuda.is_available() else 1)
PY
then
  # One CUDA lane plus CPU lanes uses both the GPU and otherwise-idle host CPUs.
  run_lane "gpu0" cuda & pids+=("$!")
  cpu_lanes=$((PARALLELISM - 1))
  for i in $(seq 1 "$cpu_lanes" 2>/dev/null || true); do
    run_lane "cpu${i}" cpu & pids+=("$!")
  done
else
  dev="$PRIMARY_DEVICE"
  [[ "$dev" == "auto" ]] && dev=cpu
  for i in $(seq 1 "$PARALLELISM"); do
    run_lane "${dev}${i}" "$dev" & pids+=("$!")
  done
fi

status=0
for pid in "${pids[@]}"; do
  wait "$pid" || status=1
done
[[ -f "$STATE/FATAL" ]] && { cat "$STATE/FATAL"; exit 1; }
finalize_once
exit "$status"
