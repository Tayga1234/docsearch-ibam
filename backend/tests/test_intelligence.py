from app.intelligence.enricher import enrich_document
from app.intelligence.entities import extract_entities
from app.intelligence.tagging import generate_summary, generate_tags
from app.models.document import Document


def test_generate_tags_includes_file_type_and_keywords():
    tags = generate_tags("rapport.txt", "Rapport annuel sur l indexation intelligente", "txt")

    assert "txt" in tags
    assert "rapport" in tags
    assert "indexation" in tags or "intelligente" in tags


def test_generate_summary_extractive():
    content = (
        "Le projet DocSearch permet l'indexation intelligente. "
        "Les documents hétérogènes sont analysés automatiquement. "
        "La recherche hybride combine mots-clés et similarité."
    )
    summary = generate_summary(content, max_length=180)
    assert summary
    assert "DocSearch" in summary or "indexation" in summary.lower()


def test_extract_entities_detects_dates_authors_and_keywords():
    content = (
        "Vers une indexation intelligente\n\n"
        "Auteurs : I. Sawadogo (2iE), M. Ouédraogo (IBAM)\n"
        "Année : 2024\n"
        "Domaine : Recherche d'information\n"
        "Mots-clés : BM25, TF-IDF, index inversé\n\n"
        "Ouagadougou, le 12 mars 2024\n"
        "Contact : fatou@ibam.bf\n"
    )
    entities = extract_entities(content)
    assert any("2024" in item or "mars" in item.lower() for item in entities["dates"])
    assert any("Sawadogo" in item for item in entities["authors"])
    assert "BM25" in entities["keywords"] or any("BM25" in item for item in entities["keywords"])
    assert any("IBAM" in item.upper() for item in entities["organizations"])
    assert "fatou@ibam.bf" in entities["emails"]


def test_enrich_document_adds_tags_summary_and_entities():
    document = Document(
        id="1",
        title="contacts.csv",
        content="nom: Amadou | ville: Ouagadougou | email: amadou@example.com",
        source_path="/tmp/contacts.csv",
        file_type="csv",
    )

    enriched = enrich_document(document)

    assert enriched.tags
    assert enriched.summary
    assert "emails" in enriched.metadata["entities"]
    assert "amadou@example.com" in enriched.metadata["entities"]["emails"]
