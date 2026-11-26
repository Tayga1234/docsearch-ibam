import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.classification import classify_path
from app.database import list_documents
from app.models.document import SearchHit

_cache: dict | None = None

# Limite le texte vectorisé : accélère le fit sans changer le comportement global.
_CONTENT_CHARS = 3500


def invalidate_semantic_cache() -> None:
    global _cache
    _cache = None


def warm_semantic_cache() -> int:
    """Prépare la matrice TF-IDF pour éviter le pic de la première requête."""
    cache = _get_cache()
    return len(cache.get("documents") or [])


def _build_cache() -> dict:
    documents = list_documents()
    if not documents:
        return {"documents": [], "vectorizer": None, "matrix": None}

    corpus = [
        f"{document.title}\n{' '.join(document.tags)}\n{document.content[:_CONTENT_CHARS]}"
        for document in documents
    ]
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform(corpus)
    return {"documents": documents, "vectorizer": vectorizer, "matrix": matrix}


def _get_cache() -> dict:
    global _cache
    if _cache is None:
        _cache = _build_cache()
    return _cache


def semantic_search(query: str, limit: int = 20) -> list[SearchHit]:
    cleaned = query.strip()
    if not cleaned:
        return []

    cache = _get_cache()
    documents = cache["documents"]
    vectorizer = cache["vectorizer"]
    matrix = cache["matrix"]

    if not documents or vectorizer is None or matrix is None:
        return []

    query_matrix = vectorizer.transform([cleaned])
    scores = cosine_similarity(query_matrix, matrix).flatten()

    # Top-k sans tri complet de tout le fonds
    positive = np.flatnonzero(scores > 0)
    if positive.size == 0:
        return []

    top_n = min(limit, positive.size)
    if positive.size <= top_n:
        chosen = positive[np.argsort(scores[positive])[::-1]]
    else:
        part = np.argpartition(scores[positive], -top_n)[-top_n:]
        chosen = positive[part[np.argsort(scores[positive][part])[::-1]]]

    hits: list[SearchHit] = []
    for index in chosen:
        document = documents[int(index)]
        score = float(scores[int(index)])
        excerpt = document.summary or document.content[:200]
        hits.append(
            SearchHit(
                id=document.id,
                title=document.title,
                file_type=document.file_type,
                score=round(score, 3),
                excerpt=excerpt + ("..." if not document.summary and len(document.content) > 200 else ""),
                tags=document.tags,
                size_bytes=document.size_bytes,
                indexed_at=document.indexed_at,
                category=classify_path(document.source_path),
            )
        )
    return hits
