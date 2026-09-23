# DATASHEET v1 CELLULE COLLISION 6q (moisson 1+2 : n=14, 2 backends)
## zz_contact(lam) : monotone -> plateau (simu 0.10->0.25)
lam: 0.4 0.6 0.8 1.0 1.2 1.4 1.6 | Marrakesh: .043 .069 .093 .125 .153 .144 .160 (sig~.02)
Kingston: .091 .142 .158 .214 .204 .217 .221 (sig~.015). Témoins ~0 (libre/echo/t0 ±.02).
Ratio hardware/simu : 60% (M) / 88% (K). Facteur backend K/M ~1.4 -> CALIBRER PAR BACKEND.
## Page S(q3)(lam) : CLOCHE pic lam~0.8 (simu .55/.73/.80/.74/.59/.43/.38)
Mesuré (2 backends IDENTIQUES) : t0 .23-.27, l06 .76-.79, l10 .78, l14 .52-.54
(sig .005-.025). Forme backend-indépendante + plancher +0.2 -> MÉTROLOGIE.
## POINTS DE FONCTIONNEMENT (figés v1)
Page@lam0.8 = métrologie (sigma .005) ; zz@lam>=1.2 = détection (plateau).
Autocalibration/session OBLIGATOIRE (t0+libre+echo) : dérive .04 >> sigma .01.
Trigger collecteur : MÉDIANE (pas moyenne : 1 ronde bruitée/5 à l8-M).
## REPRODUCTIBILITÉ : n=14 par point fort (3+1 moisson1, 5+5 moisson2),
2 backends, 3 layouts : formes stables, facteurs backend quantifiés.
Débit cloud ~2000-2600 shots/s mur (file variable). Chaînes forcées+loggées.
