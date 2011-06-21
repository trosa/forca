# -*- coding: utf-8 -*- 

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('Fórum Colaborativo de Avaliação')
response.meta.author = '@trsilva'
response.meta.description = 'Fórum Colaborativo de Avaliação Docente'
response.meta.keywords = 'forum colaborativo avaliação docente'

##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
        (T('Início'),      False, URL(request.application,'default','index'),   []),
        (T('Professores'), False, URL(request.application,'prof','list'),       []),
        (T('Disciplinas'), False, URL(request.application,'disc','list'),       []),
        (T('Pesquisar'),   False, URL(request.application,'eval','filter'),     []),
        (T('FAQ'),         False, URL(request.application,'default','faq'),     [])
    ]

if auth.has_membership('Admin'):
    response.menu += [(T('Admin'), False, URL(request.application, 'admin', 'index'), [])]
