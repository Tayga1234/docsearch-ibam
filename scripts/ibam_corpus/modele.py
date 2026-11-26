from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .identite import (
    BP,
    DEVISE,
    ETABLISSEMENT,
    FAX,
    FONT_BOLD,
    FONT_REGULAR,
    MINISTERE,
    SIGLE,
    SIGLE_UNIV,
    TEL,
    UNIVERSITE,
)


@dataclass
class Piece:
    nom: str
    service: str
    ref: str
    date: str
    objet: str
    signataire: str
    destinataires: str = ""
    paragraphes: list[str] = field(default_factory=list)
    colonnes: list[str] = field(default_factory=list)
    lignes: list[list[str]] = field(default_factory=list)


def en_tete(piece: Piece) -> list[str]:
    lines = [
        "BURKINA FASO",
        DEVISE,
        "",
        MINISTERE,
        UNIVERSITE.upper(),
        f"{ETABLISSEMENT.upper()} ({SIGLE})",
        piece.service,
        "",
        f"{BP}  —  Tél. {TEL}  —  Fax {FAX}",
        "",
        f"Réf. : {piece.ref}",
        f"Ouagadougou, le {piece.date}",
        "",
        f"Objet : {piece.objet}",
    ]
    if piece.destinataires:
        lines.append(f"Destinataires : {piece.destinataires}")
    lines.append("")
    return lines


def pied(piece: Piece) -> list[str]:
    return [
        "",
        "Ampliations :",
        f"  – Direction de l'{SIGLE}",
        f"  – Centre de documentation et des archives",
        f"  – Chrono / archives {SIGLE}",
        "",
        piece.signataire,
        f"{SIGLE} / {SIGLE_UNIV} — document interne, reproduction soumise à autorisation.",
    ]


def texte_complet(piece: Piece) -> str:
    bloc = en_tete(piece) + piece.paragraphes + pied(piece)
    return "\n".join(bloc).strip() + "\n"


def ecrire_txt(path: Path, piece: Piece) -> None:
    path.write_text(texte_complet(piece), encoding="utf-8")


def ecrire_csv(path: Path, piece: Piece) -> None:
    import csv

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(piece.colonnes)
        writer.writerows(piece.lignes)


def ecrire_docx(path: Path, piece: Piece) -> None:
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    for line in en_tete(piece):
        para = doc.add_paragraph(line)
        if line in {ETABLISSEMENT.upper() + f" ({SIGLE})", UNIVERSITE.upper(), "BURKINA FASO"}:
            para.runs[0].bold = True if para.runs else False

    for bloc in piece.paragraphes:
        if not bloc:
            continue
        if bloc.startswith("## "):
            doc.add_heading(bloc[3:], level=2)
        else:
            doc.add_paragraph(bloc)

    for line in pied(piece):
        if line:
            doc.add_paragraph(line)
    doc.save(path)


def ecrire_pdf(path: Path, piece: Piece) -> None:
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    if FONT_REGULAR.exists():
        pdfmetrics.registerFont(TTFont("CorpusSans", str(FONT_REGULAR)))
        font_name = "CorpusSans"
        if FONT_BOLD.exists():
            pdfmetrics.registerFont(TTFont("CorpusSans-Bold", str(FONT_BOLD)))
            font_bold = "CorpusSans-Bold"
        else:
            font_bold = font_name
    else:
        font_name = "Helvetica"
        font_bold = "Helvetica-Bold"

    styles = getSampleStyleSheet()
    center = ParagraphStyle(
        "Centre",
        parent=styles["Normal"],
        fontName=font_bold,
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    meta = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=2,
    )
    body = ParagraphStyle(
        "Corps",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10.5,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    heading = ParagraphStyle(
        "TitreSection",
        parent=styles["Normal"],
        fontName=font_bold,
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=6,
    )

    story: list = []
    for line in [
        "BURKINA FASO",
        DEVISE,
        MINISTERE,
        UNIVERSITE,
        f"{ETABLISSEMENT} ({SIGLE})",
        piece.service,
    ]:
        story.append(Paragraph(_xml(line), center))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(_xml(f"{BP} — Tél. {TEL}"), meta))
    story.append(Paragraph(_xml(f"Réf. : {piece.ref}"), meta))
    story.append(Paragraph(_xml(f"Ouagadougou, le {piece.date}"), meta))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(_xml(f"<b>Objet :</b> {piece.objet}"), meta))
    if piece.destinataires:
        story.append(Paragraph(_xml(f"<b>Destinataires :</b> {piece.destinataires}"), meta))
    story.append(Spacer(1, 4 * mm))

    for bloc in piece.paragraphes:
        if not bloc:
            continue
        if bloc.startswith("## "):
            story.append(Paragraph(_xml(bloc[3:]), heading))
        else:
            story.append(Paragraph(_xml(bloc), body))

    story.append(Spacer(1, 6 * mm))
    for line in pied(piece):
        if line:
            story.append(Paragraph(_xml(line), meta))

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=piece.objet,
        author=f"{SIGLE} / {SIGLE_UNIV}",
    )
    doc.build(story)


def _xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("&lt;b&gt;", "<b>")
        .replace("&lt;/b&gt;", "</b>")
    )


def ecrire_piece(dossier: Path, piece: Piece) -> None:
    path = dossier / piece.nom
    suffix = path.suffix.lower()
    if suffix == ".csv":
        ecrire_csv(path, piece)
    elif suffix == ".docx":
        ecrire_docx(path, piece)
    elif suffix == ".pdf":
        ecrire_pdf(path, piece)
    else:
        ecrire_txt(path, piece)
