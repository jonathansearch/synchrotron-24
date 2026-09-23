# SYNTHÈSE DES MOISSONS (exploitation, sept 2026)
## M1 (kingston, 51 pubs, n=3) — job dapumhj18flc739mu8lg
- zz brutal>mid 3/3 rondes (0.126±0.015 vs 0.072±0.006, 3.3σ) = simu.
- Page mid>brutal (0.761±0.005 vs 0.613±0.018) : revival = simu.
- Dérive session ~0.04 >> σ intra ~0.01 → autocalibration/session.
## M2 (marrakesh+kingston, 2×120 pubs, n=5+5)
- zz(λ) monotone → plateau : M 0.16 (60% théorie), K 0.22 (88% théorie).
- Page(λ) CLOCHE pic λ≈0.8 (0.78, 2 backends identiques) = simu + plancher.
- Facteur backend K/M ≈ 1.4 → calibrage par backend. Témoins ~0, écho revient.
- Chaînes : M [5,6,4,3,7,8], K [10,11,18,9,31,30]. Débit ~2000-2600 shots/s.
## RADAR sim-bruit (modèles K/M réels, chaînes M2)
- Horizon ≥ 8L (zz 0.27 >> plancher 0.03), pic 4L + revival 6L visibles.
- Modèle = 87% théorie (K réel) ; optimiste pour M (calib périmée ?).
- Job radar réel (marrakesh) bloqué : quota IBM épuisé 23/09.
## MICROSCOPE (exact vs bruit K, 0-12L @λ0.8)
- zz : pic 4L (.46/.40) → 12L (.13/.16), horizon extrapolé ~14L.
- MI meurt AVANT zz (12L : .13 exact / .07 bruit).
- H exacte creuse à 7L (revival), H bruit monte (5.25) → Page/H seule MENT.
- Loi : trio (zz, MI, H) obligatoire ; mort-unitaire vs mort-bruit distinguées.
## Points figés (datasheet v2)
- Page@λ0.8 = métrologie (σ 0.005). zz@λ≥1.2 = détection (8σ vs témoin).
- Trigger à la MÉDIANE (1 ronde bruitée/5). Autocalibration par session.
## Routes QPU (23/09 soir)
- IBM : quota mensuel mort (définitif, ~400 pubs tirées). qBraid : chaîne validée
  (simu=exacte, bit-order OK), solde 0, devis lite ~$5 / full ~$36 (Rigetti).
  AWS Braket : clés IAM OK (Ratiss23), S3 OK, Braket en attente vérif CB ($100/mois).
