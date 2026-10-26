"""Build a self-contained, checksum-verified N114 research release."""
from pathlib import Path
import hashlib,zipfile,os
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'N114_ARC_AGI3_PUBLIC25_FROZEN_N093_20261026.zip'
chosen=[]
for relative in ['README.md','FINDINGS.md','PROTOCOL_AND_SUMMARY.json','prepare_runtime.py',
                 'run_public_games.py','run_all_isolated.py','verify_release.py']:
    chosen.append(ROOT/relative)
chosen.extend(p for p in (ROOT/'inputs').iterdir() if p.is_file())
chosen.extend(p for p in (ROOT/'results').iterdir() if p.is_file())
chosen.sort(key=lambda x:str(x))
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in chosen)
(ROOT/'SHA256SUMS.txt').write_text(manifest)
with zipfile.ZipFile(OUT,'w') as z:
    for p in chosen+[ROOT/'SHA256SUMS.txt']:
        name=ROOT.name+'/'+p.relative_to(ROOT).as_posix()
        z.write(p,name,compress_type=zipfile.ZIP_DEFLATED,compresslevel=5)
print('WROTE',OUT,'bytes',OUT.stat().st_size,'files',len(chosen)+1)
