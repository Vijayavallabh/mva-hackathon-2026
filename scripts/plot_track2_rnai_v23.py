#!/usr/bin/env python3
"""Plot public v23 RNAi findings; no subject input or online rendering."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);a=p.parse_args();a.output.mkdir(exist_ok=False,parents=True)
root=Path(__file__).resolve().parents[1];d=json.loads((root/'notes/track2-rnai-results-v23.json').read_text())
s=json.loads((root/'notes/track2-rnai-tail-sensitivity-v23.json').read_text())
cells=['A375','A549','HA1E','HCC515','HEPG2','HT29','MCF7','PC3','VCAP']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':14,'axes.labelsize':11,'svg.fonttype':'none','pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(13.2,7.4),gridspec_kw={'width_ratios':[1,1.2]})
fig.patch.set_facecolor('#faf8f3');fig.subplots_adjust(left=.08,right=.975,top=.78,bottom=.31,wspace=.32)
fig.text(.065,.94,'Seed effects limit the BUB1B expression argument',fontsize=21,fontweight='bold',color='#173b45')
fig.text(.065,.875,'GSE106127 • nine cell lines • deposited PRIME representation • overlapping public experiments',fontsize=11,color='#40575e')
y=np.arange(len(cells));a0,a1=axes
for ax in axes:
 ax.set_facecolor('#faf8f3');ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color('#718084');ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0);ax.set_yticks(y,cells);ax.invert_yaxis()
rows=[next(r for r in d['rows'] if r['cell']==c and r['space']=='prime') for c in cells]
gx=[r['classes']['same_gene_different_seed6']['mean'] for r in rows];sx=[r['classes']['different_gene_same_seed6']['mean'] for r in rows]
a0.hlines(y,gx,sx,color='#b8b6ae',linewidth=2)
a0.scatter(gx,y,c='#147d85',s=44,label='Same target; different seed',zorder=3)
a0.scatter(sx,y,c='#b95139',marker='s',s=40,label='Different target; same seed',zorder=3)
a0.set_title('A  Global RNAi comparison',loc='left',pad=15,fontweight='bold',color='#173b45');a0.set_xlim(0,.245);a0.set_xlabel('Mean pairwise Spearman correlation');a0.legend(loc='upper left',bbox_to_anchor=(-.04,-.18),frameon=False,fontsize=10)
for i,row in enumerate(rows):
 null=row['bub1b']['nulls'][1];q=null['summary']['quantiles']
 a1.plot([q[1],q[5]],[i,i],color='#bbc5c3',linewidth=7,solid_capstyle='round',label='Batch-matched 5th–95th percentile' if i==0 else None)
 a1.scatter(q[3],i,marker='|',s=100,c='#45595e',zorder=3,label='Matched-control median' if i==0 else None)
 a1.scatter(row['bub1b']['mean_pair'],i,c='#147d85',marker='D',s=45,zorder=4,label='Observed BUB1B coherence' if i==0 else None)
a1.axvline(0,color='#7a8587',linewidth=.8,linestyle='--');a1.set_title('B  BUB1B versus matched controls',loc='left',pad=15,fontweight='bold',color='#173b45');a1.set_xlabel('Mean pairwise correlation within reagent set');a1.set_xlim(min(r['bub1b']['nulls'][1]['summary']['quantiles'][1] for r in rows)-.018, .215)
a1.legend(loc='upper left',bbox_to_anchor=(-.025,-.18),frameon=False,fontsize=9.5)
fig.text(.065,.055,'HT29 retains a positive signal. Its adjusted tail changes from 0.014 to 0.085 in the finite-reference sensitivity.',fontsize=10.5,color='#173b45')
fig.text(.065,.022,'Control ranges describe resampled sets, not confidence intervals. Correlation and computational QC do not establish rescue.',fontsize=10,color='#40575e')
for suffix in ['png','pdf','svg']:
 fig.savefig(a.output/f'track2-rnai-v23.{suffix}',dpi=220,facecolor=fig.get_facecolor())
 if suffix=='svg':
  path=a.output/f'track2-rnai-v23.{suffix}'
  path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
plt.close(fig)
