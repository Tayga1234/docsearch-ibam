# Résultats des tests de performance — DocSearch

*Généré le 2026-11-04 11:53 UTC*

## Synthèse

| Indicateur | Valeur | Objectif | Statut |
|------------|--------|----------|--------|
| Documents indexés | 1110 | >= 20 | OK |
| Durée indexation complète | 25.742 s | < 120 s | OK |
| Recherche max (tous modes) | 463.5 ms | < 1000 ms | OK |

## Détail par mode de recherche

| Mode | Moyenne (ms) | P95 (ms) | Max (ms) |
|------|--------------|----------|----------|
| keyword | 37.04 | 51.2 | 51.2 |
| semantic | 99.87 | 463.5 | 463.5 |
| hybrid | 82.22 | 99.6 | 99.6 |

## Méthodologie

- Corpus : fichiers dans `C:\Users\korog\Desktop\ecole\projet_tutore\data\raw`
- Requêtes testées : formation, DocSearch, budget, IBAM, indexation (cinq mesures par mode)
- Modes, dans cet ordre : keyword, semantic, hybrid
- Commande : `python scripts/benchmark.py`
- L’indexation Whoosh n’entraîne pas la matrice TF-IDF. Celle-ci est construite au premier appel de `semantic_search`, puis réutilisée. Le maximum sémantique (463,5 ms) est ce premier appel, construction comprise. L’hybride a été chronométré ensuite, cache déjà construit.
- Avec cinq mesures, le P95 calculé coïncide avec le maximum dans les trois modes. Les deux colonnes sont conservées.
