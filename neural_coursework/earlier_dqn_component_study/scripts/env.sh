#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="/home-mscluster/astrauss/arc_rl_mechanics_killtest/.venv"
E004="/home-mscluster/astrauss/arc_rl_architecture_e004"
E005D="/home-mscluster/astrauss/arc_rl_exploration_e005d"
E008="/home-mscluster/astrauss/arc_rl_backbone_e008"
E009="/home-mscluster/astrauss/arc_rl_exploration_e009"
E011="/home-mscluster/astrauss/arc_rl_persistence_e011"

[[ -x "$VENV/bin/python" ]] || { echo "ERROR missing venv $VENV" >&2; exit 2; }
[[ -d "$E004/src/arc_e004" ]] || { echo "ERROR missing E004 $E004" >&2; exit 2; }
[[ -d "$E005D/src/arc_e005" ]] || { echo "ERROR missing E005D $E005D" >&2; exit 2; }
[[ -f "$E008/results/LOCK_IN.json" ]] || { echo "ERROR missing E008 lock-in" >&2; exit 2; }
[[ -f "$E009/results/LOCK_IN.json" ]] || { echo "ERROR missing E009 lock-in" >&2; exit 2; }
[[ -f "$E011/results/LOCK_IN.json" ]] || { echo "ERROR missing E011 lock-in" >&2; exit 2; }

source "$VENV/bin/activate"
export E004_ROOT="$E004"
export E005D_ROOT="$E005D"
export E008_ROOT="$E008"
export E009_ROOT="$E009"
export E011_ROOT="$E011"
export PYTHONPATH="$ROOT/src:$E005D/src:$E004/src:${PYTHONPATH:-}"
# Each worker launches multiple independent trials; keep each trial single-threaded.
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
mkdir -p "$ROOT/logs" "$ROOT/artifacts/e012_scheduler/task_locks" "$ROOT/artifacts/e012_scheduler/failures" "$ROOT/results/runs"
cd "$ROOT"
