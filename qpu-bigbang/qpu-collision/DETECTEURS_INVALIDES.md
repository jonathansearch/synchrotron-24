# DETECTEURS INVALIDES — beta1-Hamming (batch 4)
MESURE : b1 = 67 (t0) -> ~90-110 (doux/mid/brutal/libre/echo-retour 64).
Saturé PARTOUT, même témoin libre : NON discriminant. CAUSE : distributions
murs PLATES (interieur tanh) -> sous-graphe hypercube dense (45-59 noeuds/64)
-> ~100 cycles de base ; seuils 2/5/10 ne sauvent rien (46-62 à thr10) ; le
bruit ajoute des noeuds (faux cycles). Le détecteur mesure la PLATITUDE, pas
les trous de collision. STATUT : REFUTE (donnée négative scellée, batch 4).
ALTERNATIVES (ticket NOUVEAUX_DETECTEURS_TOPO) : superlevel sets (filtration
par masse : noeuds top-p%, trous dans le SUPPORT du pic), Rips sur distances
de Hamming + persistance (ripser : diagramme, pas un nombre), complexes lazy/
witness, MI/corrélateurs (VALIDES batch 4), Page-tomo (VALIDE batch 2-4).
Critère d'acceptation : témoin libre = 0 ET échelle brutalité monotone ou
revival prédit. Ne plus utiliser Hamming-brut sans filtration.
