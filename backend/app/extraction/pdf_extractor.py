from pathlib import Path

import pdfplumber

from app.extraction.base import BaseExtractor, ExtractionResult


class PdfExtractor(BaseExtractor):
    extensions = {".pdf"}

    def extract(self, path: Path) -> ExtractionResult:
        pages_text: list[str] = []
        total_pages = 0

        with pdfplumber.open(path) as pdf:
            total_pages = len(pdf.pages)
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)

        return ExtractionResult(
            content="\n\n".join(pages_text).strip(),
            metadata={
                "page_count": total_pages,
                "pages_with_text": len(pages_text),
            },
        )
