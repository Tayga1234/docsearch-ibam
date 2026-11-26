"""
Génère le corpus de démonstration DocSearch — cas IBAM / UJKZ.

Cadre institutionnel réel :
  Institut Burkinabè des Arts et Métiers (IBAM)
  Université Joseph Ki-Zerbo, Ouagadougou
  Centre de documentation et des archives

Les agents, étudiants, montants et délibérations sont fictifs.
Le fonds vise un usage de soutenance, pas la publication de données personnelles.
Volume : au moins 1 000 pièces (noyau métier + fonds 2020-2026).

Usage :
    .venv\\Scripts\\python.exe scripts\\generate_demo_dataset.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from ibam_corpus.catalogue import toutes_les_pieces  # noqa: E402
from ibam_corpus.identite import ETABLISSEMENT, SIGLE  # noqa: E402
from ibam_corpus.modele import ecrire_piece  # noqa: E402

RAW_DIR = PROJECT_ROOT / "data" / "raw"

JUNK_PREFIXES = (
    "collision",
    "same",
    "demo",
    "upload",
    "exemple",
    "extra_",
    "00_CAS_METIER_ISGO",
    "brochure_isgo",
)


def _clean_raw(keep: set[str]) -> int:
    removed = 0
    if not RAW_DIR.exists():
        return 0
    for path in RAW_DIR.iterdir():
        if not path.is_file() or path.name == ".gitkeep":
            continue
        junk = path.name.startswith(JUNK_PREFIXES) or path.name not in keep
        if junk:
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pieces = toutes_les_pieces()
    keep = {piece.nom for piece in pieces}

    for index, piece in enumerate(pieces, start=1):
        ecrire_piece(RAW_DIR, piece)
        if index % 100 == 0 or index == len(pieces):
            print(f"  {index}/{len(pieces)} fichiers écrits")

    removed = _clean_raw(keep)
    counts = Counter(Path(piece.nom).suffix.lower() for piece in pieces)

    print(f"Cas métier : {SIGLE} — {ETABLISSEMENT}")
    print(f"Fichiers générés : {len(pieces)}")
    print("  " + ", ".join(f"{ext} {n}" for ext, n in sorted(counts.items())))
    print(f"Anciens fichiers retirés : {removed}")
    print(f"Dossier : {RAW_DIR}")
    print("Ensuite : indexer le dossier depuis l'administration, ou POST /ingest/scan?force=true")


if __name__ == "__main__":
    main()
