#!/usr/bin/env python3
from pathlib import Path
import argparse,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from operational_fidelity.execute_day import execute
PHASES=[('referral-records', 1, 4, 'referral-desk'), ('authorization', 5, 8, 'auth-desk'), ('scheduling-readiness', 9, 11, 'clinical-admin-desk'), ('handoff-close', 12, 14, 'ops-desk')]
def main(argv=None):
 ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); a=ap.parse_args(argv)
 execute(record_path=HERE/'operating-day.json',out_dir=a.out_dir,domain='specialty-care-administration',authority_prefix='care-operations',run_root=Path('/tmp/axiom-care-hifi-day-001'),phases=PHASES,api_key='care-hifi-local-key'); return 0
if __name__=='__main__': raise SystemExit(main())
