# VetCare 🐾

VetCare es una aplicación en Java diseñada para la gestión básica de una clínica veterinaria, estructurada con una **arquitectura en capas (Frontend / Controller / Service / Repository)** y **pruebas unitarias con JUnit 5**.

## Problema que resuelve

Permite a una veterinaria registrar y consultar de manera sencilla y centralizada los datos básicos de las mascotas que ingresan para su atención (**nombre**, **especie** y **edad**), asegurando que se cumplan las reglas de negocio antes de ser almacenadas en el sistema.

## Reglas de Validación de Negocio

Para que una mascota pueda registrarse en el sistema, deben cumplirse las siguientes reglas:
1. **Nombre**: No puede ser nulo ni estar vacío/en blanco.
2. **Especie**: No puede ser nula ni estar vacía/en blanco.
3. **Edad**: No puede ser negativa (`< 0`).
4. **Edad cero (`0`)**: Se considera un valor completamente válido (representa cachorros o recién nacidos).

Si alguno de los datos ingresados no cumple con estas reglas, el sistema rechaza el registro e informa el error de validación (`HTTP 400 Bad Request` / `IllegalArgumentException`).

## Arquitectura y Estructura del Proyecto

- `pom.xml`: Configuración de Maven (Java 17 y JUnit 5).
- `src/main/java/com/vetcare/`:
  - `Main.java`: Punto de entrada principal (inicia la interfaz gráfica por defecto o la consola interactiva con `--cli`).
  - `Mascota.java`: Entidad de dominio que representa a una mascota.
  - `Veterinaria.java`: Fachada compatible con la versión original.
  - `ui/VetCareGUI.java`: Interfaz gráfica de escritorio en **Java Swing** con formulario de alta, chips rápidos de especie, tabla en vivo y barra de estado HTTP.
  - `controller/MascotaController.java`: Controlador que recibe DTOs y devuelve respuestas estructuradas (`RespuestaBackend<T>`).
  - `service/MascotaService.java`: Capa de lógica de negocio y validaciones.
  - `repository/MascotaRepository.java` y `InMemoryMascotaRepository.java`: Capa de persistencia en memoria con ID autoincremental.
  - `dto/RegistrarMascotaDTO.java` y `RespuestaBackend.java`: Objetos de transferencia de datos.
- `src/test/java/com/vetcare/`: Suite de pruebas unitarias con **JUnit 5** (`MascotaServiceTest`, `MascotaControllerTest`, `VeterinariaTest`).

## Cómo ejecutar el proyecto

### 1. Ejecutar la Interfaz Gráfica (GUI)

Con Maven:
```bash
mvn clean compile exec:java -Dexec.mainClass="com.vetcare.Main"
```

O con `javac` / `java` directo:
```bash
javac -encoding UTF-8 -d target/classes src/main/java/com/vetcare/*.java src/main/java/com/vetcare/controller/*.java src/main/java/com/vetcare/dto/*.java src/main/java/com/vetcare/repository/*.java src/main/java/com/vetcare/service/*.java src/main/java/com/vetcare/ui/*.java
java -cp target/classes com.vetcare.Main
```
*(Para abrir en modo consola interactiva, agregar el argumento `--cli`)*

### 2. Ejecutar las Pruebas Unitarias (JUnit 5)

Con Maven:
```bash
mvn test
```

O con el runner standalone incluido en `lib/`:
```bash
java -jar lib/junit-platform-console-standalone-1.10.2.jar execute --class-path "target/classes;target/test-classes" --scan-class-path
```
