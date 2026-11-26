from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ExtractionResult:
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseExtractor:
    extensions: set[str]

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def extract(self, path: Path) -> ExtractionResult:
        raise NotImplementedError
