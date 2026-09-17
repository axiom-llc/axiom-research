#!/usr/bin/env python3
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; SIM=HERE.parents[1]; sys.path.insert(0,str(SIM/'operational-fidelity'))
from execute_day import execute
P=[('order-allocation',1,4,'inventory-desk'),('warehouse-booking',5,7,'warehouse-dock'),('exception-recovery',8,10,'transport-desk'),('ship-close',11,13,'carrier-b')]
def main():
 a=argparse.ArgumentParser(); a.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); x=a.parse_args(); execute(record_path=HERE/'operating-day.json',out_dir=x.out_dir,domain='logistics-supply-chain',authority_prefix='logistics-operations',run_root=Path('/tmp/axiom-logistics-hifi-day-001'),phases=P,api_key='logistics-hifi-local-key')
if __name__=='__main__': main()
