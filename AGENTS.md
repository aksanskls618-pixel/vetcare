# Instrucciones para Agentes de IA (AGENTS.md)

Este documento define las directrices y restricciones obligatorias para cualquier modelo o agente de Inteligencia Artificial que colabore en este repositorio.

## 1. Naturaleza y Propósito del Proyecto
- **Propósito Educativo**: Este proyecto fue creado con fines didácticos para la enseñanza y práctica de **refactoring** y diseño de **pruebas unitarias con JUnit 5**.
- **Simplicidad ante todo**: El código debe mantenerse intencionalmente simple, legible y libre de sobreingeniería.

## 2. Restricciones Estrictas de Alcance (NO AGREGAR)
Queda expresamente prohibido agregar las siguientes funcionalidades o tecnologías a menos que el usuario lo solicite explícitamente por escrito:
- Sistemas de autenticación, login o roles de usuario.
- Gestión de usuarios o perfiles de clientes.
- Turnos, citas o calendarios.
- Bases de datos (relacionales o no relacionales) o frameworks ORM (como Hibernate o JPA).
- Historial médico o historias clínicas.
- Entidades de veterinarios o personal médico.
- APIs web (REST, GraphQL, Spring Boot, etc.).
- Librerías o integraciones con Inteligencia Artificial.
- Interfaces gráficas (GUI, frameworks web o frontend complejo).

## 3. Stack Tecnológico Aprobado
- **Lenguaje**: Java (Java SE estándar).
- **Gestor de dependencias / construcción**: Apache Maven (`pom.xml`).
- **Framework de pruebas**: JUnit 5 (JUnit Jupiter).
- **Interfaz**: Consola de terminal interactiva simple (`Scanner` / `System.out`).
- **Persistencia**: Estructuras en memoria (e.g. `List<Mascota>`).

## 4. Reglas de Validación de Negocio
Toda mascota registrada en el sistema debe cumplir estrictamente:
- **Nombre**: No puede ser nulo ni estar vacío/en blanco.
- **Especie**: No puede ser nula ni estar vacía/en blanco.
- **Edad**: No puede ser un número negativo (< 0).
- **Edad 0**: Es un valor completamente válido (representa cachorros o neonatos).
- Ante datos inválidos, el sistema debe rechazar el registro e informar el error de forma clara (por ejemplo, arrojando `IllegalArgumentException`).

## 5. Reglas para Refactoring y Pruebas Unitarias
- **Preservar comportamiento existente**: Cualquier refactoring posterior (por ejemplo, separar responsabilidades de validación, creación y persistencia) **no debe romper** el comportamiento externo esperado ni las validaciones existentes.
- **Pruebas unitarias**: Las pruebas deben desarrollarse utilizando exclusivamente **JUnit 5** bajo la carpeta `src/test/java/com/vetcare/`, cubriendo casos exitosos y casos límite/erróneos (nombres vacíos, edades negativas, edad 0, etc.).
- **Consultar antes de cambiar alcance**: Si surge la necesidad de modificar contratos públicos o agregar nuevas clases de utilidad, asegúrate de que mantenga la coherencia con el objetivo pedagógico.
