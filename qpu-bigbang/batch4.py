#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""BATCH 4 — COLLISIONNEUR : 2 murs tanh (3+3 qubits) + contact RZZ(lambda).
CALIBRAGE (sonde exacte pre-tir) : MI(L:R) 0.003->0.022->0.060 (x20) et
<Z2Z3>c 0.05->0.14->0.23 (10-sigma) pour lam 0.2/0.6/1.2 ; au-dela (lam>=2,
4 couches) SURCUISSON (revival unitaire : MI->0.002). Brutal = lam 1.2 x 2L.
OBSERVABLES : PRIMAIRES = zz_contact (10-sigma) + Page tomo 1q + REM (matche
simu au %) ; SECONDAIRES = MI (biais shot ~0.016, differentiel seul) +
Hellinger ; REFUTE = beta1-Hamming (sature ~100, aveugle, voir
qpu-collision/DETECTEURS_INVALIDES.md). Layout fixe 6-ch-qubits (reproductible).
Controles : libre (lam=0 -> 0) + echo (+U-U -> retour).
Brutalite : lambda 0.2 (doux) / 0.6 / 1.2 (BRUTAL), 2 couches Trotter.
Detecteur de forme : Page (tomo 1q), beta1-graphe (cycles de Hamming),
echo (elasticite). 23 pubs, 1 job."""
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 2000
R = np.arange(8)
F = 0.5*(np.tanh(1*(R+2.5))-np.tanh(1*(R-4.5)))
AMP = np.sqrt(F/F.sum())

def init_murs(c):
    c.initialize(AMP, [0, 1, 2])
    c.initialize(AMP, [3, 4, 5])

def couche(c, lam):
    c.rx(0.2, range(6))
    for a, b in ((0, 1), (1, 2), (3, 4), (4, 5)):
        c.rzz(0.2, a, b)
    if lam:
        c.rzz(lam, 2, 3)  # LE CONTACT (collision)

def build_batch4():
    b = []
    def pop(nom, lam, nl=2, echo=False):
        c = QuantumCircuit(6, 6)
        init_murs(c)
        u = QuantumCircuit(6)
        for _ in range(nl):
            couche(u, lam)
        c.compose(u, inplace=True)
        if echo:
            c.compose(u.inverse(), inplace=True)
        c.measure(range(6), range(6))
        b.append((nom, c))
    pop('T0-init', 0.0, 0)
    for nom, lam in (('T2-doux', 0.2), ('T2-mid', 0.6), ('T2-brutal', 1.2)):
        pop(nom, lam)
    pop('CTRL-libre', 0.0)
    pop('ECHO-mid', 0.6, 2, True)
    c = QuantumCircuit(3, 3)
    c.initialize(AMP, range(3))
    c.measure(range(3), range(3))
    b.append(('CTRL-1mur', c))
    for qb in (0, 3):
        for tm, lam in (('t0', 0.0), ('mid', 0.6), ('brutal', 1.2)):
            for base in ('Z', 'X', 'Y'):
                c = QuantumCircuit(6, 6)
                init_murs(c)
                if lam:
                    u = QuantumCircuit(6)
                    for _ in range(2):
                        couche(u, lam)
                    c.compose(u, inplace=True)
                if base == 'X': c.h(qb)
                elif base == 'Y': c.sdg(qb); c.h(qb)
                c.measure(qb, 0)
                b.append((f'PAGE-q{qb}-{tm}-{base}', c))
    for qb in (0, 3):
        for prep in ('0', '1'):
            c = QuantumCircuit(6, 6)
            if prep == '1': c.x(qb)
            c.measure(qb, 0)
            b.append((f'CALq{qb}-{prep}', c))
    return b

def P1(counts, nq=1, qb=0):
    n = sum(counts.values())
    return sum(v for k, v in counts.items() if k[nq-1-qb] == '1')/n

def page_S(cZ, cX, cY, nq=6):
    r = np.array([2*P1(cX, nq, 0)-1, 2*P1(cY, nq, 0)-1, 2*P1(cZ, nq, 0)-1])
    lam = (1+min(np.linalg.norm(r), 1))/2
    return float(-(lam*np.log2(lam)+(1-lam)*np.log2(1-lam))) if 0 < lam < 1 else 0.0

def beta1_hamming(counts, thr):
    nodes = [k for k, v in counts.items() if v >= thr]
    S = set(nodes)
    parent = {k: k for k in nodes}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    E = 0
    for k in nodes:
        for i in range(len(k)):
            m = k[:i]+('1' if k[i] == '0' else '0')+k[i+1:]
            if m in S and m > k:
                E += 1
                rk, rm = find(k), find(m)
                if rk != rm: parent[rk] = rm
    C = len({find(k) for k in nodes}) if nodes else 0
    return E-len(nodes)+C, len(nodes)

def hellinger(c1, c2):
    n1, n2 = sum(c1.values()), sum(c2.values())
    keys = set(c1) | set(c2)
    return float(1-sum(((c1.get(k, 0)/n1)*(c2.get(k, 0)/n2))**0.5 for k in keys))

def analyse4(nom, counts):
    if nom.startswith('PAGE'):
        return {'moy1': round(P1(counts, 6, 0), 4)}
    if nom.startswith('CAL'):
        return {'calib': True}
    n = sum(counts.values())
    ent = float(-sum((v/n)*np.log2(v/n) for v in counts.values()))
    out = {'entropie': round(ent, 3)}
    if len(next(iter(counts))) == 6:
        z = np.array([1 if k[5-2] == '0' else -1 for k in counts])
        w = np.array([1 if k[5-3] == '0' else -1 for k in counts])
        v = np.array([c/n for c in counts.values()])
        out['zz_contact'] = round(float((v*z*w).sum()-(v*z).sum()*(v*w).sum()), 4)
        p = np.zeros(64)
        for k, c in counts.items():
            p[int(k, 2)] = c/n
        def H(q):
            q = q[q > 0]
            return float(-(q*np.log2(q)).sum())
        out['MI_LR'] = round(H(p.reshape(8, 8).sum(1))+H(p.reshape(8, 8).sum(0))-H(p), 4)
    return out

def unfold1_mit(counts, cal0, cal1, nq=6):
    n = sum(counts.values())
    p = np.array([sum(v for k, v in counts.items() if k[nq-1] == b)/n for b in ('0', '1')])
    n0, n1 = sum(cal0.values()), sum(cal1.values())
    M = np.array([[sum(v for k, v in cal0.items() if k[nq-1] == b)/n0 for b in ('0', '1')],
                  [sum(v for k, v in cal1.items() if k[nq-1] == b)/n1 for b in ('0', '1')]]).T
    q, *_ = np.linalg.lstsq(M, p, rcond=None)
    return float(np.clip(q[1], 0, 1))

def page_S_mit(cZ, cX, cY, cal0, cal1, nq=6):
    r = np.array([2*unfold1_mit(c, cal0, cal1, nq)-1 for c in (cX, cY, cZ)])
    lam = (1+min(np.linalg.norm(r), 1))/2
    return float(-(lam*np.log2(lam)+(1-lam)*np.log2(1-lam))) if 0 < lam < 1 else 0.0

if __name__ == '__main__':
    sam = StatevectorSampler(seed=21)
    circs = build_batch4()
    print(f'{len(circs)} pubs')
    res = {}
    for nom, qc in circs:
        n2q = sum(1 for i in qc.data if len(i.qubits) == 2 and i.operation.name != 'barrier')
        pub = sam.run([(qc, None, SHOTS)], shots=SHOTS).result()[0].data
        c = pub[list(pub)[0]].get_counts()
        res[nom] = {'counts': {k: int(v) for k, v in c.items()}, **analyse4(nom, c)}
        print(f'{nom:18s} 2q={n2q:>2d} d={qc.depth():>3d} {analyse4(nom, c)}')
    c0 = res['T0-init']['counts']
    print('--- Hellinger vs T0 / beta1-graphe (thr 2/5/10) ---')
    for nom in ('T0-init', 'T2-doux', 'T2-mid', 'T2-brutal', 'CTRL-libre', 'ECHO-mid'):
        cc = res[nom]['counts']
        b1 = [beta1_hamming(cc, t)[0] for t in (2, 5, 10)]
        print(f'{nom:12s} H={hellinger(c0, cc):.3f} b1={b1} noeuds={beta1_hamming(cc, 2)[1]}')
    for tm in ('t0', 'mid', 'brutal'):
        sq = [page_S(res[f'PAGE-q{qb}-{tm}-Z']['counts'], res[f'PAGE-q{qb}-{tm}-X']['counts'],
                     res[f'PAGE-q{qb}-{tm}-Y']['counts']) for qb in (0, 3)]
        print(f'Page S(q0,q3) {tm}: {[round(v,3) for v in sq]}')
    json.dump(res, open('synchrotron-24/qpu-bigbang/simu_batch4.json', 'w'), indent=0)
    print('[simu4] ok')
