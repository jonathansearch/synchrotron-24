#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire moisson 1 (51 pubs, 1 job). Reutilise chaine batch4 si saine."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang/moissonneur')
from harvest1 import build_harvest, BASE
from batch4 import analyse4, page_S_mit, hellinger, SHOTS
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
try:
    be = service.backend('ibm_marrakesh')
    assert be.status().operational
except Exception:
    bes = [(b, b.status().pending_jobs) for b in service.backends()
           if b.status().operational and b.num_qubits >= 6]
    bes.sort(key=lambda t: t[1])
    be = bes[0][0]
print('CIBLE:', be.name, flush=True)
P, cmap = be.properties(), be.coupling_map
def ok1(i):
    try: return bool(np.isfinite(P.readout_error(i)) and np.isfinite(P.t1(i)))
    except Exception: return False
old = json.load(open('/home/user/synchrotron-24/qpu-bigbang/qpu_batch4.json'))['chaine6']
E = set(cmap.get_edges()) | {(b, a) for a, b in cmap.get_edges()}
chain = old if all(ok1(q) for q in old) and all((old[i], old[i+1]) in E for i in range(5)) else None
print('chaine batch4 reutilisee:', chain, flush=True)
pm = generate_preset_pass_manager(backend=be, optimization_level=1, initial_layout=chain)
pubs = build_harvest(3)
tc = [(nom, pm.run(qc)) for nom, qc in pubs]
job = Sampler(mode=be).run([c for _, c in tc], shots=SHOTS)
open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/job_h1_id.txt', 'w').write(f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
R = {}
for (nom, _), pub in zip(tc, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    R[nom] = {'counts': {k: int(v) for k, v in counts.items()}, **analyse4(nom, counts)}
for r in range(3):
    for tm in ('t0', 'mid', 'brutal'):
        g = lambda b: R[f'R{r}-PAGE-q3-{tm}-{b}']['counts']
        c0, c1 = R[f'R{r}-CALq3-0']['counts'], R[f'R{r}-CALq3-1']['counts']
        R[f'R{r}-PAGE-q3-{tm}'] = {'S_mit': round(page_S_mit(g('Z'), g('X'), g('Y'), c0, c1), 3)}
json.dump({'backend': be.name, 'job': job.job_id(), 'chaine': chain, 'R': R},
          open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/moisson1.json', 'w'), indent=0)
b4 = json.load(open('/home/user/synchrotron-24/qpu-bigbang/qpu_batch4.json'))['pubs']
print('--- MOISSON (rondes R0-R2 + batch4) ---')
for nom in ('T0-init', 'T2-doux', 'T2-mid', 'T2-brutal', 'CTRL-libre', 'ECHO-mid'):
    zz = [R[f'R{r}-{nom}']['zz_contact'] for r in range(3)]
    mi = [R[f'R{r}-{nom}']['MI_LR'] for r in range(3)]
    print(f"{nom:12s} zz={np.mean(zz):.4f}±{np.std(zz):.4f} (b4 {b4[nom]['zz_contact']}) "
          f"MI={np.mean(mi):.4f}±{np.std(mi):.4f} (b4 {b4[nom]['MI_LR']})")
for tm in ('t0', 'mid', 'brutal'):
    v = [R[f'R{r}-PAGE-q3-{tm}']['S_mit'] for r in range(3)]
    print(f'Page-q3-{tm}: S_mit={np.mean(v):.3f}±{np.std(v):.3f}')
print('[moisson1] ok')
