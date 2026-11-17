# Mini actividad — Medí tu revisor

**Módulo 3 · Trabajo individual · 30 minutos**  
**Estudiante:** Araceli  
**Proyecto:** VetCare  
**Fecha:** Octubre 2026  

---

## Introducción

En esta actividad se evalúa de forma objetiva y cuantificable la eficacia del subagente revisor (`revisor`), midiendo su capacidad tanto para detectar problemas reales como para **saber callarse** ante archivos sanos y no generar falsos positivos.

---

## Paso 1 — Elección de los 5 archivos del proyecto

Se seleccionaron 5 archivos reales del proyecto **VetCare** combinando archivos con problemas conocidos y archivos sanos:

* **Archivos sanos (2):**
  1. `src/main/java/com/vetcare/Mascota.java`: Entidad de dominio POJO básica. Solo contiene atributos privados, constructores, getters y setters. Está sana y no debería disparar alertas.
  2. `src/main/java/com/vetcare/dto/RegistrarMascotaDTO.java`: Objeto de transferencia de datos (DTO). Es una clase pasiva sin lógica de negocio, utilizada únicamente para transportar información entre capas. Está sana.
* **Archivos con problemas conocidos (3):**
  3. `src/main/java/com/vetcare/repository/InMemoryMascotaRepository.java`: Almacenamiento en memoria mediante un `ArrayList` no sincronizado. Presenta problemas de concurrencia en entornos multi-hilo y riesgo de `OutOfMemoryError` por acumulación ilimitada de elementos sin paginación.
  4. `src/main/java/com/vetcare/service/MascotaService.java`: Capa de negocio que valida campos no vacíos y edad no negativa, pero **carece de límites superiores** (no restringe la longitud máxima de cadenas de texto ni establece un tope de edad razonable).
  5. `src/main/java/com/vetcare/Main.java`: Frontend de consola que utiliza `Scanner(System.in)` sin sanitización de caracteres ni control de tamaño en las entradas por teclado.

---

## Paso 2 y 3 — Tabla comparativa: Corrida 1 (Punto de partida)

Antes de ejecutar las pruebas, se definieron los hallazgos esperados (columnas 1 y 2). Luego se ejecutó el revisor de manera aislada sobre cada archivo para verificar sus respuestas.

| Archivo | Tipo de Archivo | Qué espero que encuentre | ¿Lo encontró en Corrida 1? |
|---|---|---|---|
| `Mascota.java` | Sano | Nada. Debe callarse o indicar 0 hallazgos porque es un POJO de dominio limpio. | **SÍ (Acertó)**<br>Indicó que no detectó problemas de seguridad ni robustez. |
| `RegistrarMascotaDTO.java` | Sano | Nada. Debe callarse porque es un DTO pasivo de transporte sin lógica. | **NO (Falló)**<br>Disparó un falso positivo alertando que los setters no validan datos externos. |
| `InMemoryMascotaRepository.java` | Con problema | Falta de sincronización concurrente en el `ArrayList` y acumulación ilimitada de memoria. | **SÍ (Acertó)**<br>Identificó concurrencia (líneas 10-22) y riesgo de `OutOfMemoryError`. |
| `MascotaService.java` | Con problema | Ausencia de límites superiores (sin tope de longitud en strings ni edad máxima). | **SÍ (Acertó)**<br>Detectó falta de límite en strings y edad (líneas 27-35). |
| `Main.java` | Con problema | Entradas de consola con `Scanner` sin límite de tamaño ni sanitización de caracteres. | **SÍ (Acertó)**<br>Señaló lecturas de consola sin control de longitud (líneas 58-66). |

### Resultado de la Corrida 1:
> **Mi revisor acertó 4 de 5.**  
*(El fallo se produjo en `RegistrarMascotaDTO.java` al disparar un falso positivo en una clase sana).*

---

## Paso 4 — Modificación de UNA sola línea en el revisor

### El problema identificado
En la Corrida 1, el revisor exigió validaciones de negocio en los setters de un **DTO**, sin comprender que en una arquitectura en capas los DTOs son contenedores agnósticos y que la validación es responsabilidad exclusiva del `Service`.

### Cambio de una sola línea en `revisor.md`
Se modificó exactamente la **línea 22** del archivo `revisor.md`:

```diff
- No reescribas el código ni apliques cambios. No propongas refactors generales. No comentes nombres de variables, formato ni estilo, salvo que afecten directamente la seguridad o el funcionamiento.
+ No reescribas código ni refactors generales. No opines de estilo ni exijas lógica de validación dentro de clases puramente pasivas (DTOs o entidades POJO).
```

---

## Corrida 2 — Medición tras el cambio

Se ejecutaron nuevamente los mismos 5 archivos con el revisor actualizado:

| Archivo | Tipo de Archivo | Qué espero que encuentre | ¿Lo encontró en Corrida 2? |
|---|---|---|---|
| `Mascota.java` | Sano | Nada (POJO limpio). | **SÍ (Acertó)** — Se mantuvo en silencio sin reportar fallos. |
| `RegistrarMascotaDTO.java` | Sano | Nada (DTO pasivo). | **SÍ (Acertó)** — Reconoció que es un DTO pasivo y no emitió falsos positivos. |
| `InMemoryMascotaRepository.java` | Con problema | Concurrencia y límite de memoria. | **SÍ (Acertó)** — Señaló con precisión el `ArrayList` y la memoria. |
| `MascotaService.java` | Con problema | Falta de límites máximos de entrada. | **SÍ (Acertó)** — Reportó la falta de longitud máxima en strings. |
| `Main.java` | Con problema | Entradas de consola sin sanitizar. | **SÍ (Acertó)** — Reportó el uso no acotado de `Scanner`. |

### Resultado de la Corrida 2:
> **Después del cambio acertó 5 de 5.**

---

## Qué entregás (Respuestas puntuales de la consigna)

### 1. La tabla completa, con las dos corridas:

| Archivo | Estado del archivo | Qué esperaba encontrar | Corrida 1 (Inicial) | Corrida 2 (Tras el cambio) |
|---|---|---|---|---|
| `Mascota.java` | Sano | Silencio / 0 hallazgos (POJO). | **Acertó** (0 hallazgos) | **Acertó** (0 hallazgos) |
| `RegistrarMascotaDTO.java` | Sano | Silencio / 0 hallazgos (DTO). | **Falló** (falso positivo en setters) | **Acertó** (se calló correctamente) |
| `InMemoryMascotaRepository.java` | Con problema | Concurrencia y memoria heap. | **Acertó** (hallazgo reportado) | **Acertó** (hallazgo reportado) |
| `MascotaService.java` | Con problema | Entradas sin límite superior. | **Acertó** (hallazgo reportado) | **Acertó** (hallazgo reportado) |
| `Main.java` | Con problema | Entradas de consola sin acotar. | **Acertó** (hallazgo reportado) | **Acertó** (hallazgo reportado) |

### 2. Qué cambiaste y por qué, en dos líneas:
> *Modifiqué la línea de restricciones del revisor para prohibirle exigir validaciones dentro de clases puramente pasivas (DTOs o POJOs).*  
> *Esto evita que el agente confunda objetos de transporte de datos con componentes de lógica activa, eliminando falsos positivos molestos.*

### 3. Qué pasó con el número y qué caso concreto cambió:
* **Evolución del número:** Subió de **4 de 5** a **5 de 5**.
* **Caso concreto que cambió:** `RegistrarMascotaDTO.java`. En la primera corrida, el agente reclamaba que los setters permitían recibir valores nulos o vacíos; tras el cambio de una sola línea, el revisor comprendió que por ser un DTO pasivo no debe contener lógica de negocio y supo callarse.

---

## Conclusión

Esta actividad demostró que **un buen revisor no es el que más habla, sino el que sabe discriminar con exactitud**. Incluir archivos sanos fue la clave del ejercicio: sin ellos, un revisor hiperactivo que inventa advertencias en cualquier clase parecería infalible. Ajustar una sola línea en las instrucciones permitió calibrar el criterio del agente, elevando su precisión de 4 a 5 aciertos sin perder capacidad para señalar riesgos reales.
