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

---
*Exécution : `cd synchrotron-24 && python3 experiences/s01_naissance.py`* 🔒
