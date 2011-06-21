def index():
    profs = db().select(db.professores.ALL, orderby=db.professores.full_name)
    return dict(profs=profs)    

@auth.requires_login()
def create():
    '''
    Função cria uma avaliação para um determinado professor.
    '''
    if 'prof_id' in request.vars:
        prof_id = request.vars['prof_id']
        prof_name = db(db.professores.id==prof_id).select().first().short_name
        form_add=SQLFORM(db.avaliacoes, submit_button = 'Criar',
            fields = ['disciplina_id','year','semester','grade','comment', 'anonimo'], 
            labels = {'disciplina_id':'Disciplina: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: ','anonimo': 'Anônimo:'},
            hidden = dict(aluno_id=get_aluno_id(), professor_id=prof_id))
        form_add.vars.professor_id = prof_id
        form_add[0][0] = gae_disc_biased_dropdown(prof_id)

    elif 'disc_id' in request.vars:
        disc_id = request.vars['disc_id']
        disc_name = db(db.disciplinas.id==disc_id).select().first().short_name
        form_add=SQLFORM(db.avaliacoes,
            fields = ['professor_id','year','semester','grade','comment', 'anonimo'],
            labels = {'professor_id':'Professor: ','year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: ','anonimo:': 'Anonimo:'},
            hidden = dict(aluno_id=get_aluno_id(), disciplina_id=disc_id))
        form_add.vars.disciplina_id = disc_id
        form_add[0][0] = gae_prof_biased_dropdown(disc_id)

    form_add.vars.aluno_id = get_aluno_id()

    if form_add.accepts(request.vars, session, onvalidation=check_unique_eval):
        session.flash = 'Avaliação realizada com sucesso'
        if 'prof_id' in request.vars:
            update_grade(prof_id, request.vars['disciplina_id'])
            update_profs_discs(prof_id, request.vars['disciplina_id'])
            redirect(URL(request.application, 'prof', 'home', vars=dict(prof_id=prof_id)))
        else:
            update_grade(request.vars['professor_id'], disc_id)
            update_profs_discs(request.vars['professor_id'], disc_id)
            redirect(URL(request.application, 'disc', 'home', vars=dict(disc_id=disc_id)))
    else:
        response.flash = 'Por favor, preencha a sua avaliação'

    if 'prof_id' in request.vars:
        return dict(prof_name=prof_name, form_add=form_add)
    else:
        return dict(disc_name=disc_name, form_add=form_add)

@auth.requires_login()
def update():
    '''
    Função faz update de registro já existente
    '''
    if request.wsgi.environ['REQUEST_METHOD'] == 'GET':
        session.jump_back = request.env.http_referer
    record = Avaliacoes(request.vars['eval_id'])
    if not record.reply:
        prof_id = record.professor_id
        disc_id = record.disciplina_id
        form_up=SQLFORM(db.avaliacoes, record, submit_button = 'Salvar',
            fields=['year','semester','grade','comment'], 
            labels={'year':'Ano: ','semester':'Semestre: ','grade':'Nota: ','comment':'Comentário: '}, showid=False)

        if form_up.accepts(request.vars, session):
            session.flash = 'Avaliação editada com sucesso'
            update_grade(prof_id, disc_id)
            update_timestamp_eval(record.id)
            redirect(session.jump_back)
        else:
            response.flash = 'Por favor, preencha a sua avaliação'  
        return dict(form_up=form_up)
    else:
        session.flash = T('Você não pode editar uma avaliação respondida')
        redirect(session.jump_back)
    
@auth.requires_login()
def favorite():
    '''
    Função favorita ou desfavorita uma avaliação para o usuario logado, dependendo do estado atual
    '''
    eval_id = request.vars['eval_id']
    favorita_eval(eval_id)
    if eh_favorita(eval_id):
        img = IMG(_src=URL('static', 'star_filled.png'), _title=T('Desfavoritar avaliação'))
    else:
        img = IMG(_src=URL('static', 'star_hollow.png'), _title=T('Favoritar avaliação'))
    return img

@auth.requires_membership('Professor')
def reply():
    '''
    Função para postagem de resposta por parte de professor
    '''
    if request.wsgi.environ['REQUEST_METHOD'] == 'GET':
        session.jump_back = request.env.http_referer
    eval = db.avaliacoes(request.vars['eval_id'])
    form_reply = SQLFORM(db.avaliacoes, eval,
            fields = ['reply'],
            labels = {'reply':'Resposta: '},
            showid = False)

    if form_reply.accepts(request.vars, session):
        update_timestamp_reply(eval.id)
        session.flash = T('Resposta postada com sucesso')
        redirect(session.jump_back)
    else:
        response.flash = T('Por favor, preencha a sua resposta')

    return dict(form_reply = form_reply, eval = eval)

@auth.requires_membership('Professor')
def reply_delete():
    '''
    Exclui uma resposta postada pelo professor a uma avaliacao
    '''
    if request.wsgi.environ['REQUEST_METHOD'] == 'GET':
        session.jump_back = request.env.http_referer
    db(Avaliacoes.id==request.vars['eval_id']).update(reply=None, timestamp_reply=None)
    db.commit()
    session.flash = T('Resposta excluída com sucesso')
    redirect(session.jump_back)

@auth.requires_login()
def delete():
    '''
    Função que deleta uma avaliação existente
    '''
    if request.wsgi.environ['REQUEST_METHOD'] == 'GET':
        session.jump_back = request.env.http_referer
    eval_id = request.vars['eval_id']
    eval = db.avaliacoes[eval_id]
    if not eval.reply:
        prof_id = eval.professor_id
        disc_id = eval.disciplina_id
        db(db.avaliacoes.id==eval_id).delete()
        db.commit()
        update_grade(prof_id, disc_id)
        session.flash = T('Avaliação excluída com sucesso')
        redirect(session.jump_back)
    else:
        session.flash = T('Você não pode excluir uma avaliação respondida')
        redirect(session.jump_back)

def filter():
    '''
    Retorna avaliações de acordo com diversos critérios e filtros
    '''
    if len(request.args) and 'submit' not in request.vars:
        page = int(request.args[0])
    else:
        page = 0
    limitby = (page*10, (page+1)*11)
    query, defaults = get_filter_query(db(Avaliacoes.id > 0))

    raw_evals = query.select()

    raw_evals = raw_evals.sort(lambda row: row.karma, reverse=True)
    raw_evals = raw_evals.sort(lambda row: row.timestamp_eval, reverse=True)
    if not auth.has_membership('Admin'):
        raw_evals = raw_evals.sort(lambda row: row.anonimo)

    result = refine_evals(raw_evals[limitby[0]:limitby[1]])
    
    fields = {}

    fields['prof'] = get_prof_dropdown(default=defaults['prof_id'])
    fields['disc'] = get_disc_dropdown(default=defaults['disc_id'])
    fields['year'] = get_year_dropdown(default=defaults['year'])
    fields['grade'] = get_grade_dropdown(default=defaults['grade'])

    return dict(page=page, per_page=10, evals = result, fields=fields)

def list(prof_id=None, disc_id=None, aluno_id=None, semester=None, year=None, grade=None, with_reply=False):
    '''
    Retorna avaliações de acordo com diversos critérios e filtros
    '''
    pass
