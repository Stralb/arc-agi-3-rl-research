"""Self-contained source/record/checksum and result verification."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
manifest=root/'SHA256SUMS.txt'
assert manifest.exists(), 'Missing SHA256SUMS.txt'
count=0
for raw in manifest.read_text().splitlines():
    if not raw:continue
    hexdigest,relative=raw.split('  ',1)
    p=root/relative
    assert p.exists(),relative
    assert hashlib.sha256(p.read_bytes()).hexdigest()==hexdigest,relative
    count+=1
s=json.loads((root/'results/summary.json').read_text())
assert s['baseline']['level_completions']==14
assert s['local']['level_completions']==15
assert s['baseline']['L3plus']==0==s['local']['L3plus']
assert s['local']['rewarded_families_l2']==['tu93','vc33']
assert s['baseline']['rewarded_families_l2']==['vc33']
assert hashlib.sha256((root/'inputs/submission.py').read_bytes()).hexdigest()==s['frozen_sha256']
assert hashlib.sha256((root/'inputs/submission.ipynb').read_bytes()).hexdigest()==s['frozen_notebook_sha256']
print('Verified',count,'file SHA-256 checksums; unchanged frozen baseline; native summary 14 vs 15 completed levels')
