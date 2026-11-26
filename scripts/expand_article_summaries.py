"""Ajoute un paragraphe de synthèse finale à chaque résumé d'article."""

from __future__ import annotations

import re
from pathlib import Path

ADDITIONS = {
    "jour_01/BILAN_JOUR_1.md": [
        None,  # article 1 déjà étendu
        (
            "Du point de vue méthodologique, Heflin et al. insistent sur l'importance de rendre "
            "la découverte de données aussi simple que la recherche web. Leur évaluation porte "
            "sur l'efficacité de l'indexation et la facilité d'usage de l'interface. L'article "
            "montre aussi que l'indexation scientifique doit respecter les principes FAIR : rendre "
            "les données trouvables et réutilisables. Pour bien comprendre l'article, il faut retenir "
            "que l'unité d'indexation n'est plus le fichier mais l'élément de donnée, ce qui change "
            "profondément la manière de concevoir la recherche sur données semi-structurées."
        ),
        (
            "Tay et al. comparent plusieurs variantes d'entraînement et mettent en évidence le rôle "
            "décisif de la représentation des docids. Leur article est souvent cité parce qu'il a "
            "ouvert la voie à toute une famille de travaux en recherche générative. Il reste toutefois "
            "important de noter que DSI dépend fortement de la taille du corpus et du coût de "
            "mémorisation. En lecture, on retient donc à la fois la nouveauté du paradigme et ses "
            "contraintes pratiques, qui expliquent pourquoi les systèmes industriels combinent encore "
            "souvent index externe et modèles de langage."
        ),
        (
            "Wang et al. détaillent aussi le rôle de la génération artificielle de requêtes pour "
            "enrichir l'apprentissage, ainsi que l'impact des identifiants sémantiques sur le rappel. "
            "Leur comparaison avec des bases fortes du domaine donne au lecteur une idée précise de "
            "l'apport réel de NCI. L'article est utile pour comprendre que la performance ne vient pas "
            "seulement du remplacement de l'index, mais de tout un ensemble de choix d'apprentissage "
            "coordonnés. C'est une lecture incontournable pour saisir comment l'indexation peut devenir "
            "une fonction apprise plutôt qu'une simple structure statique."
        ),
        (
            "Le survey de Zhang et al. est particulièrement utile pour organiser ses lectures ultérieures. "
            "Il relie les travaux fondateurs aux tendances récentes comme la recherche multimodale, "
            "l'apprentissage incrémental ou la génération de réponses avec citations. Les auteurs "
            "discutent aussi des métriques d'évaluation et des limites actuelles de la GenIR, ce qui "
            "aide à adopter un regard critique. Pour un travail universitaire, cet article sert de "
            "carte du territoire : il permet de comprendre où se situe chaque contribution sans se "
            "perdre dans la multiplicité des publications récentes."
        ),
    ],
    "jour_02/BILAN_JOUR_2.md": [
        (
            "L'article de Yang et al. est intéressant parce qu'il répond à une objection concrète "
            "faite à la recherche générative : celle de l'obsolescence rapide de l'index. Leur module "
            "d'indexation sémantique et leur mécanisme de reparamétrisation sont les pièces centrales "
            "à comprendre. Les expériences sur données industrielles renforcent la crédibilité du modèle. "
            "En synthèse, ASI montre que l'on peut rapprocher indexation automatique et récupération "
            "dans un même apprentissage, ce qui rapproche la recherche académique des besoins réels des "
            "moteurs documentaires évolutifs."
        ),
        (
            "Lee et al. insistent sur la lisibilité des identifiants lexicaux et sur la réduction des "
            "collisions entre documents. Leur stratégie d'apprentissage en deux temps est plus facile "
            "à suivre que certaines architectures entièrement monolithiques. GLEN est aussi intéressant "
            "parce qu'il obtient de bons résultats sur plusieurs benchmarks différents, ce qui suggère "
            "une certaine robustesse. Pour le lecteur, l'article montre qu'améliorer la recherche générative "
            "ne signifie pas forcément abandonner toute interprétabilité de l'index."
        ),
        (
            "Même si HetaRAG est présenté comme un rapport technique encore en cours, il décrit très "
            "clairement une architecture cible où chaque type de donnée est traité par le moteur le plus "
            "adapté. Les auteurs expliquent aussi pourquoi le RAG a besoin de preuves variées pour limiter "
            "les hallucinations. Le lecteur y gagne une vision systémique : l'indexation intelligente n'est "
            "plus seulement une question de format de fichier, mais de coordination entre plusieurs formes "
            "de mémoire documentaire."
        ),
        (
            "Gollapudi et al. fournissent en plus une analyse détaillée des compromis entre précision, "
            "rappel et vitesse. Leur capacité à étendre des bibliothèques existantes rend ACORN plus "
            "convaincant pour un déploiement réel. L'article est utile pour comprendre comment les contraintes "
            "structurées peuvent être intégrées très tôt dans la recherche vectorielle, plutôt qu'ajoutées "
            "comme simple filtre après coup. C'est une lecture importante pour saisir la hybridation "
            "vecteur + métadonnées."
        ),
        (
            "DiscoverPath montre aussi comment une interface peut transformer une structure complexe en "
            "outil de navigation compréhensible. Chuang et al. ne se limitent pas à publier un algorithme : "
            "ils proposent un système complet, avec recommandations de requêtes et visualisation. Leur "
            "choix du domaine biomédical renforce l'intérêt du travail, car la terminologie y est "
            "particulièrement difficile. En résumé, l'article illustre comment l'indexation intelligente "
            "peut devenir exploratoire et pas seulement discriminative."
        ),
    ],
    "jour_03/BILAN_JOUR_3.md": [
        (
            "Pérez et Vizcaino décrivent précisément le rôle de chaque stratégie d'extraction selon le "
            "type de document rencontré. Leur agent assembleur est essentiel pour comprendre comment les "
            "fragments extraits sont recombinés en un document cohérent. Les métriques de fidélité et de "
            "pertinence montrent que leurs gains ne sont pas théoriques. Pour le lecteur, l'article rappelle "
            "qu'un pipeline documentaire performant doit être adaptatif : il ne s'agit pas de choisir une "
            "seule bibliothèque d'extraction, mais d'orchestrer plusieurs lectures du même document."
        ),
        (
            "Faysse et al. comparent ColPali non seulement aux méthodes textuelles, mais aussi aux coûts "
            "de prétraitement. Le benchmark ViDoRe est une contribution en soi, car il formalise des tâches "
            "de recherche visuelle de pages. L'article montre en outre que la late interaction permet de "
            "conserver de bonnes performances sans sacrifier toute la richesse visuelle. Pour bien saisir "
            "ColPali, il faut retenir que l'image de la page devient l'unité d'indexation, ce qui change "
            "radicalement la définition même du document searchable."
        ),
        (
            "Yu et al. détaillent aussi l'entraînement du retriever visuel et les différentes stratégies "
            "de génération aval. Leur comparaison avec le RAG textuel est convaincante parce qu'elle couvre "
            "à la fois la récupération et la qualité finale de la réponse. VisRAG montre surtout que le "
            "parsing n'est pas une étape neutre : c'est souvent là que l'information se perd. L'article est "
            "donc fondamental pour comprendre pourquoi l'indexation multimodale progresse si vite dans la "
            "littérature récente."
        ),
        (
            "Zhong et al. expliquent clairement le fonctionnement du routeur et la logique du "
            "Mix-of-Granularity. L'extension MoG-Graph est particulièrement utile pour les documents où "
            "l'information pertinente est dispersée. Leur article montre aussi que le chunking ne doit pas "
            "être fixé une fois pour toutes lors de l'indexation : on peut préparer plusieurs granularités "
            "et laisser la requête choisir la plus adaptée. C'est une idée puissante pour les corpus "
            "hétérogènes mêlant notices courtes et rapports longs."
        ),
        (
            "Dadopoulos et al. décrivent en détail leur pipeline offline de génération de métadonnées et "
            "le rôle du reranker personnalisé. Leur étude sur FinanceBench est utile parce qu'elle porte "
            "sur un domaine où la précision est cruciale. L'article montre aussi qu'on peut obtenir de "
            "bons résultats sans toujours recourir aux solutions commerciales les plus coûteuses. En "
            "lecture, on retient surtout que les métadonnées ne sont pas un simple habillage : elles "
            "participent directement à la qualité de l'index et donc de la recherche."
        ),
    ],
}


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "travaux"
    for rel_path, paragraphs in ADDITIONS.items():
        path = root / rel_path
        text = path.read_text(encoding="utf-8")
        chunks = re.split(r"(## Article \d+\s*\n)", text)
        output = [chunks[0]]
        article_idx = 0
        for i in range(1, len(chunks), 2):
            article_idx += 1
            header = chunks[i]
            body = chunks[i + 1] if i + 1 < len(chunks) else ""
            if article_idx - 1 < len(paragraphs) and paragraphs[article_idx - 1]:
                extra = "\n\n" + paragraphs[article_idx - 1]
                if paragraphs[article_idx - 1] not in body:
                    body = re.sub(r"\n---\s*$", extra + "\n\n---", body.rstrip())
            output.append(header + body)
        path.write_text("".join(output), encoding="utf-8")
        print("Updated", rel_path)


if __name__ == "__main__":
    main()
