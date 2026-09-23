# COLLECTEUR GCR-Cell v0 (appareil nouvelle génération : QPU + récupérateur)
MISSION : reproduire la collision à la demande (cellule 6q, lam calibré) et
ABSORBER chaque collision (tous les shots) pour analyse : zz/Page/MI/H live,
trigger étincelle (zz>0.05 ET dS>0.3 vs t0 session), banque JSON croissante.
ARCHI : [cellule QPU 6q fixe] -> [boucle moisson (rondes, REM/ronde)] ->
[banque stats + datasheet auto] -> [trigger -> flag « étincelle » + dump].
MESURÉ (moisson1) : Page sigma 0.005 (métrologie !), zz 8-sigma vs témoin,
contrôles à zéro, dérive session 0.04 -> autocalibration obligatoire.
LIMITES CLOUD : pas de temps réel strict (trigger différé minutes) ; file
variable ; layout à forcer+logger. PHASE LABO (roadmap) : readout FPGA live,
vrai temps réel, cellule multi-contact (2-3 collisions), détecteurs Rips
(ticket NOUVEAUX_DETECTEURS_TOPO). Le phénomène est REPRODUCTIBLE (n=4) :
on passe de la découverte à l'INSTRUMENT.
