#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire radar 3 (69 pubs, 1 job, kingston)."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang/moissonneur')
from radar3 import build_radar, NLS
from batch4 import analyse4, page_S_mit, SHOTS
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
be = service.backend('ibm_kingston')
print('CIBLE:', be.name, 'file:', be.status().pending_jobs, flush=True)
P, cmap = be.properties(), be.coupling_map
def ok1(i):
    try: return bool(np.isfinite(P.readout_error(i)) and np.isfinite(P.t1(i)))
    except Exception: return False
def g2err(a, b):
    for gn in ('cz', 'ecr', 'cx'):
        try: return P.gate_error(gn, [a, b])
        except Exception: pass
    return np.nan
edges = sorted([(a, b) for a, b in cmap.get_edges() if ok1(a) and ok1(b) and np.isfinite(g2err(a, b))])
s0, e0 = min([(P.readout_error(a)+P.readout_error(b)+5*g2err(a, b), (a, b)) for a, b in edges])
chain = list(e0)
while len(chain) < 6:
    nb = sorted(set().union(*[set(cmap.neighbors(q)) for q in chain]) - set(chain))
    cand = []
    for c in nb:
        if not ok1(c): continue
        gs = [g2err(c, q) for q in chain if (c, q) in edges or (q, c) in edges]
        gs = [g for g in gs if np.isfinite(g)]
        if gs: cand.append((P.readout_error(c)+5*min(gs), c))
    chain.append(min(cand)[1])
print('CHAINE:', chain, flush=True)
pm = generate_preset_pass_manager(backend=be, optimization_level=1, initial_layout=chain)
pubs, base = build_radar(3)
tc = [(nom, pm.run(qc)) for nom, qc in pubs]
for nom, t in tc[:9]:
    n2q = sum(1 for i in t.data if len(i.qubits) == 2 and i.operation.name != 'barrier')
    print(f'  {nom}: depth={t.depth()} 2q={n2q}', flush=True)
job = Sampler(mode=be).run([c for _, c in tc], shots=SHOTS)
open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/job_r3_kingston.txt', 'w').write(f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
R = {}
for (nom, _), pub in zip(tc, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    R[nom] = {'counts': {k: int(v) for k, v in counts.items()}, **analyse4(nom[3:], counts)}
for r in range(3):
    for tm in ('t0', '2L', '4L', '8L'):
        g = lambda b: R[f'R{r}-PAGE-q3-{tm}-{b}']['counts']
        c0, c1 = R[f'R{r}-CALq3-0']['counts'], R[f'R{r}-CALq3-1']['counts']
        R[f'R{r}-PAGE-q3-{tm}'] = {'S_mit': round(page_S_mit(g('Z'), g('X'), g('Y'), c0, c1), 3)}
json.dump({'backend': be.name, 'job': job.job_id(), 'chaine': chain, 'R': R},
          open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/moisson3_kingston.json', 'w'), indent=0)
print('--- RADAR kingston (simu: zz .18/.38/.46/.29/.31 @2/3/4/6/8) ---')
for nom in ['T0-init', 'LIBRE-4L', 'ECHO-4L'] + [f'D{n}L' for n in NLS]:
    zz = [R[f'R{r}-{nom}']['zz_contact'] for r in range(3)]
    mi = [R[f'R{r}-{nom}']['MI_LR'] for r in range(3)]
    print(f"{nom:10s} zz={np.mean(zz):.4f}±{np.std(zz):.4f} MI={np.mean(mi):.4f}±{np.std(mi):.4f}")
for tm in ('t0', '2L', '4L', '8L'):
    v = [R[f'R{r}-PAGE-q3-{tm}']['S_mit'] for r in range(3)]
    print(f'Page-q3-{tm}: {np.mean(v):.3f}±{np.std(v):.3f}')
print('[radar3] ok')
