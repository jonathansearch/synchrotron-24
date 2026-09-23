#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Autopsie hardware SANS job QPU (proprietes + choix qubits). Cle via env."""
import os, numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel='ibm_quantum_platform',
                               token=os.environ['IBM_TOKEN'])
bes = [(b, b.status().pending_jobs) for b in service.backends()
       if b.status().operational and b.num_qubits >= 5]
for b, q in sorted(bes, key=lambda t: t[1])[:6]:
    print('backend:', b.name, 'file:', q)
be = service.backend('ibm_kingston')
print('CIBLE:', be.name, '| dt =', be.dt, 's')
P = be.properties()
def safe(f, i):
    try: return f(i)
    except Exception: return np.nan
ro = np.array([safe(P.readout_error, i) for i in range(be.num_qubits)])
t1 = np.array([safe(P.t1, i) for i in range(be.num_qubits)])
t2 = np.array([safe(P.t2, i) for i in range(be.num_qubits)])
for nom, v, u in [('readout_err', ro, ''), ('T1', t1*1e6, 'us'), ('T2', t2*1e6, 'us')]:
    o = np.argsort(v)
    print(f'{nom}: med={np.nanmedian(v):.4g}{u} | 3 meilleurs: ' +
          ', '.join(f'q{i}={v[i]:.4g}' for i in o[:3]) + ' | 3 pires: ' +
          ', '.join(f'q{i}={v[i]:.4g}' for i in o[-3:]))
g2 = []
for (a, b_) in be.coupling_map.get_edges():
    try: g2.append(P.gate_error('cz', [a, b_]))
    except Exception: pass
print(f'2q gate_err: med={np.median(g2):.4g} max={np.max(g2):.4g} n={len(g2)}')
ok = ~np.isnan(ro); o = np.argsort(np.where(ok, ro, 9))
print('TOP qubits (faible readout):', [int(i) for i in o[:8]])
