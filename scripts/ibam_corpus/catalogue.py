from .bureautique import pieces_docx, pieces_pdf
from .csv_pieces import pieces as pieces_csv
from .expansion import pieces as pieces_expansion
from .modele import Piece
from .txt_direction import pieces as pieces_direction
from .txt_dsi_archives import pieces as pieces_dsi
from .txt_rh_finance import pieces as pieces_rh
from .txt_scolarite import pieces as pieces_scolarite
from .txt_stages_qualite import pieces as pieces_stages

CORPUS_MINIMUM = 1000


def pieces_noyau() -> list[Piece]:
    return (
        pieces_direction()
        + pieces_scolarite()
        + pieces_rh()
        + pieces_dsi()
        + pieces_stages()
        + pieces_csv()
        + pieces_docx()
        + pieces_pdf()
    )


def toutes_les_pieces() -> list[Piece]:
    ensemble = pieces_noyau() + pieces_expansion()
    noms = [piece.nom for piece in ensemble]
    if len(noms) != len(set(noms)):
        doubles = sorted({nom for nom in noms if noms.count(nom) > 1})
        raise SystemExit(f"Noms de fichiers en double : {doubles}")
    if len(ensemble) < CORPUS_MINIMUM:
        raise SystemExit(
            f"Le corpus doit contenir au moins {CORPUS_MINIMUM} pièces, {len(ensemble)} obtenues."
        )
    return ensemble
