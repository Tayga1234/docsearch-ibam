# Cahier des charges — Projet tutoré

**Thème :** Indexation intelligente de données hétérogènes pour la recherche d'information  
**Étudiant :** Master Ingénierie des Systèmes d'Information en Entreprise — Burkina Faso  
**Langage principal :** Python  
**Environnement :** Local d'abord, cloud plus tard 

---

## 1. Cas d'usage retenu

### Contexte

Une petite structure (école, ONG, PME, administration locale) possède des documents stockés dans plusieurs formats et emplacements. Les collaborateurs perdent du temps à chercher une information car il n'existe pas de point d'accès unique.

### Problème

- Données **dispersées** (dossiers locaux, exports, rapports)
- Formats **hétérogènes** (PDF, Word, CSV, TXT, JSON…)
- Recherche **manuelle** et lente
- Pas de vision unifiée du contenu documentaire

### Solution visée

Un **portail de recherche documentaire local** qui :

1. **Ingère** des fichiers déposés dans un dossier (ou uploadés via l'interface)
2. **Extrait** le texte et les métadonnées selon le format
3. **Normalise** les données dans un schéma commun
4. **Indexe** le contenu pour la recherche
5. **Permet de rechercher** via une interface web moderne (React)
6. **Enrichit progressivement** le système avec des fonctions « intelligentes » (classification, entités, sémantique)

### Utilisateurs cibles

| Profil | Besoin |
|--------|--------|
| Utilisateur final | Rechercher un document ou une information précise |
| Administrateur | Ajouter / réindexer des sources, consulter l'état du système |
| Étudiant | Configurer, maintenir et faire évoluer le prototype |

### Périmètre MVP (version minimale fonctionnelle)

- [ ] Déposer des fichiers dans `data/raw/` ou via l'interface
- [ ] Supporter au minimum : **PDF, DOCX, CSV, TXT**
- [ ] Extraire texte + métadonnées de base (nom, type, date, taille)
- [ ] Indexer en local (SQLite + moteur plein texte)
- [ ] Rechercher par mots-clés avec classement des résultats
- [ ] Afficher les résultats dans une interface React
- [ ] API REST documentée (FastAPI)

### Hors périmètre initial (phase ultérieure)

- Déploiement cloud
- Authentification multi-utilisateurs avancée
- Connecteurs distants (API externes, bases distantes)
- Traitement de gros volumes (millions de documents)

---

## 2. Problématique (pour le rapport)

> *Comment concevoir et implémenter un système local capable d'indexer automatiquement des données hétérogènes et d'offrir une recherche d'information pertinente et exploitable via une interface web ?*

### Objectifs généraux

1. Étudier les enjeux de l'indexation de données hétérogènes
2. Concevoir une architecture modulaire ingestion → extraction → indexation → recherche
3. Réaliser un prototype fonctionnel en Python
4. Évaluer la pertinence des résultats sur un jeu de données de test
5. Proposer des perspectives d'évolution (IA, cloud, scalabilité)

### Objectifs techniques mesurables

| Objectif | Indicateur |
|----------|------------|
| Formats supportés | ≥ 4 types (PDF, DOCX, CSV, TXT) |
| Temps d'indexation | Indexer 50 documents en < 2 min (machine locale standard) |
| Recherche | Résultats en < 1 seconde sur corpus de test |
| API | Endpoints REST testables (Swagger / OpenAPI) |
| Interface | Recherche + affichage des résultats opérationnels |

---

## 3. Stack technique retenue

### Backend (Python)

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| API | **FastAPI** | Endpoints REST, documentation auto |
| Extraction PDF | **pdfplumber** | Texte depuis PDF |
| Extraction Word | **python-docx** | Texte depuis DOCX |
| Extraction CSV | **pandas** | Lecture et aplatissement du contenu |
| Métadonnées | **SQLite** + SQLAlchemy (optionnel) | Stockage structuré |
| Index plein texte | **Whoosh** | Recherche locale sans service externe |
| Validation | **Pydantic** | Schémas de données API |

### Frontend

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| UI | **React** (Vite) | Interface utilisateur moderne |
| Requêtes API | **fetch** ou **axios** | Communication avec FastAPI |
| Style | **CSS modules** ou **Tailwind** (à décider) | Mise en page |

### Intelligence (phase 4 — optionnelle mais valorisante)

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Classification | **scikit-learn** | Type de document, catégorisation |
| Entités / NLP | **spaCy** (modèle français si possible) | Dates, organisations, mots-clés |
| Recherche sémantique | **sentence-transformers** | Similarité de sens entre requête et documents |

### Outils

- **Python 3.10+**
- **Node.js 18+** (pour React)
- **Git** pour le versioning
- **pytest** pour les tests backend

---

## 4. Architecture cible

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface React (Vite)                    │
│         Recherche · Résultats · Upload · Statut              │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (REST)
┌──────────────────────────▼──────────────────────────────────┐
│                     API FastAPI (Python)                       │
│   /search · /documents · /ingest · /health                   │
└──────────┬───────────────────────────────┬──────────────────┘
           │                               │
┌──────────▼──────────┐         ┌──────────▼──────────┐
│   Couche métier     │         │   Stockage          │
│ ingestion           │         │ SQLite (métadonnées)│
│ extraction          │         │ Whoosh (index texte)│
│ indexing            │         │ data/raw/ (fichiers)│
│ search              │         └─────────────────────┘
└─────────────────────┘
```

### Structure des dossiers prévue

```
projet_tutore/
├── backend/
│   ├── app/
│   │   ├── api/           # routes FastAPI
│   │   ├── ingestion/     # scan dossier, upload
│   │   ├── extraction/    # PDF, DOCX, CSV, TXT
│   │   ├── indexing/      # Whoosh + SQLite
│   │   ├── search/        # logique de recherche
│   │   ├── models/        # schémas Pydantic + ORM
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/      # appels API
│   │   └── App.jsx
│   └── package.json
├── data/
│   ├── raw/               # fichiers à indexer
│   └── db/                # SQLite + index Whoosh
├── docs/                  # notes, diagrammes rapport
├── CAHIER_DES_CHARGES.md  # ce fichier
└── README.md
```

---

## 5. Modèle de données commun

Chaque document indexé est normalisé ainsi :

| Champ | Type | Description |
|-------|------|-------------|
| `id` | UUID / entier | Identifiant unique |
| `title` | string | Titre ou nom de fichier |
| `content` | text | Contenu textuel extrait |
| `source_path` | string | Chemin du fichier source |
| `file_type` | enum | pdf, docx, csv, txt, json… |
| `mime_type` | string | Type MIME |
| `size_bytes` | int | Taille du fichier |
| `created_at` | datetime | Date d'ajout au système |
| `indexed_at` | datetime | Date d'indexation |
| `metadata` | JSON | Infos spécifiques au format (auteur, colonnes CSV…) |
| `summary` | string | Résumé court (phase IA) |
| `tags` | list[string] | Mots-clés / catégories |

---

## 6. API REST prévue (brouillon)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | État du service |
| `GET` | `/documents` | Liste des documents indexés |
| `GET` | `/documents/{id}` | Détail d'un document |
| `POST` | `/ingest/scan` | Scanner le dossier `data/raw/` |
| `POST` | `/ingest/upload` | Upload d'un fichier |
| `GET` | `/search?q=...` | Recherche plein texte |
| `DELETE` | `/documents/{id}` | Supprimer un document de l'index |

---

## 7. Plan de réalisation par phases

### Phase 1 — Fondations
- [x] Initialiser backend FastAPI + frontend React
- [x] Définir le modèle `Document`
- [x] Endpoint `/health`
- [x] CORS configuré entre React et FastAPI

### Phase 2 — Ingestion & extraction
- [x] Scanner un dossier local
- [x] Extracteurs PDF, DOCX, CSV, TXT
- [x] Persistance SQLite
- [x] Tests unitaires sur chaque extracteur
- [x] Upload de fichiers via API (`POST /ingest/upload`)
- [x] Détail document (`GET /documents/{id}`)

### Phase 3 — Indexation & recherche
- [x] Index Whoosh sur le champ `content`
- [x] Endpoint `/search` avec score et surbrillance
- [x] Réindexation complète (`POST /index/rebuild`)

### Phase 4 — Interface React
- [x] Page d'accueil avec barre de recherche
- [x] Liste des résultats (titre, extrait, type, date)
- [x] Page détail document
- [x] Upload de fichier (optionnel MVP+)

### Phase 5 — Intelligence
- [x] Auto-tagging / classification du type
- [x] Extraction d'entités (regex + spaCy optionnel)
- [x] Recherche sémantique (TF-IDF) et mode hybride

### Phase 6 — Rapport & soutenance
- [x] Jeu de données de démonstration (20–50 fichiers) — 1 110 fichiers IBAM dans `data/raw/`
- [x] Script de génération (`scripts/generate_demo_dataset.py`)
- [x] Tests de performance basiques (`scripts/benchmark.py`, `tests/test_performance.py`)
- [x] Documentation rapport (`docs/NOTES_RAPPORT.md`, `docs/GUIDE_INSTALLATION.md`, `docs/MANUEL_UTILISATEUR.md`)
- [x] Checklist captures d'écran (`docs/CAPTURES_ECRAN.md`)
- [x] README projet
- [ ] Captures d'écran réalisées (à faire manuellement dans `docs/captures/`)
- [ ] Rédaction finale du rapport (Word/LaTeX)
- [ ] Slides de soutenance

---

## 8. Structure du rapport (format classique informatique)

1. **Page de garde** — titre, nom, encadrant, année
2. **Remerciements**
3. **Résumé / Abstract** (FR + EN si demandé)
4. **Introduction** — contexte, problématique, objectifs, méthodologie
5. **État de l'art** — texte : `rapport/02_etat_de_lart.md`
   - Recherche sans index vs avec index
   - Moteurs existants (Web, entreprise, embarqués, vectoriels)
   - Indexation classique puis indexation intelligente (littérature 2022–2026)
6. **Analyse et conception**
   - Besoins fonctionnels et non fonctionnels
   - Architecture (diagrammes)
   - Choix technologiques justifiés
7. **Réalisation**
   - Environnement de développement
   - Modules implémentés (avec extraits de code commentés)
8. **Tests et validation**
   - Protocole de test
   - Résultats (tableaux, captures)
9. **Conclusion et perspectives**
   - Bilan, limites, travaux futurs (cloud, sécurité, volume)
10. **Bibliographie / Webographie**
11. **Annexes** — guide d'installation, manuel utilisateur

> **Note :** Rédiger chaque chapitre au fur et à mesure de l'implémentation pour gagner du temps.

---

## 9. Questions ouvertes / doutes à trancher

| # | Question | Statut | Décision |
|---|----------|--------|----------|
| 1 | Date exacte de soutenance | ⏳ En attente | — |
| 2 | Consignes précises de l'école (nb pages, norme) | ⏳ En attente | À communiquer |
| 3 | Interface : React confirmé | ✅ Validé | React + Vite |
| 4 | Moteur d'index : Whoosh vs Meilisearch | 🤔 À voir | Whoosh pour simplicité locale |
| 5 | Style UI : Tailwind ou CSS simple | 🤔 À voir | — |
| 6 | Nom de la structure fictive pour la démo | 🤔 À voir | Ex. « DocuSearch BF » |
| 7 | Faut-il une authentification login ? | 🤔 À voir | Probablement non pour le MVP |
| 8 | Encadrant / tuteur — attentes spécifiques | ⏳ En attente | — |

---

## 10. Textes réutilisables pour le rapport

### Introduction (brouillon)

Les organisations produisent et accumulent quotidiennement des documents numériques sous des formats variés. Cette hétérogénéité complique la recherche d'information et réduit la productivité des utilisateurs. Ce projet vise à concevoir un système d'indexation intelligente permettant de centraliser, structurer et interroger ces données via une interface web unifiée. Développé en Python avec une API FastAPI et une interface React, le prototype fonctionne en environnement local et constitue une base extensible vers des déploiements cloud futurs.

### Mots-clés

`indexation` · `données hétérogènes` · `recherche d'information` · `plein texte` · `FastAPI` · `React` · `Python` · `NLP`

### Justification du choix React

React permet de construire une interface utilisateur moderne, réactive et maintenable. Couplé à FastAPI, il sépare clairement la couche présentation de la couche métier — une architecture en couches conforme aux bonnes pratiques en ingénierie logicielle, valorisable dans le rapport et la soutenance.

### Justification du choix Python

Python dispose d'un écosystème riche pour le traitement de documents (PDF, Office), l'analyse de données et le machine learning. Il est adapté au prototypage rapide tout en restant crédible pour un projet de master en systèmes d'information.

---

## 11. Jalons importants (checklist globale)

- [ ] Cahier des charges validé
- [ ] Environnement dev installé (Python, Node, Git)
- [ ] Backend FastAPI opérationnel
- [ ] Frontend React opérationnel
- [ ] Premier fichier PDF indexé avec succès
- [ ] Première recherche fonctionnelle bout en bout
- [x] Jeu de données de démo prêt
- [ ] Chapitres rapport rédigés
- [ ] Soutenance préparée (démo + slides)

---

## 12. Notes personnelles

_Espace libre pour vos remarques, retours du tuteur, idées en cours de route._

```
Date       | Note
-----------|--------------------------------------------------
           |
           |
```

---

*Dernière mise à jour : juillet 2026 — document vivant, à compléter au fil du projet.*
