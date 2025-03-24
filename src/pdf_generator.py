from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors

def gerar_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para o corpo do texto
    styles.add(ParagraphStyle(
        name='Corpo',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        leading=14,
        spaceAfter=6,
    ))

    elements = []
    
    # Cabeçalho
    elements.append(Paragraph(f"Crônicas de {data['mundo']}", styles['Title']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Corpo do documento
    for capitulo in data['historico']:
        # Sanitizar o conteúdo
        descricao = capitulo['descricao'].replace('<br>', '<br/>')  # Garantir tags válidas
        
        elements.append(Paragraph(capitulo['titulo'], styles['Heading2']))
        elements.append(Paragraph(descricao, styles['Corpo']))
        elements.append(Spacer(1, 0.2*inch))
        
        if capitulo.get('acao_escolhida'):
            elements.append(Paragraph(f"Escolha: {capitulo['acao_escolhida']}", styles['Heading3']))
        
        elements.append(PageBreak())
    
    doc.build(elements)