from storm.locals import *
from storm.expr import And

from webpy.dark import *
from model.company import *
from model.transaction import *
from model.users import *

from itertools import izip
from datetime import date

class Report(Storm):
    """
    I represent a report generated off the Dashboard
    """

    def __init__(self, companies=[], divisions=[], regions=[], trans_obj='acquisition', **kwargs):
        """
        Build the base object
        """
        self.store = get_store() 
        self.companies = companies
        self.divisions = divisions
        self.regions = regions
       
        if trans_obj == 'acquisition':
            self.trans_obj = Acquisition
        elif trans_obj == 'disposition':
            self.trans_obj = Disposition

        if 'filters' in kwargs:
            self.filters = kwargs['filters']
        else:
            self.filters = []

    def buildReport(self):
        
        self.trans = self.store.find(Transaction)

        if self.companies:
            self.trans = self.store.find(Transaction, Transaction.company_id.is_in(self.companies))
        if self.divisions:
            self.trans = trans.find(Transaction.division_id.is_in(self.divisions))
        if self.regions:
            self.trans = trans.find(Transaction.region_id.is_in(self.regions))


        if self.filters:
            self.exp = self.buildExp(self.trans_obj, 
                self.filters['fields'],
                self.filters['constraints'],
                self.filters['args'],
                self.filters['operators']
            )
            
            self.origin = [Transaction, Join(self.trans_obj, self.trans_obj.trans_id == Transaction.id)]

            self.subselect = Select(Transaction.id, Transaction.company_id.is_in(self.companies),
                Transaction.division_id.is_in(self.divisions),Transaction.region_id.is_in(self.regions))

            #self.transactions = self.store.find(Transaction, Transaction.id.is_in(self.subselect))
            self.transactions = self.store.using(*self.origin).find(Transaction, And(*self.exp))

            #self.transactions = self.transactions.find(And(*self.exp))


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
            y, m, d = map(int, a.split('-'))
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
        Take a list of fields, constraints, args, operators, and build an expression
        for the Storm object to read
        """

        expressions = []
        for f, c, a, o in izip(fields, constraints, args, op):
            if hasattr(Transaction, f):
                fieldObj = getattr(Transaction, f)
            else:
                fieldObj = getattr(obj, f)
            
            a = self.returnValidated(a, fieldObj.cprop) #cprop is a storm hack
            
            if c == '==':
                expressions = self.buildAndOr(o, expressions, [ fieldObj == a ])
            elif c == '<':
                expressions = self.buildAndOr(o, expressions, [ fieldObj < a ])
            elif c == '>':
                expressions = self.buildAndOr(o, expressions, [ fieldObj > a ])

        return expressions
            
