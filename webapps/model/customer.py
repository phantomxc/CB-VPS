from webpy.dark import *
from hashlib import md5

class User(web.Storage):
    
    def __init__(self, dbrow=None):
        if dbrow:
            self.update(dbrow)

    @classmethod
    def create(cls, **kwargs):
        db = get_db()
        kwargs['password'] = md5(kwargs['password']).hexdigest()
        res = db.insert('users', **kwargs)
        
        if res:
            return cls.fetch(kwargs['email'])
    
    @classmethod
    def fetch(cls, email):
        db = get_db()
        row = db.select('users', where="email=$email", vars={'email':email})
        
        if not row:
            return None
        f = User(dbrow=row[0])
        return f

    
