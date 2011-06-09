from webpy.dark import *
from model.trans2 import *

import sys
from storm.locals import *
from storm.tracer import debug
from decimal import Decimal as Dec

class Foo(Storm):
    __storm_table__ = 'foo'    

    id = Int(primary=True)
    a = Decimal()


debug(True, stream=sys.stdout)
store = get_store()
#store.execute('create table foo (id serial, a decimal)')
blah = store.add(Foo())
blah.a = Dec('100.00')

store.commit()

