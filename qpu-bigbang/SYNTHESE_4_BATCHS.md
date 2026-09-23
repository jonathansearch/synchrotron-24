# SYNTHESE 4 BATCHS QPU (2026-09-23, IBM kingston/marrakesh 156q)
B1 BIG BANG (7 pubs) : KZ 1.96/0.50, faux-vide bulles 0.39, GHZ5 0.93, BV 101.
B2 PROGRAMME (28 pubs, 1 job) : Page S=0.89/0.99, Grover 0.42/0.70/0.42,
mur tanh corr 0.994, Planck 0.33/GR 0.04, T1 0.85/0.26. FAILLES : dt=4ns
(délais 18x), loterie layout (q121/q146), pas de REM.
B3 REVANCHE (30 pubs) : T1=230us fité (=props !), T2*=30us, reset 99%,
Bell 0.997, Planck 0.967/ZNE 0.977, écho +23% vs libre. Layout fixe + REM.
B4 COLLISION (29 pubs) : contact zz 0.03/0.05/0.11/0.08 (5-sigma, témoin
libre -0.001), Page q3 0.27/0.80/0.66 (=simu 0.06/0.75/0.60 +plancher),
echo H 0.014 vs 0.029 (revient 2x mieux), beta1 REFUTE (saturé ~100).
THESE ROBUSTESSE : détection différentielle (témoin à zéro), contrôles
(libre/echo), layout fixe, REM, simu exacte pré-tir (revival prédit, observé).
~120 circuits, 4 jobs. Dossier collision : qpu-collision/. Exploitation :
moissonneur/ (banque stats + datasheet + collecteur).
