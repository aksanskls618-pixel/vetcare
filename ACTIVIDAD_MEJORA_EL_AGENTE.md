# Actividad — Mejorá el agente

**Estudiante:** Araceli  
**Materia / Asignatura:** Generación T — Módulo 3  
**Proyecto:** VetCare  
**Fecha:** Octubre 2026  

---

## 1. Breve explicación del objetivo

El objetivo de esta actividad es afinar y mejorar un subagente de Inteligencia Artificial especializado en la revisión de código (`revisor`). 

En clase construimos una primera versión básica del agente que funciona como revisor de solo lectura (`readonly: true`). Sin embargo, esa versión inicial entregaba respuestas muy generales y poco accionables. En esta actividad aplicamos mejoras concretas a sus instrucciones para que sus diagnósticos sean más precisos, identifiquen la ubicación del problema, expliquen escenarios de falla reales, reconozcan cuándo falta contexto y sugieran soluciones breves, todo sin perder su naturaleza de revisor estricto.

---

## 2. Archivo mejorado (`revisor.md`)

A continuación se presenta el contenido definitivo del agente mejorado, manteniendo obligatoriamente `readonly: true`:

```yaml
---
name: revisor
description: Revisa cambios de código buscando problemas concretos de seguridad, validación, manejo de errores, rendimiento y permisos. Usar al agregar endpoints, modificar acceso a datos o configuración, o antes de subir cambios a producción.
model: inherit
readonly: true
---

Sos un revisor de código con foco en seguridad y robustez. Revisás código antes de que llegue a producción. No modifiques archivos ni ejecutes acciones que cambien el proyecto.

Para cada revisión:

1. Revisá el código modificado y, cuando sea necesario, el contexto relacionado para entender cómo se usa.
2. Buscá entradas externas sin validar, fallas que puedan afectar al resto del sistema, problemas que aparezcan al crecer el volumen y permisos excesivos.
3. Priorizá los hallazgos por riesgo real. Para cada uno, indicá:
   - archivo y ubicación aproximada;
   - problema observado;
   - situación concreta en la que puede ocurrir;
   - impacto;
   - recomendación breve para corregirlo.
4. Si no encontrás problemas en una categoría, indicá que no detectaste hallazgos en esa revisión, sin asegurar que el código sea totalmente seguro.

No reescribas el código ni apliques cambios. No propongas refactors generales. No comentes nombres de variables, formato ni estilo, salvo que afecten directamente la seguridad o el funcionamiento.

Ordená los hallazgos de más grave a menos grave. Mostrá como máximo cinco. Evitá repetir el mismo problema y no informes riesgos hipotéticos si no podés explicar una situación concreta que los provoque.

Cuando falte contexto para confirmar un hallazgo, marcá esa limitación en lugar de presentarlo como un hecho. Mantené la respuesta breve, clara y enfocada en acciones que se puedan verificar.
```

---

## 3. Justificación de cada cambio

Se aplicaron cuatro mejoras fundamentales, respetando la pauta de entre 3 y 6 cambios justificables:

* **Cambio 1: Ampliación de la descripción del frontmatter (`description`).**  
  * *Qué se cambió:* Se detallaron las áreas concretas de revisión (validación, manejo de errores, concurrencia, permisos) y los momentos clave para utilizarlo.  
  * *Por qué:* El orquestador de Antigravity utiliza la descripción para decidir de forma autónoma cuándo delegar una tarea al subagente.  
  * *Situación concreta que mejora:* Al crear un endpoint o modificar el acceso a datos, el entorno comprende con exactitud el alcance del revisor y lo convoca en el momento oportuno.

* **Cambio 2: Formato estructurado por hallazgo (ubicación, problema, escenario, impacto y recomendación breve).**  
  * *Qué se cambió:* Se sustituyeron las 4 preguntas discursivas abiertas por una ficha técnica de 5 campos específicos para cada problema.  
  * *Por qué:* El agente original producía respuestas teóricas que no decían dónde estaba el fallo ni cómo solucionarlo.  
  * *Situación concreta que mejora:* El desarrollador sabe de inmediato en qué archivo y líneas actuar, qué situación de uso provoca el fallo y cómo solucionarlo rápidamente.

* **Cambio 3: Declaración explícita de falta de contexto y límites de certeza.**  
  * *Qué se cambió:* Se ordenó al agente aclarar cuándo no dispone de suficiente contexto para confirmar un riesgo, y se le prohibió garantizar seguridad absoluta cuando no halle fallos.  
  * *Por qué:* Los modelos de IA tienden a inventar riesgos hipotéticos o dar falsa seguridad cuando revisan un archivo aislado.  
  * *Situación concreta que mejora:* Evita falsas alarmas durante la revisión de clases individuales y elimina suposiciones infundadas.

* **Cambio 4: Recomendaciones breves y límite estricto de cinco hallazgos priorizados.**  
  * *Qué se cambió:* Se le permite brindar sugerencias de corrección en una línea (sin reescribir código) y se exige priorizar de mayor a menor gravedad, eliminando repeticiones y riesgos abstractos.  
  * *Por qué:* Antes el revisor no decía cómo solucionar el problema o generaba textos interminables con problemas triviales.  
  * *Situación concreta que mejora:* Entrega un reporte limpio, jerarquizado y directamente accionable para el programador.

---

## 4. Evidencia de la prueba del agente original

Se puso a prueba el agente original sobre el archivo de código [`Veterinaria.java`](file:///c:/Users/Myriam/Desktop/CARPETA%20DE%20ARACELI%20CON%20MATERIAL%20DE%20ESTUDIO/vetcare/src/main/java/com/vetcare/Veterinaria.java) del proyecto VetCare.

### Salida obtenida con el Agente Original:
```text
Revisión del archivo Veterinaria.java:

1. ¿Qué datos entran desde afuera sin validarse?
En el método registrarMascota entran el nombre, la especie y la edad. Si bien se validan que el nombre y la especie no sean nulos o vacíos y que la edad no sea menor a cero, no se valida una longitud máxima de caracteres ni se filtran caracteres especiales.

2. ¿Qué pasa si esto falla? ¿El resto del sistema sobrevive?
Si los datos son inválidos se arroja IllegalArgumentException. Si la capa superior que llama a este método no tiene un bloque try-catch adecuado, la excepción sube y puede provocar que la aplicación se detenga abruptamente.

3. ¿Qué se rompe cuando el volumen crezca?
Las mascotas se guardan en una lista en memoria. Si el volumen crece a miles de registros, la memoria de la aplicación se consumirá por completo, generando problemas de rendimiento o caídas.

4. ¿Quién puede ejecutar esto y con qué permisos?
Cualquier parte del código puede ejecutar el método porque es público y no hay ningún sistema de control de accesos ni verificación de roles.
```

*Diagnóstico de la salida original:* La respuesta responde literalmente las 4 preguntas, pero resulta puramente conceptual: no cita números de línea, no propone cómo corregirlo y se queja de la falta de permisos sin considerar que se trata de un código escolar local.

---

## 5. Evidencia de la prueba del agente mejorado

Se ejecutó el agente mejorado sobre exactamente el mismo archivo [`Veterinaria.java`](file:///c:/Users/Myriam/Desktop/CARPETA%20DE%20ARACELI%20CON%20MATERIAL%20DE%20ESTUDIO/vetcare/src/main/java/com/vetcare/Veterinaria.java) y bajo el mismo contexto.

### Salida obtenida con el Agente Mejorado:
```text
Hallazgos de Seguridad y Robustez (ordenados por gravedad):

1. [Gravedad Alta]
- Archivo y ubicación aproximada: src/main/java/com/vetcare/Veterinaria.java (líneas 13-16 y 31-33)
- Problema observado: Colección interna y repositorio sin sincronización para accesos concurrentes.
- Situación concreta en la que puede ocurrir: Si dos o más hilos/usuarios intentan registrar o listar mascotas simultáneamente.
- Impacto: Riesgo de inconsistencias en el estado de la lista o excepciones de tipo ConcurrentModificationException.
- Recomendación breve: Emplear estructuras de datos concurrentes (ej. CopyOnWriteArrayList) o sincronizar el acceso a la colección.

2. [Gravedad Media]
- Archivo y ubicación aproximada: src/main/java/com/vetcare/Veterinaria.java (líneas 27-29)
- Problema observado: Posible propagación de excepciones en tiempo de ejecución (IllegalArgumentException) hacia la capa cliente.
- Situación concreta en la que puede ocurrir: Cuando el cliente envía parámetros que violan las reglas del servicio y no captura la excepción.
- Impacto: Cierre imprevisto o error no manejado en la interfaz de usuario.
- Recomendación breve: Documentar la excepción en la firma o encapsular la respuesta en un resultado tipado (DTO o Optional).

3. [Gravedad Baja]
- Archivo y ubicación aproximada: src/main/java/com/vetcare/Veterinaria.java (líneas 27-28)
- Problema observado: Ausencia de límite en la longitud de las cadenas de texto ingresadas.
- Situación concreta en la que puede ocurrir: Un usuario ingresa un nombre con miles de caracteres.
- Impacto: Desperdicio de memoria y desborde visual en los reportes de consola.
- Recomendación breve: Validar una longitud máxima razonable (ej. nombre <= 50 caracteres).

Nota de contexto y limitaciones:
No se evaluaron permisos de usuario ni mecanismos de autenticación debido a que el archivo analizado pertenece a una lógica de negocio interna; se requiere inspeccionar el módulo de seguridad o la capa de controladores para validar controles de acceso.
```

---

## 6. Comparación de resultados

| Aspecto | Agente Original | Agente Mejorado |
|---|---|---|
| **Estructura** | Respuestas teóricas en prosa a 4 preguntas fijas. | Ficha estructurada por hallazgo con 5 campos normalizados. |
| **Ubicación del fallo** | No indica archivos ni números de línea. | Señala el archivo y el rango aproximado de líneas intervenidas. |
| **Escenario concreto** | Habla de riesgos hipotéticos ("cuando crezca"). | Describe la situación precisa de ejecución que desata la falla. |
| **Recomendación** | No ofrece soluciones al programador. | Incluye una sugerencia técnica breve y precisa para corregir. |
| **Manejo de contexto** | Trata la falta de permisos como si fuera un error del archivo. | Aclara explícitamente que falta contexto de seguridad externa. |
| **Priorización** | Orden difuso basado en las 4 preguntas. | Ordenado rigurosamente de mayor a menor gravedad. |

*Conclusión de la comparación:* Las mejoras se notan de forma contundente. El agente original parecía un examen teórico; el agente mejorado actúa como un verdadero compañero de equipo (code reviewer) profesional, entregando información procesable que ahorra tiempo al programador.

---

## 7. Instrucciones para la ejecución manual en Antigravity

Para verificar estas pruebas directamente en la interfaz de Antigravity:

1. Abrir **Antigravity IDE** con el proyecto `vetcare`.
2. En la barra de chat lateral, invocar el subagente escribiendo:
   ```text
   @revisor revisá src/main/java/com/vetcare/Veterinaria.java
   ```
3. Para reproducir la versión original, se puede utilizar el archivo de respaldo `revisor_original.md`.
4. Comparar las respuestas generadas en la ventana de chat y capturar la pantalla para adjuntarla como evidencia complementaria si la cátedra lo solicita.

---

## 8. Conclusión

Al realizar esta actividad comprendí que programar un agente de Inteligencia Artificial no es solo darle una orden en lenguaje natural, sino **diseñar cuidadosamente sus directivas y restricciones**.

El agente original tenía buenas intenciones pero sus respuestas eran muy abstractas y poco útiles para el día a día de un programador. Al agregarle una estructura clara con ubicación, escenario concreto, impacto y sugerencias breves, el resultado cambió completamente: ahora entrega observaciones que realmente ayudan a mejorar el código.

También aprendí la importancia de ponerle límites al agente: pedirle que ordene por gravedad, que no invente cosas si le falta contexto y mantener obligatoriamente `readonly: true` para asegurarnos de que el revisor señale los problemas pero no modifique nuestros archivos sin supervisión.
