# QPU-BIGBANG — campagne de mesures quantiques 2026
On mesure la cellule de collision (2 murs + contact λ + couches) sur vrais QPU
et sims bruitées, avec témoins (T0/LIBRE/ÉCHO/CAL) à chaque ronde.

## Campagnes
| Dossier/fichiers | Contenu |
|---|---|
| batch1-3.py + qpu_batch1-3.json | GHZ, KZ-5q, Grover, Bell, Page, tomo (65 pubs IBM) |
| batch4.py + SYNTHESE_4_BATCHS.md | collision λ-sweep + écho (29 pubs, kingston) |
| qpu-collision/ | archive batch4 + tickets (COLLISION clos, RIPS ouvert) |
| moissonneur/ | exploitation : datasheets, collecteur, radar, microscope |
| diag.py | sonde qubits (a trouvé q121/q146 morts) |

## Résultats (détails : SYNTHESE_MOISSONS.md)
- Contact zz : 5σ, monotone en λ puis plateau (88% théorie sur kingston).
- Page S_mit : cloche, pic λ≈0.8 (σ 0.005), revival mid>brutal.
- Dérive session ~0.04 >> σ intra ~0.01 → autocalibration obligatoire.
- Microscope 0-12L : MI meurt avant zz ; H exacte creuse, H bruit sature.
- Points figés : Page@λ0.8 (métrologie), zz@λ≥1.2 (détection 8σ vs témoin).

## Reproduire (sims, $0)
`pip install qiskit qiskit-aer` puis `python3 simu_batchN.py` / `moissonneur/microscope.py`
(sans token IBM : le microscope a besoin des props backend, sinon tout est local).
Tirs QPU : voir moissonneur/QBRAID.md (devis) et moissonneur/AWS.md (Braket).

## Licence
MIT (racine du dépôt).
