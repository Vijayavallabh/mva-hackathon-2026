#!/usr/bin/env python3
"""Independent original-GCTX score audit and allowlisted campaign archive."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import tarfile
from track2_transcriptome import digest,write_json,require


def audit(root):
    import h5py
    import numpy as np
    import pandas as pd
    from scipy.stats import spearmanr
    one=json.loads((root/'outputs/transcriptome-results.json').read_text())
    two=json.loads((root/'outputs/phase2-results.json').read_text())
    one_file=root/'inputs/GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx'
    two_file=root/'inputs/phase2/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx'
    genes=pd.read_csv(root/'inputs/GSE92742_Broad_LINCS_gene_info.txt.gz',sep='\t',dtype=str)
    measured=set(genes.loc[genes.pr_is_lm.eq('1'),'pr_gene_id'])
    decode=lambda xs:[x.decode() if isinstance(x,bytes) else str(x) for x in xs]
    checks=[]
    with h5py.File(one_file,'r') as a,h5py.File(two_file,'r') as b:
        row1=decode(a['0/META/ROW/id'][:]);col1={x:i for i,x in enumerate(decode(a['0/META/COL/id'][:]))}
        row2=decode(b['0/META/ROW/id'][:]);col2={x:i for i,x in enumerate(decode(b['0/META/COL/id'][:]))}
        ids=[x for x in row1 if x in measured]
        pos1=[row1.index(x) for x in ids];pos2=[row2.index(x) for x in ids]
        require(len(ids)==978,'Independent audit landmark mismatch')
        for release,result,data,columns,positions in [('GSE92742',one,a,col1,pos1),('GSE70138',two,b,col2,pos2)]:
            for q in result['queries']:
                query=np.asarray(a['0/DATA/0/matrix'][col1[q['query_id']],:])[pos1]
                raw=next(s for s in q['spaces'] if s['name']=='raw')
                for r in raw['named_compounds']:
                    if r['compound']!='everolimus':continue
                    chemical=np.asarray(data['0/DATA/0/matrix'][columns[r['signature_id']],:])[positions]
                    expected=float(spearmanr(query,chemical).statistic)
                    error=abs(expected-r['correlation']);require(error<=2e-5,'Original-GCTX score mismatch')
                    checks.append(dict(release=release,query_id=q['query_id'],signature_id=r['signature_id'],
                                       scipy_spearman=expected,gpu_score=r['correlation'],absolute_difference=error))
    result=dict(passed=True,method='Independent SciPy spearmanr from original GCTX coordinates and gene metadata',
                comparisons=len(checks),maximum_absolute_error=max(r['absolute_difference'] for r in checks),checks=checks)
    write_json(root/'outputs/original-gctx-audit.json',result)
    # Bind every scientific output, including the large genetic x compound matrices.
    output_files=[p for p in (root/'outputs').rglob('*') if p.is_file() and p.suffix not in {'.txt','.csv'}]
    inventory=[]
    for p in sorted(output_files):
        inventory.append(dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=digest(p)))
    write_json(root/'outputs/output-inventory.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),files=inventory))
    selected=[]
    for folder in ['inputs','scripts','outputs','logs']:
        for path in (root/folder).rglob('*'):
            if not path.is_file() or path.is_symlink():continue
            relative=str(path.relative_to(root))
            if relative=='logs/audit.log':continue
            if folder=='inputs' and not (path.name.endswith('.txt.gz') or path.name in ['plan.json','phase2-plan.json','followup-plan.json']):continue
            if folder=='scripts' and not path.name.startswith(('track2_transcriptome','run_track2_transcriptome','test_track2_transcriptome')):continue
            if '__pycache__' in path.parts or path.suffix=='.pyc':continue
            if folder=='outputs' and (path.name=='landmarks.npy' or path.name.endswith('-genetic-compound.npy')):continue
            selected.append(path)
    selected.extend([root/'pyproject.toml',root/'uv.lock'])
    paths=sorted(set(selected))
    manifest={str(p.relative_to(root)):dict(bytes=p.stat().st_size,sha256=digest(p)) for p in paths}
    write_json(root/'archive-manifest.json',dict(files=manifest,
        omissions='Original GEO matrices are fetched by pinned URLs/checksums; prepared landmark matrices and full genetic-by-compound matrices remain on the owner host and are hashed in output-inventory.json. All BUB1B-to-compound score vectors, named-drug records, random-null results and matched-cell tables are included.'))
    archive=root/'transcriptome-v19-audit.tar.gz'
    with tarfile.open(archive,'w:gz') as tar:
        for path in paths+[root/'archive-manifest.json']:tar.add(path,arcname=str(path.relative_to(root)),recursive=False)
    print(json.dumps(dict(archive=archive.name,bytes=archive.stat().st_size,sha256=digest(archive),files=len(paths)+1,
                         original_gctx_comparisons=len(checks),max_error=result['maximum_absolute_error'])),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    audit(p.parse_args().root)
