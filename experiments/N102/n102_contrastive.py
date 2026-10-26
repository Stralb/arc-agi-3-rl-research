"""N102 offline goal-predicate nomination with explicit negative controls.

This module *nominates* terminal-associated predicates from user-approved
public SDK observations. A first-time false->true predicate does not establish
necessity, sufficiency, or portability to unseen levels.

Pre-reward observation comes from the state before executing the reward
producing ACTION. The reward response's frame[-2] is the last outgoing L1
frame in the frozen traces. frame[-3] is NOT the pre-action frame.
"""
from __future__ import annotations
import numpy as np
from scipy import ndimage as ndi

# Thresholds fixed before inspecting reward-associated features.
AREA_THRESHOLDS=(2,4,8,16,32,64,128,256,512)
CONTACT_THRESHOLDS=(1,2,4,8,16)


def source_palette(initial_frame:np.ndarray)->tuple[int,...]:
    """Use only the first (unrewarded) frame to freeze a colour vocabulary."""
    v,n=np.unique(initial_frame,return_counts=True)
    return tuple(sorted(int(c) for c,count in zip(v,n) if count>=2 and count<3700))


def predicates(frame:np.ndarray, palette:tuple[int,...])->dict[str,bool]:
    f=np.asarray(frame,dtype=np.uint8)
    if f.shape!=(64,64):raise ValueError('Expected public 64x64 observation')
    data={};masks={};stats={}
    for c in palette:
        mask=f==c
        n=int(np.count_nonzero(mask))
        masks[c]=mask
        yy,xx=np.nonzero(mask)
        comp,cc=ndi.label(mask)
        holes=int(np.count_nonzero(ndi.binary_fill_holes(mask)&(~mask))) if n else 0
        w=int(np.ptp(xx)+1) if n else 0
        h=int(np.ptp(yy)+1) if n else 0
        cx=float(np.mean(xx)) if n else -100.
        cy=float(np.mean(yy)) if n else -100.
        stats[c]=(n,cx,cy,w,h)
        tag=f'c{c}'
        data[f'{tag}:exists']=n>0
        data[f'{tag}:absent']=n==0
        data[f'{tag}:one_component']=n>0 and cc==1
        data[f'{tag}:multiple_components']=cc>=2
        data[f'{tag}:holes_zero']=n>0 and holes==0
        data[f'{tag}:has_hole']=holes>0
        data[f'{tag}:bbox_filled']=n>=4 and n==w*h
        data[f'{tag}:horizontal_run']=n>=4 and h<=2 and w>=5
        data[f'{tag}:vertical_run']=n>=4 and w<=2 and h>=5
        data[f'{tag}:mirror_lr']=n>=4 and np.array_equal(mask,mask[:,::-1])
        data[f'{tag}:mirror_ud']=n>=4 and np.array_equal(mask,mask[::-1,:])
        data[f'{tag}:complete_row']=bool(n>0 and np.any(np.all(mask,axis=1)))
        data[f'{tag}:complete_col']=bool(n>0 and np.any(np.all(mask,axis=0)))
        for t in AREA_THRESHOLDS:
            data[f'{tag}:area_ge_{t}']=n>=t
            data[f'{tag}:area_le_{t}']=n>0 and n<=t
    for i,a in enumerate(palette):
        na,xa,ya,wa,ha=stats[a]
        for b in palette[i+1:]:
            nb,xb,yb,wb,hb=stats[b]
            ma,mb=masks[a],masks[b]
            contact=int(np.count_nonzero(ma[:,1:]&mb[:,:-1])+np.count_nonzero(ma[:,:-1]&mb[:,1:])+
                        np.count_nonzero(ma[1:]&mb[:-1])+np.count_nonzero(ma[:-1]&mb[1:]))
            t=f'c{a}_c{b}'
            for k in CONTACT_THRESHOLDS:
                data[f'{t}:touches_ge_{k}']=bool(na and nb and contact>=k)
            data[f'{t}:separated']=bool(na and nb and contact==0)
            data[f'{t}:aligned_x_1']=bool(na>=2 and nb>=2 and abs(xa-xb)<=1.)
            data[f'{t}:aligned_y_1']=bool(na>=2 and nb>=2 and abs(ya-yb)<=1.)
            data[f'{t}:aligned_x_2']=bool(na>=2 and nb>=2 and abs(xa-xb)<=2.)
            data[f'{t}:aligned_y_2']=bool(na>=2 and nb>=2 and abs(ya-yb)<=2.)
    return data


def new_true_candidates(history:list[dict[str,bool]], after:dict[str,bool])->list[str]:
    """Strict False on EVERY recorded earlier state, True after the action."""
    if not history:raise ValueError('Nonempty pre-action history required')
    keys=set.intersection(*(set(x) for x in history),set(after))
    return sorted(k for k in keys if after[k] and all(not before[k] for before in history))


def last_step_flip(before:dict[str,bool],after:dict[str,bool])->list[str]:
    """Ablation: only last transition, ignores earlier occurrences."""
    return sorted(k for k in before.keys() & after.keys() if not before[k] and after[k])


def first_flip_events(frames:np.ndarray, terminal:np.ndarray):
    if len(frames)<2:raise ValueError('At least two pre-action source frames')
    palette=source_palette(frames[0])
    states=[predicates(s,palette) for s in frames]
    win=predicates(terminal,palette)
    positives=new_true_candidates(states,win)
    local_positive=last_step_flip(states[-1],win)
    negatives=[]
    for i in range(1,len(frames)):
        neg=new_true_candidates(states[:i],states[i])
        loc=last_step_flip(states[i-1],states[i])
        negatives.append({'event_index':i,'first_true_candidates':neg,'count':len(neg),
                          'local_candidates_count':len(loc)})
    return {'palette':list(palette),'positive_first_true_candidates':positives,
            'positive_count':len(positives),'local_positive_count':len(local_positive),
            'negative_events':negatives,
            'n_negative_events':len(negatives)}
