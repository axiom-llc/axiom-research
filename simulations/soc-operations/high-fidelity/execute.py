#!/usr/bin/env python3
from pathlib import Path
import argparse,sys
HERE=Path(__file__).resolve().parent
SIM=HERE.parents[1]; sys.path.insert(0,str(SIM/'operational-fidelity'))
from execute_day import execute
PHASES=[('detect-triage', 1, 4, 'soc-desk'), ('contain-authorize', 5, 6, 'response-desk'), ('collect-recover', 7, 9, 'forensics-desk'), ('validate-close', 10, 12, 'incident-command')]
def main(argv=None):
 ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); a=ap.parse_args(argv)
 execute(record_path=HERE/'operating-day.json',out_dir=a.out_dir,domain='cybersecurity-soc',authority_prefix='soc-operations',run_root=Path('/tmp/axiom-soc-hifi-day-001'),phases=PHASES,api_key='soc-hifi-local-key'); return 0
if __name__=='__main__': raise SystemExit(main())
