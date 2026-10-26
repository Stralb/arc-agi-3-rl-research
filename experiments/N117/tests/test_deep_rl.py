from __future__ import annotations
import ast,hashlib,json
from pathlib import Path
import numpy as np
import pytest
from submission import PretrainedPUCTCore,MyAgent
from policy import AuditedCrossLevelCore
ROOT=Path(__file__).resolve().parents[1]

def new(mode='baseline'):
    return AuditedCrossLevelCore(checkpoint=None,seed=76,learning=True,prior_enabled=True,
            puct=True,uniform=False,c=.1,temperature=2.,mode=mode)

def test_frozen_checksums():
    assert hashlib.sha256((ROOT/'inputs/submission.py').read_bytes()).hexdigest()=='e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d'
    assert hashlib.sha256((ROOT/'inputs/submission.ipynb').read_bytes()).hexdigest()=='1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4'

def test_candidate_is_standalone_and_frozen_unchanged():
    candidate=(ROOT/'candidate_submission.py').read_text()
    assert candidate.startswith((ROOT/'inputs/submission.py').read_text())
    ast.parse(candidate)
    assert 'class MyAgent(_FrozenBaselineMyAgent)' in candidate
    assert 'mode=\'local\'' in candidate

def test_no_source_family_specific_dispatch():
    policy=(ROOT/'src/policy.py').read_text()
    for name in ('vc33','tu93','ar25','lp85','sc25'):
        assert name not in policy

def test_original_bellman_q_drops_after_nonreward():
    core=new();f=np.zeros((64,64),dtype=np.uint8);legal=np.array([1,1,1,1,1,0,0],bool)
    core.start_level(1,f);s=core.node(f,legal);a=int(core.nodes[s]['actions'][0]);assert core.nodes[s]['q'][a]==1.0
    core._observe_q(s,a,s,0.,False)
    assert np.isclose(core.nodes[s]['q'][a],0.985)
    assert max(core.nodes[s]['q'].values())==1.0

def test_frozen_puct_does_not_consult_belief_rank():
    core=new();f=np.zeros((64,64),dtype=np.uint8);legal=np.array([1,1,1,1,1,0,0],bool)
    core.start_level(1,f)
    core.beliefs.rank=lambda *a:(_ for _ in ()).throw(AssertionError('rank() called'))
    core.choose(f,legal)

def test_local_effect_penalizes_tiny_effects():
    core=new('local');f=np.zeros((64,64),dtype=np.uint8)
    ev=core.beliefs.current[('primitive',3)]
    ev.no=3
    prior,local,_,_,obs=core._memory_bonus(f,3,'local')
    assert obs==3 and prior==0 and local<0

def test_zero_nonzero_threshold_control_reverses_preference():
    core=new('local_any_pixel');f=np.zeros((64,64),dtype=np.uint8)
    desc=('primitive',3)
    core.beliefs.current[desc].no=3
    core.visible_totals[desc]=3;core.visible_changes[desc]=3
    x,y,_,_,_=core._memory_bonus(f,3,'local_any_pixel')
    assert x+y>0

def test_shuffled_evidence_does_not_use_own_descriptor():
    core=new('local_shuffled');f=np.zeros((64,64),dtype=np.uint8)
    core.beliefs.current[('primitive',3)].no=3
    core.beliefs.current[('primitive',4)].yes=3
    x,y,desc,_,n=core._memory_bonus(f,3,'local_shuffled')
    assert desc==('primitive',4) and n==3 and x+y>0

def test_crosslevel_does_not_change_bellman_rewards():
    core=new('transfer');f=np.zeros((64,64),dtype=np.uint8)
    core.beliefs.past[('primitive',3)].yes=4
    x,y,_,n,_=core._memory_bonus(f,3,'transfer')
    assert x>0 and y==0 and n==4
    assert core.beliefs.past[('primitive',3)].native_reward==0

def test_initial_level_b1_action_matches():
    f=np.zeros((64,64),np.uint8); legal=np.array([1,1,1,1,1,0,0],bool)
    b=new('baseline');c=new('local');b.start_level(0,f);c.start_level(0,f)
    assert b.choose(f,legal)==c.choose(f,legal)

def test_budget_and_legal_filter_are_unchanged():
    assert MyAgent.MAX_ACTIONS_PER_LEVEL==200
    legal=np.array([0,1,0,0,0,0,0],bool)
    assert new()._legal_encoded(1,legal)
    assert not new()._legal_encoded(0,legal)
    assert not new()._legal_encoded(4090,legal)

def test_summary_matches_real_per_family_native_ledgers():
    data=json.loads((ROOT/'results/summary.json').read_text())
    assert data['baseline']['families']==25
    assert data['baseline']['level_completions']==14
    assert data['local']['families']==25
    assert data['local']['level_completions']==15
    assert data['baseline']['rewarded_families_l2']==['vc33']
    assert data['local']['rewarded_families_l2']==['tu93','vc33']
    assert data['local']['L3plus']==0
    assert data['arm_ablations_13']['local_shuffled']['L2']==1
    assert data['arm_ablations_13']['local_any_pixel']['L2']==1

def test_native_records_only_advance_on_actual_reward():
    r=json.loads((ROOT/'results/local/tu93.json').read_text())
    assert r['levels']==2
    assert [t['t'] for t in r['trace'] if t['reward']==1]==[22,44]
    assert r['per_level_actions']=={'1':22,'2':22,'3':35}
    assert all(x['diag']['native_reward']==x['reward'] for x in r['trace'] if 'native_reward' in x['diag'])
