"""Pruebas iniciales del contrato de datos del agente."""

import pytest
from pydantic import ValidationError

from austral_radar.models import (
    AnalysisRecord,
    AnalysisRequest,
    Entity,
    EntityType,
    SourceProvenance,
    SourceType,
)


def test_request_rejects_short_text() -> None:
    with pytest.raises(ValidationError):
        AnalysisRequest(source_text="muy corto")


def test_request_accepts_valid_text_and_url() -> None:
    request = AnalysisRequest(
        source_text="Fuente documental suficiente para ejecutar el análisis especializado.",
        source_url="https://example.org/source",
    )

    assert request.source_text.startswith("Fuente documental")
    assert str(request.source_url) == "https://example.org/source"


def test_analysis_record_serializes_valid_structure() -> None:
    record = AnalysisRecord(
        title="Conectividad austral",
        summary="La fuente describe una conexión territorial que requiere revisión documental.",
        territory=["Puerto Williams", "Puerto Williams", "Punta Arenas"],
        category="conectividad",
        entities=[Entity(name="Puerto Williams", type=EntityType.PLACE)],
        source=SourceProvenance(type=SourceType.USER_TEXT),
    )

    payload = record.model_dump(mode="json")

    assert payload["territory"] == ["Puerto Williams", "Punta Arenas"]
    assert payload["entities"][0]["type"] == "place"
    assert payload["source"]["type"] == "user_text"
