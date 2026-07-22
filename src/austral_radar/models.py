"""Modelos de datos validados para las entradas y salidas del agente."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, field_validator


class EntityType(StrEnum):
    PLACE = "place"
    INSTITUTION = "institution"
    ROUTE = "route"
    INFRASTRUCTURE = "infrastructure"
    PERSON = "person"
    OTHER = "other"


class Level(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SourceType(StrEnum):
    URL = "url"
    USER_TEXT = "user_text"


class Entity(BaseModel):
    """Entidad relevante detectada dentro de una fuente."""

    name: str = Field(min_length=1, max_length=160)
    type: EntityType = EntityType.OTHER


class SourceProvenance(BaseModel):
    """Procedencia original conservada sin modificaciones."""

    type: SourceType
    url: HttpUrl | None = None


class AnalysisRequest(BaseModel):
    """Entrada mínima aceptada por el agente."""

    source_text: str = Field(min_length=20, max_length=20_000)
    source_url: HttpUrl | None = None

    @field_validator("source_text")
    @classmethod
    def normalize_source_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("El texto de la fuente no puede estar vacío.")
        return normalized


class AnalysisRecord(BaseModel):
    """Ficha estructurada producida por el agente especializado."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: str = Field(min_length=1, max_length=240)
    summary: str = Field(min_length=1, max_length=2_000)
    territory: list[str] = Field(default_factory=list, max_length=20)
    category: str = Field(default="unknown", max_length=120)
    entities: list[Entity] = Field(default_factory=list, max_length=50)
    related_project: str = Field(default="Sin clasificar", max_length=120)
    editorial_relevance: Level = Level.MEDIUM
    confidence: Level = Level.MEDIUM
    requires_human_review: bool = False
    review_reason: str = Field(default="", max_length=500)
    source: SourceProvenance

    @field_validator("territory")
    @classmethod
    def clean_territories(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for value in values:
            normalized = value.strip()
            if normalized and normalized not in cleaned:
                cleaned.append(normalized)
        return cleaned
