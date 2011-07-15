def prof_create(data):
    '''
    Adiciona o user_id ao campo da tabela 'professores'
    '''
    db(db.professores.email==data.email).update(
        user_id    = data.id
    )
    db.commit()

def aluno_create(data):
    '''
    Insere um registro na tabela 'alunos'
    '''
    db.alunos.insert(
        email      = data.email,
        full_name  = data.first_name,
        short_name = data.last_name,
        user_id    = data.id
    )
    db.commit()
    
#########################################
#              Charts                   #
#########################################
 
def generate_basic_graph(type,widht, height, min, max, values):
    '''
    Gera um gráfico simples com os parâmetros passados, sendo que values é um array de triplas contendo value, label e color.
    '''
    graph = 'http://chart.apis.google.com/chart?chxt=y' #Código padrão para montar gráfico de barras
    graph += '&cht='+type
    graph += '&chs='+str(widht)+'x'+str(height) #Tamanho do gráfico
    graph += '&chds='+str(min)+','+str(max) #Min e Max dos dados
    graph += '&chxr=0,'+str(min)+','+str(max) #Min e Max do eixo Y
    graph += '&chd=t:' #Valores
    for value in values:
        graph += str(value['value'])+','
    graph = graph[:len(graph)-1]
    graph += '&chl=' #Labels, eixo X
    for value in values:
        graph += value['label']+'|'
    graph = graph[:len(graph)-1]
    graph += '&chco=' #Cores
    for value in values:
        graph += value['color']+'|'    
    graph = graph[:len(graph)-1]
    return graph
    
def graph_grades(evals):
    '''
    Gera um gráfico de barras de acordo com as notas das avaliacoes
    '''    
    colors = {'A':'A6EFA5', 'B':'D2EFA5', 'C':'EFEFA5', 'D':'EFC4A5', 'FF':'EFA5A5'}
    values = []
    max_len_grade = 0
    for grade in ['A', 'B', 'C', 'D', 'FF']:
        entry = {}
        grade_count = evals(Avaliacoes.grade==grade).count()
        entry['label'] = grade
        entry['value'] = grade_count
        entry['color'] = colors[grade]
        values.append(entry)
        if grade_count > max_len_grade:
            max_len_grade = grade_count
    return generate_basic_graph('bvs',175, 150, 0, max_len_grade, values) 
    
def graph_karmas(evals_info):
    '''
    Gera um gráfico pizza de acordo com os karmas do array de evals_info
    '''    
    values = []
    value = {}
    value['label'] = ('Positivas' if evals_info['karma_up'] > 0 else '')
    value['value'] = evals_info['karma_up']
    value['color'] = '219A21'
    values.append(value)
    value = {}
    value['label'] = ('Negativas' if evals_info['karma_down'] > 0 else '')
    value['value'] = evals_info['karma_down']
    value['color'] = 'FF0000'
    values.append(value)
    return generate_basic_graph('p3',300, 125, 0, evals_info['karma_len'], values)
    
def graph_evolution_evals(eval_rows):
    '''
    Gera um gráfico de linha com a evolução das notas ao longo dos semestres
    '''
    raw_evals = eval_rows.select(Avaliacoes.year)
    raw_evals = set(map(lambda eval: eval['year'], raw_evals))
    years = []
    for year in raw_evals:
        years.append(year)
    years.sort()
    evals = []
    #Intera os resultados por ano
    for year in years:
        for x in [1,2]:#Cria uma entrada pra cada semestre do ano 
            evals_semester = eval_rows((db.avaliacoes.year==year)&(db.avaliacoes.semester==x))
            result = evals_semester.select().first()
            if result: 
                eval = {}
                eval['year']     = year
                eval['semester'] = x    
                eval['grade'] = grade_average(evals_semester)
                evals.append(eval)        
    if len(evals)>1:        
         #Gera código do gráfico
        graph = 'http://chart.apis.google.com/chart?chf=c,lg,90,EFA5A5,0,A6EFA5,1\
&chxs=0,00000099,12.5,0,l,00000099|1,676767,11.5,0,lt,676767&chxt=y,x&cht=lxy&chco=00000099&chds=1,5,1,5.1\
&chdl=M%E9dia&chdlp=b&chls=5&chm=o,00000099,0,-1,5&chxl=0:|FF|D|C|B|A|1:|'
        for eval in evals:
             graph += str(eval['year'])[-2:]+'%2F'+str(eval['semester'])+'|'
        graph = graph[:len(graph)-1]
        graph += '&chd=t:-1|'
        for eval in evals:
            graph += get_grade_value_graph(eval['grade'])+','
        graph = graph[:len(graph)-1]
        graph += '&chxp=0,1.2,2,3,4,5|1,'
        for x in range(1,len(evals)):
            graph += str(x)+','
        graph = graph[:len(graph)-1]     
        graph += '&chxr=0,1,5|1,1,'+str(len(evals))
        graph += '&chg='+str(100/(len(evals)-1))+',0,0,0'
        graph += '&chs='+str(50*len(evals))+'x150'
        return graph
    else:
        return ''
        
        
#########################################
#              Aluno getters            #
#########################################

def get_aluno_id():
    '''
    Retorna o aluno_id do usuario logado
    '''
    try:
        user_id = session.auth.user.id
        aluno_id = db(db.alunos.user_id == user_id).select().first().id
        return aluno_id
    except:
        return 0

def get_aluno_user_id(aluno_id):
    '''
    Retorna o user_id do aluno referenciado por aluno_id
    '''
    aluno = db(Alunos.id==aluno_id).select().first()
    return aluno.user_id

def get_aluno_full_name(aluno_id):
    '''
    Retorna o nome completo do aluno referenciado por aluno_id
    '''
    aluno = db(db.alunos.id==aluno_id).select().first()
    return aluno.full_name

def get_posted_evals(aluno_id):
    '''
    Retorna todas as avaliacoes postadas por um aluno
    '''
    aluno_evals = db(db.avaliacoes.aluno_id==aluno_id).select()
    return aluno_evals

def get_karma_avg(aluno_id):
    '''
    Retorna a soma de karmas recebidos pelas avaliacoes
    postadas pelo aluno referenciado por aluno_id
    '''
    aluno_evals = get_posted_evals(aluno_id)
    karmas = []
    for eval in aluno_evals:
        eval_karmas = db(Karmas.avaliacao_id==eval.id).select()
        for karma in eval_karmas:
            karmas.append(karma.value)
    return sum(karmas)

def get_link_to_aluno_home(aluno_id, name=None):
    '''
    Retorna um link para o profile/home do aluno referenciado por aluno_id
    '''
    if not name:
        name = db(Alunos.id==aluno_id).select().first().full_name
    return A(name, _href=URL(request.application, 'profile', 'home', vars=dict(aluno_id=aluno_id)))

#########################################
#              Prof getters             #
#########################################

def get_prof_id():
    '''
    Retorna o professor_id do usuario logado
    '''
    try:
        user_id = session.auth.user.id
        prof_id = db(db.professores.user_id == user_id).select().first().id
        return prof_id
    except:
        return 0

def get_prof_name(prof_id):
    '''
    Retorna o nome completo do professor referenciado por prof_id
    '''
    prof = db(db.professores.id==prof_id).select().first()
    return prof.full_name

def get_prof_id_from_email(prof_email):
    '''
    Retorna o id no datastore do professor cujo e-mail eh prof_email
    '''
    prof = db(db.professores.email==prof_email).select().first()
    return prof.id

def is_prof_registered(prof_id):
    '''
    Retorna True se o professor esta registrado no sistema
    '''
    prof = db(Professores.id==prof_id).select().first()
    if prof.user_id:
        return True
    else:
        return False

#########################################
#              Disc getters             #
#########################################

def get_disc_name(disc_id):
    '''
    Retorna o nome da disciplina referenciada por disc_id
    '''
    disc = db(db.disciplinas.id==disc_id).select().first()
    return disc.name

def get_disc_id_from_code(disc_code):
    '''
    Retorna o id no datastore da disciplina cujo codigo eh disc_code
    '''
    disc = db(db.disciplinas.code==disc_code).select().first()
    return disc.id

def get_link_to_disc_home(disc_id, name=None):
    if not name:
        name = db(Disciplinas.id==disc_id).select().first().name
    return A(name, _href=URL(request.application, 'disc', 'home', vars=dict(disc_id=disc_id)))

#########################################
#              Eval getters             #
#########################################

def get_evals(prof_id = None, disc_id = None):
    '''
    Exibe a lista de avalições (já faz o join com tabela de professores, alunos e disciplinas).
    '''
    if((prof_id != None)&(disc_id != None)):
        evals = db((db.avaliacoes.professor_id == prof_id)&(db.avaliacoes.disciplina_id == disc_id))
    elif(prof_id != None):
        evals = db(db.avaliacoes.professor_id == prof_id)
    elif(disc_id != None):
        evals = db(db.avaliacoes.disciplina_id == disc_id)
    else:
        evals = db(db.avaliacoes.aluno_id == get_aluno_id())
    return evals

def refine_evals(raw_evals):
    '''
    Retorna uma lista de avaliações com campos refinados - referências resolvidas, campos tratados, etc
    '''
    evals = []
    for raw_eval in raw_evals:
        prof  = db(Professores.id==raw_eval['professor_id']).select().first()
        aluno = db(Alunos.id==raw_eval['aluno_id']).select().first()
        disc  = db(Disciplinas.id==raw_eval['disciplina_id']).select().first()
        eval = {}
        eval['id']               = raw_eval['id']
        eval['prof_id']          = raw_eval['professor_id']
        eval['prof_user_id']     = prof.user_id
        eval['prof_blocked']     = prof.blocked
        eval['disc_id']          = raw_eval['disciplina_id']
        eval['aluno_user_id']    = aluno.user_id
        eval['aluno_id']         = raw_eval['aluno_id']
        eval['aluno_name']       = aluno.full_name
        eval['aluno_short_name'] = aluno.short_name
        eval['prof_name']        = prof.full_name
        eval['prof_short_name']  = prof.short_name
        eval['disc_name']        = disc.name
        eval['disc_short_name']  = disc.short_name
        eval['semester']         = str(raw_eval['year'])+'/'+str(raw_eval['semester'])
        eval['grade']            = raw_eval['grade']
        eval['karma']            = raw_eval['karma']
        eval['karma_up']         = db((Karmas.avaliacao_id==raw_eval['id']) & (Karmas.value==1)).count()
        eval['karma_down']       = db((Karmas.avaliacao_id==raw_eval['id']) & (Karmas.value==-1)).count()
        eval['comment']          = raw_eval['comment']
        eval['reply']            = raw_eval['reply']
        eval['anonimo']          = raw_eval['anonimo']
        eval['timestamp_eval']   = raw_eval['timestamp_eval']
        eval['timestamp_reply']  = raw_eval['timestamp_reply']
        evals.append(eval)
    return evals

def get_refined_evals(prof_id=None, disc_id=None):
    '''
    Seleciona as avaliações dados um prof_id ou disc_id e as refina, devolvendo avaliações tratadas
    '''
    raw_evals = get_evals(prof_id, disc_id).select()
    evals = refine_evals(raw_evals)
    return evals
    

def get_karmas(evals):
    '''
    Retorna informacoes de karma das avaliacoes como um dict
    (karma_len, karma_up, karma_down, karma_avg)
    '''
    karmas = []
    for eval in evals.select():
        eval_karmas = db(Karmas.avaliacao_id==eval.id).select()
        for karma in eval_karmas:
            karmas.append(karma.value)
    karma_dict = {}
    karma_dict['len']  = len(karmas)
    karma_dict['up']   = len(filter(lambda karma: karma > 0, karmas))
    karma_dict['down'] = len(filter(lambda karma: karma < 0, karmas))
    karma_dict['avg']  = sum(karmas)
    return karma_dict
    
def get_evals_info(evals):
    '''
    Retorna um dic com informações úteis para as avaliações passadas como parâmetro
    '''
    evals_info = {}
    evals_info['len'] = evals.count()
    evals_info['grade_avg'] = grade_average(evals)
    evals_info['A'] = evals(db.avaliacoes.grade == 'A').count()
    evals_info['B'] = evals(db.avaliacoes.grade == 'B').count()
    evals_info['C'] = evals(db.avaliacoes.grade == 'C').count()
    evals_info['D'] = evals(db.avaliacoes.grade == 'D').count()
    evals_info['FF'] = evals(db.avaliacoes.grade == 'FF').count()
    evals_info['max_len_grade'] = max(evals_info['A'],evals_info['B'],evals_info['C'],evals_info['D'],evals_info['FF'])
    
    karmas = get_karmas(evals)
    evals_info['karma_len'] = karmas['len']
    evals_info['karma_up'] = karmas['up']
    evals_info['karma_down'] = karmas['down']
    evals_info['karma_avg'] = karmas['avg']

    return evals_info


#########################################
#           Funções auxiliares          #
#########################################

def rem_acentos(str):
    '''
    Remove acentuação de uma string. Exemplo Não faça -> Nao faca
    '''
    from unicodedata import normalize
    return normalize('NFKD', str.decode('utf-8')).encode('ASCII', 'ignore')
    
    
def update_timestamp_eval(eval_id):
    Avaliacoes[eval_id] = dict(timestamp_eval=datetime.now())
    db.commit()

def update_timestamp_reply(eval_id):
    #db(db.avaliacoes.id==eval_id).update(timestamp_reply=datetime.now())
    Avaliacoes[eval_id] = dict(timestamp_reply=datetime.now())
    db.commit()

def check_unique_eval(form):
    aluno_id      = form.vars['aluno_id']
    professor_id  = form.vars['professor_id']
    disciplina_id = form.vars['disciplina_id']
    check = db(
        (db.avaliacoes.aluno_id      == aluno_id     ) &
        (db.avaliacoes.professor_id  == professor_id ) &
        (db.avaliacoes.disciplina_id == disciplina_id))
    if check.count():
        form.errors.disciplina_id = 'Você já postou uma avaliação para este\
        professor nesta disciplina'
    return check.count() == 0

def has_karmed(aluno_id, eval_id):
    return db(
        (db.karmas.aluno_id==aluno_id) &
        (db.karmas.avaliacao_id==eval_id)
    ).count()


def update_profs_discs(prof_id, disc_id):
    prof_disc = db((db.profs_discs.professor_id==prof_id)&(db.profs_discs.disciplina_id==disc_id)).select().first()
    if not prof_disc:
        db.profs_discs.insert(professor_id=prof_id, disciplina_id=disc_id)
        return 0
    count = prof_disc.count
    db(db.profs_discs.id==prof_disc.id).update(count = count+1)
    db.commit()
    return count + 1

#########################################
#           favorites                   #
#########################################

def get_favorite_evals(user_id):
    '''
    Retorna uma lista refinada de avaliacoes favoritas de um usuario referenciado por user_id
    '''
    favorite_rows = db(Favoritos.user_id==user_id).select()
    raw_evals = []
    for row in favorite_rows:
        raw_evals.append(db(Avaliacoes.id==row.avaliacao_id).select().first())
    return refine_evals(raw_evals)

    
def favorita_eval(eval_id):
    '''
    Favorita ou desfavorita uma determinada avaliação para o usuário logado, dependendo do atual estado
    '''
    favorito = db((db.favoritos.avaliacao_id==eval_id)&(db.favoritos.user_id==session.auth.user.id)).select().first()
    if not favorito:
        db.favoritos.insert(
            user_id      = session.auth.user.id,
            avaliacao_id = eval_id
        )
    else:
        db(db.favoritos.id==favorito.id).delete()    
    db.commit()
    
def eh_favorita(eval_id):
    '''
    Verifica se determinada avaliação é favorita para o usuário logado
    '''
    favorito = db((db.favoritos.avaliacao_id==eval_id)&(db.favoritos.user_id==session.auth.user.id)).select().first()
    if not favorito:
        return False
    else:
        return True


#########################################
# Biased dropdowns: the pretty way      #
#########################################

def disc_biased_dropdown(prof_id):
    rows = db().select(db.disciplinas.id, db.disciplinas.name,
            left = db.profs_discs.on(
                (db.disciplinas.id==db.profs_discs.disciplina_id)&
                (db.profs_discs.professor_id==prof_id)),
            orderby=db.profs_discs.professor_id|db.disciplinas.name)
    key = [row.id for row in rows]
    value = [row.name for row in rows]
    form = SQLFORM.factory(
            Field('disciplina_id', label="Disciplina", requires=IS_IN_SET(key,value,zero=None)))
    return form[0][0]

def prof_biased_dropdown(disc_id):
    rows = db().select(db.professores.id, db.professores.full_name,
            left = db.profs_discs.on(
                (db.professores.id==db.profs_discs.professor_id)&
                (db.profs_discs.disciplina_id==disc_id)),
            orderby=db.profs_discs.disciplina_id|db.professores.full_name)
    key = [row.id for row in rows]
    value = [row.full_name for row in rows]
    form = SQLFORM.factory(
            Field('professor_id', label="Professor", requires=IS_IN_SET(key,value,zero=None)))
    return form[0][0]

#########################################
# Biased dropdowns: the GAE way         #
#########################################

def gae_disc_biased_dropdown(prof_id):
    discs = db(db.disciplinas.id>0).select(db.disciplinas.ALL)
    profs_discs = db(db.profs_discs.id>0).select(db.profs_discs.ALL).as_list()
    pds = map(lambda x: {'professor_id': x['professor_id'], 'disciplina_id': x['disciplina_id']}, profs_discs)
    results = []
    for disc in discs:
        dictkey = {'professor_id': int(prof_id), 'disciplina_id': disc.id}
        if dictkey in pds:
            results.append([disc.id, disc.name, profs_discs[pds.index(dictkey)]['count']])
        else:
            results.append([disc.id, disc.name, 0])
    key = [res[0] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    value = [res[1] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    form = SQLFORM.factory(
            Field('disciplina_id', label="Disciplina", requires=IS_IN_SET(key, value, zero=None)))
    return form[0][0]

def gae_prof_biased_dropdown(disc_id):
    profs = db(db.professores.id>0).select(db.professores.ALL)
    profs_discs = db(db.profs_discs.id>0).select(db.profs_discs.ALL).as_list()
    pds = map(lambda x: {'professor_id': x['professor_id'], 'disciplina_id': x['disciplina_id']}, profs_discs)
    results = []
    for prof in profs:
        if prof.blocked: continue
        dictkey = {'disciplina_id': int(disc_id), 'professor_id': prof.id}
        if dictkey in pds:
            results.append([prof.id, prof.full_name, profs_discs[pds.index(dictkey)]['count']])
        else:
            results.append([prof.id, prof.full_name, 0])
    key = [res[0] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    value = [res[1] for res in sorted(sorted(results, key=lambda x: rem_acentos(x[1])), key=lambda x: x[2], reverse=True)]
    form = SQLFORM.factory(
            Field('professor_id', label="Professor", requires=IS_IN_SET(key, value, zero=None)))
    return form[0][0]
