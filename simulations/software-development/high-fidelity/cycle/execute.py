#!/usr/bin/env python3
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; SIM=HERE.parents[2]; sys.path.insert(0,str(SIM/'operational-fidelity'))
from execute_cycle import execute
def main():
 a=argparse.ArgumentParser(); a.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); x=a.parse_args(); execute(cycle_path=HERE/'operational-cycle.json',out_dir=x.out_dir,authority_prefix='software-development-cycle',run_root=Path('/tmp/axiom-software-cycle-001'),api_key='software-cycle-local-key')
if __name__=='__main__': main()
