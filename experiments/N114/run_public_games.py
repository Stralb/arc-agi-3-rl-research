"""N114 corrected public ARC-AGI-3 test, NOT a 400+400 ARC-AGI-1 task test.

Uses the exact core embedded in the original frozen submission.py. All execution
passes through public SDK calls. No reward oracle, source-code inspection,
reset queries, per-game rule dispatch, test-time fitting or agent modifications.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,os,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'work/N100_ACTIVE_FSM'
for p in [SOURCE/'sdk_runtime/site',SOURCE/'baseline_source',SOURCE/'src',SOURCE,ROOT/'inputs']:
    sys.path.insert(0,str(p))
os.environ['ARC_ENV_ROOT']=str(SOURCE/'sdk_runtime/environment_files')
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
import torch
torch.set_num_threads(1)
from replay_native import make_arcade,GameAction,frame_sha
from n090.run import legal_vector,sdk_action,ended
from submission import PretrainedPUCTCore, MyAgent

PUBLIC=tuple(sorted(p.name for p in (SOURCE/'sdk_runtime/environment_files').iterdir() if p.is_dir()))
TRAIN=('ar25','bp35','cn04','dc22','g50t','ka59','lf52','lp85','m0r0','re86','sb26','sp80','tn36','tu93','wa30')
VALID=('cd82','ls20','sc25','sk48','su15')
SEALED=('ft09','r11l','s5i5','tr87','vc33')
assert set(PUBLIC)==set(TRAIN+VALID+SEALED) and len(PUBLIC)==25
assert MyAgent.MAX_ACTIONS_PER_LEVEL==200


def run(game,native_seed=47,policy_seed=76):
    started=time.monotonic()
    env=make_arcade().make(game,seed=native_seed)
    obs=env.observation_space
    first=np.asarray(obs.frame[-1],dtype=np.uint8).copy()
    core=PretrainedPUCTCore(checkpoint=None,seed=policy_seed,learning=True,prior_enabled=True,
                            puct=True,uniform=False,c=0.1,temperature=2.0)
    core.start_level(int(obs.levels_completed),first)
    trace=[]; wins=[]; counts={}; reason=None
    if ended(obs.state): reason='sdk_already_terminal'
    while reason is None:
        obs=env.observation_space
        before_level=int(obs.levels_completed)
        current_level=before_level+1
        if ended(obs.state):reason='native_terminal';break
        if core.since_reset>=MyAgent.MAX_ACTIONS_PER_LEVEL:
            reason='per_level_200_cap';break
        legal=legal_vector(env)
        if not legal.any():reason='no_legal_action';break
        old=np.asarray(obs.frame[-1],dtype=np.uint8).copy()
        action_index=int(core.choose(old,legal))
        act=sdk_action(action_index)
        if not bool(legal[GameAction[act['action']].value-1]):
            raise RuntimeError('illegal action chosen')
        outgoing=env.step(GameAction[act['action']],data=act['data'])
        after_level=int(outgoing.levels_completed)
        if not before_level<=after_level<=before_level+1:
            raise RuntimeError('Unexpected completed-level delta')
        counts[str(current_level)]=counts.get(str(current_level),0)+1
        post=np.asarray(outgoing.frame[-1],np.uint8).copy()
        core.observe(post,legal_vector(env),after_level,terminal=ended(outgoing.state))
        row={'i':len(trace)+1,'action':act,'level_before':before_level,'level_after':after_level,
             'pre_sha':frame_sha(old),'post_sha':frame_sha(post),'state':str(outgoing.state),
             'reward':bool(after_level>before_level)}
        trace.append(row)
        if after_level>before_level:
            wins.append({'completed_level':after_level,'charged_action':len(trace),'action':act})
        if ended(outgoing.state):reason='native_terminal';break
        if len(trace)>=10000:
            reason='emergency_game_cap';break
    return {'family':game,'split':'original_train' if game in TRAIN else 'original_validation' if game in VALID else 'original_sealed_historically_exposed',
            'native_seed':native_seed,'policy_seed':policy_seed,
            'level1':int(len(wins)>=1),'level2':int(len(wins)>=2),'level3plus':int(len(wins)>=3),
            'levels_completed':int(env.observation_space.levels_completed),
            'sdk_actions':len(trace),'initial_sha':frame_sha(first),'by_level_actions':counts,
            'wins':wins,'termination_reason':reason,'final_native_state':str(env.observation_space.state),
            'q_updates':int(core.num_updates),'puct_choices':int(core.puct_choices),
            'elapsed_seconds':round(time.monotonic()-started,3),'trace':trace}


def save(rows, out):
    out=Path(out);out.mkdir(exist_ok=True,parents=True)
    (out/'public25_native_traces.json').write_text(json.dumps({'experiment':'N114_VALID_ARC3_PUBLIC','source_archive':'N100_ACTIVE_FSM_20261025.zip',
                    'note':'25 local publicly distributed interactive game environments, NOT 800 static ARC-AGI-1 grids',
                    'agent_sha256':hashlib.sha256((ROOT/'inputs/submission.py').read_bytes()).hexdigest(),
                    'per_level_cap':MyAgent.MAX_ACTIONS_PER_LEVEL,'native_seed':47,'policy_seed':76,
                    'episodes':rows},indent=2)+'\n')
    with (out/'public25_matrix.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['game','original_split','l1','l2','l3plus','levels_completed','charged_sdk_actions','l1_actions','l2_actions','l3_actions','termination','final_state','elapsed_s'])
        for r in rows:
            w.writerow([r['family'],r['split'],r['level1'],r['level2'],r['level3plus'],r['levels_completed'],r['sdk_actions'],
                r['by_level_actions'].get('1',0),r['by_level_actions'].get('2',0),r['by_level_actions'].get('3',0),
                r['termination_reason'],r['final_native_state'],r['elapsed_seconds']])


def main():
    p=argparse.ArgumentParser();p.add_argument('--families',nargs='*',default=list(PUBLIC))
    p.add_argument('--resume',action='store_true');p.add_argument('--output-dir',default=str(ROOT/'results'));a=p.parse_args()
    assert all(g in PUBLIC for g in a.families)
    outdir=Path(a.output_dir);path=outdir/'public25_native_traces.json'; rows=[]
    if a.resume and path.exists():rows=json.loads(path.read_text())['episodes']
    done=set(r['family'] for r in rows)
    for family in a.families:
        if family in done:continue
        try:r=run(family)
        except Exception as e:
            r={'family':family,'fatal':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
        rows.append(r);save(rows,outdir)
        print('N114',family,'levels',r.get('levels_completed'),'actions',r.get('sdk_actions'),
              'wins',[x['charged_action'] for x in r.get('wins',[])],
              'time',r.get('elapsed_seconds'),'error',r.get('fatal'),flush=True)
    print('N114_RESULT',len(rows),'/',len(PUBLIC),'completed_level_counts',
        [sum(r.get('levels_completed',0)>=j for r in rows) for j in [1,2,3]],flush=True)
if __name__=='__main__':main()
