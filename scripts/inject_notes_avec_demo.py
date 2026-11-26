"""Injecte les notes orateur (11 slides + démo) dans le PPTX."""

from pathlib import Path

from pptx import Presentation
from pptx.util import Pt

CANDIDATES = [
    Path(__file__).resolve().parent.parent / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan_AVEC_DEMO.pptx",
    Path(__file__).resolve().parent.parent / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan.pptx",
]

NOTES = [
    """[15 s]

Bonjour. Je suis KOROGO Wendkuuni Ange Gaetan.
Projet tutoré Master ISIE : indexation intelligente de données hétérogènes.
Prototype : DocuSearch.""",
    """[15 s]

Je présenterai le contexte, les objectifs, l'état de l'art, la solution, l'architecture, les réalisations, puis une démonstration live, avant les limites et la conclusion.""",
    """[50 s]

Dans les petites structures, les documents sont dispersés et hétérogènes : PDF, Word, CSV, texte.
Sans outil central, la recherche reste manuelle et lente.
Enjeu : indexer intelligemment pour retrouver l'information rapidement, en restant local et simple.""",
    """[50 s]

Question centrale :
Comment indexer automatiquement des données hétérogènes et offrir une recherche pertinente via une interface web locale ?

Objectifs : état de l'art, architecture modulaire, prototype, évaluation, perspectives.""",
    """[1 min]

15 articles, 2022–2026, lus en 3 jours.

Jour 1 : indexation unifiée et index appris (Clarke, DSI, NCI, GenIR).
Jour 2 : hybridation des moteurs (HetaRAG, ACORN, graphes).
Jour 3 : qualité de l'ingestion, vision, chunking, métadonnées.

Message clé : l'indexation intelligente est un pipeline complet, pas seulement un index de mots.""",
    """[50 s]

DocuSearch est un portail local :
ingestion → extraction → enrichissement → indexation → recherche

Il ajoute tags, résumé et entités.
Trois modes : mots-clés, sémantique, hybride.
Choix volontaire : adapté à un contexte à ressources limitées.""",
    """[50 s]

Quatre couches :
1. Interface React
2. API FastAPI
3. Métier : ingestion, extraction, enrichissement, recherche
4. Stockage : SQLite + Whoosh + fichiers locaux

Cette séparation facilite tests, maintenance et démonstration.""",
    """[50 s]

Le prototype sait aujourd'hui :
- ingérer PDF, DOCX, CSV, TXT ;
- enrichir automatiquement les documents ;
- rechercher en mots-clés, sémantique et hybride ;
- filtrer, supprimer, reconstruire l'index.

Je vais maintenant le montrer en live.""",
    """[1 min 30] — DÉMONSTRATION

Scénario live :
1. Badge API vert (v0.5.0)
2. Indexer le dossier ou importer un fichier
3. Recherche « formation » en mode Hybride
4. Comparer rapidement Mots-clés puis Sémantique
5. Ouvrir un document : résumé, tags, entités

Message : DocuSearch unifie des formats hétérogènes et offre une recherche intelligente, utilisable tout de suite.

Plan B : si l'application ne répond pas, montrer les captures préparées.""",
    """[45 s]

Limites : sémantique légère (TF-IDF), pas d'auth multi-utilisateurs, pas de cloud, volumes modestes.

Perspectives : métadonnées plus riches, hybridation plus fine, OCR, puis module RAG.""",
    """[40 s]

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


def inject(path: Path) -> Path:
    prs = Presentation(str(path))
    n = len(prs.slides)
    if n != 11:
        raise SystemExit(f"{path.name}: attendu 11 slides (avec démo), trouvé {n}")

    for slide, note in zip(prs.slides, NOTES):
        set_notes(slide, note)

    try:
        prs.save(str(path))
        return path
    except PermissionError:
        alt = path.with_name(path.stem + "_NOTES.pptx")
        prs.save(str(alt))
        print(f"Fichier verrouillé, sauvegarde : {alt}")
        return alt


def main() -> None:
    target = next((p for p in CANDIDATES if p.exists()), None)
    if target is None:
        raise SystemExit("Aucune présentation KOROGO trouvée")

    # Prefer AVEC_DEMO if present
    demo = CANDIDATES[0]
    path = demo if demo.exists() else target
    saved = inject(path)
    print(f"Notes injectées ({11} slides) : {saved}")


if __name__ == "__main__":
    main()
