# Déployer DocSearch sur Render (URL publique)

## Prérequis

- Dépôt GitHub : https://github.com/Tayga1234/docsearch-ibam
- Compte [Render](https://render.com) (offre Free)

## Étapes

1. Ouvre [https://dashboard.render.com](https://dashboard.render.com) et connecte-toi.
2. **New** → **Web Service** → branche le dépôt `Tayga1234/docsearch-ibam`.
3. Réglages :
   - **Runtime** : Docker
   - **Branch** : `main`
   - **Plan** : Free
   - **Health Check Path** : `/health`
4. Clique **Create Web Service** et attends le build (plusieurs minutes : corpus + npm + pip).
5. Quand le statut est **Live**, ouvre l’URL `https://docsearch-ibam-xxxx.onrender.com`.

## Avant une démo

Le plan gratuit **endort** le service après inactivité. Ouvre l’URL **2 minutes avant** la présentation pour le réveiller (premier chargement plus long).

## Vérifications rapides

- `/health` → `"status": "ok"` et un nombre de documents > 0
- Recherche `BM25` → résultats scientifiques
- Recherche `formation` → pièces archives IBAM

## Compte admin (démo)

- Identifiant : `admin`
- Mot de passe : `archives`
