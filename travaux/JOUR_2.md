# Bilan du Jour 2

**Nombre d'articles lus :** 5  
**Orientation :** recherche générative, hybridation des moteurs et graphes de connaissances

---

## Article 6

**Intitulé :** Auto Search Indexer for End-to-End Document Retrieval  
**Auteurs :** Tianchi Yang, Minghui Song, Zihan Zhang et al. (Microsoft)  
**Année / source :** 2023, Findings of EMNLP  
**Lien :** https://aclanthology.org/2023.findings-emnlp.464/

**Résumé personnel :**

Yang et ses collègues s'attaquent à une limite de la recherche générative : les identifiants de documents sont souvent créés en prétraitement et ne s'adaptent pas aux nouveaux fichiers. Leur Auto Search Indexer apprend automatiquement des docids sémantiques pour les documents existants et futurs. Le système combine un module d'indexation sémantique et un modèle génératif entraînés conjointement grâce à un mécanisme de reparamétrisation. Yang et al. montrent aussi que des documents proches peuvent partager un même identifiant, ce qui permet de récupérer plusieurs résultats pertinents plus efficacement. Les expériences sur jeux publics et industriels montrent des gains significatifs. L'article rend la recherche générative plus réaliste pour des corpus en évolution continue.

---

## Article 7

**Intitulé :** GLEN: Generative Retrieval via Lexical Index Learning  
**Auteurs :** Sunkyu Lee, Jihyuk Kim et al.  
**Année / source :** 2023, EMNLP  
**Lien :** https://aclanthology.org/2023.emnlp-main.477/

**Résumé personnel :**

Lee et al. proposent GLEN pour améliorer la recherche générative tout en gardant des identifiants plus interprétables. Leur méthode apprend un index lexical en deux phases : d'abord la structure des identifiants, puis la relation entre requêtes et documents pertinents. GLEN cherche à réduire le décalage entre le modèle pré-entraîné et les docids, ainsi que l'écart entre entraînement et inférence. Les auteurs introduisent aussi une inférence sans collision pour classer les documents sans surcoût important. Les résultats sur NQ320k, MS MARCO et BEIR montrent que GLEN rivalise avec les meilleures méthodes génératives. Lee et al. démontrent qu'un index appris peut rester lisible et efficace.

---

## Article 8

**Intitulé :** HetaRAG: Hybrid Deep Retrieval-Augmented Generation across Heterogeneous Data Stores  
**Auteurs :** Équipe KnowledgeXLab (rapport technique, 2025)  
**Année / source :** 2025, arXiv  
**Lien :** https://arxiv.org/html/2509.21336

**Résumé personnel :**

Les auteurs de HetaRAG partent du constat qu'un seul type d'index ne suffit plus dans les systèmes RAG modernes. La recherche vectorielle comprend bien le sens, le plein texte trouve les termes exacts, les graphes représentent les relations et les bases relationnelles structurent les données. HetaRAG propose de fusionner ces moteurs dans un plan de récupération unique, capable de router et combiner les preuves selon la requête. Le rapport insiste sur le fait que la qualité de la récupération conditionne directement la fiabilité des réponses générées. Même s'il s'agit d'un travail encore en cours, HetaRAG formalise clairement la tendance à combiner plusieurs paradigmes de recherche plutôt qu'à en choisir un seul.

---

## Article 9

**Intitulé :** ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data  
**Auteurs :** Siddharth Gollapudi, Neel Karia, Varun Sivashankar et al.  
**Année / source :** 2024, Proceedings of the ACM on Management of Data (PODS)  
**Lien :** https://doi.org/10.1145/3654923

**Résumé personnel :**

Gollapudi et son équipe étudient la recherche hybride lorsque l'on combine similarité vectorielle et contraintes structurées, comme une catégorie, une date ou un attribut précis. Beaucoup de méthodes existantes sont soit trop lentes, soit trop limitées dans les filtres qu'elles acceptent. ACORN étend l'index HNSW avec une stratégie de parcours tenant compte des prédicats de la requête. Les auteurs montrent que leur approche peut être intégrée à des bibliothèques existantes et qu'elle améliore fortement le débit à rappel équivalent. Les expériences couvrent des benchmarks classiques et des corpus multimodaux plus complexes. Gollapudi et al. démontrent qu'on ne doit pas traiter la recherche sémantique et les métadonnées séparément jusqu'au dernier moment.

---

## Article 10

**Intitulé :** DiscoverPath: A Knowledge Refinement and Retrieval System for Interdisciplinarity on Biomedical Research  
**Auteurs :** Yu-Neng Chuang, Guanchu Wang, Kaixiong Zhou et al.  
**Année / source :** 2023, arXiv  
**Lien :** https://arxiv.org/pdf/2309.01808

**Résumé personnel :**

Chuang et al. développent DiscoverPath pour aider à retrouver des articles scientifiques biomédicaux, surtout dans des contextes interdisciplinaires où le vocabulaire change d'un domaine à l'autre. Le système transforme les résumés en graphe de connaissances en extrayant entités et relations. Plutôt que d'afficher tout le graphe, les auteurs ne montrent qu'un sous-graphe centré sur la requête de l'utilisateur. DiscoverPath propose aussi des recommandations de requêtes pour affiner progressivement la recherche. Chuang et al. montrent que l'indexation intelligente ne se limite pas au texte : elle peut aussi organiser les relations entre documents et concepts. Leur travail illustre comment la recherche documentaire peut devenir un parcours guidé plutôt qu'une simple liste de résultats.

---

## Point de synthèse — fin du Jour 2

Les cinq articles du Jour 2 montrent que la recherche documentaire évolue vers des systèmes plus flexibles. Yang et Lee améliorent la recherche générative ; HetaRAG et ACORN combinent plusieurs types d'index ; Chuang et al. ajoutent une navigation par graphe de connaissances.
