#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tire batch1 sur vrai QPU IBM. Clé via env IBM_TOKEN (jamais sur disque)."""
import json, os, sys
sys.path.insert(0, '/home/user/qpu-bigbang')
from batch1 import build_batch, analyse, SHOTS
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
circs = [(n, pm.run(qc)) for n, qc in build_batch()]
for n, qc in circs:
    n2q = sum(1 for i in qc.data if len(i.qubits) == 2)
    print(f'  {n}: depth={qc.depth()} 2q={n2q}', flush=True)
job = Sampler(mode=be).run([c for _, c in circs], shots=SHOTS)
open('/home/user/qpu-bigbang/job1_id.txt', 'w').write(f'{job.job_id()} {be.name}')
print('JOB:', job.job_id(), flush=True)
try:
    res = job.result(timeout=1550)
except Exception as e:
    print('ENCORE_EN_FILE:', type(e).__name__, '| job_id sauve, relancer repoll',
          flush=True)
    raise SystemExit(2)
out = {}
for (nom, _), pub in zip(circs, res):
    counts = pub.data[list(pub.data)[0]].get_counts()
    out[nom] = {'counts': {k: int(v) for k, v in counts.items()},
                **analyse(nom, counts)}
json.dump(out, open('/home/user/qpu-bigbang/qpu_batch1.json', 'w'), indent=1)
print(f"--- QPU {be.name} ---")
for nom, a in out.items():
    print(f"{nom:16s} {a}")
