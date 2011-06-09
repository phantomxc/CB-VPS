from webpy.dark import *
from model.users import Employee

from hashlib import md5
import random
#subapps
import apps.zoomerang
import apps.dashboard
import apps.transactions


urls = (
    '/', 'login',
    '/login', 'login',
    '/logout', 'logout',
    '/zoomerang/', apps.zoomerang.app,
    '/dashboard/', apps.dashboard.app,
    '/transactions/', apps.transactions.app
)

    

class index:


    def GET(self):
        return jrender('login.html')



class login:


    def GET(self):
        return jrender('login.html')


    def POST(self):
        i = web.input()
        store = get_store()
        employee = store.find(Employee, 
            Employee.email == i.email,
            Employee._password == unicode(md5(i.password).hexdigest())
        ).one()
        if employee:
            user_login(employee)
            raise web.seeother('/dashboard/')

        else:
            return jrender('login.html')



class logout:


    def GET(self):
        wsession().kill()
        wsession().logged = False
        raise web.seeother('/login')


def session_hook():
    web.ctx['session'] = main_session

    
def random_key():
    s = '.'.join(map(str, [['what the heck are you doing'], [random.getrandbits(32)], [id([])]]))
    return md5(s).hexdigest()


def user_login(user):
    key = random_key()
    web.setcookie('wtf', key, secure=True)
    main_session['wtf'] = key
    main_session['logged'] = True
    main_session['user'] = user.email


app = web.application(urls, globals(), autoreload=False)

_db = get_db()
main_session = web.session.Session(app, web.session.DBStore(_db, 'sessions'))

app.add_processor(web.loadhook(session_hook))
application = app.wsgifunc()



