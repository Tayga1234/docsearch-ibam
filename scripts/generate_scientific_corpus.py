"""
Génère un corpus scientifique informatique dans data/raw/ (préfixe sci_).

Par défaut, les pièces IBAM existantes sont conservées : le fonds mélange
archives administratives et littérature scientifique reconstituée.
Utiliser --replace-all pour vider data/raw avant génération (déconseillé
si le mémoire s'appuie encore sur le cas IBAM).

Usage :
    .venv\\Scripts\\python.exe scripts\\generate_scientific_corpus.py
    .venv\\Scripts\\python.exe scripts\\generate_scientific_corpus.py --count 600
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from scientific_corpus.generator import (  # noqa: E402
    CIBLE,
    PREFIX,
    ecrire_doc,
    toutes_les_pieces,
)

RAW_DIR = PROJECT_ROOT / "data" / "raw"


def _purge_scientific() -> int:
    removed = 0
    if not RAW_DIR.exists():
        return 0
    for path in RAW_DIR.iterdir():
        if path.is_file() and path.name.startswith(PREFIX):
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def _purge_all() -> int:
    removed = 0
    if not RAW_DIR.exists():
        return 0
    for path in RAW_DIR.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="Corpus scientifique CS pour DocSearch")
    parser.add_argument("--count", type=int, default=CIBLE, help=f"Nombre de pièces (défaut {CIBLE})")
    parser.add_argument(
        "--replace-all",
        action="store_true",
        help="Vider tout data/raw avant génération (supprime aussi le corpus IBAM)",
    )
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if args.replace_all:
        removed = _purge_all()
        print(f"Fonds vidé : {removed} fichiers retirés")
    else:
        removed = _purge_scientific()
        print(f"Anciennes pièces scientifiques retirées : {removed}")

    docs = toutes_les_pieces(cible=max(50, args.count))
    for index, doc in enumerate(docs, start=1):
        ecrire_doc(RAW_DIR, doc)
        if index % 100 == 0 or index == len(docs):
            print(f"  {index}/{len(docs)} documents scientifiques écrits")

    counts = Counter(Path(doc.nom).suffix.lower() for doc in docs)
    total = sum(1 for path in RAW_DIR.iterdir() if path.is_file() and path.name != ".gitkeep")

    print(f"Pièces scientifiques générées : {len(docs)}")
    print("  " + ", ".join(f"{ext} {n}" for ext, n in sorted(counts.items())))
    print(f"Total dans data/raw : {total} fichiers")
    print(f"Dossier : {RAW_DIR}")
    print("Ensuite : se connecter en admin, puis Indexation > scan (force),")
    print("          ou POST /ingest/scan?force=true")


if __name__ == "__main__":
    main()
