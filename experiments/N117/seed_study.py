from __future__ import annotations
import argparse,concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(job):
    mode,game,seed,native,timeout=job
    out=ROOT/'results'/'seed_checks'/f'p{seed}_n{native}'
    outfile=out/mode/(game+'.json')
    if outfile.exists():return mode,game,seed,native,'cached',0
    cmd=[sys.executable,str(ROOT/'run_native.py'),'--arm',mode,'--families',game,'--policy-seed',str(seed),'--native-seed',str(native),'--out',str(out)]
    try:
        b=time.monotonic()
        r=subprocess.run(cmd,cwd=ROOT,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'},capture_output=True,text=True,timeout=timeout)
        return mode,game,seed,native,('ok' if r.returncode==0 else 'error '+r.stderr[-250:]),round(time.monotonic()-b,2)
    except subprocess.TimeoutExpired:return mode,game,seed,native,'timeout',timeout

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--families',nargs='+',default=['tu93']);p.add_argument('--seeds',nargs='+',type=int,default=[76,77,78,79,80,81]);p.add_argument('--native-seeds',nargs='+',type=int,default=[47]);p.add_argument('--arms',nargs='+',default=['baseline','local']);p.add_argument('--workers',type=int,default=3);p.add_argument('--timeout',type=int,default=35)
    a=p.parse_args()
    jobs=[(mode,game,seed,n,a.timeout) for game in a.families for seed in a.seeds for n in a.native_seeds for mode in a.arms]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for result in concurrent.futures.as_completed([ex.submit(run,j) for j in jobs]):
            print('SEED',*result.result(),flush=True)
