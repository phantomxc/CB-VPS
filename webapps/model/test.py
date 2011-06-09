from webpy.dark import *
from storm.locals import *
from model.users import *
from model.company import *
from model.report import *
from storm.tracer import debug
import sys

debug(True, stream=sys.stdout)
store = get_store()


filters = {'fields':['trans_type', 'trans_manager', 'trans_type', 'region_id', 'region_id', 'region_id'], 
    'constraints':['==', '==', '==', '==', '==', '=='], 
    'args':['New Lease', '1', 'Purchase', '1', '2', '3'],
    'operators':['none', 'and', 'or', 'and', 'or', 'or']}

filters = {
    'fields':['company_id', 'trans_id', 'trans_id', 'old_sqft', 'trans_manager'],
    'constraints':['==', '==', '==', '==', '=='],
    'args':['3', '325', '326', '100', '1'],
    'operators':['none', 'and', 'or', 'and', 'and']
}

r = Report(companies=[1, 2], divisions=[], regions=[], filters=filters, trans_obj='acquisition')
r.buildReport()
#print r.transactions
#print [x for x in r.transactions.values(Transaction.id)]
print r.transactions
#print [x for x in r.transactions]
print [x for x in r.transactions.values(Transaction.id)]
