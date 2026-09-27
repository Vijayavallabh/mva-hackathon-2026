#!/usr/bin/env python3
"""Plot observed public reanalysis values without implying a clinical effect."""
import argparse
import json
from pathlib import Path


def render(root,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
        'axes.spines.right':False,'axes.edgecolor':'#A7B7BD','axes.labelcolor':'#142C3C',
        'text.color':'#142C3C','xtick.color':'#4C6370','ytick.color':'#142C3C',
        'pdf.fonttype':42,'svg.fonttype':'none','svg.hashsalt':'track2-transcriptome-v19'})
    rows=json.loads((root/'notes/track2-transcriptome-results-v19.json').read_text())['queries']
    labels=[f"{r['cell_id']}  /  {r['knockdown_time']}  /  n={r['n_reagents']}" for r in rows]
    fig,(a,b)=plt.subplots(1,2,figsize=(13.5,8),sharey=True,layout='constrained',gridspec_kw={'width_ratios':[1,1.35]})
    fig.set_facecolor('#F7FAFC')
    for ax in [a,b]:
        ax.set_facecolor('#F7FAFC');ax.grid(axis='y',color='#DBE4E8',linewidth=.7,zorder=0)
    y=np.arange(len(rows))
    a.scatter([r['split_null_BH_q'] for r in rows],y,s=48,c='#176359',zorder=3)
    a.axvline(.05,c='#48419D',ls='--',lw=1.3,label='Prespecified q threshold')
    a.set_xlim(0,1);a.set_xticks([0,.05,.25,.5,.75,1],['0','.05','.25','.50','.75','1'])
    a.set_yticks(y,labels);a.set_ylim(len(rows)+.4,-.65);a.set_xlabel('BH-adjusted empirical tail area')
    a.set_title('Reagent holdout filter\n0 of 14 contexts pass the full gate',loc='left',fontsize=14,pad=15)
    a.legend(loc='lower right',frameon=False,fontsize=9)
    shown=set()
    for i,q in enumerate(rows):
        raw=next(s for s in q['spaces'] if s['name']=='raw')
        for r in raw['named_compounds']:
            if r['compound']!='everolimus':continue
            marker,color=('o','#176359') if r['time']=='6 h' else ('s','#48419D')
            label=r['time']+' drug exposure'
            b.scatter(r['correlation'],i,s=55,c=color,marker=marker,zorder=3,label=label if label not in shown else None)
            shown.add(label)
    b.axvline(0,c='#7E959D',lw=1.1);b.set_xlim(-.31,.31);b.set_xticks([-.3,-.15,0,.15,.3])
    b.set_xlabel('Spearman correlation\nOpposite expression  ←  0  →  Similar expression')
    b.set_title('Everolimus: 10 µM nominal culture exposure\n13 of 19 context comparisons have positive correlation',loc='left',fontsize=14,pad=15)
    b.legend(loc='lower right',frameon=False,fontsize=9)
    fig.suptitle('Public expression screen did not qualify a drug ranking',fontsize=20,fontweight='bold',x=.02,ha='left')
    fig.supxlabel('GSE92742 · 978 measured genes · n = unique shRNA reagents\nDependent profiles; no joint drug–knockdown treatment or functional-rescue endpoint.',fontsize=10,color='#4C6370')
    output.mkdir(exist_ok=False)
    for suffix in ['png','pdf','svg']:
        fig.savefig(output/f'track2-transcriptome-v19.{suffix}',dpi=180,bbox_inches='tight',metadata={'Date':None} if suffix in ['svg','pdf'] else None)
    svg=output/'track2-transcriptome-v19.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);a=p.parse_args()
    render(Path(__file__).resolve().parents[1],a.output)
