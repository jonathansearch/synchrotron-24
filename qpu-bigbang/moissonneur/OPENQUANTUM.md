# OpenQuantum (route QPU n°4, depuis 24/09/2026 — CELLE QUI MARCHE)
- Compte mariée (25 Spark initiaux, 0 Complet, +50$ dans 6j). Clés SDK (ID+s_c9d0...,
  secret 64hex) chez l'utilisateur, jamais commitées. SDK : pip install openquantum-sdk.
- Auth : ClientCredentialsAuth(ClientCredentials(client_id, client_secret)).
- Backend testé : rigetti:cepheus-1-108q (QASM2, 128 shots, ~1 Spark/job).
- CANARIS 24/09 : X0 {0:10,1:118} ✓ / H0 {0:61,1:67} ✓ / Bell 2x IDENTIQUE
  {00:71-75, 10:52-56, 11:1} : 1q parfait, CX systématiquement inopérant
  (mapping/precompile à investiguer — pas de calibration dispo sur ces jobs).
- Contraintes : qubits virtuels contigus depuis 0 ; Public Plan = attribution requise.
- Solde : 21 Spark le 24/09 ~3h. Prochain : Bell sur IQM/IonQ ? + ticket CX-Rigetti.
