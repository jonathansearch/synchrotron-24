#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Repoll job radar 3 par ID (reprise apres interruption)."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang/moissonneur')
from radar3 import build_radar, NLS
from batch4 import analyse4, page_S_mit
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
jid = open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/job_r3_kingston.txt').read().split()[0]
job = service.job(jid)
print('JOB:', jid, 'statut:', job.status(), flush=True)
try:
    res = job.result(timeout=90)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
pubs, base = build_radar(3)
R = {}
for (nom, _), pub in zip(pubs, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    R[nom] = {'counts': {k: int(v) for k, v in counts.items()}, **analyse4(nom[3:], counts)}
for r in range(3):
    for tm in ('t0', '2L', '4L', '8L'):
        g = lambda b: R[f'R{r}-PAGE-q3-{tm}-{b}']['counts']
        c0, c1 = R[f'R{r}-CALq3-0']['counts'], R[f'R{r}-CALq3-1']['counts']
        R[f'R{r}-PAGE-q3-{tm}'] = {'S_mit': round(page_S_mit(g('Z'), g('X'), g('Y'), c0, c1), 3)}
json.dump({'backend': 'ibm_kingston', 'job': jid, 'R': R},
          open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/moisson3_kingston.json', 'w'), indent=0)
print('--- RADAR kingston (simu zz: D2 .18 / D3 .38 / D4 .46 / D6 .29 / D8 .31) ---')
for nom in ['T0-init', 'LIBRE-4L', 'ECHO-4L'] + [f'D{n}L' for n in NLS]:
    zz = [R[f'R{r}-{nom}']['zz_contact'] for r in range(3)]
    mi = [R[f'R{r}-{nom}']['MI_LR'] for r in range(3)]
    print(f"{nom:10s} zz={np.mean(zz):.4f}±{np.std(zz):.4f} MI={np.mean(mi):.4f}±{np.std(mi):.4f}")
for tm in ('t0', '2L', '4L', '8L'):
    v = [R[f'R{r}-PAGE-q3-{tm}']['S_mit'] for r in range(3)]
    print(f'Page-q3-{tm}: {np.mean(v):.3f}±{np.std(v):.3f}')
print('[radar3] ok')
