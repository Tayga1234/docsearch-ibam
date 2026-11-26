"""Met à jour la diapo État de l'art avec un texte plus clair."""
from pathlib import Path

from pptx import Presentation
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan_AVEC_DEMO_NOTES.pptx"
ALSO = [
    ROOT / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan_AVEC_DEMO.pptx",
    ROOT / "travaux" / "PRESENTATION_KOROGO_W_Ange_Gaetan.pptx",
]

SUBTITLE = "15 articles (2022–2026)  ·  3 idées clés  ·  lien direct avec DocuSearch"

COL_TITLES = [
    "1. Mieux indexer",
    "2. Combiner les moteurs",
    "3. Soigner l’amont",
]

COL_BODIES = [
    [
        "•  On n’indexe plus seulement des mots",
        "•  Formats très variés (texte, JSON…)",
        "•  Nouveaux index « appris » (GenIR)",
        "•  Ex. : Clarke, DSI, NCI",
        "→ L’index devient plus intelligent",
    ],
    [
        "•  Un seul moteur ne suffit plus",
        "•  Mots-clés + sens + structure",
        "•  Chaque requête a un signal utile",
        "•  Ex. : HetaRAG, recherche hybride",
        "→ Combiner plusieurs pertinences",
    ],
    [
        "•  Bien extraire le contenu des fichiers",
        "•  Découper les documents (chunks)",
        "•  Ajouter tags / métadonnées",
        "•  Ex. : ingestion, OCR, enrichissement",
        "→ La qualité amont conditionne tout",
    ],
]


def replace_paragraphs(shape, lines, font_size=13, bold=False):
    tf = shape.text_frame
    existing = list(tf.paragraphs)

    for i, line in enumerate(lines):
        if i < len(existing):
            p = existing[i]
            if not p.runs:
                run = p.add_run()
            else:
                run = p.runs[0]
                for rr in p.runs[1:]:
                    rr.text = ""
            run.text = line
            run.font.size = Pt(font_size)
            run.font.bold = bold
        else:
            p = tf.add_paragraph()
            run = p.add_run()
            run.text = line
            run.font.size = Pt(font_size)
            run.font.bold = bold

    for i in range(len(lines), len(existing)):
        for r in existing[i].runs:
            r.text = ""


def update_file(path: Path, out: Path | None = None) -> Path:
    prs = Presentation(str(path))
    slide = prs.slides[4]
    shapes = list(slide.shapes)
    # Indices connus (diapo 3 colonnes)
    replace_paragraphs(shapes[2], [SUBTITLE], font_size=13, bold=False)
    replace_paragraphs(shapes[5], [COL_TITLES[0]], font_size=16, bold=True)
    replace_paragraphs(shapes[6], COL_BODIES[0], font_size=12, bold=False)
    replace_paragraphs(shapes[9], [COL_TITLES[1]], font_size=14, bold=True)
    replace_paragraphs(shapes[10], COL_BODIES[1], font_size=12, bold=False)
    replace_paragraphs(shapes[13], [COL_TITLES[2]], font_size=15, bold=True)
    replace_paragraphs(shapes[14], COL_BODIES[2], font_size=12, bold=False)
    dest = out or path
    prs.save(str(dest))
    print(f"OK {dest.name}")
    return dest


def main():
    out = TARGET.with_name("PRESENTATION_KOROGO_ETAT_ART_CLAIR.pptx")
    saved = update_file(TARGET, out)

    # Vérification
    prs = Presentation(str(saved))
    slide = prs.slides[4]
    print("\n=== VÉRIFICATION SLIDE 5 ===")
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text.strip():
            print(shape.text_frame.text)
            print("---")


if __name__ == "__main__":
    main()
