#!/usr/bin/env python3
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; SIM=HERE.parents[1]; sys.path.insert(0,str(SIM/'operational-fidelity'))
from execute_day import execute
P=[('intake-implementation',1,4,'dev-desk'),('ci-review',5,9,'ci-review'),('security-build',10,14,'security-desk'),('release-close',15,18,'release-desk')]
def main():
 a=argparse.ArgumentParser(); a.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); x=a.parse_args(); execute(record_path=HERE/'operating-day.json',out_dir=x.out_dir,domain='software-development',authority_prefix='software-operations',run_root=Path('/tmp/axiom-software-hifi-day-001'),phases=P,api_key='software-hifi-local-key')
if __name__=='__main__': main()
