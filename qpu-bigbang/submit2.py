#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire batch2 (28 pubs, TOUT le programme) en 1 job QPU. Cle via env IBM_TOKEN."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/qpu-bigbang')
from batch2 import build_batch2, analyse2, page_S, SHOTS
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

service = QiskitRuntimeService(channel='ibm_quantum_platform',
                               token=os.environ['IBM_TOKEN'])
bes = [b for b in service.backends()
       if b.status().operational and b.num_qubits >= 5]
bes.sort(key=lambda b: b.status().pending_jobs)
for b in bes[:8]:
    print('backend:', b.name, b.num_qubits, 'q, file:', b.status().pending_jobs,
          flush=True)
be = bes[0]
print('CHOIX:', be.name, flush=True)
pm = generate_preset_pass_manager(backend=be, optimization_level=1)
circs, mur = build_batch2()
tc = [(n, pm.run(qc)) for n, qc in circs]
for n, qc in tc:
    n2q = sum(1 for i in qc.data if len(i.qubits) == 2
              and i.operation.name != 'barrier')
    print(f'  {n}: depth={qc.depth()} 2q={n2q}', flush=True)
job = Sampler(mode=be).run([c for _, c in tc], shots=SHOTS)
open('/home/user/qpu-bigbang/job2_id.txt', 'w').write(f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, flush=True)
    raise SystemExit(2)
out = {}
for (nom, _), pub in zip(tc, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    out[nom] = {'counts': {k: int(v) for k, v in counts.items()},
                **analyse2(nom, counts)}
try:
    out['_page'] = {'S_q0': round(page_S(out['S02-Page-q0-Z']['counts'],
                                         out['S02-Page-q0-X']['counts'],
                                         out['S02-Page-q0-Y']['counts']), 3),
                    'S_q2': round(page_S(out['S02-Page-q2-Z']['counts'],
                                         out['S02-Page-q2-X']['counts'],
                                         out['S02-Page-q2-Y']['counts']), 3)}
except Exception as e:
    out['_page'] = {'erreur': str(e)}
try:
    mc = out['WARP-etat-mur']['counts']; n = sum(mc.values())
    mv = np.array([mc.get(format(i, '03b'), 0)/n for i in range(8)])
    out['_mur'] = {'corr': round(float(np.corrcoef(mv, mur)[0, 1]), 3)}
except Exception as e:
    out['_mur'] = {'erreur': str(e)}
json.dump(out, open('/home/user/qpu-bigbang/qpu_batch2.json', 'w'), indent=0)
print(f"--- QPU {be.name} ---")
for nom, a in out.items():
    if not nom.startswith('_'):
        print(f"{nom:20s} {a}")
print('PAGE:', out['_page'], 'MUR:', out['_mur'])
