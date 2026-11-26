from whoosh.highlight import ContextFragmenter, Formatter, get_text
from whoosh.qparser import MultifieldParser, QueryParserError

from app.classification import classify_path
from app.database import get_documents_by_ids
from app.indexing.whoosh_index import get_index
from app.models.document import SearchHit

FIELD_BOOSTS = {
    "title": 2.5,
    "tags": 1.8,
    "content": 1.0,
}


class MarkFormatter(Formatter):
    """Surlignage minimal <mark>…</mark> sans attributs HTML."""

    def format_token(self, text, token, replace=False):
        return f"<mark>{get_text(text, token, replace)}</mark>"


def _build_excerpt(hit) -> str:
    highlights = hit.highlights("content", top=1)
    if highlights:
        return highlights
    highlights = hit.highlights("title", top=1)
    if highlights:
        return highlights
    highlights = hit.highlights("tags", top=1)
    if highlights:
        return highlights
    content = hit.get("content", "")
    return content[:200] + ("..." if len(content) > 200 else "")


def _parse_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in str(raw).split(",") if part.strip()]


def keyword_search(query: str, limit: int = 20) -> list[SearchHit]:
    cleaned = query.strip()
    if not cleaned:
        return []

    ix = get_index()
    parser = MultifieldParser(
        ["title", "content", "tags"],
        schema=ix.schema,
        fieldboosts=FIELD_BOOSTS,
    )

    with ix.searcher() as searcher:
        try:
            parsed_query = parser.parse(cleaned)
        except (QueryParserError, ValueError):
            special = set(':()[]{}^~*?"+\\')
            escaped = "".join(f"\\{ch}" if ch in special else ch for ch in cleaned)
            parsed_query = parser.parse(escaped)
        results = searcher.search(parsed_query, limit=limit)
        results.fragmenter = ContextFragmenter(maxchars=250, surround=40)
        results.formatter = MarkFormatter()

        result_rows = list(results)
        stored = get_documents_by_ids([row["id"] for row in result_rows])

        hits: list[SearchHit] = []
        for result in result_rows:
            document = stored.get(result["id"])
            tags = document.tags if document else _parse_tags(result.get("tags"))
            hits.append(
                SearchHit(
                    id=result["id"],
                    title=result["title"],
                    file_type=result.get("file_type") or "",
                    score=round(float(result.score), 3),
                    excerpt=_build_excerpt(result),
                    tags=tags,
                    size_bytes=document.size_bytes if document else 0,
                    indexed_at=document.indexed_at if document else None,
                    category=classify_path(document.source_path) if document else "archives",
                )
            )
        return hits
