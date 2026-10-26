"""Build optional single-file self-contained experimental candidate (NOT frozen)."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
source=(root/'inputs/submission.py').read_text()
policy=(root/'src/policy.py').read_text()
lines=policy.splitlines(keepends=True)
lines=[s for s in lines if s.strip() not in ('from __future__ import annotations','from submission import PretrainedPUCTCore')]
append='''\n\n# EXPERIMENTAL candidate: action-effect ranking in Level 2 onward.\n# All native Bellman Q updates, Level-1 behavior and frozen checkpoint unchanged.\n'''+''.join(lines)+'''\n\n_FrozenBaselineMyAgent = MyAgent\nclass MyAgent(_FrozenBaselineMyAgent):\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args, **kwargs)\n        self.core = AuditedCrossLevelCore(\n            checkpoint=None, seed=76, learning=True, prior_enabled=True,\n            puct=True, uniform=False, c=0.1, temperature=2.0, mode='local')\n\n    @property\n    def name(self):\n        return f'{super().name}.experimental_local_effect'\n'''
standalone=source+append
path=root/'candidate_submission.py'
path.write_text(standalone)
import ast
ast.parse(standalone)
nb=json.loads((root/'inputs/submission.ipynb').read_text())
nb['cells'][0]['source']=['# Experimental Level-2 effect-memory candidate — NOT verified on hidden Kaggle games\n',
                        '\n','Frozen N093 Level 1 and checkpoint, Level 2 native effect-based action ranking.\n']
nb['cells'][2]['source']=['%%writefile /tmp/my_agent.py\n']+standalone.splitlines(keepends=True)
(root/'candidate_submission.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
print('Frozen SHA256',hashlib.sha256(source.encode()).hexdigest())
print('Candidate',path,hashlib.sha256(path.read_bytes()).hexdigest())
