from storm.locals import *
from webpy.dark import *
from hashlib import md5

class Client(Storm):
    __storm_table__ = "clients"
    
    #ID's
    id = Int(primary=True)
    
    #Text
    email = Unicode(validator=unicoder)
    password = Unicode(validator=unicoder)
    fname = Unicode(validator=unicoder)
    lname = Unicode(validator=unicoder)
    title = Unicode(validator=unicoder)

    #References
    companies = ReferenceSet(id, 'Company.client_id')

class ClientUser(Storm):
    ___storm_table__ = "client_users"
    
    #ID's
    id = Int(primary=True)
    client_id = Int()

    #Text
    email = Unicode(validator=unicoder)
    password = Unicode(validator=unicoder)
    fname = Unicode(validator=unicoder)
    lname = Unicode(validator=unicoder)

    #References
    client = ReferenceSet(client_id, 'Client.id')
    
class Employee(Storm):
    __storm_table__ = "employees"
    
    #ID's
    id = Int(primary=True)
    
    #Text
    email = Unicode(validator=unicoder)
    _password = Unicode('password', validator=unicoder) 
    fname = Unicode(validator=unicoder)
    lname = Unicode(validator=unicoder)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = md5(value).hexdigest()
    
    
