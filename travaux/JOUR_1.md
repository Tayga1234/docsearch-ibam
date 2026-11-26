# Bilan du Jour 1

**Nombre d'articles lus :** 5  
**Orientation :** fondements de l'indexation, données semi-structurées et recherche générative

---

## Article 1

**Intitulé :** Annotative Indexing  
**Auteurs :** Charles L. A. Clarke  
**Année / source :** 2024, arXiv / University of Waterloo  
**Lien :** https://arxiv.org/html/2411.06256

**Résumé personnel :**

Clarke observe que les collections documentaires actuelles combinent texte, JSON, CSV, HTML et PDF, alors qu'aucun outil unique ne permet de les stocker, transformer et rechercher ensemble. Il propose l'indexation annotative : le contenu est placé dans un espace d'adresses, puis enrichi d'annotations comme la segmentation, les entités, les scores de pertinence ou les vecteurs denses. Selon Clarke, ce cadre unifie l'index inversé, les magasins de colonnes, les bases orientées objet et les graphes de connaissances. Il montre aussi qu'un tel index peut évoluer dynamiquement et supporter des transactions. Clarke présente une implémentation de référence et discute de l'intégration possible avec des modèles de langage. Pour le lecteur, l'apport principal est une vision unificatrice de l'indexation, au-delà du simple moteur de recherche par mots-clés.

---

## Article 2

**Intitulé :** Data Discovery and Indexing for Semi-Structured Scientific Data  
**Auteurs :** Kaushik Jagini, Yifan Zhang, Jeff Heflin et al.  
**Année / source :** 2024, SCIEPRESS (DATA 2024)  
**Lien :** https://www.scitepress.org/Papers/2024/127060/

**Résumé personnel :**

Heflin et ses collaborateurs étudient la difficulté de retrouver des données scientifiques stockées en JSON lorsque leur structure varie d'un fichier à l'autre. Les chercheurs ignorent souvent les clés et l'organisation interne des jeux de données partagés. Pour répondre à ce problème, les auteurs étendent l'indexation cell-centric : chaque valeur ou paire clé-valeur devient une unité indexable. Leur système s'appuie sur Elasticsearch et une interface de recherche sans schéma prédéfini. Le cas d'usage en science des matériaux montre que l'on peut découvrir des données pertinentes sans connaître à l'avance leur format exact. Heflin et al. insistent aussi sur l'importance des principes FAIR et sur le rôle d'une interface claire pour favoriser la réutilisation des données.

---

## Article 3

**Intitulé :** Transformer Memory as a Differentiable Search Index  
**Auteurs :** Yi Tay, Vinh Q. Tran, Donald Metzler et al. (Google Research)  
**Année / source :** 2022, NeurIPS  
**Lien :** https://proceedings.neurips.cc/paper_files/paper/2022/file/892840a6123b5ec99ebaab8be1530fba-Paper-Conference.pdf

**Résumé personnel :**

Tay et son équipe introduisent le Differentiable Search Index, qui remplace l'index externe classique par la mémoire d'un modèle Transformer. Le principe est de transformer la recherche en tâche de génération : à partir d'une requête, le modèle produit directement l'identifiant du document pertinent. Les auteurs étudient plusieurs façons de représenter les documents et leurs identifiants, ainsi que différentes stratégies d'entraînement. Leurs expériences montrent que DSI peut surpasser des méthodes fortes comme les encodeurs duaux. L'article marque une rupture importante : l'index n'est plus seulement une structure intermédiaire, il peut devenir une fonction apprise par le modèle. Tay et al. ouvrent ainsi la voie à la recherche générative.

---

## Article 4

**Intitulé :** A Neural Corpus Indexer for Document Retrieval  
**Auteurs :** Ziqi Wang, Houxing Ren et al.  
**Année / source :** 2022, NeurIPS  
**Lien :** https://papers.neurips.cc/paper_files/paper/2022/file/a46156bd3579c3b268108ea6aca71d13-Paper-Conference.pdf

**Résumé personnel :**

Wang et al. proposent le Neural Corpus Indexer, un modèle séquence-à-séquence qui associe directement une requête à l'identifiant sémantique du document recherché. Leur critique des systèmes classiques est claire : l'index est construit séparément du modèle de ranking, ce qui empêche d'optimiser finement la récupération. NCI fusionne donc indexation et entraînement dans un même réseau. Les auteurs introduisent un décodeur spécialisé, des identifiants sémantiques et des techniques d'apprentissage complémentaires pour améliorer le rappel. Les résultats sur NQ320k et TriviaQA montrent des gains importants par rapport à l'état de l'art. Wang et al. démontrent qu'une meilleure représentation des documents dans l'index peut être aussi décisive que l'algorithme de recherche lui-même.

---

## Article 5

**Intitulé :** From Matching to Generation: A Survey on Generative Information Retrieval  
**Auteurs :** Yubao Zhang, Jiaxin Mao, et al.  
**Année / source :** 2024, arXiv  
**Lien :** https://arxiv.org/html/2404.14851

**Résumé personnel :**

Zhang et ses coauteurs proposent une synthèse du passage de la recherche par correspondance à la recherche générative. Les méthodes traditionnelles comparent une requête à des documents indexés et renvoient une liste ordonnée. La Generative Information Retrieval va plus loin en faisant produire au modèle des identifiants de documents ou des réponses fondées sur des preuves. Zhang et al. distinguent la récupération générative de documents et la génération fiable de réponses avec citations. Le survey couvre l'entraînement des modèles, les identifiants documentaires, l'apprentissage incrémental et le multimodal. Les auteurs rappellent aussi les limites actuelles : coût, mise à jour du corpus et passage à l'échelle. Pour le lecteur, cet article sert de carte d'ensemble pour situer les travaux récents du domaine.

---

## Point de synthèse — fin du Jour 1

Les cinq articles du Jour 1 montrent que l'indexation doit s'adapter à des données de plus en plus variées. Clarke et Heflin proposent des structures d'indexation plus flexibles ; Tay et Wang explorent des index appris par réseaux de neurones ; Zhang et al. en dressent la synthèse générale.
