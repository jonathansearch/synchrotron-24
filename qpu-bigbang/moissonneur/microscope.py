#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""MICROSCOPE : mort d'un ansatz couche par couche (exact vs bruit kingston)."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
from batch4 import init_murs, couche, analyse4, SHOTS
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
DEPTHS = list(range(0, 13))
LAM = 0.8
def build(nl):
    c = QuantumCircuit(6)
    init_murs(c)
    for _ in range(nl):
        couche(c, LAM)
    return c
exact = {}
for nl in DEPTHS:
    sc = Statevector.from_instruction(build(nl)).sample_counts(SHOTS)
    exact[nl] = analyse4('X', {k: int(v) for k, v in sc.items()})
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
be = service.backend('ibm_kingston')
sim = AerSimulator.from_backend(be)
pm = generate_preset_pass_manager(backend=be, optimization_level=1, initial_layout=[10, 11, 18, 9, 31, 30])
noisy = {}
for nl in DEPTHS:
    m = build(nl).copy()
    m.measure_all()
    counts = sim.run(pm.run(m), shots=SHOTS, seed_simulator=7).result().get_counts()
    noisy[nl] = analyse4('X', {k: int(v) for k, v in counts.items()})
json.dump({'exact': exact, 'noisy_kingston': noisy},
          open('/home/user/synchrotron-24/qpu-bigbang/moissonneur/microscope.json', 'w'), indent=0)
print('nl | zz_exact zz_noisy | MI_exact MI_noisy | H_exact H_noisy')
for nl in DEPTHS:
    e, n = exact[nl], noisy[nl]
    print(f"{nl:2d} | {e['zz_contact']:+.3f} {n['zz_contact']:+.3f} | {e['MI_LR']:.3f} {n['MI_LR']:.3f} | {e['entropie']:.3f} {n['entropie']:.3f}")
print('[microscope] ok')
