# Scénarios de tests manuels — DocSearch

**Projet :** Indexation intelligente de données pour la recherche d’information  
**Périmètre :** Interface web (frontend) + intégration API  
**URL interface :** [http://localhost:5173](http://localhost:5173)  
**URL API (Swagger) :** [http://localhost:8010/docs](http://localhost:8010/docs)  

---

## Prérequis

- [x] Backend lancé (port 8010)
- [x] Frontend lancé (port 5173)
- [x] Corpus IBAM présent dans `data/raw/` (1 110 fichiers)
- [x] Version API affichée : **0.7.0**

**Lancement rapide :** Run & Debug → **Full Stack** (F5)

---

## 1. Tests d'affichage et connexion

| ID   | Scénario                         | Étapes                                              | Résultat attendu                                              | OK  |
| ---- | -------------------------------- | --------------------------------------------------- | ------------------------------------------------------------- | --- |
| T-01 | Chargement initial               | Ouvrir [http://localhost:5173](http://localhost:5173) | Espace public (recherche) sans connexion                      | [x] |
| T-02 | Consultation publique            | Rechercher / ouvrir Fonds sans compte               | Accès recherche et fonds, pas d’administration                | [x] |
| T-03 | Authentification administrateur  | Compte `admin` / `archives`                         | Menu Documents et Indexation visibles                         | [x] |
| T-04 | API hors ligne                   | Arrêter le backend, rafraîchir                      | Message d’erreur clair, interface encore lisible              | [x] |
| T-05 | Responsive                       | Réduire la fenêtre                                  | Barre de recherche et cartes restent lisibles                 | [x] |

---

## 2. Tests d'ingestion (interface)

| ID   | Scénario             | Étapes                                      | Résultat attendu                                   | OK  |
| ---- | -------------------- | ------------------------------------------- | -------------------------------------------------- | --- |
| T-10 | Scan dossier         | Indexation → confirmer → indexer le dossier | Compteur porté à 1 110 documents                   | [x] |
| T-11 | Affichage après scan | Ouvrir Fonds / Documents                    | Liste paginée, types PDF, DOCX, CSV, TXT           | [x] |
| T-12 | Carte document       | Vérifier une carte du fonds                 | Titre, type, taille, tags, extrait visibles        | [x] |
| T-13 | Upload TXT           | Documents → ajouter un `.txt`               | Nouveau document dans la liste                     | [x] |
| T-14 | Upload refusé        | Importer un `.png`                          | Message d’erreur, pas d’ajout                      | [x] |
| T-15 | Garde-fou import     | Choisir des fichiers                        | Dialogue de confirmation avant l’envoi             | [x] |

---

## 3. Tests de recherche (interface)

| ID   | Scénario             | Étapes                                      | Résultat attendu                                   | OK  |
| ---- | -------------------- | ------------------------------------------- | -------------------------------------------------- | --- |
| T-20 | Recherche mots-clés  | Mode **Mots-clés**, requête `DocSearch`     | Document pertinent, terme surligné                 | [x] |
| T-21 | Recherche IBAM       | Mode **Mots-clés**, requête `IBAM`          | Pièces institutionnelles dans les résultats        | [x] |
| T-22 | Recherche budget     | Mode **Mots-clés**, requête `budget`        | Notes budgétaires / prévisionnel                   | [x] |
| T-23 | Recherche sémantique | Mode **Sémantique**, requête proche métier  | Classement par proximité de vocabulaire            | [x] |
| T-24 | Recherche hybride    | Mode **Hybride**, requête `indexation`      | Résultats avec score, comparaison des 3 modes      | [x] |
| T-25 | Aucun résultat       | Requête `xyz123introuvable`                 | Message « aucun résultat », pas de crash           | [x] |
| T-26 | Nouvelle recherche   | Cliquer **Nouvelle recherche**              | Formulaire réinitialisé                            | [x] |
| T-27 | Recherche vide       | Soumettre sans texte                        | Pas de crash                                       | [x] |

---

## 4. Tests de la fiche document

| ID   | Scénario        | Étapes                         | Résultat attendu                          | OK  |
| ---- | --------------- | ------------------------------ | ----------------------------------------- | --- |
| T-30 | Ouverture fiche | Ouvrir un résultat             | Résumé, tags et contenu visibles          | [x] |
| T-31 | Contenu complet | Lire le texte indexé           | Texte extractible affiché                 | [x] |
| T-32 | Export de fiche | Cliquer **Exporter**           | Fichier texte téléchargé                  | [x] |
| T-33 | Tags            | Vérifier les badges            | Tags cohérents                            | [x] |
| T-34 | Entités         | Ouvrir une pièce avec contacts | Entités visibles si présentes             | [x] |
| T-35 | Retour          | Retour Documents / Fonds       | Liste toujours disponible                 | [x] |

---

## 5. Tests d’administration et garde-fous

| ID   | Scénario                 | Étapes                                      | Résultat attendu                                      | OK  |
| ---- | ------------------------ | ------------------------------------------- | ----------------------------------------------------- | --- |
| T-36 | Suppression (Documents)  | Corbeille → saisir `SUPPRIMER`              | Document retiré du fonds, de l’index et du dossier    | [x] |
| T-37 | Reconstruction d’index   | Indexation → saisir `RECONSTRUIRE`          | Index recréé, recherche encore fonctionnelle          | [x] |
| T-38 | API sans confirm         | `DELETE` sans `?confirm=true`               | Erreur 400                                            | [x] |
| T-39 | Lecteur bloqué           | Compte lecteur sur `/documents`             | Redirection, pas d’administration                     | [x] |

---

## 6. Tests d'ergonomie et design

| ID   | Scénario            | Étapes                      | Résultat attendu                      | OK  |
| ---- | ------------------- | --------------------------- | ------------------------------------- | --- |
| T-40 | Lisibilité          | Parcourir les pages         | Contrastes et interlignes suffisants  | [x] |
| T-41 | Hiérarchie visuelle | Page recherche              | Barre de recherche mise en avant      | [x] |
| T-42 | Icônes d’action     | Tableau Documents           | Œil = voir, corbeille = supprimer     | [x] |
| T-43 | Badges type fichier | PDF, TXT, CSV, DOCX         | Couleurs distinctes                   | [x] |
| T-44 | Messages d’erreur   | API arrêtée                 | Message rouge visible                 | [x] |
| T-45 | Cohérence           | Naviguer 5 min              | Style uniforme, trois thèmes          | [x] |

---

## 7. Parcours utilisateur complet (démo soutenance)

**Durée estimée : 5 minutes**

1. [x] Ouvrir l’interface → espace public (recherche) sans connexion
2. [x] Rechercher `IBAM` en mode **Hybride** + comparaison des modes
3. [x] Ouvrir une fiche → résumé, tags, export
4. [x] Se connecter en administrateur (`admin` / `archives`)
5. [x] Montrer le fonds (1 110 documents) et la page Documents
6. [x] Tenter une suppression → garde-fou `SUPPRIMER`
7. [x] Montrer l’indexation (scan / reconstruction protégés)

---

## 8. Tests API complémentaires (Swagger)

| Endpoint                                         | Test    | Attendu      | OK  |
| ------------------------------------------------ | ------- | ------------ | --- |
| `GET /health`                                    | Execute | `status: ok` | [x] |
| `GET /documents`                                 | Execute | Liste JSON   | [x] |
| `GET /search?q=DocSearch&mode=keyword`           | Execute | `total >= 1` | [x] |
| `POST /index/rebuild` sans confirm               | Execute | 400          | [x] |
| `POST /index/rebuild?confirm=true`               | Execute | `indexed` > 0 | [x] |

---

## Journal de test

| Date       | Testeur                              | Version | Tests OK / Total | Remarques                                      |
| ---------- | ------------------------------------ | ------- | ---------------- | ---------------------------------------------- |
| 2026-10-27 | KOROGO Wendkuuni Ange Gaëtan 1er     | 0.7.0   | 35 / 35          | Grille cochée jointe au mémoire (figure 21).   |

---

## Anomalies trouvées

| ID test | Description du bug | Gravité | Statut   |
| ------- | ------------------ | ------- | -------- |
| —       | Aucune anomalie bloquante relevée sur cette session. | — | Clos |

---

*Session du 27 octobre 2026 — grille cochée pour la soutenance.*
