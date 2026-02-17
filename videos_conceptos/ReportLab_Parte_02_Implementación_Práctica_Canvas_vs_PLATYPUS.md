Imagina que tienes dos herramientas: un pincel de precisión para control absoluto y un motor de composición automática que maquetea por ti. ¿Cuándo usarías cada una? Descubramos el poder de las dos APIs de ReportLab, `canvas` y `PLATYPUS`, para crear desde un simple ticket hasta una factura compleja de varias páginas.

# ReportLab

## 4. Implementación Práctica: Del Pincel al Motor de Composición

Basta de teoría. Vamos a mancharnos las manos de tinta digital.

### El Pincel: La API `canvas`

Imagina que estás diseñando una entrada para un evento. El diseño es fijo. Aquí, el `canvas` es tu mejor amigo.

```python
# canvas_example.py
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_ticket():
    """
    Genera una entrada de evento simple usando la API de bajo nivel Canvas.
    """
    file_path = "event_ticket.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # --- Cabecera ---
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2.0, height - inch, "CONCIERTO DE PYTHON CÓSMICO")

    # --- Línea divisoria ---
    c.setStrokeColor(colors.grey)
    c.setLineWidth(2)
    c.line(0.5 * inch, height - 1.25 * inch, width - 0.5 * inch, height - 1.25 * inch)

    # --- Contenido ---
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    
    # Usando text objects para un mejor control del posicionamiento
    text = c.beginText()
    text.setTextOrigin(inch, height - 2 * inch)
    text.setFont("Helvetica", 12)
    text.textLine("Artista: The GILs")
    text.textLine("Fecha: 31 de Octubre, 2023")
    text.textLine("Lugar: El Bucle Infinito, Sala 42")
    text.moveCursor(0, 20) # Mover el cursor hacia arriba 20 puntos
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Asiento: Fila 1, Silla 0")
    c.drawText(text)

    # --- Código QR (simulado con un rectángulo) ---
    c.setFillColor(colors.black)
    c.rect(width - 2 * inch, inch, 1.5 * inch, 1.5 * inch, fill=1)
    c.setFont("Courier", 8)
    c.setFillColor(colors.white)
    c.drawCentredString(width - 1.25 * inch, inch + 0.75 * inch, "SCAN ME")

    # --- Guardar el PDF ---
    c.showPage()
    c.save()
    print(f"Ticket generado en: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    create_ticket()
```

**Análisis del código:**
*   **Control Absoluto:** Nota cómo especificamos cada coordenada `(x, y)`. Esto es potente pero frágil. Si el texto del título cambia a algo más largo, tendremos que recalcular el centro manualmente.
*   **Estado de la Máquina:** El `canvas` es una máquina de estados. `setFont`, `setFillColor`, etc., establecen el estado para las operaciones de dibujo subsiguientes.
*   **Text Objects:** Usar `beginText()` y `drawText()` es más eficiente que múltiples llamadas a `drawString()` para bloques de texto, ya que agrupa las operaciones de texto en el PDF subyacente.

### El Motor de Composición: PLATYPUS

Ahora, el caso de estudio del mundo real: una factura. Múltiples productos, totales, impuestos, y podría ocupar varias páginas. Usar el `canvas` para esto sería una pesadilla de mantenimiento.

**Mal vs. Bien: La Factura**

*   **Mal (Solo Canvas):** Tendrías que calcular la altura de cada línea de producto, mantener un contador `y` actual, y cuando `y` sea menor que el margen inferior, insertar un salto de página manualmente y dibujar la cabecera de la nueva página. Si una fuente cambia, todo se descuadra. Es un castillo de naipes.
*   **Bien (PLATYPUS):** Defines la estructura y dejas que el motor haga el trabajo pesado.

```python
# platypus_invoice.py
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_invoice(data):
    """
    Genera una factura compleja usando la API de alto nivel PLATYPUS.
    """
    file_path = "invoice.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    
    # Contenedor para los "Flowables"
    story = []
    
    styles = getSampleStyleSheet()
    # Estilo personalizado para el título
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, alignment=TA_CENTER, spaceAfter=20))
    # Estilo personalizado para las celdas de la tabla
    styles.add(ParagraphStyle(name='TableCellRight', alignment=TA_RIGHT))

    # --- Título ---
    story.append(Paragraph("FACTURA", styles['TitleStyle']))
    
    # --- Información del cliente (usando un párrafo con formato) ---
    customer_info = f"""
    <b>Cliente:</b> {data['customer_name']}<br/>
    <b>Dirección:</b> {data['customer_address']}<br/>
    <b>Fecha:</b> {data['invoice_date']}
    """
    story.append(Paragraph(customer_info, styles['Normal']))
    story.append(Spacer(1, 0.25 * inch))

    # --- Tabla de productos ---
    table_data = [['Producto', 'Cantidad', 'Precio Unitario', 'Total']]
    for item in data['items']:
        total_item = item['quantity'] * item['price']
        table_data.append([
            Paragraph(item['description'], styles['Normal']),
            Paragraph(str(item['quantity']), styles['TableCellRight']),
            Paragraph(f"${item['price']:.2f}", styles['TableCellRight']),
            Paragraph(f"${total_item:.2f}", styles['TableCellRight'])
        ])
    
    # --- Fila de totales ---
    subtotal = sum(item['quantity'] * item['price'] for item in data['items'])
    tax = subtotal * data['tax_rate']
    total = subtotal + tax
    
    table_data.append(['', '', Paragraph("<b>Subtotal</b>", styles['TableCellRight']), Paragraph(f"${subtotal:.2f}", styles['TableCellRight'])])
    table_data.append(['', '', Paragraph("<b>Impuestos (16%)</b>", styles['TableCellRight']), Paragraph(f"${tax:.2f}", styles['TableCellRight'])])
    table_data.append(['', '', Paragraph("<b>TOTAL</b>", styles['TableCellRight']), Paragraph(f"<b>${total:.2f}</b>", styles['TableCellRight'])])

    invoice_table = Table(table_data, colWidths=[3 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    
    # --- Estilos de la tabla ---
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Estilos para las filas de totales
        ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ])
    invoice_table.setStyle(style)
    
    story.append(invoice_table)
    
    # --- Construir el PDF ---
    doc.build(story)
    print(f"Factura generada en: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    invoice_data = {
        "customer_name": "Acme Corp.",
        "customer_address": "123 Main Street, Anytown",
        "invoice_date": "2023-10-31",
        "tax_rate": 0.16,
        "items": [
            {"description": "Cohete Personal de Bolsillo", "quantity": 2, "price": 1200.00},
            {"description": "Semillas de Pájaro Gigante (saco)", "quantity": 10, "price": 25.50},
            {"description": "Yunque de Suspensión de Incredulidad", "quantity": 1, "price": 450.75},
            # Añade suficientes items para forzar un salto de página
            *([{"description": f"Tornillo Estándar #{i}", "quantity": 100, "price": 0.05} for i in range(30)])
        ]
    }
    create_invoice(invoice_data)
```

**Análisis del código:**
*   **Declarativo:** No decimos *dónde* dibujar la tabla. Simplemente la añadimos al `story`. PLATYPUS se encarga de colocarla, y si no cabe en la página actual, la dividirá elegantemente (con cabeceras repetidas si se lo pides).
*   **Flowables:** `Paragraph`, `Spacer`, `Table` son los bloques de construcción. Fluyen dentro de los marcos definidos en la plantilla del documento.
*   **Estilos:** La separación de contenido y presentación es clave. Usamos `ParagraphStyle` y `TableStyle` para definir la apariencia. Cambiar el estilo de todas las celdas de la tabla es un cambio en un solo lugar. Esto es mantenibilidad.