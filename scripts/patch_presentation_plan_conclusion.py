"""Patch PRESENTATION_PROJET_TUTORE.pptx : plan (slide 2) + conclusion."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

PATH = Path(__file__).resolve().parent.parent / "travaux" / "PRESENTATION_PROJET_TUTORE.pptx"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
DARK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xE2, 0xE8, 0xF0)
MUTED = RGBColor(0xCB, 0xD5, 0xE1)
MINT = RGBColor(0x99, 0xF6, 0xE4)


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


def build_plan(slide):
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
    set_run(sub.text_frame.paragraphs[0], "   Déroulement de l'exposé", size=12, color=WHITE)

    plan_items = [
        ("01", "Contexte et problématique terrain"),
        ("02", "Problématique et objectifs"),
        ("03", "État de l'art (2022–2026)"),
        ("04", "Solution proposée : DocuSearch"),
        ("05", "Architecture technique"),
        ("06", "Réalisations concrètes"),
        ("07", "Limites et perspectives"),
        ("08", "Conclusion"),
    ]

    for i, (num, title) in enumerate(plan_items):
        col = i // 4
        row = i % 4
        left = 0.7 + col * 6.2
        top = 1.7 + row * 1.2
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(5.8), Inches(1.0)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD
        card.line.color.rgb = SOFT

        stripe = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.12), Inches(1.0)
        )
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = TEAL
        stripe.line.fill.background()

        num_box = slide.shapes.add_textbox(
            Inches(left + 0.3), Inches(top + 0.28), Inches(0.7), Inches(0.45)
        )
        set_run(num_box.text_frame.paragraphs[0], num, size=20, bold=True, color=TEAL)

        title_box = slide.shapes.add_textbox(
            Inches(left + 1.1), Inches(top + 0.3), Inches(4.4), Inches(0.45)
        )
        set_run(title_box.text_frame.paragraphs[0], title, size=16, bold=True, color=DARK)

    foot = slide.shapes.add_textbox(Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3))
    p = foot.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    set_run(p, "Projet tutoré Master ISIE  |  2/10", size=11, color=GRAY)


def build_conclusion(slide):
    clear_shapes(slide)
    add_bg(slide, NAVY)

    band = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.18), Inches(7.5)
    )
    band.fill.solid()
    band.fill.fore_color.rgb = TEAL
    band.line.fill.background()

    box = slide.shapes.add_textbox(Inches(1.0), Inches(1.15), Inches(11.3), Inches(5.4))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    set_run(p, "Conclusion", size=18, color=SOFT)

    p = tf.add_paragraph()
    p.space_before = Pt(16)
    set_run(
        p,
        "Ce projet tutoré a permis de relier un problème concret\n"
        "à une réponse technique démontrable.",
        size=24,
        bold=True,
        color=WHITE,
    )

    p = tf.add_paragraph()
    p.space_before = Pt(22)
    set_run(
        p,
        "À partir d'une revue de littérature récente (2022–2026),\n"
        "nous avons conçu et réalisé DocuSearch : un portail local capable\n"
        "d'ingérer, d'indexer et de rechercher des documents hétérogènes\n"
        "avec des modes mots-clés, sémantique et hybride.",
        size=16,
        color=MUTED,
    )

    p = tf.add_paragraph()
    p.space_before = Pt(18)
    set_run(
        p,
        "Le travail montre qu'une indexation intelligente reste accessible\n"
        "dans un contexte à ressources limitées, tout en ouvrant des perspectives\n"
        "claires : métadonnées enrichies, hybridation plus fine et module RAG.",
        size=16,
        color=MUTED,
    )

    p = tf.add_paragraph()
    p.space_before = Pt(28)
    set_run(p, "Merci de votre attention.", size=20, bold=True, color=MINT)

    p = tf.add_paragraph()
    p.space_before = Pt(8)
    set_run(p, "Je reste disponible pour vos questions.", size=16, color=SOFT)

    foot = slide.shapes.add_textbox(Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3))
    p = foot.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    set_run(p, "Projet tutoré Master ISIE  |  10/10", size=11, color=SOFT)


def main():
    prs = Presentation(str(PATH))
    build_plan(prs.slides[1])
    build_conclusion(prs.slides[9])
    prs.save(str(PATH))
    print(f"Mis à jour : {PATH}")


if __name__ == "__main__":
    main()
