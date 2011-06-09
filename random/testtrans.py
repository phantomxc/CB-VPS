from webpy.dark import *
from storm.locals import *
from model.transaction import Transaction, NewLease

store = get_store()

trans = store.add(Transaction())

trans.client_id = 69
trans.trans_type = 'NewLease'
store.commit()

lease = store.add(NewLease())

lease.trans_id = trans.id
lease.old_sqft = 12
store.commit()
print lease.id
print lease.transaction.client_id
print trans.newlease.old_sqft

trans.getLink()
