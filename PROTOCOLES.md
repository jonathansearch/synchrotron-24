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

---
*Exécution : `cd synchrotron-24 && python3 experiences/s01_naissance.py`* 🔒
