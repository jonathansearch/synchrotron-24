#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire batch4 (collisionneur, 29 pubs) en 1 job. Layout fixe. Cle env."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
from batch4 import (build_batch4, analyse4, page_S, page_S_mit, beta1_hamming,
                    hellinger, SHOTS)
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

service = QiskitRuntimeService(channel='ibm_quantum_platform',
                               token=os.environ['IBM_TOKEN'])
bes = [(b, b.status().pending_jobs) for b in service.backends()
       if b.status().operational and b.num_qubits >= 6]
bes.sort(key=lambda t: t[1])
print('files:', [(b.name, q) for b, q in bes[:4]], flush=True)
be = bes[0][0]
print('CHOIX:', be.name, flush=True)
P, cmap, n = be.properties(), be.coupling_map, be.num_qubits
def ok1(i):
    try:
        return bool(np.isfinite(P.readout_error(i)) and np.isfinite(P.t1(i)))
    except Exception:
        return False
def g2err(a, b):
    for gn in ('cz', 'ecr', 'cx'):
        try: return P.gate_error(gn, [a, b])
        except Exception: pass
    return np.nan
edges = [(a, b) for a, b in cmap.get_edges() if ok1(a) and ok1(b)
         and np.isfinite(g2err(a, b))]
s0, e0 = min([(P.readout_error(a)+P.readout_error(b)+5*g2err(a, b), (a, b))
              for a, b in edges])
chain = list(e0)
while len(chain) < 6:
    nb = set()
    for q in chain:
        nb |= set(cmap.neighbors(q))
    nb -= set(chain)
    cand = [(P.readout_error(c)+5*min(g2err(c, q) for q in chain
             if (c, q) in edges or (q, c) in edges), c) for c in nb if ok1(c)]
    cand = [x for x in cand if np.isfinite(x[0])]
    if not cand: break
    chain.append(min(cand)[1])
trip = min([(P.readout_error(a)+P.readout_error(b)+P.readout_error(c)
             + 5*(g2err(a, b)+g2err(b, c)), (a, b, c))
            for a, b in edges for c in set(cmap.neighbors(b))-{a}
            if ok1(c) and ((b, c) in edges or (c, b) in edges)
            and np.isfinite(g2err(b, c))])
print(f'CHAINE6: {chain} | TRIPLE: {trip[1]}', flush=True)
circs = build_batch4()
groups = {6: [], 3: []}
for nom, qc in circs:
    groups[qc.num_qubits].append((nom, qc))
lay = {6: chain, 3: list(trip[1])}
tc = []
for w, lst in groups.items():
    pm = generate_preset_pass_manager(backend=be, optimization_level=1,
                                      initial_layout=lay[w])
    for nom, qc in lst:
        t = pm.run(qc)
        n2q = sum(1 for i in t.data if len(i.qubits) == 2
                  and i.operation.name != 'barrier')
        tc.append((nom, t))
        print(f'  {nom}: depth={t.depth()} 2q={n2q}', flush=True)
job = Sampler(mode=be).run([c for _, c in tc], shots=SHOTS)
open('/home/user/synchrotron-24/qpu-bigbang/job4_id.txt', 'w').write(
    f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
out = {'backend': be.name, 'job': job.job_id(), 'chaine6': chain,
       'triple': trip[1], 'pubs': {}}
for (nom, _), pub in zip(tc, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    out['pubs'][nom] = {'counts': {k: int(v) for k, v in counts.items()},
                        **analyse4(nom, counts)}
c0 = out['pubs']['T0-init']['counts']
print('--- QPU (zz_contact / MI / Hellinger / b1_thr5) ---')
for nom in ('T0-init', 'T2-doux', 'T2-mid', 'T2-brutal', 'CTRL-libre', 'ECHO-mid'):
    e = out['pubs'][nom]
    cc = e['counts']
    print(f"{nom:12s} zz={e.get('zz_contact')} MI={e.get('MI_LR')} "
          f"H={hellinger(c0, cc):.3f} b1={beta1_hamming(cc, 5)[0]}")
for tm in ('t0', 'mid', 'brutal'):
    row = []
    for qb in (0, 3):
        g = lambda b: out['pubs'][f'PAGE-q{qb}-{tm}-{b}']['counts']
        c0c = out['pubs'][f'CALq{qb}-0']['counts']
        c1c = out['pubs'][f'CALq{qb}-1']['counts']
        row.append((round(page_S(g('Z'), g('X'), g('Y')), 3),
                    round(page_S_mit(g('Z'), g('X'), g('Y'), c0c, c1c), 3)))
    print(f'Page(raw,mit) {tm}: q0={row[0]} q3={row[1]}')
json.dump(out, open('/home/user/synchrotron-24/qpu-bigbang/qpu_batch4.json', 'w'), indent=0)
print('[qpu4] ok')
