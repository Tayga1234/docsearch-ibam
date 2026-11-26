import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.config import API_VERSION, PROJECT_ROOT
from app.database import init_db, list_documents
from app.indexing.whoosh_index import init_search_index

STATIC_DIR = PROJECT_ROOT / "frontend" / "dist"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def _warm_semantic_in_background() -> None:
    try:
        from app.search.semantic import warm_semantic_cache

        count = warm_semantic_cache()
        logger.info("Cache TF-IDF préchauffé (%s documents)", count)
    except Exception:
        logger.exception("Échec du préchauffage TF-IDF")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_search_index(list_documents())
    threading.Thread(target=_warm_semantic_in_background, daemon=True).start()
    yield


OPENAPI_TAGS = [
    {"name": "Santé", "description": "État du service, version et volume du fonds."},
    {"name": "Authentification", "description": "Connexion Bearer, profil et déconnexion."},
    {"name": "Ingestion", "description": "Scan du dossier data/raw et téléversement de fichiers."},
    {"name": "Recherche", "description": "Modes mots-clés, sémantique et hybride."},
    {"name": "Documents", "description": "Liste, fiche enrichie et suppression."},
    {"name": "Index", "description": "Reconstruction de l’index Whoosh."},
]

app = FastAPI(
    title="DocSearch API",
    description=(
        "Indexation intelligente de données pour la recherche d’information.\n\n"
        "L’API REST expose l’ingestion, la recherche et l’administration. "
        "Les données sont validées par Pydantic. Cette documentation OpenAPI "
        "est générée automatiquement.\n\n"
        "**Erreurs :** format non supporté ou fichier trop volumineux → 400 "
        "(limite 20 Mo). Requête vide, mode inconnu ou limite hors intervalle → 400. "
        "Identifiant inconnu → 404. Les actions destructives exigent `confirm=true`."
    ),
    version=API_VERSION,
    lifespan=lifespan,
    openapi_tags=OPENAPI_TAGS,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_origin_regex=(
        r"https?://(localhost|127\.0\.0\.1)(:\d+)?|"
        r"https://[\w-]+\.onrender\.com"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def _mount_frontend() -> None:
    if not STATIC_DIR.is_dir():
        logger.info("Frontend statique absent (%s) — API seule", STATIC_DIR)
        return

    assets_dir = STATIC_DIR / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str):
        # Fichiers publics du build (logo, favicon…)
        candidate = STATIC_DIR / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        index = STATIC_DIR / "index.html"
        if index.is_file():
            return FileResponse(index)
        return {"detail": "Frontend non disponible"}

    logger.info("Frontend servi depuis %s", STATIC_DIR)


_mount_frontend()
