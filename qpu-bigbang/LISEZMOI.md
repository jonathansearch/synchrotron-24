# QPU : Big Bang + programme synchrotron sur hardware IBM (2026-09-23)
- `batch1.py` = Big Bang (7 circuits) · `batch2.py` = TOUT S01-S06+warp (28 pubs, 1 job) · `batch3.py` = revanche (30 pubs, layout fixe, REM)
- `submit*.py` = tir QPU (clé via env `IBM_TOKEN`, JAMAIS dans le repo) · `diag.py` = autopsie hardware sans job
- `simu_*.json` = prédictions exactes · `qpu_*.json` = mesures hardware · `job*_id.txt` = identifiants jobs IBM (références, pas des secrets)
- `fig_*.png` = simu vs QPU. Règle maison : AUCUN secret commité (audit pre-push à chaque fois).
