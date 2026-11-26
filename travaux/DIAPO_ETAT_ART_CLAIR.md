# Diapo État de l’art — version enrichie et compréhensible

## Avant (trop technique)

Trois colonnes : Fondements / Hybridation / Pipeline RAG  
Beaucoup d’acronymes (DSI, NCI, ASI, GLEN, ACORN, ColPali…) sans explication.

## Après (à mettre sur la diapo)

**Titre :** 3. État de l’art (2022–2026)

**Sous-titre :**  
15 articles (2022–2026) · 3 idées clés · lien direct avec DocuSearch

| 1. Mieux indexer | 2. Combiner les moteurs | 3. Soigner l’amont |
|------------------|-------------------------|---------------------|
| On n’indexe plus seulement des mots | Un seul moteur ne suffit plus | Bien extraire le contenu des fichiers |
| Formats très variés (texte, JSON…) | Mots-clés + sens + structure | Découper les documents (chunks) |
| Nouveaux index « appris » (GenIR) | Chaque requête a un signal utile | Ajouter tags / métadonnées |
| Ex. : Clarke, DSI, NCI | Ex. : HetaRAG, recherche hybride | Ex. : ingestion, OCR, enrichissement |
| **→ L’index devient plus intelligent** | **→ Combiner plusieurs pertinences** | **→ La qualité amont conditionne tout** |

## Phrase de bas de slide (optionnelle, si tu as la place)

**Pour DocuSearch :** recherche hybride + enrichissement (tags, résumé) — version locale, sans GPU.

## Ce que tu dis à l’oral (≈ 50 s)

> « J’ai analysé quinze articles récents. Trois idées ressortent.  
> Premièrement, l’index n’est plus une simple table de mots : il devient plus riche, parfois même appris par un modèle.  
> Deuxièmement, on combine plusieurs moteurs : mots-clés, sens, structure — car un seul signal ne suffit pas.  
> Troisièmement, tout dépend de l’amont : bien extraire, découper et enrichir les documents.  
> DocuSearch reprend ces deux derniers points de façon réaliste : **hybride** et **enrichissement**, en local. »

Fichier PowerPoint mis à jour : `PRESENTATION_KOROGO_W_Ange_Gaetan_AVEC_DEMO_NOTES.pptx` (slide 5).
