from pathlib import Path

from docx import Document as DocxDocument

from app.extraction.base import BaseExtractor, ExtractionResult


class DocxExtractor(BaseExtractor):
    extensions = {".docx"}

    def extract(self, path: Path) -> ExtractionResult:
        doc = DocxDocument(path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        return ExtractionResult(
            content="\n".join(paragraphs),
            metadata={"paragraph_count": len(paragraphs)},
        )
