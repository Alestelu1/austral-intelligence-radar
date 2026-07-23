# Tareas

## Fase 1 — Fundación

- [x] Inicializar el repositorio público.
- [x] Definir el problema y los límites del MVP.
- [x] Añadir el contexto de Steering y las reglas editoriales.
- [x] Definir los requisitos y el diseño inicial.
- [x] Añadir la estructura del proyecto Python y la gestión de dependencias.
- [x] Definir en código el esquema JSON del análisis.

## Fase 2 — Flujo vertical local

- [x] Implementar validación de entrada.
- [x] Implementar un analizador simulado y determinista para desarrollar la interfaz.
- [ ] Construir el formulario web mínimo y la vista de resultados.
- [ ] Añadir pruebas para entrada vacía y salida estructurada válida.
- [ ] Demostrar localmente el flujo completo sin persistencia en AWS.

## Fase 3 — Integración de IA

- [ ] Confirmar el servicio de modelos de AWS disponible en la cuenta.
- [ ] Implementar el adaptador del modelo.
- [ ] Crear un prompt de sistema restringido según las reglas de Steering.
- [ ] Interpretar y validar el JSON producido por el modelo.
- [ ] Añadir un comportamiento seguro ante respuestas incompletas.
- [ ] Probar con al menos cinco fuentes representativas.

## Fase 4 — Integración con AWS

- [ ] Crear el diseño de la tabla DynamoDB.
- [ ] Implementar la persistencia de registros.
- [ ] Empaquetar el backend para AWS Lambda.
- [ ] Configurar API Gateway.
- [ ] Configurar permisos IAM con mínimo privilegio.
- [ ] Confirmar registros en CloudWatch sin secretos.

## Fase 5 — Despliegue y validación

- [ ] Desplegar la demostración pública.
- [ ] Configurar el endpoint de la API y CORS en el frontend.
- [ ] Probar los flujos de éxito, validación y fallo de servicio.
- [ ] Verificar que cada resultado conserve la procedencia.
- [ ] Verificar que el contenido incierto active revisión humana.

## Fase 6 — Entregables

- [ ] Completar en el README las secciones de instalación y arquitectura.
- [ ] Añadir un diagrama de arquitectura.
- [ ] Documentar Specs, Steering y el flujo de desarrollo con Kiro.
- [ ] Documentar los servicios de AWS utilizados.
- [ ] Eliminar secretos e inspeccionar el historial de Git.
- [ ] Preparar un guion de video de menos de cinco minutos.
- [ ] Grabar la demostración funcional.
- [ ] Verificar los enlaces del repositorio, la demo y el video antes de entregar.

## Orden de implementación

Trabajar desde un flujo vertical mínimo y no comenzar funciones opcionales hasta que funcione este recorrido:

```text
enviar texto → recibir análisis válido → mostrar resultado → persistir en AWS
```
