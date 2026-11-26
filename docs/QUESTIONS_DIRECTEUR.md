# Questions au directeur de mémoire

## Ouverture — thème et solution

À dire en premier, avant les questions.

**Thème.** Indexation intelligente de données pour la recherche d’information.

**Constat.** Dans une petite organisation, les documents existent (PDF, Word, tableaux, textes), mais l’accès est mauvais. Beaucoup d’outils proposent une barre de recherche sans construire d’index : ils parcourent les fichiers au moment de la requête. Les moteurs industriels (Elasticsearch, Solr) sont trop lourds pour ce cadre.

**Problématique.** Comment concevoir un système local de recherche d’information fondé sur une indexation intelligente, alors que beaucoup d’outils « recherchent » sans vraiment indexer le contenu ?

**Solution : DocSearch.** Un portail web local. On ingère PDF, DOCX, CSV et TXT ; on extrait le texte ; on enrichit le document (tags, résumé extractif, entités) ; on le stocke (fichier original + SQLite + index Whoosh) ; on recherche en mots-clés, en similarité TF-IDF, ou en hybride (0,6 / 0,4). Deux profils : lecteur et administrateur. Pas de GPU, pas de cluster, pas de grand modèle de langage.

**Ce que le mémoire défend.** L’intelligence n’est pas un chatbot. C’est ce qu’on prépare **avant** la requête : extraire, enrichir, indexer, puis combiner deux signaux de pertinence.

**Phrase d’ouverture.** *« Mon mémoire porte sur l’indexation intelligente pour la recherche d’information. Beaucoup d’outils cherchent sans index. J’ai conçu DocSearch, un prototype local qui extrait, enrichit, indexe, puis recherche. Je voudrais aussi votre avis sur l’ergonomie du rapport : est-il lisible pour un jury, ou trop chargé ? »*

---

## 1. Méthode d’analyse des exigences

**Question.** Concernant la méthode d’analyse des exigences et des besoins, je suis parti sur une approche basée sur mon pipeline, ma ligne de logique métier. Est-ce correct, ou devais-je forcément aller sur une base de méthode d’analyse comme MERISE ou UML ?

**Réponse.** Oui : **la démarche est correcte**. Tu n’étais **pas obligé** de partir de MERISE, ni d’appliquer UML comme *méthode complète*.

Tu n’as pas « sauté » l’analyse des besoins. Tu l’as faite **à partir du traitement**, ce qui colle au sujet : le problème n’est pas de gérer des dossiers étudiants ou un budget, c’est de **transformer un fichier en document recherchable**.

---

## Pourquoi le pipeline est une vraie méthode d’analyse ici

Une exigence, chez toi, naît d’une étape du métier :

- extraire → EF3
- enrichir → EF4
- persister / indexer → EF5, EF6
- rechercher → EF7, EF8, EF12
- administrer l’index → EF1, EF2, EF10

Plus les acteurs (lecteur / administrateur), les ENF, le hors-périmètre. C’est une analyse **orientée processus**, légitime en ingénierie des SI, surtout pour un moteur d’indexation.

MERISE (MCD, MCT, MLD) sert surtout un SI de gestion : entités, règles de gestion, circulation de documents administratifs. L’appliquer ici t’aurait poussé vers un modèle « Document / Utilisateur / Service » sans expliquer **l’indexation intelligente**, qui est le cœur du mémoire.

UML n’est pas une méthode obligatoire : c’est un **langage**. Tu l’as déjà utilisé là où il sert : diagramme de cas d’utilisation (paquets, `include`, `extend`, généralisation). Tu n’avais pas à en faire un cycle en V UML (classes, séquences, états, déploiement) pour que l’analyse soit valable.

---

## Comment le dire au directeur

*« Je n’ai pas écarté l’analyse des besoins. Je n’ai pas pris MERISE, parce que l’objet n’est pas un SI de gestion, c’est un pipeline d’indexation. Les exigences sont dérivées des étapes métier (extraction, enrichissement, index, recherche) et des deux acteurs. UML est utilisé pour les cas d’utilisation, pas comme méthode unique de conception. »*

---

## Le seul point à assumer, pas à cacher

Tu as **fusionné** analyse des besoins et conception du pipeline (chapitre 2 : exigences + architecture). Certains jurys ISIE, formés à MERISE, attendront le mot « méthode ». Dans le texte, tu parles déjà d’approche expérimentale appliquée. Si le directeur insiste, tu peux **nommer** ta démarche, sans tout réécrire, par exemple :

**analyse des besoins guidée par le processus d’indexation** (acteurs, EF/ENF, cas d’utilisation UML, puis architecture en couches).

Ce n’est pas un aveu de faiblesse. C’est préciser que tu as choisi une méthode **adaptée à l’objet**, pas une méthode par habitude de cours.

**En une phrase.** MERISE n’était pas obligatoire ; UML non plus comme méthode ; ta ligne métier est la bonne base, à condition de la présenter comme un choix assumé, pas comme un oubli.

---

## 2. Comment les fichiers et les données sont-ils stockés dans la plateforme ?

**Question.** Comment mes fichiers et mes données sont-ils stockés dans ma plateforme ?

**Réponse.** DocSearch ne met **pas tout au même endroit**. Trois couches locales se complètent. C’est un choix de prototype, pas un entrepôt unique.

### Les trois lieux de stockage

| Couche | Emplacement | Ce qu’on y met | Rôle |
|--------|-------------|----------------|------|
| Fichiers originaux | `data/raw/` | PDF, DOCX, CSV, TXT tels quels | Source de vérité du document |
| Métadonnées et texte | `data/db/documents.db` (SQLite) | Titre, contenu extractible, tags, résumé, entités, empreinte, chemin | Fiche document, enrichissement |
| Index de recherche | `data/db/whoosh_index/` | Identifiant, titre, contenu, type, tags | Recherche lexicale (Whoosh / BM25) |

Un téléversement copie le fichier dans `data/raw/`, puis déclenche le même pipeline qu’un scan. Rien n’est envoyé dans le cloud.

### Ce que contient SQLite (table `documents`)

Chaque ligne = un document indexé :

- `id`, `title`, `content` (texte extrait) ;
- `source_path` (chemin unique vers le fichier dans `data/raw/`) ;
- `file_type`, `mime_type`, `size_bytes` ;
- `created_at`, `indexed_at` ;
- `summary`, `tags` ;
- `metadata` (JSON) : empreinte SHA-256, date de modification, entités, catégorie, détails d’extraction.

Le fichier binaire **n’est pas** dans la base. SQLite pointe vers lui via `source_path`.

### Ce que Whoosh indexe

Pas le PDF brut : le **texte déjà extrait et enrichi**. Schéma : `id`, `title` (poids 2,5), `content`, `file_type`, `tags` (scorables). La recherche lexicale lit cet index, pas le dossier `data/raw/`.

### Ce qui n’est pas persisté sur disque

La matrice TF-IDF (mode « sémantique ») est un **cache mémoire**. Elle est reconstruite à partir de SQLite (titre + tags + contenu) et invalidée à chaque indexation, suppression ou reconstruction.

### Cohérence à la suppression

Supprimer un document retire **les trois** : le fichier dans `data/raw/`, la ligne SQLite, l’entrée Whoosh. Sinon la recherche montrerait une fiche dont le fichier n’existe plus.

### Phrase à dire au directeur

*« Je ne stocke pas tout dans une seule base. Le fichier original reste dans un dossier local. SQLite garde le texte extractible et l’enrichissement. Whoosh garde l’index inversé pour la recherche. Les trois sont liés par l’identifiant et le chemin source. En production, le dossier deviendrait un NAS ou MinIO, et SQLite deviendrait PostgreSQL ; l’architecture à trois couches resterait la même. »*

### Le point à assumer

C’est du **stockage local de prototype** (fichiers + SQLite + index fichier), pas un SI documentaire d’établissement (pas de versions, pas de GED, pas de droits par pièce). Tu l’as déjà écrit au chapitre 4.7. Si le directeur demande « où est la base ? », la réponse n’est pas « SQLite seulement » : c’est **fichier + fiche + index**.

---

## 3. Puis-je appeler « sémantique » un classement TF-IDF, et « intelligente » un enrichissement sans LLM ?

**Question.** Dans l’interface et le mémoire, j’ai un mode « sémantique » qui est en réalité du TF-IDF et une similarité cosinus. L’enrichissement (tags, résumé, entités) se fait par règles, sans grand modèle de langage. Est-ce défendable devant un jury, ou dois-je renommer le mode et affaiblir le mot « intelligent » ?

**Réponse.** C’est **le point le plus risqué à l’oral**. Il faut l’assumer, pas le cacher. Le choix technique est cohérent pour un prototype local sans GPU. Le vocabulaire, lui, peut prêter à confusion.

### Ce qui est vrai

- Le TF-IDF rapproche des documents qui partagent un **vocabulaire** (unigrammes et bigrammes), même si la requête n’est pas une occurrence exacte. Ce n’est pas du Ctrl+F.
- L’enrichissement pèse vraiment : les tags sont surpondérés dans Whoosh (× 1,8). Un document « mieux annoté » remonte davantage.
- L’intelligence, dans le mémoire, est définie comme **ce qu’on prépare avant la requête**, pas comme une génération de texte.

### Ce qu’un jury peut reprocher

- Depuis 2018, « sémantique » évoque BERT, embeddings, e5, pas Salton 1988.
- « Indexation intelligente » évoque parfois un LLM ou un RAG. Toi tu as volontairement écarté les deux.

### Ce que tu peux proposer

Deux options, à lui faire choisir :

1. **Garder « sémantique »** dans l’interface, mais le qualifier partout dans le texte : *sémantique légère / similarité de vocabulaire TF-IDF*. C’est déjà le fond du chapitre 3.7.
2. **Renommer le mode** en « similarité » ou « vocabulaire », et réserver « sémantique » aux perspectives (embeddings e5-small, tableau 4.7).

**Question au directeur.** *« Est-ce que je garde le mot “sémantique” pour le mode TF-IDF, en le qualifiant, ou je le renomme pour éviter l’ambiguïté à la soutenance ? »*

**Phrase à dire.** *« Je n’ai pas de modèle de langue. Mon mode sémantique, c’est du TF-IDF plus cosinus. Mon enrichissement est déterministe. Je l’assume pour un prototype local. La question est seulement : est-ce que le vocabulaire du mémoire et de l’interface reste acceptable ? »*

---

## 4. Mon évaluation (temps, tests) suffit-elle sans précision ni rappel ?

**Question.** J’évalue DocSearch par la couverture fonctionnelle, le temps d’indexation (1 110 documents en 25,74 s), la latence de recherche (< 500 ms) et des tests manuels. Je n’ai pas de collection annotée, donc pas de précision, de rappel ni de MRR. Pour un Master ISIE, est-ce suffisant, ou dois-je ajouter une mini-évaluation de pertinence à la main ?

**Réponse.** Pour un mémoire **ISIE** (ingénierie des SI), une évaluation de **faisabilité** est défendable : le livrable est un système qui marche, explicable, dans un cadre à ressources limitées. Ce n’est pas une thèse de RI expérimentale type TREC.

### Ce que tu as déjà, et qui compte

- le pipeline tourne de bout en bout (formats, enrichissement, trois modes) ;
- des ordres de grandeur mesurés (indexation, recherche) ;
- des tests automatisés et une grille manuelle cochée ;
- les limites sont écrites (corpus petit, TF-IDF ≠ sens, pas d’OCR).

### Ce qui manque, scientifiquement

Sans jugements de pertinence (requête → documents attendus), tu **ne peux pas prouver** H2 (« l’hybride est plus exploitable que le lexical seul »). Tu la **montres** (comparaison des trois modes, extraits, tags), tu ne la **mesures** pas.

### Ce que tu peux proposer, si le directeur insiste

Un protocole léger, sans relancer tout le prototype :

- 8 à 10 requêtes métier (`budget`, `formation`, `archivage`, `IBAM`…) ;
- pour chacune, noter à la main si le 1er / les 3 premiers résultats sont pertinents (oui / non / partiel) ;
- comparer les trois modes sur ces requêtes.

Cela donne un Precision@3 artisanal, honnête, et protège H2 à l’oral. Ce n’est pas obligatoire si lui dit que la faisabilité suffit.

**Question au directeur.** *« Est-ce que l’évaluation de faisabilité (fonctionnel + temps + tests) clôt le chapitre 4, ou dois-je ajouter une petite grille de pertinence à la main pour étayer l’hypothèse H2 ? »*

**Phrase à dire.** *« Je n’ai pas fait une campagne TREC. J’ai montré que le système indexe et répond vite, et que l’enrichissement est visible. Si vous jugez que H2 exige une preuve de pertinence, je peux noter une dizaine de requêtes à la main. Sinon je fige le chapitre 4 tel quel. »*

---

## 5. Ergonomie du rapport

Ces questions portent sur le **mémoire Word**, pas sur l’interface DocSearch. Objectif : un jury qui feuillette 10 minutes doit retrouver le fil (problématique → pipeline → preuve) sans se perdre dans les annexes et les cadres vides.

**Phrase d’entrée.** *« Sur le fond je me suis fixé. Je voudrais maintenant votre lecture d’ergonomie : est-ce que le document se parcourt bien, ou est-ce trop dense, trop d’annexes, trop de cadres à coller ? »*

### 5.1. Le fil de lecture est-il assez visible ?

**Question.** Un lecteur qui n’ouvre que les figures 1, 2, 3 et 4 + le tableau des exigences, a-t-il compris le mémoire ? Ou le chapitre 1 (état de l’art) et les annexes I–J alourdissent-ils trop le parcours ?

**Réponse.** Le canevas IBAM (intro, 4 chapitres, conclusion, biblio, annexes) est respecté. Le risque n’est pas l’ordre, c’est la **charge** : beaucoup de tableaux, un chapitre 1 dense, puis deux annexes techniques longues. Les quatre diagrammes portent déjà l’essentiel. Si le directeur trouve le document lourd, on raccourcit l’état de l’art ou on laisse le code en annexe J **sur clé / dépôt**, pas imprimé in extenso.

**À lui demander.** *« Est-ce que le fil “besoins → pipeline → résultats” se lit clairement, ou faut-il alléger le chapitre 1 et les annexes pour l’oral ? »*

### 5.2. Cadres vides et planches : ça aide ou ça gêne ?

**Question.** Les figures 5 à 19 et les planches A à P sont encore des cadres « à coller ». Pour un directeur qui relit maintenant, ces pages blanches rendent-elles le rapport illisible ? Dois-je coller les captures avant la prochaine relecture, ou puis-je les laisser en attente ?

**Réponse.** Pour **toi**, les cadres réservent la pagination. Pour **lui**, un document plein de rectangles vides a l’air inachevé et casse la lecture (surtout aux chapitres 3 et 4, au milieu du propos). Ergonomiquement, mieux vaut **coller d’abord les captures essentielles** (connexion, recherche, fiche, un Swagger, pytest) et retirer ou regrouper le reste en une seule annexe « captures ».

**À lui demander.** *« Préférez-vous relire une version avec les captures déjà collées, quitte à ce qu’il y en ait moins, plutôt qu’un mémoire avec une vingtaine de cadres vides ? »*

### 5.3. Algorithmes (annexe I) et code (annexe J) : les deux à l’imprimé ?

**Question.** J’ai formalisé la logique en algorithmes (annexe I) et recopié les extraits Python (annexe J). Sur papier, le code en Consolas 9 pt est-il lisible et utile, ou l’annexe I suffit-elle au jury, le dépôt Git servant de preuve ?

**Réponse.** Pour un master ISIE, **l’annexe I est la plus ergonomique** : un jury la parcourt. L’annexe J rassure (« ce n’est pas du vent ») mais fatigue à l’impression (listings longs, peu de commentaires). Compromis possible : garder J.1 à J.6 en extraits courts, ou déplacer J en « code source consultable » et ne laisser qu’un listing par couche.

**À lui demander.** *« Gardez-vous les deux annexes dans le volume imprimé, ou l’annexe algorithmes suffit-elle, avec le code sur le dépôt ? »*

### 5.4. Diagramme de cas d’utilisation : assez clair, ou trop chargé ?

**Question.** La figure 4 (paquets UML, `include`, `extend`, généralisation) est voulue « niveau master ». À l’impression, reste-t-elle lisible, ou dois-je la simplifier / la scinder en deux schémas (consultation / administration) ?

**Réponse.** Un schéma unique riche est pédagogique **si** on peut le lire A4. S’il devient illisible (petites ellipses, traits qui se croisent), l’ergonomie perd face à l’ambition UML. Le directeur tranche : un diagramme dense mais unique, ou deux figures plus aérées.

**À lui demander.** *« Sur papier, la figure 4 se lit-elle d’un coup d’œil, ou je la sépare en deux paquets, chacun sur une figure ? »*

### Phrase de clôture sur l’ergonomie

*« Je ne vous demande pas une relecture orthographique. Je vous demande si le document se navigue : fil visible, captures au bon endroit, annexes utiles sans noyer le lecteur. Si quelque chose casse la lecture, je le corrige en priorité. »*
