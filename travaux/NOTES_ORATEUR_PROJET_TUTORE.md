# Notes orateur — Présentation 10 minutes (+ démo)

**Fichier slides :** `travaux/PRESENTATION_KOROGO_RICHE_IMAGES.pptx`  
*(version enrichie images ; originale : `PRESENTATION_KOROGO_W_Ange_Gaetan_AVEC_DEMO_NOTES.pptx`)*  
**Durée stricte :** 10 minutes + questions  
**Prototype :** DocuSearch  
Conseil : une idée par slide. La démo dure ~1 min 30 max.

**Fichiers complémentaires (à réviser) :**
- `SCRIPT_DEMO_ET_ETAT_ART.md` — script détaillé démo + texte oral état de l’art
- `FICHE_MAITRISE_THEME.md` — définitions, sigles, questions/réponses

---

## Chronométrage (10 min)

| Slide | Contenu | Temps |
|------:|---------|------:|
| 1 | Titre | 15 s |
| 2 | Plan | 15 s |
| 3 | Contexte | 50 s |
| 4 | Problématique / objectifs | 50 s |
| 5 | État de l’art | 1 min |
| 6 | Solution DocuSearch | 50 s |
| 7 | Architecture | 50 s |
| 8 | Réalisations | 50 s |
| 9 | **Démonstration** | **1 min 30** |
| 10 | Limites / perspectives | 45 s |
| 11 | Conclusion | 40 s |
| | **Total** | **~10 min** |

Si tu prends du retard avant la démo : saute l’état de l’art détaillé (garde 30 s) et va à la démo.

---

## Slide 1 — Titre (15 s)

Bonjour. Je suis **KOROGO Wendkuuni Ange Gaetan**.  
Projet tutoré Master ISIE : **indexation intelligente de données hétérogènes**.  
Prototype : **DocuSearch**.

---

## Slide 2 — Plan (15 s)

Je présenterai le contexte, les objectifs, l’état de l’art, la solution, l’architecture, les réalisations, puis une **démonstration live**, avant les limites et la conclusion.

---

## Slide 3 — Contexte (50 s)

**Contexte :** aujourd’hui, dans plusieurs structures, les documents sont dispersés et hétérogènes (PDF, Word, CSV, texte, Excel, JSON…).

**Problème :** sans outil central, la recherche reste manuelle et lente.

**Enjeu :** indexer intelligemment pour retrouver l’information rapidement, en restant local et simple.

**Texte à dire :**

> « Aujourd’hui, dans plusieurs structures — écoles, ONG, PME, administrations — les documents sont dispersés et de formats différents : PDF, Word, CSV, texte, Excel, JSON…  
> Sans outil central, la recherche reste manuelle et lente.  
> L’enjeu est donc d’indexer intelligemment ces documents pour retrouver l’information rapidement, tout en restant local et simple. »

---

## Slide 4 — Problématique / objectifs (50 s)

**Question centrale :**  
Comment indexer automatiquement des données hétérogènes et offrir une recherche pertinente via une interface web locale ?

**Nos objectifs :**
1. Maîtriser l’état de l’art  
2. Concevoir une architecture modulaire  
3. Réaliser un prototype fonctionnel  
4. Proposer des perspectives réalistes  

**Texte à dire :**

> « Notre question centrale est simple : comment indexer automatiquement des documents de formats différents, et offrir une recherche pertinente, via une interface web locale ?  
> Pour y répondre, nous nous sommes fixé quatre objectifs : bien maîtriser l’état de l’art, concevoir une architecture claire et modulaire, réaliser un prototype fonctionnel, puis ouvrir des perspectives réalistes. »

---

## Slide 5 — État de l’art (1 min)

**Texte oral clarifié :** voir `SCRIPT_DEMO_ET_ETAT_ART.md` § E.

Rappel : 15 articles → 3 axes (fondements, hybridation, pipeline RAG) → 4 idées → choix DocuSearch = multi-formats + enrichissement + hybride léger.

---

## Slide 6 — Solution (50 s)

**DocuSearch** : portail local  
Pipeline : ingestion → extraction → enrichissement → indexation → recherche  

- Enrichissement : tags, résumé, entités  
- 3 modes : mots-clés, sémantique, hybride  
- Adapté aux ressources limitées  

**Texte à dire :** voir `DIAPO_SOLUTION_CLAIR.md`

---

## Slide 7 — Architecture (50 s)

React → FastAPI → métier → SQLite/Whoosh.  
Séparation claire pour tester et démontrer.

---

## Slide 8 — Réalisations (50 s)

Ingestion multi-formats, enrichissement, 3 modes de recherche, filtres, suppression, rebuild.  
Je vais maintenant le montrer en live.

---

## Slide 9 — Démonstration (1 min 30)

**Script pas à pas (faire + dire) :** `SCRIPT_DEMO_ET_ETAT_ART.md` § B.

Rappel express : badge vert → chip `formation` → **Hybride** → ouvrir une fiche → phrase de sortie ISGO/local.  
**Plan B :** captures d’écran.

---

## Slide 10 — Limites / perspectives (45–50 s)

### Notes à mettre dans PowerPoint (notes de bas de page)

Limites :
Nous assumons plusieurs limites du prototype. La recherche sémantique reste légère : elle repose sur TF-IDF, une pondération classique où un terme est important s’il est fréquent dans un document (TF) mais rare dans le corpus (IDF). Ce n’est pas une approche par embeddings neuronaux. Ensuite, DocuSearch ne gère pas encore l’authentification multi-utilisateurs, reste volontairement local (pas de cloud), et cible des volumes encore modestes.

Perspectives :
Les suites possibles sont réalistes : affiner la recherche hybride, enrichir davantage les métadonnées, ajouter l’OCR pour les PDF scannés, puis un module RAG pour générer des réponses sourcées à partir des documents retrouvés. Un déploiement cloud pourra être envisagé plus tard, si le besoin organisationnel l’exige.

### Version à apprendre (enchaînement fluide)

> « Notre prototype a des limites, et nous les assumons.  
> La recherche sémantique est légère : elle s’appuie sur TF-IDF — un terme compte s’il est fréquent dans un document, mais rare dans l’ensemble du corpus. Ce n’est pas un modèle d’embeddings lourd.  
> Ajoutons aussi l’absence d’authentification multi-utilisateurs, le choix d’un fonctionnement local sans cloud, et des volumes encore modestes.  
>  
> Les perspectives restent claires : améliorer l’hybridation, enrichir les métadonnées, intégrer l’OCR pour les documents scannés, puis un module RAG pour des réponses fondées sur les sources. Le cloud pourra venir ensuite, si nécessaire. »

Détail : `DIAPO_LIMITES_PERSPECTIVES_CLAIR.md`

---

## Slide 11 — Conclusion (40 s)

Problème concret → solution démontrable.  
DocuSearch montre qu’une indexation intelligente est accessible en local.  
Merci. Je suis prêt pour vos questions.

---

## Checklist démo (avant d’entrer)

- [ ] Backend 8010 lancé  
- [ ] Frontend 5173 lancé  
- [ ] Corpus déjà indexé (ou prêt à indexer)  
- [ ] Requête testée : `formation`  
- [ ] Captures de secours prêtes  
