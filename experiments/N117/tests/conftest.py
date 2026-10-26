import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=Path(os.environ.get('N093_RUNTIME_ROOT',str(root/'work/N100_ACTIVE_FSM')))
for p in (root/'src',root/'inputs',root,source/'sdk_runtime/site',source/'baseline_source',source/'src',source):
    sys.path.insert(0,str(p))
os.environ.setdefault('ARC_ENV_ROOT',str(source/'sdk_runtime/environment_files'))
