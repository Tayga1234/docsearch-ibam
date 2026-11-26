import mimetypes
from pathlib import Path

from app.extraction.base import BaseExtractor, ExtractionResult
from app.extraction.csv_extractor import CsvExtractor
from app.extraction.docx_extractor import DocxExtractor
from app.extraction.pdf_extractor import PdfExtractor
from app.extraction.txt_extractor import TxtExtractor

EXTRACTORS: list[BaseExtractor] = [
    TxtExtractor(),
    PdfExtractor(),
    DocxExtractor(),
    CsvExtractor(),
]


def get_extractor(path: Path) -> BaseExtractor | None:
    for extractor in EXTRACTORS:
        if extractor.supports(path):
            return extractor
    return None


def extract_text(path: Path) -> ExtractionResult:
    extractor = get_extractor(path)
    if extractor is None:
        raise ValueError(f"Format non supporté : {path.suffix}")

    mime_type, _ = mimetypes.guess_type(path.name)
    result = extractor.extract(path)
    result.metadata["mime_type"] = mime_type
    return result
