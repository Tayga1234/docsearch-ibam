from app.intelligence.entities import extract_entities
from app.intelligence.tagging import generate_summary, generate_tags
from app.models.document import Document


def enrich_document(document: Document) -> Document:
    document.tags = generate_tags(document.title, document.content, document.file_type)
    document.summary = generate_summary(document.content)
    # Titre + contenu : les auteurs et dates figurent souvent en tête
    blob = f"{document.title}\n{document.content}"
    document.metadata = {
        **document.metadata,
        "entities": extract_entities(blob),
        "category": next(
            (tag for tag in document.tags if tag in {"rapport", "contacts", "technique", "administratif"}),
            None,
        ),
    }
    return document
