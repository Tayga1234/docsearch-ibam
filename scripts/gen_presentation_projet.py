"""
Génère la présentation PowerPoint du projet tutoré DocuSearch BF (10 slides).

Usage :
    .venv\\Scripts\\python.exe scripts\\gen_presentation_projet.py
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT_ROOT / "travaux" / "PRESENTATION_PROJET_TUTORE.pptx"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
ACCENT = RGBColor(0xC2, 0x41, 0x0C)
DARK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xE2, 0xE8, 0xF0)


def _run(p, text, *, size=18, bold=False, color=DARK, font="Calibri"):
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return run


def _bg(slide, color):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    spTree = slide.shapes._spTree
    sp = shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def _header(slide, title: str, subtitle: str | None = None):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tf = bar.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    _run(p, "  " + title, size=26, bold=True, color=WHITE)
    if subtitle:
        accent = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.05), Inches(13.333), Inches(0.38)
        )
        accent.fill.solid()
        accent.fill.fore_color.rgb = TEAL
        accent.line.fill.background()
        tf = accent.text_frame
        p = tf.paragraphs[0]
        _run(p, "   " + subtitle, size=12, color=WHITE)


def _footer(slide, page: int, total: int = 10):
    box = slide.shapes.add_textbox(Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3))
    p = box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    _run(p, f"DocuSearch BF — Projet tutoré Master ISI  |  {page}/{total}", size=11, color=GRAY)


def _card(slide, left, top, width, height, title, lines, accent=TEAL):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD
    shape.line.color.rgb = SOFT
    stripe = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.12), Inches(height)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()

    title_box = slide.shapes.add_textbox(
        Inches(left + 0.28), Inches(top + 0.15), Inches(width - 0.4), Inches(0.4)
    )
    p = title_box.text_frame.paragraphs[0]
    _run(p, title, size=15, bold=True, color=NAVY)

    body = slide.shapes.add_textbox(
        Inches(left + 0.28), Inches(top + 0.55), Inches(width - 0.45), Inches(height - 0.7)
    )
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(6)
        _run(p, "•  " + line, size=13, color=DARK)


def _bullets(slide, items, *, left=0.7, top=1.7, width=12, size=18):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10)
        _run(p, "▸  " + item, size=size, color=DARK)


def build() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = 10

    # 1. Titre
    s = prs.slides.add_slide(blank)
    _bg(s, NAVY)
    band = s.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(5.9), Inches(13.333), Inches(1.6)
    )
    band.fill.solid()
    band.fill.fore_color.rgb = TEAL
    band.line.fill.background()

    box = s.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(11.5), Inches(3.8))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(p, "PROJET TUTORÉ — MASTER ISI", size=16, color=SOFT)
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(18)
    _run(
        p,
        "Indexation intelligente de données hétérogènes\npour la recherche d'information",
        size=30,
        bold=True,
        color=WHITE,
    )
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(22)
    _run(p, "Prototype : DocuSearch BF", size=20, bold=True, color=RGBColor(0x99, 0xF6, 0xE4))

    foot = s.shapes.add_textbox(Inches(0.9), Inches(6.15), Inches(11.5), Inches(1.1))
    tf = foot.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(
        p,
        "Master Ingénierie des Systèmes d'Information en Entreprise — Burkina Faso\n"
        "Revue de littérature 2022–2026  ·  Prototype local FastAPI + React  ·  API v0.5.0",
        size=14,
        color=WHITE,
    )
    _footer(s, 1, total)

    # 2. Contexte & problème
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "1. Contexte et problématique terrain", "Pourquoi ce projet ?")
    _card(
        s,
        0.5,
        1.7,
        4.0,
        4.8,
        "Contexte",
        [
            "École, ONG, PME, administration locale",
            "Documents dispersés dans plusieurs dossiers",
            "Formats variés : PDF, Word, CSV, TXT",
            "Pas de point d'accès unique",
            "Perte de temps à chercher l'information",
        ],
        accent=NAVY,
    )
    _card(
        s,
        4.75,
        1.7,
        4.0,
        4.8,
        "Problèmes observés",
        [
            "Données hétérogènes difficiles à unifier",
            "Recherche manuelle et peu fiable",
            "Mise en page / tableaux souvent perdus",
            "Pas de tags ni d'enrichissement",
            "Outils cloud parfois inadaptés (coût, données locales)",
        ],
        accent=ACCENT,
    )
    _card(
        s,
        9.0,
        1.7,
        3.8,
        4.8,
        "Enjeu",
        [
            "Indexer intelligemment des formats différents",
            "Offrir une recherche pertinente",
            "Rester local, simple et démontrable",
            "Lier science (état de l'art) et réalisation",
        ],
        accent=TEAL,
    )
    _footer(s, 2, total)

    # 3. Problématique & objectifs
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "2. Problématique et objectifs", "Cadrage scientifique et technique")

    quote = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(12.1), Inches(1.55)
    )
    quote.fill.solid()
    quote.fill.fore_color.rgb = WHITE
    quote.line.color.rgb = TEAL
    tf = quote.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(
        p,
        "Comment concevoir et implémenter un système local capable d'indexer automatiquement\n"
        "des données hétérogènes et d'offrir une recherche d'information pertinente\n"
        "via une interface web ?",
        size=16,
        bold=True,
        color=NAVY,
    )

    _card(
        s,
        0.6,
        3.5,
        6.0,
        3.1,
        "Objectifs généraux",
        [
            "Étudier l'état de l'art (15 articles, 2022–2026)",
            "Concevoir une architecture modulaire",
            "Réaliser un prototype fonctionnel",
            "Évaluer la pertinence sur un corpus de test",
            "Proposer des perspectives réalistes",
        ],
        accent=NAVY,
    )
    _card(
        s,
        6.9,
        3.5,
        5.8,
        3.1,
        "Objectifs techniques",
        [
            "≥ 4 formats : PDF, DOCX, CSV, TXT",
            "Indexation locale SQLite + Whoosh",
            "3 modes : mots-clés, sémantique, hybride",
            "API REST documentée (FastAPI / OpenAPI)",
            "Interface React moderne et démontrable",
        ],
        accent=TEAL,
    )
    _footer(s, 3, total)

    # 4. État de l'art
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "3. État de l'art (2022–2026)", "15 articles — 5 par jour × 3 jours")
    _card(
        s,
        0.5,
        1.65,
        4.0,
        4.9,
        "Jour 1 — Fondements",
        [
            "Indexation annotative (Clarke)",
            "Données semi-structurées JSON",
            "DSI / NCI : index appris",
            "Survey GenIR (matching → génération)",
            "Idée : l'index n'est plus une simple table de mots",
        ],
        accent=NAVY,
    )
    _card(
        s,
        4.7,
        1.65,
        4.0,
        4.9,
        "Jour 2 — Hybridation",
        [
            "ASI / GLEN : docids dynamiques",
            "HetaRAG : multi-moteurs",
            "ACORN : vecteurs + filtres",
            "DiscoverPath : graphes de connaissances",
            "Idée : combiner plusieurs signaux de pertinence",
        ],
        accent=TEAL,
    )
    _card(
        s,
        8.9,
        1.65,
        3.9,
        4.9,
        "Jour 3 — Pipeline RAG",
        [
            "Ingestion & parsing LLM",
            "ColPali / VisRAG : pages images",
            "Mix-of-Granularity : chunking",
            "Métadonnées enrichies",
            "Idée : la qualité amont conditionne tout",
        ],
        accent=ACCENT,
    )
    _footer(s, 4, total)

    # 5. Solution
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "4. Solution proposée : DocuSearch BF", "Portail documentaire local intelligent")
    _bullets(
        s,
        [
            "Un portail web local pour ingérer, indexer et rechercher des documents hétérogènes",
            "Pipeline complet : ingestion → extraction → enrichissement → indexation → recherche",
            "Enrichissement intelligent : tags, résumé extractif, entités (dates, e-mails, orgs…)",
            "Recherche multi-modes : mots-clés (Whoosh), sémantique (TF-IDF), hybride",
            "Conçu pour un contexte à ressources limitées : pas de cloud obligatoire, pas de GPU",
            "Lien direct avec la littérature : hybridation, métadonnées, qualité d'ingestion",
        ],
        top=1.7,
        size=18,
    )
    _footer(s, 5, total)

    # 6. Architecture
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "5. Architecture technique", "Séparation claire des responsabilités")

    layers = [
        ("Interface", "React + Vite\nRecherche, filtres,\nmodal, upload", NAVY),
        ("API", "FastAPI v0.5.0\nREST + OpenAPI\nLogging & health", TEAL),
        ("Métier", "Ingestion\nExtraction\nEnrichissement\nSearch engine", ACCENT),
        ("Stockage", "SQLite\nWhoosh\ndata/raw/", NAVY),
    ]
    for i, (title, body, color) in enumerate(layers):
        left = 0.55 + i * 3.15
        shape = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.8), Inches(2.95), Inches(3.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = WHITE
        shape.line.color.rgb = SOFT
        top = s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.8), Inches(2.95), Inches(0.7)
        )
        top.fill.solid()
        top.fill.fore_color.rgb = color
        top.line.fill.background()
        tf = top.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        _run(p, title, size=16, bold=True, color=WHITE)
        body_box = s.shapes.add_textbox(
            Inches(left + 0.2), Inches(2.7), Inches(2.55), Inches(2.4)
        )
        tf = body_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        _run(p, body, size=14, color=DARK)
        if i < 3:
            arrow = s.shapes.add_textbox(
                Inches(left + 2.85), Inches(3.3), Inches(0.4), Inches(0.4)
            )
            p = arrow.text_frame.paragraphs[0]
            _run(p, "→", size=22, bold=True, color=TEAL)

    note = s.shapes.add_textbox(Inches(0.6), Inches(5.6), Inches(12), Inches(1.1))
    tf = note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    _run(
        p,
        "Stack : Python 3.10+, FastAPI, Whoosh, scikit-learn, SQLite  |  Frontend React  |  "
        "Tests pytest (34+)  |  Déploiement local (port API 8010)",
        size=14,
        color=GRAY,
    )
    _footer(s, 6, total)

    # 7. Fonctionnalités réalisées
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "6. Réalisations concrètes", "Ce que le prototype sait faire aujourd'hui")
    _card(
        s,
        0.5,
        1.65,
        4.0,
        4.9,
        "Ingestion & extraction",
        [
            "Scan du dossier data/raw/",
            "Upload multi-formats",
            "PDF, DOCX, CSV, TXT",
            "Skip intelligent (hash contenu)",
            "Indexation Whoosh en batch",
            "Limite taille + noms uniques",
        ],
        accent=NAVY,
    )
    _card(
        s,
        4.7,
        1.65,
        4.0,
        4.9,
        "Intelligence & recherche",
        [
            "Tags automatiques",
            "Résumé extractif",
            "Entités nommées",
            "Whoosh + boost titre/tags",
            "TF-IDF mis en cache",
            "Hybride 60% / 40% + highlights",
        ],
        accent=TEAL,
    )
    _card(
        s,
        8.9,
        1.65,
        3.9,
        4.9,
        "Interface & API",
        [
            "UI React modulaire",
            "Filtres type / tag",
            "Suppression de documents",
            "Rebuild index",
            "Health enrichi",
            "Messages d'erreur lisibles",
        ],
        accent=ACCENT,
    )
    _footer(s, 7, total)

    # 8. Résultats / démo
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "7. Résultats, tests et démonstration", "Preuves de fonctionnement")
    _card(
        s,
        0.5,
        1.65,
        6.1,
        4.9,
        "Évaluation",
        [
            "34 tests automatisés backend (pytest)",
            "Scénarios manuels d'interface documentés",
            "Corpus de démo ISGO (~30+ documents)",
            "Recherche < 1 s sur le corpus de test",
            "API documentée : /docs (Swagger)",
            "Trois modes comparables en live devant jury",
        ],
        accent=TEAL,
    )
    _card(
        s,
        6.9,
        1.65,
        5.8,
        4.9,
        "Scénario de démo (5 min)",
        [
            "1. Afficher le badge API v0.5.0",
            "2. Indexer le dossier / importer un fichier",
            "3. Rechercher « formation » en hybride",
            "4. Comparer mots-clés vs sémantique",
            "5. Ouvrir un document : résumé, tags, entités",
            "6. Filtrer par type / supprimer un document",
        ],
        accent=NAVY,
    )
    _footer(s, 8, total)

    # 9. Limites & perspectives
    s = prs.slides.add_slide(blank)
    _bg(s, LIGHT)
    _header(s, "8. Limites et perspectives", "Transparence scientifique + feuille de route")
    _card(
        s,
        0.5,
        1.65,
        6.1,
        4.9,
        "Limites assumées",
        [
            "Sémantique = TF-IDF (pas d'embeddings lourds)",
            "Pas d'auth multi-utilisateurs ni cloud",
            "Pas d'indexation visuelle type ColPali",
            "Volumes ciblés : dizaines/centaines de docs",
            "Certains articles d'état de l'art restent hors MVP",
        ],
        accent=ACCENT,
    )
    _card(
        s,
        6.9,
        1.65,
        5.8,
        4.9,
        "Perspectives",
        [
            "Hybridation plus fine + reranking",
            "Enrichissement métadonnées plus riche",
            "Ingestion adaptative (OCR / PDF scannés)",
            "Module RAG pour réponses sourcées",
            "Déploiement cloud progressif si besoin",
        ],
        accent=TEAL,
    )
    _footer(s, 9, total)

    # 10. Conclusion
    s = prs.slides.add_slide(blank)
    _bg(s, NAVY)
    box = s.shapes.add_textbox(Inches(0.9), Inches(1.3), Inches(11.5), Inches(4.8))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(p, "Conclusion", size=18, color=SOFT)
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(14)
    _run(
        p,
        "Un thème actuel, une revue de littérature solide,\nun prototype démontrable et une trajectoire claire.",
        size=24,
        bold=True,
        color=WHITE,
    )
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(28)
    _run(
        p,
        "DocuSearch BF montre qu'on peut appliquer l'indexation intelligente\n"
        "à des données hétérogènes, même dans un contexte local et à ressources limitées.",
        size=16,
        color=RGBColor(0xCB, 0xD5, 0xE1),
    )
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(36)
    _run(p, "Merci de votre attention — questions ?", size=20, bold=True, color=RGBColor(0x99, 0xF6, 0xE4))
    _footer(s, 10, total)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(f"Présentation générée : {path}")
