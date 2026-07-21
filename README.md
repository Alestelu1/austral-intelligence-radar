# Austral Intelligence Radar

Agente de IA especializado para analizar, clasificar y preservar la procedencia de fuentes sobre el extremo austral de Chile y la Antártica.

## Hackathon

- Evento: Hackathon Kiro de Código Facilito y AWS
- Reto: Reto 3 — Agentes especializados
- Periodo de desarrollo: 20–27 de julio de 2026
- Participante: Alexis Stelu
- Estado: MVP en desarrollo

## Problema

Investigadores, editores y desarrolladores que trabajan con información territorial y antártica deben revisar manualmente fuentes dispersas, identificar su alcance geográfico, extraer entidades relevantes, evaluar su valor editorial y conservar su procedencia. Este proceso es repetitivo, lento y propenso a perder trazabilidad.

## Solución propuesta

Austral Intelligence Radar recibe contenido de una fuente y produce un análisis estructurado con:

- título;
- resumen;
- territorio;
- categoría;
- entidades detectadas;
- fuente original;
- proyecto relacionado de Austral Beacon;
- relevancia editorial;
- nivel de confianza;
- necesidad de revisión humana.

## Flujo del MVP

```text
Texto de una fuente
    ↓
Análisis especializado con IA
    ↓
Resultado JSON estructurado
    ↓
Persistencia en AWS
    ↓
Resultado legible para una persona
```

## Stack previsto

- Kiro IDE y Spec-Driven Development
- Python
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon Bedrock u otro servicio de modelos compatible con AWS
- Interfaz web mínima

## Fuera del alcance del hackathon

- Plataforma RAG completa
- Knowledge Graph
- Múltiples agentes autónomos
- Ingesta masiva de PDF
- Panel editorial completo de Austral Beacon
- Autenticación y gestión multiusuario

## Estructura del repositorio

```text
.kiro/
├── steering/
└── specs/
    └── austral-intelligence-radar/
        ├── requirements.md
        ├── design.md
        └── tasks.md

docs/
src/
tests/
```

## Criterios de éxito

- Una persona puede enviar el texto de una fuente.
- El agente devuelve un análisis estructurado válido.
- El resultado conserva la procedencia de la fuente.
- Las afirmaciones inciertas quedan marcadas para revisión humana.
- La aplicación puede demostrarse públicamente.
- El uso de AWS y Kiro queda documentado.

## Licencia

MIT
