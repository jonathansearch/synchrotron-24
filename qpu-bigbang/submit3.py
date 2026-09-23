#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire batch3 (30 pubs revanche) en 1 job. Layout fixe, REM, fits. Cle env."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/qpu-bigbang')
from batch3 import build_batch3, analyse3, unfold1, unfold2, SHOTS
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

service = QiskitRuntimeService(channel='ibm_quantum_platform',
                               token=os.environ['IBM_TOKEN'])
be = service.backend('ibm_kingston')
print('CIBLE:', be.name, '| file:', be.status().pending_jobs, '| dt:', be.dt,
      flush=True)
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
q1 = min([i for i in range(n) if ok1(i)], key=lambda i: P.readout_error(i))
bp = min([(P.readout_error(a)+P.readout_error(b)+5*g2err(a, b), (a, b))
          for a, b in cmap.get_edges() if ok1(a) and ok1(b)
          and np.isfinite(g2err(a, b))])
pair = bp[1]
cand = []
for a, b in cmap.get_edges():
    for c_ in (set(cmap.neighbors(a)) | set(cmap.neighbors(b))) - {a, b}:
        if not ok1(c_): continue
        g = [g2err(*e) for e in ((a, b), (a, c_), (b, c_)) if e in cmap.get_edges()
             or (e[1], e[0]) in cmap.get_edges()]
        g = [x for x in g if np.isfinite(x)]
        if len(g) < 2: continue
        cand.append((P.readout_error(a)+P.readout_error(b)+P.readout_error(c_)
                     + 5*sum(g), (a, b, c_)))
triple = min(cand)[1]
print(f'QUBITS FIXES: 1q=q{q1} (ro={P.readout_error(q1):.4f}, '
      f'T1={P.t1(q1)*1e6:.0f}us, T2={P.t2(q1)*1e6:.0f}us) | '
      f'2q={pair} | 3q={triple}', flush=True)
circs = build_batch3(be.dt)
groups = {1: [], 2: [], 3: []}
for nom, qc in circs:
    groups[qc.num_qubits].append((nom, qc))
lay = {1: [q1], 2: list(pair), 3: list(triple)}
tc = []
for w, lst in groups.items():
    pm = generate_preset_pass_manager(backend=be, optimization_level=1,
                                      initial_layout=lay[w])
    for nom, qc in lst:
        t = pm.run(qc)
        n2q = sum(1 for i in t.data if len(i.qubits) == 2
                  and i.operation.name != 'barrier')
        try:
            fin = [int(t.layout[q]) for q in t.qubits]
        except Exception:
            fin = None
        tc.append((nom, t, fin))
        print(f'  {nom}: depth={t.depth()} 2q={n2q} map={fin}', flush=True)
job = Sampler(mode=be).run([c for _, c, _ in tc], shots=SHOTS)
open('/home/user/qpu-bigbang/job3_id.txt', 'w').write(f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
raw = {}
for (nom, _, fin), pub in zip(tc, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    raw[nom] = {'counts': {k: int(v) for k, v in counts.items()}, 'map': fin,
                **analyse3(nom, counts)}
c0, c1 = raw['CAL-1q-0']['counts'], raw['CAL-1q-1']['counts']
c2 = {k: raw[f'CAL-2q-{k}']['counts'] for k in ('00', '01', '10', '11')}
out = {'backend': be.name, 'dt': be.dt, 'job': job.job_id(),
       'q1': q1, 'pair': pair, 'triple': triple, 'pubs': {}}
for nom, r in raw.items():
    e = dict(r)
    if r.get('P0') is not None or r.get('P1') is not None:
        e.update(unfold1(r['counts'], c0, c1))
    if r.get('coincidence') is not None:
        e.update(unfold2(r['counts'], c2))
    out['pubs'][nom] = e

def fit_exp(t, y):
    t = np.array(t, float); y = np.array(y, float)
    best = None
    for T in np.linspace(20, 800, 157):
        G = np.column_stack([np.exp(-t/T), np.ones_like(t)])
        c, *_ = np.linalg.lstsq(G, y, rcond=None)
        sse = float(((G @ c - y)**2).sum())
        if best is None or sse < best[0]:
            best = (sse, T, c)
    return {'T': round(float(best[1]), 1), 'A': round(float(best[2][0]), 3),
            'B': round(float(best[2][1]), 3)}
t1t = [0, 25, 50, 100, 200]
out['fit_T1'] = fit_exp(t1t, [out['pubs'][f'S01-T1-{t}us']['P1_mit'] for t in t1t])
t2t = [0, 10, 25, 50, 100]
out['fit_T2'] = fit_exp(t2t, [out['pubs'][f'S06b-ramsey-{t}us']['P0_mit'] for t in t2t])
f1 = out['pubs']['S03-planck-x1']['P_retour']
f3 = out['pubs']['S03-planck-x3']['P_retour']
out['zne'] = {'F_x1': f1, 'F_x3': f3,
              'F_zero': round(float(np.clip((3*f1-f3)/2, 0, 1)), 3)}
json.dump(out, open('/home/user/qpu-bigbang/qpu_batch3.json', 'w'), indent=0)
print(f"--- QPU {be.name} (RAW -> MIT) ---")
for nom, e in out['pubs'].items():
    if nom.startswith('CAL'): continue
    line = f"{nom:20s} "
    if 'P0' in e: line += f"P0={e['P0']}->{e['P0_mit']}"
    if 'P1' in e: line += f"P1={e['P1']}->{e['P1_mit']}"
    if 'coincidence' in e: line += f"C={e['coincidence']}->{e['coinc_mit']}"
    if 'P_retour' in e: line += f"R={e['P_retour']}"
    print(line)
print('fit_T1:', out['fit_T1'], 'fit_T2:', out['fit_T2'], 'ZNE:', out['zne'])
