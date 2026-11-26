import shutil

from whoosh import index
from whoosh.fields import ID, KEYWORD, Schema, TEXT

from app.config import WHOOSH_INDEX_DIR
from app.models.document import Document


def _invalidate_semantic_cache() -> None:
    from app.search.semantic import invalidate_semantic_cache

    invalidate_semantic_cache()

SCHEMA = Schema(
    id=ID(stored=True, unique=True),
    title=TEXT(stored=True, field_boost=2.5),
    content=TEXT(stored=True),
    file_type=KEYWORD(stored=True),
    tags=KEYWORD(stored=True, commas=True, lowercase=True, scorable=True),
)


def _document_fields(document: Document) -> dict:
    tags = ",".join(tag.strip() for tag in document.tags if tag and tag.strip())
    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "file_type": document.file_type,
        "tags": tags,
    }


def _schema_is_current(ix) -> bool:
    names = set(ix.schema.names())
    return {"id", "title", "content", "file_type", "tags"}.issubset(names)


def get_index():
    WHOOSH_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    if index.exists_in(str(WHOOSH_INDEX_DIR)):
        ix = index.open_dir(str(WHOOSH_INDEX_DIR))
        if _schema_is_current(ix):
            return ix
        shutil.rmtree(WHOOSH_INDEX_DIR)
        WHOOSH_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    return index.create_in(str(WHOOSH_INDEX_DIR), SCHEMA)


def index_document(document: Document) -> None:
    index_documents([document])


def index_documents(documents: list[Document]) -> int:
    if not documents:
        return 0

    ix = get_index()
    writer = ix.writer()
    for document in documents:
        writer.delete_by_term("id", document.id)
        writer.add_document(**_document_fields(document))
    writer.commit()
    _invalidate_semantic_cache()
    return len(documents)


def remove_document(document_id: str) -> None:
    ix = get_index()
    writer = ix.writer()
    writer.delete_by_term("id", document_id)
    writer.commit()
    _invalidate_semantic_cache()


def rebuild_index(documents: list[Document]) -> int:
    if WHOOSH_INDEX_DIR.exists():
        shutil.rmtree(WHOOSH_INDEX_DIR)
    WHOOSH_INDEX_DIR.mkdir(parents=True, exist_ok=True)

    ix = index.create_in(str(WHOOSH_INDEX_DIR), SCHEMA)
    writer = ix.writer()
    for document in documents:
        writer.add_document(**_document_fields(document))
    writer.commit()
    _invalidate_semantic_cache()
    return len(documents)


def init_search_index(documents: list[Document]) -> None:
    if not index.exists_in(str(WHOOSH_INDEX_DIR)):
        rebuild_index(documents)
        return

    ix = index.open_dir(str(WHOOSH_INDEX_DIR))
    if not _schema_is_current(ix):
        rebuild_index(documents)


def index_is_ready() -> bool:
    try:
        if not index.exists_in(str(WHOOSH_INDEX_DIR)):
            return False
        ix = index.open_dir(str(WHOOSH_INDEX_DIR))
        return _schema_is_current(ix)
    except Exception:
        return False
