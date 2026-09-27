#!/usr/bin/env python3
"""Bounded public-literature discovery; no subject files, credentials or model calls."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

QUERIES = [
    '(BUBR1 OR BUB1B) AND (everolimus OR rapamycin OR autophagy)',
    '(BUBR1 OR BUB1B) AND (SIRT2 OR niacin OR nicotinamide)',
    '(BUBR1 OR BUB1B) AND (rescue OR correction OR regeneration)',
    '(everolimus OR rapamycin OR sirolimus) AND muscle AND (function OR force OR regeneration)',
    '"RAPA-EX-01"',
    '"Autophagy unrelated transcriptional mechanisms"',
    '(hydroxychloroquine OR chloroquine) AND (chromosome OR myopathy OR aneuploidy)',
    '(pralatrexate OR temsirolimus) AND rhabdomyosarcoma',
    '(entinostat OR vorinostat OR niclosamide OR posaconazole) AND (BUB1B OR aneuploidy OR rhabdomyosarcoma)',
    '(senolytic OR readthrough OR PP2A) AND (BUB1B OR BUBR1)',
    '(LINCS OR L1000) AND (reproducibility OR off-target OR seed)',
    '(everolimus OR sirolimus) AND (pediatric OR children) AND (growth OR kidney OR infection)',
    '"Rapamycin does not compromise physical performance"',
    '"Niacin Cures Systemic"',
    '"NAD+-Precursor Supplementation"',
    '("10.15252/embj.201386907" OR "10.1080/15384101.2024.2402191" OR "10.1002/jcsm.70274" OR "10.1371/journal.pone.0312859") AND (correction OR retraction OR erratum)',
]

def fetch(job):
    index, query, provider = job
    if provider == 'EuropePMC':
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urlencode(dict(
            query='('+query+') AND FIRST_PDATE:[1900-01-01 TO 2026-09-27]',
            format='json', resultType='core', pageSize=20, sort='RELEVANCE'))
    else:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' + urlencode(dict(
            db='pubmed', term='('+query+') AND ("1900/01/01"[Date - Publication] : "2026/09/27"[Date - Publication])',
            retmax=20, retmode='xml', sort='relevance'))
    base = dict(index=index, provider=provider, query=query, url=url,
                retrieved_utc=datetime.now(timezone.utc).isoformat(),
                date_filter='1900-01-01 through 2026-09-27', inspected_window='first 20 metadata records; not full-paper screening')
    try:
        with urlopen(Request(url,headers={'User-Agent':'Track2-public-evidence-audit/21'}),timeout=45) as response:
            raw=response.read()
            base.update(http_status=response.status,sha256=hashlib.sha256(raw).hexdigest())
        if provider == 'EuropePMC':
            data=json.loads(raw)
            base.update(hit_count=data['hitCount'], records=[{k:r.get(k) for k in
                ['id','source','pmid','pmcid','doi','title','firstPublicationDate','pubTypeList','commentCorrectionList']}
                for r in data['resultList']['result']])
        else:
            data=ET.fromstring(raw)
            base.update(hit_count=int(data.findtext('Count')),pubmed_ids=[x.text for x in data.findall('./IdList/Id')],
                        translated_query=data.findtext('QueryTranslation'),
                        warnings=[x.text for x in data.findall('./WarningList/*')])
    except Exception as error:
        base.update(error=type(error).__name__+': '+str(error),hit_count=None)
    return base

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    p.add_argument('--pubmed-fallback',action='store_true',help='Only eight queries not previously sent to PubMed')
    args=p.parse_args()
    if args.output.exists(): raise ValueError('Use a new output path')
    jobs=[(i+1,q,'EuropePMC') for i,q in enumerate(QUERIES)]
    # Sequential requests within each provider avoid a burst against NCBI.
    jobs += [(i+1,QUERIES[i],'PubMed') for i in [0,1,3,4,5,7,10,15]]
    if args.pubmed_fallback:
        jobs=[(i+1,QUERIES[i],'PubMed') for i in [2,6,8,9,11,12,13,14]]
    rows=[fetch(j) for j in jobs]
    out=dict(schema_version=21,scope='Public metadata discovery, not a systematic review or biological experiment',
        queries=rows,complete=all('error' not in r for r in rows),subject_inputs=False,model_provider_added=False)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(requests=len(rows),successful=sum('error' not in r for r in rows),output=str(args.output))))

if __name__=='__main__': main()
