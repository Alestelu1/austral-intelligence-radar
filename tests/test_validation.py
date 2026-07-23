"""Pruebas unitarias del módulo de validación de entrada."""


from austral_radar.validation import (
    MAX_TEXT_LENGTH,
    MIN_TEXT_LENGTH,
    ValidationResult,
    validate_input,
)


# --- Texto vacío ---


class TestEmptyText:
    """Casos donde el texto está ausente o vacío."""

    def test_none_text_is_rejected(self) -> None:
        result = validate_input(source_text=None)
        assert not result.is_valid
        assert any("vacío" in e for e in result.errors)

    def test_empty_string_is_rejected(self) -> None:
        result = validate_input(source_text="")
        assert not result.is_valid
        assert any("vacío" in e for e in result.errors)

    def test_whitespace_only_is_rejected(self) -> None:
        result = validate_input(source_text="     ")
        assert not result.is_valid
        assert any("vacío" in e for e in result.errors)

    def test_tabs_and_newlines_only_is_rejected(self) -> None:
        result = validate_input(source_text="\t\n\r  \n")
        assert not result.is_valid
        assert any("vacío" in e for e in result.errors)


# --- Texto demasiado corto ---


class TestShortText:
    """Casos donde el texto es más corto que el mínimo requerido."""

    def test_text_below_minimum_is_rejected(self) -> None:
        short_text = "a" * (MIN_TEXT_LENGTH - 1)
        result = validate_input(source_text=short_text)
        assert not result.is_valid
        assert any("corto" in e for e in result.errors)

    def test_error_includes_character_count(self) -> None:
        short_text = "hola mundo"
        result = validate_input(source_text=short_text)
        assert not result.is_valid
        assert any(str(len(short_text)) in e for e in result.errors)

    def test_text_at_exact_minimum_is_accepted(self) -> None:
        exact_min = "a" * MIN_TEXT_LENGTH
        result = validate_input(source_text=exact_min)
        assert result.is_valid
        assert result.request is not None


# --- Texto demasiado largo ---


class TestLongText:
    """Casos donde el texto excede el máximo permitido."""

    def test_text_above_maximum_is_rejected(self) -> None:
        long_text = "a" * (MAX_TEXT_LENGTH + 1)
        result = validate_input(source_text=long_text)
        assert not result.is_valid
        assert any("excede" in e or "máximo" in e for e in result.errors)

    def test_text_at_exact_maximum_is_accepted(self) -> None:
        exact_max = "a" * MAX_TEXT_LENGTH
        result = validate_input(source_text=exact_max)
        assert result.is_valid
        assert result.request is not None


# --- URL inválida ---


class TestInvalidUrl:
    """Casos donde la URL proporcionada tiene formato incorrecto."""

    def test_malformed_url_is_rejected(self) -> None:
        result = validate_input(
            source_text="Texto suficientemente largo para superar el mínimo de caracteres requerido.",
            source_url="not-a-url",
        )
        assert not result.is_valid
        assert any("URL" in e for e in result.errors)

    def test_url_without_scheme_is_rejected(self) -> None:
        result = validate_input(
            source_text="Texto suficientemente largo para superar el mínimo de caracteres requerido.",
            source_url="www.example.com/path",
        )
        assert not result.is_valid
        assert any("URL" in e for e in result.errors)

    def test_valid_url_is_accepted(self) -> None:
        result = validate_input(
            source_text="Texto suficientemente largo para superar el mínimo de caracteres requerido.",
            source_url="https://example.org/document",
        )
        assert result.is_valid

    def test_empty_url_is_treated_as_absent(self) -> None:
        result = validate_input(
            source_text="Texto suficientemente largo para superar el mínimo de caracteres requerido.",
            source_url="",
        )
        assert result.is_valid

    def test_none_url_is_accepted(self) -> None:
        result = validate_input(
            source_text="Texto suficientemente largo para superar el mínimo de caracteres requerido.",
            source_url=None,
        )
        assert result.is_valid


# --- Espacios innecesarios ---


class TestWhitespace:
    """Casos de espacios al inicio, final o dobles dentro del texto."""

    def test_leading_spaces_produce_warning(self) -> None:
        text = "   Texto con suficiente longitud para pasar la validación mínima requerida."
        result = validate_input(source_text=text)
        # Se reporta el problema de espacios, pero si el texto normalizado es válido,
        # el resultado contiene el error/advertencia
        assert any("inicio o al final" in e for e in result.errors)

    def test_trailing_spaces_produce_warning(self) -> None:
        text = "Texto con suficiente longitud para pasar la validación mínima requerida.   "
        result = validate_input(source_text=text)
        assert any("inicio o al final" in e for e in result.errors)

    def test_double_spaces_produce_warning(self) -> None:
        text = "Texto con  espacios dobles y suficiente longitud para pasar la validación mínima."
        result = validate_input(source_text=text)
        assert any("dobles" in e for e in result.errors)

    def test_clean_text_has_no_whitespace_warnings(self) -> None:
        text = "Texto limpio con suficiente longitud para superar la validación mínima requerida."
        result = validate_input(source_text=text)
        assert result.is_valid
        assert len(result.errors) == 0


# --- Caso exitoso completo ---


class TestValidInput:
    """Verifica que una entrada correcta genere un AnalysisRequest válido."""

    def test_valid_text_and_url_produce_request(self) -> None:
        result = validate_input(
            source_text="Fuente documental suficiente para ejecutar el análisis especializado.",
            source_url="https://example.org/source",
        )
        assert result.is_valid
        assert result.request is not None
        assert result.request.source_text.startswith("Fuente documental")
        assert str(result.request.source_url) == "https://example.org/source"

    def test_valid_text_without_url_produces_request(self) -> None:
        result = validate_input(
            source_text="Fuente documental suficiente para ejecutar el análisis especializado.",
        )
        assert result.is_valid
        assert result.request is not None
        assert result.request.source_url is None

    def test_result_type_is_validation_result(self) -> None:
        result = validate_input(
            source_text="Fuente documental suficiente para ejecutar el análisis especializado.",
        )
        assert isinstance(result, ValidationResult)
