"""Verify original frozen code, N093 parity, game coverage, action accounting and CSV."""
from pathlib import Path
import hashlib,json,zipfile,csv,collections
ROOT=Path(__file__).resolve().parent
z=zipfile.ZipFile(ROOT/'inputs/N100_ACTIVE_FSM_20261025.zip')
old=json.loads(z.read('N100_ACTIVE_FSM/results/N093_10X3X5.json'))
ref={r['game']:r for r in old['results'] if r.get('arm')=='puct_pretrained' and r.get('policy_seed')==76}
with zipfile.ZipFile(ROOT/'inputs/FROZEN_B1_PRETRAINED_PUCT_KAGGLE_20261025.zip') as pkg:
    for name in ('submission.py','submission.ipynb'):
        target=(ROOT/'inputs'/name).read_bytes()
        assert target==pkg.read(name),name
with (ROOT/'results/public25_native_traces.json').open() as f:
    package=json.load(f)
rows=package['episodes']
assert len(rows)==25 and len(set(r['family'] for r in rows))==25
assert all(not r.get('fatal') for r in rows)
assert all(r['native_seed']==47 and r['policy_seed']==76 for r in rows)
assert all(r['termination_reason'] in ('native_terminal','per_level_200_cap','no_legal_action','sdk_already_terminal') for r in rows)
assert all(r['sdk_actions']==len(r['trace']) for r in rows)
for row in rows:
    for level,count in row['by_level_actions'].items():
        assert 0<=int(count)<=200,(row['family'],level,count)
    assert sum(row['by_level_actions'].values())==len(row['trace'])
    assert row['levels_completed']==len(row['wins'])
    assert row['level1']==(row['levels_completed']>=1)
    assert row['level2']==(row['levels_completed']>=2)
    assert row['level3plus']==(row['levels_completed']>=3)
    assert [e['i'] for e in row['trace']]==list(range(1,len(row['trace'])+1))
    for previous,current in zip(row['trace'],row['trace'][1:]):
        assert previous['post_sha']==current['pre_sha'],(row['family'],current['i'])
parity={}
for r in rows:
    if r['family'] not in ref: continue
    src=ref[r['family']]
    assert len(r['trace'])>=len(src['trace'])
    for ours,original in zip(r['trace'],src['trace']):
        assert ours['action']==original['action'],(r['family'],'action',ours['i'])
        assert ours['pre_sha']==original['pre_sha'],(r['family'],'pre',ours['i'])
        assert ours['post_sha']==original['post_sha'],(r['family'],'post',ours['i'])
        assert ours['level_after']==original['level_after'],(r['family'],'level',ours['i'])
    parity[r['family']]=len(src['trace'])
assert len(parity)==10
matrix=list(csv.DictReader((ROOT/'results/public25_matrix.csv').open()))
assert len(matrix)==25
for a,b in zip(matrix,rows):
    assert a['game']==b['family'] and int(a['levels_completed'])==b['levels_completed']
    assert int(a['charged_sdk_actions'])==b['sdk_actions']
assert (sum(x['level1'] for x in rows),sum(x['level2'] for x in rows),sum(x['level3plus'] for x in rows))==(13,1,0)
assert sum(x['sdk_actions'] for x in rows)==2982
result={'passed':True,'n_families':25,'sdk_actions':2982,'completed_l1':13,'completed_l2':1,'completed_l3plus':0,
        'n093_parity_families':len(parity),'n093_parity_actions':sum(parity.values()),'per_family_n093_parity':parity,
        'sha256_submission_py':hashlib.sha256((ROOT/'inputs/submission.py').read_bytes()).hexdigest(),
        'sha256_submission_ipynb':hashlib.sha256((ROOT/'inputs/submission.ipynb').read_bytes()).hexdigest(),
        'sha256_N100_archive':hashlib.sha256((ROOT/'inputs/N100_ACTIVE_FSM_20261025.zip').read_bytes()).hexdigest()}
(ROOT/'results/verified_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
