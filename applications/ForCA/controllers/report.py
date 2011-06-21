from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from uuid import uuid4
from cgi import escape

from cStringIO import StringIO

def generate():
    '''
    Gera um relatorio em pdf contendo as avaliacoes de um professor
    '''

    prof_id = request.vars['prof_id']
    prof = db(Professores.id==prof_id).select().first()
    evals = get_refined_evals(prof_id=prof_id)

    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=avaliacoes.pdf'

    buf = StringIO()

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(buf)
    story = []

    title = '''
    Avaliacoes de %s
    ''' % prof.full_name

    subtitle = '''
    Média geral: %s    Total de avaliações: %s
    ''' % (prof.grade, str(len(evals)))

    story.append(Paragraph(escape(title), styles["Title"]))
    story.append(Spacer(1,0.5*inch))
    story.append(Paragraph(escape(subtitle), styles["Heading2"]))
    story.append(Spacer(1,0.5*inch))

    for eval in evals:
        
        heading = '''
        %s sobre %s por %s em %s:
        ''' % ((eval['aluno_name'] if not eval['anonimo'] else 'Anônimo'),
                eval['prof_name'],
                eval['disc_name'],
                eval['semester'])

        date = str(eval['timestamp_eval'])

        text = (eval['comment'] or '<o aluno não deixou um comentário>')

        story.append(Paragraph(escape(heading), styles["Heading2"]))
        story.append(Paragraph(escape(date), styles["Normal"]))
        story.append(Paragraph(escape(text), styles["Normal"]))
        story.append(Spacer(1,0.5*inch))

    doc.build(story)

    #doc.showPage()
    #doc.save()
    return buf.getvalue()
