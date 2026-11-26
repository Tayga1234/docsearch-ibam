"""
Génère le mémoire Word selon le canevas IBAM (V1.0, 26/09/2024).

Usage :
    .venv\\Scripts\\python.exe scripts\\build_memoire_ibam.py
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
CORPS = ROOT / "rapport" / "memoire_corps.md"
FIGURES = ROOT / "rapport" / "figures"
OUTPUT = ROOT / "rapport" / "MEMOIRE_KOROGO_Indexation_intelligente.docx"

NAVY = RGBColor(0x1A, 0x36, 0x5D)
AUTEUR = "KOROGO Wendkuuni Ange Gaëtan 1er (Jumeau)"
AUTEUR_COURT = "KOROGO Wendkuuni Ange Gaëtan"
TITRE = "Indexation intelligente de données pour la recherche d’information"
OPTION = "Ingénierie des Systèmes d’Information en Entreprise (ISIE)"
DIRECTEUR = "[Nom et prénoms du directeur de mémoire à compléter]"


def set_run_font(run, name: str = "Times New Roman", size: int = 12, bold: bool = False, italic: bool = False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_page_number(paragraph):
    run = paragraph.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    set_run_font(run, size=10)


def configure_section(document: Document) -> None:
    section = document.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = header.add_run("IBAM  —  Mémoire de Master informatique  —  " + AUTEUR_COURT)
    set_run_font(r, size=9, italic=True, color=RGBColor(0x55, 0x55, 0x55))
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(footer)


def style_base(document: Document) -> None:
    normal = document.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal.paragraph_format.space_after = Pt(10)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for i, size in ((1, 16), (2, 14), (3, 12)):
        h = document.styles[f"Heading {i}"]
        h.font.name = "Times New Roman"
        h.font.color.rgb = NAVY
        h.font.size = Pt(size)
        h.font.bold = True
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(8)
        h.paragraph_format.line_spacing = 1.15


def p(document: Document, text: str, *, size=12, bold=False, italic=False, align=None, space_after=8, first_line=True):
    para = document.add_paragraph()
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    para.paragraph_format.space_after = Pt(space_after)
    para.alignment = align or WD_ALIGN_PARAGRAPH.JUSTIFY
    if first_line and align is None:
        para.paragraph_format.first_line_indent = Cm(1.25)
    run = para.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return para


def centered(document: Document, text: str, *, size=12, bold=False, italic=False, space_after=6):
    return p(document, text, size=size, bold=bold, italic=italic, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=space_after, first_line=False)


def shade_paragraph(paragraph, fill: str = "F2F4F7") -> None:
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def add_code_block(document: Document, lines: list[str]) -> None:
    cleaned = list(lines)
    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    if not cleaned:
        return
    for idx, line in enumerate(cleaned):
        para = document.add_paragraph()
        para.paragraph_format.first_line_indent = Cm(0)
        para.paragraph_format.left_indent = Cm(0.35)
        para.paragraph_format.space_before = Pt(6 if idx == 0 else 0)
        para.paragraph_format.space_after = Pt(10 if idx == len(cleaned) - 1 else 0)
        para.paragraph_format.line_spacing = 1.08
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        shade_paragraph(para)
        run = para.add_run(line.replace("\t", "    ") if line else " ")
        set_run_font(run, name="Consolas", size=9, color=NAVY)
        text_el = run._r.find(qn("w:t"))
        if text_el is not None:
            text_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


def add_formatted_runs(paragraph, text: str, size: int = 12) -> None:
    pattern = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")
    for part in pattern.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_run_font(run, size=size, bold=True)
        elif part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, size=size, italic=True)
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, name="Consolas", size=10)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, size=size)


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and "|" in s[1:-1]


def parse_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells if c)


def add_cadre(document: Document, title: str, hint: str, height_in: float = 4.6) -> None:
    """Zone réservée : l'étudiant colle ensuite une capture ou un schéma."""
    from PIL import Image, ImageDraw, ImageFont

    FIGURES.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", title)[:50].strip("_") or "cadre"
    path = FIGURES / f"cadre_{safe}.png"
    w, h = 1600, int(620 * height_in / 3.5)
    img = Image.new("RGB", (w, h), (247, 249, 252))
    draw = ImageDraw.Draw(img)
    draw.rectangle((12, 12, w - 13, h - 13), outline=(26, 54, 93), width=4)
    draw.rectangle((28, 28, w - 29, h - 29), outline=(47, 111, 176), width=2)
    try:
        f_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
        f_body = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    except OSError:
        f_title = ImageFont.load_default()
        f_body = f_title
    label = "À COMPLÉTER PAR L’ÉTUDIANT"
    tb = draw.textbbox((0, 0), label, font=f_title)
    draw.text(((w - (tb[2] - tb[0])) / 2, h * 0.22), label, font=f_title, fill=(26, 54, 93))
    tb2 = draw.textbbox((0, 0), title, font=f_body)
    draw.text(((w - (tb2[2] - tb2[0])) / 2, h * 0.40), title, font=f_body, fill=(26, 54, 93))
    # wrap hint
    words = hint.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=f_body)[2] < w - 120:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    y = h * 0.55
    for line in lines[:4]:
        lb = draw.textbbox((0, 0), line, font=f_body)
        draw.text(((w - (lb[2] - lb[0])) / 2, y), line, font=f_body, fill=(80, 80, 80))
        y += 36
    img.save(path, "PNG")

    para = document.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.first_line_indent = Cm(0)
    para.paragraph_format.space_before = Pt(6)
    run = para.add_run()
    run.add_picture(str(path), width=Inches(6.1))
    cap = document.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = Cm(0)
    cap.paragraph_format.space_after = Pt(14)
    r = cap.add_run(title + "  —  " + hint)
    set_run_font(r, size=10, italic=True, color=NAVY)


def add_table_caption(document: Document, text: str) -> None:
    cap = document.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = Cm(0)
    cap.paragraph_format.space_before = Pt(10)
    cap.paragraph_format.space_after = Pt(4)
    r = cap.add_run(text)
    set_run_font(r, size=11, italic=True, color=NAVY)


def add_table(document: Document, rows: list[list[str]], caption: str | None = None) -> None:
    if not rows:
        return
    if caption:
        add_table_caption(document, caption)
    table = document.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            para = cell.paragraphs[0]
            para.paragraph_format.first_line_indent = Cm(0)
            add_formatted_runs(para, val, size=10)
            if i == 0:
                for run in para.runs:
                    run.bold = True
    document.add_paragraph("")


def convert_markdown(document: Document, markdown: str) -> None:
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped == "---":
            i += 1
            continue
        if stripped in {"<!--pagebreak-->", "\\newpage"}:
            document.add_page_break()
            i += 1
            continue
        if stripped.startswith(":::cadre"):
            payload = stripped[len(":::cadre"):].strip()
            parts = [part.strip() for part in payload.split("|")]
            title = parts[0] if parts else "Élément à coller"
            hint = parts[1] if len(parts) > 1 else "Coller ici l’élément manquant (capture, schéma ou tableau)."
            height = float(parts[2]) if len(parts) > 2 else 4.6
            add_cadre(document, title, hint, height_in=height)
            i += 1
            continue
        if stripped.startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i].rstrip("\n"))
                i += 1
            if i < len(lines):
                i += 1
            add_code_block(document, code_lines)
            continue
        img_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if img_match:
            caption, rel = img_match.group(1), img_match.group(2)
            path = (CORPS.parent / rel).resolve()
            if path.exists():
                para = document.add_paragraph()
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                para.paragraph_format.first_line_indent = Cm(0)
                run = para.add_run()
                run.add_picture(str(path), width=Inches(6.1))
                cap = document.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.paragraph_format.first_line_indent = Cm(0)
                cap.paragraph_format.space_after = Pt(12)
                r = cap.add_run(caption)
                set_run_font(r, size=11, italic=True, color=NAVY)
            i += 1
            continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            if level == 1 and any(
                title.upper().startswith(prefix)
                for prefix in ("CHAPITRE", "CONCLUSION", "BIBLIOGRAPHIE", "WEBOGRAPHIE", "ANNEXES")
            ):
                document.add_page_break()
            document.add_heading(title, level=min(level, 3))
            i += 1
            continue
        tab_cap = re.match(r"^(Tableau\s+\d+\..+)$", stripped)
        if tab_cap:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and is_table_row(lines[j].strip()):
                caption = tab_cap.group(1)
                i = j
                rows = []
                while i < len(lines) and is_table_row(lines[i].strip()):
                    cells = parse_table_row(lines[i])
                    if not is_sep(cells):
                        rows.append(cells)
                    i += 1
                add_table(document, rows, caption=caption)
                continue
        if is_table_row(stripped):
            rows = []
            while i < len(lines) and is_table_row(lines[i].strip()):
                cells = parse_table_row(lines[i])
                if not is_sep(cells):
                    rows.append(cells)
                i += 1
            add_table(document, rows)
            continue
        if stripped.startswith("- "):
            while i < len(lines) and lines[i].strip().startswith("- "):
                item = lines[i].strip()[2:].strip()
                para = document.add_paragraph(style="List Bullet")
                para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                add_formatted_runs(para, item)
                i += 1
            continue
        if re.match(r"^\d+\.\s", stripped):
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                item = re.sub(r"^\d+\.\s*", "", lines[i].strip())
                para = document.add_paragraph(style="List Number")
                para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                add_formatted_runs(para, item)
                i += 1
            continue
        if stripped.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            para = document.add_paragraph()
            para.paragraph_format.left_indent = Cm(1)
            para.paragraph_format.first_line_indent = Cm(0)
            para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
            add_formatted_runs(para, " ".join(quote))
            for run in para.runs:
                run.italic = True
            continue
        block = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith("#")
                or nxt.startswith("- ")
                or re.match(r"^\d+\.\s", nxt)
                or is_table_row(nxt)
                or nxt.startswith(">")
                or nxt.startswith(":::")
                or nxt.startswith("![")
                or nxt.startswith("```")
                or re.match(r"^Tableau\s+\d+\.", nxt)
                or nxt in {"<!--pagebreak-->", "\\newpage"}
            ):
                break
            block.append(nxt)
            i += 1
        para = document.add_paragraph()
        para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        para.paragraph_format.first_line_indent = Cm(1.25)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_formatted_runs(para, " ".join(block))


def cover(document: Document) -> None:
    centered(document, "MINISTÈRE DE L’ENSEIGNEMENT SUPÉRIEUR, DE LA RECHERCHE ET DE L’INNOVATION", size=11, bold=True, space_after=4)
    centered(document, "UNIVERSITÉ JOSEPH KI-ZERBO (UJKZ)", size=14, bold=True, space_after=4)
    centered(document, "INSTITUT BURKINABÈ DES ARTS ET MÉTIERS (IBAM)", size=14, bold=True, space_after=14)
    centered(document, "Mémoire pour l’obtention du diplôme du", size=12, italic=True, space_after=4)
    centered(document, "MASTER EN INFORMATIQUE", size=16, bold=True, space_after=8)
    centered(document, "Option : " + OPTION, size=12, italic=True, space_after=18)
    centered(document, "Sous le thème :", size=12, italic=True, space_after=8)
    centered(document, TITRE, size=16, bold=True, space_after=8)
    centered(document, "Prototype : portail local DocSearch", size=12, italic=True, space_after=24)
    centered(document, "Présenté par", size=12, space_after=4)
    centered(document, AUTEUR, size=14, bold=True, space_after=16)
    centered(document, "Directeur de mémoire", size=12, space_after=4)
    centered(document, DIRECTEUR, size=12, italic=True, space_after=20)
    centered(document, "Année universitaire 2025–2026", size=13, bold=True, space_after=8)
    centered(document, "Canevas type des mémoires de Master informatique de l’IBAM (V1.0 — 26/09/2024)", size=10, italic=True, space_after=8)
    document.add_page_break()


def dedicace(document: Document) -> None:
    document.add_heading("Dédicace", level=1)
    p(
        document,
        "Je dédie ce mémoire à ma famille, pour son soutien indéfectible, ses encouragements et sa patience tout au long de ce parcours académique.",
        italic=True,
        first_line=False,
    )
    document.add_page_break()


def remerciements(document: Document) -> None:
    document.add_heading("Remerciements", level=1)
    p(
        document,
        "La réalisation de ce mémoire n’aurait pas été possible sans le soutien et la contribution de plusieurs personnes, à qui je tiens à exprimer toute ma gratitude.",
    )
    p(
        document,
        "Je remercie mon directeur de mémoire, " + DIRECTEUR + ", pour son encadrement, sa disponibilité et ses conseils durant la période de recherche et de rédaction. Merci à Monsieur le Directeur de l’IBAM, au corps professoral et à tout le personnel de l’Institut pour leur accompagnement tout au long de ma formation.",
    )
    p(
        document,
        "Je tiens à exprimer ma profonde gratitude à ma famille, pour son soutien indéfectible et sa patience. Mes remerciements vont également à mes amis et camarades de promotion pour leur entraide et les échanges enrichissants durant ces années d’études. À tous ceux qui, de près ou de loin, ont contribué à ce travail, je dis merci.",
    )
    document.add_page_break()


def resumes(document: Document) -> None:
    document.add_heading("Résumé", level=1)
    p(
        document,
        "Nos travaux portent sur l’indexation intelligente de données pour la recherche d’information, dans le cadre d’une petite organisation. Le constat de départ est double. D’un côté, les outils du quotidien proposent souvent une barre de recherche sans construire d’index : ils parcourent les fichiers au moment de la requête, sans classement par pertinence et sans enrichissement du document. De l’autre, les moteurs industriels (Elasticsearch, Solr, index vectoriels, recherche générative) restent trop lourds à installer et à exploiter pour une structure aux ressources limitées. La qualité des résultats dépend pourtant d’abord de ce qui a été préparé avant la question : extraire, annoter, indexer, puis combiner plusieurs signaux.",
    )
    p(
        document,
        "Par la revue de la littérature, nous distinguons la recherche sans index de la recherche avec index, puis nous retenons trois apports récents transférables en local : un index enrichi, une hybridation légère des scores et une ingestion soignée des formats hétérogènes. Sur cette base, nous concevons un pipeline local, reproductible, sans cluster ni processeur graphique. Chaque fichier éligible (PDF, Word, CSV, texte) est extrait, enrichi de manière déterministe (tags, résumé extractif, entités), persisté, versé dans un index inversé Whoosh, puis interrogé selon trois modes : mots-clés, similarité TF-IDF et fusion hybride. Le prototype DocSearch, développé avec FastAPI, SQLite, Whoosh, scikit-learn et React, matérialise ce pipeline derrière une API REST et une interface web.",
    )
    p(
        document,
        "L’expérimentation porte sur un corpus de démonstration ancré au Centre de documentation de l’IBAM (Université Joseph Ki-Zerbo) : 1 110 pièces reconstituées, multi-formats, couvrant plusieurs années académiques. L’indexation complète dure 25,74 secondes, très en deçà de l’objectif de 120 secondes. La recherche la plus lente observée reste sous 500 millisecondes, pour un objectif d’une seconde. Ces mesures établissent la faisabilité opérationnelle de l’approche. Elles n’équivalent pas à une campagne d’évaluation IR annotée (précision, rappel, MRR), que nous inscrivons en perspective. L’apport du mémoire n’est pas un nouveau paradigme génératif. C’est une démonstration cohérente d’indexation intelligente, explicable et locale, adaptée à un contexte à ressources limitées.",
    )
    p(document, "Mots-clés : recherche d’information ; indexation intelligente ; index inversé ; recherche hybride ; Whoosh ; FastAPI ; métadonnées.", italic=True, first_line=False)

    document.add_heading("Abstract", level=1)
    p(
        document,
        "Our work addresses intelligent data indexing for information retrieval, in the setting of a small organisation. The starting observation is twofold. On the one hand, everyday tools often provide a search box without building an index. They scan files at query time, without ranking them by relevance and without enriching the documents. On the other hand, industrial engines such as Elasticsearch, Solr, vector indexes and generative search remain too heavy to install and operate for an organisation with limited resources. Result quality nevertheless depends first on what has been prepared before the query. This means extracting, annotating, indexing, and then combining several relevance signals.",
    )
    p(
        document,
        "Through the literature review, we distinguish search without an index from search with an index, and we retain three recent contributions that transfer to a local setting: an enriched index, lightweight score hybridisation, and careful ingestion of heterogeneous formats. On that basis we designed a local, reproducible pipeline that requires neither a cluster nor a GPU. Each eligible file (PDF, Word, CSV, plain text, and so on) is extracted, enriched deterministically with tags, extractive summaries and entities, written to a Whoosh inverted index, and then queried in three modes: keywords, TF-IDF similarity and hybrid fusion. The prototype we demonstrate, built with FastAPI, SQLite, Whoosh, scikit-learn and React, implements this pipeline behind a REST API and a web interface.",
    )
    p(
        document,
        "The experiment is based on a demonstration corpus anchored in the Documentation Centre of IBAM (Joseph Ki-Zerbo University). It comprises more than a thousand reconstructed, multi-format records covering several academic years. Full indexing takes 25.74 seconds, well below the 120-second target. The slowest observed search remains under 500 milliseconds, against a one-second objective. These measurements establish the operational feasibility of the approach. They are not equivalent to an annotated IR evaluation campaign (precision, recall, MRR), which we record as a perspective. The contribution of the thesis is not a new generative paradigm. It is a coherent demonstration of intelligent indexing that is explainable, local and suited to a resource-constrained setting.",
    )
    p(document, "Keywords: information retrieval; intelligent indexing; inverted index; hybrid search; Whoosh; FastAPI; metadata.", italic=True, first_line=False)
    document.add_page_break()


def toc_and_lists(document: Document) -> None:
    document.add_heading("Table des matières", level=1)
    items = [
        "Dédicace",
        "Remerciements",
        "Résumé / Abstract",
        "Table des matières",
        "Liste des figures",
        "Liste des tableaux",
        "Liste des algorithmes",
        "Liste des sigles et acronymes",
        "INTRODUCTION GÉNÉRALE",
        "    1. Contexte et motivation",
        "    2. Problématique et hypothèses",
        "    3. Objectifs",
        "    4. Organisation du mémoire",
        "CHAPITRE 1. CONCEPTS FONDAMENTAUX ET ÉTAT DE L’ART",
        "CHAPITRE 2. MÉTHODOLOGIE ET ANALYSE DES BESOINS",
        "CHAPITRE 3. CONCEPTION ET IMPLÉMENTATION DE LA SOLUTION",
        "CHAPITRE 4. EXPÉRIMENTATION, RÉSULTATS ET DISCUSSION",
        "CONCLUSION GÉNÉRALE",
        "BIBLIOGRAPHIE",
        "WEBOGRAPHIE",
        "ANNEXES",
    ]
    for item in items:
        para = document.add_paragraph()
        para.paragraph_format.first_line_indent = Cm(0)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.line_spacing = 1.15
        run = para.add_run(item)
        set_run_font(run, size=12)

    document.add_page_break()
    document.add_heading("Liste des figures", level=1)
    for fig in [
        "Figure 1. Pipeline d’indexation intelligente",
        "Figure 2. Architecture logique de DocSearch",
        "Figure 3. Fusion des scores en recherche hybride",
        "Figure 4. Diagramme de cas d’utilisation de DocSearch",
        "Figure 5 à 10. Captures Swagger des routes de l’API (à coller)",
        "Figure 11 à 14. Captures de l’interface React (à coller)",
        "Figure 15 à 19. Captures des résultats et des tests (à coller)",
        "Figure 20. Extrait du dossier data/raw (à coller)",
        "Figure 21. Grille de tests manuels cochée",
        "Figure 23. Répartition du corpus par format",
        "Figure 24. Composition du fonds par type de pièce",
        "Figure 25. Latence de recherche par mode",
        "Figure 26. Temps observés rapportés aux objectifs",
        "Planches A à P. Captures complémentaires de soutenance (annexes, à coller)",
    ]:
        p(document, fig, first_line=False)

    document.add_heading("Liste des tableaux", level=1)
    for t in [
        "Tableau 1. Synthèse recherche sans index / avec index / indexation intelligente",
        "Tableau 2. Moteurs et plateformes existants",
        "Tableau 3. Corpus de lecture 2022–2026",
        "Tableau 4. Positionnement par rapport à l’état de l’art",
        "Tableau 5. Exigences fonctionnelles",
        "Tableau 6. Exigences non fonctionnelles",
        "Tableau 7. Modèle de données du document",
        "Tableau 8. Choix technologiques",
        "Tableau 9. Organisation logicielle du projet",
        "Tableau 10. Routes principales de l’API",
        "Tableau 11. Cadre expérimental",
        "Tableau 12. Indicateurs de performance",
        "Tableau 13. Latence par mode de recherche",
        "Tableau 14. Comparaison qualitative des méthodes",
        "Tableau 15. Passage du prototype à une solution réelle",
        "Tableau 16. Principaux endpoints de l’API (annexe)",
        "Tableau 17. Extrait du corpus de démonstration",
        "Tableau 18. Extrait des tests manuels",
        "Tableau 19. Correspondance des algorithmes du prototype",
        "Tableau 20. Listings de code du prototype",
    ]:
        p(document, t, first_line=False)

    document.add_heading("Liste des algorithmes", level=1)
    for algo in [
        "Algorithme 1. Ingestion d’un fichier",
        "Algorithme 2. Enrichissement intelligent",
        "Algorithme 3. Résumé extractif",
        "Algorithme 4. Recherche lexicale (Whoosh)",
        "Algorithme 5. Recherche sémantique (TF-IDF / cosinus)",
        "Algorithme 6. Fusion hybride des scores",
    ]:
        p(document, algo, first_line=False)

    document.add_heading("Liste des sigles et acronymes", level=1)
    add_table_caption(document, "Tableau des sigles et acronymes")
    rows = [
        ["Sigle", "Signification"],
        ["API", "Application Programming Interface (interface de programmation)"],
        ["ASI", "Auto Search Indexer"],
        ["BERT", "Bidirectional Encoder Representations from Transformers"],
        ["BM25", "Best Matching 25 (fonction de ranking lexical)"],
        ["CAS", "Central Authentication Service"],
        ["CPU", "Central Processing Unit (processeur central)"],
        ["CSV", "Comma-Separated Values"],
        ["DCMI", "Dublin Core Metadata Initiative"],
        ["DOCX", "Document Office Open XML (format Word)"],
        ["DSI", "Differentiable Search Index"],
        ["EF", "Exigence fonctionnelle"],
        ["ENF", "Exigence non fonctionnelle"],
        ["FAISS", "Facebook AI Similarity Search"],
        ["FAQ", "Frequently Asked Questions (foire aux questions)"],
        ["FTS / FTS5", "Full-Text Search (extension de SQLite)"],
        ["GenIR", "Generative Information Retrieval"],
        ["GLEN", "Generative Retrieval via Lexical Index Learning"],
        ["GPU", "Graphics Processing Unit (processeur graphique)"],
        ["HNSW", "Hierarchical Navigable Small World"],
        ["HTML", "HyperText Markup Language"],
        ["HTTP", "HyperText Transfer Protocol"],
        ["IBAM", "Institut burkinabè des arts et métiers"],
        ["IR / RI", "Information Retrieval / recherche d’information"],
        ["ISIE", "Ingénierie des systèmes d’information en entreprise"],
        ["ISO", "Organisation internationale de normalisation"],
        ["JSON", "JavaScript Object Notation"],
        ["LDAP", "Lightweight Directory Access Protocol"],
        ["LLM", "Large Language Model (grand modèle de langage)"],
        ["MRR", "Mean Reciprocal Rank (rang réciproque moyen)"],
        ["NAS", "Network Attached Storage (stockage en réseau)"],
        ["NCI", "Neural Corpus Indexer"],
        ["nDCG", "Normalized Discounted Cumulative Gain"],
        ["OCR", "Optical Character Recognition (reconnaissance optique de caractères)"],
        ["ONG", "Organisation non gouvernementale"],
        ["OpenAPI", "Spécification OpenAPI (documentation d’API, Swagger)"],
        ["PDF", "Portable Document Format"],
        ["PME", "Petite et moyenne entreprise"],
        ["RAG", "Retrieval-Augmented Generation"],
        ["REST", "Representational State Transfer"],
        ["RQ", "Redis Queue (file d’attente de tâches)"],
        ["SHA-256", "Secure Hash Algorithm, 256 bits"],
        ["SPLADE", "Sparse Lexical and Expansion Model"],
        ["SQL", "Structured Query Language"],
        ["SSO", "Single Sign-On (authentification unique)"],
        ["TF-IDF", "Term Frequency – Inverse Document Frequency"],
        ["TREC", "Text REtrieval Conference"],
        ["TXT", "Fichier texte"],
        ["UJKZ", "Université Joseph Ki-Zerbo"],
        ["UML", "Unified Modeling Language (langage de modélisation unifié)"],
        ["USB", "Universal Serial Bus"],
        ["VM", "Virtual Machine (machine virtuelle)"],
    ]
    add_table(document, rows)
    document.add_page_break()


def main() -> None:
    if not CORPS.exists():
        raise SystemExit(f"Fichier manquant : {CORPS}")
    import runpy

    runpy.run_path(str(ROOT / "scripts" / "gen_figures_memoire.py"), run_name="__main__")
    document = Document()
    configure_section(document)
    style_base(document)
    cover(document)
    dedicace(document)
    remerciements(document)
    resumes(document)
    toc_and_lists(document)
    convert_markdown(document, CORPS.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        document.save(OUTPUT)
        print(f"Mémoire généré : {OUTPUT}")
    except PermissionError:
        alt = OUTPUT.with_name(OUTPUT.stem + "_MAJ.docx")
        try:
            document.save(alt)
            print(f"Fichier Word ouvert. Mémoire enregistré sous : {alt}")
        except PermissionError:
            alt2 = OUTPUT.with_name(OUTPUT.stem + "_legendes.docx")
            document.save(alt2)
            print(f"Fichiers Word ouverts. Mémoire enregistré sous : {alt2}")


if __name__ == "__main__":
    main()
