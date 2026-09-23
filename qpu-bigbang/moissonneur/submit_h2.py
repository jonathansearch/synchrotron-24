#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire moisson 2 sur 1 backend (argv). Chaine gloutonne deterministe + log."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang/moissonneur')
from harvest2 import build_harvest2
from batch4 import analyse4, page_S_mit, SHOTS
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
BE = sys.argv[1]
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
be = service.backend(BE)
assert be.status().operational
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
cprops = {str(q): {'ro': round(P.readout_error(q), 5), 'T1': round(P.t1(q)*1e6), 'T2': round(P.t2(q)*1e6)} for q in chain}
print('CHAINE:', chain, 'PROPS:', cprops, flush=True)
pm = generate_preset_pass_manager(backend=be, optimization_level=1, initial_layout=chain)
pubs, base = build_harvest2(5)
def getmap(t):
    try: return ('final_index', list(t.layout.final_index_layout()))
    except Exception: pass
    try: return ('direct', [int(t.layout[q]) for q in t.qubits])
    except Exception: pass
    return ('none', None)
tc, meth = [], None
for nom, qc in pubs:
    t = pm.run(qc)
    m, mp = getmap(t)
    meth = meth or m
    tc.append((nom, t, mp))
print(f'{len(tc)} pubs transpilees, layout={meth}, ex={tc[0][2]}', flush=True)
job = Sampler(mode=be).run([c for _, c, _ in tc], shots=SHOTS)
open(f'/home/user/synchrotron-24/qpu-bigbang/moissonneur/job_h2_{BE}.txt', 'w').write(f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
R = {}
for (nom, _, mp), pub in zip(tc, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    R[nom] = {'counts': {k: int(v) for k, v in counts.items()}, 'map': mp, **analyse4(nom[3:], counts)}
for r in range(5):
    for tm in ('t0', 'l06', 'l10', 'l14'):
        g = lambda b: R[f'R{r}-PAGE-q3-{tm}-{b}']['counts']
        c0, c1 = R[f'R{r}-CALq3-0']['counts'], R[f'R{r}-CALq3-1']['counts']
        R[f'R{r}-PAGE-q3-{tm}'] = {'S_mit': round(page_S_mit(g('Z'), g('X'), g('Y'), c0, c1), 3)}
json.dump({'backend': be.name, 'job': job.job_id(), 'chaine': chain, 'cprops': cprops, 'R': R},
          open(f'/home/user/synchrotron-24/qpu-bigbang/moissonneur/moisson2_{BE}.json', 'w'), indent=0)
print(f'--- {BE} ---')
for nom in ['T0-init'] + [f'T2-l{int(l*10)}' for l in (0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6)] + ['CTRL-libre', 'ECHO-mid']:
    zz = [R[f'R{r}-{nom}']['zz_contact'] for r in range(5)]
    print(f"{nom:12s} zz={np.mean(zz):.4f}±{np.std(zz):.4f}")
for tm in ('t0', 'l06', 'l10', 'l14'):
    v = [R[f'R{r}-PAGE-q3-{tm}']['S_mit'] for r in range(5)]
    print(f'Page-q3-{tm}: {np.mean(v):.3f}±{np.std(v):.3f}')
print('[moisson2] ok', BE)
