"""Pruebas unitarias del analizador simulado y determinista."""

from austral_radar.models import (
    AnalysisRecord,
    AnalysisRequest,
    EntityType,
    Level,
    SourceType,
)
from austral_radar.mock_analyzer import analyze_mock


def _make_request(text: str, url: str | None = None) -> AnalysisRequest:
    """Helper para crear un AnalysisRequest válido."""
    return AnalysisRequest(source_text=text, source_url=url)


# ---------------------------------------------------------------------------
# Texto sobre Puerto Williams
# ---------------------------------------------------------------------------


class TestPuertoWilliams:
    """Verifica detección de Puerto Williams como territorio y entidad."""

    def test_detects_puerto_williams_territory(self) -> None:
        request = _make_request(
            "El gobierno anunció mejoras de infraestructura en Puerto Williams "
            "para fortalecer la conectividad austral."
        )
        record = analyze_mock(request)

        assert "Puerto Williams" in record.territory

    def test_detects_puerto_williams_entity(self) -> None:
        request = _make_request(
            "El gobierno anunció mejoras de infraestructura en Puerto Williams "
            "para fortalecer la conectividad austral."
        )
        record = analyze_mock(request)

        entity_names = [e.name for e in record.entities]
        assert "Puerto Williams" in entity_names

        pw_entity = next(e for e in record.entities if e.name == "Puerto Williams")
        assert pw_entity.type == EntityType.PLACE


# ---------------------------------------------------------------------------
# Distinción entre Puerto Williams y Puerto Toro
# ---------------------------------------------------------------------------


class TestPuertoWilliamsVsToro:
    """Verifica que el analizador distingue ambos puertos."""

    def test_text_with_both_detects_both(self) -> None:
        request = _make_request(
            "La ruta conecta Puerto Williams con Puerto Toro, "
            "dos localidades del extremo austral de Chile."
        )
        record = analyze_mock(request)

        assert "Puerto Williams" in record.territory
        assert "Puerto Toro" in record.territory

    def test_text_only_toro_does_not_include_williams(self) -> None:
        request = _make_request(
            "Puerto Toro es considerado el pueblo más austral del mundo, "
            "ubicado en la Isla Navarino."
        )
        record = analyze_mock(request)

        assert "Puerto Toro" in record.territory
        assert "Puerto Williams" not in record.territory

    def test_entities_are_distinct(self) -> None:
        request = _make_request(
            "Puerto Williams y Puerto Toro son localidades diferentes en Navarino."
        )
        record = analyze_mock(request)

        entity_names = [e.name for e in record.entities]
        assert "Puerto Williams" in entity_names
        assert "Puerto Toro" in entity_names


# ---------------------------------------------------------------------------
# Contenido sobre conectividad
# ---------------------------------------------------------------------------


class TestConectividad:
    """Verifica detección de categoría conectividad."""

    def test_detects_conectividad_category(self) -> None:
        request = _make_request(
            "El plan busca mejorar la conectividad aérea y marítima "
            "en la región de Magallanes."
        )
        record = analyze_mock(request)

        assert record.category == "conectividad"

    def test_assigns_correct_project(self) -> None:
        request = _make_request(
            "La conectividad digital es un desafío permanente "
            "para las comunidades del extremo austral."
        )
        record = analyze_mock(request)

        assert record.related_project == "Observatorio de Conectividad Austral"

    def test_high_relevance_with_territory_and_category(self) -> None:
        request = _make_request(
            "La conectividad en Punta Arenas mejora gracias "
            "a nueva infraestructura de fibra óptica."
        )
        record = analyze_mock(request)

        assert record.editorial_relevance == Level.HIGH
        assert record.confidence == Level.HIGH


# ---------------------------------------------------------------------------
# Contenido sin territorio reconocible
# ---------------------------------------------------------------------------


class TestNoTerritory:
    """Verifica comportamiento cuando no se detectan territorios ni categoría."""

    def test_no_territory_activates_human_review(self) -> None:
        request = _make_request(
            "Este es un texto genérico que no menciona ninguna localidad "
            "específica ni temática reconocible del extremo austral."
        )
        record = analyze_mock(request)

        assert record.territory == []
        assert record.requires_human_review is True
        assert record.review_reason != ""

    def test_no_territory_has_low_confidence(self) -> None:
        request = _make_request(
            "Un documento sin referencias geográficas claras "
            "ni categorías temáticas identificables por el sistema."
        )
        record = analyze_mock(request)

        assert record.confidence == Level.LOW
        assert record.editorial_relevance == Level.LOW

    def test_no_territory_uses_default_project(self) -> None:
        request = _make_request(
            "Contenido abstracto sin mencionar lugares "
            "ni temas reconocidos por las reglas del analizador."
        )
        record = analyze_mock(request)

        assert record.related_project == "Sin clasificar"
        assert record.category == "unknown"


# ---------------------------------------------------------------------------
# Conservación de URL
# ---------------------------------------------------------------------------


class TestUrlPreservation:
    """Verifica que la URL se conserva sin modificaciones."""

    def test_url_preserved_in_source(self) -> None:
        url = "https://example.org/nota-austral"
        request = _make_request(
            "Puerto Williams recibe nueva inversión en infraestructura portuaria.",
            url=url,
        )
        record = analyze_mock(request)

        assert record.source.type == SourceType.URL
        assert str(record.source.url) == url

    def test_no_url_marks_user_text(self) -> None:
        request = _make_request(
            "Puerto Williams recibe nueva inversión en infraestructura portuaria.",
        )
        record = analyze_mock(request)

        assert record.source.type == SourceType.USER_TEXT
        assert record.source.url is None


# ---------------------------------------------------------------------------
# Salida válida según AnalysisRecord
# ---------------------------------------------------------------------------


class TestValidOutput:
    """Verifica que la salida cumple el esquema de AnalysisRecord."""

    def test_output_is_analysis_record(self) -> None:
        request = _make_request(
            "Investigación científica en la Antártica confirma "
            "hallazgos relevantes para estudios climáticos."
        )
        record = analyze_mock(request)

        assert isinstance(record, AnalysisRecord)

    def test_output_serializes_to_json(self) -> None:
        request = _make_request(
            "Canal Beagle es una ruta marítima fundamental "
            "para la conectividad austral de Chile."
        )
        record = analyze_mock(request)

        payload = record.model_dump(mode="json")
        assert "id" in payload
        assert "created_at" in payload
        assert "title" in payload
        assert "summary" in payload
        assert "territory" in payload
        assert "source" in payload

    def test_id_and_timestamp_are_generated(self) -> None:
        request = _make_request(
            "El Estrecho de Magallanes conecta el Atlántico con el Pacífico."
        )
        record = analyze_mock(request)

        assert record.id is not None
        assert record.created_at is not None

    def test_different_calls_produce_different_ids(self) -> None:
        request = _make_request(
            "El Estrecho de Magallanes conecta el Atlántico con el Pacífico."
        )
        record_a = analyze_mock(request)
        record_b = analyze_mock(request)

        assert record_a.id != record_b.id


# ---------------------------------------------------------------------------
# Comportamiento determinista de campos editoriales
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Verifica que los campos editoriales son reproducibles."""

    def test_same_input_produces_same_editorial_fields(self) -> None:
        request = _make_request(
            "Cabo de Hornos es un hito geográfico para la ciencia polar "
            "y la navegación internacional."
        )
        record_a = analyze_mock(request)
        record_b = analyze_mock(request)

        assert record_a.title == record_b.title
        assert record_a.summary == record_b.summary
        assert record_a.territory == record_b.territory
        assert record_a.category == record_b.category
        assert record_a.entities == record_b.entities
        assert record_a.related_project == record_b.related_project
        assert record_a.editorial_relevance == record_b.editorial_relevance
        assert record_a.confidence == record_b.confidence
        assert record_a.requires_human_review == record_b.requires_human_review

    def test_different_input_produces_different_output(self) -> None:
        request_a = _make_request(
            "Puerto Williams recibe nueva inversión en infraestructura portuaria.")
        request_b = _make_request(
            "Un documento sin referencias geográficas claras "
            "ni categorías temáticas identificables por el sistema.")

        record_a = analyze_mock(request_a)
        record_b = analyze_mock(request_b)

        assert record_a.territory != record_b.territory
        assert record_a.confidence != record_b.confidence
