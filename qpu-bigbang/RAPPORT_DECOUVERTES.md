# RAPPORT DE DÉCOUVERTES — campagne QPU 2026
*Cellule de collision 6q : 2 murs + contact λ + couches. ~400 pubs IBM (batchs 1-4,
moissons 1-2) + sims bruitées (radar, microscope). Méthode : SANS NEURONES, témoins
à chaque ronde, simu exacte en référence. Licence MIT.*

## 0. Résumé en 30 secondes
| # | Découverte | Preuve |
|---|---|---|
| D1 | Le contact zz existe (signal réel, pas bruit) | 5σ vs témoins ; monotone en λ sur 2 backends |
| D2 | L'inversion batch4 (mid>brutal) = bruit | moisson1 tranche : brutal>mid **3/3 rondes** (3.3σ) |
| D3 | Page en cloche + revival (prédit puis mesuré) | pic λ≈0.8 (0.78, 2 backends) ; mid>brutal .761 vs .613 |
| D4 | Chaque backend a sa réponse (facteur 1.4) + dérive session 0.04 | → autocalibration + calibrage/backend obligatoires |
| D5 | Horizons de mort : ≥8L (radar) / ~14L (microscope) ; **MI meurt avant zz** | loi du trio (zz, MI, H) — Page/H seule ment |
| D6 | Détecteurs invalidés + qubits morts cartographiés | β1-Hamming jeté ; q113/q121/q146 morts (diag) |
| D7 | DOSIMÉTRIE DE L'INTRICATION = problème nouveau | P1 opérateurs, P2 radar/microscope, P3 benchmark |

## 1. L'instrument
Cellule 6 qubits : murs préparés (AMP⊗AMP), couches rx+rzz+contact rzz(λ) sur (2,3).
Détecteurs : zz_contact (corrélateur au contact), MI_L/R, S_mit Page (tomo 1q mit),
H totale, écho (couches+H+H† : doit revenir à ~0). Témoins : T0, LIBRE (λ=0),
CAL. Chaînes qubits forcées + loggées (ex. K [10,11,18,9,31,30]).

## 2. D1 — le contact existe (batch4 + moissons)
Batch4 (marrakesh, n=1, job dapu6sic505c73cir6f0) : doux .049 / mid .107 /
brutal .080 contre libre −.001, écho −.010, T0 .028 → signal net, témoins ~0.
Moisson2 (n=5+5) : zz(λ) monotone → plateau, **2 backends** :
- marrakesh : .043/.069/.093/.125/.153/.144/.160 (60% théorie)
- kingston : .091/.142/.158/.214/.204/.217/.221 (**88% théorie**)

## 3. D2 — l'inversion batch4 tranchée (moisson1, kingston, 51 pubs, n=3)
Batch4 (n=1) montrait mid>brutal (.107 vs .080). Bruit ou physique ?
Moisson1 : brutal .125±.015 > mid .072±.006, **3 rondes sur 3** (3.3σ) = simu.
Verdict : **l'inversion était du bruit** (n=1). Leçon : rien sous n=3.

## 4. D3 — Page en cloche + revival (prédiction → mesure)
Simu exacte : S_q3 cloche, pic 0.798 @λ0.8 ; revival mid>brutal.
Mesure moisson2 (pic 0.78, **2 backends identiques**) :
- Page M : t0 .274±.025 / .763±.005 / .779±.010 / .543±.016
- Page K : t0 .225±.010 / .785±.024 / .783±.008 / .520±.024
Mesure moisson1 : Page mid .761±.005 > brutal .613±.018 (revival confirmé).
**Points figés** : Page@λ0.8 = métrologie (σ 0.005) ; zz@λ≥1.2 = détection (8σ).

## 5. D4 — backends + dérive (→ autocalibration)
- Facteur kingston/marrakesh ≈ **1.4** en zz → calibrage par backend.
- Dérive inter-session ~**0.04** >> σ intra-ronde ~0.01 → session témoin + autocal.
- Trigger collecteur à la **médiane** (1 ronde bruitée/5 : σ 0.040 @l8-M).
- Débit mesuré ~2000-2600 shots/s (mur) ; files variables (0 à 2h !).

## 6. D5 — radar + microscope (sims bruitées, modèles K/M réels)
- **RADAR** zz(nl) : exact D2 .18 / D3 .38 / D4 .46 / D6 .29 / D8 .31 (pic + revival).
  Sous bruit : signal vivant à 8L (zz .27 >> plancher .03) → **horizon ≥ 8L**.
  Modèle bruit = 87-99% de l'exact (kingston) ; optimiste pour marrakesh.
- **MICROSCOPE** 0-12L : zz pic 4L (.46/.40) → 12L (.13/.16), horizon ~14L ;
  **MI meurt avant zz** (12L : .13 exact / .07 bruit) ; H exacte creuse à 7L
  (revival 4.44), H bruit monte (5.25, pompe entropique).
- **Loi du trio** : (zz, MI, H) obligatoire — Page/H seule confond bruit et
  brouillage. Mort-unitaire (revival) vs mort-bruit (pompe) distinguées.

## 7. D6 — ce qu'on a jeté et cartographié (négatif = science)
- **β1-Hamming INVALIDÉ** comme détecteur (ticket DETECTEURS_INVALIDES.md).
- Sonde diag : qubits morts **q113/q121/q146** → sélection de chaîne forcée.
- Surcuisson λ (sonde exacte) : trop de λ tue le signal (S au-delà du pic).

## 8. D7 — le problème nouveau : DOSIMÉTRIE DE L'INTRICATION
Personne ne dose λ/profondeur (QV = chiffre abstrait). Notre instrument donne
des courbes dose→réponse → datasheet (v1 : 2 backends, n=14 ; v2 : +radar).
- **P1 opérateurs** : canari 6q + santé vivante + carte défauts/chip.
- **P2 utilisateurs** : RADAR (« à quelle profondeur mon algo meurt AUJOURD'HUI ? »)
  + MICROSCOPE d'ansatz (VQE/QAOA : voir où ça meurt).
- **P3 hardware** : benchmark applicatif calibré (des courbes, pas un chiffre).
Détail : moissonneur/PROBLEME.md. Honnêteté : pas de stockage (pas de qubits
volants en supra) → l'appareil est un OSCILLOSCOPE, pas une usine.

## 9. Limites (à lire avant de crier au Nobel)
- N=6 qubits, n≤5/ronde, 2 backends supraconducteurs (IBM).
- Cloud = latence : pas de trigger temps réel (médiane offline).
- Modèle de bruit optimiste pour marrakesh (non-markovien ? calib périmée ?).
- Radar réel et microscope QAOA réel : en attente (quota IBM mort ; qBraid/AWS prêts).

## 10. Données + reproduction
Données : moisson1.json, moisson2_ibm_{marrakesh,kingston}.json,
qpu_batch1-4.json, radar_noisy.json, microscope.json (+ figs).
Sims ($0) : `pip install qiskit qiskit-aer`, `python3 simu_batchN.py`,
`moissonneur/microscope.py`. Tirs QPU : moissonneur/QBRAID.md, AWS.md.

*Cellule + moissonneur : SPDX MIT. Données et docs : MIT (racine).*
