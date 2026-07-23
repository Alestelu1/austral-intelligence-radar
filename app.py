"""Interfaz web mínima de Austral Intelligence Radar.

Formulario local con Streamlit para enviar texto fuente, validar la entrada
y mostrar el resultado del análisis simulado (mock_analyzer).

Ejecutar con:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from austral_radar.mock_analyzer import analyze_mock
from austral_radar.models import AnalysisRecord, Level
from austral_radar.validation import validate_input

# ---------------------------------------------------------------------------
# Configuración de página
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Austral Intelligence Radar",
    page_icon="🧭",
    layout="centered",
)


# ---------------------------------------------------------------------------
# Funciones auxiliares de presentación
# ---------------------------------------------------------------------------


def _level_label(level: Level) -> str:
    """Convierte un Level a etiqueta legible en español."""
    labels = {
        Level.LOW: "Baja",
        Level.MEDIUM: "Media",
        Level.HIGH: "Alta",
    }
    return labels.get(level, str(level))


def _display_record(record: AnalysisRecord) -> None:
    """Muestra el AnalysisRecord de forma estructurada."""
    st.markdown("---")
    st.subheader("📋 Resultado del análisis")

    # --- Métricas destacadas ---
    col1, col2, col3 = st.columns(3)

    with col1:
        confidence_label = _level_label(record.confidence)
        st.metric(label="Confianza", value=confidence_label)

    with col2:
        relevance_label = _level_label(record.editorial_relevance)
        st.metric(label="Relevancia editorial", value=relevance_label)

    with col3:
        review_label = "Sí ⚠️" if record.requires_human_review else "No ✅"
        st.metric(label="Revisión humana", value=review_label)

    # --- Alerta de revisión humana ---
    if record.requires_human_review:
        st.warning(f"🔍 **Revisión requerida:** {record.review_reason}")

    # --- Título y resumen ---
    st.markdown(f"**Título:** {record.title}")
    st.markdown(f"**Resumen:** {record.summary}")

    # --- Territorio ---
    st.markdown("**Territorios detectados:**")
    if record.territory:
        for t in record.territory:
            st.markdown(f"- 📍 {t}")
    else:
        st.markdown("- _Ninguno detectado_")

    # --- Categoría y proyecto ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Categoría:** {record.category}")
    with col_b:
        st.markdown(f"**Proyecto relacionado:** {record.related_project}")

    # --- Entidades ---
    st.markdown("**Entidades detectadas:**")
    if record.entities:
        entity_data = [{"Nombre": e.name, "Tipo": e.type.value} for e in record.entities]
        st.table(entity_data)
    else:
        st.markdown("- _Ninguna detectada_")

    # --- Procedencia ---
    st.markdown("---")
    st.markdown("**📎 Procedencia de la fuente:**")
    if record.source.url:
        st.markdown("- Tipo: URL")
        st.markdown(f"- Enlace: {record.source.url}")
    else:
        st.markdown("- Tipo: Texto proporcionado por el usuario")

    # --- Datos técnicos colapsados ---
    with st.expander("🔧 Datos técnicos"):
        st.json(record.model_dump(mode="json"))


# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------

st.title("🧭 Austral Intelligence Radar")
st.markdown(
    "Agente de inteligencia editorial que transforma contenido no estructurado "
    "en fichas trazables para **Austral Beacon Media**."
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Formulario de entrada
# ---------------------------------------------------------------------------

st.subheader("Enviar fuente para análisis")

with st.form(key="analysis_form"):
    source_text = st.text_area(
        label="Texto de la fuente",
        height=200,
        placeholder="Pega aquí el contenido de la fuente a analizar (mínimo 20 caracteres)...",
        help="Texto completo o extracto relevante de la fuente.",
    )

    source_url = st.text_input(
        label="URL de la fuente (opcional)",
        placeholder="https://ejemplo.cl/articulo",
        help="Si la fuente tiene URL, inclúyela para conservar la procedencia.",
    )

    submitted = st.form_submit_button("🔍 Analizar fuente", use_container_width=True)

# ---------------------------------------------------------------------------
# Procesamiento
# ---------------------------------------------------------------------------

if submitted:
    # Validar entrada usando el módulo existente (sin duplicar reglas)
    url_value = source_url.strip() if source_url else None
    validation = validate_input(source_text=source_text, source_url=url_value)

    if not validation.is_valid:
        for error_msg in validation.errors:
            st.error(f"⚠️ {error_msg}")
    else:
        # Analizar con el mock determinista
        with st.spinner("Analizando fuente..."):
            assert validation.request is not None
            record = analyze_mock(validation.request)

        st.success("✅ Análisis completado")
        _display_record(record)
