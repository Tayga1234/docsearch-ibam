from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DB_DIR = PROJECT_ROOT / "data" / "db"
DB_PATH = DB_DIR / "documents.db"
WHOOSH_INDEX_DIR = DB_DIR / "whoosh_index"

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx", ".csv"}

# Recherche hybride : pondération normalisée keyword / semantic
HYBRID_KEYWORD_WEIGHT = 0.6
HYBRID_SEMANTIC_WEIGHT = 0.4

# Upload
MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 Mo

API_VERSION = "0.7.0"
