# Manuel utilisateur — DocSearch BF

**Public** : collaborateurs et étudiants de l'ISGO (contexte de démonstration).

## 1. Accès au portail

1. Ouvrir le navigateur à l'adresse fournie (ex. http://localhost:5173).
2. L’espace public s’ouvre sans connexion : recherche, fonds, fiches et état du système.
3. Vérifier que l’API est en ligne (badge / page Système).
4. Pour indexer ou supprimer, cliquer sur **Administration** et se connecter (`admin` / `archives`).

## 2. Rechercher un document

1. Saisir un ou plusieurs mots dans la barre de recherche.
2. Choisir le mode :
   - **Hybride** (recommandé) : combine mots-clés et similarité TF-IDF.
   - **Mots-clés** : correspondance exacte dans le texte indexé (BM25).
   - **Sémantique** : similarité TF-IDF locale (pas d’embedding neuronal).
3. Cliquer sur **Rechercher** ou appuyer sur Entrée.
4. Les résultats s'affichent sous forme de cartes (titre, extrait, type, score).

### Exemples de requêtes (jeu de démo ISGO)

| Requête | Documents attendus |
|---------|-------------------|
| `formation` | Plan de formation, catalogue master, fiches stage |
| `budget` | Budget prévisionnel, note de service budget |
| `DocSearch` | Projet tutoré, comptes rendus, FAQ |
| `partenariat` | Convention, partenaires institutionnels |

## 3. Consulter le détail d'un document

1. Cliquer sur une carte de résultat ou sur un document de la liste.
2. La fenêtre modale affiche :
   - Résumé automatique
   - Tags générés
   - Entités extraites (organisations, dates…)
   - Contenu textuel extrait

## 4. Ajouter des documents (administrateur)

Se connecter d’abord via **Administration**.

### Méthode A — Dépôt dans le dossier partagé

1. Copier le fichier (PDF, DOCX, CSV ou TXT) dans `data/raw/`.
2. Ouvrir **Indexation** → indexer le dossier.

### Méthode B — Upload direct

1. Ouvrir **Documents** → choisir un fichier supporté.
2. Le document est indexé automatiquement.

## 5. Formats supportés

| Format | Extension | Exemple |
|--------|-----------|---------|
| Texte | `.txt` | Notes, procédures |
| Tableur | `.csv` | Listes, inventaires |
| Word | `.docx` | Rapports, courriers |
| PDF | `.pdf` | Brochures, notes officielles |

## 6. Indicateurs de l'interface

| Élément | Signification |
|---------|---------------|
| Badge vert **API v0.7.0** | Connexion au backend OK |
| Badge rouge **API hors ligne** | Backend arrêté ou inaccessible |
| Nombre de documents | Total indexé dans la base |
| Résultat du scan | Fichiers traités lors du dernier scan |

## 7. Limites connues

- Recherche locale uniquement (pas d'accès Internet).
- Pas d'authentification utilisateur dans cette version.
- Les PDF scannés (images) ne sont pas reconnus (texte non extractible).
- Un seul dossier source : `data/raw/` (pas de sous-dossiers).

## 8. Support

Contacter le service informatique ISGO ou consulter la FAQ intégrée au jeu de démo (`faq_recherche_documentaire.txt`).
