from storm.locals import *
from storm.expr import And, LeftJoin

from webpy.dark import *
from model.company import *
from model.trans2 import *
from model.users import *

from itertools import izip
from datetime import date

class Report(Storm):
    """
    I represent a report generated off the Dashboard
    """

    def __init__(self, companies=[], divisions=[], regions=[], areas=[], trans_obj='acquisition', **kwargs):
        """
        Build the base object
        """
        self.store = get_store() 
        self.companies = [int(id) for id in companies]
        self.divisions = [int(id) for id in divisions]
        self.regions = [int(id) for id in regions]
        self.areas = [int(id) for id in areas]
        self.acq_types = [u'New Lease', u'Lease Extension', u'Purchase']
        self.disp_types = [u'Sublease', u'Lease Termination', u'Sale']

        self.obj_map = {
            'New Lease':NewLease,
            'Lease Extension':LeaseExtension,
            'Purchase':Purchase,
            'Sublease':SubLease,
            'Lease Termination':LeaseTermination,
            'Sale':Sale,
            'Transaction':Transaction
        }


        self.trans_obj = trans_obj

        if 'filters' in kwargs:
            self.filters = kwargs['filters']
        else:
            self.filters = []

    def buildReport(self):
        
        self.trans = self.store.find(Transaction)

        if self.companies:
            self.trans = self.store.find(Transaction, Transaction.company_id.is_in(self.companies))
        if self.divisions:
            self.trans = self.trans.find(Transaction.division_id.is_in(self.divisions))
        if self.regions:
            self.trans = self.trans.find(Transaction.region_id.is_in(self.regions))
        if self.areas:
            self.trans = self.trans.find(Transaction.area_id.is_in(self.areas))
        
        if self.trans_obj == 'acquisition':
            self.trans = self.trans.find(Transaction.trans_type.is_in(self.acq_types))
        else:
            self.trans = self.trans.find(Transaction.trans_type.is_in(self.disp_types))

        if self.filters:
            self.exp = self.buildExp(
                self.filters['objects'], 
                self.filters['fields'],
                self.filters['constraints'],
                self.filters['args'],
                self.filters['operators']
            )
            self.origin = self.buildJoin(self.filters['objects']) 
            #self.origin = [Transaction, Join(self.trans_obj, self.trans_obj.trans_id == Transaction.id)]

            #self.subselect = Select(Transaction.id, Transaction.company_id.is_in(self.companies),
            #    Transaction.division_id.is_in(self.divisions),Transaction.region_id.is_in(self.regions))

            #self.transactions = self.store.find(Transaction, Transaction.id.is_in(self.subselect))
            self.transactions = self.store.using(*self.origin).find(Transaction, And(*self.exp),
                And(Transaction.id.is_in([tran.id for tran in self.trans])))


    def buildJoin(self, obs):
        """
        Determine which tables need to be joined to make this report
        """

        origin = [Transaction]
        for ob in set(obs):
            if ob == 'Transaction':
                continue
            obj = self.obj_map[ob]
            origin.append(LeftJoin(obj,obj.trans_id == Transaction.id))
        return origin


    def returnValidated(self, a, t):
        """
        I hacked storm and I don't like this
        Returns the argument in the proper type to be compared in the database

        a - argument to validate
        t - type of column
        """

        if 'Unicode' in str(type(t)):
            return unicode(a)
        if 'Int' in str(type(t)):
            return int(a)
        if 'Date' in str(type(t)):
            m, d, y = map(int, a.split('-'))
            return date(y, m, d)

    def buildAndOr(self, op, baseExp, joiner):
        """
        Take an operator, expression list, and joining expression and determine
        how to wrap it.
        """

        if baseExp:
            if op == 'and':
                baseExp += [joiner] 
                return baseExp
            elif op == 'or':
                last = baseExp.pop()
                baseExp += [Or(last, joiner)]
                return baseExp
        else:
            baseExp = []
            baseExp += joiner
            return baseExp

    def buildExp(self, obj, fields, constraints, args, op):
        """
        Take a list of objects, fields, constraints, args, operators, and build an expression
        for the Storm object to read
        """

        expressions = []
        for ob, f, c, a, o in izip(obj, fields, constraints, args, op):
            trans_obj = self.obj_map[ob]
            trans_field = trans_obj.imap[f]
            
            if hasattr(trans_obj, trans_field):
                fieldObj = getattr(trans_obj, trans_field)
            
            a = self.returnValidated(a, fieldObj.cprop) #cprop is a storm hack
            
            if c == '==':
                expressions = self.buildAndOr(o, expressions, [ fieldObj == a ])
            elif c == '<':
                expressions = self.buildAndOr(o, expressions, [ fieldObj < a ])
            elif c == '>':
                expressions = self.buildAndOr(o, expressions, [ fieldObj > a ])

        return expressions
            
