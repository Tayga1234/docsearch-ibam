# -*- coding: utf-8 -*-
"""Construit une présentation enrichie (images) fidèle au texte et aux notes existants."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt, Emu

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "travaux" / "PRESENTATION_KOROGO_RICHE_IMAGES.pptx"
ASSETS = ROOT / "travaux" / "ppt_assets"
ASSETS.mkdir(parents=True, exist_ok=True)

LOGO = ROOT / "travaux" / "docusearch-logo.png"
HERO = Path(
    r"C:\Users\korog\.cursor\projects\c-Users-korog-Desktop-ecole-projet-tutore\assets\ppt-hero-banner.png"
)
if not HERO.exists():
    HERO = ROOT / "assets" / "ppt-hero-banner.png"

# Couleurs (alignées DocuSearch)
NAVY = RGBColor(0x0B, 0x12, 0x20)
CARD = RGBColor(0x15, 0x23, 0x3B)
TEAL = RGBColor(0x0E, 0xA5, 0xE9)
INDIGO = RGBColor(0x63, 0x66, 0xF1)
WHITE = RGBColor(0xF8, 0xFA, 0xFC)
MUTED = RGBColor(0x94, 0xA3, 0xB8)
GREEN = RGBColor(0x22, 0xC5, 0x5E)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
ACCENT_BAR = RGBColor(0x0E, 0xA5, 0xE9)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def _font(size: int):
    for name in (
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_icon(path: Path, label: str, color: tuple[int, int, int], symbol: str) -> Path:
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 8, 248, 248), radius=48, fill=(*color, 255))
    d.text((128, 100), symbol, font=_font(72), fill=(255, 255, 255, 255), anchor="mm")
    d.text((128, 190), label, font=_font(28), fill=(255, 255, 255, 230), anchor="mm")
    img.save(path)
    return path


def make_pipeline_banner(path: Path) -> Path:
    steps = ["Ingestion", "Extraction", "Enrichissement", "Indexation", "Recherche"]
    w, h = 1600, 220
    img = Image.new("RGB", (w, h), (11, 18, 32))
    d = ImageDraw.Draw(img)
    box_w = 260
    gap = 40
    total = len(steps) * box_w + (len(steps) - 1) * gap
    x0 = (w - total) // 2
    y = 40
    for i, step in enumerate(steps):
        x = x0 + i * (box_w + gap)
        d.rounded_rectangle((x, y, x + box_w, y + 120), radius=20, fill=(14, 165, 233))
        d.text((x + box_w // 2, y + 60), step, font=_font(28), fill=(11, 18, 32), anchor="mm")
        if i < len(steps) - 1:
            ax = x + box_w + 8
            d.polygon(
                [(ax, y + 50), (ax + 24, y + 60), (ax, y + 70)],
                fill=(99, 102, 241),
            )
    img.save(path)
    return path


def make_arch_diagram(path: Path) -> Path:
    layers = [
        ("Interface", "React + Vite", (99, 102, 241)),
        ("API", "FastAPI v0.5.0", (14, 165, 233)),
        ("Métier", "Ingestion · Extraction · Enrichissement · Search", (34, 197, 94)),
        ("Stockage", "SQLite · Whoosh · data/raw/", (245, 158, 11)),
    ]
    w, h = 1400, 720
    img = Image.new("RGB", (w, h), (11, 18, 32))
    d = ImageDraw.Draw(img)
    for i, (title, sub, color) in enumerate(layers):
        y = 40 + i * 165
        d.rounded_rectangle((80, y, w - 80, y + 130), radius=24, fill=color)
        d.text((120, y + 40), title, font=_font(40), fill=(11, 18, 32))
        d.text((120, y + 90), sub, font=_font(28), fill=(11, 18, 32))
        if i < len(layers) - 1:
            cx = w // 2
            d.polygon([(cx - 18, y + 138), (cx + 18, y + 138), (cx, y + 158)], fill=(248, 250, 252))
    img.save(path)
    return path


def make_demo_strip(path: Path) -> Path:
    steps = [
        ("1", "Lancer"),
        ("2", "Indexer"),
        ("3", "Rechercher"),
        ("4", "Comparer"),
        ("5", "Détail"),
    ]
    w, h = 1500, 200
    img = Image.new("RGB", (w, h), (11, 18, 32))
    d = ImageDraw.Draw(img)
    for i, (num, label) in enumerate(steps):
        x = 60 + i * 290
        d.ellipse((x, 40, x + 80, 120), fill=(14, 165, 233))
        d.text((x + 40, 80), num, font=_font(36), fill=(11, 18, 32), anchor="mm")
        d.text((x + 160, 80), label, font=_font(30), fill=(248, 250, 252), anchor="mm")
        if i < len(steps) - 1:
            d.rectangle((x + 220, 75, x + 270, 85), fill=(99, 102, 241))
    img.save(path)
    return path


def set_run(run, text, size=18, bold=False, color=WHITE):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"


def add_textbox(slide, left, top, width, height, text, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        set_run(run, line, size, bold, color)
    return box


def fill_shape(shape, color: RGBColor):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_bg(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    fill_shape(shape, NAVY)
    # send to back
    spTree = slide.shapes._spTree
    sp = shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def add_header(slide, title: str, subtitle: str = ""):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(1.05))
    fill_shape(bar, RGBColor(0x0F, 0x17, 0x2A))
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.05), SLIDE_W, Inches(0.08))
    fill_shape(accent, ACCENT_BAR)
    add_textbox(slide, Inches(0.5), Inches(0.22), Inches(12), Inches(0.55), title, size=28, bold=True)
    if subtitle:
        add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12), Inches(0.35), subtitle, size=14, color=MUTED)


def add_footer(slide, page: str):
    add_textbox(
        slide,
        Inches(8.5),
        Inches(7.05),
        Inches(4.5),
        Inches(0.35),
        f"Projet tutoré Master ISIE  |  {page}",
        size=11,
        color=MUTED,
        align=PP_ALIGN.RIGHT,
    )


def add_card(slide, left, top, width, height, color=CARD):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    fill_shape(shape, color)
    shape.adjustments[0] = 0.08
    return shape


def set_notes(slide, text: str):
    notes = slide.notes_slide
    notes.notes_text_frame.text = text


def add_bullets(slide, left, top, width, height, lines, size=15):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(6)
        if p.runs:
            set_run(p.runs[0], line, size=size, color=WHITE)
        else:
            r = p.add_run()
            set_run(r, line, size=size, color=WHITE)
    return box


def build_assets():
    icons = {
        "pdf": make_icon(ASSETS / "icon_pdf.png", "PDF", (220, 53, 69), "📄"),
        "docx": make_icon(ASSETS / "icon_docx.png", "Word", (46, 116, 181), "W"),
        "csv": make_icon(ASSETS / "icon_csv.png", "CSV", (40, 167, 69), "#"),
        "txt": make_icon(ASSETS / "icon_txt.png", "TXT", (108, 117, 125), "T"),
        "search": make_icon(ASSETS / "icon_search.png", "Search", (14, 165, 233), "⌕"),
        "hybrid": make_icon(ASSETS / "icon_hybrid.png", "Hybride", (99, 102, 241), "⇄"),
        "local": make_icon(ASSETS / "icon_local.png", "Local", (34, 197, 94), "⌂"),
    }
    # Prefer ASCII symbols if emoji renders poorly - remake without emoji for pdf
    icons["pdf"] = make_icon(ASSETS / "icon_pdf.png", "PDF", (220, 53, 69), "P")
    pipeline = make_pipeline_banner(ASSETS / "pipeline.png")
    arch = make_arch_diagram(ASSETS / "architecture.png")
    demo = make_demo_strip(ASSETS / "demo_steps.png")
    return icons, pipeline, arch, demo


def build():
    icons, pipeline, arch, demo = build_assets()
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    # ---------- SLIDE 1 Titre ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    if HERO.exists():
        s.shapes.add_picture(str(HERO), Inches(6.2), 0, width=Inches(7.2), height=SLIDE_H)
    panel = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(7.0), SLIDE_H)
    fill_shape(panel, NAVY)
    add_textbox(s, Inches(0.6), Inches(1.2), Inches(6.5), Inches(0.4), "PROJET TUTORÉ — MASTER ISIE", 14, False, TEAL)
    add_textbox(s, Inches(0.6), Inches(1.8), Inches(6.5), Inches(0.35), "thème:", 14, False, MUTED)
    add_textbox(
        s,
        Inches(0.6),
        Inches(2.2),
        Inches(6.8),
        Inches(1.4),
        "Indexation intelligente de données hétérogènes\npour la recherche d'information",
        28,
        True,
        WHITE,
    )
    add_textbox(
        s,
        Inches(0.6),
        Inches(3.9),
        Inches(6.5),
        Inches(0.5),
        "Master Ingénierie des Systèmes d'Information en Entreprise — IBAM",
        13,
        False,
        MUTED,
    )
    add_textbox(s, Inches(0.6), Inches(4.6), Inches(6.5), Inches(0.4), "Prototype : DocuSearch", 18, True, TEAL)
    add_textbox(s, Inches(0.6), Inches(5.3), Inches(6.5), Inches(0.4), "KOROGO Wendkuuni Ange Gaetan 1er Jumeau", 16, False, WHITE)
    if LOGO.exists():
        s.shapes.add_picture(str(LOGO), Inches(9.2), Inches(2.3), width=Inches(3.2))
    set_notes(
        s,
        "Bonjour. Je suis KOROGO Wendkuuni Ange Gaetan.\n"
        "Projet tutoré Master ISIE : indexation intelligente de données hétérogènes.\n"
        "Prototype : DocuSearch.",
    )

    # ---------- SLIDE 2 Plan ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "Plan de la présentation", "Déroulement de la présentation")
    plan = [
        ("01", "Contexte et problèmes terrains"),
        ("02", "Problématique et objectifs"),
        ("03", "État de l'art (2022–2026)"),
        ("04", "Solution proposée : DocuSearch"),
        ("05", "Architecture technique"),
        ("06", "Réalisations concrètes"),
        ("07", "Démonstration"),
        ("08", "Limites et perspectives"),
        ("09", "Conclusion"),
    ]
    for i, (num, label) in enumerate(plan):
        col = i % 3
        row = i // 3
        left = Inches(0.5 + col * 4.2)
        top = Inches(1.5 + row * 1.7)
        add_card(s, left, top, Inches(3.9), Inches(1.4))
        add_textbox(s, left + Inches(0.2), top + Inches(0.25), Inches(1), Inches(0.4), num, 22, True, TEAL)
        add_textbox(s, left + Inches(0.2), top + Inches(0.7), Inches(3.5), Inches(0.55), label, 14, False, WHITE)
    add_footer(s, "2/11")
    set_notes(
        s,
        "Je présenterai d’abord le contexte, les problèmes et les objectifs,\n"
        "Ensuite l'état de l'art,\n"
        "la solution que nous proposons,\n"
        "l'architecture que nous avons adoptée,\n"
        "les réalisations, puis une démonstration live,\n"
        "avant de terminer avec les limites les perspectives et la conclusion.",
    )

    # ---------- SLIDE 3 Contexte ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "1. Contexte et problèmes terrains")
    # format icons
    for i, key in enumerate(["pdf", "docx", "csv", "txt"]):
        s.shapes.add_picture(str(icons[key]), Inches(0.5 + i * 1.15), Inches(1.35), width=Inches(1.0))
    cols = [
        (
            "Contexte",
            [
                "•  École, ONG, PME, administration locale",
                "•  Documents dispersés dans plusieurs dossiers",
                "•  Formats variés : PDF, Word, CSV, TXT",
                "•  Pas de point d'accès unique",
                "•  Perte de temps à chercher l'information",
            ],
        ),
        (
            "Problèmes observés",
            [
                "•  Données hétérogènes difficiles à unifier",
                "•  Recherche manuelle et peu fiable",
                "•  Mise en page / tableaux souvent perdus",
                "•  Pas de tags ni d'enrichissement",
                "•  Outils cloud parfois inadaptés (coût, données locales)",
            ],
        ),
        (
            "Enjeu",
            [
                "•  Indexer intelligemment des formats différents",
                "•  Offrir une recherche pertinente",
                "•  Rester local, simple et démontrable",
                "•  Lier science (état de l'art) et réalisation",
            ],
        ),
    ]
    for i, (title, bullets) in enumerate(cols):
        left = Inches(0.4 + i * 4.25)
        add_card(s, left, Inches(2.55), Inches(4.05), Inches(4.1))
        accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(2.55), Inches(0.12), Inches(4.1))
        fill_shape(accent, [TEAL, AMBER, GREEN][i])
        add_textbox(s, left + Inches(0.3), Inches(2.7), Inches(3.5), Inches(0.4), title, 16, True, TEAL)
        add_bullets(s, left + Inches(0.25), Inches(3.2), Inches(3.6), Inches(3.2), bullets, size=13)
    add_footer(s, "3/11")
    set_notes(
        s,
        "Aujourd’hui, dans plusieurs structures — écoles, ONG, PME ou administrations — "
        "les documents sont dispersés et de formats différents : PDF, Word, CSV, texte, Excel, JSON…\n"
        "Sans outil central, la recherche reste manuelle et lente.\n"
        "L’enjeu est donc d’indexer intelligemment ces documents pour retrouver l’information rapidement, "
        "tout en restant local et simple.",
    )

    # ---------- SLIDE 4 Problématique ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "2. Problématique et objectifs", "Cadrage scientifique et technique")
    add_card(s, Inches(0.5), Inches(1.4), Inches(12.3), Inches(1.6))
    add_textbox(
        s,
        Inches(0.8),
        Inches(1.6),
        Inches(11.8),
        Inches(1.2),
        "Comment concevoir et implémenter un système local capable d'indexer automatiquement\n"
        "des données hétérogènes et d'offrir une recherche d'information pertinente\n"
        "via une interface web ?",
        16,
        True,
        WHITE,
    )
    add_card(s, Inches(0.5), Inches(3.3), Inches(6.0), Inches(3.3))
    add_textbox(s, Inches(0.75), Inches(3.45), Inches(5.5), Inches(0.4), "Objectifs généraux", 16, True, TEAL)
    add_bullets(
        s,
        Inches(0.75),
        Inches(3.95),
        Inches(5.5),
        Inches(2.5),
        [
            "•  Étudier l'état de l'art (15 articles, 2022–2026)",
            "•  Concevoir une architecture modulaire",
            "•  Réaliser un prototype fonctionnel",
            "•  Évaluer la pertinence sur un corpus de test",
            "•  Proposer des perspectives réalistes",
        ],
        14,
    )
    add_card(s, Inches(6.8), Inches(3.3), Inches(6.0), Inches(3.3))
    add_textbox(s, Inches(7.05), Inches(3.45), Inches(5.5), Inches(0.4), "Objectifs techniques", 16, True, TEAL)
    add_bullets(
        s,
        Inches(7.05),
        Inches(3.95),
        Inches(5.5),
        Inches(2.5),
        [
            "•  ≥ 4 formats : PDF, DOCX, CSV, TXT",
            "•  Indexation locale SQLite + Whoosh",
            "•  3 modes : mots-clés, sémantique, hybride",
            "•  API REST documentée (FastAPI / OpenAPI)",
            "•  Interface React moderne et démontrable",
        ],
        14,
    )
    add_footer(s, "4/11")
    set_notes(
        s,
        "Notre question centrale est simple : comment indexer automatiquement des documents de formats différents, "
        "et offrir une recherche pertinente, via une interface web locale ?\n"
        "Pour y répondre, quatre objectifs :\n"
        "maîtriser l’état de l’art,\n"
        "concevoir une architecture modulaire,\n"
        "réaliser un prototype fonctionnel,\n"
        "puis proposer des perspectives réalistes.",
    )

    # ---------- SLIDE 5 État de l'art ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "3. État de l'art (2022–2026)", "+ 15 articles")
    axes = [
        (
            "Fondements",
            [
                "•  Indexation annotative (Clarke)",
                "•  Données semi-structurées JSON",
                "•  DSI / NCI : index appris",
                "•  Survey GenIR (matching → génération)",
                "•  Idée : l'index n'est plus une simple table de mots",
            ],
            TEAL,
        ),
        (
            "Hybridation",
            [
                "•  ASI / GLEN : docids dynamiques",
                "•  HetaRAG : multi-moteurs",
                "•  ACORN : vecteurs + filtres",
                "•  DiscoverPath : graphes de connaissances",
                "•  Idée : combiner plusieurs signaux de pertinence",
            ],
            INDIGO,
        ),
        (
            "Pipeline RAG",
            [
                "•  Ingestion & parsing LLM",
                "•  ColPali / VisRAG : pages images",
                "•  Mix-of-Granularity : chunking",
                "•  Métadonnées enrichies",
                "•  Idée : la qualité amont conditionne tout",
            ],
            GREEN,
        ),
    ]
    for i, (title, bullets, color) in enumerate(axes):
        left = Inches(0.4 + i * 4.25)
        add_card(s, left, Inches(1.4), Inches(4.05), Inches(5.2))
        accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.4), Inches(0.12), Inches(5.2))
        fill_shape(accent, color)
        add_textbox(s, left + Inches(0.3), Inches(1.6), Inches(3.5), Inches(0.4), title, 18, True, color)
        add_bullets(s, left + Inches(0.25), Inches(2.2), Inches(3.6), Inches(4.0), bullets, 13)
    add_footer(s, "5/11")
    set_notes(
        s,
        "Pour l’état de l’art, nous avons analysé quinze articles récents, de 2022 à 2026.\n"
        "Nous les avons organisés autour de Trois axes : les fondements — comment indexer intelligemment ; "
        "l’hybridation — comment combiner plusieurs recherches ; et le pipeline RAG — comment bien préparer "
        "et enrichir les documents avant de chercher.\n\n"
        "Le constat commun : face à des documents de formats différents, un simple moteur de mots-clés ne suffit plus.\n"
        "De cette lecture, quatre idées se dégagent.\n"
        "Premièrement, on enrichit l’index : on ne stocke plus seulement des mots, mais aussi des informations utiles "
        "sur le document. Par exemple, Clarke parle d’un index annotatif.\n"
        "Deuxièmement, certains travaux vont plus loin : le modèle peut retrouver un document en générant directement "
        "son identifiant. C’est ce qu’on appelle la recherche générative, avec des approches comme DSI, NCI ou GenIR.\n"
        "Troisièmement, on combine plusieurs moteurs — mots exacts, sens du texte, relations entre informations — "
        "car une seule méthode n’est pas assez fiable.\n"
        "Quatrièmement, la qualité dépend de l’amont : bien lire les fichiers, les découper, les enrichir avec des "
        "métadonnées. Si cette étape est mauvaise, la recherche sera mauvaise.\n"
        "Pour notre contexte — local, avec des ressources limitées — nous retenons surtout trois points : lire plusieurs "
        "formats, enrichir les documents, et faire une recherche hybride légère.\n"
        "C’est exactement ce sur quoi nous avons travaillé dans notre prototype DocuSearch.",
    )

    # ---------- SLIDE 6 Solution ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "4. Solution proposée : DocuSearch", "Portail documentaire local intelligent")
    if LOGO.exists():
        s.shapes.add_picture(str(LOGO), Inches(11.5), Inches(0.15), width=Inches(1.3))
    s.shapes.add_picture(str(pipeline), Inches(0.6), Inches(1.35), width=Inches(12.1))
    bullets = [
        "▸  Un portail web local pour ingérer, indexer et rechercher des documents hétérogènes",
        "▸  Parcours complet : ingestion → extraction → enrichissement → indexation → recherche",
        "▸  Enrichissement intelligent : tags, résumé extractif, entités (dates, e-mails, orgs…)",
        "▸  Recherche multi-modes : mots-clés (Whoosh), sémantique (TF-IDF), hybride",
        "▸  Conçu pour un contexte à ressources limitées : pas de cloud obligatoire, pas de GPU",
        "▸  Lien direct avec la littérature : hybridation, métadonnées, qualité d'ingestion",
    ]
    add_card(s, Inches(0.5), Inches(2.9), Inches(12.3), Inches(3.6))
    add_bullets(s, Inches(0.8), Inches(3.15), Inches(11.7), Inches(3.2), bullets, 15)
    # tiny icons
    s.shapes.add_picture(str(icons["search"]), Inches(10.8), Inches(5.5), width=Inches(0.7))
    s.shapes.add_picture(str(icons["hybrid"]), Inches(11.6), Inches(5.5), width=Inches(0.7))
    s.shapes.add_picture(str(icons["local"]), Inches(12.4), Inches(5.5), width=Inches(0.7))
    add_footer(s, "6/11")
    set_notes(
        s,
        "La solution que nous proposons s’appelle DocuSearch.\n"
        "C’est un portail local qui suit un parcours clair : ingestion, extraction, enrichissement, indexation, puis recherche.\n"
        "On découvre les fichiers, on récupère leur contenu, on les enrichit avec résumé, tags et entités, puis on les indexe.\n"
        "Pour la recherche : trois modes — mots-clés, sémantique et hybride — adaptés à un contexte à ressources limitées",
    )

    # ---------- SLIDE 7 Architecture ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "5. Architecture technique", "Séparation claire des responsabilités")
    s.shapes.add_picture(str(arch), Inches(2.2), Inches(1.3), width=Inches(8.8))
    add_textbox(
        s,
        Inches(0.5),
        Inches(6.45),
        Inches(12.3),
        Inches(0.45),
        "Stack : Python 3.10+, FastAPI, Whoosh, scikit-learn, SQLite  |  Frontend React  |  Tests pytest (34+)  |  Déploiement local (port API 8010)",
        12,
        False,
        MUTED,
        PP_ALIGN.CENTER,
    )
    add_footer(s, "7/11")
    set_notes(
        s,
        "Quatre couches :\n"
        "1. Interface React\n"
        "2. API FastAPI\n"
        "3. Métier : ingestion, extraction, enrichissement, recherche\n"
        "4. Stockage : SQLite + Whoosh + fichiers locaux\n\n"
        "Cette séparation facilite tests, maintenance et démonstration.",
    )

    # ---------- SLIDE 8 Réalisations ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "6. Réalisations concrètes", "Ce que le prototype doit pouvoir faire")
    blocks = [
        (
            "Ingestion & extraction",
            [
                "•  Scan du dossier data/raw/",
                "•  Upload multi-formats",
                "•  PDF, DOCX, CSV, TXT",
                "•  Skip intelligent (hash contenu)",
                "•  Indexation Whoosh en batch",
                "•  Limite taille + noms uniques",
            ],
            icons["pdf"],
        ),
        (
            "Intelligence & recherche",
            [
                "•  Tags automatiques",
                "•  Résumé extractif",
                "•  Entités nommées",
                "•  Whoosh + boost titre/tags",
                "•  TF-IDF mis en cache",
                "•  Hybride 60% / 40% + highlights",
            ],
            icons["hybrid"],
        ),
        (
            "Interface & API",
            [
                "•  UI React modulaire",
                "•  Filtres type / tag",
                "•  Suppression de documents",
                "•  Rebuild index",
                "•  Health enrichi",
                "•  Messages d'erreur lisibles",
            ],
            icons["search"],
        ),
    ]
    for i, (title, bullets, icon) in enumerate(blocks):
        left = Inches(0.4 + i * 4.25)
        add_card(s, left, Inches(1.35), Inches(4.05), Inches(5.3))
        s.shapes.add_picture(str(icon), left + Inches(0.25), Inches(1.55), width=Inches(0.7))
        add_textbox(s, left + Inches(1.1), Inches(1.65), Inches(2.7), Inches(0.45), title, 15, True, TEAL)
        add_bullets(s, left + Inches(0.25), Inches(2.45), Inches(3.6), Inches(3.9), bullets, 13)
    add_footer(s, "8/11")
    set_notes(
        s,
        "Le prototype sait aujourd'hui :\n"
        "- ingérer PDF, DOCX, CSV, TXT ;\n"
        "- enrichir automatiquement les documents ;\n"
        "- rechercher en mots-clés, sémantique et hybride ;\n"
        "- filtrer, supprimer, reconstruire l'index.\n\n"
        "Je vais maintenant le montrer en live.",
    )

    # ---------- SLIDE 9 Démo ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "7. Démonstration — DocuSearch", "Scénario live")
    s.shapes.add_picture(str(demo), Inches(0.7), Inches(1.3), width=Inches(11.9))
    steps = [
        ("1. Lancer", "Ouvrir DocuSearch\nBadge API v0.5.0 vert"),
        ("2. Indexer", "Indexer le dossier\nou importer un fichier"),
        ("3. Rechercher", "Requête : « formation »\nMode Hybride"),
        ("4. Comparer", "Basculer Mots-clés\npuis Sémantique"),
        ("5. Détail", "Ouvrir un document\nRésumé · tags · entités"),
    ]
    for i, (title, body) in enumerate(steps):
        left = Inches(0.35 + i * 2.55)
        add_card(s, left, Inches(2.7), Inches(2.4), Inches(2.4))
        add_textbox(s, left + Inches(0.15), Inches(2.85), Inches(2.1), Inches(0.4), title, 13, True, TEAL)
        add_textbox(s, left + Inches(0.15), Inches(3.4), Inches(2.1), Inches(1.4), body, 12, False, WHITE)
    add_card(s, Inches(0.5), Inches(5.35), Inches(12.3), Inches(1.2))
    add_textbox(s, Inches(0.7), Inches(5.45), Inches(11.9), Inches(0.3), "Message à faire passer", 12, True, AMBER)
    add_textbox(
        s,
        Inches(0.7),
        Inches(5.8),
        Inches(11.9),
        Inches(0.6),
        "DocuSearch unifie des formats différents, enrichit automatiquement les documents "
        "et permet de comparer trois modes de recherche en conditions réelles.",
        13,
        False,
        WHITE,
    )
    add_footer(s, "9/11")
    set_notes(
        s,
        "Scénario live :\n"
        "1. Badge API vert (v0.5.0)\n"
        "2. Indexer le dossier ou importer un fichier\n"
        "3. Recherche « formation » en mode Hybride\n"
        "4. Comparer rapidement Mots-clés puis Sémantique\n"
        "5. Ouvrir un document : résumé, tags, entités\n\n"
        "Message : DocuSearch unifie des formats hétérogènes et offre une recherche intelligente, utilisable tout de suite.\n\n"
        "Plan B : si l'application ne répond pas, montrer les captures préparées.",
    )

    # ---------- SLIDE 10 Limites ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "7. Limites et perspectives", "Transparence scientifique + feuille de route")
    add_card(s, Inches(0.5), Inches(1.4), Inches(6.0), Inches(5.1))
    accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.4), Inches(0.12), Inches(5.1))
    fill_shape(accent, AMBER)
    add_textbox(s, Inches(0.85), Inches(1.6), Inches(5.4), Inches(0.4), "Limites", 18, True, AMBER)
    add_bullets(
        s,
        Inches(0.85),
        Inches(2.2),
        Inches(5.4),
        Inches(4.0),
        [
            "•  Sémantique = TF-IDF (pas d'embeddings lourds)",
            "•  Pas d'auth multi-utilisateurs ni cloud",
            "•  Pas d'indexation visuelle type ColPali",
            "•  Volumes ciblés : dizaines/centaines de docs",
            "•  Certains articles d'état de l'art restent hors MVP",
        ],
        14,
    )
    add_card(s, Inches(6.8), Inches(1.4), Inches(6.0), Inches(5.1))
    accent2 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.4), Inches(0.12), Inches(5.1))
    fill_shape(accent2, GREEN)
    add_textbox(s, Inches(7.15), Inches(1.6), Inches(5.4), Inches(0.4), "Perspectives", 18, True, GREEN)
    add_bullets(
        s,
        Inches(7.15),
        Inches(2.2),
        Inches(5.4),
        Inches(4.0),
        [
            "•  Hybridation plus fine + reranking",
            "•  Enrichissement métadonnées plus riche",
            "•  Ingestion adaptative (OCR / PDF scannés)",
            "•  Module RAG pour réponses sourcées",
            "•  Déploiement cloud progressif si besoin",
        ],
        14,
    )
    add_footer(s, "10/11")
    set_notes(
        s,
        "Limites\n"
        "La recherche sémantique reste légère : elle repose sur TF-IDF, une pondération classique où un terme est "
        "important s’il est fréquent dans un document (TF) mais rare dans le corpus (IDF). Ce n’est pas une approche "
        "par embeddings neuronaux.\n"
        "La solution ne gère pas encore l’authentification multi-utilisateurs, reste volontairement local (pas de cloud), "
        "et cible des volumes encore modestes.\n\n"
        "Perspectives\n"
        "Les suites possibles sont réalistes :\n"
        "affiner la recherche hybride,\n"
        "enrichir davantage les métadonnées,\n"
        "ajouter l’OCR (Reconnaissance Optique par Caractères) pour les PDF scannés, puis un module RAG pour générer "
        "des réponses sourcées à partir des documents retrouvés.\n"
        "Un déploiement cloud pourra être envisagé plus tard, si le besoin organisationnel l’exige",
    )

    # ---------- SLIDE 11 Conclusion ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    add_header(s, "8. Conclusion")
    if LOGO.exists():
        s.shapes.add_picture(str(LOGO), Inches(11.5), Inches(0.15), width=Inches(1.3))
    add_card(s, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.2))
    add_textbox(
        s,
        Inches(1.2),
        Inches(1.9),
        Inches(11.0),
        Inches(3.2),
        "Ce projet tutoré a permis de relier un problème concret à une réponse technique démontrable.\n\n"
        "À partir d'une revue de littérature récente (2022–2026), nous avons pensé à la conception et à la réalisation "
        "de DocuSearch : un portail local capable d'ingérer, d'indexer et de rechercher des documents hétérogènes avec "
        "des modes mots-clés, sémantique et hybride. Le travail montre qu'une indexation intelligente reste accessible "
        "dans un contexte à ressources limitées, tout en ouvrant des perspectives claires : métadonnées enrichies, "
        "hybridation plus fine et module RAG.\n\n"
        "Merci de votre attention.",
        15,
        False,
        WHITE,
    )
    add_footer(s, "11/11")
    set_notes(
        s,
        "Ce projet relie un problème concret à une solution démontrable.\n"
        "À partir de la littérature récente, Nous avons conçu DocuSearch pour indexer et rechercher des documents "
        "hétérogènes en local.\n"
        "L'indexation intelligente est accessible même avec des ressources limitées.\n\n"
        "Merci de votre attention. Je suis prêt pour vos questions.",
    )

    prs.save(str(OUT))
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    build()
