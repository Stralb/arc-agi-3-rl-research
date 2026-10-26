"""Acting-time candidate parity on SDK; only compare results after execution."""
from __future__ import annotations
import json
from pathlib import Path
import run_native as runner
from candidate_submission import AuditedCrossLevelCore
runner.AuditedCrossLevelCore=AuditedCrossLevelCore
root=Path(__file__).resolve().parent
for game in ('ar25','tu93','vc33','lp85'):
    fresh=runner.run(game,mode='local',native_seed=47,policy_seed=76)
    ref=json.loads((root/'results'/'local'/(game+'.json')).read_text())
    assert fresh['levels']==ref['levels']
    assert fresh['charged_actions']==ref['charged_actions']
    assert [(v['a'],v['pre_sha'],v['post_sha'],v['reward']) for v in fresh['trace']]==[(v['a'],v['pre_sha'],v['post_sha'],v['reward']) for v in ref['trace']],game
    print('CANDIDATE PARITY',game,fresh['levels'],fresh['charged_actions'],flush=True)
print('CANDIDATE PARITY 4/4 native episodes matched')
