import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.config import DB_DIR, DB_PATH
from app.models.document import Document


def _connect() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source_path TEXT NOT NULL UNIQUE,
                file_type TEXT NOT NULL,
                mime_type TEXT,
                size_bytes INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                indexed_at TEXT NOT NULL,
                metadata TEXT NOT NULL DEFAULT '{}',
                summary TEXT,
                tags TEXT NOT NULL DEFAULT '[]'
            )
            """
        )


def _row_to_document(row: sqlite3.Row) -> Document:
    return Document(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        source_path=row["source_path"],
        file_type=row["file_type"],
        mime_type=row["mime_type"],
        size_bytes=row["size_bytes"],
        created_at=datetime.fromisoformat(row["created_at"]),
        indexed_at=datetime.fromisoformat(row["indexed_at"]),
        metadata=json.loads(row["metadata"]),
        summary=row["summary"],
        tags=json.loads(row["tags"]),
    )


def get_document_by_path(source_path: str) -> Document | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM documents WHERE source_path = ?",
            (source_path,),
        ).fetchone()
    return _row_to_document(row) if row else None


# Normalise les chemins Windows/Unix pour détecter le préfixe sci_
_PATH_NORM = "LOWER(REPLACE(source_path, '\\', '/'))"
_IS_SCIENTIFIC = (
    f"({_PATH_NORM} LIKE '%/sci_%' OR {_PATH_NORM} LIKE 'sci_%')"
)

SORT_SQL = {
    "date": "indexed_at DESC",
    "title": "LOWER(title) ASC",
    "type": "file_type ASC, indexed_at DESC",
    # Scientifique (sci_) d'abord, puis archives IBAM, puis date
    "category": f"CASE WHEN {_IS_SCIENTIFIC} THEN 0 ELSE 1 END ASC, indexed_at DESC",
}

CATEGORY_SQL = {
    "scientific": _IS_SCIENTIFIC,
    "archives": f"NOT {_IS_SCIENTIFIC}",
}


def _filter_clauses(
    *,
    file_type: str | None = None,
    tag: str | None = None,
    q: str | None = None,
    category: str | None = None,
) -> tuple[list[str], list[object]]:
    clauses: list[str] = []
    params: list[object] = []

    if file_type:
        clauses.append("LOWER(file_type) = LOWER(?)")
        params.append(file_type)

    if tag:
        clauses.append("LOWER(tags) LIKE ?")
        params.append(f'%"{tag.lower()}"%')

    if q:
        clauses.append("(LOWER(title) LIKE ? OR LOWER(content) LIKE ? OR LOWER(tags) LIKE ?)")
        needle = f"%{q.lower()}%"
        params.extend([needle, needle, needle])

    if category in CATEGORY_SQL:
        clauses.append(CATEGORY_SQL[category])

    return clauses, params


def list_documents(
    *,
    limit: int | None = None,
    offset: int = 0,
    file_type: str | None = None,
    tag: str | None = None,
    q: str | None = None,
    category: str | None = None,
    sort: str = "category",
) -> list[Document]:
    clauses, params = _filter_clauses(file_type=file_type, tag=tag, q=q, category=category)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    order = SORT_SQL.get(sort, SORT_SQL["category"])
    sql = f"SELECT * FROM documents {where} ORDER BY {order}"

    if limit is not None:
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

    with _connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_document(row) for row in rows]


def count_documents(
    *,
    file_type: str | None = None,
    tag: str | None = None,
    q: str | None = None,
    category: str | None = None,
) -> int:
    clauses, params = _filter_clauses(file_type=file_type, tag=tag, q=q, category=category)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with _connect() as conn:
        row = conn.execute(f"SELECT COUNT(*) AS total FROM documents {where}", params).fetchone()
    return int(row["total"]) if row else 0


def count_by_file_type() -> dict[str, int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT LOWER(file_type) AS file_type, COUNT(*) AS total FROM documents GROUP BY LOWER(file_type)"
        ).fetchall()
    return {str(row["file_type"]): int(row["total"]) for row in rows}


def count_by_category() -> dict[str, int]:
    scientific = count_documents(category="scientific")
    archives = count_documents(category="archives")
    return {"scientific": scientific, "archives": archives}


def latest_indexed_at() -> str | None:
    with _connect() as conn:
        row = conn.execute("SELECT MAX(indexed_at) AS last FROM documents").fetchone()
    return str(row["last"]) if row and row["last"] else None


def get_document(document_id: str) -> Document | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM documents WHERE id = ?",
            (document_id,),
        ).fetchone()
    return _row_to_document(row) if row else None


def get_documents_by_ids(document_ids: list[str]) -> dict[str, Document]:
    """Charge plusieurs fiches en une seule requête (évite N allers-retours SQLite)."""
    ids = [doc_id for doc_id in document_ids if doc_id]
    if not ids:
        return {}
    placeholders = ",".join("?" for _ in ids)
    with _connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM documents WHERE id IN ({placeholders})",
            ids,
        ).fetchall()
    return {row["id"]: _row_to_document(row) for row in rows}


def delete_document(document_id: str) -> bool:
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        return cursor.rowcount > 0


def upsert_document(document: Document) -> Document:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    existing = get_document_by_path(document.source_path)

    if existing:
        document.id = existing.id
        document.created_at = existing.created_at

    document.indexed_at = now
    if document.created_at is None:
        document.created_at = now

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO documents (
                id, title, content, source_path, file_type, mime_type,
                size_bytes, created_at, indexed_at, metadata, summary, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_path) DO UPDATE SET
                title = excluded.title,
                content = excluded.content,
                file_type = excluded.file_type,
                mime_type = excluded.mime_type,
                size_bytes = excluded.size_bytes,
                indexed_at = excluded.indexed_at,
                metadata = excluded.metadata,
                summary = excluded.summary,
                tags = excluded.tags
            """,
            (
                document.id,
                document.title,
                document.content,
                document.source_path,
                document.file_type,
                document.mime_type,
                document.size_bytes,
                document.created_at.isoformat(),
                document.indexed_at.isoformat(),
                json.dumps(document.metadata, ensure_ascii=False),
                document.summary,
                json.dumps(document.tags, ensure_ascii=False),
            ),
        )
    return document


def create_document_from_file(
    source_path: Path,
    title: str,
    content: str,
    file_type: str,
    mime_type: str | None,
    metadata: dict | None = None,
) -> Document:
    stat = source_path.stat()
    return Document(
        id=str(uuid4()),
        title=title,
        content=content,
        source_path=str(source_path.resolve()),
        file_type=file_type,
        mime_type=mime_type,
        size_bytes=stat.st_size,
        metadata=metadata or {},
    )
