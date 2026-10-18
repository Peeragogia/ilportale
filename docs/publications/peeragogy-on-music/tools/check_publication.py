#!/usr/bin/env python3
"""Checks editorial integrity. Does not validate scientific claims or a physical prototype."""
from pathlib import Path
import re,sys,hashlib,json
p=Path(__file__).resolve().parents[1]
main=(p/'main.tex').read_text()
inputs=re.findall(r'\\input\{([^}]+)\}',main)
missing=[x for x in inputs if not (p/(x+'.tex')).is_file()]
text=main+'\n'+'\n'.join((p/(x+'.tex')).read_text() for x in inputs if (p/(x+'.tex')).exists())
keys=re.findall(r'@\w+\{([^,]+)',(p/'references.bib').read_text())
cites=set(k.strip() for group in re.findall(r'\\cite\w*\*?(?:\[[^]]*\])*\{([^}]+)\}',text) for k in group.split(','))
errors=[]
if missing:errors.append('Missing inputs: '+str(missing))
if len(keys)!=len(set(keys)):errors.append('Duplicate bibliography keys')
if cites-set(keys):errors.append('Missing citation keys: '+str(cites-set(keys)))
for logfile in ['main.log','main.blg']:
 if not (p/logfile).exists():errors.append('Missing build log '+logfile);continue
 s=(p/logfile).read_text(errors='replace')
 for line in s.splitlines():
  if re.search(r'Warning|Overfull|Underfull|^!',line):errors.append(logfile+': '+line)
report={'inputs':len(inputs),'bibliography_entries':len(keys),'cited_entries':len(cites),'errors':errors}
if (p/'main.pdf').exists():report['pdf_sha256']=hashlib.sha256((p/'main.pdf').read_bytes()).hexdigest()
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
