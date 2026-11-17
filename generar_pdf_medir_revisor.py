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
            self.drawString(45, A4[1] - 30, "Mini actividad: Medí tu revisor — Generación T (Módulo 3)")
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
    pdf_filename = "MINI_ACTIVIDAD_MEDI_TU_REVISOR.pdf"
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
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=muted_text,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=dark_text,
        spaceAfter=4
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
        fontSize=7.6,
        leading=9.8,
        spaceAfter=0
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Mini actividad — Medí tu revisor", title_style))
    story.append(Paragraph("<b>Módulo 3 · Trabajo individual · 30 minutos</b> &nbsp;|&nbsp; <b>Proyecto:</b> VetCare &nbsp;|&nbsp; <b>Fecha:</b> Octubre 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    # Introducción
    story.append(Paragraph(
        "<b>Propósito:</b> Medir de forma cuantitativa y objetiva si el subagente revisor realmente sirve, evaluando no solo si detecta "
        "problemas reales, sino también si tiene la capacidad de callarse ante archivos sanos sin emitir falsos positivos.",
        body_style
    ))

    # Paso 1
    story.append(Paragraph("Paso 1 — Elección de los 5 archivos del proyecto", h1_style))
    story.append(Paragraph("Se seleccionaron dos archivos sanos y tres con problemas conocidos de <b>VetCare</b>:", body_style))
    story.append(Paragraph("• <b>Mascota.java (Sano):</b> POJO plano de entidad. No maneja persistencia ni lógica; debe mantenerse en silencio.", bullet_style))
    story.append(Paragraph("• <b>RegistrarMascotaDTO.java (Sano):</b> DTO puro de transporte entre capas. No debe exigir validaciones de negocio internas.", bullet_style))
    story.append(Paragraph("• <b>InMemoryMascotaRepository.java (Con problema):</b> ArrayList sin sincronización multi-hilo y acumulación ilimitada en memoria RAM.", bullet_style))
    story.append(Paragraph("• <b>MascotaService.java (Con problema):</b> Validación incompleta (no restringe longitud máxima de texto ni edad máxima biológica).", bullet_style))
    story.append(Paragraph("• <b>Main.java (Con problema):</b> Entrada por consola con Scanner sin sanitización ni acotación de tamaño por teclado.", bullet_style))

    # Paso 2 y 3 - Corrida 1
    story.append(Paragraph("Paso 2 y 3 — Tabla y Medición Inicial (Corrida 1)", h1_style))
    story.append(Paragraph("Completado de expectativas antes de correr y resultado de la primera evaluación:", body_style))

    c1_data = [
        [Paragraph("Archivo", table_header_style), Paragraph("Estado", table_header_style), Paragraph("Qué espero que encuentre", table_header_style), Paragraph("¿Lo encontró en Corrida 1?", table_header_style)],
        [Paragraph("<code>Mascota.java</code>", table_cell_style), Paragraph("Sano", table_cell_style), Paragraph("Nada. Silencio o 0 hallazgos (POJO limpio).", table_cell_style), Paragraph("<b>SÍ (Acertó)</b>: No reportó problemas.", table_cell_style)],
        [Paragraph("<code>RegistrarMascotaDTO.java</code>", table_cell_style), Paragraph("Sano", table_cell_style), Paragraph("Nada. Debe callarse (DTO pasivo sin lógica).", table_cell_style), Paragraph("<b>NO (Falló)</b>: Alertó falsos positivos en setters.", table_cell_style)],
        [Paragraph("<code>InMemoryMascotaRepository.java</code>", table_cell_style), Paragraph("Con problema", table_cell_style), Paragraph("Falta de sincronización concurrente y memoria.", table_cell_style), Paragraph("<b>SÍ (Acertó)</b>: Detectó concurrencia y heap.", table_cell_style)],
        [Paragraph("<code>MascotaService.java</code>", table_cell_style), Paragraph("Con problema", table_cell_style), Paragraph("Ausencia de límites superiores en texto y edad.", table_cell_style), Paragraph("<b>SÍ (Acertó)</b>: Reportó falta de límite máximo.", table_cell_style)],
        [Paragraph("<code>Main.java</code>", table_cell_style), Paragraph("Con problema", table_cell_style), Paragraph("Lectura por consola con Scanner sin acotar.", table_cell_style), Paragraph("<b>SÍ (Acertó)</b>: Señaló lecturas no acotadas.", table_cell_style)]
    ]
    t_c1 = Table(c1_data, colWidths=[120, 60, 175, 150])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Resultado inicial:</b> Mi revisor acertó <b>4 de 5</b>.", ParagraphStyle('R1', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#B45309"))))

    # Paso 4 - Cambio de una línea
    story.append(Paragraph("Paso 4 — Modificación de UNA sola línea en el revisor", h1_style))
    story.append(Paragraph(
        "<b>Problema detectado:</b> El revisor consideraba un defecto que las clases DTO no contaran con lógica de validación interna, "
        "ignorando que los DTOs son contenedores agnósticos y que la validación corresponde al Service.<br/>"
        "<b>Línea modificada en <code>revisor.md</code> (línea 22):</b>",
        body_style
    ))

    diff_text = (
        "- No reescribas el codigo ni apliques cambios. No propongas refactors generales.\n"
        "  No comentes nombres de variables, formato ni estilo, salvo que afecten directamente...\n"
        "+ No reescribas codigo ni refactors generales. No opines de estilo ni exijas logica\n"
        "  de validacion dentro de clases puramente pasivas (DTOs o entidades POJO)."
    )
    t_diff = Table([[Preformatted(diff_text, code_style)]], colWidths=[505])
    t_diff.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF3C7")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#F59E0B")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_diff)
    story.append(Spacer(1, 4))

    # Qué entregás
    story.append(Paragraph("Qué entregás — Respuestas requeridas", h1_style))

    story.append(Paragraph("<b>1. Tabla completa comparativa con las dos corridas:</b>", body_style))
    
    comparativa_final = [
        [Paragraph("Archivo", table_header_style), Paragraph("Estado", table_header_style), Paragraph("Qué esperaba encontrar", table_header_style), Paragraph("Corrida 1 (Inicial)", table_header_style), Paragraph("Corrida 2 (Tras cambio)", table_header_style)],
        [Paragraph("<code>Mascota.java</code>", table_cell_style), Paragraph("Sano", table_cell_style), Paragraph("Silencio / 0 hallazgos", table_cell_style), Paragraph("<b>Acertó</b> (silencio)", table_cell_style), Paragraph("<b>Acertó</b> (silencio)", table_cell_style)],
        [Paragraph("<code>RegistrarMascotaDTO.java</code>", table_cell_style), Paragraph("Sano", table_cell_style), Paragraph("Silencio / 0 hallazgos", table_cell_style), Paragraph("<b>Falló</b> (falso positivo)", table_cell_style), Paragraph("<b>Acertó</b> (silencio)", table_cell_style)],
        [Paragraph("<code>InMemoryMascotaRepository.java</code>", table_cell_style), Paragraph("Con problema", table_cell_style), Paragraph("Concurrencia y memoria", table_cell_style), Paragraph("<b>Acertó</b> (detectó)", table_cell_style), Paragraph("<b>Acertó</b> (detectó)", table_cell_style)],
        [Paragraph("<code>MascotaService.java</code>", table_cell_style), Paragraph("Con problema", table_cell_style), Paragraph("Falta de tope superior", table_cell_style), Paragraph("<b>Acertó</b> (detectó)", table_cell_style), Paragraph("<b>Acertó</b> (detectó)", table_cell_style)],
        [Paragraph("<code>Main.java</code>", table_cell_style), Paragraph("Con problema", table_cell_style), Paragraph("Entrada Scanner no acotada", table_cell_style), Paragraph("<b>Acertó</b> (detectó)", table_cell_style), Paragraph("<b>Acertó</b> (detectó)", table_cell_style)]
    ]
    t_final = Table(comparativa_final, colWidths=[105, 55, 135, 105, 105])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_final)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Qué cambiaste y por qué, en dos líneas:</b>", body_style))
    story.append(Paragraph(
        "<i>Modifiqué la directiva de restricciones del revisor para prohibirle exigir lógica de validación dentro de clases puramente pasivas (DTOs o entidades POJO). "
        "Esto evita que el agente confunda objetos de transferencia de datos con capas de negocio activas, eliminando falsos positivos.</i>",
        ParagraphStyle('Ans2', parent=body_style, leftIndent=10)
    ))

    story.append(Paragraph("<b>3. Qué pasó con el número y qué caso concreto cambió:</b>", body_style))
    story.append(Paragraph(
        "• <b>Evolución del número:</b> Subió de <b>4 de 5</b> a <b>5 de 5</b> tras el cambio.<br/>"
        "• <b>Caso concreto modificado:</b> <code>RegistrarMascotaDTO.java</code>. En la primera corrida, el agente emitía una advertencia innecesaria sobre los setters del DTO; en la segunda corrida, reconoció su naturaleza pasiva y supo callarse con total precisión.",
        ParagraphStyle('Ans3', parent=body_style, leftIndent=10)
    ))

    story.append(Paragraph("Conclusión", h1_style))
    story.append(Paragraph(
        "Esta actividad demostró que evaluar un agente requiere obligatoriamente incluir archivos sanos para verificar si sabe callarse. "
        "Ajustar una sola línea de instrucción calibró la sensibilidad del revisor, eliminando falsas alarmas y elevando su precisión a 5 de 5.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generado exitosamente:", pdf_filename)

if __name__ == '__main__':
    build_pdf()
