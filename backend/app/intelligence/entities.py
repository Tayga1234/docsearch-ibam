"""Extraction d'entités déterministe (regex) + spaCy optionnel."""

from __future__ import annotations

import re

MONTHS = (
    "janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|"
    "septembre|octobre|novembre|décembre|decembre"
)

DATE_NUMERIC = re.compile(
    r"\b(?:\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\d{4}[/.-]\d{1,2}[/.-]\d{1,2})\b"
)
DATE_FRENCH = re.compile(
    rf"\b(?:le\s+)?(\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}})\b",
    re.IGNORECASE,
)
DATE_MONTH_YEAR = re.compile(
    rf"\b((?:{MONTHS})\s+\d{{4}})\b",
    re.IGNORECASE,
)
YEAR_PATTERN = re.compile(r"\b(19\d{2}|20[0-3]\d)\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(
    r"\b(?:\+?\d{1,3}[\s.-]?)?(?:\d{2}[\s.-]?){3,4}\d{2}\b"
)
AUTHORS_LINE = re.compile(
    r"(?im)^(?:auteurs?|authors?|rédigé par|signe(?:́|e)? par|par)\s*[:\-–]\s*(.+)$"
)
YEAR_LINE = re.compile(r"(?im)^(?:année|annee|year|date)\s*[:\-–]\s*(\d{4})\b")
KEYWORDS_LINE = re.compile(
    r"(?im)^(?:mots[-\s]?clés?|keywords?|thèmes?)\s*[:\-–]\s*(.+)$"
)
DOMAIN_LINE = re.compile(r"(?im)^(?:domaine|field)\s*[:\-–]\s*(.+)$")
ORG_PATTERN = re.compile(
    r"\b(?:"
    r"IBAM|UJKZ|ANPTIC|CAMES|2iE|SONABEL|"
    r"Université(?:\s+[A-ZÀ-Ÿ][\w'’\-]+)+(?:\s+[A-ZÀ-Ÿ][\w'’\-]+)*|"
    r"Institut(?:\s+[A-ZÀ-Ÿ][\w'’\-]+){1,6}|"
    r"Centre\s+de\s+documentation(?:\s+et\s+des\s+archives)?"
    r")\b",
    re.IGNORECASE,
)
# Pas de \s : évite de coller « Résumé\nCet » comme un nom
PERSON_INLINE = re.compile(
    r"\b([A-ZÀ-Ÿ](?:\.|[a-zà-ÿ'’\-]+)[ \t]+[A-ZÀ-Ÿ][a-zà-ÿ'’\-]{2,})"
    r"(?:[ \t]*\([^)]+\))?"
)

SECTION_STOPWORDS = {
    "résumé",
    "resume",
    "abstract",
    "introduction",
    "méthode",
    "methode",
    "méthodes",
    "methodes",
    "résultats",
    "resultats",
    "discussion",
    "conclusion",
    "conclusions",
    "références",
    "references",
    "annexe",
    "annexes",
    "bibliographie",
    "mots",
    "domaine",
    "catalogue",
    "article",
    "chapitre",
    "section",
}

_nlp = None


def _load_spacy():
    global _nlp
    if _nlp is not None:
        return _nlp

    try:
        import spacy
    except ImportError:
        return None

    try:
        _nlp = spacy.load("fr_core_news_sm")
    except OSError:
        _nlp = None
    return _nlp


def _clean_list(values: list[str], *, limit: int = 12) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = " ".join(str(value).split()).strip(" ,;.|")
        if len(item) < 2:
            continue
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
        if len(cleaned) >= limit:
            break
    return cleaned


def _is_plausible_person(name: str) -> bool:
    first = name.strip().split()[0].lower().strip(".,;:") if name.strip() else ""
    if first in SECTION_STOPWORDS:
        return False
    # Rejette les paires du type « Cet article », « Les résultats »
    tokens = [t for t in re.split(r"[ \t]+", name.strip()) if t]
    if len(tokens) >= 2 and tokens[0][0].isupper() and tokens[1][0].islower():
        # "Résumé Cet" après normalisation n'arrive plus ; garde "Fatou Sanou"
        pass
    low = name.lower()
    if any(w in low for w in ("article", "document", "rapport", "chapitre")):
        return False
    return True


def _split_people(blob: str) -> list[str]:
    parts = re.split(r"\s*(?:,|;|\bet\b|&|/)\s*", blob)
    people: list[str] = []
    for part in parts:
        name = part.strip()
        # Garde "I. Sawadogo (2iE)" ou "Fatou Sanou"
        if len(name) < 3:
            continue
        if EMAIL_PATTERN.search(name) or PHONE_PATTERN.fullmatch(name or ""):
            continue
        if not _is_plausible_person(name):
            continue
        people.append(name)
    return people


def _extract_with_regex(text: str) -> dict[str, list[str]]:
    dates = (
        DATE_NUMERIC.findall(text)
        + DATE_FRENCH.findall(text)
        + DATE_MONTH_YEAR.findall(text)
        + YEAR_LINE.findall(text)
    )
    # Années isolées utiles, mais limitées pour éviter le bruit
    years = [y for y in YEAR_PATTERN.findall(text) if 1990 <= int(y) <= 2035]
    dates.extend(years[:8])

    authors: list[str] = []
    for match in AUTHORS_LINE.finditer(text):
        authors.extend(_split_people(match.group(1)))

    # Fallback : signatures en tête (ligne auteurs sans préfixe, ou initiales)
    if not authors:
        head = text[:2500]
        # Préfère les noms avec affiliation entre parenthèses
        with_affil = [
            m.group(0).strip()
            for m in PERSON_INLINE.finditer(head)
            if "(" in m.group(0) and _is_plausible_person(m.group(0))
        ]
        if with_affil:
            authors.extend(with_affil)
        else:
            for match in PERSON_INLINE.finditer(head):
                candidate = match.group(0).strip()
                if _is_plausible_person(candidate):
                    authors.append(candidate)

    keywords: list[str] = []
    for match in KEYWORDS_LINE.finditer(text):
        keywords.extend(
            p.strip()
            for p in re.split(r"\s*(?:,|;)\s*", match.group(1))
            if len(p.strip()) > 1
        )

    domains: list[str] = []
    for match in DOMAIN_LINE.finditer(text):
        domains.append(match.group(1).strip())

    organizations = ORG_PATTERN.findall(text)

    return {
        "dates": _clean_list(dates, limit=10),
        "authors": _clean_list(authors, limit=10),
        "emails": _clean_list(EMAIL_PATTERN.findall(text), limit=8),
        "phones": _clean_list(PHONE_PATTERN.findall(text), limit=8),
        "keywords": _clean_list(keywords, limit=12),
        "domains": _clean_list(domains, limit=6),
        "organizations": _clean_list(organizations, limit=10),
        "persons": [],
        "locations": [],
    }


def extract_entities(text: str) -> dict[str, list[str]]:
    if not text or not text.strip():
        return {
            "dates": [],
            "authors": [],
            "emails": [],
            "phones": [],
            "keywords": [],
            "domains": [],
            "organizations": [],
            "persons": [],
            "locations": [],
        }

    entities = _extract_with_regex(text)
    nlp = _load_spacy()
    if nlp is None:
        # Sans spaCy, les auteurs servent aussi de personnes détectées
        if entities["authors"] and not entities["persons"]:
            entities["persons"] = list(entities["authors"][:8])
        return entities

    doc = nlp(text[:10000])
    for ent in doc.ents:
        label = ent.label_.lower()
        value = ent.text.strip()
        if not value:
            continue
        if label in {"per", "person"}:
            if _is_plausible_person(value):
                entities["persons"].append(value)
        elif label in {"org", "organization"}:
            entities["organizations"].append(value)
        elif label in {"loc", "gpe", "location"}:
            entities["locations"].append(value)
        elif label in {"date", "time"}:
            entities["dates"].append(value)

    for key, values in list(entities.items()):
        entities[key] = _clean_list(values)

    if entities["authors"] and not entities["persons"]:
        entities["persons"] = list(entities["authors"][:8])

    return entities
