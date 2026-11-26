# Corps du travail

## 1. Présentation

Ce chapitre organise les apports de quinze articles scientifiques (2022–2026) autour des grandes approches de l'indexation intelligente. Il ne remplace pas les bilans journaliers, qui détaillent chaque publication. Il propose une lecture transversale : constats communs, familles d'approches, puis enseignements.

## 2. Constats communs

Tous les articles partent d'un même point de départ : les données documentaires ne sont plus homogènes. Les collections mélangent texte libre, tableaux, JSON, PDF, HTML et parfois des éléments visuels. Dans ce contexte, un simple moteur de mots-clés ne suffit plus.

Trois difficultés reviennent régulièrement :

- la **diversité des formats**, qui empêche d'appliquer une seule méthode d'extraction ;
- la **perte d'information** lors du passage d'un document complexe vers un texte plat ;
- le **choix de la représentation** : termes, vecteurs, identifiants appris, métadonnées ou graphes.

Indexer devient donc un problème de conception globale : extraction, structure de l'index, modes de recherche, enrichissement et mise à jour du corpus.

## 3. Quatre familles d'approches

### 3.1. Indexation enrichie et unifiée

Une première famille modernise l'indexation sans abandonner les structures classiques. Clarke (2024) propose l'indexation annotative : le contenu est placé dans un espace d'adresses, puis enrichi d'annotations. Selon Clarke, ce cadre peut unifier index inversé, magasins de colonnes, bases orientées objet et graphes de connaissances. L'index n'est plus une simple table de mots, mais un espace annoté capable d'accueillir des données hétérogènes.

Heflin et al. (2024) traitent un cas plus concret : les données scientifiques semi-structurées en JSON. Leur indexation cell-centric transforme chaque valeur ou paire clé-valeur en unité indexable. Ces travaux confirment qu'une bonne indexation commence souvent par un choix de granularité adapté au format.

### 3.2. Indexation apprise et recherche générative

Une deuxième famille remplace, en partie, l'index externe par un modèle de neurones. Tay et al. (2022) introduisent le Differentiable Search Index (DSI) : le modèle génère directement l'identifiant du document pertinent. Wang et al. (2022) proposent le Neural Corpus Indexer (NCI), qui associe une requête à un identifiant sémantique. Zhang et al. (2024) synthétisent ce mouvement sous le nom de Generative Information Retrieval (GenIR).

Yang et al. (2023) et Lee et al. (2023) corrigent ensuite certaines limites. Avec ASI, Yang et al. apprennent dynamiquement des docids, y compris pour de nouveaux documents. Avec GLEN, Lee et al. cherchent des identifiants plus interprétables. La recherche générative est prometteuse, mais reste sensible à la représentation des documents, à l'évolution du corpus et au coût de calcul.

### 3.3. Hybridation des moteurs

Une troisième famille affirme qu'aucun moteur unique ne suffit. HetaRAG (2025) propose de combiner recherche vectorielle, plein texte, graphes et bases relationnelles. Gollapudi et al. (2024) approfondissent la recherche hybride avec ACORN, une extension de HNSW capable de traiter simultanément similarité vectorielle et contraintes structurées. Chuang et al. (2023) ajoutent une navigation par graphe de connaissances avec DiscoverPath. L'idée commune est claire : combiner plusieurs signaux de pertinence.

### 3.4. Ingestion, vision, granularité et métadonnées

Le troisième axe insiste sur l'amont du pipeline. Pérez et Vizcaino (2024) montrent que la qualité d'un système RAG dépend de l'ingestion : extraction, OCR et parsing par LLM. Faysse et al. (2024) et Yu et al. (2024) proposent d'indexer les pages comme images avec ColPali et VisRAG. Zhong et al. (2024) travaillent sur la taille des segments avec Mix-of-Granularity. Dadopoulos et al. (2025) démontrent l'intérêt des métadonnées enrichies sur documents longs et structurés.

Sans bonne extraction, sans découpage adapté et sans enrichissement, même le meilleur index produit de mauvais résultats.

## 4. Organisation des lectures

| Jour | Articles | Orientation |
|------|----------|-------------|
| **Jour 1** | Clarke ; Heflin et al. ; Tay et al. ; Wang et al. ; Zhang et al. | Fondements, données semi-structurées, naissance de la GenIR |
| **Jour 2** | Yang et al. ; Lee et al. ; HetaRAG ; Gollapudi et al. ; Chuang et al. | Docids dynamiques, hybridation, graphes |
| **Jour 3** | Pérez et Vizcaino ; Faysse et al. ; Yu et al. ; Zhong et al. ; Dadopoulos et al. | Ingestion, vision, chunking, métadonnées |

## 5. Enseignements principaux

1. L'indexation intelligente ne se réduit plus à stocker des mots : elle doit aussi représenter le sens, la structure, les relations et parfois l'apparence visuelle.  
2. La recherche générative ouvre une voie nouvelle, sans effacer les besoins classiques de mise à jour, de coût et d'interprétabilité.  
3. Les systèmes hybrides constituent une réponse pragmatique à la diversité des requêtes et des données.  
4. La qualité de l'amont — extraction, OCR, chunking, métadonnées — conditionne toute la chaîne.  
5. Pour un contexte à ressources limitées, les approches les plus immédiatement transférables semblent être l'ingestion adaptative, l'hybridation légère et l'enrichissement par métadonnées.

## 6. Synthèse

La littérature 2022–2026 décrit le passage d'un index monolithique vers des pipelines plus flexibles. Indexer des données hétérogènes demande aujourd'hui de concevoir ensemble l'extraction, la structure de l'index, la combinaison des moteurs et l'enrichissement des documents. Les bilans des trois journées détaillent chaque article ; le présent chapitre en dégage la logique d'ensemble.
