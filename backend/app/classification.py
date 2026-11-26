"""Classification des pièces du fonds (listing et filtres)."""

from __future__ import annotations

from pathlib import Path

CATEGORY_SCIENTIFIC = "scientific"
CATEGORY_ARCHIVES = "archives"

CATEGORY_LABELS = {
    CATEGORY_SCIENTIFIC: "Scientifique",
    CATEGORY_ARCHIVES: "Archives IBAM",
}


def classify_path(source_path: str | None) -> str:
    """Classe un document à partir du nom de fichier source."""
    name = Path(source_path or "").name.lower()
    if name.startswith("sci_"):
        return CATEGORY_SCIENTIFIC
    return CATEGORY_ARCHIVES


def category_label(category: str) -> str:
    return CATEGORY_LABELS.get(category, category)
