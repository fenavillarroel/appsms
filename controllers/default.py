# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    redirect (URL('canales'),client_side=True)

@auth.requires_login()
def canales():

    
    query=(db.canales)
    db.canales.status.represent = lambda id,row: estado[id]
    fields=[db.canales.numero,db.canales.cantidad,db.canales.credito,db.canales.queue,db.canales.status]
        #headers = {'db.pagos.fecha':   'Fecha',
        #   'db.pagos.monto': 'Valor','db.pagos.comments':'Observaciones'}
    orderby=(db.canales.queue)
    links=[lambda row: A(IMG(_src=URL(r=request,c='static',f='images/green_dollar.png'), _width=16, _height=16), 
        _href=URL('update_saldo', args=[row.id,row.queue])),
            lambda row: A(IMG(_src=URL(r=request,c='static',f='images/icon-recarga.png'), _width=16, _height=16), 
        _href=URL('recarga', args=[row.queue]))]
    #links = [lambda row: A('View Post',_href=URL("default","update_saldo",args=[row.id,row.queue]))]
    form = SQLFORM.grid(query=query, fields=fields, orderby=orderby, csv=False, create=True, links=links, 
                         deletable=True , editable=True, details=False,paginate=15,maxtextlength=50, user_signature=False)
    form['_style']='border:1px solid black'

    #customized = myformat(form.rows)
    #form.element('.web2py_table', replace=customized)

    #query=db(db.canales).select(db.canales.ALL, orderby=db.canales.queue)
    #print query
    #orm=SQLFORM.grid(query=query)

    return dict(form=form)

@auth.requires_login()
def update_saldo():

    r=request.args[0]
    q=request.args[1]

    #cl=db(db.auth_user.id == recors).select(db.auth_user.saldo,db.auth_user.first_name,db.auth_user.last_name)[0]

    form = SQLFORM.factory(Field('monto','integer', label="Monto",requires=IS_INT_IN_RANGE(1000,100000),default=(1600)),formstyle='bootstrap')


    submit = form.element(_type="submit")
    submit["_onclick"] = "return confirm('Confirma Recarga Saldo');"
    form['_style']='border:1px solid black'

    #submit["_onclick"] = "return confirm('Confirma o Cancela Datos Cliente');"
    if form.accepts(request.vars,session):

                db(db.canales.id==r).update(credito=db.canales.credito+int(form.vars.monto))
                db.commit()
                #cadena='/usr/local/bin/send_my_sms %s 103 250SMS' % (q,)
                #os.system(cadena)
                session.flash = T('Recarga Exitosa!!!')
                redirect(URL('canales'))

    return dict(form=form)




@auth.requires_login()
def recarga():

    r=request.args[0]
    #q=request.args[1]

    #cl=db(db.auth_user.id == recors).select(db.auth_user.saldo,db.auth_user.first_name,db.auth_user.last_name)[0]

    form = SQLFORM.factory(Field('monto','integer', default=1600, label="Recarga Bolsa 80 SMS"),formstyle='bootstrap')


    submit = form.element(_type="submit")
    submit["_onclick"] = "return confirm('Confirma Recarga');"
    form['_style']='border:1px solid black'

    #submit["_onclick"] = "return confirm('Confirma o Cancela Datos Cliente');"
    if form.accepts(request.vars,session):

                #db(db.canales.id==r).update(credito=db.canales.credito+int(form.vars.monto))
                #db.commit()
                try:
                    cadena="echo vmo123 | sudo -S /usr/local/bin/send_my_sms %s 103 80SMS" % (q,)
                    #cadena='echo vmo123 | sudo -S /usr/local/bin/send_my_sms %s 103 80SMS' % (q,)
                    os.system(cadena)
                    session.flash = T('Recarga Exitosa!!!')
                    redirect(URL('canales'))
                except:
                    session.flash = T('Fallo APP Recarga !!!!!!!!!!')
                    redirect(URL('canales'))

    return dict(form=form)

@auth.requires_login()
def recibidos():

    query=(db.sms_log.type=='RECEIVED')
    fields=[db.sms_log.id,db.sms_log.type,db.sms_log.sent,db.sms_log.received,db.sms_log.sender,db.sms_log.receiver,db.sms_log.text]
    orderby=(~db.sms_log.id)
    form = SQLFORM.grid(query=query, fields=fields, orderby=orderby,
                        create=False, deletable=False, editable=False,details=False,paginate=15,maxtextlength=50,)

    return dict(form=form)





@auth.requires_login()
def log():

    query=(db.sms_log)

    fields=[db.sms_log.type,db.sms_log.sent,db.sms_log.received,db.sms_log.sender,db.sms_log.receiver,db.sms_log.text,db.sms_log.status,db.sms_log.id_outgoing]
    orderby=(~db.sms_log.sent)
    #links=[lambda row: A(IMG(_src=URL(r=request,c='static',f='images/Edit_Icon.png'), _width=16, _height=16), _href=URL('edit_device', args=row.id)),lambda row: A(IMG(_src=URL(r=request,c='static',f='images/followme.png'), _width=24, _height=24), _href=URL('add_follow', args=row.id))]
    #links = [lambda row: A('View Post',_href=URL("default","update_saldo",args=[row.id,row.queue]))]
    form = SQLFORM.grid(query=query, fields=fields, orderby=orderby, csv=True, create=False, formstyle='bootstrap',
                         deletable=False , editable=False, details=False,paginate=50,maxtextlength=50, user_signature=False)
        #form['_style']='border:1px solid black'
    #customized = myformat(form.rows)
    #form.element('.web2py_table', replace=customized)


    return dict(form=form)

@auth.requires_login()
def outgoing():

    query=(db.outgoing)

    fields=[db.outgoing.customer_id,db.outgoing.number,db.outgoing.sms_text,db.outgoing.checked,db.outgoing.created_at]
    orderby=(~db.outgoing.created_at)
    #links=[lambda row: A(IMG(_src=URL(r=request,c='static',f='images/Edit_Icon.png'), _width=16, _height=16), _href=URL('edit_device', args=row.id)),lambda row: A(IMG(_src=URL(r=request,c='static',f='images/followme.png'), _width=24, _height=24), _href=URL('add_follow', args=row.id))]
    #links = [lambda row: A('View Post',_href=URL("default","update_saldo",args=[row.id,row.queue]))]
    form = SQLFORM.grid(query=query, fields=fields, orderby=orderby, csv=True, create=False, formstyle='table3cols',
                         deletable=False , editable=False, details=False,paginate=100,maxtextlength=50, user_signature=False)
        #form['_style']='border:1px solid black'


    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def myformat(rows):
    #import gluon
    #nuevo = gluon.dal.Rows()

    new = TABLE()

    for i in rows:
        if i.received:

            row = TR(TD(i.sent ), TD(i.type),TD(i.received),TD(i.sender),TD(i.receiver),TD(i.text),TD(i.status),TD(i.id_outgoing), _class='green')
        #elif i.account.startswith('B'):
        #    row = TR(TD(i.account), TD(i.concept), _class='orange')
        else:
            row = TR(TD(i.sent), TD(i.type),TD(i.received),TD(i.sender),TD(i.receiver),TD(i.text),TD(i.status),TD(i.id_outgoing), _class='red')
        new.append(row)
    return new



@auth.requires_login()
def dispositivos():

        import os,re
        #Variable para la ruta al directorio
        path = '/dev/'
        #Lista vacia para incluir los ficheros
        lstFiles = []
        #Lista con todos los ficheros del directorio:
        lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
        #Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
        codigos = ['BUS1-HUB1-PORT1','BUS1-HUB1-PORT2','BUS1-HUB1-PORT3','BUS1-HUB1-PORT4','BUS1-HUB1-PORT5','BUS1-HUB1-PORT6','BUS1-HUB1-PORT7']
        for root, dirs, files in lstDir:
            for fichero in files:
                (nombreFichero, extension) = os.path.splitext(fichero)
                for elemento in codigos:
                    #if re.match(nombreFichero, 'BUS1-HUB1-PORT.'):
                    if re.match(nombreFichero, elemento):
                        lstFiles.append(nombreFichero)#+extension)
        lstFiles.sort()
        #return dict(files=TABLE(*[TR(TD(f)) for f in lstFiles]),total=len(lstFiles))
        return dict(files=lstFiles,total=len(lstFiles))

@auth.requires_login()
def colas():

        import os

        queue= db().select(db.canales.queue, orderby=db.canales.queue)
        colas=[]
        for i in queue:


                try:
                    files=os.listdir('/var/spool/sms/%s/' % i.queue)
                    colas.append(files)
                except:
                    files=[]
                    colas.append(files)



        return dict(queue=queue,colas=colas)


@auth.requires_login()
def reload():

    p=None
    form = SQLFORM.factory(Field('Reload',default='Reload SMS Tools',writable=False))
    submit = form.element('input',_type='submit')
    #submit['_style'] = 'display:none;'
    #submit["_onclick"] = "return confirm('Confirma Recarga Saldo');"
    #form['_style']='border:1px solid black'

    #submit["_onclick"] = "return confirm('Confirma Reload SMS Tools');"
    if form.accepts(request.vars,session):
        import os
        #import subprocess
        #p = subprocess.Popen('/usr/bin/sudo -S /etc/init.d/sms3 restart', shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = p.communicate(input='vmo123')
                         #    print "\n".join("out: " + x for x in out.split('\n'))
                         #    print "\n".join("err: " + x for x in err.split('\n'))

        #p=os.popen("/usr/bin/sudo -S /etc/init.d/sms3 restart", 'w').write("vmo123\n")
        p=os.system("echo -e '%s'|/usr/bin/sudo -S %s" % ('vmo123\n', '/etc/init.d/sms3 restart'))
        if not p:
            response.flash = T('Reload SMS Tools Exitoso!!!')
        #p=os.system('echo -e vmo123 | sudo -u fvillarroel -S /etc/init.d/sms3 stop')
    return dict(form=form,p=p)

@request.restful()
def api():
    response.view = 'generic.json'

    def GET(tablename, id):
        if not tablename == 'person':
            raise HTTP(400)
        return dict(person = db.person(id))

    def POST(*args, **vars):

        bin_sendsms="/usr/local/bin/new_sendsms %s -A idsms:%s '%s'"
        text = request.vars.text
        number = request.vars.number
        username = request.vars.username
        password = request.vars.password
        id_sms = request.vars.id
        if username != 'fenvillarroel' or password !='abc123jU':
            #app.logger.debug('login error send')
            return True

        canal = db.executesql('select * canales where status = 1 and cantidad > 0 order by random() limit 1',as_dict=True)

        if not canal:
            raise HTTP(500)

        #db.executesql('update canales set cantidad=cantidad -1 where id=%s' % (canal.id,))
        #db.commit()

        #channel=canal.queue
        cmd = "%s %s  \"%s\"" %  (bin_sendsms, number, text)
        execute = os.popen(cmd).read()
        #app.logger.debug(execute)
        #sms_id = execute.split('\n')[0]

        #if not tablename == 'person':
        #    raise HTTP(400)
        #return number.json

    return locals() 

