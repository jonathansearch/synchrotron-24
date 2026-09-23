#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""MOISSONNEUR v3 = RADAR : profondeur clinique (mort du signal vs couches).
lam=0.8 fixe, nl=1..8 + T0 + libre + echo + Page-q3. 23 pubs/ronde x3."""
import sys
sys.path.insert(0, '/home/user/synchrotron-24/qpu-bigbang')
from batch4 import init_murs, couche, analyse4, SHOTS
from qiskit import QuantumCircuit
NLS = [1, 2, 3, 4, 6, 8]
LAM = 0.8
def pop_nl(lam, nl, echo=False):
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
def page_nl(qb, lam, nl, base):
    c = QuantumCircuit(6, 6)
    init_murs(c)
    if nl:
        u = QuantumCircuit(6)
        for _ in range(nl):
            couche(u, lam)
        c.compose(u, inplace=True)
    if base == 'X': c.h(qb)
    elif base == 'Y': c.sdg(qb); c.h(qb)
    c.measure(qb, 0)
    return c
def build_radar(rounds=3):
    base = [('T0-init', pop_nl(0.0, 0)), ('LIBRE-4L', pop_nl(0.0, 4)),
            ('ECHO-4L', pop_nl(LAM, 4, True))]
    base += [(f'D{n}L', pop_nl(LAM, n)) for n in NLS]
    for tag, nl in (('t0', 0), ('2L', 2), ('4L', 4), ('8L', 8)):
        for b in 'XYZ':
            base.append((f'PAGE-q3-{tag}-{b}', page_nl(3, LAM, nl, b)))
    for prep in ('0', '1'):
        c = QuantumCircuit(6, 6)
        if prep == '1': c.x(3)
        c.measure(3, 0)
        base.append((f'CALq3-{prep}', c))
    pubs = []
    for r in range(rounds):
        for nom, qc in base:
            pubs.append((f'R{r}-{nom}', qc))
    return pubs, [n for n, _ in base]
if __name__ == '__main__':
    from qiskit.primitives import StatevectorSampler
    sam = StatevectorSampler(seed=51)
    pubs, base = build_radar(1)
    for nom, qc in pubs:
        if nom.startswith('R0-D') or nom.startswith('R0-T0') or nom.startswith('R0-L') or nom.startswith('R0-E'):
            pub = sam.run([(qc, None, SHOTS)], shots=SHOTS).result()[0].data
            c = pub[list(pub)[0]].get_counts()
            print(f'{nom[3:]:10s} {analyse4(nom[3:], c)}')
    print('[simu-radar] logique ok')
