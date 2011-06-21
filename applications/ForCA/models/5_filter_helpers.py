def get_prof_dropdown(default=None):
    prof_drop = SQLFORM.factory(
            Field('prof_id', Professores, default=default,
                requires = IS_IN_DB(db, Professores.id, 
                    '%(full_name)s', zero = '')))
    return prof_drop.custom.widget.prof_id

def get_disc_dropdown(default=None):
    disc_drop = SQLFORM.factory(
            Field('disc_id', Disciplinas, default=default,
                requires = IS_IN_DB(db, Disciplinas.id,
                    '%(name)s', zero = '')))
    return disc_drop.custom.widget.disc_id

def get_year_dropdown(default=None):
    year_drop = SQLFORM.widgets.options.widget(Avaliacoes.year, default)
    year_drop.insert(0, '')
    if not default:
        for x in year_drop:
            if '_selected' in x.attributes:
                x.attributes['_selected'] = False
        year_drop[0].attributes['_selected'] = 'selected'
    return year_drop

def get_grade_dropdown(default=None):
    grade_drop = SQLFORM.widgets.options.widget(Avaliacoes.grade, default)
    grade_drop.insert(0, '')
    if not default:
        for x in grade_drop:
            if '_selected' in x.attributes:
                x.attributes['_selected'] = False
        grade_drop[0].attributes['_selected'] = 'selected'
    return grade_drop

def get_filter_query(query):
    '''
    Retorna uma query baseada nos request.vars
    e os defaults como um dict
    '''
    defaults = {
            'prof_id': None,
            'disc_id': None,
            'year'   : None,
            'grade'  : None
            }

    if 'prof_id' in request.vars and request.vars['prof_id']:
        query = query(Avaliacoes.professor_id==request.vars['prof_id'])
        defaults['prof_id'] = request.vars['prof_id']
    if 'disc_id' in request.vars and request.vars['disc_id']:
        query = query(Avaliacoes.disciplina_id==request.vars['disc_id'])
        defaults['disc_id'] = request.vars['disc_id']
    if 'year' in request.vars and request.vars['year']:
        query = query(Avaliacoes.year==request.vars['year'])
        defaults['year'] = request.vars['year']
    if 'grade' in request.vars and request.vars['grade']:
        query = query(Avaliacoes.grade==request.vars['grade'])
        defaults['grade'] = request.vars['grade']

    return query, defaults

