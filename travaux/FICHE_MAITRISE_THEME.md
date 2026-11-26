# Fiche de maîtrise du thème

**Thème :** Indexation intelligente de données hétérogènes pour la recherche d’information  
**Prototype :** DocuSearch  
**Objectif :** réviser definitions, sigles et réponses types avant les questions du jury

Lis aussi : `SCRIPT_DEMO_ET_ETAT_ART.md` (oral démo + état de l’art).

---

## 1. En une phrase (à savoir par cœur)

> DocuSearch est un portail **local** qui **ingère** des documents de formats différents (PDF, DOCX, CSV, TXT), les **enrichit** (résumé, tags, entités), les **indexe**, puis permet une **recherche** par mots-clés, sémantique ou hybride.

**Problématique :**  
> Comment concevoir un système local capable d’indexer automatiquement des données hétérogènes et d’offrir une recherche d’information pertinente ?

---

## 2. Définitions essentielles

| Terme | Définition  |
|-------|-------------------------------------|
| **Recherche d’information (RI / IR)** | Discipline qui vise à retrouver, dans une collection, les documents pertinents pour une requête utilisateur. |
| **Indexation** | Opération qui transforme des documents en une structure (index) permettant de les retrouver rapidement. |
| **Index intelligent** | Index qui ne se limite pas aux mots bruts : il peut intégrer sens, structure, annotations, métadonnées, parfois des représentations apprises. |
| **Données hétérogènes** | Données de natures/formats différents (texte, tableaux, PDF scannés ou natifs, JSON, etc.) dans une même collection. |
| **Index inversé** | Structure classique : pour chaque terme, la liste des documents (et positions) où il apparaît. Base des moteurs mots-clés. |
| **Pertinence** | Mesure de l’adéquation entre un document et le besoin exprimé par la requête. |
| **Ingestion** | Étape amont : découverte des fichiers, extraction du texte/structure, nettoyage, préparation avant indexation. |
| **Extraction** | Récupération du contenu utile depuis un format (ex. texte d’un PDF ou d’un DOCX). |
| **Enrichissement** | Ajout d’informations dérivées : résumé, tags, entités nommées, métadonnées. |
| **Métadonnées** | Données sur les données : titre, auteur, date, type de fichier, tags, etc. |
| **Chunking / segmentation** | Découpage d’un long document en segments indexables (taille et stratégie influencent la qualité). |
| **TF-IDF** | Pondération classique : un terme est important s’il est fréquent dans un document (**TF**) mais rare dans le corpus (**IDF**). |
| **Recherche mots-clés (plein texte)** | Correspondance sur les termes exacts (ou proches) via un index lexical / inversé. |
| **Recherche sémantique** | Recherche basée sur le **sens** (similarité de représentations), pas seulement sur les mots exacts. |
| **Recherche hybride** | Combinaison de plusieurs signaux (ex. mots-clés + sémantique) pour classer les résultats. |
| **Embedding / vecteur** | Représentation numérique d’un texte dans un espace où des contenus proches en sens sont proches géométriquement. |
| **Similarité cosinus** | Mesure d’angle entre deux vecteurs ; souvent utilisée pour comparer requête et documents. |
| **OCR** | Reconnaissance optique de caractères : transformer une image de texte (scan) en texte éditable. |
| **RAG** | Générer une réponse à partir de documents **retrouvés** (retrieval) puis **générés** par un modèle, en s’appuyant sur le contexte trouvé. |
| **GenIR** | Recherche d’information générative : le modèle peut générer directement des identifiants de documents (plutôt que seulement scorer une liste). |
| **DocID** | Identifiant de document ; en GenIR, parfois un identifiant **sémantique** appris, pas seulement un numéro technique. |
| **Pipeline** | Chaîne d’étapes ordonnées : ingestion → extraction → enrichissement → indexation → recherche. |
| **MVP** | Version minimale viable : prototype qui prouve le concept avec l’essentiel des fonctions. |
| **API** | Interface de programmation : le frontend appelle le backend via des endpoints HTTP. |

---

## 3. Sigles et acronymes (à connaître)

### Ton projet / stack

| Sigle | Signification | Rôle chez toi |
|-------|---------------|---------------|
| **ISGO** | (cas démo) Institut / structure du scénario Ouagadougou — Direction Documentation & Archives | Cas métier de la démo |
| **ISIE / ISI** | Master (Systèmes d’Information…) — selon l’intitulé exact de ta filière | Cadre académique |
| **API** | Application Programming Interface | FastAPI expose l’API DocuSearch |
| **HTTP** | HyperText Transfer Protocol | Communication client ↔ serveur |
| **REST** | Architectural style d’API via HTTP | Endpoints `/search`, `/ingest`, etc. |
| **JSON** | JavaScript Object Notation | Format d’échange API |
| **PDF** | Portable Document Format | Format document |
| **DOCX** | Document Word (Office Open XML) | Format document |
| **CSV** | Comma-Separated Values | Tableaux / exports |
| **TXT** | Fichier texte brut | Format simple |
| **UI** | User Interface | Interface React |
| **SPA** | Single Page Application | Frontend React/Vite |
| **SQLite** | Base SQL légère fichier | Métadonnées documents |
| **Whoosh** | Moteur de recherche plein texte Python | Index mots-clés |
| **TF-IDF** | Term Frequency – Inverse Document Frequency | Pondération / similarité sémantique légère |
| **CRUD** | Create Read Update Delete | Gestion documents (dont suppression) |

### État de l’art / littérature

| Sigle | Signification | Idée en une ligne |
|-------|---------------|-------------------|
| **IR** | Information Retrieval | Recherche d’information |
| **RI** | Recherche d’Information | Équivalent FR |
| **DSI** | Differentiable Search Index (Tay et al., 2022) | L’index est « dans » le modèle Transformer |
| **NCI** | Neural Corpus Indexer (Wang et al., 2022) | Associe requête → identifiant sémantique |
| **GenIR** | Generative Information Retrieval | RI où la génération joue un rôle central |
| **ASI** | Auto Search Indexer (Yang et al., 2023) | Apprend des docids, y compris pour nouveaux docs |
| **GLEN** | (Lee et al., 2023) index lexical appris | Docids plus interprétables |
| **RAG** | Retrieval-Augmented Generation | Retrouver puis générer une réponse |
| **HetaRAG** | Approche RAG hétérogène multi-index (2025) | Combiner plusieurs types d’index |
| **HNSW** | Hierarchical Navigable Small World | Index approximatif de voisins (vecteurs) |
| **ACORN** | Extension hybride autour de HNSW (Gollapudi et al.) | Vecteurs + contraintes structurées |
| **ColPali** | Modèle vision-langage pour pages (Faysse et al.) | Indexer la page comme image |
| **VisRAG** | RAG basé vision (Yu et al.) | Pipeline RAG multimodal |
| **MoG** | Mix-of-Granularity (Zhong et al.) | Adapter la taille des segments |
| **LLM** | Large Language Model | Grand modèle de langage |
| **VLM** | Vision-Language Model | Modèle vision + langage |
| **NLP** | Natural Language Processing | Traitement automatique du langage |
| **NER** | Named Entity Recognition | Extraction d’entités nommées |
| **BM25** | Fonction de ranking lexical classique | Souvent opposée/complétée aux vecteurs |
| **ANN** | Approximate Nearest Neighbor | Recherche approximative de voisins |

Tu n’as pas besoin de réciter tous les sigles. Priorité : **IR, index inversé, TF-IDF, hybride, RAG, GenIR, DSI/NCI, OCR, embedding, métadonnées, Whoosh, FastAPI**.

---

## 4. Architecture DocuSearch (réponse type)

> « Le frontend **React** envoie des requêtes à une API **FastAPI**.  
> Le backend orchestre l’ingestion, l’extraction selon le type de fichier, l’enrichissement, puis stocke les métadonnées en **SQLite** et l’index lexical avec **Whoosh**.  
> Pour la partie sémantique légère, j’utilise une similarité de type **TF-IDF**.  
> La recherche peut être mots-clés, sémantique ou **hybride**. »

Pipeline à dessiner mentalement :

```
Fichiers (PDF/DOCX/CSV/TXT)
    → Extraction
    → Enrichissement (résumé, tags, entités)
    → Stockage métadonnées (SQLite) + index (Whoosh)
    → Recherche (mots-clés / sémantique / hybride)
    → Interface React
```

---

## 5. Lien littérature ↔ prototype (très important)

| Idée littérature | Choix DocuSearch |
|------------------|------------------|
| Données hétérogènes (Clarke, Heflin…) | Extracteurs multi-formats |
| Hybridation (HetaRAG, ACORN…) | Modes mots-clés + sémantique + hybride |
| Amont critique (Pérez, Dadopoulos…) | Ingestion + enrichissement métadonnées |
| GenIR / DSI / NCI | **Non repris tel quel** (coût, GPU, complexité) — cités comme état de l’art |
| Vision (ColPali, VisRAG) | Perspective (OCR / vision), pas le cœur du MVP |

Phrase type :  
> « Je m’inspire de l’état de l’art, mais je **transfère** ce qui est réaliste en local : hybridation légère et enrichissement, pas un index génératif lourd. »

---

## 6. Questions probables + réponses courtes

### Sur le thème

**Q. Pourquoi « intelligente » ?**  
R. Parce que l’indexation ne s’arrête pas aux mots : enrichissement (résumé, tags), et recherche qui peut aller au-delà de la correspondance exacte (sémantique / hybride).

**Q. Pourquoi données hétérogènes ?**  
R. Dans une organisation réelle, l’information est éclatée en PDF, Word, tableaux CSV, notes texte. Un seul format = cas trop simplifié.

**Q. En quoi c’est original ?**  
R. Pas inventer GenIR, mais **adapter** l’indexation intelligente à un contexte local / ressources limitées, avec un prototype démontrable.

### Sur les choix techniques

**Q. Pourquoi Whoosh et pas Elasticsearch ?**  
R. Whoosh est embarqué en Python, simple à déployer en local pour un MVP académique, sans cluster ni infra lourde.

**Q. Pourquoi TF-IDF et pas des embeddings BERT ?**  
R. TF-IDF reste interprétable, léger CPU, suffisant pour démontrer la sémantique relative. Les embeddings neuronaux sont une perspective.

**Q. Différence mots-clés / sémantique / hybride ?**  
R. Mots-clés = termes exacts (Whoosh). Sémantique = similarité de contenu (TF-IDF). Hybride = combinaison des deux scores.

**Q. Comment gérez-vous les doublons ?**  
R. Via empreinte / hash du fichier pour éviter de réindexer inutilement le même contenu (selon implémentation du scan).

### Sur l’évaluation

**Q. Comment évaluez-vous la qualité ?**  
R. Démonstration qualitative sur un corpus métier (ISGO), inspection des top résultats, comparaison des modes. Une évaluation IR complète (précision/rappel, nDCG) est une perspective.

**Q. Qu’est-ce que précision / rappel ?**  
R. Précision = parmi les docs renvoyés, quelle part est pertinente. Rappel = parmi tous les docs pertinents, quelle part a été retrouvée.

### Sur les limites (montre que tu es lucide)

**Q. Limites principales ?**  
R. Pas d’authentification multi-utilisateurs, volumes modestes, sémantique TF-IDF (pas embeddings profonds), peu d’OCR avancé, pas encore de module RAG conversationnel.

**Q. Et si le PDF est scanné ?**  
R. Sans OCR solide, l’extraction texte échoue ou est pauvre. C’est une limite connue ; OCR / vision sont en perspectives (littérature ColPali/VisRAG).

### Sur la littérature

**Q. Citez un article clé.**  
R. Tay et al. (2022) DSI — l’index différentiable ; ou Clarke (2024) index annotatif ; ou HetaRAG pour l’hybride. *(Prépare 2 noms.)*

**Q. GenIR vs votre système ?**  
R. GenIR génère des identifiants via un modèle entraîné. DocuSearch garde un index externe classique + scoring, plus robuste à mettre à jour et plus simple à déployer.

**Q. Qu’est-ce que le RAG ?**  
R. On récupère des passages pertinents, puis un modèle génère une réponse **ancrée** sur ces sources. DocuSearch fait aujourd’hui la partie retrieval ; le RAG est une suite logique.

---

## 7. Quatre familles d’approches (carte mentale)

1. **Enrichie / unifiée** — Clarke, Heflin  
2. **Apprise / GenIR** — Tay (DSI), Wang (NCI), Zhang, Yang (ASI), Lee (GLEN)  
3. **Hybride** — HetaRAG, ACORN, DiscoverPath  
4. **Amont** — ingestion (Pérez), vision (ColPali, VisRAG), granularité (MoG), métadonnées (Dadopoulos)

**Message unique :**  
> Extraire → structurer → enrichir → indexer → rechercher : une chaîne ; la qualité de chaque maillon compte.

---

## 8. Vocabulaire FR/EN utile

| Français | English |
|----------|---------|
| Recherche d’information | Information retrieval |
| Index inversé | Inverted index |
| Pertinence | Relevance |
| Requête | Query |
| Classement / ranking | Ranking |
| Corpus | Corpus / collection |
| Rappel | Recall |
| Précision | Precision |
| Découpage | Chunking |
| Mise à jour de l’index | Index update |

---

## 9. Plan de révision (2 heures)

| Temps | Action |
|------:|--------|
| 20 min | Relire section 1–4 de cette fiche à voix haute |
| 20 min | Apprendre le script état de l’art (`SCRIPT_DEMO_ET_ETAT_ART.md` § E) |
| 25 min | Répéter la démo chronométrée (1 min 30) |
| 20 min | S’entraîner aux questions § 6 (à voix haute) |
| 15 min | Relire limites + perspectives + 2 articles phares |
| 20 min | Refaire une fois démo + plan B captures |

---

## 10. Phrases de secours (si tu bloques)

- « Je reformule : … »
- « Dans mon prototype, concrètement, cela correspond à … »
- « La littérature propose X ; mon choix pragmatique est Y parce que … »
- « C’est une limite que j’assume ; la perspective serait … »

---

*Dernière mise à jour : préparation soutenance DocuSearch / projet tutoré.*
