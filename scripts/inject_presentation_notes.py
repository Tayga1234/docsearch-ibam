"""Injecte les notes orateur dans le panneau Notes du PPTX."""

from pathlib import Path

from pptx import Presentation
from pptx.util import Pt

PPTX = Path(__file__).resolve().parent.parent / "travaux" / "PRESENTATION_PROJET_TUTORE.pptx"

NOTES = [
    # Slide 1
    """[20 s]

Bonjour. Je présente mon projet tutoré de Master ISI.

Thème : indexation intelligente de données hétérogènes pour la recherche d'information.
Prototype réalisé : DocuSearch.""",
    # Slide 2
    """[20 s]

Je présenterai le contexte, les objectifs, l'état de l'art, la solution DocuSearch, l'architecture, les réalisations, puis les limites et la conclusion.""",
    # Slide 3
    """[1 min]

Dans les petites structures, les documents sont dispersés et hétérogènes : PDF, Word, CSV, texte.

Sans outil central, la recherche reste manuelle et lente.
L'enjeu : indexer intelligemment ces formats pour retrouver l'information rapidement, en restant local et simple.""",
    # Slide 4
    """[1 min]

Question centrale :
Comment indexer automatiquement des données hétérogènes et offrir une recherche pertinente via une interface web locale ?

Objectifs : étudier l'état de l'art, concevoir une architecture modulaire, réaliser un prototype, l'évaluer, et proposer des perspectives.""",
    # Slide 5
    """[1 min 30]

15 articles, 2022–2026, lus en 3 jours.

Jour 1 : indexation unifiée et index appris (Clarke, DSI, NCI, GenIR).
Jour 2 : hybridation des moteurs (HetaRAG, ACORN, graphes).
Jour 3 : qualité de l'ingestion, vision, chunking, métadonnées.

Message clé : l'indexation intelligente est un pipeline complet, pas seulement un index de mots.""",
    # Slide 6
    """[1 min]

DocuSearch est un portail local qui suit le parcours :
ingestion → extraction → enrichissement → indexation → recherche

Il ajoute tags, résumé et entités.
Il propose 3 modes : mots-clés, sémantique, hybride.
Choix volontaire : adapté à un contexte à ressources limitées.""",
    # Slide 7
    """[1 min]

Quatre couches :
1. Interface React
2. API FastAPI
3. Métier : ingestion, extraction, enrichissement, recherche
4. Stockage : SQLite + Whoosh + fichiers locaux

Cette séparation facilite tests, maintenance et démonstration.""",
    # Slide 8
    """[2 min]

Le prototype sait aujourd'hui :
- ingérer PDF, DOCX, CSV, TXT ;
- enrichir automatiquement les documents ;
- rechercher en mots-clés, sémantique et hybride ;
- filtrer, supprimer, reconstruire l'index.

Démo courte si le temps le permet (45–60 s) :
1) rechercher un terme en hybride ;
2) ouvrir un document et montrer résumé + tags.

Sinon : « la démo montre ces trois modes et l'enrichissement automatique. »""",
    # Slide 9
    """[1 min]

Limites : sémantique légère (TF-IDF), pas d'auth multi-utilisateurs, pas de cloud, volumes modestes.

Perspectives : métadonnées plus riches, hybridation plus fine, OCR, puis module RAG.""",
    # Slide 10
    """[50 s]

Ce projet relie un problème concret à une solution démontrable.

À partir de la littérature récente, j'ai conçu DocuSearch pour indexer et rechercher des documents hétérogènes en local.

L'indexation intelligente est accessible même avec des ressources limitées.

Merci de votre attention. Je suis prêt pour vos questions.""",
]


def set_notes(slide, text: str) -> None:
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text.strip()
    run.font.name = "Calibri"
    run.font.size = Pt(12)


def main() -> None:
    prs = Presentation(str(PPTX))
    if len(prs.slides) != len(NOTES):
        raise SystemExit(f"Attendu {len(NOTES)} slides, trouvé {len(prs.slides)}")

    for slide, note in zip(prs.slides, NOTES):
        set_notes(slide, note)

    prs.save(str(PPTX))
    print(f"Notes injectées dans : {PPTX}")


if __name__ == "__main__":
    main()
