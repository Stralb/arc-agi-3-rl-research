"""One public SDK game per fresh Python process; avoids cross-game memory buildup."""
import argparse,subprocess,sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PUBLIC='ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30'.split()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output-dir',default=str(ROOT/'reproduction/fresh'))
    p.add_argument('--timeout-seconds',type=int,default=90)
    a=p.parse_args();out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
    for fam in PUBLIC:
        cmd=[sys.executable,str(ROOT/'run_public_games.py'),'--families',fam,'--resume','--output-dir',str(out)]
        log=out/(fam+'.log')
        with log.open('w') as f:
            try:
                result=subprocess.run(cmd,timeout=a.timeout_seconds,stdout=f,stderr=subprocess.STDOUT)
            except subprocess.TimeoutExpired:
                raise RuntimeError(f'Native game {fam} timed out; inspect {log}')
        if result.returncode!=0:
            raise RuntimeError(f'Native game {fam} failed with exit {result.returncode}; inspect {log}')
        j=json.loads((out/'public25_native_traces.json').read_text())
        row=next((r for r in j['episodes'] if r['family']==fam),None)
        if row is None or 'fatal' in row:
            raise RuntimeError(f'Native game {fam} missing or failed; inspect {log}')
        print('N114_ISOLATED',fam,'levels',row['levels_completed'],'steps',row['sdk_actions'],flush=True)
    j=json.loads((out/'public25_native_traces.json').read_text()); rows=j['episodes']
    if len(rows)!=25: raise RuntimeError('Incomplete 25-game public evaluation')
    print('TOTAL',len(rows),'wins', [sum(r['levels_completed']>=k for r in rows) for k in [1,2,3]],
          'actions',sum(r['sdk_actions'] for r in rows),flush=True)
if __name__=='__main__':main()
