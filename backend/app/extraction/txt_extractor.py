from pathlib import Path

from app.extraction.base import BaseExtractor, ExtractionResult


class TxtExtractor(BaseExtractor):
    extensions = {".txt"}

    def extract(self, path: Path) -> ExtractionResult:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="latin-1")

        return ExtractionResult(content=content.strip())
