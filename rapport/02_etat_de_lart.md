# Chapitre — État de l’art

**Thème :** Indexation intelligente de données pour la recherche d’information  
**Objet :** situer le travail par rapport aux moteurs existants, à la différence *avec / sans index*, puis à la littérature scientifique récente (2022–2026).

Ce chapitre constitue le socle théorique du rapport. L’application (DocuSearch) n’est évoquée qu’en **positionnement** en fin de chapitre ; sa conception et sa réalisation font l’objet des chapitres suivants.

---

## 1. Introduction

La recherche d’information (RI, *Information Retrieval*) vise à retrouver, dans une collection, les documents **pertinents** vis-à-vis d’un besoin exprimé par une requête. Dans les organisations, ce besoin est quotidien : retrouver un compte rendu, une procédure, un budget, une note de service. Or beaucoup d’outils présentés comme des « moteurs de recherche » ne font que **parcourir** des fichiers au moment de la requête. D’autres, au contraire, **préparent** le corpus : ils extraient le contenu, le structurent, l’indexent, parfois l’enrichissent, puis répondent rapidement.

Le thème retenu — *indexation intelligente de données pour la recherche d’information* — place donc l’**index** au centre. L’intelligence ne désigne pas seulement l’usage d’un modèle de langage. Elle désigne l’ensemble des méthodes qui vont au-delà d’un simple inventaire de mots : métadonnées, tags, résumés, entités, signaux sémantiques, combinaison de plusieurs moteurs.

Ce chapitre procède en trois temps :

1. clarifier ce qu’est (et n’est pas) un moteur de recherche, en distinguant **recherche sans index** et **recherche avec index** ;
2. dresser un **panorama des moteurs et plateformes existants** ;
3. présenter l’**évolution scientifique** de l’indexation (fondements classiques, puis quinze articles 2022–2026) et en dégager les enseignements pour un système local.

---

## 2. Définitions et cadre

### 2.1. Recherche d’information

Selon le cadre classique (Manning, Raghavan et Schütze, *Introduction to Information Retrieval*), un système de RI comprend au minimum :

- une **collection** de documents ;
- une **requête** exprimant un besoin ;
- un mécanisme qui produit une **liste ordonnée** (ranking) ;
- une notion de **pertinence** (adéquation document / besoin).

Les mesures usuelles d’évaluation sont la **précision** (parmi les documents renvoyés, quelle part est pertinente) et le **rappel** (parmi tous les documents pertinents, quelle part a été retrouvée). Des mesures agrégées comme le nDCG évaluent aussi la qualité du classement.

### 2.2. Indexation

**Indexer**, ce n’est pas classer des fichiers dans des dossiers. C’est transformer les documents en une **structure de données** qui rend la recherche efficace. L’index inversé, fondement des moteurs lexicaux, associe à chaque terme la liste des documents (et souvent des positions) où il apparaît. Sans cette préparation, chaque requête obligerait à relire l’ensemble du corpus.

On appellera **indexation intelligente** une indexation qui ne se limite pas aux termes bruts. Elle peut intégrer :

- des **métadonnées** (titre, type, date, auteur) ;
- des **annotations** (tags, entités, résumés, scores) ;
- des **représentations de sens** (vecteurs, similarité) ;
- parfois des **identifiants appris** par un modèle (recherche générative).

### 2.3. Données documentaires

Les collections réelles mélangent PDF, documents bureautiques, tableaux, notes texte, parfois JSON ou pages HTML. Cette diversité n’est plus le titre du thème, mais elle reste un **fait empirique** : un système de RI utile doit pouvoir **lire** ces contenus avant de les indexer. La qualité de l’extraction conditionne celle de l’index.

---

## 3. Recherche sans indexation et recherche avec indexation

Cette distinction est le premier levier d’analyse du présent travail. Elle évite de confondre **interface de recherche** et **moteur de recherche**.

### 3.1. Recherche sans index (parcours à la requête)

Le système parcourt les fichiers, les lignes d’une table ou le document ouvert **au moment** où l’utilisateur cherche.

| Mécanisme | Exemples | Comportement |
|-----------|----------|----------------|
| Recherche dans le fichier ouvert | `Ctrl+F` dans un PDF ou un traitement de texte | Scan linéaire du contenu affiché |
| Recherche dans un dossier | Explorateur Windows (contenu non indexé), `grep` | Lecture successive des fichiers |
| Filtrage SQL naïf | `LIKE '%terme%'` sans index plein texte | Parcours des lignes |
| Recherche sur le nom | beaucoup de partages de fichiers mal configurés | Aucune analyse du contenu |

**Avantages :** simplicité, pas de phase de préparation, résultats toujours « à jour » par rapport au disque.

**Limites :**

- le temps croît avec le volume (complexité proche d’un parcours complet) ;
- pas de **classement par pertinence** (ou un classement très pauvre) ;
- pas d’enrichissement (résumé, tags, entités) ;
- difficulté à retrouver une information si le mot exact n’apparaît pas ;
- impossible de combiner efficacement plusieurs signaux (titre, contenu, métadonnées).

En résumé : l’outil **cherche dans les fichiers**. Il ne dispose pas d’une mémoire organisée du corpus.

### 3.2. Recherche avec index (préparation puis interrogation)

Le système construit **avant** les requêtes une structure (index inversé, index vectoriel, table de métadonnées, ou combinaison). La requête consulte cet index.

**Avantages :**

- temps de réponse faible, même sur des corpus plus larges ;
- ranking (TF-IDF, BM25, similarité vectorielle, fusion hybride) ;
- possibilité d’enrichir les documents **à l’ingestion** ;
- mises à jour incrémentales (réindexer un fichier modifié plutôt que tout relire à chaque recherche).

**Contrepartie :** il faut un **pipeline** d’ingestion, de l’espace disque pour l’index, et une stratégie de mise à jour (ajout, modification, suppression).

En résumé : l’outil **cherche dans un index préparé**. C’est la condition d’une RI digne de ce nom.

### 3.3. Tableau de synthèse

| Critère | Sans index | Avec index lexical | Indexation plus « intelligente » |
|---------|------------|--------------------|----------------------------------|
| Quand a lieu le travail lourd | À chaque requête | À l’ingestion (puis requêtes légères) | Idem, plus enrichissement |
| Objet interrogé | Fichiers / chaînes | Termes (index inversé) | Termes + métadonnées + éventuellement vecteurs |
| Pertinence | Absente ou faible | BM25 / TF-IDF | Hybride, annotations, parfois génération |
| Exemples | Ctrl+F, grep, LIKE | Lucene, Elasticsearch, Whoosh | Systèmes hybrides, GenIR, RAG enrichi |

Cette grille guide la lecture des moteurs du marché comme celle de la littérature récente : la question n’est plus seulement « y a-t-il une barre de recherche ? », mais « **que contient l’index, et comment a-t-il été construit ?** »

---

## 4. Panorama des moteurs et plateformes existants

Les outils ci-dessous ne sont pas tous des « concurrents » d’un prototype académique. Ils illustrent **où** se situe l’indexation dans l’écosystème réel.

### 4.1. Moteurs du Web

Google et Bing incarnent la RI à très grande échelle : crawl, index mondial, ranking sophistiqué (signaux lexicaux, liens, comportement, désormais aussi modèles de langage). Ils démontrent la puissance d’un index **préparé**, mais leur objet est le Web public, pas les archives internes d’une organisation. Ils ne se déploient pas en local sur un corpus métier privé.

### 4.2. Moteurs documentaires d’entreprise

| Famille | Exemples | Caractéristique |
|---------|----------|-----------------|
| Plein texte distribué | Elasticsearch, OpenSearch, Apache Solr (Lucene) | Index inversé, facettes, montée en charge, exploitation |
| Suite collaborative | SharePoint Search | Recherche intégrée à la GED Microsoft |
| SaaS de search | Algolia | Recherche rapide, surtout pour sites et catalogues |

Ces moteurs **possèdent une indexation**. Ils sont adaptés aux volumes importants et aux équipes d’exploitation. Leur coût (infra, configuration, compétences) les rend souvent disproportionnés pour une petite structure ou un MVP académique.

Heflin et al. (2024) s’appuient d’ailleurs sur **Elasticsearch** pour indexer des données scientifiques semi-structurées : le moteur industriel sert de brique, l’apport scientifique portant sur *quoi* indexer (granularité cell-centric), pas sur le remplacement de Lucene.

### 4.3. Moteurs embarqués, légers ou open source « search »

| Outil | Positionnement |
|-------|----------------|
| Apache Lucene | Bibliothèque d’indexation (cœur de Solr / Elasticsearch) |
| Whoosh | Moteur plein texte en Python, embarqué, sans serveur dédié |
| SQLite FTS | Plein texte dans un fichier SQLite |
| Meilisearch, Typesense | Moteurs modernes, plus simples qu’un cluster Elastic |

Ils illustrent qu’un **vrai index** n’exige pas un data center. Ils restent toutefois, dans leur usage de base, des index **lexicaux** : mots, éventuellement typo-tolérance, pas forcément enrichissement sémantique ni pipeline multi-formats.

### 4.4. Index vectoriels et systèmes RAG

La recherche sémantique encode textes et requêtes en vecteurs, puis cherche les plus proches voisins (ANN, HNSW, etc.). Bibliothèques et bases : FAISS, Qdrant, Milvus, kNN dans Elasticsearch/OpenSearch.

Les assistants documentaires (PrivateGPT, AnythingLLM, et plus généralement les pipelines RAG) **retrèvent** des passages puis **génèrent** une réponse. Leur qualité dépend entièrement de l’index de récupération (Pérez et Vizcaino, 2024 ; HetaRAG, 2025). Ce ne sont pas des substituts à l’indexation : ils la **supposent**.

### 4.5. Stockage, GED et outils qui « cherchent » sans index de contenu

Google Drive, OneDrive, Nextcloud, l’explorateur de fichiers ou une GED minimale offrent souvent une recherche sur **noms**, dossiers, parfois un index partiel du contenu selon l’offre et la configuration. Paperless-ngx, Zotero ou Mendeley indexent un type de corpus particulier (scans administratifs, références bibliographiques). Ils montrent que le besoin existe, mais que **l’objet** (stockage, archivage, bibliographie, chat) n’est pas toujours une RI documentaire générale avec enrichissement.

**Enseignement :** il existe de nombreux outils. La ligne de partage utile n’est pas « plateforme connue / prototype étudiant », c’est **présence ou absence d’une indexation de contenu**, puis **richesse de cette indexation**.

---

## 5. Fondements de l’indexation classique

Avant les travaux 2022–2026, le modèle dominant est le suivant.

### 5.1. Pipeline lexical

1. acquisition des documents ;  
2. analyse (tokenisation, éventuellement stemming, suppression de mots vides) ;  
3. construction de l’**index inversé** ;  
4. pour une requête : lookup des termes, scoring, liste ordonnée.

Le scoring **TF-IDF** pondère un terme s’il est fréquent dans le document (TF) mais rare dans la collection (IDF). **BM25** est une fonction de ranking lexicale encore largement utilisée, souvent combinée aujourd’hui à un signal vectoriel.

### 5.2. Limites reconnues

- **Vocabulaire :** le document pertinent peut ne pas contenir les mots exacts de la requête (*mismatch*).  
- **Structure :** tableaux, mises en page, champs JSON mal aplatis perdent de l’information.  
- **Mise à jour :** un index figé vieillit ; un corpus vivant exige une politique d’update.  
- **Un seul signal :** le lexical seul ignore le sens, les relations et une partie des métadonnées.

Ces limites expliquent le tournant décrit dans la section suivante : enrichir l’index, l’apprendre, le combiner, ou soigner l’amont.

---

## 6. Indexation intelligente : littérature 2022–2026

Le corpus de quinze articles (cinq par jour, trois jours) n’a pas été changé avec le recentrage du thème. Il décrit **comment l’index devient plus riche**, une fois admis qu’il faut un index.

Quatre familles se dégagent.

### 6.1. Index enrichi et unifié

Clarke (2024) propose l’**indexation annotative** : le contenu est placé dans un espace d’adresses, puis enrichi d’annotations (segmentation, entités, scores, vecteurs). Ce cadre vise à unifier index inversé, magasins de colonnes, bases objets et graphes. L’index n’est plus une simple table de mots.

Heflin et al. (2024) traitent des JSON scientifiques dont le schéma varie. L’indexation **cell-centric** rend chaque valeur ou paire clé-valeur interrogeable, via Elasticsearch, sans schéma unique connu à l’avance.

**Apport pour le thème :** l’intelligence commence par le **choix de ce que l’on indexe** (unité, annotations), pas seulement par l’algorithme de ranking.

### 6.2. Index appris et recherche générative (GenIR)

Tay et al. (2022) introduisent le *Differentiable Search Index* (DSI) : la mémoire d’un Transformer **remplace** en partie l’index externe ; la recherche devient génération d’identifiants de documents (docids).

Wang et al. (2022) proposent le *Neural Corpus Indexer* (NCI) : un modèle séquence-à-séquence associe requête et identifiant sémantique, en fusionnant indexation et entraînement.

Zhang et al. (2024) synthétisent le passage *from matching to generation* (GenIR) : limites de coût, de mise à jour du corpus et de passage à l’échelle.

Yang et al. (2023), avec ASI, apprennent des docids aussi pour les **nouveaux** documents. Lee et al. (2023), avec GLEN, visent des identifiants plus **interprétables** via un index lexical appris.

**Apport pour le thème :** une branche de l’état de l’art **intériorise** l’index dans le modèle. C’est puissant, mais exigeant (GPU, réentraînement, corpus évolutif). Ce n’est pas le seul chemin vers une indexation « intelligente ».

### 6.3. Hybridation des moteurs

HetaRAG (KnowledgeXLab, 2025) part du constat qu’un seul type d’index ne suffit plus : vecteurs (sens), plein texte (termes exacts), graphes (relations), bases relationnelles (structure). Il faut **router et fusionner** selon la requête.

Gollapudi et al. (2024) présentent ACORN : recherche hybride **vecteurs + prédicats structurés** (catégorie, date, attributs) au-dessus de HNSW, plutôt que de filtrer trop tard.

Chuang et al. (2023) illustrent avec DiscoverPath une navigation par **graphe de connaissances** sur la littérature biomédicale.

**Apport pour le thème :** les moteurs existants ne s’excluent pas. La RI contemporaine **combine des index**. L’hybride lexical + sémantique en est la version la plus transférable hors des très gros systèmes.

### 6.4. Amont : ingestion, vision, granularité, métadonnées

Pérez et Vizcaino (2024) montrent que la qualité d’un RAG dépend de l’**ingestion** : extraction, OCR, parsing, Markdown structuré. Un mauvais amont ruine le meilleur index.

Faysse et al. (2024), ColPali, et Yu et al. (2024), VisRAG, indexent la **page comme image** via des modèles vision-langage, pour limiter la perte liée à un OCR ou un parsing pauvre.

Zhong et al. (2024) étudient la **granularité** des chunks (Mix-of-Granularity) : trop petit ou trop grand dégrade la récupération.

Dadopoulos et al. (2025) montrent, sur des rapports financiers longs, que des **métadonnées riches** (résumés, entités, thèmes) intégrées aux segments améliorent fortement la RI, parfois plus qu’un seul reranker.

**Apport pour le thème :** l’index intelligent est aussi le produit de ce que l’on a **extrait et ajouté** avant de stocker les termes ou les vecteurs.

### 6.5. Organisation du corpus de lecture

| Jour | Articles | Orientation |
|------|----------|-------------|
| 1 | Clarke ; Heflin et al. ; Tay et al. ; Wang et al. ; Zhang et al. | Fondements, données semi-structurées, naissance de la GenIR |
| 2 | Yang et al. ; Lee et al. ; HetaRAG ; Gollapudi et al. ; Chuang et al. | Docids dynamiques, hybridation, graphes |
| 3 | Pérez et Vizcaino ; Faysse et al. ; Yu et al. ; Zhong et al. ; Dadopoulos et al. | Ingestion, vision, chunking, métadonnées |

Les résumés individuels (~200 mots) figurent dans les bilans journaliers (`travaux/JOUR_1.md`, `JOUR_2.md`, `JOUR_3.md`). Le présent chapitre en donne la **lecture transversale** alignée sur le thème.

---

## 7. Enseignements transversaux

1. **Sans index, pas de RI scalable.** Les outils de parcours (Ctrl+F, grep, LIKE) et les moteurs à index n’appartiennent pas à la même famille fonctionnelle.

2. **Les moteurs du marché confirment ce constat.** Google, Elasticsearch, Lucene, Whoosh, Meilisearch, les bases vectorielles : tous **indexent**. Ils diffèrent par l’échelle, le type d’index (lexical, vectoriel, hybride) et le coût de déploiement.

3. **L’indexation intelligente élargit le contenu de l’index.** Annotations (Clarke), granularité adaptée (Heflin, Zhong), identifiants appris (DSI, NCI, ASI, GLEN), multi-stores (HetaRAG, ACORN), enrichissement (Dadopoulos), vision (ColPali, VisRAG).

4. **Un seul moteur ne suffit plus** pour toutes les requêtes : termes exacts, sens, filtres structurés, relations.

5. **L’amont conditionne l’aval.** Extraire, découper, enrichir mal, c’est indexer du bruit.

6. **Le transfert vers un contexte à ressources limitées** favorise l’hybridation légère, l’enrichissement de métadonnées et une ingestion multi-formats, plutôt que la GenIR lourde ou un cluster Elastic.

---

## 8. Positionnement du présent travail

Le prototype associé au rapport se situe explicitement du côté des **systèmes à index**, non du côté de la recherche naïve dans les fichiers.

Il ne prétend ni égaler un moteur Web, ni reproduire DSI/NCI, ni déployer Elasticsearch. Il **transfère** ce qui est réaliste en local :

| Idée de l’état de l’art | Traduction visée |
|-------------------------|------------------|
| Nécessité d’un index | Index lexical embarqué (type Whoosh) + persistance des métadonnées |
| Hybridation (HetaRAG, ACORN) | Modes mots-clés, sémantique légère, hybride |
| Enrichissement (Clarke, Dadopoulos) | Tags, résumé extractif, entités |
| Ingestion (Pérez) | Extracteurs selon le type de fichier |
| GenIR / vision | Cités comme perspectives, hors cœur d’un MVP local |

L’originalité n’est pas d’inventer un paradigme nouveau, mais de **rendre visible**, dans un pipeline démontrable, que la qualité de la recherche d’information dépend d’une indexation préparée et enrichie — là où beaucoup d’usages organisationnels en restent au parcours de dossiers.

---

## 9. Conclusion du chapitre

L’état de l’art distingue d’abord les outils qui **parcourent** le corpus à la requête et ceux qui **indexent**. Les moteurs existants (Web, entreprise, embarqués, vectoriels) appartiennent à la seconde famille, avec des écarts d’échelle et de richesse. La littérature 2022–2026 ne remet pas en cause le besoin d’index : elle en **complexifie le contenu** (annotations, apprentissage, hybridation, amont multimodal).

Le chapitre suivant pourra s’appuyer sur cette carte pour justifier l’analyse des besoins et les choix de conception : un système local d’indexation intelligente, au service de la recherche d’information.

---

## Références

### Fondements

Manning, C. D., Raghavan, P. et Schütze, H. *Introduction to Information Retrieval*. Cambridge University Press. (index inversé, TF-IDF, évaluation de la RI)

Robertson, S. et Zaragoza, H. Travaux fondateurs sur **BM25** (ranking lexical).

Documentation et écosystème : Apache Lucene ; Elasticsearch / OpenSearch ; Whoosh.

### Corpus scientifique du travail (2022–2026)

Clarke, C. L. A. (2024). *Annotative Indexing*. arXiv. https://arxiv.org/html/2411.06256

Jagini, K., Zhang, Y., Heflin, J. et al. (2024). *Data Discovery and Indexing for Semi-Structured Scientific Data*. DATA 2024, SCIEPRESS. https://www.scitepress.org/Papers/2024/127060/

Tay, Y., Tran, V. Q., Metzler, D. et al. (2022). *Transformer Memory as a Differentiable Search Index*. NeurIPS. https://proceedings.neurips.cc/paper_files/paper/2022/file/892840a6123b5ec99ebaab8be1530fba-Paper-Conference.pdf

Wang, Z., Ren, H. et al. (2022). *A Neural Corpus Indexer for Document Retrieval*. NeurIPS. https://papers.neurips.cc/paper_files/paper/2022/file/a46156bd3579c3b268108ea6aca71d13-Paper-Conference.pdf

Zhang, Y., Mao, J. et al. (2024). *From Matching to Generation: A Survey on Generative Information Retrieval*. arXiv. https://arxiv.org/html/2404.14851

Yang, T., Song, M., Zhang, Z. et al. (2023). *Auto Search Indexer for End-to-End Document Retrieval*. Findings of EMNLP. https://aclanthology.org/2023.findings-emnlp.464/

Lee, S., Kim, J. et al. (2023). *GLEN: Generative Retrieval via Lexical Index Learning*. EMNLP. https://aclanthology.org/2023.emnlp-main.477/

KnowledgeXLab (2025). *HetaRAG: Hybrid Deep Retrieval-Augmented Generation across Heterogeneous Data Stores*. arXiv. https://arxiv.org/html/2509.21336

Gollapudi, S., Karia, N., Sivashankar, V. et al. (2024). *ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data*. PACMMOD / PODS. https://doi.org/10.1145/3654923

Chuang, Y.-N., Wang, G., Zhou, K. et al. (2023). *DiscoverPath: A Knowledge Refinement and Retrieval System for Interdisciplinarity on Biomedical Research*. arXiv. https://arxiv.org/pdf/2309.01808

Pérez, A. et Vizcaino, X. (2024). *Advanced Ingestion Process Powered by LLM Parsing for RAG System*. arXiv. https://arxiv.org/html/2412.15262

Faysse, M., Sibille, H., Wu, T. et al. (2024). *ColPali: Efficient Document Retrieval with Vision Language Models*. arXiv. https://arxiv.org/pdf/2407.01449

Yu, S., Chen, C., Liu, Z. et al. (2024). *VisRAG: Vision-based Retrieval-Augmented Generation on Multi-modality Documents*. arXiv. https://arxiv.org/html/2410.10594

Zhong, Z., Shen, Y., Liu, P. et al. (2024). *Mix-of-Granularity: Optimize the Chunking Granularity for Retrieval-Augmented Generation*. arXiv / COLING. https://arxiv.org/html/2406.00456

Dadopoulos, M., Ladas, A., Moschidis, S. et Negkakis, I. (2025). *Metadata-Driven Retrieval-Augmented Generation for Financial Question Answering*. arXiv. https://arxiv.org/html/2510.24402
