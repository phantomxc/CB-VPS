import web

#session.params = {
#    'cookie_name':'pacportal',
#    'cookie_domain':None,
#    'ignore_change_ip': False,
#    'timeout':14400,
#    'secret_key':'asdfghjklCantguessthisqwertyui1!34%'
#}

#session.init = {
#    'data': None,
#    'etk': None,
#    'wtf': None,
#    'user': None,
#    'employee': None,
#}

#_db = get_db()
#session.store = web.session.DBStore(_db, 'sessions')

def get_session():
    return web.ctx.session
