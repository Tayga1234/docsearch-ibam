from app.config import HYBRID_KEYWORD_WEIGHT, HYBRID_SEMANTIC_WEIGHT
from app.models.document import SearchHit
from app.search.keyword import keyword_search
from app.search.semantic import semantic_search

VALID_MODES = {"keyword", "semantic", "hybrid"}


def _prefer_keyword_excerpt(keyword_hit: SearchHit | None, semantic_hit: SearchHit | None) -> str:
    """Conserve les surbrillances <mark> du mode keyword quand disponibles."""
    if keyword_hit and keyword_hit.excerpt and "<mark" in keyword_hit.excerpt:
        return keyword_hit.excerpt
    if keyword_hit and keyword_hit.excerpt:
        return keyword_hit.excerpt
    if semantic_hit and semantic_hit.excerpt:
        return semantic_hit.excerpt
    return ""


def _merge_hits(keyword_hits: list[SearchHit], semantic_hits: list[SearchHit], limit: int) -> list[SearchHit]:
    keyword_by_id = {hit.id: hit for hit in keyword_hits}
    semantic_by_id = {hit.id: hit for hit in semantic_hits}
    all_ids = list(dict.fromkeys([hit.id for hit in keyword_hits] + [hit.id for hit in semantic_hits]))

    keyword_scores = {hit.id: hit.score for hit in keyword_hits}
    semantic_scores = {hit.id: hit.score for hit in semantic_hits}
    max_keyword = max(keyword_scores.values(), default=1) or 1
    max_semantic = max(semantic_scores.values(), default=1) or 1

    merged: list[SearchHit] = []
    for doc_id in all_ids:
        keyword_hit = keyword_by_id.get(doc_id)
        semantic_hit = semantic_by_id.get(doc_id)
        base_hit = keyword_hit or semantic_hit
        if base_hit is None:
            continue

        keyword_score = keyword_scores.get(doc_id, 0) / max_keyword
        semantic_score = semantic_scores.get(doc_id, 0) / max_semantic
        combined = round(
            HYBRID_KEYWORD_WEIGHT * keyword_score + HYBRID_SEMANTIC_WEIGHT * semantic_score,
            3,
        )

        merged.append(
            SearchHit(
                id=base_hit.id,
                title=base_hit.title,
                file_type=base_hit.file_type,
                score=combined,
                excerpt=_prefer_keyword_excerpt(keyword_hit, semantic_hit),
                tags=base_hit.tags,
                size_bytes=base_hit.size_bytes,
                indexed_at=base_hit.indexed_at,
                category=keyword_hit.category if keyword_hit else base_hit.category,
            )
        )

    merged.sort(key=lambda hit: hit.score, reverse=True)
    return merged[:limit]


def search_documents(query: str, limit: int = 20, mode: str = "keyword") -> list[SearchHit]:
    if mode not in VALID_MODES:
        raise ValueError(f"Mode de recherche invalide : {mode}")

    if mode == "keyword":
        return keyword_search(query, limit=limit)
    if mode == "semantic":
        return semantic_search(query, limit=limit)

    # Récupérer un pool un peu plus large pour une meilleure fusion
    pool = max(limit * 2, limit)
    keyword_hits = keyword_search(query, limit=pool)
    semantic_hits = semantic_search(query, limit=pool)
    return _merge_hits(keyword_hits, semantic_hits, limit=limit)
