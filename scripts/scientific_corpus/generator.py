"""
Génère un corpus scientifique en informatique (reconstitutions pédagogiques).

Les textes simulent articles, surveys, notes techniques et jeux de métadonnées
autour de la RI, du NLP, des bases de données et des SI. Aucun article sous
droit d'auteur n'est recopié : titres, auteurs et contenus sont synthétiques.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass, field
from pathlib import Path

from .topics import AUTEURS, DOMAINES, REVUES, TYPES_DOC

SEED = 20261124
CIBLE = 520
PREFIX = "sci_"


@dataclass
class SciDoc:
    nom: str
    titre: str
    auteurs: list[str]
    annee: int
    domaine: str
    type_doc: str
    mots_cles: list[str]
    resume: str
    sections: list[tuple[str, str]] = field(default_factory=list)
    colonnes: list[str] = field(default_factory=list)
    lignes: list[list[str]] = field(default_factory=list)


def _slug(text: str, limit: int = 48) -> str:
    keep = []
    for ch in text.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in {" ", "-", "_"} and keep and keep[-1] != "-":
            keep.append("-")
    slug = "".join(keep).strip("-")
    return slug[:limit] or "document"


def _auteurs(rng: random.Random, n: int = 3) -> list[str]:
    chosen = rng.sample(AUTEURS, k=min(n, len(AUTEURS)))
    return [f"{nom} ({aff})" for nom, aff in chosen]


def _mots_cles(domaine: dict, rng: random.Random) -> list[str]:
    base = rng.sample(domaine["mots"], k=min(5, len(domaine["mots"])))
    extras = ["informatique", "système d'information", "évaluation expérimentale"]
    return base + rng.sample(extras, k=1)


def _resume(domaine: dict, titre: str, mots: list[str], rng: random.Random) -> str:
    methode = rng.choice(
        [
            "une revue systématique de la littérature",
            "une expérimentation sur un corpus de démonstration",
            "une comparaison de trois approches d'indexation",
            "une analyse de pipeline d'ingestion multi-formats",
            "une étude de cas dans un centre de documentation universitaire",
            "une évaluation des métriques de ranking lexical et hybride",
        ]
    )
    resultat = rng.choice(
        [
            "améliore la précision au rang 10 sans GPU",
            "réduit le temps de recherche sous la seconde",
            "montre l'intérêt d'un enrichissement déterministe",
            "confirme la faisabilité d'un prototype local",
            "met en évidence le rôle des métadonnées dans le ranking",
            "distingue clairement parcours sans index et moteur à index",
        ]
    )
    return (
        f"Cet article traite de « {titre} » dans le domaine {domaine['label'].lower()}. "
        f"Nous présentons {methode}, centrée sur {', '.join(mots[:3])}. "
        f"Les résultats indiquent que l'approche retenue {resultat}. "
        f"Les apports portent sur la conception, l'implémentation et l'évaluation "
        f"d'un système d'information documentaire reproductible."
    )


def _section(titre: str, domaine: dict, mots: list[str], rng: random.Random) -> str:
    phrases = [
        f"Dans le champ {domaine['label'].lower()}, la notion de {rng.choice(mots)} "
        f"reste centrale pour comprendre la qualité des réponses.",
        f"Les travaux récents insistent sur {rng.choice(mots)} et sur "
        f"{rng.choice(domaine['mots'])}, souvent combinés dans des architectures hybrides.",
        f"Notre protocole mesure le temps d'indexation, la latence de requête et "
        f"l'exploitabilité qualitative des extraits.",
        f"Contrairement à un parcours de fichiers à la requête, un index préparé "
        f"sépare clairement ingestion et interrogation.",
        f"Le prototype DocSearch illustre ces choix en local : extraction multi-formats, "
        f"enrichissement, Whoosh et similarité TF-IDF.",
        f"Les limites concernent l'absence d'une collection annotée type TREC et "
        f"l'approximation sémantique du TF-IDF face aux embeddings denses.",
        f"En perspective, un moteur Meilisearch, un OCR asynchrone et un annuaire LDAP "
        f"permettraient une mise en production sur le campus.",
        f"La discussion replace ces résultats dans l'ingénierie des SI : traçabilité "
        f"du pipeline, droits d'accès et conservation des originaux.",
    ]
    rng.shuffle(phrases)
    return " ".join(phrases[:4])


def _titre(domaine: dict, type_doc: str, rng: random.Random) -> str:
    focus = rng.choice(domaine["mots"])
    modeles = {
        "article": [
            f"{focus.capitalize()} pour la recherche documentaire locale",
            f"Évaluation de {focus} dans un moteur d'indexation hybride",
            f"Vers une indexation intelligente fondée sur {focus}",
        ],
        "survey": [
            f"État de l'art : {domaine['label'].lower()} et {focus}",
            f"Cartographie des approches de {focus} (2018-2026)",
        ],
        "note_technique": [
            f"Note technique — déploiement de {focus} en environnement local",
            f"Retour d'expérience : {focus} dans un portail documentaire",
        ],
        "preprint": [
            f"Prépublication : {focus} et ranking multi-signaux",
            f"Brouillon — {focus} sans processeur graphique",
        ],
        "compte_rendu": [
            f"Compte rendu du séminaire {domaine['label']} — session {focus}",
            f"Synthèse atelier Master MISIE : {focus}",
        ],
        "dataset": [
            f"Jeu de métadonnées — corpus {domaine['label'].lower()}",
            f"Catalogue expérimental des documents {focus}",
        ],
        "poster": [
            f"Poster : {focus} et indexation multi-formats",
            f"Affiche scientifique — {domaine['label']} / {focus}",
        ],
        "tutoriel": [
            f"Tutoriel : mettre en œuvre {focus} avec Python",
            f"Guide pratique — {focus} pour un prototype de master",
        ],
    }
    return rng.choice(modeles[type_doc])


def _build_doc(index: int, rng: random.Random) -> SciDoc:
    domaine = rng.choice(DOMAINES)
    type_doc = rng.choice(TYPES_DOC)
    annee = rng.randint(2019, 2026)
    titre = _titre(domaine, type_doc, rng)
    mots = _mots_cles(domaine, rng)
    auteurs = _auteurs(rng, n=rng.randint(2, 4))
    slug = _slug(f"{domaine['id']}-{titre}")
    ext = rng.choices([".txt", ".pdf", ".docx", ".csv"], weights=[45, 20, 20, 15], k=1)[0]
    nom = f"{PREFIX}{annee}_{domaine['id']}_{index:04d}_{slug}{ext}"

    if ext == ".csv":
        colonnes = ["id", "titre", "domaine", "annee", "mots_cles", "score_pertinence"]
        lignes = []
        for i in range(rng.randint(12, 28)):
            d2 = rng.choice(DOMAINES)
            lignes.append(
                [
                    f"P{index:04d}-{i:02d}",
                    _titre(d2, "article", rng)[:80],
                    d2["label"],
                    str(rng.randint(2019, 2026)),
                    ";".join(rng.sample(d2["mots"], k=3)),
                    f"{rng.uniform(0.35, 0.98):.3f}",
                ]
            )
        return SciDoc(
            nom=nom,
            titre=titre,
            auteurs=auteurs,
            annee=annee,
            domaine=domaine["label"],
            type_doc=type_doc,
            mots_cles=mots,
            resume=_resume(domaine, titre, mots, rng),
            colonnes=colonnes,
            lignes=lignes,
        )

    sections = [
        ("Introduction", _section("Introduction", domaine, mots, rng)),
        ("Cadre théorique", _section("Cadre", domaine, mots, rng)),
        ("Méthode", _section("Méthode", domaine, mots, rng)),
        ("Résultats", _section("Résultats", domaine, mots, rng)),
        ("Discussion", _section("Discussion", domaine, mots, rng)),
        ("Conclusion", _section("Conclusion", domaine, mots, rng)),
    ]
    return SciDoc(
        nom=nom,
        titre=titre,
        auteurs=auteurs,
        annee=annee,
        domaine=domaine["label"],
        type_doc=type_doc,
        mots_cles=mots,
        resume=_resume(domaine, titre, mots, rng),
        sections=sections,
    )


def toutes_les_pieces(cible: int = CIBLE) -> list[SciDoc]:
    rng = random.Random(SEED)
    docs = [_build_doc(i + 1, rng) for i in range(cible)]
    noms = [doc.nom for doc in docs]
    if len(noms) != len(set(noms)):
        raise SystemExit("Noms scientifiques en double — ajuster le générateur.")
    return docs


def _texte(doc: SciDoc) -> str:
    revue = REVUES[hash(doc.nom) % len(REVUES)]
    lines = [
        doc.titre,
        "",
        f"Auteurs : {', '.join(doc.auteurs)}",
        f"Année : {doc.annee}",
        f"Type : {doc.type_doc}",
        f"Domaine : {doc.domaine}",
        f"Revue / support : {revue}",
        f"Mots-clés : {', '.join(doc.mots_cles)}",
        "",
        "Résumé",
        doc.resume,
        "",
    ]
    for titre, corps in doc.sections:
        lines.extend([titre, corps, ""])
    lines.append(
        "Document de démonstration généré pour DocSearch (reconstitution pédagogique, "
        "non publié). Usage : mémoire Master MISIE / IBAM — indexation intelligente."
    )
    return "\n".join(lines).strip() + "\n"


def ecrire_txt(path: Path, doc: SciDoc) -> None:
    path.write_text(_texte(doc), encoding="utf-8")


def ecrire_csv(path: Path, doc: SciDoc) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(doc.colonnes)
        writer.writerows(doc.lignes)


def ecrire_docx(path: Path, doc: SciDoc) -> None:
    from docx import Document
    from docx.shared import Pt

    document = Document()
    style = document.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    document.add_heading(doc.titre, level=1)
    document.add_paragraph(f"Auteurs : {', '.join(doc.auteurs)}")
    document.add_paragraph(
        f"{doc.annee} · {doc.domaine} · {doc.type_doc} · mots-clés : {', '.join(doc.mots_cles)}"
    )
    document.add_heading("Résumé", level=2)
    document.add_paragraph(doc.resume)
    for titre, corps in doc.sections:
        document.add_heading(titre, level=2)
        document.add_paragraph(corps)
    document.add_paragraph(
        "Reconstitution pédagogique DocSearch — Master MISIE / IBAM."
    )
    document.save(path)


def ecrire_pdf(path: Path, doc: SciDoc) -> None:
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    def xml(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "SciTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    meta = ParagraphStyle(
        "SciMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "SciBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    heading = ParagraphStyle(
        "SciH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
    )

    story = [
        Paragraph(xml(doc.titre), title),
        Paragraph(xml(", ".join(doc.auteurs)), meta),
        Paragraph(xml(f"{doc.annee} — {doc.domaine} — {doc.type_doc}"), meta),
        Paragraph(xml(f"Mots-clés : {', '.join(doc.mots_cles)}"), meta),
        Spacer(1, 4 * mm),
        Paragraph(xml("Résumé"), heading),
        Paragraph(xml(doc.resume), body),
    ]
    for titre_sec, corps in doc.sections:
        story.append(Paragraph(xml(titre_sec), heading))
        story.append(Paragraph(xml(corps), body))

    pdf = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=doc.titre,
        author=", ".join(doc.auteurs[:2]),
    )
    pdf.build(story)


def ecrire_doc(dossier: Path, doc: SciDoc) -> None:
    path = dossier / doc.nom
    suffix = path.suffix.lower()
    if suffix == ".csv":
        ecrire_csv(path, doc)
    elif suffix == ".docx":
        ecrire_docx(path, doc)
    elif suffix == ".pdf":
        ecrire_pdf(path, doc)
    else:
        ecrire_txt(path, doc)
