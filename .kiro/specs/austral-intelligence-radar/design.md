# Diseño

## 1. Arquitectura

```text
Interfaz web
   ↓ HTTPS
Amazon API Gateway
   ↓
AWS Lambda
   ├── validar solicitud
   ├── invocar modelo de IA
   ├── validar salida estructurada
   └── persistir resultado
        ↓
Amazon DynamoDB
```

El servicio de modelos debe estar disponible mediante AWS. Se prefiere Amazon Bedrock cuando el acceso de la cuenta y la disponibilidad del modelo lo permitan.

## 2. Modelo de solicitud

```json
{
  "source_text": "string",
  "source_url": "string | null"
}
```

## 3. Registro de análisis

```json
{
  "id": "uuid",
  "created_at": "ISO-8601 timestamp",
  "title": "string",
  "summary": "string",
  "territory": ["string"],
  "category": "string",
  "entities": [
    {
      "name": "string",
      "type": "place | institution | route | infrastructure | person | other"
    }
  ],
  "related_project": "string",
  "editorial_relevance": "low | medium | high",
  "confidence": "low | medium | high",
  "requires_human_review": true,
  "review_reason": "string",
  "source": {
    "type": "url | user_text",
    "url": "string | null"
  }
}
```

Las claves JSON y sus valores enumerados permanecen en inglés para mantener consistencia técnica en el código y las integraciones.

## 4. Responsabilidades del backend

- Rechazar entradas vacías o demasiado extensas.
- Construir un prompt de análisis restringido a partir de las reglas de Steering.
- Solicitar al modelo una respuesta JSON estructurada.
- Validar campos obligatorios y valores enumerados.
- Aplicar valores seguros cuando el modelo omita campos.
- Añadir en el servidor el identificador y la marca temporal.
- Guardar el registro validado en DynamoDB.
- Devolver a la interfaz una respuesta sanitizada.

## 5. Responsabilidades del frontend

- Proporcionar campos para texto y URL opcional.
- Mostrar estados de carga, éxito y error.
- Presentar el resultado estructurado en secciones legibles.
- Destacar visualmente la confianza y el estado de revisión humana.
- Evitar exponer credenciales de AWS o prompts internos del modelo.

## 6. Recursos de AWS

Recursos mínimos:

- endpoint de API Gateway;
- función Lambda de análisis;
- tabla DynamoDB;
- registros de CloudWatch;
- rol IAM con principio de mínimo privilegio.

## 7. Manejo de errores

- `400`: solicitud no válida.
- `422`: la salida del modelo no puede validarse.
- `500`: fallo inesperado de procesamiento o persistencia.
- Los registros no deben contener secretos ni documentos fuente sensibles completos.

## 8. Seguridad

- No incluir credenciales en Git.
- Usar variables de entorno y roles IAM.
- Restringir CORS al frontend desplegado cuando sea viable.
- Definir límites de longitud para la entrada.
- Escapar en el navegador el contenido generado por el modelo.
