from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    title: str
    content: str
    source_path: str
    file_type: str
    mime_type: str | None = None
    size_bytes: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    indexed_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    summary: str | None = None
    tags: list[str] = Field(default_factory=list)


class DocumentSummary(BaseModel):
    id: str
    title: str
    file_type: str
    size_bytes: int
    indexed_at: datetime | None
    excerpt: str
    tags: list[str] = Field(default_factory=list)
    category: str = "archives"


class ScanResponse(BaseModel):
    scanned: int
    indexed: int
    skipped: int
    errors: list[str]


class UploadResponse(BaseModel):
    status: str
    document: DocumentSummary


class SearchHit(BaseModel):
    id: str
    title: str
    file_type: str
    score: float
    excerpt: str
    tags: list[str] = Field(default_factory=list)
    size_bytes: int = 0
    indexed_at: datetime | None = None
    category: str = "archives"


class SearchResponse(BaseModel):
    query: str
    mode: str
    total: int
    results: list[SearchHit]


class CompareResponse(BaseModel):
    query: str
    modes: dict[str, list[SearchHit]]


class DocumentListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[DocumentSummary]


class DeleteDocumentResponse(BaseModel):
    deleted: bool
    id: str


class RebuildIndexResponse(BaseModel):
    indexed: int
