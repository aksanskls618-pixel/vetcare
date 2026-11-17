import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
            self.drawString(45, A4[1] - 30, "Actividad: Mejorá el agente — Generación T (Módulo 3)")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(45, A4[1] - 34, A4[0] - 45, A4[1] - 34)
            
        # Footer (all pages)
        footer_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 45, 25, footer_text)
        self.drawString(45, 25, "Entrega Académica — Trabajo Individual · Módulo 3")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(45, 35, A4[0] - 45, 35)
        self.restoreState()

def build_pdf():
    pdf_filename = "ACTIVIDAD_MEJORA_EL_AGENTE.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1E3A8A")   # Blue-900
    dark_text = colors.HexColor("#1F2937")       # Gray-800
    muted_text = colors.HexColor("#4B5563")      # Gray-600
    bg_code = colors.HexColor("#F8FAFC")         # Slate-50

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=muted_text,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=dark_text,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-9,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=body_style,
        fontSize=7.8,
        leading=10,
        spaceAfter=0
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Actividad — Mejorá el agente", title_style))
    story.append(Paragraph("<b>Módulo 3 · Trabajo individual</b> &nbsp;|&nbsp; <b>Proyecto:</b> VetCare &nbsp;|&nbsp; <b>Fecha:</b> Octubre 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    # 1. Breve explicación del objetivo
    story.append(Paragraph("1. Breve explicación del objetivo", h1_style))
    story.append(Paragraph(
        "El objetivo de esta actividad es afinar y mejorar un subagente revisor de código (<code>revisor</code>). "
        "En clase se construyó una versión inicial básica que cumple con no modificar archivos (<code>readonly: true</code>), "
        "pero sus respuestas resultaban abstractas y poco prácticas. En esta entrega se implementan cuatro mejoras justificadas "
        "para que el revisor proporcione hallazgos precisos, señale la ubicación de los fallos, describa situaciones concretas de ocurrencia, "
        "advierta cuando falta contexto y brinde recomendaciones breves de corrección.",
        body_style
    ))

    # 2. Archivo mejorado
    story.append(Paragraph("2. Archivo mejorado (revisor.md)", h1_style))
    story.append(Paragraph("Se mantiene obligatoriamente <code>readonly: true</code> como exige la consigna:", body_style))

    revisor_code = (
        "---\n"
        "name: revisor\n"
        "description: Revisa cambios de codigo buscando problemas concretos de seguridad, validacion, manejo de errores, rendimiento y permisos. Usar al agregar endpoints, modificar acceso a datos o configuracion, o antes de subir cambios a produccion.\n"
        "model: inherit\n"
        "readonly: true\n"
        "---\n\n"
        "Sos un revisor de codigo con foco en seguridad y robustez. Revisas codigo antes de que llegue a produccion. No modifiques archivos ni ejecutes acciones que cambien el proyecto.\n\n"
        "Para cada revision:\n"
        "1. Revisa el codigo modificado y, cuando sea necesario, el contexto relacionado para entender como se usa.\n"
        "2. Busca entradas externas sin validar, fallas que puedan afectar al resto del sistema, problemas que aparezcan al crecer el volumen y permisos excesivos.\n"
        "3. Prioriza los hallazgos por riesgo real. Para cada uno, indica:\n"
        "   - archivo y ubicacion aproximada;\n"
        "   - problema observado;\n"
        "   - situacion concreta en la que puede ocurrir;\n"
        "   - impacto;\n"
        "   - recomendacion breve para corregirlo.\n"
        "4. Si no encontras problemas en una categoria, indica que no detectaste hallazgos en esa revision, sin asegurar que el codigo sea totalmente seguro.\n\n"
        "No reescribas el codigo ni apliques cambios. No propongas refactors generales. No comentes nombres de variables, formato ni estilo, salvo que afecten directamente la seguridad o el funcionamiento.\n\n"
        "Ordena los hallazgos de mas grave a menos grave. Mostra como maximo cinco. Evita repetir el mismo problema y no informes riesgos hipoteticos si no podes explicar una situacion concreta que los provoque.\n\n"
        "Cuando falte contexto para confirmar un hallazgo, marca esa limitacion en lugar de presentarlo como un hecho. Mantene la respuesta breve, clara y enfocada en acciones que se puedan verificar."
    )
    
    t_box = Table([[Preformatted(revisor_code, code_style)]], colWidths=[505])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_code),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 6))

    # 3. Justificación de cada cambio
    story.append(Paragraph("3. Justificación de cada cambio", h1_style))
    story.append(Paragraph("• <b>Cambio 1: Ampliar la descripción del agente (frontmatter).</b> Se detallaron los temas específicos que revisa (seguridad, validación, manejo de errores, rendimiento y permisos) y ejemplos de uso. Esto permite que el orquestador sepa exactamente cuándo invocar al subagente.", bullet_style))
    story.append(Paragraph("• <b>Cambio 2: Pedir ubicación, escenario concreto e impacto por hallazgo.</b> Antes el agente respondía preguntas teóricas al aire. Ahora debe indicar el archivo, ubicación aproximada y la situación en que ocurre la falla para que el reporte sea directamente accionable.", bullet_style))
    story.append(Paragraph("• <b>Cambio 3: Declarar explícitamente la falta de contexto y límites de certeza.</b> Si no cuenta con suficiente información para confirmar un riesgo, debe marcar esa limitación en vez de inventar supuestos. También evita garantizar seguridad absoluta cuando no halla problemas.", bullet_style))
    story.append(Paragraph("• <b>Cambio 4: Permitir recomendación breve y limitar a 5 hallazgos priorizados.</b> Puede sugerir una solución de una línea sin reescribir código ni hacer refactors generales, ordenando de más grave a menos grave para evitar reportes interminables.", bullet_style))

    # 4. Evidencia de la prueba del agente original
    story.append(Paragraph("4. Evidencia de la prueba del agente original", h1_style))
    story.append(Paragraph("Se evaluó el subagente original sobre el archivo <code>Veterinaria.java</code> de VetCare:", body_style))
    
    original_evidence = (
        "Revision del archivo Veterinaria.java con el Agente Original:\n\n"
        "1. Que datos entran desde afuera sin validarse?\n"
        "En el metodo registrarMascota entran nombre, especie y edad. Se valida que no sean vacios\n"
        "y edad no negativa, pero no hay limite de caracteres ni sanitizacion.\n\n"
        "2. Que pasa si esto falla? El resto del sistema sobrevive?\n"
        "Si los datos son invalidos se lanza IllegalArgumentException. Si quien llama no tiene\n"
        "un try-catch adecuado, la aplicacion puede caerse de forma no controlada.\n\n"
        "3. Que se rompe cuando el volumen crezca?\n"
        "Las mascotas se guardan en memoria. Al llegar a miles de registros se consumira la memoria RAM,\n"
        "afectando el rendimiento general.\n\n"
        "4. Quien puede ejecutar esto y con que permisos?\n"
        "Cualquiera puede invocar el metodo ya que es publico y no hay control de roles ni permisos."
    )
    t_evid1 = Table([[Preformatted(original_evidence, code_style)]], colWidths=[505])
    t_evid1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#FCD34D")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_evid1)
    story.append(Spacer(1, 6))

    # 5. Evidencia de la prueba del agente mejorado
    story.append(Paragraph("5. Evidencia de la prueba del agente mejorado", h1_style))
    story.append(Paragraph("Se evaluó el subagente mejorado sobre exactamente el mismo archivo <code>Veterinaria.java</code>:", body_style))

    mejorado_evidence = (
        "Hallazgos de Seguridad y Robustez (ordenados por gravedad):\n\n"
        "1. [Gravedad Alta]\n"
        "- Archivo y ubicacion: src/main/java/com/vetcare/Veterinaria.java (lineas 13-16 y 31-33)\n"
        "- Problema observado: Coleccion interna y repositorio sin sincronizacion concurrente.\n"
        "- Situacion concreta: Si multiples hilos/usuarios registran o listan mascotas en paralelo.\n"
        "- Impacto: Riesgo de estado inconsistente o excepciones ConcurrentModificationException.\n"
        "- Recomendacion breve: Usar estructuras concurrentes o sincronizar accesos.\n\n"
        "2. [Gravedad Media]\n"
        "- Archivo y ubicacion: src/main/java/com/vetcare/Veterinaria.java (lineas 27-29)\n"
        "- Problema observado: Propagacion de IllegalArgumentException hacia la capa cliente.\n"
        "- Situacion concreta: Cliente ingresa datos invalidos y la UI no captura la excepcion.\n"
        "- Impacto: Cierre inesperado o falla no manejada en la interfaz.\n"
        "- Recomendacion breve: Documentar excepcion en contrato o usar respuesta tipada/DTO.\n\n"
        "3. [Gravedad Baja]\n"
        "- Archivo y ubicacion: src/main/java/com/vetcare/Veterinaria.java (lineas 27-28)\n"
        "- Problema observado: Ausencia de limite superior en la longitud de strings.\n"
        "- Situacion concreta: Usuario ingresa textos con miles de caracteres.\n"
        "- Impacto: Desperdicio de memoria y desborde visual en pantalla.\n"
        "- Recomendacion breve: Validar longitud maxima razonable (ej. nombre <= 50 caracteres).\n\n"
        "Nota de contexto y limitaciones:\n"
        "No se evaluaron permisos de usuario por tratarse de logica de negocio interna; se requiere\n"
        "inspeccionar controladores o modulo de autenticacion para verificar control de acceso."
    )
    t_evid2 = Table([[Preformatted(mejorado_evidence, code_style)]], colWidths=[505])
    t_evid2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#86EFAC")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_evid2)
    story.append(Spacer(1, 6))

    # 6. Comparación de resultados
    story.append(Paragraph("6. Comparación de resultados", h1_style))
    
    comparacion_data = [
        [Paragraph("Aspecto", table_header_style), Paragraph("Agente Original", table_header_style), Paragraph("Agente Mejorado", table_header_style)],
        [Paragraph("<b>Estructura</b>", table_cell_style), Paragraph("Respuestas en prosa a 4 preguntas fijas.", table_cell_style), Paragraph("Ficha técnica estructurada con 5 campos por hallazgo.", table_cell_style)],
        [Paragraph("<b>Ubicación del fallo</b>", table_cell_style), Paragraph("No indica archivos ni números de línea.", table_cell_style), Paragraph("Señala el archivo y el rango aproximado de líneas.", table_cell_style)],
        [Paragraph("<b>Escenario concreto</b>", table_cell_style), Paragraph("Riesgos abstractos sin escenario de prueba.", table_cell_style), Paragraph("Describe la situación exacta de ejecución que provoca la falla.", table_cell_style)],
        [Paragraph("<b>Recomendación</b>", table_cell_style), Paragraph("No sugiere cómo resolver el problema.", table_cell_style), Paragraph("Aporta una recomendación breve de una línea para corregir.", table_cell_style)],
        [Paragraph("<b>Manejo de contexto</b>", table_cell_style), Paragraph("Critica la falta de permisos como un fallo.", table_cell_style), Paragraph("Aclara la limitación de contexto sin asumir hechos.", table_cell_style)],
        [Paragraph("<b>Priorización</b>", table_cell_style), Paragraph("Orden disperso según las 4 preguntas.", table_cell_style), Paragraph("Jerarquizado estrictamente de mayor a menor gravedad.", table_cell_style)]
    ]
    t_comp = Table(comparacion_data, colWidths=[105, 200, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    # 7. Cómo ejecutar manualmente en Antigravity
    story.append(Paragraph("7. Instrucciones para ejecución manual en Antigravity", h1_style))
    story.append(Paragraph(
        "Para comprobar estas pruebas directamente en Antigravity: "
        "<br/>1. Abrir el proyecto <code>vetcare</code> en Antigravity IDE."
        "<br/>2. En el chat lateral, invocar al subagente escribiendo: <code>@revisor revisá src/main/java/com/vetcare/Veterinaria.java</code>"
        "<br/>3. Para probar la versión original, usar las instrucciones guardadas en <code>revisor_original.md</code>."
        "<br/>4. Se pueden capturar ambas ventanas de chat para anexar como evidencia adicional.",
        body_style
    ))

    # 8. Conclusión
    story.append(Paragraph("8. Conclusión", h1_style))
    story.append(Paragraph(
        "Al realizar esta actividad aprendí que mejorar un agente de IA no consiste en hacerlo hablar más, sino en <b>darle instrucciones más claras y estructuradas</b>. "
        "El agente original respondía de manera abstracta y poco útil para el trabajo diario. Al agregarle una estructura con ubicación exacta, "
        "escenario concreto, impacto y sugerencias breves, los resultados se volvieron realmente aplicables para el programador. "
        "También aprendí la importancia de ponerle límites: mantenerlo en <code>readonly: true</code> para que nunca modifique código sin permiso, "
        "pedirle que no invente suposiciones cuando le falta contexto y acotar los resultados a un máximo de cinco hallazgos priorizados.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generado exitosamente:", pdf_filename)

if __name__ == '__main__':
    build_pdf()
