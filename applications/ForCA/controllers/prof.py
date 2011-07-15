from operator import itemgetter

@auth.requires_membership('Admin')
def create():
    form = SQLFORM(db.professores)
    if form.accepts(request.vars, session):
        session.flash = 'Professor criado com sucesso'
    return dict(form=form)

@auth.requires_membership('Admin')
def edit():
    prof_id = request.vars['prof_id']
    prof = db(db.professores.id==prof_id).select().first()
    form = SQLFORM(db.professores, prof)
    if form.accepts(request.vars, session):
        session.flash = 'Professor atualizado com sucesso'
        redirect(URL(request.application, 'prof', 'list'))
    return dict(form=form)

@auth.requires_membership('Admin')
def delete():
    prof_id = request.vars['prof_id']
    if request.wsgi.environ['REQUEST_METHOD'] == 'GET':
        session.jump_back = request.env.http_referer
    prof_evals = get_evals(prof_id,None).select()
    for eval in prof_evals:
        db(Avaliacoes.id==eval.id).delete()
    db(Professores.id==prof_id).delete()
    db.commit()
    session.flash = T('Professor excluído com sucesso')
    redirect(session.jump_back)

def list():
    '''
    Exibe a lista de professores
    '''
    return dict(profs=db().select(db.professores.ALL).sort(lambda profs: rem_acentos(profs.full_name)))

def home():
    '''
    Lista avaliações recebidas pelo professor
    '''
    prof_id = request.vars['prof_id']

    if len(request.args) and 'submit' not in request.vars:
        page = int(request.args[0])
    else:
        page = 0
    limitby = (page*10, (page+1)*11)
    prof = db(db.professores.id==prof_id).select(db.professores.ALL).first()

    #escapa se perfil do professor esta bloqueado - PALAZZO QUERIDO!

    #result_query, defaults = get_filter_query(db(Avaliacoes.professor_id == prof_id))

    #fields = {}

    #fields['disc'] = get_disc_dropdown(default=defaults['disc_id'])
    #fields['year'] = get_year_dropdown(default=defaults['year'])
    #fields['grade'] = get_grade_dropdown(default=defaults['grade'])

    #Lista de avaliações
    prof_evals = get_evals(prof_id,None)
    evals_stats = {}
    evals_stats['len'] = prof_evals.count()
    #prof_evals = result_query
    raw_evals = prof_evals.select()
    raw_evals = raw_evals.sort(lambda row: row.timestamp_eval, reverse=True)
    raw_evals = raw_evals.sort(lambda row: row.karma, reverse=True)
    evals = refine_evals(raw_evals[limitby[0]:limitby[1]])    
    #Lista de disciplinas lecionadas pelo professor
    raw_discs = db(db.profs_discs.professor_id==prof_id).select()
    discs = []
    for raw_disc in raw_discs:
        disc = {}
        disc['id']        = raw_disc['disciplina_id']
        disc['name']      = db(db.disciplinas.id==raw_disc['disciplina_id']).select().first().name
        evals_prof_disc   = get_evals(prof_id,raw_disc['disciplina_id'])
        #Se não tem avaliação, a nota média recebe '\' pra colocar as disciplinas sem nota no fim, ao ordenar
        #Se alguém souber um jeito sem gambiarra seria interessante, favor me contar depois (Thomas)
        if len(evals_prof_disc.select()) < 1:
            disc['grade'] = '\\'
        else:
            disc['grade'] = grade_average(evals_prof_disc) 
        discs.append(disc)
   
    return dict(prof=prof, page=page, per_page=10, prof_evals=prof_evals, evals_stats=evals_stats, \
            evals = evals, blocked = prof.blocked,\
            discs=sorted(sorted(discs, key=lambda x: rem_acentos(x['name'])), key=lambda x: x['grade'], reverse=False))
            #fields=fields)

@auth.requires_membership('Professor')
def block():
    """
    Funcao para bloqueio do perfil de um professor
    """
    prof_id = request.vars['prof_id']
    Professores[prof_id] = dict(blocked = True)
    db.commit()
    session.flash = 'Seu perfil foi bloqueado com sucesso.'
    redirect(URL('default', 'index'))

@auth.requires_membership('Professor')
def unblock():
    """
    Funcao para desbloqueio do perfil de um professor
    """
    prof_id = request.vars['prof_id']
    Professores[prof_id] = dict(blocked = False)
    db.commit()
    session.flash = 'Seu perfil foi desbloqueado com sucesso!'
    redirect(URL('default', 'index'))

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
