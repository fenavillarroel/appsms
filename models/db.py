# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################
db = DAL('mysql://root:vmo123@127.0.0.1/smsd', fake_migrate=False)
from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False, migrate=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
estado={1:'Habilidato',0:'Desabilitado'}

db.define_table("canales",      
          Field("numero", "string", length=30, notnull=True, default=None, label='Chip Numero'),
          Field("cantidad", "integer", notnull=True, default=None, label='Numero SMS Disponibles',writable=True),
          Field("credito", "integer", notnull=True, default=0,label='Saldo SIM Card'),
          Field("queue", "string", length=30, notnull=True,label='Puerto GSM'),
          Field("status", "integer", notnull=True, default=0,label='Habilidato / Desabilitado', requires=IS_IN_SET(estado)),migrate=False)

db.canales.status.requires = IS_IN_SET((estado))
          
db.define_table("outgoing",
          Field("customer_id", "string", length=30, notnull=True, default=None, label='Id Cliente',writable=False),
          Field("number", "string", length=30, notnull=True, default=None,label='Numero SMS Destino',writable=False),
          Field("sms_text", "string", length=160, notnull=True, label='Texto Mensaje',writable=False),
          Field("checked", "integer", notnull=False, default=0,label='Verificacion',writable=False),
          Field("created_at", "datetime", notnull=True, default=None, label='Fecha',writable=False),migrate=False)

db.define_table("sms_log",
          Field("type", "string", length=10, notnull=True, default=None, label='Estado SMS',writable=False),
          Field("sent", "string", length=30, notnull=False,label='Fecha SMS',writable=False),
          Field("received", "string", length=30, notnull=False, label='Confirmacion Fecha',writable=False),
          Field("sender", "string", length=30, notnull=True, label='Chip Emisor',writable=False),
          Field("receiver", "string", length=30, notnull=True, label='Chip Receptor',writable=False),
          Field("text", "string", length=255, notnull=True, label='Texto SMS',writable=False),
          Field("status", "string", length=20, notnull=True, label='Estado SMS',writable=False),
          Field("id_outgoing", "integer", notnull=True, label='Id SMS',writable=False),migrate=False)


## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
auth.settings.actions_disabled.append('register')
