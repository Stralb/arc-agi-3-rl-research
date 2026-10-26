"""Reproducible native SDK experiment, no game source inspection at acting time."""
from __future__ import annotations
import argparse,hashlib,json,os,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('N093_RUNTIME_ROOT',str(ROOT/'work/N100_ACTIVE_FSM')))
for p in [ROOT/'src',SOURCE/'sdk_runtime/site',SOURCE/'baseline_source',SOURCE/'src',SOURCE,ROOT/'inputs']:
    sys.path.insert(0,str(p))
os.environ['ARC_ENV_ROOT']=str(SOURCE/'sdk_runtime/environment_files')
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
import torch
torch.set_num_threads(1)
from replay_native import make_arcade,GameAction,frame_sha
from n090.run import legal_vector,sdk_action,ended
from submission import MyAgent
from policy import AuditedCrossLevelCore,MODES
FAMILIES=tuple(sorted(p.name for p in (SOURCE/'sdk_runtime/environment_files').iterdir() if p.is_dir()))
TRAIN=('ar25','bp35','cn04','dc22','g50t','ka59','lf52','lp85','m0r0','re86','sb26','sp80','tn36','tu93','wa30')
VALID=('cd82','ls20','sc25','sk48','su15')
assert len(FAMILIES)==25
assert MyAgent.MAX_ACTIONS_PER_LEVEL==200


def run(family,mode='baseline',native_seed=47,policy_seed=76):
    if family not in FAMILIES:raise ValueError(family)
    started=time.monotonic()
    env=make_arcade().make(family,seed=native_seed)
    obs=env.observation_space
    frame=np.asarray(obs.frame[-1],np.uint8).copy()
    core=AuditedCrossLevelCore(checkpoint=None,seed=policy_seed,learning=True,
            prior_enabled=True,puct=True,uniform=False,c=.1,temperature=2.,mode=mode)
    core.start_level(int(obs.levels_completed),frame)
    rows=[];wins=[];counts={};stop=None
    while not stop:
        obs=env.observation_space
        level=int(obs.levels_completed)
        stage=level+1
        if ended(obs.state):stop='native_terminal';break
        if counts.get(str(stage),0)>=200:stop='per_level_200_cap';break
        legal=legal_vector(env)
        if not legal.any():stop='no_legal_action';break
        pre=np.asarray(obs.frame[-1],np.uint8).copy()
        action_index=int(core.choose(pre,legal))
        native=sdk_action(action_index)
        if not core._legal_encoded(action_index,legal):raise AssertionError('illegal action')
        new=env.step(GameAction[native['action']],data=native['data'])
        new_level=int(new.levels_completed)
        if not level<=new_level<=level+1:raise AssertionError('invalid level')
        post=np.asarray(new.frame[-1],np.uint8).copy()
        core.observe(post,legal_vector(env),new_level,terminal=ended(new.state))
        counts[str(stage)]=counts.get(str(stage),0)+1
        if new_level>level:wins.append({'level':new_level,'action':len(rows)+1})
        diag=core.action_diag[-1]
        rows.append({'t':len(rows)+1,'a':native,'index':action_index,'level':stage,
                     'pre_sha':frame_sha(pre),'post_sha':frame_sha(post),
                     'delta_pixels':int(np.count_nonzero(pre!=post)),
                     'reward':int(new_level>level),'next_state':str(new.state),
                     'diag':diag})
        if ended(new.state):stop='native_terminal';break
        if len(rows)>10000:stop='emergency_cap';break
    return {'family':family,'arm':mode,'native_seed':native_seed,'policy_seed':policy_seed,
            'levels':int(env.observation_space.levels_completed),'wins':wins,
            'charged_actions':len(rows),'per_level_actions':counts,'stop':stop,
            'native_state':str(env.observation_space.state),'report':core.report(),
            'elapsed_seconds':round(time.monotonic()-started,4),'trace':rows}


def main():
    p=argparse.ArgumentParser();p.add_argument('--arm',choices=MODES,default='baseline')
    p.add_argument('--families',nargs='*',default=list(FAMILIES))
    p.add_argument('--out',default=str(ROOT/'results'))
    p.add_argument('--resume',action='store_true')
    p.add_argument('--policy-seed',type=int,default=76)
    p.add_argument('--native-seed',type=int,default=47)
    args=p.parse_args();out=Path(args.out)/args.arm;out.mkdir(parents=True,exist_ok=True)
    for g in args.families:
        target=out/(g+'.json')
        if target.exists() and args.resume:continue
        try:r=run(g,args.arm,args.native_seed,args.policy_seed)
        except Exception as e:
            r={'family':g,'arm':args.arm,'fatal':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
        target.write_text(json.dumps(r,indent=2)+'\n')
        print(args.arm,g,'LEVELS',r.get('levels'),'SDK',r.get('charged_actions'),
              'SWITCH',r.get('report',{}).get('changed_vs_frozen_state_choice'),
              'ERROR',r.get('fatal'),flush=True)
        if 'fatal' in r:raise RuntimeError(r['traceback'])
if __name__=='__main__':main()
