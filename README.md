# DocSearch

Portail de recherche documentaire local — projet tutoré Master ISI (Burkina Faso).

Indexation intelligente de données hétérogènes (PDF, DOCX, CSV, TXT) avec recherche plein texte, sémantique et hybride.

## Stack

| Couche | Technologies |
|--------|--------------|
| Backend | Python 3.10+, FastAPI, SQLite, Whoosh, scikit-learn |
| Frontend | React, Vite |
| Tests | pytest (30+ tests automatisés) |

## Démarrage rapide

### Prérequis

- Python 3.10+
- Node.js 18+

### Installation

```powershell
# Racine du projet
python -m venv .venv
.venv\Scripts\pip install -r backend\requirements.txt

cd frontend
npm install
cd ..
```

### Lancer l'application

**Terminal 1 — Backend (port 8010)**

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

**Terminal 2 — Frontend**

```powershell
cd frontend
npm run dev
```

Ouvrir l'URL affichée par Vite (ex. http://localhost:5173). Se connecter, puis vérifier le badge **API v0.7.0**.

Alternative : lancer **Full Stack** depuis Run & Debug (`.vscode/launch.json`).

### Jeu de démonstration

```powershell
# Corpus administratif IBAM (~1 110 pièces)
.venv\Scripts\python.exe scripts\generate_demo_dataset.py

# Corpus scientifique informatique (~520 pièces, préfixe sci_) — s'ajoute au fonds IBAM
.venv\Scripts\python.exe scripts\generate_scientific_corpus.py
```

Puis dans l'interface (admin) : **Indexer le dossier** ou `POST /ingest/scan?force=true`.

## Documentation

| Fichier | Contenu |
|---------|---------|
| [CAHIER_DES_CHARGES.md](CAHIER_DES_CHARGES.md) | Spécifications et plan par phases |
| [TESTS_MANUELS.md](TESTS_MANUELS.md) | Grille de tests manuels cochée (session du 27/10/2026) |
| [docs/GUIDE_INSTALLATION.md](docs/GUIDE_INSTALLATION.md) | Installation détaillée |
| [docs/MANUEL_UTILISATEUR.md](docs/MANUEL_UTILISATEUR.md) | Guide utilisateur du portail |
| [docs/NOTES_RAPPORT.md](docs/NOTES_RAPPORT.md) | Structure et brouillons pour le rapport |
| [docs/PERFORMANCE_RESULTS.md](docs/PERFORMANCE_RESULTS.md) | Résultats des benchmarks |

## Tests

```powershell
# Tests automatisés
cd backend
..\.venv\Scripts\python.exe -m pytest tests -v

# Benchmark performance (corpus réel)
..\.venv\Scripts\python.exe scripts\benchmark.py
```

## API principale

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | État du service (version, nb docs, index) |
| GET | `/documents` | Liste paginée + filtres `file_type`, `tag`, `q` |
| GET | `/documents/{id}` | Détail d'un document |
| DELETE | `/documents/{id}` | Suppression document + index |
| GET | `/search?q=...&mode=hybrid` | Recherche keyword / semantic / hybrid |
| POST | `/ingest/scan` | Scanner `data/raw/` |
| POST | `/ingest/upload` | Upload fichier |
| POST | `/index/rebuild` | Réindexation Whoosh |

Documentation interactive : http://127.0.0.1:8010/docs

## Structure

```
projet_tutore/
├── backend/app/     # API, ingestion, extraction, indexation, recherche
├── frontend/src/    # Interface React
├── data/raw/        # Fichiers sources (1 110 pièces IBAM / UJKZ)
├── data/db/         # SQLite + index Whoosh
├── docs/            # Documentation rapport et utilisateur
└── scripts/         # Génération démo + benchmark
```

## Contexte de démonstration

Le jeu de données reconstitue le **Centre de documentation de l'IBAM** (Institut Burkinabè des Arts et Métiers, Université Joseph Ki-Zerbo) : notes, PV, budgets, listes CSV, conventions Word et circulaires PDF. Les personnes et montants sont fictifs ; le cadre institutionnel est réel.

---

*Projet tutoré — Indexation intelligente de données hétérogènes pour la recherche d'information*
