from webpy.dark import *
from storm.locals import *

class ClientProperty(Storm):
    """
    I represent a property
    """
    __storm_table__ = "clientproperties"
    
    id = Int(primary=True)
    address = Unicode(validator=unicoder)
    city = Unicode(validator=unicoder)
    state = Unicode(validator=unicoder)
    zipcode = Unicode(validator=unicoder)
    sqft = Int(validator=intify)

    #References
    trans = ReferenceSet(id, 'Transaction.property_id')


    def __init__(self):
        self.imap = {
            'addr':'address',
            'cty':'city',
            'st':'state',
            'zip':'zipcode',
            'sqft':'sqft',
        }

    
    def create(self, **kwargs):
        """
        Create a new property from a list of mapped kwargs
        """

        for k, v in kwargs.items():
            if k in self.imap:
                ik = self.interfaceMap(k)
                if hasattr(self, ik):
                    setattr(self, ik, v)

    def interfaceMap(self, key):
        """
        Return the appropriate attribute name for the key provided
        """
        return self.imap[key]

