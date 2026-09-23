#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""BATCH 3 — revanche sur les echoues (30 pubs, 1 job, layout fixe, REM).
Delais en VRAIES microsecondes (dt backend). Barrieres anti-optimiseur.
S06b: Ramsey sweep + echo/CPMG@50us | S01: T1 sweep + reset x1-5 + horloge |
S05/S06a sur bons qubits | S03: ZNE x1/x3. Calibration readout incluse."""
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 2000
ANG = [3.597, 1.77, 4.616, 6.235, 3.743, 0.526]

def D(dt, us):
    return int(us*1e-6/dt)

def build_batch3(dt):
    b = []
    d = lambda us: D(dt, us)
    # --- calibration readout (memes qubits fixes que les tests) ---
    c = QuantumCircuit(1, 1); c.measure(0, 0); b.append(('CAL-1q-0', c))
    c = QuantumCircuit(1, 1); c.x(0); c.measure(0, 0); b.append(('CAL-1q-1', c))
    for prep in ('00', '01', '10', '11'):
        c = QuantumCircuit(2, 2)
        if prep[1] == '1': c.x(0)
        if prep[0] == '1': c.x(1)
        c.measure(range(2), range(2)); b.append((f'CAL-2q-{prep}', c))
    # --- S06b : Ramsey sweep + echo + CPMG ---
    for t in (0, 10, 25, 50, 100):
        c = QuantumCircuit(1, 1); c.h(0); c.barrier(0); c.delay(d(t), 0)
        c.barrier(0); c.h(0); c.measure(0, 0)
        b.append((f'S06b-ramsey-{t}us', c))
    c = QuantumCircuit(1, 1); c.h(0); c.barrier(0); c.delay(d(25), 0); c.barrier(0)
    c.x(0); c.barrier(0); c.delay(d(25), 0); c.barrier(0); c.h(0); c.measure(0, 0)
    b.append(('S06b-echo-50us', c))
    c = QuantumCircuit(1, 1); c.h(0)
    for w in (12.5, 25, 12.5):
        c.barrier(0); c.delay(d(w), 0); c.barrier(0); c.x(0)
    c.barrier(0); c.h(0); c.measure(0, 0)
    b.append(('S06b-cpmg-50us', c))
    # --- S01 : T1 sweep ---
    for t in (0, 25, 50, 100, 200):
        c = QuantumCircuit(1, 1); c.x(0); c.barrier(0); c.delay(d(t), 0)
        c.barrier(0); c.measure(0, 0)
        b.append((f'S01-T1-{t}us', c))
    # --- S01 : init + reset x1/x2/x3/x5 ---
    c = QuantumCircuit(1, 1); c.measure(0, 0); b.append(('S01-INIT', c))
    for k in (1, 2, 3, 5):
        c = QuantumCircuit(1, 1); c.x(0)
        for _ in range(k): c.barrier(0); c.reset(0)
        c.measure(0, 0); b.append((f'S01-RESET-x{k}', c))
    # --- S01 : horloge pres (REM ensuite) ---
    c = QuantumCircuit(1, 1); c.rx(np.pi*np.sqrt(1-1/1.1), 0); c.measure(0, 0)
    b.append(('S01-horloge-pres', c))
    # --- S05 / S06a sur paire fixe ---
    c = QuantumCircuit(2, 2); c.h(0); c.cx(0, 1); c.measure(range(2), range(2))
    b.append(('S05-fantome-bell', c))
    c = QuantumCircuit(2, 2); c.h(range(2)); c.measure(range(2), range(2))
    b.append(('S05-vide-plus', c))
    c = QuantumCircuit(2, 2); c.h(0); c.cx(0, 1); c.measure(range(2), range(2))
    b.append(('S06a-lien-fixe', c))
    # --- S03 : ZNE (barrieres empechent cx^3 -> cx) ---
    def U(c, rep=1):
        c.h(range(3))
        for i in range(2):
            for _ in range(rep):
                c.cx(i, i+1); c.barrier(i, i+1)
        for i, a in enumerate(ANG[:3]): c.rz(a, i)
    c = QuantumCircuit(3, 3); U(c); Ui = QuantumCircuit(3); U(Ui)
    c.compose(Ui.inverse(), inplace=True)
    c.measure(range(3), range(3)); b.append(('S03-planck-x1', c))
    c = QuantumCircuit(3, 3); U(c, 3); U3 = QuantumCircuit(3); U(U3, 3)
    c.compose(U3.inverse(), inplace=True)
    c.measure(range(3), range(3)); b.append(('S03-planck-x3', c))
    c = QuantumCircuit(3, 3); U(c); U(c)
    c.measure(range(3), range(3)); b.append(('S03-gr-x1', c))
    return b

def P1(counts, nq=1, qb=0):
    n = sum(counts.values())
    return sum(v for k, v in counts.items() if k[nq-1-qb] == '1')/n

def analyse3(nom, counts):
    n = sum(counts.values())
    g = lambda k: counts.get(k, 0)/n
    if nom.startswith('CAL'): return {'calib': True}
    if nom.startswith('S06b') or nom in ('S01-INIT',) or nom.startswith('S01-RESET'):
        return {'P0': round(g('0'), 4)}
    if nom.startswith('S01-T1') or nom == 'S01-horloge-pres':
        return {'P1': round(P1(counts), 4)}
    if nom.startswith('S05') or nom.startswith('S06a'):
        return {'coincidence': round(g('00')+g('11'), 4)}
    if nom.startswith('S03'): return {'P_retour': round(g('000'), 4)}
    return {}

def unfold1(counts, cal0, cal1):
    n = sum(counts.values())
    p = np.array([counts.get('0', 0), counts.get('1', 0)])/n
    n0 = sum(cal0.values()); n1 = sum(cal1.values())
    M = np.array([[cal0.get('0', 0)/n0, cal1.get('0', 0)/n1],
                  [cal0.get('1', 0)/n0, cal1.get('1', 0)/n1]])
    q, *_ = np.linalg.lstsq(M, p, rcond=None)
    return {'P0_mit': round(float(np.clip(q[0], 0, 1)), 4),
            'P1_mit': round(float(np.clip(q[1], 0, 1)), 4)}

def unfold2(counts, cals):
    keys = ['00', '01', '10', '11']
    n = sum(counts.values())
    p = np.array([counts.get(k, 0) for k in keys])/n
    M = np.zeros((4, 4))
    for j, prep in enumerate(keys):
        nj = sum(cals[prep].values())
        for i, k in enumerate(keys):
            M[i, j] = cals[prep].get(k, 0)/nj
    q, *_ = np.linalg.lstsq(M, p, rcond=None)
    q = np.clip(q, 0, 1)
    return {'coinc_mit': round(float(q[0]+q[3]), 4)}

if __name__ == '__main__':
    sam = StatevectorSampler(seed=3)
    circs = build_batch3(4e-9)
    print(f'{len(circs)} pubs')
    res = {}
    for nom, qc in circs:
        pub = sam.run([(qc, None, SHOTS)], shots=SHOTS).result()[0].data
        c = pub[list(pub)[0]].get_counts()
        an = analyse3(nom, c)
        res[nom] = {'counts': {k: int(v) for k, v in c.items()}, **an}
        print(f'{nom:20s} {an}')
    u = unfold1(res['S01-horloge-pres']['counts'], res['CAL-1q-0']['counts'],
                res['CAL-1q-1']['counts'])
    print('REM-test horloge:', u, '(cible P1=0.207)')
    json.dump(res, open('qpu-bigbang/simu_batch3.json', 'w'), indent=0)
    print('[simu3] ok')
