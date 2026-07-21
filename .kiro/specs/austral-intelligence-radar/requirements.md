# Requisitos

## 1. Propósito

Construir un agente de IA especializado que convierta el texto de una fuente en una ficha de inteligencia estructurada y trazable para Austral Beacon Media.

## 2. Requisitos funcionales

### RF-1 — Enviar contenido de una fuente

La persona usuaria debe poder enviar texto y, de manera opcional, una URL de origen.

**Criterios de aceptación**

- CUANDO la persona envíe texto no vacío, EL SISTEMA DEBERÁ aceptarlo para su análisis.
- CUANDO el texto esté vacío, EL SISTEMA DEBERÁ devolver un error de validación claro.

### RF-2 — Generar análisis estructurado

El sistema debe devolver:

- título;
- resumen conciso;
- territorio;
- categoría;
- entidades detectadas;
- proyecto relacionado de Austral Beacon;
- relevancia editorial;
- nivel de confianza;
- indicador de revisión humana;
- procedencia de la fuente.

**Criterios de aceptación**

- CUANDO el análisis finalice correctamente, EL SISTEMA DEBERÁ devolver JSON válido conforme al esquema definido.
- SI un campo no puede determinarse, EL SISTEMA DEBERÁ usar `unknown` o una colección vacía en lugar de inventar datos.

### RF-3 — Conservar la procedencia

El sistema debe conservar la URL o el identificador de origen proporcionado.

**Criterios de aceptación**

- CUANDO se proporcione una URL, EL SISTEMA DEBERÁ incluirla sin modificaciones en el resultado.
- CUANDO no se proporcione una URL, EL SISTEMA DEBERÁ indicar explícitamente que la fuente corresponde a texto proporcionado por la persona usuaria.

### RF-4 — Requerir revisión humana cuando corresponda

El agente debe detectar incertidumbre o afirmaciones sin respaldo suficiente.

**Criterios de aceptación**

- SI la confianza es baja o existen afirmaciones contradictorias, EL SISTEMA DEBERÁ establecer `requires_human_review` en `true`.
- EL SISTEMA DEBERÁ entregar una razón breve para activar la revisión.

### RF-5 — Persistir el análisis en AWS

El sistema debe guardar los análisis correctos en un servicio de datos de AWS.

**Criterios de aceptación**

- CUANDO un análisis finalice correctamente, EL SISTEMA DEBERÁ guardar un registro con identificador único y marca temporal.
- SI la persistencia falla, EL SISTEMA DEBERÁ informar el error sin exponer secretos.

### RF-6 — Proporcionar una demostración utilizable

El proyecto debe ofrecer una interfaz pública o una experiencia ejecutable.

**Criterios de aceptación**

- Una persona evaluadora DEBERÁ poder enviar una fuente e inspeccionar el resultado.
- La interfaz DEBERÁ mostrar claramente los estados de carga y los errores.

## 3. Requisitos no funcionales

- Las respuestas deben completarse dentro de un tiempo razonable para una demostración.
- Los secretos deben almacenarse en variables de entorno o en la configuración de AWS y nunca incluirse en commits.
- La implementación debe incluir registros básicos y manejo de errores.
- El código debe mantenerse lo bastante pequeño como para completarse y probarse durante el hackathon.
- El README debe documentar el uso de Kiro y AWS.

## 4. Fuera del alcance

- Ingesta de PDF
- RAG completo
- Knowledge Graph
- Múltiples agentes autónomos
- Autenticación
- Soporte multi-tenant
