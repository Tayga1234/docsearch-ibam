"""Ajoute une phrase finale pour viser ~200 mots par résumé."""

from __future__ import annotations

import re
from pathlib import Path

TAILS = {
    "jour_01/BILAN_JOUR_1.md": [
        " En lecture, on retient surtout que Clarke replace l'indexation au centre du problème des données hétérogènes, en proposant un cadre unique plutôt qu'une accumulation d'outils spécialisés.",
        " L'article de Heflin et al. est donc utile pour montrer comment rendre interrogeables des données semi-structurées sans imposer un schéma unique à l'avance.",
        " Tay et al. ouvrent ainsi une perspective nouvelle, même si leur approche reste coûteuse et dépendante de la taille du corpus étudié.",
        " Wang et al. confirment que l'avenir de la recherche documentaire ne concerne pas seulement de meilleurs scores, mais aussi de meilleures représentations des documents dans l'index.",
        " Le survey de Zhang et al. permet enfin de situer ces travaux dans une évolution plus large, sans perdre de vue les limites encore ouvertes du domaine.",
    ],
    "jour_02/BILAN_JOUR_2.md": [
        " Yang et al. montrent ainsi que la recherche générative devient plus crédible lorsqu'elle accepte l'arrivée continue de nouveaux documents.",
        " GLEN illustre une voie intermédiaire entre index classique et index entièrement neuronal, ce qui en facilite la compréhension.",
        " HetaRAG aide surtout à comprendre pourquoi les systèmes récents combinent plusieurs moteurs au lieu d'en choisir un seul.",
        " ACORN confirme que la recherche moderne doit souvent articuler similarité sémantique et contraintes structurées dans un même mécanisme.",
        " DiscoverPath montre enfin qu'un graphe de connaissances peut améliorer la découverte documentaire au-delà du simple classement par mots-clés.",
    ],
    "jour_03/BILAN_JOUR_3.md": [
        " Pérez et Vizcaino rappellent donc que la qualité de l'ingestion conditionne toute la chaîne de recherche documentaire.",
        " ColPali propose une alternative convaincante lorsque la mise en page et les éléments visuels sont déterminants.",
        " VisRAG prolonge cette idée à l'ensemble du pipeline RAG et montre les limites du traitement purement textuel.",
        " Zhong et al. soulignent que le découpage des documents n'est pas un détail technique, mais un vrai choix d'indexation.",
        " Dadopoulos et al. démontrent enfin que les métadonnées enrichies peuvent devenir un levier majeur de pertinence sur documents complexes.",
    ],
}

root = Path(__file__).resolve().parent.parent / "travaux"
for rel, tails in TAILS.items():
    path = root / rel
    text = path.read_text(encoding="utf-8")
    blocks = list(re.finditer(r"(\*\*Résumé personnel :\*\*\s*\n)(.*?)(\n---)", text, re.S))
    if len(blocks) != len(tails):
        raise ValueError(f"{rel}: {len(blocks)} blocs, {len(tails)} tails")
    offset = 0
    for match, tail in zip(blocks, tails):
        if tail.strip() in match.group(2):
            continue
        start = match.start(2) + offset
        end = match.end(2) + offset
        body = match.group(2).rstrip() + tail
        text = text[:start] + body + text[end:]
        offset += len(tail)
    path.write_text(text, encoding="utf-8")
    print("Updated", rel)
