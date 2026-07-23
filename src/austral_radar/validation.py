"""Módulo de validación de entrada reutilizable.

Provee una función principal `validate_input` que verifica las restricciones
de texto y URL antes de construir un `AnalysisRequest`. Los mensajes de error
se entregan en español.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import HttpUrl, ValidationError

from austral_radar.models import AnalysisRequest

# Constantes de validación (coherentes con AnalysisRequest)
MIN_TEXT_LENGTH = 20
MAX_TEXT_LENGTH = 20_000


@dataclass
class ValidationResult:
    """Resultado de la validación de entrada."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    request: AnalysisRequest | None = None


def _check_whitespace_issues(text: str) -> list[str]:
    """Detecta espacios innecesarios y devuelve advertencias."""
    warnings: list[str] = []
    if text != text.strip():
        warnings.append("El texto contiene espacios en blanco innecesarios al inicio o al final.")
    if "  " in text:
        warnings.append("El texto contiene espacios dobles consecutivos.")
    return warnings


def _validate_url(url: str) -> list[str]:
    """Valida formato de URL usando el tipo HttpUrl de Pydantic."""
    errors: list[str] = []
    try:
        HttpUrl(url)
    except (ValidationError, ValueError):
        errors.append(f"La URL proporcionada no es válida: '{url}'.")
    return errors


def validate_input(
    source_text: str | None,
    source_url: str | None = None,
) -> ValidationResult:
    """Valida la entrada del usuario y retorna un resultado estructurado.

    Verifica:
    - Texto vacío o solo espacios.
    - Texto demasiado corto (< 20 caracteres útiles).
    - Texto demasiado largo (> 20 000 caracteres).
    - URL con formato inválido (si se proporciona).
    - Espacios innecesarios (advertencias incluidas en errores).

    Parámetros
    ----------
    source_text : str | None
        Texto de la fuente a analizar.
    source_url : str | None
        URL opcional de la fuente original.

    Retorna
    -------
    ValidationResult
        Contiene `is_valid`, lista de `errors` y, si es válido, el `request` construido.
    """
    errors: list[str] = []

    # --- Validar texto ---
    if source_text is None or source_text.strip() == "":
        errors.append("El texto de la fuente no puede estar vacío.")
        return ValidationResult(is_valid=False, errors=errors)

    # Detectar espacios innecesarios
    whitespace_issues = _check_whitespace_issues(source_text)
    errors.extend(whitespace_issues)

    # Normalizar para verificar longitud útil
    normalized = source_text.strip()

    if len(normalized) < MIN_TEXT_LENGTH:
        errors.append(
            f"El texto es demasiado corto. Se requieren al menos {MIN_TEXT_LENGTH} caracteres "
            f"(se recibieron {len(normalized)})."
        )

    if len(normalized) > MAX_TEXT_LENGTH:
        errors.append(
            f"El texto excede el límite máximo de {MAX_TEXT_LENGTH:,} caracteres "
            f"(se recibieron {len(normalized):,})."
        )

    # --- Validar URL ---
    if source_url is not None and source_url.strip() != "":
        url_errors = _validate_url(source_url.strip())
        errors.extend(url_errors)

    # --- Si hay errores de longitud o URL, la entrada es inválida ---
    if errors:
        return ValidationResult(is_valid=False, errors=errors)

    # --- Construir el request validado ---
    try:
        request = AnalysisRequest(
            source_text=normalized,
            source_url=source_url.strip() if source_url else None,
        )
    except ValidationError as exc:
        for error in exc.errors():
            msg = error.get("msg", "Error de validación desconocido.")
            errors.append(msg)
        return ValidationResult(is_valid=False, errors=errors)

    return ValidationResult(is_valid=True, request=request)
