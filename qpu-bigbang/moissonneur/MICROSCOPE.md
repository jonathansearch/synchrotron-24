# MICROSCOPE (jalon P2 : voir mourir un ansatz, couche par couche)
Ansatz = nos couches (rx+rzz+contact) @lam0.8, nl 0..12, exact vs bruit kingston.
- zz : pic 4L (.46/.40) -> 8L (.29/.27) -> 12L (.13/.16). Horizon extrapolé ~14L.
- MI : pic 4L (.26/.19) -> 12L (.13/.07). **MI meurt AVANT zz** (bruit tue les corrélations d'abord).
- H : exacte CREUSE à 7L (4.44, revival) ; bruitée MONTE (5.25 à 12L, pompe entropique).
Loi microscope : signal vivant = zz>plancher + MI>0.05 + H_non_saturée. Page/H seule MENT (bruit ressemble au brouillage) -> il faut le TRIO (zz, MI, H). C'est la valeur du microscope : distinguer mort-unitaire (revival) de mort-bruit (pompe).
Méthode gratuite (simu), prête pour QAOA/VQE réels dès crédits qBraid.
