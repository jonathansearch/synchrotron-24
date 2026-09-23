# DATASHEET CELLULE COLLISION 6q (moisson 1, n=3 + batch4, marrakesh)
| lambda | zz_contact (n=3) | batch4 | MI (n=3) | Page-q3 mit (n=3) | batch4 |
|---|---|---|---|---|---|
| t0 | -0.001±0.009 | 0.028 | 0.019±0.000 (biais) | 0.205±0.028 | 0.273 |
| 0.2 doux | 0.030±0.014 | 0.049 | 0.021±0.002 | — | — |
| 0.6 mid | 0.072±0.006 | 0.107 | 0.026±0.006 | 0.761±0.005 | 0.80 |
| 1.2 brutal | 0.126±0.015 | 0.080 | 0.038±0.005 | 0.613±0.018 | 0.662 |
| libre (temoin) | 0.008±0.021 | -0.001 | 0.020±0.004 | — | — |
| echo | 0.010±0.012 | -0.010 | 0.019±0.003 | — | — |
POINT DE FONCTIONNEMENT : Page-q3 @ lam0.6 = métrologie (sigma 0.005 !) ;
zz @ lam1.2 = détection (0.126±0.015, 8-sigma vs témoin). Brutal>mid en zz
(3/3 rondes, 3.3-sigma, =simu) ; mid>brutal en Page (revival, =simu).
DÉRIVE inter-session ~0.04 (layout/jour) >> sigma intra ~0.01 -> RECALIBRER
(t0+libre+echo) CHAQUE session. Chaîne batch4 NON réutilisée (verif None ->
layout auto : robustesse inter-layout prouvée, comparabilité affaiblie).
DÉBIT cloud : ~2000 shots/s mur (borne basse, file incluse). Moisson2 : lam
fin 0.4-1.6, 5 rondes, chaîne forcée+log, 2 backends.
