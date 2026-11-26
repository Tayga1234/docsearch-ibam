# Conclusion et perspectives

## 1. Bilan

L'analyse de quinze articles publiés entre 2022 et 2026 permet de mieux comprendre l'évolution de l'indexation intelligente de données hétérogènes. Le domaine ne se limite plus à l'index inversé classique. Les recherches récentes proposent des index unifiés, appris, hybrides, multimodaux et enrichis par des métadonnées.

Les lectures confirment quatre tendances :

- adapter l'indexation à des formats variés (Clarke, 2024 ; Heflin et al., 2024) ;
- faire évoluer la recherche vers des modèles génératifs (Tay et al., 2022 ; Wang et al., 2022 ; Yang et al., 2023 ; Lee et al., 2023 ; Zhang et al., 2024) ;
- combiner plusieurs moteurs de recherche (HetaRAG, 2025 ; Gollapudi et al., 2024 ; Chuang et al., 2023) ;
- améliorer l'amont du pipeline — ingestion, chunking, vision et métadonnées (Pérez et Vizcaino, 2024 ; Faysse et al., 2024 ; Yu et al., 2024 ; Zhong et al., 2024 ; Dadopoulos et al., 2025).

Au terme de cette revue, l'indexation intelligente apparaît comme un problème de conception globale. Extraire, structurer, enrichir, indexer et rechercher forment une chaîne continue : la qualité de chaque étape conditionne celle des suivantes.

## 2. Apports du travail

Ce travail a permis de :

1. constituer un corpus récent et cohérent de quinze articles scientifiques ;
2. produire des résumés personnels, distincts des abstracts, en citant les auteurs ;
3. dégager quatre familles d'approches ;
4. formuler des enseignements transversaux utiles pour situer le sujet dans son contexte scientifique actuel.

La méthode en trois journées de cinq articles s'est révélée efficace : elle force à lire régulièrement, à synthétiser chaque jour, puis à construire une vision d'ensemble.

## 3. Limites

Du côté de la littérature, certains articles restent très techniques et difficiles à déployer sans ressources importantes. D'autres travaux sont encore en cours de développement, comme HetaRAG. Peu d'articles traitent explicitement le contexte des petites organisations ou des environnements à ressources limitées.

Du côté de ce travail, la revue reste sélective : quinze articles ne couvrent pas tout le domaine. Les bilans privilégient la compréhension des idées plutôt qu'une évaluation expérimentale comparative. Cette synthèse est donc une cartographie raisonnée, non un benchmark.

## 4. Perspectives

Les travaux futurs pourraient explorer :

1. **Hybridation légère** — combiner recherche par mots-clés et recherche sémantique sans dépendre exclusivement de modèles très coûteux ;
2. **Enrichissement automatique** — générer tags, entités, résumés et métadonnées ;
3. **Ingestion adaptative** — choisir la stratégie d'extraction selon le type de fichier ;
4. **Granularité du découpage** — tester plusieurs tailles de chunks et, si possible, un routage selon la requête ;
5. **Indexation visuelle** — expérimenter, pour les PDF complexes, une indexation par pages images ;
6. **Module RAG** — générer des réponses fondées sur les documents retrouvés, avec attention à la source et à la fidélité.

Pour des données hétérogènes, l'index intelligent n'est pas une structure unique, mais un pipeline capable de s'adapter au format, au contenu et au type de requête.

## 5. Conclusion finale

Entre 2022 et 2026, la littérature est passée d'une vision centrée sur l'index inversé à des approches plus riches : annotations, index appris, moteurs hybrides, vision-langage et métadonnées. Les quinze articles lus offrent une base solide pour comprendre les problèmes, les solutions actuelles et les directions de recherche.

Ce travail de revue de littérature situe le sujet dans son contexte scientifique récent. Il prépare aussi toute réflexion applicative visant à indexer et rechercher efficacement des collections documentaires variées.
