# LE PROBLEME (nouvelle catégorie : DOSIMETRIE DE L'INTRICATION)
Personne ne DOSE l'intrication : QV = un chiffre abstrait, pas de courbes
dose-réponse. Notre instrument (cellule collision + moissonneur + témoins)
mesure dose (lam/profondeur) -> réponse (zz/Page/MI/echo) -> datasheet.
## P1 OPERATEURS : santé vivante + cartographie défauts + sélection qubits
Preuves : facteur backend K/M 1.4, qubits morts trouvés (q121/q146), dérive
session 0.04, autocalibration. Produit : canari 6q + carte défauts/chip.
## P2 UTILISATEURS : RADAR profondeur + MICROSCOPE ansatz
« À quelle profondeur mon algo meurt-il AUJOURD'HUI ? » Preuves : radar
sim-bruit horizon >=8L, Page sigma 0.005, revival prédit/observé. Produit :
profil Page/couche pour VQE/QAOA (voir où l'ansatz meurt).
## P3 HARDWARE TEAMS : benchmark applicatif calibré (courbes, pas chiffre)
Preuves : datasheet v1 (2 backends, n=14). Courbes > QV pour dynamique.
## Que faire des « particules » (poches d'intrication) ?
Les MESURER comme signal (pas les stocker : pas de qubits volants sur
supraconducteurs — honnête). L'appareil = OSCILLOSCOPE topologique, pas usine.
Roadmap : quota IBM -> radar réel ; Quantum Inspire 5q ? ; Rips (ticket) ;
microscope QAOA-6q ; moisson multi-jours (stabilité).
