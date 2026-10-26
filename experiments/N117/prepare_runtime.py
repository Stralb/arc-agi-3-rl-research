"""Extract only the public archived SDK and frozen code dependencies; no game internals are read."""
from pathlib import Path
import zipfile,shutil,hashlib
ROOT=Path(__file__).resolve().parent
src=ROOT/'inputs/N100_ACTIVE_FSM_20261025.zip'
dest=ROOT/'work'
with zipfile.ZipFile(src) as z:
    for entry in z.infolist():
        name=entry.filename
        if not name.startswith('N100_ACTIVE_FSM/') or entry.is_dir():
            continue
        sub=name[len('N100_ACTIVE_FSM/'):]
        if not (sub.startswith(('sdk_runtime/site/','sdk_runtime/environment_files/','baseline_source/','src/','n090/','n093/')) or sub=='replay_native.py'):
            continue
        target=dest/name
        if target.exists() and target.stat().st_size==entry.file_size:
            continue
        target.parent.mkdir(parents=True,exist_ok=True)
        with z.open(entry) as r,target.open('wb') as w:
            shutil.copyfileobj(r,w)
print('Runtime prepared:',dest/'N100_ACTIVE_FSM')
