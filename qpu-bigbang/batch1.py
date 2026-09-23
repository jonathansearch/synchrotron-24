#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""BATCH 1 — Big Bang + fun sur QPU (5 qubits, peu profond).
Construit les circuits (simu + QPU), prédictions simu exact.
Usage: python3 batch1.py   (simu)  |  import build_batch (QPU)
"""
import json
from collections import Counter
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 4000

def build_batch():
    b = []
    # BB1 Rien -> Tout : vide -> superposition uniforme (32 univers)
    q = QuantumCircuit(5, 5)
    q.h(range(5)); q.measure(range(5), range(5))
    b.append(('BB1-vide-tout', q))
    # BB2 Planck BANG : brouillage leger fige (reproductible)
    q = QuantumCircuit(5, 5)
    q.h(range(5))
    for i in range(4): q.cx(i, i + 1)
    for i, a in enumerate([0.5, 1.1, 2.3, 0.7, 1.9]): q.rz(a, i)
    for i in reversed(range(4)): q.cx(i, i + 1)
    q.measure(range(5), range(5))
    b.append(('BB2-planck-bang', q))
    # BB3 faux vide |11111> -> 2 pas Ising incline -> bulles de 0
    q = QuantumCircuit(5, 5)
    q.x(range(5))
    for _ in range(2):
        q.rx(0.3, range(5))
        for i in range(4): q.rzz(0.4, i, i + 1)
        q.rz(-0.1, range(5))
    q.measure(range(5), range(5))
    b.append(('BB3-faux-vide', q))
    # BB4 Kibble-Zurek : trempe rapide (1 pas fort) vs lente (3 pas doux)
    q = QuantumCircuit(5, 5)
    q.rx(np.pi / 2, range(5))
    for i in range(4): q.rzz(1.2, i, i + 1)
    q.measure(range(5), range(5))
    b.append(('BB4a-kz-rapide', q))
    q = QuantumCircuit(5, 5)
    q.rx(np.pi / 2, range(5))
    for th_zz, th_x in [(0.3, 1.0), (0.6, 0.5), (0.9, 0.2)]:
        q.rx(th_x, range(5))
        for i in range(4): q.rzz(th_zz, i, i + 1)
    q.measure(range(5), range(5))
    b.append(('BB4b-kz-lente', q))
    # GHZ5 : thermometre du QPU
    q = QuantumCircuit(5, 5)
    q.h(0)
    for i in range(4): q.cx(i, i + 1)
    q.measure(range(5), range(5))
    b.append(('GHZ5-sante', q))
    # BV : devine le code secret du chef s=101
    q = QuantumCircuit(4, 3)
    q.x(3); q.h(range(4))
    for i in (0, 2): q.cx(i, 3)
    q.h(range(3)); q.measure(range(3), range(3))
    b.append(('BV-secret-101', q))
    return b

def analyse(nom, counts):
    n = sum(counts.values())
    p = np.array([c / n for c in counts.values()])
    ent = float(-(p * np.log2(p)).sum())
    bs = list(counts.keys())
    ham = float(sum(s.count('1') * counts[s] for s in bs) / n)
    out = {'shots': n, 'entropie': round(ent, 3), 'hamming_moy': round(ham, 3)}
    if nom.startswith('BB3'):
        def bulles(s):
            return sum(1 for i, ch in enumerate(s) if ch == '0' and (i == 0 or s[i-1] == '1'))
        out['bulles_moy'] = round(sum(bulles(s) * counts[s] for s in bs) / n, 3)
        out['P_sans_bulle'] = round(counts.get('11111', 0) / n, 4)
    if nom.startswith('BB4'):
        def kinks(s):
            return sum(1 for i in range(4) if s[i] != s[i+1])
        out['kinks_moy'] = round(sum(kinks(s) * counts[s] for s in bs) / n, 3)
    if nom.startswith('GHZ5'):
        out['fidelite'] = round((counts.get('00000', 0) + counts.get('11111', 0)) / n, 4)
    if nom.startswith('BV'):
        top = max(counts, key=counts.get)
        out['devine'] = top[::-1]  # qiskit: bit 0 = gauche
        out['P_bonne'] = round(counts.get(top, 0) / n, 4)
    if nom.startswith('BB1'):
        top = max(counts, key=counts.get)
        out['univers_tire'] = int(top, 2)
    return out

if __name__ == '__main__':
    sam = StatevectorSampler(seed=7)
    res = {}
    print(f"{'circuit':16s} {'2q':>3s} {'prof':>4s}  observables simu")
    for nom, qc in build_batch():
        n2q = sum(1 for i in qc.data if len(i.qubits) == 2)
        pub = sam.run([(qc, None, SHOTS)], shots=SHOTS).result()[0].data
        c = pub[list(pub)[0]].get_counts()
        a = analyse(nom, c)
        res[nom] = {'counts': {k: int(v) for k, v in c.items()}, **a}
        print(f"{nom:16s} {n2q:>3d} {qc.depth():>4d}  {a}")
    json.dump(res, open('qpu-bigbang/simu_batch1.json', 'w'), indent=1)
    print('[simu] qpu-bigbang/simu_batch1.json OK')
