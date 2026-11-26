# Notes orateur — Limites et perspectives

À coller dans **Notes de la diapo** (PowerPoint), pas sur le slide lui-même.

---

## Texte pour les notes

**Limites**  
Nous assumons plusieurs limites du prototype. La recherche sémantique reste légère : elle repose sur TF-IDF, une pondération classique où un terme est important s’il est fréquent dans un document (TF) mais rare dans le corpus (IDF). Ce n’est pas une approche par embeddings neuronaux. DocuSearch ne gère pas encore l’authentification multi-utilisateurs, reste volontairement local (pas de cloud), et cible des volumes encore modestes.

**Perspectives**  
Les suites possibles sont réalistes : affiner la recherche hybride, enrichir davantage les métadonnées, ajouter l’OCR pour les PDF scannés, puis un module RAG pour générer des réponses sourcées à partir des documents retrouvés. Un déploiement cloud pourra être envisagé plus tard, si le besoin organisationnel l’exige.

---

## Sur la diapo (rappels courts seulement)

**Limites**
- Sémantique légère (TF-IDF)
- Pas d’auth multi-utilisateurs
- Pas de cloud (local)
- Volumes modestes

**Perspectives**
- Hybridation plus fine
- Métadonnées enrichies
- OCR / PDF scannés
- Module RAG
- Cloud progressif si besoin
