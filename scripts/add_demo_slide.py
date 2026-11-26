"""
Ajoute une slide Démonstration à PRESENTATION_KOROGO_W_Ange_Gaetan.pptx
et met à jour le plan + notes.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

PPTX = Path(__file__).resolve().parent.parent / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan.pptx"
OUTPUT = Path(__file__).resolve().parent.parent / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan_AVEC_DEMO.pptx"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
ACCENT = RGBColor(0xC2, 0x41, 0x0C)
DARK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xE2, 0xE8, 0xF0)


def set_run(p, text, *, size=18, bold=False, color=DARK):
    run = p.add_run()
    run.text = text
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def clear_shapes(slide):
    sp_tree = slide.shapes._spTree
    for shape in list(slide.shapes):
        sp_tree.remove(shape._element)


def add_bg(slide, color):
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    sp_tree = slide.shapes._spTree
    sp = bg._element
    sp_tree.remove(sp)
    sp_tree.insert(2, sp)


def set_notes(slide, text: str) -> None:
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text.strip()
    run.font.name = "Calibri"
    run.font.size = Pt(12)


def move_slide(prs: Presentation, old_index: int, new_index: int) -> None:
    sld_id_lst = prs.slides._sldIdLst
    slides = list(sld_id_lst)
    el = slides[old_index]
    sld_id_lst.remove(el)
    sld_id_lst.insert(new_index, el)


def rebuild_plan(slide) -> None:
    clear_shapes(slide)
    add_bg(slide, LIGHT)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    set_run(bar.text_frame.paragraphs[0], "  Plan de la présentation", size=26, bold=True, color=WHITE)

    sub = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.05), Inches(13.333), Inches(0.38)
    )
    sub.fill.solid()
    sub.fill.fore_color.rgb = TEAL
    sub.line.fill.background()
    set_run(sub.text_frame.paragraphs[0], "   Déroulement de la présentation", size=12, color=WHITE)

    plan_items = [
        ("01", "Contexte et problématique terrain"),
        ("02", "Problématique et objectifs"),
        ("03", "État de l'art (2022–2026)"),
        ("04", "Solution proposée : DocuSearch"),
        ("05", "Architecture technique"),
        ("06", "Réalisations concrètes"),
        ("07", "Démonstration"),
        ("08", "Limites et perspectives"),
        ("09", "Conclusion"),
    ]

    for i, (num, title) in enumerate(plan_items):
        col = 0 if i < 5 else 1
        row = i if i < 5 else i - 5
        left = 0.7 + col * 6.2
        top = 1.65 + row * 0.95
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(5.8), Inches(0.82)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD
        card.line.color.rgb = SOFT
        accent = TEAL if num != "07" else ACCENT
        stripe = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.12), Inches(0.82)
        )
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = accent
        stripe.line.fill.background()

        num_box = slide.shapes.add_textbox(
            Inches(left + 0.28), Inches(top + 0.2), Inches(0.7), Inches(0.4)
        )
        set_run(num_box.text_frame.paragraphs[0], num, size=18, bold=True, color=accent)
        title_box = slide.shapes.add_textbox(
            Inches(left + 1.05), Inches(top + 0.22), Inches(4.5), Inches(0.4)
        )
        set_run(title_box.text_frame.paragraphs[0], title, size=15, bold=True, color=DARK)

    foot = slide.shapes.add_textbox(Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3))
    p = foot.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    set_run(p, "Projet tutoré Master ISIE  |  2/11", size=11, color=GRAY)


def build_demo_slide(slide) -> None:
    clear_shapes(slide)
    add_bg(slide, LIGHT)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    set_run(bar.text_frame.paragraphs[0], "  7. Démonstration — DocuSearch", size=26, bold=True, color=WHITE)

    sub = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.05), Inches(13.333), Inches(0.38)
    )
    sub.fill.solid()
    sub.fill.fore_color.rgb = ACCENT
    sub.line.fill.background()
    set_run(sub.text_frame.paragraphs[0], "   Scénario live (≈ 90 secondes)", size=12, color=WHITE)

    steps = [
        ("1", "Lancer", "Ouvrir DocuSearch\nBadge API v0.5.0 vert"),
        ("2", "Indexer", "Indexer le dossier\nou importer un fichier"),
        ("3", "Rechercher", "Requête : « formation »\nMode Hybride"),
        ("4", "Comparer", "Basculer Mots-clés\npuis Sémantique"),
        ("5", "Détail", "Ouvrir un document\nRésumé · tags · entités"),
    ]

    for i, (num, title, body) in enumerate(steps):
        left = 0.45 + i * 2.55
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.8), Inches(2.4), Inches(3.6)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD
        card.line.color.rgb = SOFT

        top = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.8), Inches(2.4), Inches(0.85)
        )
        top.fill.solid()
        top.fill.fore_color.rgb = TEAL if i % 2 == 0 else NAVY
        top.line.fill.background()
        p = top.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        set_run(p, f"{num}. {title}", size=15, bold=True, color=WHITE)

        body_box = slide.shapes.add_textbox(
            Inches(left + 0.15), Inches(2.9), Inches(2.1), Inches(2.2)
        )
        tf = body_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        set_run(p, body, size=13, color=DARK)

        if i < 4:
            arrow = slide.shapes.add_textbox(
                Inches(left + 2.25), Inches(3.3), Inches(0.35), Inches(0.4)
            )
            set_run(arrow.text_frame.paragraphs[0], "→", size=18, bold=True, color=TEAL)

    note = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(5.65), Inches(12.4), Inches(1.15)
    )
    note.fill.solid()
    note.fill.fore_color.rgb = WHITE
    note.line.color.rgb = SOFT
    tf = note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p, "Message à faire passer", size=13, bold=True, color=ACCENT)
    p = tf.add_paragraph()
    p.space_before = Pt(4)
    set_run(
        p,
        "DocuSearch unifie des formats différents, enrichit automatiquement les documents "
        "et permet de comparer trois modes de recherche en conditions réelles.",
        size=14,
        color=DARK,
    )

    foot = slide.shapes.add_textbox(Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3))
    p = foot.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    set_run(p, "Projet tutoré Master ISIE  |  9/11", size=11, color=GRAY)

    set_notes(
        slide,
        """[1 min 30]

Je passe maintenant à la démonstration.

1. L'application est lancée : le badge API est vert.
2. J'indexe le dossier (ou j'importe un fichier).
3. Je recherche « formation » en mode hybride.
4. Je compare rapidement avec mots-clés puis sémantique.
5. J'ouvre un document : résumé, tags et entités.

Ce que cela montre : DocuSearch traite des formats hétérogènes et offre une recherche intelligente, directement utilisable.""",
    )


def update_footers(prs: Presentation) -> None:
    total = len(prs.slides)
    for i, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = shape.text_frame.text
            if "|  " in text and ("Master ISIE" in text or "Master ISI" in text or "DocuSearch" in text):
                # Replace page numbers like 5/10 or 9/11
                import re

                new_text = re.sub(r"\b\d+\s*/\s*\d+\b", f"{i}/{total}", text)
                if new_text != text and len(shape.text_frame.paragraphs) == 1:
                    p = shape.text_frame.paragraphs[0]
                    # Keep style of first run if any
                    if p.runs:
                        p.runs[0].text = new_text
                        for extra in p.runs[1:]:
                            extra.text = ""
                    else:
                        set_run(p, new_text, size=11, color=GRAY)


def main() -> None:
    prs = Presentation(str(PPTX))

    # Rebuild plan with Démonstration
    rebuild_plan(prs.slides[1])
    set_notes(
        prs.slides[1],
        """[15 s]

Voici le plan. Après le contexte, les objectifs, l'état de l'art, la solution et l'architecture, je montrerai les réalisations puis une démonstration live de DocuSearch, avant les limites et la conclusion.""",
    )

    # Create demo slide at end then move after réalisations (index 8)
    blank = prs.slide_layouts[6]
    demo = prs.slides.add_slide(blank)
    build_demo_slide(demo)
    move_slide(prs, len(prs.slides) - 1, 8)

    # Light footer refresh where simple
    update_footers(prs)

    # Ensure demo notes remain after move
    set_notes(
        prs.slides[8],
        """[1 min 30]

Je passe maintenant à la démonstration.

1. L'application est lancée : le badge API est vert.
2. J'indexe le dossier (ou j'importe un fichier).
3. Je recherche « formation » en mode hybride.
4. Je compare rapidement avec mots-clés puis sémantique.
5. J'ouvre un document : résumé, tags et entités.

Ce que cela montre : DocuSearch traite des formats hétérogènes et offre une recherche intelligente, directement utilisable.

Plan B si l'app plante : montrer des captures préparées.""",
    )

    try:
        prs.save(str(PPTX))
        target = PPTX
    except PermissionError:
        prs.save(str(OUTPUT))
        target = OUTPUT
        print(f"Fichier verrouillé, sauvegarde alternative : {OUTPUT}")

    print(f"Demo ajoutée : {target} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
