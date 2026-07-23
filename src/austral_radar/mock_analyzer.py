"""Analizador simulado y determinista para desarrollo de la interfaz.

Produce un AnalysisRecord válido a partir de un AnalysisRequest sin depender
de modelos de IA, red ni servicios externos.  El resultado es determinista
para los campos editoriales (excepto `id` y `created_at`).
"""

from __future__ import annotations

from austral_radar.models import (
    AnalysisRecord,
    AnalysisRequest,
    Entity,
    EntityType,
    Level,
    SourceProvenance,
    SourceType,
)

# ---------------------------------------------------------------------------
# Tablas de palabras clave
# ---------------------------------------------------------------------------

# Territorios: clave de búsqueda (minúsculas) → nombre canónico
_TERRITORY_KEYWORDS: dict[str, str] = {
    "puerto williams": "Puerto Williams",
    "puerto toro": "Puerto Toro",
    "punta arenas": "Punta Arenas",
    "cabo de hornos": "Cabo de Hornos",
    "canal beagle": "Canal Beagle",
    "estrecho de magallanes": "Estrecho de Magallanes",
    "antártica": "Antártica",
    "antartica": "Antártica",
}

# Entidades: clave de búsqueda (minúsculas) → (nombre, tipo)
_ENTITY_KEYWORDS: dict[str, tuple[str, EntityType]] = {
    "puerto williams": ("Puerto Williams", EntityType.PLACE),
    "puerto toro": ("Puerto Toro", EntityType.PLACE),
    "punta arenas": ("Punta Arenas", EntityType.PLACE),
    "cabo de hornos": ("Cabo de Hornos", EntityType.PLACE),
    "canal beagle": ("Canal Beagle", EntityType.ROUTE),
    "estrecho de magallanes": ("Estrecho de Magallanes", EntityType.ROUTE),
}

# Categorías temáticas: clave de búsqueda (minúsculas) → categoría
_CATEGORY_KEYWORDS: dict[str, str] = {
    "conectividad": "conectividad",
    "ciencia": "ciencia",
    "turismo": "turismo",
    "infraestructura": "infraestructura",
}

# Mapeo categoría → proyecto relacionado
_CATEGORY_PROJECT_MAP: dict[str, str] = {
    "conectividad": "Observatorio de Conectividad Austral",
    "ciencia": "Antarctic Pulse",
    "turismo": "End of the World Travel",
    "infraestructura": "Austral Dispatch",
}


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------


def _detect_territories(text_lower: str) -> list[str]:
    """Detecta territorios mencionados en el texto."""
    found: list[str] = []
    for keyword, name in _TERRITORY_KEYWORDS.items():
        if keyword in text_lower and name not in found:
            found.append(name)
    return found


def _detect_entities(text_lower: str) -> list[Entity]:
    """Detecta entidades mencionadas en el texto."""
    found: list[Entity] = []
    seen_names: set[str] = set()
    for keyword, (name, entity_type) in _ENTITY_KEYWORDS.items():
        if keyword in text_lower and name not in seen_names:
            found.append(Entity(name=name, type=entity_type))
            seen_names.add(name)
    return found


def _detect_category(text_lower: str) -> str:
    """Detecta la categoría temática principal."""
    for keyword, category in _CATEGORY_KEYWORDS.items():
        if keyword in text_lower:
            return category
    return "unknown"


def _build_title(text: str, category: str) -> str:
    """Genera un título determinista basado en las primeras palabras y la categoría."""
    words = text.split()
    prefix = " ".join(words[:5]) if len(words) >= 5 else " ".join(words)
    # Limitar longitud y agregar categoría si se conoce
    if category != "unknown":
        title = f"Análisis ({category}): {prefix}"
    else:
        title = f"Análisis: {prefix}"
    # Truncar a 240 caracteres respetando el modelo
    return title[:240]


def _build_summary(text: str, territories: list[str], category: str) -> str:
    """Genera un resumen determinista basado en la fuente."""
    parts: list[str] = []
    parts.append("Fuente analizada de forma simulada.")

    if territories:
        parts.append(f"Territorios detectados: {', '.join(territories)}.")
    else:
        parts.append("No se detectaron territorios específicos.")

    if category != "unknown":
        parts.append(f"Categoría identificada: {category}.")
    else:
        parts.append("No se identificó una categoría temática.")

    # Incluir extracto del texto original (primeros 120 caracteres)
    excerpt = text[:120].strip()
    parts.append(f'Extracto: "{excerpt}..."')

    summary = " ".join(parts)
    return summary[:2000]


# ---------------------------------------------------------------------------
# Función pública
# ---------------------------------------------------------------------------


def analyze_mock(request: AnalysisRequest) -> AnalysisRecord:
    """Analiza una solicitud de forma determinista y devuelve un AnalysisRecord válido.

    No utiliza modelos de IA, red ni servicios externos.  El resultado es
    reproducible para los campos editoriales dada la misma entrada (excepto
    `id` y `created_at` que se generan automáticamente).

    Parámetros
    ----------
    request : AnalysisRequest
        Solicitud previamente validada.

    Retorna
    -------
    AnalysisRecord
        Ficha de inteligencia editorial completa y válida.
    """
    text = request.source_text
    text_lower = text.lower()

    # Detección basada en reglas
    territories = _detect_territories(text_lower)
    entities = _detect_entities(text_lower)
    category = _detect_category(text_lower)
    related_project = _CATEGORY_PROJECT_MAP.get(category, "Sin clasificar")

    # Título y resumen deterministas
    title = _build_title(text, category)
    summary = _build_summary(text, territories, category)

    # Determinar relevancia y confianza
    has_territory = len(territories) > 0
    has_category = category != "unknown"

    if has_territory and has_category:
        editorial_relevance = Level.HIGH
        confidence = Level.HIGH
    elif has_territory or has_category:
        editorial_relevance = Level.MEDIUM
        confidence = Level.MEDIUM
    else:
        editorial_relevance = Level.LOW
        confidence = Level.LOW

    # Revisión humana cuando la información es insuficiente
    requires_human_review = not has_territory and not has_category
    review_reason = (
        "No se detectaron territorios ni categoría temática en la fuente."
        if requires_human_review
        else ""
    )

    # Procedencia conservada sin modificaciones
    if request.source_url is not None:
        source = SourceProvenance(type=SourceType.URL, url=request.source_url)
    else:
        source = SourceProvenance(type=SourceType.USER_TEXT)

    return AnalysisRecord(
        title=title,
        summary=summary,
        territory=territories,
        category=category,
        entities=entities,
        related_project=related_project,
        editorial_relevance=editorial_relevance,
        confidence=confidence,
        requires_human_review=requires_human_review,
        review_reason=review_reason,
        source=source,
    )
