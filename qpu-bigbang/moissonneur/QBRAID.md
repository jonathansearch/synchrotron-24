# qBraid (route QPU n°2, depuis 23/09/2026, IBM quota mort)
- Clé : chez l'utilisateur (jamais commitée). SDK : pip install 'qbraid[qiskit]'.
- QbraidProvider() + QBRAID_API_KEY. Pas de batch (1 circuit = 1 tâche).
- Transpile locale OBLIGATOIRE : initialize -> basis rx/rz/cz (QASM3 refuse reset).
- Ordre bits = qiskit (X0 -> 000001) : analyse4 SANS changement. Valide sur qir-sv : D4L zz .478 (=exact .455).
- Prix (crédit=$0.01) : Rigetti Cepheus AWS 30/tache + 0.0425/shot (le moins cher) ; IQM Garnet 30 + 0.145 ; IonQ Forte 30 + 8 !
- Coûts radar : LITE 9 pubs x500 shots Rigetti ~460cr (~$5) ; FULL 3 rondes 69x500 ~3540cr (~$36) ; +Page ~+600cr.
- Simus gratuits : qbraid:qbraid:sim:qir-sv (30q), ionq sim. OpenQuantum ($50 gratuits/90j) : à lier par l'user sur openquantum.com/qbraid.
- Solde au 23/09 19h : 0.00 (recharge requise, min ~100cr pour instances).
