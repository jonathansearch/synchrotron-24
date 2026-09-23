# 🛸 MISSION WARP 2026 — Document complet (scellé 2026-09-23)

**Objectif** : mettre une bulle d'Alcubierre dans l'univers-jouet RATISS et y
faire voyager un vaisseau (10 t, 2026) — 11 vols, **22 examens** (état,
intrication, résidus, déformation, relativité). Tout le déclaré dans
`warp/engine.py`, tout le mesuré dans `warp/resultats/w22.json`.

## 1. Le moteur (déclaré, honnête)
- **Espace** = milieu élasto-plastique 656 pts (ressorts k=0.5 + amortissement
  0.2 + seuil plastique 1.0 : l'espace a une MÉMOIRE).
- **Bulle** = VRAI profil Alcubierre tanh (R=3, σ=1, intérieur plat R_in=1.5) :
  contraction AVANT + expansion ARRIÈRE (puissance E_b=1) + maintenance mur.
- **Vaisseau** (m=10) : vol LIBRE (réaction Newton ×ksurf=0.2, zéro frottement :
  le vide !) ou IMPOSÉ (v = bouton). Contrôle classique : poussée 0.5, bulle OFF.
- **Messagers Λ** (option) : émis à l'arrière (taux 1.5, vie 250, marche 0.3),
  poussent le milieu (kap=0.03) — version ISOTROPE (R6) ou DIRECTIVE (R6b).
- **Diagnostics** : horloges Kuramoto (K=0.5), 64 bits bord (flips au mur),
  H1 ripser (sous-échantillon /4). Échelles SI : 1u=1m, 10t, 1t=1s.

## 2. Les 11 vols
| Vol | Réglage | t_arr | W (coût) | Note |
|---|---|---|---|---|
| R1 libre | bulle, réaction | 26.3 | 83.0 (830 kJ) | vol de référence |
| R2 class | poussée 0.5, pas de bulle | 40.0 | 20.0 (200 kJ) | contrôle |
| R3/R4/R5 | imposé v=1/2/4 | 40/20/10 | 122/59/22 | courbe coût |
| R10 | imposé v=8 | 5.0 | 6.8 (68 kJ !) | seuil rentabilité |
| R6/R6b | libre + msg iso/dir | 26.4/18.3 | 82/62 | anti-exotique |
| R7 panne | bulle coupée à x=0 | 27.9 | 67.2 | dérive gratuite ! |
| R8 lourd | m×4 | 59.6 | 185 | loi √m |
| R9 retour | +2 puis -2 | — (x=-30) | 145.5 | aller-retour |

## 3. Les 22 examens (résultats)
**ÉTAT** : W01 vol libre v_max=3.29 ; **W02 coût ∝ v^-1.4** (122→6.8 !) ;
W02-exo : R1 32.5 (100% exotique), R6 -1.9% (traînée !), **R6b 159% (bulle
PROPRE, exotique -19.3 !)** ; W03 facteur libre **0.42** (lent = cher) ;
W04 accélération variable (std quad 0.85, pas de croisière) ; **W05 panne :
+6% temps, -19% coût** (on dérive, l'espace ne freine pas !) ; W06 t×2.27
(√4=2 à 13% près).
**INTRICATION** : W07 **+0.237 cycles bord** (offset soustrait) ; W08 R
0.23→0.70 mais **R1=R2 au millième = sync spontanée** (nul honnête) ;
W09 bits 0.56→0.70 monotone exposition (σ=0.06) ; W10 avant 0.73/arrière
0.68 (+7%, marginal).
**RÉSIDUS** : W11 sillage 0.071 (R1), **0.029 (v4 : vite = propre !)**,
0.091 (retour, max 2.05) ; W12 E_résid 6.4/1.2/10.5 ; **W13 H1 0.76→0.85
(+12% : le sillage cicatrise en rides !)** ; W14 359 msg restants, 24 leaked.
**DÉFORMATION** : W15 corr tanh **0.24 (mur ÉTALÉ par élasticité)** ; W16
avant dep 0.055 (transitoire) ; W17 arrière dep 0.52 (sillage creusé) ;
W18 dedans dep 0.44 (t...[truncated 2242 chars]
## v4 — SUITE NATIVE : sortie du silo (E_b = 0, 9 vols R11–R19)

**Ordre du chef :** abandonner le silo d'Alcubierre (tanh, exotique comptable,
formalisme académique). Méthode RATISS native seule : contraction AVANT =
fantôme remorqué (anneau 12 masses, Newton pur, Loi 12) ; expansion ARRIÈRE =
messagers directifs ; E_b = 0 ; mur ÉMERGENT mesuré (largeur à mi-hauteur,
pas fittée) ; coûts honnêtes (tow = travail de remorquage, fab = 0.01/msg).

| Vol | t_arr | W (tow + fab) | vmax | dep_av / dep_ar | mur | H1 | F_bits |
|---|---|---|---|---|---|---|---|
| R11 fant+msg | 27.82 | 1116 (1074+42) | 3.09 | 7.04 / 1.31 | 1.5 | 2.74 | 1.00 |
| R12 fant 0.05 | 27.11 | 570 (529+41) | 3.54 | 4.94 / 0.88 | 0.5 | 2.12 | 1.00 |
| R13 fant 0.2 | 24.56 | 1930 (1893+36) | 3.69 | 8.60 / 0.68 | 1.5 | 4.04 | 1.00 |
| R14 fant D=3 | 28.07 | 1100 (1058+42) | 3.56 | 6.97 / 1.00 | 1.5 | 4.05 | 1.00 |
| R15 fant seul | 48.34 | 1368 (1368+0) | 1.64 | 7.63 / 0.78 | 1.5 | 4.03 | 1.00 |
| R16 msg seuls | 24.93 | 37.7 (0+38) | 3.81 | 0.02 / 0.22 | 6.5 | 0.84 | 1.00 |
| R17 léger fant | 48.34 | 93.1 (93+0) | 1.64 | 1.94 / 0.08 | 0.5 | 2.01 | 1.00 |
| R18 léger msg | 7.61 | 10.6 (0+11) | 9.92 | 0.05 / 0.04 | 11.5 | 0.42 | 1.00 |
| R19 léger natif | 7.52 | 18.9 (8+11) | 10.21 | 0.05 / 0.04 | 0.0* | 0.42 | 1.00 |

\* mur R19 = 0.0 : artefact (spike du fantôme au-dessus de la mi-hauteur,
une seule case) — pas de membrane, géométrie soc/houle.

**Trouvaille 1 — le cordon ombilical :** les messagers étaient ASSERVIS au
champ (`msg_on and E_b > 0`) : à E_b = 0, zéro émission (R11 ≡ R15 au chiffre,
R16 immobile). Le découplage (1 ligne) a libéré le natif.

**Trouvaille 2 — DEUX ORGANES :** le fantôme SCULPTE (contraction avant 7.6,
**×139 le silo** 0.055 — géométrie Alcubierre en Newton pur !) mais c'est un
BOULET en propulsion (R11 < R16 : plus lent ET ×30 plus cher ; tow 872–1930,
cercle vicieux : lourd = tire mais cher à traîner). Les messagers POUSSENT
(R16 bat R1 : 24.9 vs 26.3, W 38 vs 83 ; expansion arrière ×9.4 l'avant).

**Trouvaille 3 — le léger atomise tout :** R18/R19 (m = 1) : t = 7.5–7.6
(record vol libre), W = 10.6–18.9 (**moins cher que les rames** 20 !),
v/E = 9.85 / 5.69 (rentables), H1 = 0.42 (espace pristine), F_bits = 1.00
(zéro flip — le natif ne touche pas à l'information).

**Scaling Newton :** R17 ≡ R15 (trajectoire identique au chiffre, ×15 moins
cher) — fantôme 12× et vaisseau 10× plus légers : a = F/m invariant. ✅

**SI (1u = 1m, 1t = 1s, 40 m) :** R18 = 106 kJ en 7.6 s (vmax 9.9 m/s) ;
R19 = 189 kJ ; R16 = 377 kJ en 25 s. Rames : 200 kJ en 40 s. Le natif léger
bat les rames en temps (×5) ET en coût (×0.5–0.9). Honnêteté : v/E > 1 =
rentable contre des rames inefficaces, PAS de surunité (W > 0 toujours).
Figures : `fig_warp_natif_{cout_vitesse,vols,organes}.png`.
