#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""MOISSONNEUR v2 : lambda fin 0.4-1.6 (7pts) x 5 rondes x 2 backends.
24 pubs/ronde : T0 + libre + echo + 7 lam + Page-q3(4 lam x XYZ) + CAL x2."""
import sys
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
from batch4 import init_murs, couche, analyse4, SHOTS
from qiskit import QuantumCircuit
LAMBDAS = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
PAGE_LAMS = {'t0': 0.0, 'l06': 0.6, 'l10': 1.0, 'l14': 1.4}
def pop(lam, nl=2, echo=False):
    c = QuantumCircuit(6, 6)
    init_murs(c)
    u = QuantumCircuit(6)
    for _ in range(nl):
        couche(u, lam)
    c.compose(u, inplace=True)
    if echo:
        c.compose(u.inverse(), inplace=True)
    c.measure(range(6), range(6))
    return c
def page_circuit(qb, lam, base):
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
    return c
def cal_circuit(qb, prep):
    c = QuantumCircuit(6, 6)
    if prep == '1': c.x(qb)
    c.measure(qb, 0)
    return c
def build_harvest2(rounds=5):
    base = [('T0-init', pop(0.0, 0)), ('CTRL-libre', pop(0.0)),
            ('ECHO-mid', pop(0.6, 2, True))]
    base += [(f'T2-l{int(l*10)}', pop(l)) for l in LAMBDAS]
    for tag, lam in PAGE_LAMS.items():
        for b in 'XYZ':
            base.append((f'PAGE-q3-{tag}-{b}', page_circuit(3, lam, b)))
    base += [('CALq3-0', cal_circuit(3, '0')), ('CALq3-1', cal_circuit(3, '1'))]
    pubs = []
    for r in range(rounds):
        for nom, qc in base:
            pubs.append((f'R{r}-{nom}', qc))
    return pubs, [n for n, _ in base]
if __name__ == '__main__':
    from qiskit.primitives import StatevectorSampler
    sam = StatevectorSampler(seed=41)
    pubs, base = build_harvest2(1)
    for nom, qc in pubs:
        pub = sam.run([(qc, None, SHOTS)], shots=SHOTS).result()[0].data
        c = pub[list(pub)[0]].get_counts()
        if nom.startswith('R0-T2') or nom.startswith('R0-T0') or nom.startswith('R0-C') or nom.startswith('R0-E'):
            print(f'{nom[3:]:12s} {analyse4(nom[3:], c)}')
    print('[simu-h2] logique ok')
