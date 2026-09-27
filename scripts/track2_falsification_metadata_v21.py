import argparse,json,hashlib
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from datetime import datetime,timezone
import xml.etree.ElementTree as ET
parser=argparse.ArgumentParser(description='Fetch public discovery metadata; use a new output path.')
parser.add_argument('output',nargs='?',type=Path,default=Path('notes/track2-falsification-metadata-v21.json'))
args=parser.parse_args()
if args.output.exists(): raise ValueError('Existing metadata is protected; use a new output path')
raw_path=Path('results/feat009')/(args.output.stem+'.xml')
if raw_path.exists(): raise ValueError('Existing raw metadata is protected; choose a new output name')
files=[Path('notes/track2-falsification-search-v21.json'),Path('notes/track2-falsification-search-fallback-v21.json')]
ids=sorted({p for f in files for q in json.loads(f.read_text())['queries'] for p in q.get('pubmed_ids',[])})
url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urlencode(dict(db='pubmed',id=','.join(ids),retmode='xml'))
out={'date_utc':datetime.now(timezone.utc).isoformat(),'requested_ids':ids,'input_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'scope':'Discovery metadata, not papers independently reviewed'}
try:
    with urlopen(Request(url,headers={'User-Agent':'Track2-public-evidence-audit/21'}),timeout=60) as r:raw=r.read()
    raw_path.write_bytes(raw)
    out['raw_sha256']=hashlib.sha256(raw).hexdigest()
    root=ET.fromstring(raw)
    out['records']=[dict(pmid=a.findtext('./MedlineCitation/PMID'),title=''.join(a.find('./MedlineCitation/Article/ArticleTitle').itertext()),doi=next((i.text for i in a.findall('./PubmedData/ArticleIdList/ArticleId') if i.attrib.get('IdType')=='doi'),None),publication_types=[i.text for i in a.findall('./MedlineCitation/Article/PublicationTypeList/PublicationType')],linked_notices=[dict(type=c.attrib.get('RefType'),pmid=c.findtext('PMID')) for c in a.findall('./MedlineCitation/CommentsCorrectionsList/CommentsCorrections')]) for a in root.findall('PubmedArticle')]
except Exception as e:out['error']=type(e).__name__+': '+str(e)
args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(requested=len(ids),retrieved=len(out.get('records',[])),error=out.get('error'))))
