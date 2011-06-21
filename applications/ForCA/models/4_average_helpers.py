def get_positive_percentage(eval_row):
    karmas = map(lambda karma: karma.value, eval_row.karmas.select())
    if len(karmas) == 0:
        return 0.5
    pos_perc = karmas.count(1)/float(len(karmas))
    return pos_perc

def get_eval_quality(eval_row):
    positive = get_positive_percentage(eval_row)
    if positive > 0.75:
        return 3
    elif positive >= 0.5:
        return 2
    else:
        return 1

def get_grade_letter(numgrade):
    if numgrade > 4.5:
        return 'A'
    elif numgrade > 3.5:
        return 'B'
    elif numgrade > 2.5:
        return 'C'
    elif numgrade > 1.5:
        return 'D'
    return 'FF'

def get_grade_value(strgrade):
    grade_dict = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'FF': 1}
    return grade_dict[strgrade]
    
def get_grade_value_graph(strgrade):
    grade_dict = {'A': '5', 'B': '4', 'C': '3', 'D': '2', 'FF': '1'}
    return grade_dict[strgrade]    

def harmonic_mean(listerms):
    numterms = len(listerms)
    return numterms / sum(map(lambda x: 1.0/x, listerms))

def update_grade(prof_id=None, disc_id=None):
    if prof_id:
        prof_evals = db(db.avaliacoes.professor_id==prof_id)
        new_grade = grade_average(prof_evals)
        db(db.professores.id==prof_id).update(grade=new_grade)
        db.commit()
    if disc_id:
        disc_evals = db(Avaliacoes.disciplina_id==disc_id)
        new_grade = grade_average(disc_evals)
        db(Disciplinas.id==disc_id).update(grade=new_grade)
        db.commit()
    return True

def grade_average(evals, with_numeric=False):
    eval_rows = evals.select()
    if len(eval_rows) < 1:
        return None
    numer = sum(map(lambda eval: get_grade_value(eval.grade) * get_eval_quality(eval), eval_rows))
    denom = len(eval_rows) + sum(map(lambda eval: get_eval_quality(eval) - 1, eval_rows))
    avg = numer/float(denom)
    return get_grade_letter(avg)
