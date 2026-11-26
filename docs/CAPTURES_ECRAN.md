# Checklist des captures d'écran — Rapport et soutenance

Réaliser ces captures une fois l'application lancée (backend 8010 + frontend Vite) avec le jeu de démo indexé.

## Préparation

1. Générer les données : `python scripts/generate_demo_dataset.py`
2. Lancer backend et frontend
3. Indexer le dossier (documents indexés)
4. Résolution recommandée : 1920×1080 ou 1440×900
5. Enregistrer dans `docs/captures/` (créer le dossier)

## Captures obligatoires

| # | Fichier suggéré | Contenu | Usage rapport |
|---|-----------------|---------|---------------|
| 1 | `01_accueil.png` | Page d'accueil, badge API vert, liste documents | Ch. Réalisation / Interface |
| 2 | `02_recherche_hybride.png` | Recherche « formation », mode Hybride, résultats | Ch. Tests |
| 3 | `03_recherche_mots_cles.png` | Même requête, mode Mots-clés | Comparaison modes |
| 4 | `04_recherche_semantique.png` | Requête « portail documentaire », mode Sémantique | Ch. Intelligence |
| 5 | `05_detail_document.png` | Modal détail : résumé, tags, entités, contenu | Ch. Réalisation |
| 6 | `06_upload.png` | Upload ou résultat après ajout fichier | Ch. Ingestion |
| 7 | `07_scan_resultat.png` | Message après scan (X indexés) | Ch. Ingestion |
| 8 | `08_swagger.png` | Page http://127.0.0.1:8010/docs | Ch. API |
| 9 | `09_architecture.png` | Diagramme architecture (export depuis CAHIER_DES_CHARGES) | Ch. Conception |
| 10 | `10_performance.png` | Tableau PERFORMANCE_RESULTS.md ou terminal benchmark | Ch. Tests |

## Captures optionnelles (soutenance)

| # | Fichier | Contenu |
|---|---------|---------|
| 11 | `11_sidebar.png` | Barre latérale avec actions |
| 12 | `12_erreur_api.png` | Badge rouge (backend arrêté) — pour expliquer le dépannage |
| 13 | `13_csv_detail.png` | Détail d'un fichier CSV (métadonnées colonnes) |

## Conseils pour la soutenance

- Préparer une **démo live** de 5 minutes : recherche → détail → upload → scan
- Avoir un **plan B** : captures en PDF si réseau ou API en panne
- Montrer la **différence hybride vs mots-clés** sur la requête « budget »

## Légendes types (à copier sous chaque figure)

> *Figure X — Interface de recherche hybride du portail DocSearch BF (corpus IBAM, 1 110 documents indexés).*

> *Figure X — Documentation OpenAPI auto-générée par FastAPI.*
