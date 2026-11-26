# Script oral — Démo convaincante + État de l’art

**Prototype :** DocuSearch (cas ISGO — Documentation & Archives)  
**Durée démo :** 1 min 30 à 2 min max  
**Durée état de l’art :** ~1 min (version courte 30 s si retard)

Complète `NOTES_ORATEUR_PROJET_TUTORE.md`.  
Révision approfondie : `FICHE_MAITRISE_THEME.md`.

---

## A. Avant d’entrer dans la salle (checklist)

### À faire (ordre)

1. Allumer le PC, brancher le vidéoprojecteur, vérifier que l’écran est lisible.
2. Lancer le backend (port **8010**) puis le frontend (port **5173**), ou Full Stack F5.
3. Vérifier le **badge API vert** dans la sidebar.
4. Confirmer qu’il y a déjà des documents indexés (idéalement ~40 docs ISGO).
  Si la liste est vide : cliquer **Indexer le dossier** une fois, attendre la fin, puis continuer.
5. Tester une fois hors jury : requête **formation** en mode **Hybride** → résultats + ouverture d’une fiche.
6. Ouvrir l’app en plein écran, zoom navigateur ~110 % si besoin.
7. Avoir un **plan B** : captures d’écran (accueil, résultats, fiche document) sur le Bureau.



### À ne pas faire

- Ne pas indexer en live pour la première fois devant le jury (trop long / risque d’erreur).
- Ne pas chercher une requête jamais testée.
- Ne pas parler en tapant trop vite : une action = une phrase.

---



## B. Script de démonstration (quoi faire + quoi dire)



### Phrase d’entrée (10 s)

> « Je vais maintenant montrer DocuSearch sur un cas concret : la **Direction de la Documentation et des Archives de l’ISGO**, à Ouagadougou. L’idée : un portail local qui indexe des PDF, Word, CSV et textes, puis permet une recherche intelligente. »

*(Pointer brièvement la bannière « Cas de démonstration ».)*

---



### Étape 1 — Confiance technique (10 s)


| Faire                                                            | Dire                                                                                 |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Montrer la sidebar : logo, badge API vert, compteur de documents | « L’API est en ligne. Les documents administratifs sont déjà indexés côté serveur. » |


**Message implicite :** le système marche, ce n’est pas une maquette.

---



### Étape 2 — Recherche métier (35–40 s)


| Faire                                                | Dire                                                                                         |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Cliquer le chip **formation** (ou taper `formation`) | « Première requête métier : retrouver tout ce qui concerne la **formation**. »               |
| Sélectionner le mode **Hybride**                     | « Je lance en mode **hybride** : ça combine mots-clés exacts et similarité sémantique. »     |
| Cliquer **Rechercher**                               | « On obtient une liste classée par pertinence, avec aperçu et mise en évidence des termes. » |
| Survoler 1–2 cartes (PDF / DOCX si visibles)         | « Formats hétérogènes : PDF, Word, etc. — une seule interface. »                             |


**Phrase clé (mémoriser) :**  

> « L’utilisateur ne cherche plus fichier par fichier : il pose une question métier, le système retrouve les documents pertinents. »

---



### Étape 3 — Comparer les modes (25–30 s) — optionnel si le temps presse


| Faire                              | Dire                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| Passer en **Mots-clés**, relancer  | « En mots-clés, on privilégie la correspondance exacte des termes. »                               |
| Passer en **Sémantique**, relancer | « En sémantique, on rapproche le sens, même si le mot exact n’est pas dans le titre. »             |
| Revenir en **Hybride**             | « L’hybride est mon choix par défaut pour la démo : le meilleur des deux mondes, sans GPU lourd. » |


Si tu as peu de temps : **saute cette étape**, garde uniquement l’hybride.

---



### Étape 4 — Fiche document (25–30 s)


| Faire                                        | Dire                                                                                                                                                      |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ouvrir un résultat pertinent                 | « J’ouvre un document. »                                                                                                                                  |
| Pointer résumé / tags / entités (selon l’UI) | « En plus du texte indexé, le système enrichit : **résumé**, **tags**, éventuellement des **entités**. Ça aide à décider vite si le document est utile. » |
| Fermer la fiche                              | « Donc : ingestion multi-formats, enrichissement, puis recherche intelligente — le pipeline complet en local. »                                           |


---



### Phrase de sortie (10 s)

> « En moins de deux minutes, on voit qu’une indexation intelligente n’est pas réservée aux grands data centers : elle est démontrable ici, sur un cas institutionnel réel. »

Puis : retour aux slides **Limites / perspectives**.

---



## C. Variantes de requêtes (si on te demande un 2ᵉ essai)


| Requête               | Ce que tu montres          | Phrase                                      |
| --------------------- | -------------------------- | ------------------------------------------- |
| `budget documentaire` | Doc financier / budget     | « Recherche administrative précise. »       |
| `partenariat ONG`     | Conventions / partenariats | « Retrouver un dossier transversal. »       |
| `stage informatique`  | RH / stages                | « Cas fréquent en école. »                  |
| `Fatou Sanou`         | Personne / agent           | « Recherche nominative dans les archives. » |


---



## D. Plan B si l’app plante

1. Respire. Dis calmement :
  > « Je bascule sur les captures préparées ; le parcours reste le même. »
2. Montrer : accueil → résultats « formation » → fiche document.
3. Terminer avec la même phrase de sortie.

Ne jamais s’excuser longuement.

---



## E. État de l’art — texte oral clarifié (~1 min)

### Structure mentale

1. Combien d’articles + 3 axes de lecture
2. Constat simple
3. Quatre idées qui ressortent (en mots faciles)
4. Ce qu’on garde pour DocuSearch

### Texte à dire (version corrigée et compréhensible)

> « Pour l’état de l’art, nous avons analysé **quinze articles** récents, de **2022 à 2026**.  
> Nous les avons organisés autour de **trois axes** : les **fondements**, l’**hybridation**, et le **pipeline RAG**.  
>  
> Le constat est simple : face à des documents de **formats différents**, un simple moteur de **mots-clés** ne suffit plus.  
>  
> De cette lecture, **quatre idées** se dégagent.  
>  
> **Premièrement**, on enrichit l’index : on ne stocke plus seulement des mots, mais aussi des informations utiles sur le document. Par exemple, Clarke parle d’un index annotatif.  
>  
> **Deuxièmement**, certains travaux vont plus loin : le modèle peut **retrouver un document** en générant directement son identifiant. C’est ce qu’on appelle la recherche générative, avec des approches comme DSI, NCI ou GenIR.  
>  
> **Troisièmement**, on **combine plusieurs moteurs** — mots exacts, sens du texte, relations entre informations — car une seule méthode n’est pas assez fiable.  
>  
> **Quatrièmement**, la qualité dépend de l’**amont** : bien lire les fichiers, les découper, les enrichir avec des métadonnées. Si cette étape est mauvaise, la recherche sera mauvaise.  
>  
> Pour notre contexte — local, avec des ressources limitées — nous retenons surtout trois points : **lire plusieurs formats**, **enrichir** les documents, et faire une **recherche hybride légère**.  
> C’est exactement ce sur quoi nous avons travaillé dans notre prototype DocuSearch. »

### Version ultra-courte (30 s) si tu es en retard

> « Quinze articles, 2022–2026, lus en trois axes : fondements, hybridation, pipeline.  
> Idée principale : les mots-clés seuls ne suffisent plus.  
> Il faut enrichir, combiner plusieurs recherches, et bien préparer les documents.  
> DocuSearch reprend ça de façon simple : multi-formats, enrichissement, recherche hybride. »

### Ce qu’il ne faut PAS faire à l’oral

- Lister les 15 titres d’articles.
- Dire des détails techniques inutiles (HNSW, docids, etc.) sauf question.
- Critiquer la littérature sans lien avec ton prototype.

### Une phrase « mastery » si le jury te coupe

> « L’indexation intelligente, ce n’est plus seulement stocker des mots : c’est un **pipeline** — extraire, enrichir, indexer, puis combiner plusieurs modes de recherche. »

---



## F. Enchaînement slide 8 → démo → slide 10

**Fin slide Réalisations :**  

> « Ingestion, enrichissement, trois modes de recherche. Je vais maintenant le montrer en live. »

*(Passer à l’écran navigateur.)*

**Retour après démo :**  

> « Voilà le prototype. Je termine par les limites et les perspectives. »

---



## G. Mini-checklist « convaincant »

- [ ] Tu nommes le **cas ISGO** (pas seulement « mon app »).
- [ ] Tu dis **hybride** et tu expliques en une phrase.
- [ ] Tu montres **formats différents** ou tu le dis explicitement.
- [ ] Tu ouvres **une fiche** (valeur ajoutée vs simple Google Desktop).
- [ ] Tu termines par **local / accessible / démontrable**.
- [ ] Tu as un plan B captures.