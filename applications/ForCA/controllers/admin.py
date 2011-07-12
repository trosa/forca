@auth.requires_membership('Admin')
def index():
    events = auth.db(auth.db.auth_event.id>0).select(orderby=~auth.db.auth_event.time_stamp)
    users = []
    for event in events:
        if event.description[-10:] == 'Registered':
            desc = event.description
            uid = desc.split()[1]
            user = auth.db(auth.db.auth_user.id==uid).select().first()
            if user:
                if not user.registration_key:
                    users.append({'email': user.email, 'name': user.first_name})

    evals = db(Avaliacoes.id>0).select().as_list()
    num_evals = len(evals)

    evals_stats = {}

    max_num = 0
    for grade in ['A', 'B', 'C', 'D', 'FF']:
        grade_evals = filter(lambda eval: eval['grade'] == grade, evals)
        num_grade = len(grade_evals)
        if num_grade > max_num:
            max_num = num_grade
        pct_grade = (num_grade/float(num_evals)) * 100
        evals_stats[grade] = {'num': num_grade, 'pct': pct_grade}
    
    chart_url='''http://chart.apis.google.com/chart?chs=400x325&cht=p\
&chco=A6EFA5|D2EFA5|EFEFA5|EFC4A5|EFA5A5\
&chd=t:%d,%d,%d,%d,%d\
&chds=0,%d
&chdl=A|B|C|D|FF\
&chma=50,50,50,50\
&chl=%d+(%d%%)|%d+(%d%%)|%d+(%d%%)|%d+(%d%%)|%d+(%d%%)\
&chtt=Distribuição+de+conceitos+de+avaliações''' % (evals_stats['A']['num'], evals_stats['B']['num'],\
                                                    evals_stats['C']['num'], evals_stats['D']['num'],\
                                                    evals_stats['FF']['num'], max_num,\
                                                    evals_stats['A']['num'], evals_stats['A']['pct'],\
                                                    evals_stats['B']['num'], evals_stats['B']['pct'],\
                                                    evals_stats['C']['num'], evals_stats['C']['pct'],\
                                                    evals_stats['D']['num'], evals_stats['D']['pct'],\
                                                    evals_stats['FF']['num'], evals_stats['FF']['pct'])

    return dict(users=users[:10], chart_url=chart_url)
