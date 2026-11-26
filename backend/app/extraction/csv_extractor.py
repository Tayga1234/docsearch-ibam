import csv
from pathlib import Path

from app.extraction.base import BaseExtractor, ExtractionResult

ENCODINGS = ("utf-8-sig", "utf-8", "latin-1", "cp1252")


def _decode_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    last_error: Exception | None = None
    for encoding in ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError as exc:
            last_error = exc
    raise ValueError(f"Impossible de décoder {path.name}: {last_error}")


class CsvExtractor(BaseExtractor):
    extensions = {".csv"}

    def extract(self, path: Path) -> ExtractionResult:
        text, encoding = _decode_text(path)
        rows: list[str] = []
        columns: list[str] = []

        reader = csv.DictReader(text.splitlines())
        columns = list(reader.fieldnames or [])

        for row in reader:
            row_text = " | ".join(
                f"{key}: {value}" for key, value in row.items() if value
            )
            if row_text:
                rows.append(row_text)

        return ExtractionResult(
            content="\n".join(rows).strip(),
            metadata={
                "columns": columns,
                "row_count": len(rows),
                "encoding": encoding,
            },
        )
