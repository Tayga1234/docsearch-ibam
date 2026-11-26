import pytest

from app.extraction import extract_text
from app.extraction.registry import get_extractor


def test_txt_extractor(sample_txt):
    result = extract_text(sample_txt)
    assert "DocSearch" in result.content
    assert "Burkina Faso" in result.content


def test_csv_extractor(sample_csv):
    result = extract_text(sample_csv)
    assert "Alice" in result.content
    assert "Ouaga" in result.content
    assert result.metadata["columns"] == ["nom", "ville"]
    assert result.metadata["row_count"] == 2


def test_docx_extractor(sample_docx):
    result = extract_text(sample_docx)
    assert "Rapport annuel" in result.content
    assert "Indexation intelligente" in result.content
    assert result.metadata["paragraph_count"] == 2


def test_pdf_extractor(sample_pdf):
    result = extract_text(sample_pdf)
    assert "Contenu extrait du PDF de test" in result.content
    assert result.metadata["page_count"] == 2
    assert result.metadata["pages_with_text"] == 1


def test_unsupported_format(isolated_storage):
    path = isolated_storage["raw_dir"] / "image.png"
    path.write_bytes(b"fake")

    with pytest.raises(ValueError, match="Format non supporté"):
        extract_text(path)


def test_get_extractor_returns_correct_type(sample_txt, sample_csv):
    assert get_extractor(sample_txt).__class__.__name__ == "TxtExtractor"
    assert get_extractor(sample_csv).__class__.__name__ == "CsvExtractor"
