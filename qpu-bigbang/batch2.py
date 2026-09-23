#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""BATCH 2 — TOUT le programme synchrotron validé, en 1 job QPU (28 pubs).
S01 horizon/horloges/T1 | S02 Page-3q (tomo q0+q2) | S02b info migre |
S03 Loschmidt (U+Uinv vs U+U) | S04 Grover 0/1/2 | S05 Bell vs ++ |
S06a Bell voisins vs loin | S06b echo vs libre | WARP mur + canal + 5 bits.
S03b = batch1. Mesures EXPLICITES partout (pas de measure_all piege)."""
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector, partial_trace, entropy

SHOTS = 2000
ANGLES = [3.597, 1.77, 4.616, 6.235, 3.743, 0.526]

def build_batch2():
    b = []
    def M(c):
        c.measure(range(c.num_qubits), range(c.num_qubits)); return c
    c = QuantumCircuit(1, 1); c.x(0); c.reset(0); b.append(('S01-horizon', M(c)))
    for nom, th in [('S01-horloge-loin', np.pi), ('S01-horloge-mid', np.pi*np.sqrt(0.5)),
                    ('S01-horloge-pres', np.pi*np.sqrt(1-1/1.1))]:
        c = QuantumCircuit(1, 1); c.rx(th, 0); b.append((nom, M(c)))
    for nom, dly in [('S01-T1-court', 0), ('S01-T1-long', 300000)]:
        c = QuantumCircuit(1, 1); c.x(0); c.delay(dly, 0); b.append((nom, M(c)))
    def page_state():
        c = QuantumCircuit(3, 3)
        c.h(range(3))
        for L in range(2):
            for i in range(2): c.cx(i, i+1)
            for i in range(3): c.rz(ANGLES[L*3+i], i)
        return c
    for qb in (0, 2):
        for base in ('Z', 'X', 'Y'):
            c = page_state()
            if base == 'X': c.h(qb)
            elif base == 'Y': c.sdg(qb); c.h(qb)
            c.measure(qb, 0); b.append((f'S02-Page-q{qb}-{base}', c))
    b.append(('S02-Page-pop', M(page_state())))
    c = QuantumCircuit(3, 3); c.x(0); c.swap(0, 1); c.swap(1, 2); c.reset(0)
    b.append(('S02b-info-migre', M(c)))
    def U(c):
        c.h(range(3))
        for i in range(2): c.cx(i, i+1)
        for i, a in enumerate(ANGLES[:3]): c.rz(a, i)
    c = QuantumCircuit(3, 3); U(c)
    Ui = QuantumCircuit(3); U(Ui); c.compose(Ui.inverse(), inplace=True)
    b.append(('S03-loschmidt-planck', M(c)))
    c = QuantumCircuit(3, 3); U(c); U(c); b.append(('S03-loschmidt-gr', M(c)))
    def grover(n):
        c = QuantumCircuit(2, 2); c.h(range(2))
        for _ in range(n):
            c.cz(0, 1); c.h(range(2)); c.x(range(2)); c.cz(0, 1); c.x(range(2)); c.h(range(2))
        return M(c)
    for n in (0, 1, 2): b.append((f'S04-grover-{n}it', grover(n)))
    c = QuantumCircuit(2, 2); c.h(0); c.cx(0, 1); b.append(('S05-fantome-bell', M(c)))
    c = QuantumCircuit(2, 2); c.h(range(2)); b.append(('S05-vide-plus', M(c)))
    c = QuantumCircuit(2, 2); c.h(0); c.cx(0, 1); b.append(('S06a-lien-voisins', M(c)))
    c = QuantumCircuit(5, 2); c.h(0); c.cx(0, 4); c.measure(0, 0); c.measure(4, 1)
    b.append(('S06a-lien-loin', c))
    c = QuantumCircuit(1, 1); c.h(0); c.delay(300000, 0); c.x(0); c.delay(300000, 0)
    c.h(0); b.append(('S06b-ferme-echo', M(c)))
    c = QuantumCircuit(1, 1); c.h(0); c.delay(600000, 0); c.h(0)
    b.append(('S06b-ouvert-libre', M(c)))
    r = np.arange(8); f = 0.5*(np.tanh(1*(r+2.5))-np.tanh(1*(r-4.5)))
    c = QuantumCircuit(3, 3); c.initialize(np.sqrt(f/f.sum()), range(3))
    b.append(('WARP-etat-mur', M(c)))
    c = QuantumCircuit(1, 1); c.x(0); b.append(('WARP-canal-direct', M(c)))
    c = QuantumCircuit(5, 5); c.x(range(5)); b.append(('WARP-natif-5bits', M(c)))
    return b, (f/f.sum()).tolist()

def P1(counts, nq=1, qb=0):
    n = sum(counts.values())
    return sum(v for k, v in counts.items() if k[nq-1-qb] == '1')/n

def page_S(cZ, cX, cY):
    r = np.array([2*P1(cX,3,0)-1, 2*P1(cY,3,0)-1, 2*P1(cZ,3,0)-1])
    lam = (1+min(np.linalg.norm(r), 1))/2
    return float(-(lam*np.log2(lam)+(1-lam)*np.log2(1-lam))) if 0 < lam < 1 else 0.0

def analyse2(nom, counts):
    n = sum(counts.values())
    g = lambda k: counts.get(k, 0)/n
    if nom.startswith('S01-horloge') or nom.startswith('S01-T1') or nom == 'WARP-canal-direct':
        return {'P1': round(P1(counts), 4)}
    if nom == 'S01-horizon': return {'P0': round(g('0'), 4)}
    if nom == 'S02-Page-pop':
        p = np.array([v/n for v in counts.values()])
        return {'entropie': round(float(-(p*np.log2(p)).sum()), 3)}
    if nom.startswith('S02-Page-q'): return {'moy1': round(P1(counts, 3, 0), 4)}
    if nom == 'S02b-info-migre':
        return {'P_info_arrivee': round(sum(v for k, v in counts.items() if k[0]=='1')/n, 4),
                'P_masse_morte': round(sum(v for k, v in counts.items() if k[-1]=='0')/n, 4)}
    if nom.startswith('S03-loschmidt'): return {'P_retour': round(g('000'), 4)}
    if nom.startswith('S04-grover'): return {'P_capture': round(g('11'), 4)}
    if nom.startswith('S05') or nom.startswith('S06a'):
        return {'coincidence': round(g('00')+g('11'), 4)}
    if nom.startswith('S06b'): return {'P0_contraste': round(g('0'), 4)}
    if nom == 'WARP-natif-5bits': return {'P_intacts': round(g('11111'), 4)}
    if nom == 'WARP-etat-mur': return {'top': max(counts, key=counts.get)}
    return {}

def cherche_angles():
    best = None
    rng = np.random.default_rng(5)
    for t in range(60):
        a = rng.uniform(0, 2*np.pi, 6) if t else np.array(ANGLES + ANGLES)
        c = QuantumCircuit(3)
        c.h(range(3))
        for L in range(2):
            for i in range(2): c.cx(i, i+1)
            for i in range(3): c.rz(a[L*3+i], i)
        sv = Statevector(c)
        s0 = entropy(partial_trace(sv, [1, 2]), base=2)
        s2 = entropy(partial_trace(sv, [0, 1]), base=2)
        if best is None or min(s0, s2) > best[0]:
            best = (min(s0, s2), a, s0, s2)
    return best

if __name__ == '__main__':
    m, a, s0, s2 = cherche_angles()
    ANGLES = list(a)
    print(f'Page angles={np.round(a,3)} S0={s0:.3f} S2={s2:.3f}')
    sam = StatevectorSampler(seed=11)
    circs, mur = build_batch2()
    print(f'{len(circs)} pubs | mur: {[round(v,3) for v in mur]}')
    res = {}
    for nom, qc in circs:
        n2q = sum(1 for i in qc.data if len(i.qubits) == 2 and i.operation.name != 'barrier')
        pub = sam.run([(qc, None, SHOTS)], shots=SHOTS).result()[0].data
        c = pub[list(pub)[0]].get_counts()
        an = analyse2(nom, c)
        res[nom] = {'counts': {k: int(v) for k, v in c.items()}, **an}
        print(f'{nom:20s} 2q={n2q:>2d} d={qc.depth():>3d} {an}')
    print('Page S(q0)=%.3f S(q2)=%.3f' % (
        page_S(res['S02-Page-q0-Z']['counts'], res['S02-Page-q0-X']['counts'], res['S02-Page-q0-Y']['counts']),
        page_S(res['S02-Page-q2-Z']['counts'], res['S02-Page-q2-X']['counts'], res['S02-Page-q2-Y']['counts'])))
    json.dump({'angles_page': ANGLES, 'res': res}, open('qpu-bigbang/simu_batch2.json', 'w'), indent=0)
    print('[simu2] ok')
