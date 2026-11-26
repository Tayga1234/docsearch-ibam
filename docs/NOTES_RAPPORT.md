# Notes pour le rapport

La rédaction se fait désormais dans le dossier **`rapport/`**.

- Corps du mémoire : [`../rapport/memoire_corps.md`](../rapport/memoire_corps.md)
- État de l’art : [`../rapport/02_etat_de_lart.md`](../rapport/02_etat_de_lart.md)
- Sommaire du dossier : [`../rapport/README.md`](../rapport/README.md)

---

# Anciennes notes (copie de travail)

Document historique. Préférer `rapport/memoire_corps.md` pour la suite.

---

## Chapitre 1 — Introduction

### Contexte (à personnaliser)

Les structures au Burkina Faso (écoles, ONG, PME) accumulent des documents sous formats variés sans outil de recherche unifié. Le projet DocSearch répond à ce besoin par un portail local d'indexation et de recherche.

### Problématique

> Comment concevoir et implémenter un système local capable d'indexer automatiquement des données hétérogènes et d'offrir une recherche d'information pertinente via une interface web ?

### Objectifs atteints

| Objectif | Réalisation |
|----------|-------------|
| ≥ 4 formats | PDF, DOCX, CSV, TXT |
| Indexation 50 docs < 2 min | 1 110 docs en 25,74 s (voir PERFORMANCE_RESULTS.md) |
| Recherche < 1 s | Max 24 ms sur corpus de démo |
| API REST | FastAPI + Swagger `/docs` |
| Interface React | Recherche, upload, détail document |

### Méthodologie

Développement incrémental en 6 phases (fondations → ingestion → indexation → interface → intelligence → rapport).

---

## Chapitre 2 — État de l'art

**Texte complet :** `rapport/02_etat_de_lart.md`  
**Thème :** Indexation intelligente de données pour la recherche d'information

Plan du chapitre :

1. Introduction (index au centre de la RI)
2. Définitions (RI, indexation intelligente, données)
3. Recherche **sans index** vs **avec index**
4. Panorama des moteurs (Web, entreprise, embarqués, vectoriels/RAG, stockage)
5. Fondements classiques (index inversé, TF-IDF, BM25)
6. Littérature 2022–2026 (15 articles, 4 familles)
7. Enseignements
8. Positionnement du travail (sans détailler encore l’implémentation)
9. Références

Les bilans jour 1–3 (`travaux/JOUR_*.md`) restent la source des résumés d’articles ; ils n’ont pas à être relus pour le recentrage du thème.

---

## Chapitre 3 — Analyse et conception

### Besoins fonctionnels

- Ingérer fichiers locaux et uploads
- Extraire texte et métadonnées
- Indexer et rechercher (3 modes)
- Enrichir par tags et entités

### Architecture

Reprendre le diagramme du `CAHIER_DES_CHARGES.md` section 4.

**Modules backend** : `ingestion/`, `extraction/`, `indexing/`, `search/`, `intelligence/`

### Modèle de données

Table `documents` SQLite + champs Pydantic `Document` (id, title, content, tags, entities, summary…).

### Choix technologiques

| Choix | Justification |
|-------|---------------|
| FastAPI | API moderne, typage, OpenAPI auto |
| Whoosh | Index local sans service externe |
| React + Vite | UI réactive, écosystème riche |
| scikit-learn TF-IDF | Sémantique légère sans GPU |
| SQLite | Persistance simple pour prototype |

---

## Chapitre 4 — Réalisation

### Environnement

- Windows 10/11, Python 3.13, Node.js
- IDE : Cursor / VS Code avec debug Full Stack

### Modules clés (extraits à inclure)

1. **Extracteurs** — `backend/app/extraction/` (pattern Strategy par format)
2. **Scanner** — `backend/app/ingestion/scanner.py`
3. **Index Whoosh** — `backend/app/indexing/whoosh_index.py`
4. **Recherche hybride** — `backend/app/search/engine.py`
5. **Enrichissement** — `backend/app/intelligence/enricher.py`
6. **Frontend** — `frontend/src/App.jsx`, `services/api.js`

### Jeu de démonstration

1 110 fichiers IBAM dans `data/raw/` — générés par `scripts/generate_demo_dataset.py`.

---

## Chapitre 5 — Tests et validation

### Tests automatisés

- 30 tests pytest (extracteurs, ingestion, API, recherche, intelligence, performance)
- Commande : `pytest tests -v`

### Tests manuels

- 45 scénarios documentés dans `TESTS_MANUELS.md`

### Performance

Résultats dans `docs/PERFORMANCE_RESULTS.md` :

- 1 110 documents indexés en 25,74 s
- Recherche hybride max 24 ms

### Captures d'écran à joindre

Voir `docs/CAPTURES_ECRAN.md`.

---

## Chapitre 6 — Conclusion et perspectives

### Bilan

Prototype fonctionnel couvrant le cycle complet ingestion → recherche → enrichissement.

### Limites

- Pas d'authentification
- Volume limité (centaines de docs, pas millions)
- PDF images non supportés
- Sémantique TF-IDF (pas de transformers lourds)

### Perspectives

- Déploiement cloud (Docker, hébergement)
- Authentification et rôles
- sentence-transformers pour sémantique avancée
- Connecteurs (email, SharePoint)
- Meilisearch ou Elasticsearch pour montée en charge

---

## Annexes suggérées

- A. Guide d'installation (`docs/GUIDE_INSTALLATION.md`)
- B. Manuel utilisateur (`docs/MANUEL_UTILISATEUR.md`)
- C. Liste des endpoints API (export Swagger)
- D. Jeu de données de démo (liste des 1 110 fichiers)

---

## Mots-clés

`indexation` · `données hétérogènes` · `recherche d'information` · `plein texte` · `FastAPI` · `React` · `Python` · `Burkina Faso`
