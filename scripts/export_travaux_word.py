"""
Exporte les fichiers Markdown du dossier travaux/ vers Word (.docx).

Usage :
    .venv\\Scripts\\python.exe scripts\\export_travaux_word.py
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRAVaux_DIR = PROJECT_ROOT / "travaux"
OUTPUT_DIR = TRAVaux_DIR / "word"

MD_FILES = [
    TRAVaux_DIR / "README.md",
    TRAVaux_DIR / "JOUR_1.md",
    TRAVaux_DIR / "JOUR_2.md",
    TRAVaux_DIR / "JOUR_3.md",
    TRAVaux_DIR / "A_resume_general.md",
    TRAVaux_DIR / "B_introduction_generale.md",
    TRAVaux_DIR / "C_corps_du_travail.md",
    TRAVaux_DIR / "D_conclusion_perspectives.md",
]

COMBINED_ORDER = [
    ("Page de garde", None),
    ("Introduction générale", TRAVaux_DIR / "B_introduction_generale.md"),
    ("Résumé général de la littérature", TRAVaux_DIR / "A_resume_general.md"),
    ("Corps du travail", TRAVaux_DIR / "C_corps_du_travail.md"),
    ("Bilan Jour 1", TRAVaux_DIR / "JOUR_1.md"),
    ("Bilan Jour 2", TRAVaux_DIR / "JOUR_2.md"),
    ("Bilan Jour 3", TRAVaux_DIR / "JOUR_3.md"),
    ("Conclusion et perspectives", TRAVaux_DIR / "D_conclusion_perspectives.md"),
]


def _add_formatted_runs(paragraph, text: str, *, bold_default: bool = False) -> None:
    pattern = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
    parts = pattern.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
        elif part.startswith("[") and "](" in part:
            match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part)
            if match:
                run = paragraph.add_run(f"{match.group(1)} ({match.group(2)})")
            else:
                paragraph.add_run(part)
        else:
            run = paragraph.add_run(part)
            if bold_default:
                run.bold = True


def _is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and "|" in stripped[1:-1]


def _parse_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells if cell)


def _add_table(document: Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    table = document.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    for row_idx, row_cells in enumerate(rows):
        for col_idx, cell_text in enumerate(row_cells):
            cell = table.rows[row_idx].cells[col_idx]
            cell.text = ""
            paragraph = cell.paragraphs[0]
            _add_formatted_runs(paragraph, cell_text)
            if row_idx == 0:
                for run in paragraph.runs:
                    run.bold = True


def _convert_markdown_to_document(markdown: str, document: Document, *, skip_first_h1: bool = False) -> None:
    lines = markdown.splitlines()
    index = 0
    first_h1_skipped = False

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped == "---":
            document.add_paragraph("")
            index += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            if skip_first_h1 and not first_h1_skipped and level == 1:
                first_h1_skipped = True
                index += 1
                continue
            document.add_heading(title, level=min(level, 3))
            index += 1
            continue

        if _is_table_row(stripped):
            table_rows: list[list[str]] = []
            while index < len(lines) and _is_table_row(lines[index].strip()):
                cells = _parse_table_row(lines[index])
                if not _is_separator_row(cells):
                    table_rows.append(cells)
                index += 1
            _add_table(document, table_rows)
            continue

        if stripped.startswith("- "):
            while index < len(lines) and lines[index].strip().startswith("- "):
                item = lines[index].strip()[2:].strip()
                paragraph = document.add_paragraph(style="List Bullet")
                _add_formatted_runs(paragraph, item)
                index += 1
            continue

        if re.match(r"^\d+\.\s", stripped):
            while index < len(lines) and re.match(r"^\d+\.\s", lines[index].strip()):
                item = re.sub(r"^\d+\.\s*", "", lines[index].strip())
                paragraph = document.add_paragraph(style="List Number")
                _add_formatted_runs(paragraph, item)
                index += 1
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip().lstrip(">").strip())
                index += 1
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Pt(18)
            _add_formatted_runs(paragraph, " ".join(quote_lines))
            for run in paragraph.runs:
                run.italic = True
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            nxt = lines[index].strip()
            if (
                not nxt
                or nxt.startswith("#")
                or nxt == "---"
                or nxt.startswith("- ")
                or re.match(r"^\d+\.\s", nxt)
                or _is_table_row(nxt)
                or nxt.startswith(">")
            ):
                break
            paragraph_lines.append(nxt)
            index += 1

        paragraph = document.add_paragraph()
        _add_formatted_runs(paragraph, " ".join(paragraph_lines))


def _style_document(document: Document) -> None:
    style = document.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    for heading_level in range(1, 4):
        heading = document.styles[f"Heading {heading_level}"]
        heading.font.name = "Calibri"
        heading.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)


def _add_cover_page(document: Document) -> None:
    for _ in range(4):
        document.add_paragraph("")

    title = document.add_paragraph()
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = title.add_run(
        "Indexation intelligente de données hétérogènes\npour la recherche d'information"
    )
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)

    document.add_paragraph("")

    subtitle = document.add_paragraph()
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    sub_run = subtitle.add_run("Revue de littérature")
    sub_run.font.size = Pt(14)
    sub_run.italic = True

    document.add_paragraph("")

    meta = document.add_paragraph()
    meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    meta.add_run("15 articles scientifiques — période 2022–2026")

    document.add_paragraph("")
    document.add_paragraph("")

    info = document.add_paragraph()
    info.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    info.add_run("Projet tutoré\n")
    info.add_run("Master Ingénierie des Systèmes d'Information en Entreprise\n")
    info.add_run("\n")
    info.add_run("Nom de l'étudiant : ____________________\n")
    info.add_run("Encadrant : ____________________\n")
    info.add_run("Date : ____________________")

    document.add_page_break()

    document.add_heading("Sommaire", level=1)
    for item in [
        "1. Introduction générale",
        "2. Résumé général de la littérature",
        "3. Corps du travail",
        "4. Bilan du Jour 1 (articles 1 à 5)",
        "5. Bilan du Jour 2 (articles 6 à 10)",
        "6. Bilan du Jour 3 (articles 11 à 15)",
        "7. Conclusion et perspectives",
    ]:
        p = document.add_paragraph(item)
        p.paragraph_format.space_after = Pt(6)

    document.add_page_break()


def export_single(md_path: Path, docx_path: Path) -> None:
    document = Document()
    _style_document(document)
    markdown = md_path.read_text(encoding="utf-8")
    _convert_markdown_to_document(markdown, document)
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(docx_path)


def export_combined(docx_path: Path) -> None:
    document = Document()
    _style_document(document)
    _add_cover_page(document)

    for section_title, md_path in COMBINED_ORDER:
        if md_path is None:
            continue
        document.add_heading(section_title, level=1)
        markdown = md_path.read_text(encoding="utf-8")
        _convert_markdown_to_document(markdown, document, skip_first_h1=True)
        document.add_page_break()

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(docx_path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for md_path in MD_FILES:
        if not md_path.exists():
            continue
        docx_name = md_path.stem + ".docx"
        docx_path = OUTPUT_DIR / docx_name
        try:
            export_single(md_path, docx_path)
            created.append(docx_path)
        except PermissionError:
            alt_path = OUTPUT_DIR / "_maj" / docx_name
            export_single(md_path, alt_path)
            created.append(alt_path)
            print(f"Fichier verrouillé, export alternatif : {alt_path}")

    combined_path = OUTPUT_DIR / "TRAVAIL_COMPLET.docx"
    try:
        export_combined(combined_path)
    except PermissionError:
        combined_path = OUTPUT_DIR / "_maj" / "TRAVAIL_COMPLET.docx"
        export_combined(combined_path)
        print(f"Fichier verrouillé, export alternatif : {combined_path}")
    created.append(combined_path)

    print(f"{len(created)} fichiers Word générés dans {OUTPUT_DIR}:")
    for path in created:
        print(f"  - {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
