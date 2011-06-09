import web
from webpy.dark import *

session.params = {
    'cookie_name':'pacportal',
    'cookie_domain':None,
    'ignore_change_ip': False,
    'timeout':14400,
    'secret_key':'asdfghjklCantguessthisqwertyui1!34%'
}

session.init = {
    'data': None,
    'etk': None,
    'ctk': None,
    'user': None,
    'employee': None,
}

_db = get_db()
session.store = web.session.DBStore(_db, 'webpy_sessions')
