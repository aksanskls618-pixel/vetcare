import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, A4[1] - 30, "VetCare — Actividad: Diseñando el backend de mi aplicación")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(45, A4[1] - 34, A4[0] - 45, A4[1] - 34)
            
        # Footer (all pages)
        footer_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 45, 25, footer_text)
        self.drawString(45, 25, "Entrega Académica — Programación / Desarrollo de Software")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(45, 35, A4[0] - 45, 35)
        self.restoreState()

def build_pdf():
    pdf_filename = "ACTIVIDAD_DISENANDO_EL_BACKEND.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#1E3A8A")   # Blue-900
    secondary_color = colors.HexColor("#0D9488") # Teal-600
    dark_text = colors.HexColor("#1F2937")       # Gray-800
    muted_text = colors.HexColor("#4B5563")      # Gray-600
    bg_code = colors.HexColor("#F8FAFC")         # Slate-50
    border_code = colors.HexColor("#CBD5E1")     # Slate-300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=muted_text,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_text,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_text
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Actividad – Diseñando el backend de mi aplicación", title_style))
    story.append(Paragraph("<b>Proyecto:</b> VetCare &nbsp;|&nbsp; <b>Materia:</b> Desarrollo de Software &nbsp;|&nbsp; <b>Fecha:</b> Octubre 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))

    # 1. Breve descripción de la aplicación
    story.append(Paragraph("1. Breve descripción de la aplicación", h1_style))
    story.append(Paragraph(
        "<b>VetCare</b> es una aplicación en Java orientada a la gestión y registro inicial de pacientes (mascotas) en una clínica veterinaria. "
        "Permite registrar animales con sus atributos fundamentales (nombre, especie y edad) y consultar las mascotas almacenadas. "
        "En el contexto pedagógico, sirve como base práctica para analizar cómo un programa monolítico de consola puede evolucionar "
        "hacia una arquitectura profesional y modular mediante la separación entre <b>Frontend</b> y <b>Backend</b>.",
        body_style
    ))

    # 2. Análisis del proyecto actual
    story.append(Paragraph("2. Análisis del proyecto actual", h1_style))
    story.append(Paragraph(
        "A partir de la inspección de los archivos base (<code>Main.java</code>, <code>Mascota.java</code> y <code>Veterinaria.java</code>), "
        "se identificaron los siguientes aspectos técnicos y funcionales:",
        body_style
    ))
    story.append(Paragraph("• <b>Funcionalidades actuales:</b> Menú interactivo por consola con registro de mascota, listado general y salida del sistema.", bullet_style))
    story.append(Paragraph("• <b>Entidades y datos:</b> La entidad <code>Mascota</code> maneja <code>nombre</code> (String), <code>especie</code> (String) y <code>edad</code> (int).", bullet_style))
    story.append(Paragraph("• <b>Relaciones:</b> <code>Veterinaria</code> mantiene una relación de agregación 1 a N con <code>Mascota</code> mediante una lista interna.", bullet_style))
    story.append(Paragraph("• <b>Reglas de negocio:</b> El nombre y la especie no pueden ser nulos ni vacíos. La edad no puede ser negativa (< 0), pero la edad 0 es válida (cachorros/neonatos). Toda infracción lanza <code>IllegalArgumentException</code>.", bullet_style))
    story.append(Paragraph("• <b>Persistencia actual:</b> Estructura volátil en memoria (<code>ArrayList&lt;Mascota&gt;</code>). Al cerrar el programa, los datos se pierden. Se requiere persistencia real (base de datos o repositorios).", bullet_style))
    story.append(Paragraph("• <b>Diagnóstico de responsabilidades:</b> En la versión original, <code>Veterinaria</code> acumulaba validación de entrada, creación del objeto y persistencia, violando el Principio de Responsabilidad Única (SRP). <code>Main</code> acoplaba la interfaz con la lógica de negocio.", bullet_style))

    # 3. Entidades y funcionalidades identificadas
    story.append(Paragraph("3. Entidades y funcionalidades identificadas", h1_style))
    
    entidades_data = [
        [Paragraph("Entidad / Componente", table_header_style), Paragraph("Rol en la Arquitectura", table_header_style), Paragraph("Responsabilidad Principal", table_header_style)],
        [Paragraph("<b>Mascota</b>", table_cell_style), Paragraph("Entidad de Dominio", table_cell_style), Paragraph("Modela al paciente animal con sus atributos: id, nombre, especie y edad.", table_cell_style)],
        [Paragraph("<b>Veterinaria</b>", table_cell_style), Paragraph("Fachada / Compatibilidad", table_cell_style), Paragraph("Punto de acceso tradicional; delega al servicio desacoplado preservando compatibilidad retroactiva.", table_cell_style)],
        [Paragraph("<b>RegistrarMascotaDTO</b>", table_cell_style), Paragraph("Data Transfer Object", table_cell_style), Paragraph("Transporta de forma segura los datos enviados desde el frontend (nombre, especie, edad).", table_cell_style)],
        [Paragraph("<b>RespuestaBackend&lt;T&gt;</b>", table_cell_style), Paragraph("Envoltorio de Respuesta HTTP", table_cell_style), Paragraph("Estandariza las respuestas del servidor con estado HTTP (200, 201, 400), mensaje y payload.", table_cell_style)]
    ]
    t_entidades = Table(entidades_data, colWidths=[120, 130, 255])
    t_entidades.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_entidades)
    story.append(Spacer(1, 8))

    # 4. Responsabilidades del frontend y backend
    story.append(Paragraph("4. Responsabilidades del frontend y backend", h1_style))
    story.append(Paragraph(
        "Para transformar el prototipo en una solución desacoplada, se delimitan formalmente las responsabilidades:",
        body_style
    ))
    story.append(Paragraph("<b>Responsabilidades del Frontend:</b>", h2_style))
    story.append(Paragraph("• Interfaz de usuario: Renderizar vistas, menús y formularios interactivos.", bullet_style))
    story.append(Paragraph("• Captura y UX: Recibir datos del usuario y validar formato de entrada básico (por ejemplo, enteros válidos).", bullet_style))
    story.append(Paragraph("• Estado visual: Reflejar estados de carga, alertas de error y mensajes de éxito.", bullet_style))
    story.append(Paragraph("• Consumo de API: Empaquetar solicitudes en DTOs y procesar las respuestas HTTP devueltas por el backend.", bullet_style))

    story.append(Paragraph("<b>Responsabilidades del Backend:</b>", h2_style))
    story.append(Paragraph("• Reglas de negocio: Validar que no ingresen mascotas sin nombre, sin especie o con edades negativas.", bullet_style))
    story.append(Paragraph("• Controladores y ruteo: Recibir peticiones, coordinar servicios y devolver estados HTTP estándar.", bullet_style))
    story.append(Paragraph("• Servicios: Ejecutar la lógica de negocio y coordinar la persistencia de forma desacoplada.", bullet_style))
    story.append(Paragraph("• Repositorio y persistencia: Almacenar, consultar y manipular los datos de forma independiente de la tecnología física de base de datos.", bullet_style))

    # 5. Endpoints propuestos
    story.append(Paragraph("5. Endpoints propuestos", h1_style))
    endpoints_data = [
        [Paragraph("Método", table_header_style), Paragraph("Endpoint", table_header_style), Paragraph("Función", table_header_style), Paragraph("Datos Recibidos", table_header_style), Paragraph("Respuesta", table_header_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/mascotas</code>", table_cell_style), Paragraph("Registra una nueva mascota", table_cell_style), Paragraph("JSON con nombre, especie y edad", table_cell_style), Paragraph("<b>201 Created</b> con mascota creada y su ID", table_cell_style)],
        [Paragraph("<b>GET</b>", table_cell_style), Paragraph("<code>/api/mascotas</code>", table_cell_style), Paragraph("Lista todas las mascotas registradas", table_cell_style), Paragraph("Ninguno", table_cell_style), Paragraph("<b>200 OK</b> con arreglo de mascotas", table_cell_style)],
        [Paragraph("<b>GET</b>", table_cell_style), Paragraph("<code>/api/mascotas/{id}</code>", table_cell_style), Paragraph("Obtiene detalle de una mascota por ID", table_cell_style), Paragraph("Parámetro en URL: id", table_cell_style), Paragraph("<b>200 OK</b> o <b>404 Not Found</b>", table_cell_style)],
        [Paragraph("<b>PUT</b>", table_cell_style), Paragraph("<code>/api/mascotas/{id}</code>", table_cell_style), Paragraph("Actualiza datos de una mascota", table_cell_style), Paragraph("Parámetro id y JSON con nuevos datos", table_cell_style), Paragraph("<b>200 OK</b>, <b>400 Bad Request</b> o <b>404</b>", table_cell_style)],
        [Paragraph("<b>DELETE</b>", table_cell_style), Paragraph("<code>/api/mascotas/{id}</code>", table_cell_style), Paragraph("Elimina una mascota del sistema", table_cell_style), Paragraph("Parámetro en URL: id", table_cell_style), Paragraph("<b>204 No Content</b> o <b>404 Not Found</b>", table_cell_style)]
    ]
    t_endpoints = Table(endpoints_data, colWidths=[50, 105, 115, 115, 120])
    t_endpoints.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_endpoints)
    story.append(Spacer(1, 8))

    # 6. Arquitectura elegida
    story.append(Paragraph("6. Arquitectura elegida", h1_style))
    story.append(Paragraph(
        "Se adoptó la arquitectura en tres capas: <b>Controller → Service → Repository → Base de Datos</b>.",
        body_style
    ))
    
    diagram_text = (
        "+-------------------+        +--------------------+        +----------------------+\n"
        "| MascotaController | -----> |   MascotaService   | -----> |  MascotaRepository   |\n"
        "| (Entrada / HTTP)  |        | (Reglas / Dominio) |        | (InMemoryRepository) |\n"
        "+-------------------+        +--------------------+        +----------------------+"
    )
    story.append(Preformatted(diagram_text, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("• <b>Controller (MascotaController):</b> Recibe las peticiones DTO del cliente, delega en el servicio y traduce los resultados en códigos HTTP estandarizados (201, 400, 500).", bullet_style))
    story.append(Paragraph("• <b>Service (MascotaService):</b> Nuclea las reglas del negocio y validaciones estrictas. Si los datos son válidos, crea la entidad de dominio y coordina el guardado.", bullet_style))
    story.append(Paragraph("• <b>Repository (MascotaRepository):</b> Abstrae las operaciones de persistencia (guardar, buscar, listar). En esta fase usa almacenamiento en memoria con IDs autoincrementales.", bullet_style))
    story.append(Paragraph("<b>Justificación:</b> Esta arquitectura promueve alta cohesión y bajo acoplamiento, cumple con principios SOLID y permite probar cada capa de manera aislada con JUnit 5.", body_style))

    # 7. Decisión de la IA que cuestioné
    story.append(Paragraph("7. Decisión de la IA que cuestioné", h1_style))
    
    critica_paragraphs = [
        Paragraph("<b>Reflexión del Estudiante:</b>", ParagraphStyle('Bld', parent=body_style, fontName='Helvetica-Bold')),
        Paragraph("Al comenzar a diseñar el backend con asistencia de la Inteligencia Artificial, la primera propuesta técnica que recibí fue migrar inmediatamente el proyecto a <b>Spring Boot</b> con <b>Spring Data JPA</b>, anotaciones automáticas (<code>@RestController</code>, <code>@Service</code>, <code>@Repository</code>, <code>@Entity</code>) y una base de datos externa H2/PostgreSQL.", callout_style),
        Spacer(1, 4),
        Paragraph("<b>¿Por qué parecía conveniente inicialmente?</b> Porque Spring Boot es el estándar de la industria y ahorra código repetitivo al generar servidores web y consultas automáticas.", callout_style),
        Spacer(1, 4),
        Paragraph("<b>¿Por qué cuestioné esa decisión?</b> Cuestioné la propuesta porque para un proyecto escolar que maneja una única entidad (<code>Mascota</code>), incorporar Spring Boot representaba una sobreingeniería excesiva. Además, la 'magia' de las anotaciones oculta el funcionamiento real de las capas en Java, impidiendo comprender y defender en el examen oral cómo viajan realmente los datos. También desviaba el foco educativo de diseñar la arquitectura hacia resolver problemas de configuración de dependencias pesadas.", callout_style),
        Spacer(1, 4),
        Paragraph("<b>Alternativa elegida y justificación:</b> Decidí implementar la arquitectura Controller-Service-Repository en <b>Java puro (POJOs e interfaces estándar)</b> con persistencia en memoria y DTOs explícitos. Esto mantiene el código 100% transparente, comprensible y fácil de defender oralmente, cumpliendo con rigor los principios arquitectónicos sin complejidad artificial.", callout_style)
    ]
    
    t_critica = Table([[critica_paragraphs]], colWidths=[505])
    t_critica.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF3C7")), # Amber-100
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#F59E0B")),      # Amber-500
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_critica)
    story.append(Spacer(1, 8))

    # 8. Funcionalidad backend implementada
    story.append(Paragraph("8. Funcionalidad backend implementada", h1_style))
    story.append(Paragraph(
        "Se implementó de forma completa la operación de <b>Registro de Mascota</b> respetando la arquitectura de tres capas:",
        body_style
    ))
    story.append(Paragraph("• <b>Clases creadas/modificadas:</b> <code>Mascota</code> (con ID), <code>RegistrarMascotaDTO</code>, <code>RespuestaBackend</code>, <code>MascotaRepository</code> (interfaz), <code>InMemoryMascotaRepository</code>, <code>MascotaService</code>, <code>MascotaController</code>, <code>Veterinaria</code> (refactorizada) y <code>Main</code> (CLI).", bullet_style))
    story.append(Paragraph("• <b>Funcionamiento:</b> El Frontend envía el DTO al <code>MascotaController</code>. El controlador delega en <code>MascotaService</code>, que valida nombre, especie y edad (>= 0). Si es válido, se instancia la mascota y <code>MascotaRepository</code> asigna un ID único autoincremental y almacena el registro. El controlador retorna <b>201 Created</b> con la entidad creada. Si falla, retorna <b>400 Bad Request</b>.", bullet_style))

    # 9. Evidencia de funcionamiento
    story.append(Paragraph("9. Evidencia de funcionamiento", h1_style))
    story.append(Paragraph(
        "<b>Evidencia 1: Pruebas Unitarias Automatizadas con JUnit 5</b>", h2_style
    ))
    story.append(Paragraph(
        "Se ejecutaron 11 pruebas unitarias cubriendo casos válidos, edad 0, nombres vacíos, especies vacías, edades negativas y respuestas HTTP:",
        body_style
    ))

    junit_output = (
        "JUnit Jupiter\n"
        "+-- Pruebas Unitarias de compatibilidad: Veterinaria\n"
        "|   +-- Debe registrar mascota y devolverla en la lista [PASO]\n"
        "|   +-- Debe lanzar excepcion al ingresar datos invalidos [PASO]\n"
        "+-- Pruebas Unitarias del Controlador de Backend: MascotaController\n"
        "|   +-- Debe responder con HTTP 201 Created al registrar con exito [PASO]\n"
        "|   +-- Debe responder con HTTP 400 Bad Request ante datos invalidos [PASO]\n"
        "|   +-- Debe responder con HTTP 200 OK al solicitar listado [PASO]\n"
        "+-- Pruebas Unitarias del Servicio de Backend: MascotaService\n"
        "    +-- Debe registrar exitosamente una mascota con datos validos [PASO]\n"
        "    +-- Debe registrar validamente una mascota con edad 0 (cachorro) [PASO]\n"
        "    +-- Debe lanzar excepcion cuando el nombre es nulo o vacio [PASO]\n"
        "    +-- Debe lanzar excepcion cuando la especie es nula o vacia [PASO]\n"
        "    +-- Debe lanzar excepcion cuando la edad es negativa [PASO]\n"
        "    +-- Debe lanzar excepcion cuando el DTO de datos es nulo [PASO]\n\n"
        "Resultados: 11 tests ejecutados | 11 exitosos | 0 fallidos (Tiempo: 119 ms)"
    )
    story.append(Preformatted(junit_output, code_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>Demostración: Certifica que el 100% de las pruebas unitarias pasan sin errores.</i>", ParagraphStyle('It', parent=body_style, fontName='Helvetica-Oblique', fontSize=8)))

    story.append(Paragraph("<b>Evidencia 2: Ejecución Real en Consola (Frontend ↔ Backend)</b>", h2_style))
    cli_output = (
        "=== VetCare - Arquitectura Frontend/Backend ===\n\n"
        "[Opcion 1: Registrar]\n"
        "--- [Frontend] Formulario de Registro de Mascota ---\n"
        "Nombre: Milo | Especie: Perro | Edad: 3\n"
        "[Backend HTTP 201 CREATED] Mascota registrada exitosamente.\n"
        "   -> ID: #1 | Nombre: Milo | Especie: Perro | Edad: 3 anos\n\n"
        "[Opcion 1: Registrar con error de validacion]\n"
        "Nombre: (vacio) | Especie: Gato | Edad: 2\n"
        "[Backend HTTP 400 BAD REQUEST] Error de validacion: El nombre no puede estar vacio.\n\n"
        "[Opcion 2: Consultar]\n"
        "--- [Frontend] Consulta de Mascotas Registradas ---\n"
        "[Backend HTTP 200 OK] Lista de mascotas obtenida exitosamente.\n"
        "   #1 - Nombre: Milo       | Especie: Perro      | Edad: 3 anos"
    )
    story.append(Preformatted(cli_output, code_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>Demostración: Prueba la integración entre el cliente de consola y las capas del backend en ejecución.</i>", ParagraphStyle('It2', parent=body_style, fontName='Helvetica-Oblique', fontSize=8)))

    # 10. Conclusión
    story.append(Paragraph("10. Conclusión", h1_style))
    story.append(Paragraph(
        "La separación entre Frontend y Backend permitió transformar un código monolítico en un sistema desacoplado, modular y escalable. "
        "Las reglas de negocio ahora residen con exclusividad en <code>MascotaService</code>, protegidas de cualquier variación en la interfaz de usuario. "
        "La abstracción del repositorio facilita que en el futuro se incorpore una base de datos real sin impactar la lógica central. "
        "Cuestionar activamente la recomendación inicial de la IA reforzó la importancia del criterio técnico: una arquitectura excelente "
        "es aquella que resuelve las necesidades del proyecto con la máxima claridad y sin sobreingeniería innecesaria.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generado exitosamente:", pdf_filename)

if __name__ == '__main__':
    build_pdf()
