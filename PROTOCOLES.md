# 📜 PROTOCOLES — synchrotron-24

## S01 — Naissance 100 M_sol + absorption 24 qubits (2026-09-22)
- **Méthode** : 24 qubits r=2-6 r_s, sub-képlériens, horloges+Kuramoto K=1,
  message 64 bits en tranches, 6 lois (LOIS.md). T=2500, DT=0.02.
- **Observé** : 24/24 absorbés à t≈25. R_global monte à 0.85 puis la
  marée le DÉCHIRE à 0.16 (t≈11), gel à 0.44 ; R_proximité tient ~0.6.
  F_info 1→0.79 (érosion thermique). P_sig 1.95→0.2→0.9 gelé.
  Horloges 0.85→0 (temps arrêté). Déformation : pic ×24000 au passage
  (spaghettification, covariance quasi-dégénérée — assumé).
  Fluctuations → 0 (gel). a_grav → 0.49 (soft-core). Queues plates =
  gel absorbé (choix, pas découverte).

## S02 — Courbe de Page : l'info revient (CIBLE 1, 2026-09-23)
- **Méthode** : S01 + évaporation déclarée (M 0.5→0.02 linéaire t=30..200,
  pas Hawking exact) + réémission kick 1.5·v_esc (déclarée ; mesuré = F, R).
  Observable : bits intacts DEHORS /64. T=10000, DT=0.02.
- **Observé** : bits_out 1.0 → 0.05 (t=20, absorption) → 0.73 (t≥80,
  plateau ±0.02 par flips aller-retour). 24/24 réémis. F_frozen S01 =
  0.79 : l'écart 0.06 = flips pendant la fuite. TRANCHEMENT : l'info
  REVIENT à ~F_gelée → unitarité mesurée (dans ce modèle), pas de
  rupture U détectée. Contrôle S01 (M const) : reste à 0.

## S02b — Dissociation masse/info : la masse meurt (CIBLE 1 FINIE, 2026-09-23)
- **Méthode** : S02 + qubits massifs m=0.01 (alourdissent le puits en
  tombant, repartent avec leur masse). M_local = M_BH + 0.01×n_gelés
  (terme qubits dynamique, pas relu) + PHI_max dehors (1/d3³, sonde de
  re-compaction). (Remappe le « S04 » du ticket : S04 reste Λ.)
- **Observé** : M_local 0.5 → pic 0.65 (t=40, les gelés PÈSENT, preuve
  de non-circularité) → 0.02. I_rec → 0.73 (S02 ✓). PHI_max 5.1 → 24
  (chute) → 0.001 (fuite diffuse, 5000× sous l'initial).
  TRANCHEMENT : masse → 0 SANS re-compaction pendant que info → 0.73.
  Hawking confondait les deux régimes : topologie (conserve) vs énergie
  (dissipe). Ticket : tickets/DISSOCIATION_MASSE_INFO.md.

## S03 — Rebond de Planck vs effondrement GR : KO de la singularité 🥊
  (CIBLE 2, 2026-09-23)
- **Méthode** : anneau N=24 (R=4, tatouage H1~5.7), chute radiale,
  micro-loi par paires F=-g/r²+k/r⁴ (k=0 GR / k=G·r_eq² Planck,
  r_eq=0.6, rho_crit~26.5 déclarées) + friction γ=0.5 (relaxation
  violente ; v1 sans friction : orbites centrifuges, rho<rho_crit,
  combat annulé — cf. S01). Le point de chute ÉMERGE, pas codé.
- **Observé** : GR traverse le centre (r 4→0.54→3.9) en PULVÉRISANT
  l'anneau : H1 5.75→0.000, ré-expansion amnésique. Planck STOPPE la
  chute à r=0.77, densité plafonnée rho~12.5 (≈rho_crit/2), mini-tatouage
  H1~0.1-0.18 (>10× GR). Pas de singularité côté Planck : l'effondrement
  est stoppé à densité finie avec mémoire survivante = rebond (v1 : la
  ré-expansion complète reste un S03b optionnel).
  Ticket : tickets/REBOND_PLANCK.md (clôt la Q2 : oui, ça rebondit).

## S03b — RÉSURRECTION : le Big Bang arrive-t-il ? OUI (match retour, 2026-09-23)
- **Méthode** : TOUT au même point (boule eps=0.1, 40x < anneau S03),
  micro-loi S03 inchangée, SANS friction, dt=0.002 (le Bang c'est violent),
  bits alternés + flip au contact (r<0.3, p=0.1, seed fixe). GR = témoin.
- **Observé Planck (LE BANG)** : r 0.1→343 (x2600 !), H1 0.005→60.9 (née du
  néant), H=1/t au millième (H.t=1.00 : Hubble ÉMERGE, non codée !),
  H1/r=0.178 constant (expansion HOMOTHÉTIQUE : garde sa forme),
  rho en 1/t³ exact, 12/12 secteurs dès t=1 (renaît ROND 🌍), F figé à 0.46
  (brouillé puis figé par l'expansion), d_min→32 (zéro fusion), 24/24 bits.
- **Observé GR (témoin, pas de Bang)** : noyau fusionné r~0.3 (H négatif par
  moments = re-contraction !), H1=0.00 tout du long (mort-né), r_rms gonflé
  par crachats (2-4/12 secteurs = jets, pas rond), d_min→0.0015 (les qubits
  SE COLLENT !), F touillé 0.33-0.58 (bits tripotés dans la fournaise).
- **Verdict** : le point zéro Planck EXPLOSE en univers rond en expansion de
  Hubble avec structure émergente ; le point zéro GR fusionne et crache.
  Rien ne se perd (24/24 bits des deux côtés) mais GR colle, Planck envole.
  Ticket : tickets/RESURRECTION_BIGBANG.md (TOUS les détails).

## S04 — LAMBDA : le fantôme capturé, séparatrice ~10^-3 ➕ (MISSION 3, 2026-09-23)
- **Méthode** : anneau N=24 libre (R0=4, pas de trou noir), attraction
  -g/r² (k=0 : grandes échelles), F_Lambda=+Lambda.r (forme exacte du vrai
  Lambda !), γ=0.3. Scan Lambda -0.05→+0.2, destins LIÉ/RIP/CRUNCH.
- **V1 réfutée** : crayon prédisait Lambda*=0.1125 + CRUNCH en dessous.
  OBSERVÉ : zéro CRUNCH (l'effondrement asymétrique rate toujours le
  centre), fragmentation UNIVERSELLE (H1 meurt, d_min->0.0001 : la vision
  POIDS se produit spontanément !), premier RIP dès 0.06.
- **V2/V3 (t=120 + extension 0.002 à t=240)** : VRAIE séparatrice LIÉ/LIBRE
  entre 0.0 (lié, repli 7.6) et 0.002 (RIP lent t~240) → **Lambda* ~ 10^-3,
  SIGNE + (répulsion, comme le vrai univers !)**, crayon réfuté x50 (la
  fragmentation + les catapultes offrent l'évasion gratuite). Ralentissement
  critique : t_RIP 8→240 près de Lambda*. Zone chaotique (l'arrondi seul
  change les détails près du fil).
- **Course mémoire** : RIPs rapides (≥0.09) figent l'anneau INTACT (H1 5.7→
  20-36, gonfle !), RIPs lents le grumèlent (H1→0), liés idem. La fuite
  rapide sauve la mémoire. Transition chaotique 0.045-0.06.
  Ticket : tickets/LAMBDA_FANTOME.md.

## S05 — FANTÔME : les trous gravitent SANS matière 👻🍎 (MISSION 4, 2026-09-23)
- **Méthode** : passé COMMUN (batch-1 : 12 qubits recette S01 gobés 12/12
  par M=0.5, gelés, masse 0.01 chacun = EMPREINTE, H1=0.677) ; puis 3
  présents : VIDE (M=0, rien), FANTOME (M=0 + empreinte), TROU (M=0.5 +
  empreinte). Batch-2 : 12 pommes, recette S01, seed IDENTIQUE (appariées).
  Gel r<1 seulement si M>0 (pas d'horizon sans masse, déclaré).
- **Observé** : VIDE 0/12 liées (rmin 2.79, rfinal 4.70 : fuite) ; FANTOME
  9/12 LIÉES (rmin 0.64 : plongent ! rfinal 3.70 : restent ! H1_fin 0.155 :
  mini-trou gardé) ; TROU 12/12 gobées. Mêmes M=0 des deux côtés VIDE/
  FANTOME → l'effet est PUR (l'empreinte 0.12 = 24% du trou retient 75%
  des pommes). OUI : gravité sans matière (mémoire topologique qui pèse).
  Ticket : tickets/TROUS_GRAVITENT.md.

---
*Exécution : `cd synchrotron-24 && python3 experiences/s01_naissance.py`* 🔒
