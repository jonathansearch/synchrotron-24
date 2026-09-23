#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""MOISSONNEUR v1 : 3 rondes x 17 pubs (cellule contact, Page-q3, REM).
Exploitation (pas d'exploration) : stats mean/sigma + derive. n=4 avec batch4."""
import json, sys
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
from batch4 import build_batch4, analyse4, SHOTS
BASE = ['T0-init', 'T2-doux', 'T2-mid', 'T2-brutal', 'CTRL-libre', 'ECHO-mid'] + \
       [f'PAGE-q3-{tm}-{b}' for tm in ('t0', 'mid', 'brutal') for b in 'XYZ'] + \
       ['CALq3-0', 'CALq3-1']
def build_harvest(rounds=3):
    allc = dict(build_batch4())
    return [(f'R{r}-{nom}', allc[nom]) for r in range(rounds) for nom in BASE]
if __name__ == '__main__':
    from qiskit.primitives import StatevectorSampler
    sam = StatevectorSampler(seed=31)
    allc = dict(build_batch4())
    for nom in BASE:
        pub = sam.run([(allc[nom], None, SHOTS)], shots=SHOTS).result()[0].data
        c = pub[list(pub)[0]].get_counts()
        print(f'{nom:16s} {analyse4(nom, c)}')
    print('[simu-moisson] logique ok')
