# Actividad – Diseñando el backend de mi aplicación

**Estudiante:** Araceli  
**Materia / Asignatura:** Programación / Desarrollo de Software  
**Proyecto:** VetCare  
**Fecha:** Octubre 2026  

---

## 1. Breve descripción de la aplicación

**VetCare** es una aplicación desarrollada en Java cuyo objetivo primordial es la gestión y registro inicial de pacientes (mascotas) que ingresan a una clínica veterinaria.

La aplicación permite a los recepcionistas o profesionales de la clínica dar de alta animales con sus atributos fundamentales (nombre, especie y edad) y consultar las mascotas registradas en el sistema. Su propósito en el contexto formativo es servir como base de estudio y refactorización, permitiendo a los estudiantes analizar cómo un código monolítico de consola puede evolucionar hacia una arquitectura robusta, modular y profesional mediante la separación entre **Frontend** y **Backend**.

---

## 2. Análisis del proyecto actual

A partir de la inspección exhaustiva de los archivos existentes en el proyecto (`Main.java`, `Mascota.java` y `Veterinaria.java`), se identificaron las siguientes características estructurales y operativas:

### 2.1. Funcionalidades actuales
1. **Registro de una nueva mascota:** Se solicitan los datos del animal mediante consola y se incorporan al sistema si superan los filtros de validación.
2. **Listado de mascotas:** Se recorre la colección de mascotas existentes y se imprime por consola un reporte ordenado con el número, nombre, especie y edad de cada una.
3. **Control de flujo por consola:** Un bucle interactivo con menú numérico (1. Registrar mascota, 2. Listar mascotas, 3. Salir) que gestiona la sesión del usuario.

### 2.2. Entidades y datos manejados
- **Entidad `Mascota`:** Representa al sujeto de atención veterinaria. Maneja los atributos:
  - `nombre` (`String`): Identificador nominal del animal.
  - `especie` (`String`): Clasificación biológica o tipo de animal (por ejemplo: Perro, Gato, Ave).
  - `edad` (`int`): Cantidad de años cumplidos del animal.
- **Clase gestora `Veterinaria`:** Actúa como contenedor de la clínica, agrupando las mascotas en memoria y ofreciendo los métodos de interacción.

### 2.3. Relaciones entre entidades
Existe una relación de agregación/composición de **1 a N** entre `Veterinaria` y `Mascota`. Una veterinaria alberga una colección (`List<Mascota>`) de cero a múltiples mascotas.

### 2.4. Reglas de negocio identificadas
1. **Obligatoriedad del Nombre:** El nombre de la mascota no puede ser `null` ni estar vacío o contener únicamente espacios en blanco.
2. **Obligatoriedad de la Especie:** La especie no puede ser `null` ni estar en blanco.
3. **No negatividad de la Edad:** La edad no puede ser un número menor a cero (`edad >= 0`).
4. **Validez de edad cero (`0`):** La edad 0 es estrictamente válida, representando cachorros, crías o neonatos.
5. **Manejo de transgresiones:** Ante cualquier dato inválido, el sistema interrumpe el registro lanzando una excepción `IllegalArgumentException`, impidiendo que datos corruptos ingresen al sistema.

### 2.5. Almacenamiento y persistencia actual
- **Estado actual:** El almacenamiento se realiza en memoria volátil mediante una colección `ArrayList<Mascota>` dentro de la clase `Veterinaria`.
- **Diagnóstico:** Si la aplicación se cierra o se reinicia, todos los datos registrados se pierden inmediatamente.
- **Necesidad de persistencia:** Para un entorno productivo, se requiere un mecanismo de persistencia duradera (como un motor de base de datos relacional o archivos estructurados) que preserve el historial clínico y los registros de las mascotas.

### 2.6. Diagnóstico de responsabilidades (Lógica de aplicación vs. Backend)
En el diseño inicial, la clase `Veterinaria` sufría de una excesiva concentración de responsabilidades (violando el principio de Responsabilidad Única - SRP):
1. **Validaba** los datos de entrada (regla de negocio).
2. **Instanciaba** el modelo `Mascota` (construcción de dominio).
3. **Almacenaba** el objeto en una lista (persistencia).

Por su parte, la clase `Main` mezclaba la interacción con el usuario (`Scanner`, `System.out`) con la invocación directa a la lógica de negocio. Esta falta de capas desacopladas es el punto de partida ideal para diseñar la separación Frontend / Backend.

---

## 3. Entidades y funcionalidades identificadas

| Entidad / Clase | Rol en el Sistema | Atributos / Responsabilidades Principales |
|---|---|---|
| **`Mascota`** | Entidad de Dominio | - `id` (Identificador único asignado por el sistema)<br>- `nombre` (Nombre de la mascota)<br>- `especie` (Especie del animal)<br>- `edad` (Edad en años) |
| **`Veterinaria`** | Fachada de la Clínica (Compatibilidad) | - Punto de entrada tradicional de la clínica.<br>- Delega la gestión al servicio desacoplado preservando compatibilidad. |
| **`RegistrarMascotaDTO`** *(Propuesta Backend)* | Objeto de Transferencia de Datos | - Transporta de forma segura los datos enviados desde el frontend (`nombre`, `especie`, `edad`) sin exponer directamente las entidades internas. |
| **`RespuestaBackend<T>`** *(Propuesta Backend)* | Envoltorio de Respuesta HTTP | - Estandariza la respuesta del servidor incluyendo código de estado HTTP (`200`, `201`, `400`, `500`), mensaje informativo y carga útil (`datos`). |

---

## 4. Responsabilidades del frontend y backend

Para transformar este prototipo en un sistema moderno y escalable, se delimitan rigurosamente las responsabilidades entre el cliente (Frontend) y el servidor (Backend):

### 4.1. Responsabilidades del Frontend
- **Interfaz y Presentación:** Mostrar menús, formularios interactivos, tablas y diálogos visuales.
- **Captura y Experiencia de Usuario (UX):** Recibir las entradas del usuario (teclado, clics), realizar validaciones superficiales de formato (por ejemplo, verificar que el campo de edad contenga dígitos numéricos antes del envío).
- **Manejo del Estado Visual:** Indicar estados de carga (*loading*), éxito de la operación o alertas de error en pantalla.
- **Consumo de Servicios:** Construir las peticiones (HTTP Requests / DTOs) dirigidas al Backend e interpretar sus respuestas (HTTP Status Codes y JSON).

### 4.2. Responsabilidades del Backend
- **Guardián de las Reglas de Negocio:** Asegurar que ninguna mascota sea registrada sin nombre, sin especie o con edades negativas, sin importar de qué cliente provenga la solicitud.
- **Capa de Entrada y Ruteo (Controllers):** Recibir solicitudes, mapear parámetros, coordinar la ejecución y devolver códigos de estado universales (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`).
- **Lógica de Servicio (Services):** Procesar las operaciones, orquestar flujos de trabajo y aplicar políticas del dominio.
- **Persistencia y Acceso a Datos (Repositories):** Interactuar con el almacén de datos (memoria, base de datos) para guardar, actualizar, consultar y eliminar registros de forma confiable e independiente de la tecnología subyacente.

---

## 5. Endpoints propuestos

Se diseñó una API RESTful intuitiva y estándar para la gestión completa de las mascotas en la clínica:

| Método | Endpoint | Función | Datos Recibidos (Body / Params) | Respuesta (Status y Payload) |
|---|---|---|---|---|
| **POST** | `/api/mascotas` | Registra una nueva mascota en el sistema | JSON: `{"nombre": "Milo", "especie": "Perro", "edad": 3}` | **201 Created**<br>`{"estadoHttp": 201, "mensaje": "Mascota registrada exitosamente.", "datos": {"id": 1, "nombre": "Milo", ...}}` |
| **GET** | `/api/mascotas` | Consulta y lista todas las mascotas registradas | Ninguno | **200 OK**<br>`{"estadoHttp": 200, "mensaje": "...", "datos": [ { ... }, { ... } ]}` |
| **GET** | `/api/mascotas/{id}` | Obtiene los detalles de una mascota específica | Parámetro de ruta: `id` (entero) | **200 OK** si existe<br>**404 Not Found** si el ID no fue encontrado |
| **PUT** | `/api/mascotas/{id}` | Actualiza los datos de una mascota existente | Parámetro `id` y JSON con datos actualizados | **200 OK** con datos actualizados<br>**400 Bad Request** si datos son inválidos<br>**404 Not Found** si no existe |
| **DELETE** | `/api/mascotas/{id}` | Da de baja o elimina una mascota del sistema | Parámetro de ruta: `id` (entero) | **204 No Content** al eliminar con éxito<br>**404 Not Found** si no existe |

### Validaciones requeridas por los endpoints:
- **`POST` y `PUT`:** El cuerpo de la solicitud no puede ser nulo; `nombre` y `especie` no pueden contener cadenas vacías o solo espacios en blanco; `edad` debe ser un entero mayor o igual a 0. En caso de error, el endpoint devuelve **400 Bad Request** con el mensaje explicativo exacto.
- **`GET /{id}`, `PUT /{id}`, `DELETE /{id}`:** El identificador `id` debe ser un entero positivo.

---

## 6. Arquitectura elegida

Para organizar el backend se adoptó la **Arquitectura en Tres Capas (Three-Tier Architecture)**:

```
[ Cliente / Frontend ]
          │
          ▼  (Petición HTTP / DTO)
┌──────────────────────────────────────────────┐
│                  CONTROLLER                  │  MascotaController
│  (Recibe peticiones, valida DTO, responde)   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼  (Llamada de negocio)
┌──────────────────────────────────────────────┐
│                   SERVICE                    │  MascotaService
│    (Reglas de negocio, validaciones núcleo)  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼  (Operaciones CRUD)
┌──────────────────────────────────────────────┐
│                  REPOSITORY                  │  MascotaRepository
│  (Interfaz y acceso a la persistencia)       │  InMemoryMascotaRepository
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│           ALMACÉN / PERSISTENCIA             │  List<Mascota> (En memoria)
│           (Base de Datos futura)             │  o Base de Datos SQL / NoSQL
└──────────────────────────────────────────────┘
```

### Responsabilidad de cada capa:
1. **Controller (`MascotaController`):** Es la puerta de entrada al backend. Su responsabilidad es recibir la solicitud, coordinar con el servicio y empaquetar el resultado en una respuesta HTTP comprensible (`RespuestaBackend`), aislando el núcleo de la aplicación de los detalles del protocolo de comunicación.
2. **Service (`MascotaService`):** Es el corazón del backend. Contiene la lógica del negocio: aplica las reglas de validación obligatorias (nombre, especie, edad) y transforma las intenciones del usuario en entidades consistentes de dominio.
3. **Repository (`MascotaRepository` / `InMemoryMascotaRepository`):** Encapsula el acceso y manipulación de los datos. Desacopla la lógica del negocio del mecanismo de almacenamiento. Si en el futuro se reemplaza la memoria RAM por una base de datos MySQL o PostgreSQL, la capa de servicio no sufre ningún cambio.

### Justificación de la estructura:
Se eligió este patrón porque proporciona **Alta Cohesión** y **Bajo Acoplamiento**, respeta los principios SOLID y es el estándar de la industria. Permite que cada componente pueda ser testeado de forma aislada mediante pruebas unitarias.

---

## 7. Decisión de la IA que cuestioné

> **Reflexión personal del estudiante:**
>
> Al comenzar el diseño del backend con la asistencia de la Inteligencia Artificial, la primera propuesta técnica que me ofreció fue realizar una migración completa del proyecto a **Spring Boot**, incorporando **Spring Web**, **Spring Data JPA**, anotaciones automáticas (`@RestController`, `@Service`, `@Repository`, `@Entity`, `@Autowired`), y la configuración de una base de datos H2 o PostgreSQL mediante contenedores Docker.
>
> ### ¿Por qué inicialmente parecía conveniente?
> A simple vista, la propuesta de la IA parecía sumamente tentadora y moderna. Spring Boot es el framework dominante en el mercado profesional para Java, automatiza la creación de servidores web embebidos, serializa objetos a JSON de forma transparente y reduce líneas de código repetitivo gracias a las anotaciones.
>
> ### ¿Por qué cuestioné esa decisión?
> Al analizar críticamente la propuesta desde la realidad de nuestro proyecto escolar, encontré serias objeciones:
> 1. **Sobreingeniería desmedida:** VetCare es una aplicación educativa con una única entidad (`Mascota`). Agregar un ecosistema de más de 50 megabytes de dependencias para registrar tres campos es una complejidad injustificada.
> 2. **Pérdida de visibilidad pedagógica:** La "magia" de los frameworks oculta cómo fluyen realmente los datos. En un examen oral, si todo lo resuelven anotaciones de Spring, es muy difícil demostrar y defender que uno comprende de verdad cómo un Controller llama a un Service y cómo este utiliza un Repository.
> 3. **Riesgo de errores de configuración ajenos a la consigna:** Configurar servidores de aplicaciones, puertos y conexiones de bases de datos externas desvía el foco del objetivo principal de la actividad: **aprender a diseñar la separación de capas y validar reglas de negocio con pruebas unitarias**.
>
> ### Decisión final adoptada
> Decidí rechazar la adopción prematura de Spring Boot y elegí implementar la arquitectura **Controller → Service → Repository utilizando Java puro (POJOs e interfaces estándar)**, acompañados de un repositorio en memoria (`InMemoryMascotaRepository`) y objetos de transferencia explícitos (`RegistrarMascotaDTO`, `RespuestaBackend`).
>
> Esta alternativa me otorga un control absoluto del código, me permite defender cada clase con total soltura en la presentación oral y demuestra fielmente los principios de la arquitectura en capas sin esconderse detrás de librerías complejas.

---

## 8. Funcionalidad backend implementada

Se implementó de forma completa y funcional la operación de **Registro de Mascota** bajo la arquitectura de tres capas.

### 8.1. Archivos y clases intervinientes
1. **`com.vetcare.dto.RegistrarMascotaDTO`**: Estructura de datos que recibe la petición con `nombre`, `especie` y `edad`.
2. **`com.vetcare.dto.RespuestaBackend<T>`**: Objeto envoltorio de respuesta HTTP que transporta el código de estado (`201` o `400`), mensaje y entidad creada.
3. **`com.vetcare.repository.MascotaRepository`**: Interfaz con las operaciones `guardar(mascota)`, `obtenerTodas()` y `buscarPorId(id)`.
4. **`com.vetcare.repository.InMemoryMascotaRepository`**: Implementación en memoria que gestiona la lista interna y genera identificadores únicos autoincrementales (`AtomicInteger`).
5. **`com.vetcare.service.MascotaService`**: Clase de servicio que aplica exhaustivamente las reglas de negocio y delega el almacenamiento.
6. **`com.vetcare.controller.MascotaController`**: Controlador que recibe el DTO, coordina con el servicio y retorna el estado HTTP correspondiente.
7. **`com.vetcare.Veterinaria`**: Refactorizada para delegar internamente en `MascotaService`, preservando la compatibilidad retroactiva.
8. **`com.vetcare.Main`**: Adaptado para simular al cliente interactivo (Frontend) comunicándose con el `MascotaController` del Backend.

### 8.2. Flujo de funcionamiento
1. El usuario ingresa los datos de la mascota en el Frontend (`Main`).
2. El Frontend empaqueta los datos en un `RegistrarMascotaDTO` y llama al método `registrarMascota(dto)` del `MascotaController`.
3. El `MascotaController` invoca al `MascotaService`.
4. El `MascotaService` verifica estrictamente que:
   - El DTO no sea nulo.
   - El nombre no esté vacío ni en blanco.
   - La especie no esté vacía ni en blanco.
   - La edad no sea menor a 0 (edad 0 es aceptada).
5. Si los datos son válidos, el servicio instancia un objeto `Mascota` limpio y llama a `MascotaRepository.guardar(nuevaMascota)`.
6. El repositorio asigna un nuevo `id` incremental (por ejemplo `#1`) y almacena el registro.
7. El controlador captura la mascota creada y retorna un `RespuestaBackend` con código **HTTP 201 Created**.
8. Si ocurre algún error de validación, el controlador captura la excepción y retorna un **HTTP 400 Bad Request** con el motivo del rechazo.

---

## 9. Evidencia de funcionamiento

Se realizaron pruebas reales y automatizadas que certifican el correcto funcionamiento de la arquitectura implementada.

### Evidencia 1: Ejecución de la suite completa de pruebas unitarias con JUnit 5
Se desarrollaron **11 pruebas unitarias** divididas en tres clases de test:
- `MascotaServiceTest` (6 pruebas de reglas de negocio y casos borde).
- `MascotaControllerTest` (3 pruebas de respuestas y códigos HTTP).
- `VeterinariaTest` (2 pruebas de compatibilidad).

**Resultado real obtenido en consola:**
```text
JUnit Jupiter
├── Pruebas Unitarias de compatibilidad: Veterinaria
│   ├── Debe registrar mascota y devolverla en la lista [PASÓ]
│   └── Debe lanzar excepción al ingresar datos inválidos a través de Veterinaria [PASÓ]
├── Pruebas Unitarias del Controlador de Backend: MascotaController
│   ├── Debe responder con HTTP 201 Created al registrar exitosamente una mascota [PASÓ]
│   ├── Debe responder con HTTP 400 Bad Request cuando los datos no cumplen las validaciones [PASÓ]
│   └── Debe responder con HTTP 200 OK al solicitar el listado de mascotas [PASÓ]
└── Pruebas Unitarias del Servicio de Backend: MascotaService
    ├── Debe registrar exitosamente una mascota con datos válidos [PASÓ]
    ├── Debe registrar válidamente una mascota con edad 0 (cachorro o recién nacido) [PASÓ]
    ├── Debe lanzar excepción cuando el nombre es nulo o está en blanco [PASÓ]
    ├── Debe lanzar excepción cuando la especie es nula o está en blanco [PASÓ]
    ├── Debe lanzar excepción cuando la edad es un número negativo [PASÓ]
    └── Debe lanzar excepción cuando el DTO de datos es nulo [PASÓ]

[ 11 tests found      ]
[ 11 tests started    ]
[ 11 tests successful ]
[  0 tests failed     ]
Test run finished after 119 ms
```
*Explicación:* Esta prueba demuestra que el 100% de los casos de prueba se ejecutaron exitosamente, comprobando tanto los caminos felices como los casos límite y de error (nombres vacíos, edad negativa, edad cero).

---

### Evidencia 2: Interacción en tiempo de ejecución (Frontend CLI ↔ Backend Controller)
Se ejecutó la aplicación `Main.java` enviando interacciones sucesivas para poner a prueba el registro exitoso, el rechazo de datos inválidos y la consulta posterior.

**Salida real obtenida por consola:**
```text
==========================================
   VetCare - Arquitectura Frontend/Backend
==========================================

Seleccione una opción:
1. Registrar mascota (POST /api/mascotas)
2. Listar mascotas   (GET  /api/mascotas)
3. Salir
Opción: 1

--- [Frontend] Formulario de Registro de Mascota ---
Ingrese el nombre de la mascota: Milo
Ingrese la especie: Perro
Ingrese la edad: 3
[Backend HTTP 201 CREATED] Mascota registrada exitosamente.
   -> ID: #1 | Nombre: Milo | Especie: Perro | Edad: 3 años

Seleccione una opción:
1. Registrar mascota (POST /api/mascotas)
2. Listar mascotas   (GET  /api/mascotas)
3. Salir
Opción: 1

--- [Frontend] Formulario de Registro de Mascota ---
Ingrese el nombre de la mascota: 
Ingrese la especie: Gato
Ingrese la edad: 2
[Backend HTTP 400 BAD REQUEST] Error de validación: El nombre no puede estar vacío.

Seleccione una opción:
1. Registrar mascota (POST /api/mascotas)
2. Listar mascotas   (GET  /api/mascotas)
3. Salir
Opción: 2

--- [Frontend] Consulta de Mascotas Registradas ---
[Backend HTTP 200 OK] Lista de mascotas obtenida exitosamente.
   #1 - Nombre: Milo       | Especie: Perro      | Edad: 3 años

Seleccione una opción:
1. Registrar mascota (POST /api/mascotas)
2. Listar mascotas   (GET  /api/mascotas)
3. Salir
Opción: 3
¡Gracias por utilizar VetCare!
```
*Explicación:* La captura demuestra cómo el Frontend interactúa con el Backend:
1. La mascota *Milo* recibe el código **HTTP 201 CREATED** y se le asigna el ID único `#1`.
2. Al intentar registrar una mascota con nombre en blanco, el Backend responde con **HTTP 400 BAD REQUEST** y rechaza la operación sin persistir datos corruptos.
3. Al consultar con la opción 2, el Backend responde **HTTP 200 OK** listando únicamente las mascotas válidamente creadas.

---

## 10. Conclusión

A lo largo de este proyecto, aprendí que la separación entre **Frontend** y **Backend** no se trata únicamente de dividir tecnologías de interfaz y de servidor, sino de establecer una clara **delimitación de responsabilidades arquitectónicas**.

Al desacoplar el monolito original en un patrón **Controller → Service → Repository**, logramos:
1. **Independencia del dominio:** Las reglas de negocio (validación de nombres, especies y edades) ahora residen exclusivamente en el servicio, inmunes a los cambios en la interfaz gráfica o de consola.
2. **Facilidad de testeo:** Cada componente pudo ser verificado de forma exhaustiva mediante pruebas unitarias con JUnit 5 sin necesidad de simular entradas de usuario por consola.
3. **Preparación para el futuro:** Gracias a la abstracción de la interfaz `MascotaRepository`, en una etapa posterior se podrá reemplazar el almacenamiento en memoria por una base de datos relacional (como MySQL o SQLite) o conectar un frontend web moderno (React, Angular o Vue) sin modificar una sola línea de la lógica de negocio.

La experiencia de cuestionar las recomendaciones de la Inteligencia Artificial fue fundamental para comprender que una buena solución de ingeniería no es la que utiliza el framework más complejo, sino la que mejor se adapta a los requerimientos, restricciones y objetivos pedagógicos del proyecto.
