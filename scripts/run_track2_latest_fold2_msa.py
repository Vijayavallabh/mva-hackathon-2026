#!/usr/bin/env python3
"""Run the fixed MSA arm after AlphaFold3 releases GPU 7."""
from track2_latest_jobs import launch,ROOT,UV

if __name__=='__main__':
    launch('ESMFold2-shared_msa-run',[7],[UV,'run','--no-sync','--project',str(ROOT/'envs/esm'),
        'python',str(ROOT/'scripts/track2_latest_protein_ccd_fix.py'),'fold','biohub/ESMFold2',
        'ESMFold2-shared_msa','--arm','shared_msa'])
