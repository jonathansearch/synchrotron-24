# AWS Braket (route QPU n°3, depuis 23/09/2026)
- Compte : $100/mois jusqu'en 2027. User IAM Ratiss23 (+AmazonBraketFullAccess,
  +AmazonS3FullAccess). Clés chez l'utilisateur (jamais commitées).
- Région : us-east-1 (IonQ/QuEra) ; Rigetti = us-west-1 ; IQM = eu-west-2.
- Prix : Rigetti Cepheus $0.30/tâche + $0.000425/shot (le moins cher) ;
  IQM Garnet $0.30 + $0.00145 ; IonQ Forte $0.30 + $0.08 ! SV1 $0.075/min.
- Coûts radar : lite 9×500 ≈ $4.60 ; full 69×500 ≈ $35. Canari ≈ $0.35.
- Statut 23/09 : STS OK, S3 OK, Braket = SubscriptionRequired (CB en cours
  de vérification côté AWS). Dès actif : bucket résultats → canari SV1 →
  canari Rigetti → RADAR-lite. SDK : amazon-braket-sdk + qiskit-braket-provider.
