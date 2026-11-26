import logging
import time
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, Header, HTTPException, Query, UploadFile

from app.auth import AuthUser, authenticate, create_session, drop_session, get_current_user, require_admin
from app.classification import CATEGORY_ARCHIVES, CATEGORY_SCIENTIFIC, classify_path
from app.config import (
    API_VERSION,
    HYBRID_KEYWORD_WEIGHT,
    HYBRID_SEMANTIC_WEIGHT,
    MAX_UPLOAD_BYTES,
    RAW_DATA_DIR,
    SUPPORTED_EXTENSIONS,
)
from app.database import (
    count_by_category,
    count_by_file_type,
    count_documents,
    delete_document,
    get_document,
    latest_indexed_at,
    list_documents,
    upsert_document,
)
from app.ingestion import ingest_file, save_uploaded_file, scan_raw_directory
from app.indexing.whoosh_index import index_is_ready, rebuild_index, remove_document
from app.intelligence import enrich_document
from app.models.auth import AuthUserResponse, LoginRequest, LoginResponse
from app.models.document import (
    CompareResponse,
    DeleteDocumentResponse,
    Document,
    DocumentListResponse,
    DocumentSummary,
    RebuildIndexResponse,
    ScanResponse,
    SearchResponse,
    UploadResponse,
)
from app.search import search_documents

logger = logging.getLogger(__name__)
router = APIRouter()


def _to_summary(document: Document) -> DocumentSummary:
    return DocumentSummary(
        id=document.id,
        title=document.title,
        file_type=document.file_type,
        size_bytes=document.size_bytes,
        indexed_at=document.indexed_at,
        excerpt=document.summary or (
            document.content[:200] + ("..." if len(document.content) > 200 else "")
        ),
        tags=document.tags,
        category=classify_path(document.source_path),
    )


@router.post(
    "/auth/login",
    response_model=LoginResponse,
    tags=["Authentification"],
    summary="Authentification (jeton Bearer)",
)
def login(payload: LoginRequest):
    user = authenticate(payload.username, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Identifiant ou mot de passe incorrect")
    token = create_session(user)
    return LoginResponse(token=token, user=AuthUserResponse(**user.to_public()))


@router.get(
    "/auth/me",
    response_model=AuthUserResponse,
    tags=["Authentification"],
    summary="Profil de la session",
)
def me(user: AuthUser = Depends(get_current_user)):
    return AuthUserResponse(**user.to_public())


@router.post(
    "/auth/logout",
    tags=["Authentification"],
    summary="Fermeture de session",
)
def logout(authorization: str | None = Header(default=None), user: AuthUser = Depends(get_current_user)):
    if authorization and authorization.lower().startswith("bearer "):
        drop_session(authorization.split(" ", 1)[1].strip())
    return {"logged_out": True, "username": user.username}


def _raw_file_count() -> int:
    if not RAW_DATA_DIR.exists():
        return 0
    return sum(
        1
        for path in RAW_DATA_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


@router.get(
    "/health",
    tags=["Santé"],
    summary="État du service et nombre de documents",
)
def health():
    types = count_by_file_type()
    return {
        "status": "ok",
        "service": "DocSearch API",
        "version": API_VERSION,
        "documents": count_documents(),
        "index_ready": index_is_ready(),
        "formats": {
            "txt": types.get("txt", 0),
            "pdf": types.get("pdf", 0),
            "docx": types.get("docx", 0),
            "csv": types.get("csv", 0),
        },
        "categories": count_by_category(),
        "modes": ["keyword", "semantic", "hybrid"],
        "hybrid": {
            "keyword": HYBRID_KEYWORD_WEIGHT,
            "semantic": HYBRID_SEMANTIC_WEIGHT,
        },
        "supported": sorted(SUPPORTED_EXTENSIONS),
        "max_upload_mb": MAX_UPLOAD_BYTES // (1024 * 1024),
        "raw_files": _raw_file_count(),
        "last_indexed_at": latest_indexed_at(),
        "store": "SQLite",
        "engine": "Whoosh",
    }


@router.post(
    "/ingest/scan",
    response_model=ScanResponse,
    tags=["Ingestion"],
    summary="Indexer le dossier data/raw",
)
def ingest_scan(
    background_tasks: BackgroundTasks,
    force: bool = Query(False, description="Réindexer les fichiers déjà connus."),
    _: AuthUser = Depends(require_admin),
):
    result = scan_raw_directory(force=force)
    from app.search.semantic import warm_semantic_cache

    background_tasks.add_task(warm_semantic_cache)
    return ScanResponse(
        scanned=result.scanned,
        indexed=result.indexed,
        skipped=result.skipped,
        errors=result.errors,
    )


@router.post(
    "/ingest/upload",
    response_model=UploadResponse,
    tags=["Ingestion"],
    summary="Téléverser et indexer un ou plusieurs fichiers",
    responses={400: {"description": "Format non supporté, fichier vide ou trop volumineux (max 20 Mo)."}},
)
async def ingest_upload(
    file: UploadFile = File(..., description="Fichier PDF, DOCX, TXT ou CSV (max 20 Mo)."),
    _: AuthUser = Depends(require_admin),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier manquant")

    extension = Path(file.filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Format non supporté : {extension}",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Fichier vide")

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux (max {MAX_UPLOAD_BYTES // (1024 * 1024)} Mo)",
        )

    try:
        saved_path = save_uploaded_file(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = ingest_file(saved_path, force=True)
    document = get_document(result.document_id) if result.document_id else None

    if document is None:
        raise HTTPException(status_code=500, detail="Échec de l'indexation")

    return UploadResponse(status=result.status, document=_to_summary(document))


@router.get(
    "/search",
    response_model=SearchResponse,
    tags=["Recherche"],
    summary="Recherche selon le mode choisi",
    responses={400: {"description": "Requête vide, mode inconnu ou limite hors intervalle."}},
)
def search(
    q: str = Query("", description="Texte de la requête. Une chaîne vide produit une erreur 400."),
    limit: int = Query(100, description="Nombre maximal de résultats (1 à 100)."),
    mode: str = Query("keyword", description="keyword, semantic ou hybrid."),
):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Paramètre de recherche 'q' requis")

    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Le paramètre limit doit être entre 1 et 100")

    if mode not in {"keyword", "semantic", "hybrid"}:
        raise HTTPException(
            status_code=400,
            detail="Le paramètre mode doit être keyword, semantic ou hybrid",
        )

    started = time.perf_counter()
    try:
        results = search_documents(q, limit=limit, mode=mode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        logger.exception("Échec de la recherche q=%r mode=%s", q, mode)
        raise HTTPException(
            status_code=400,
            detail="Requête invalide. Essayez des mots simples, sans caractères spéciaux.",
        )

    logger.info(
        "search q=%r mode=%s results=%s duration_ms=%.1f",
        q,
        mode,
        len(results),
        (time.perf_counter() - started) * 1000,
    )
    return SearchResponse(query=q, mode=mode, total=len(results), results=results)


@router.get(
    "/search/compare",
    response_model=CompareResponse,
    tags=["Recherche"],
    summary="Comparaison des trois modes (top 3)",
    responses={400: {"description": "Requête vide."}},
)
def search_compare(
    q: str = Query("", description="Texte de la requête. Une chaîne vide produit une erreur 400."),
):
    """Retourne le top 3 de chaque mode pour une même requête."""
    if not q.strip():
        raise HTTPException(status_code=400, detail="Paramètre de recherche 'q' requis")
    try:
        modes = {
            "keyword": search_documents(q, limit=3, mode="keyword"),
            "semantic": search_documents(q, limit=3, mode="semantic"),
            "hybrid": search_documents(q, limit=3, mode="hybrid"),
        }
    except Exception:
        logger.exception("Échec de la comparaison q=%r", q)
        raise HTTPException(status_code=400, detail="Impossible de comparer les modes pour cette requête.")
    return CompareResponse(query=q, modes=modes)


def require_action_confirm(confirm: bool) -> None:
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Action sensible : confirmez avec le paramètre confirm=true.",
        )


@router.post(
    "/index/rebuild",
    response_model=RebuildIndexResponse,
    tags=["Index"],
    summary="Reconstruction de l’index",
    responses={400: {"description": "Confirmation manquante (confirm=true)."}},
)
def rebuild_search_index(
    confirm: bool = Query(False, description="Doit valoir true pour confirmer la reconstruction."),
    _: AuthUser = Depends(require_admin),
):
    require_action_confirm(confirm)
    documents = [enrich_document(document) for document in list_documents()]
    for document in documents:
        upsert_document(document)
    indexed = rebuild_index(documents)
    return RebuildIndexResponse(indexed=indexed)


@router.get(
    "/documents",
    response_model=DocumentListResponse,
    tags=["Documents"],
    summary="Liste des documents",
)
def get_documents(
    limit: int = Query(100, description="Taille de page (1 à 200)."),
    offset: int = Query(0, description="Décalage de pagination (>= 0)."),
    file_type: str | None = Query(None, description="Filtrer par extension (pdf, docx, txt, csv)."),
    tag: str | None = Query(None, description="Filtrer par étiquette."),
    q: str | None = Query(None, description="Filtrer par titre ou extrait."),
    category: str | None = Query(
        None,
        description="Classe du fonds : scientific ou archives.",
    ),
    sort: str = Query("category", description="Tri : category, date, title ou type."),
):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="Le paramètre limit doit être entre 1 et 200")
    if offset < 0:
        raise HTTPException(status_code=400, detail="Le paramètre offset doit être >= 0")
    if sort not in {"category", "date", "title", "type"}:
        raise HTTPException(
            status_code=400,
            detail="Le paramètre sort doit être category, date, title ou type",
        )
    if category and category not in {CATEGORY_SCIENTIFIC, CATEGORY_ARCHIVES}:
        raise HTTPException(
            status_code=400,
            detail="Le paramètre category doit être scientific ou archives",
        )

    total = count_documents(file_type=file_type, tag=tag, q=q, category=category)
    documents = list_documents(
        limit=limit,
        offset=offset,
        file_type=file_type,
        tag=tag,
        q=q,
        category=category,
        sort=sort,
    )
    return DocumentListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[_to_summary(doc) for doc in documents],
    )


@router.get(
    "/documents/{document_id}",
    response_model=Document,
    tags=["Documents"],
    summary="Détail enrichi",
    responses={404: {"description": "Document introuvable."}},
)
def get_document_detail(document_id: str):
    document = get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document introuvable")
    return document


@router.delete(
    "/documents/{document_id}",
    response_model=DeleteDocumentResponse,
    tags=["Documents"],
    summary="Suppression base et index",
    responses={
        400: {"description": "Confirmation manquante (confirm=true)."},
        404: {"description": "Document introuvable."},
    },
)
def remove_document_endpoint(
    document_id: str,
    confirm: bool = Query(False, description="Doit valoir true pour confirmer la suppression."),
    _: AuthUser = Depends(require_admin),
):
    require_action_confirm(confirm)
    document = get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document introuvable")

    source = Path(document.source_path)
    deleted = delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document introuvable")

    remove_document(document_id)

    try:
        raw_root = RAW_DATA_DIR.resolve()
        if source.exists() and raw_root in source.resolve().parents:
            source.unlink()
    except OSError as exc:
        logger.warning("Impossible de supprimer le fichier source %s: %s", source, exc)

    return DeleteDocumentResponse(deleted=True, id=document_id)
