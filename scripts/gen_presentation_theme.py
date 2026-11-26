"""
Génère la présentation PowerPoint pour convaincre le jury
de valider le thème de projet tutoré / soutenance.

Usage :
    .venv\\Scripts\\python.exe scripts\\gen_presentation_theme.py
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT_ROOT / "travaux" / "PRESENTATION_VALIDATION_THEME.pptx"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT = RGBColor(0x2E, 0x7D, 0x4F)
DARK = RGBColor(0x22, 0x22, 0x22)
GRAY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF4, 0xF6, 0xF8)


def _set_run(run, *, size=18, bold=False, color=DARK, font="Calibri"):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def _add_bg(slide, color: RGBColor):
    fill = slide.shapes.add_shape(
        1,  # rectangle
        Inches(0),
        Inches(0),
        Inches(13.333),
        Inches(7.5),
    )
    fill.fill.solid()
    fill.fill.fore_color.rgb = color
    fill.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = fill._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def _title_bar(slide, text: str):
    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = "  " + text
    _set_run(run, size=28, bold=True, color=WHITE)


def _bullets(slide, items: list[str], *, top=1.5, left=0.7, width=12, size=20):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.5))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(12)
        run = p.add_run()
        run.text = "•  " + item
        _set_run(run, size=size, color=DARK)


def _footer(slide, page: int, total: int = 10):
    box = slide.shapes.add_textbox(Inches(0.5), Inches(7.05), Inches(12.3), Inches(0.35))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f"Validation du thème — Master ISI  |  {page}/{total}"
    _set_run(run, size=11, color=GRAY)


def build() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = 10

    # 1. Titre
    s = prs.slides.add_slide(blank)
    _add_bg(s, NAVY)
    box = s.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.7), Inches(3.5))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Validation du thème de projet tutoré"
    _set_run(r, size=22, color=RGBColor(0xB8, 0xC7, 0xD9))

    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(18)
    r = p.add_run()
    r.text = "Indexation intelligente de données hétérogènes\npour la recherche d'information"
    _set_run(r, size=32, bold=True, color=WHITE)

    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(28)
    r = p.add_run()
    r.text = "Master Ingénierie des Systèmes d'Information en Entreprise\nPrésentation devant jury — demande de poursuite du thème"
    _set_run(r, size=16, color=RGBColor(0xD0, 0xD8, 0xE0))
    _footer(s, 1, total)

    # 2. Objectif de la présentation
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Objectif de cette présentation")
    _bullets(
        s,
        [
            "Convaincre le jury de valider la poursuite de ce thème",
            "Montrer que le sujet est pertinent, faisable et déjà engagé",
            "Présenter la problématique, l'état d'avancement et le plan de travail",
            "Obtenir un avis favorable pour continuer jusqu'à la soutenance",
        ],
        size=22,
    )
    _footer(s, 2, total)

    # 3. Thème proposé
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Thème proposé")
    box = s.shapes.add_shape(1, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = NAVY
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Indexation intelligente de données hétérogènes\npour la recherche d'information"
    _set_run(r, size=24, bold=True, color=NAVY)

    _bullets(
        s,
        [
            "Problème réel : documents dispersés, formats variés (PDF, Word, CSV, TXT, JSON…)",
            "Besoin : un point d'accès unique pour retrouver l'information rapidement",
            "Réponse : pipeline ingestion → extraction → indexation → recherche",
            "Application : portail local DocuSearch BF (prototype déjà en cours)",
        ],
        top=3.7,
        size=18,
    )
    _footer(s, 3, total)

    # 4. Pourquoi ce thème
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Pourquoi ce thème ?")
    _bullets(
        s,
        [
            "Pertinence scientifique : domaine actif (2022–2026) — GenIR, RAG, hybridation",
            "Pertinence pratique : besoin concret des petites structures (école, ONG, PME, admin)",
            "Alignement Master ISI : architecture SI, données, recherche d'information, prototype",
            "Faisabilité : périmètre clair, technologies maîtrisables en local (Python, FastAPI, React)",
            "Originalité raisonnable : indexation intelligente adaptée à un contexte à ressources limitées",
        ],
        size=19,
    )
    _footer(s, 4, total)

    # 5. Problématique
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Problématique")
    box = s.shapes.add_shape(1, Inches(0.8), Inches(2.0), Inches(11.7), Inches(2.2))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = ACCENT
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = (
        "Comment concevoir et implémenter un système local capable\n"
        "d'indexer automatiquement des données hétérogènes\n"
        "et d'offrir une recherche d'information pertinente ?"
    )
    _set_run(r, size=22, bold=True, color=NAVY)

    _bullets(
        s,
        [
            "Sous-questions : extraction multi-formats, structure d'index, modes de recherche, enrichissement",
            "Objectif : un prototype évaluable, documenté et démontrable devant jury",
        ],
        top=4.6,
        size=18,
    )
    _footer(s, 5, total)

    # 6. Ce qui est déjà fait
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Ce qui est déjà avancé")
    _bullets(
        s,
        [
            "Revue de littérature : 15 articles scientifiques (2022–2026), 5 par jour × 3 jours",
            "Synthèses rédigées : résumé général, introduction, corps, conclusion et perspectives",
            "Cahier des charges et architecture technique définis",
            "Prototype DocuSearch BF : ingestion, indexation, recherche (mots-clés / sémantique / hybride)",
            "Interface web React + API FastAPI + tests automatisés",
        ],
        size=19,
    )
    note = s.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.5), Inches(0.5))
    p = note.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "→ Le thème n'est pas une idée floue : un travail concret est déjà engagé."
    _set_run(r, size=16, bold=True, color=ACCENT)
    _footer(s, 6, total)

    # 7. Plan de poursuite
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Plan de poursuite si le thème est validé")
    _bullets(
        s,
        [
            "Finaliser et peaufiner le prototype (démo stable, corpus de test)",
            "Évaluer la pertinence des résultats (mots-clés vs sémantique vs hybride)",
            "Rédiger le rapport de projet (conception, réalisation, tests, limites)",
            "Préparer la soutenance : slides, captures d'écran, scénario de démonstration",
            "Proposer des perspectives réalistes : métadonnées, hybridation légère, module RAG",
        ],
        size=19,
    )
    _footer(s, 7, total)

    # 8. Risques et maîtrise
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Risques identifiés et maîtrise")
    _bullets(
        s,
        [
            "Risque technique : trop viser l'état de l'art (DSI, vision-langage) → rester sur un MVP local",
            "Risque de périmètre : trop de formats / fonctionnalités → prioriser PDF, DOCX, CSV, TXT",
            "Risque temps : rapport + démo → s'appuyer sur l'existant déjà construit",
            "Risque scientifique : sujet trop large → cadrer sur indexation + recherche pour données hétérogènes",
        ],
        size=19,
    )
    _footer(s, 8, total)

    # 9. Arguments pour le jury
    s = prs.slides.add_slide(blank)
    _add_bg(s, LIGHT)
    _title_bar(s, "Pourquoi valider ce thème ?")
    _bullets(
        s,
        [
            "Sujet clair, actuel et utile",
            "Lien fort entre littérature scientifique et réalisation logicielle",
            "Travail déjà engagé : littérature + prototype + documentation",
            "Périmètre réaliste pour un projet tutoré Master ISI",
            "Démonstration possible devant jury (application concrète)",
            "Perspectives d'évolution crédibles sans promesse irréaliste",
        ],
        size=20,
    )
    _footer(s, 9, total)

    # 10. Demande
    s = prs.slides.add_slide(blank)
    _add_bg(s, NAVY)
    box = s.shapes.add_textbox(Inches(1), Inches(2.0), Inches(11.3), Inches(3.5))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Demande au jury"
    _set_run(r, size=22, color=RGBColor(0xB8, 0xC7, 0xD9))

    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(20)
    r = p.add_run()
    r.text = (
        "Nous sollicitons la validation de ce thème\n"
        "afin de poursuivre le projet jusqu'à la soutenance."
    )
    _set_run(r, size=28, bold=True, color=WHITE)

    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(28)
    r = p.add_run()
    r.text = "Merci de votre attention — questions ?"
    _set_run(r, size=18, color=RGBColor(0xD0, 0xD8, 0xE0))
    _footer(s, 10, total)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(f"Présentation générée : {path}")
