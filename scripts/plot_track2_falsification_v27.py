#!/usr/bin/env python3
"""Plot complete v27 context sensitivity; no confidence intervals or efficacy estimates."""
import argparse
import json
from pathlib import Path


def plot(root,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    p=json.loads((root/'notes/track2-saturation-results-v27.json').read_text())
    s=json.loads((root/'notes/track2-specificity-results-v27.json').read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none',
                         'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold',
                         'axes.labelcolor':'#142c3c','text.color':'#142c3c','svg.hashsalt':'track2-v27'})
    fig,axes=plt.subplots(1,3,figsize=(17,5.8))
    fig.subplots_adjust(left=.09,right=.985,bottom=.31,top=.79,wspace=.39)
    colors=['#176359','#48419d','#ad6500'];markers=['o','s','^']
    for j in range(3):
        xs=[100*m['windows'][j]['backgrounds']['whole_window']['at_or_below_candidate_fraction'] for m in p['models']]
        axes[0].scatter(xs,range(4),color=colors[j],marker=markers[j],s=55,
                        label=['N-terminal window','C-terminal window','Domain window'][j])
    axes[0].set(yticks=range(4),yticklabels=['ESMC 300M','ESMC 600M','ESMC 6B','ESM3-open'],xlim=(0,100),
                xlabel='Substitutions at/below N1002K (%)',title='A  Candidate rank varies')
    axes[0].invert_yaxis();axes[0].grid(axis='x',alpha=.2);axes[0].legend(loc='upper center',bbox_to_anchor=(.5,-.23),fontsize=9,frameon=False)
    labels=['Original','−13 genes','Mean + 1','Mean + 3','Mean + 10']
    ht=next(r for r in s['records'] if r['cell']=='HT29' and r['space']=='prime')
    qs=[next(q for q in v['queries'] if q['gene']=='BUB1B') for v in ht['representations'].values()]
    axes[1].plot(range(5),[q['correlation'] for q in qs],'-o',color=colors[0],linewidth=2)
    for i,q in enumerate(qs):
        axes[1].annotate(f"{q['rnai_rank']} / {q['crispr_rank']}",(i,q['correlation']),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10)
    axes[1].set(xticks=range(5),xticklabels=labels,ylim=(-.03,.47),title='B  HT29 retrieval persists',
                ylabel='Rank-vector correlation / residual cosine')
    axes[1].text(.5,-.34,'Labels: RNAi rank / CRISPR rank\nOne guide; qualification remains incomplete.',
                  ha='center',va='top',transform=axes[1].transAxes,fontsize=10)
    mc=next(r for r in s['records'] if r['cell']=='MCF7' and r['space']=='prime')
    for gene,color,marker in [('BUB1B',colors[1],'s'),('MTOR',colors[0],'o')]:
        rows=[next(q for q in v['drug_rows'] if q['gene']==gene and float(q['dose'])==.1) for v in mc['representations'].values()]
        axes[2].plot(range(5),[r['correlation'] for r in rows],'-'+marker,color=color,label=gene,linewidth=2)
    axes[2].set(xticks=range(5),xticklabels=labels,ylim=(-.3,.39),title='C  MTOR signal is more stable')
    axes[2].legend(frameon=False,loc='upper right',fontsize=10)
    axes[2].text(.5,-.34,'MCF7, everolimus 0.1 µM nominal culture\nDrug QC passes; BUB1B query QC fails.',
                  ha='center',va='top',transform=axes[2].transAxes,fontsize=10)
    for ax in axes[1:]:
        ax.axhline(0,color='#8899a0',linewidth=.8);ax.grid(axis='y',alpha=.2)
        ax.tick_params(axis='x',labelrotation=35,labelsize=9)
    fig.suptitle('Track 2: stronger model scrutiny changes the interpretation',fontsize=18,x=.055,ha='left',y=.97)
    fig.text(.055,.865,'Protein ranks are descriptive. Expression projections remove the mean direction plus the stated principal components.',fontsize=11)
    fig.text(.055,.03,'Public, reused data and related models. No clinical calibration, joint rescue experiment, qualified non-cancer model or exposure margin.',fontsize=11)
    out.mkdir(exist_ok=False)
    for ext in ['svg','png','pdf']:
        fig.savefig(out/f'track2-falsification-v27.{ext}',dpi=180,metadata={'Date':None} if ext=='svg' else None)
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();plot(a.root,a.output)
