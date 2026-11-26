# Guide d'installation — DocSearch BF

Ce guide décrit l'installation de l'environnement de développement sur Windows (adaptable Linux/macOS).

## 1. Prérequis

| Logiciel | Version minimale | Vérification |
|----------|------------------|--------------|
| Python | 3.10 | `python --version` |
| Node.js | 18 | `node --version` |
| npm | 9+ | `npm --version` |
| Git | 2.x | `git --version` |

## 2. Cloner et préparer le projet

```powershell
cd C:\Users\korog\Desktop\ecole
git clone <url-du-repo> projet_tutore
cd projet_tutore
```

## 3. Environnement Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Dépendance optionnelle (NLP avancé)

```powershell
pip install spacy
python -m spacy download fr_core_news_sm
```

Sans spaCy, l'extraction d'entités utilise des expressions régulières (fonctionnel).

## 4. Frontend React

```powershell
cd frontend
npm install
cd ..
```

## 5. Données de démonstration

```powershell
.venv\Scripts\python.exe scripts\generate_demo_dataset.py
```

1 110 fichiers sont créés dans `data/raw/` (TXT, CSV, DOCX, PDF, années 2020-2026). La génération des PDF et DOCX peut prendre une minute.

## 6. Lancement

### Backend (port 8010)

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Vérifier : http://127.0.0.1:8010/health

### Frontend

```powershell
cd frontend
npm run dev
```

Ouvrir l'URL indiquée (souvent http://localhost:5173).

## 7. Indexation initiale

Depuis l'interface : bouton **Indexer le dossier**.

Ou en ligne de commande :

```powershell
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:8010/ingest/scan?force=true"
```

## 8. Dépannage

| Problème | Solution |
|----------|----------|
| Badge API rouge | Vérifier que le backend tourne sur 8010 ; rafraîchir Ctrl+F5 |
| Port 8010 occupé | `netstat -ano \| findstr :8010` puis `Stop-Process -Id <PID> -Force` |
| Port 5173 occupé | Vite bascule sur 5174 (normal) ; le proxy `/api` gère le CORS |
| Erreur debugpy | Utiliser uvicorn directement, pas la commande debugpy manuelle |

## 9. Tests

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest tests -v
..\.venv\Scripts\python.exe ..\scripts\benchmark.py
```

Résultats performance : `docs/PERFORMANCE_RESULTS.md`
