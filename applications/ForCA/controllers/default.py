# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    """
    """
    if auth.is_logged_in():
        redirect(URL('profile','home'))
    else:
        redirect(URL('default','home'))
    return dict()

def home():
    return dict()

def faq():
    len_users = db(Alunos.id>0).count()+db(Professores.user_id>0).count()
    len_evals = db(Avaliacoes.id>0).count()
    len_karmas= db(Karmas.id>0).count()
    return dict(len_users=len_users, len_evals=len_evals, len_karmas=len_karmas)

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
            @auth.requires_membership('group name')
            @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    forca_auth.email.writable = (request.args(0)!='profile')
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


