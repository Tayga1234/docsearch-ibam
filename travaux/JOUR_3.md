# Bilan du Jour 3

**Nombre d'articles lus :** 5  
**Orientation :** ingestion, indexation visuelle, granularité et métadonnées

---

## Article 11

**Intitulé :** Advanced Ingestion Process Powered by LLM Parsing for RAG System  
**Auteurs :** Alejandro Pérez, Xavier Vizcaino  
**Année / source :** 2024, arXiv  
**Lien :** https://arxiv.org/html/2412.15262

**Résumé personnel :**

Pérez et Vizcaino montrent que la qualité d'un système RAG dépend fortement de la phase d'ingestion. Si l'extraction initiale est mauvaise, la recherche et la génération aval seront elles aussi dégradées. Face à des PDF scannés, des présentations ou des documents complexes, ils combinent trois stratégies : extraction rapide, OCR et analyse par modèle de langage. Un agent assembleur reconstitue ensuite le document en Markdown structuré, avec des métadonnées contextuelles. Pérez et Vizcaino insistent sur le fait que l'ingestion doit être adaptative selon le type de document. Leurs expériences montrent des gains en pertinence et en fidélité des réponses. L'article rappelle qu'avant d'indexer intelligemment, il faut d'abord lire correctement des données hétérogènes.

---

## Article 12

**Intitulé :** ColPali: Efficient Document Retrieval with Vision Language Models  
**Auteurs :** Manuel Faysse, Hugues Sibille, Tony Wu et al.  
**Année / source :** 2024, arXiv  
**Lien :** https://arxiv.org/pdf/2407.01449

**Résumé personnel :**

Faysse et ses coauteurs expliquent qu'un document n'est pas réduit à sa transcription textuelle. Mise en page, tableaux, figures et structure visuelle portent aussi de l'information. ColPali indexe directement les pages comme images à l'aide d'un modèle vision-langage, sans passer par un long pipeline OCR et chunking. Les auteurs introduisent aussi ViDoRe, un benchmark pour évaluer la recherche visuelle de pages. Les résultats montrent que ColPali surpasse de nombreuses méthodes textuelles tout en réduisant parfois le temps d'indexation. Faysse et al. proposent ainsi une autre définition de l'indexation : l'unité de recherche peut être l'image de la page elle-même.

---

## Article 13

**Intitulé :** VisRAG: Vision-based Retrieval-Augmented Generation on Multi-modality Documents  
**Auteurs :** Shi Yu, Chaoyu Chen, Zhiyuan Liu et al. (OpenBMB)  
**Année / source :** 2024, arXiv  
**Lien :** https://arxiv.org/html/2410.10594

**Résumé personnel :**

Yu et al. proposent VisRAG, un pipeline RAG qui évite de convertir les documents en texte avant l'indexation. Un modèle vision-langage encode les pages comme images, puis les récupère pour alimenter la génération de réponse. Les auteurs montrent que le parsing textuel entraîne souvent une perte d'information, surtout pour les documents multimodaux. VisRAG améliore les performances de récupération et de génération par rapport aux approches purement textuelles, avec des gains importants en bout de bout. Yu et al. élargissent ainsi la réflexion ouverte par ColPali à l'ensemble du cycle RAG. L'article démontre que l'indexation peut s'appuyer sur la vision lorsque le format du document le rend nécessaire.

---

## Article 14

**Intitulé :** Mix-of-Granularity: Optimize the Chunking Granularity for Retrieval-Augmented Generation  
**Auteurs :** Zijie Zhong, Yikang Shen, Pengfei Liu et al.  
**Année / source :** 2024, COLING 2025 / arXiv  
**Lien :** https://arxiv.org/html/2406.00456

**Résumé personnel :**

Zhong et al. s'intéressent à la taille des morceaux de texte utilisés pour l'indexation dans les systèmes RAG. Un chunk trop petit perd le contexte ; un chunk trop grand noie l'information utile. Leur méthode Mix-of-Granularity utilise un routeur entraîné pour choisir dynamiquement la granularité la plus adaptée à chaque requête. Les auteurs préparent plusieurs versions du corpus, chacune découpée différemment. L'extension MoG-Graph modélise en plus les documents comme des graphes pour relier des passages éloignés. Zhong et al. montrent que la granularité d'indexation est un choix de conception majeur, souvent sous-estimé. Leur article rappelle qu'un découpage unique ne convient pas aux corpus hétérogènes.

---

## Article 15

**Intitulé :** Metadata-Driven Retrieval-Augmented Generation for Financial Question Answering  
**Auteurs :** Michail Dadopoulos, Anestis Ladas, Stratos Moschidis, Ioannis Negkakis  
**Année / source :** 2025, arXiv  
**Lien :** https://arxiv.org/html/2510.24402

**Résumé personnel :**

Dadopoulos et ses collègues étudient les limites du RAG sur les rapports financiers longs et très structurés. Dans ces documents, l'information pertinente est souvent dispersée et difficile à retrouver avec une simple similarité textuelle. Leur architecture génère des métadonnées riches : résumés, entités, thèmes, clusters et paires question-réponse possibles. Ces éléments sont intégrés aux chunks avant la recherche et le reranking. Dadopoulos et al. montrent qu'un bon reranker est important, mais que l'enrichissement des métadonnées apporte souvent les gains les plus solides. Leurs expériences sur FinanceBench confirment l'intérêt de cette approche. L'article rappelle que l'indexation intelligente concerne aussi les informations qui entourent le texte brut.

---

## Point de synthèse — fin du Jour 3

Les cinq articles du Jour 3 insistent sur la qualité de l'ingestion et de l'indexation. Pérez et Vizcaino rappellent l'importance d'une bonne extraction ; Faysse et al. ainsi que Yu et al. proposent des approches visuelles ; Zhong et al. travaillent sur la taille des segments ; Dadopoulos et al. montrent l'utilité des métadonnées enrichies.
