"""Independent retrospective native SDK replay, never exposed to acting policy."""
import argparse,json,os,sys
from pathlib import Path
root=Path(__file__).resolve().parent
source=Path(os.environ.get('N093_RUNTIME_ROOT',str(root/'work/N100_ACTIVE_FSM')))
for p in [source/'sdk_runtime/site',source/'baseline_source',source/'src',source]:sys.path.insert(0,str(p))
os.environ['ARC_ENV_ROOT']=str(source/'sdk_runtime/environment_files')
import numpy as np
from replay_native import make_arcade,GameAction,frame_sha
from n090.run import legal_vector,ended

def verify(path):
    r=json.loads(Path(path).read_text());env=make_arcade().make(r['family'],seed=r['native_seed']);correct=0
    for t in r['trace']:
        obs=env.observation_space
        old=np.asarray(obs.frame[-1],dtype=np.uint8)
        assert frame_sha(old)==t['pre_sha'],('pre',r['family'],t['t'])
        assert not ended(obs.state),('game over before action',r['family'],t['t'])
        before=int(obs.levels_completed)
        native=t['a'];item=GameAction[native['action']];valid=legal_vector(env)
        assert bool(valid[item.value-1]),('illegal',t['t'])
        outgoing=env.step(item,data=native['data'])
        frame=np.asarray(outgoing.frame[-1],np.uint8)
        assert frame_sha(frame)==t['post_sha'],('post',r['family'],t['t'])
        assert int(outgoing.levels_completed)-before==t['reward'],('reward',t['t'])
        assert int(np.count_nonzero(old!=frame))==t['delta_pixels'],('pixels',t['t'])
        correct+=1
    assert int(env.observation_space.levels_completed)==r['levels'],('levels',r['family'])
    assert str(env.observation_space.state)==r['native_state'],('native state',r['family'])
    return correct
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('paths',nargs='+');a=parser.parse_args()
    count=0
    for p in a.paths:
        n=verify(p);count+=n;print('REPLAY OK',p,n,flush=True)
    print('TOTAL VERIFIED',len(a.paths),'EPISODES',count,'SDK ACTIONS',flush=True)
