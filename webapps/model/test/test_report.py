import unittest
from unittest import TestCase
from storm.locals import *
from webpy.dark import *

from model.company import *
from model.transaction import *
from model.users import *
from model.report import Report

from datetime import date

import sys
from storm.tracer import debug
debug(False, stream=sys.stdout)

class TestReport(TestCase):

    def fstore(self, obj):
        """
        Fake store so it's easy to delete all created objects
        """
        self.objs.append(obj)
        x = self.store.add(obj)
        return x

    def setUp(self):
        self.store = get_store()
        self.objs = []
        
        self.comp1 = self.store.add(Company())
        self.comp2 = self.store.add(Company())
        self.div1 = self.store.add(CompanyDivision())
        self.div2 = self.store.add(CompanyDivision())
        self.reg1 = self.store.add(CompanyRegion())
        self.reg2 = self.store.add(CompanyRegion())
        self.comp1.divisions.add(self.div1)
        
        self.objs += [self.comp1, self.comp2, self.div1, self.div2, self.reg1, self.reg2]

        self.store.commit()

    def tearDown(self):
       
        for x in self.objs:
            self.store.remove(x) 
        self.store.commit()

    def test_create_basic(self):
        """
        I test that you can create the basic Report object
        """
        
        r = Report(companies=[self.comp1.id], divisions=[self.div1.id])
        self.assertEqual(r.companies, [self.comp1.id])
        self.assertEqual(r.divisions, [self.div1.id])
        self.assertEqual(r.regions, [])

    def test_build_report_transactions(self):
        """
        I test that a report can be generated soley on company, division or region
        """
        
        t1 = self.fstore(Transaction())
        t1.company_id = self.comp1.id
        t1.division_id = self.div1.id

        t2 = self.fstore(Transaction())
        t2.company_id = self.comp1.id
        t2.division_id = 23

    
        t3 = self.fstore(Transaction())
        t3.company_id = self.comp1.id
        t3.division_id = self.div1.id
        t3.region_id = self.reg1.id

        self.store.commit()

        r = Report(companies=[self.comp1.id], divisions=[self.div1.id])
        r.buildReport()
        self.assertEqual(r.transactions.count(), 2)

        r = Report(companies=[self.comp1.id])
        r.buildReport()
        self.assertEqual(r.transactions.count(), 3)

        r = Report(companies=[self.comp1.id], divisions=[self.div1.id], regions=[self.reg1.id])
        r.buildReport()
        self.assertEqual(r.transactions.count(), 1)

    def test_build_report_transactions_expressions(self):
        """
        I test that we can build some basic expressions on the transaction obj
        """
        
        t1 = self.fstore(Transaction())
        t1.company_id = self.comp1.id
        t1.trans_type = 'New Lease'
        t1.trans_manager = 3

        t2 = self.fstore(Transaction())
        t2.company_id = self.comp1.id
        t2.trans_type = 'New Lease'
        t2.trans_manager = 1

    
        t3 = self.fstore(Transaction())
        t3.company_id = self.comp1.id

        self.store.commit()
        
        # ONE FILTER == CONSTRAINT
        filters = {
            'fields':['trans_type'], 
            'constraints':['=='], 
            'args':['New Lease'],
            'operators':['none']}


        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()
        
        self.assertEqual(r.transactions.count(), 2)

        # TWO FILTERS
        filters = {
            'fields':['trans_type', 'trans_manager'], 
            'constraints':['==', '=='], 
            'args':['New Lease', '1'],
            'operators':['none','and']}


        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
        # THREE FILTERS NO RESULTS
        filters = {
            'fields':['trans_type', 'trans_manager', 'trans_date'], 
            'constraints':['==', '==', '=='], 
            'args':['New Lease', '1', '2011-05-15'],
            'operators':['none','and', 'and']}


        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()

        self.assertEqual(r.transactions.count(), 0)
        
        # THREE FILTERS
        filters = {
            'fields':['trans_type', 'trans_manager', 'trans_date'], 
            'constraints':['==', '==', '=='], 
            'args':['New Lease', '1', '2011-05-15'],
            'operators':['none','and', 'and']}

        timevar = '2011-05-15'
        year, month, day = map(int, timevar.split('-'))
        t2.trans_date = date(year, month, day)
        self.store.commit()

        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
        # SINGLE FILTER < CONSTRAINT
        filters = {
            'fields':['trans_date'], 
            'constraints':['<'], 
            'args':['2011-05-20'],
            'operators':['none']}
        
        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()
        
        self.assertEqual(r.transactions.count(), 1)
        self.assertEqual(r.transactions.one().trans_manager, 1)

    def test_build_report_acq_expressions(self):
        """
        I test that we can build some basic expressions on the acq obj
        """
        t1 = self.fstore(Transaction())  
        a1 = self.fstore(Acquisition())
        self.store.commit()
        t1.company_id = self.comp1.id
        t1.trans_type = 'New Lease'
        t1.trans_manager = 3
        a1.old_sqft = 100
        a1.trans_id = t1.id
        
        t2 = self.fstore(Transaction())
        a2 = self.fstore(Acquisition())
        self.store.commit()
        t2.company_id = self.comp1.id
        t2.trans_type = 'New Lease'
        t2.trans_manager = 1
        a2.old_sqft = 200
        a2.trans_id = t2.id

    
        t3 = self.fstore(Transaction())
        t3.company_id = self.comp1.id

        self.store.commit()
        
        # ONE FILTER == CONSTRAINT
        filters = {
            'fields':['old_sqft'], 
            'constraints':['=='], 
            'args':['100'],
            'operators':['none']}


        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()
        print [x.old for x in r.transactions] 
        self.assertEqual(r.transactions.count(), 1)

        # TWO FILTERS
        filters = {
            'fields':['old_sqft', 'old_sqft'], 
            'constraints':['<', '>'], 
            'args':['500', '101'],
            'operators':['none','or']}


        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
        # THREE FILTERS NO RESULTS
        filters = {
            'fields':['trans_type', 'trans_manager', 'trans_date'], 
            'constraints':['==', '==', '=='], 
            'args':['New Lease', '1', '2011-05-15'],
            'operators':['none','and', 'and']}


        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()

        self.assertEqual(r.transactions.count(), 0)
        
        # THREE FILTERS
        filters = {
            'fields':['trans_type', 'trans_manager', 'trans_date', 'old_sqft'], 
            'constraints':['==', '==', '==', '<'], 
            'args':['New Lease', '1', '2011-05-15', '300'],
            'operators':['none','and', 'and', 'and']}

        timevar = '2011-05-15'
        year, month, day = map(int, timevar.split('-'))
        a2.trans_date = date(year, month, day)
        self.store.commit()

        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
if __name__ == '__main__':
    unittest.main() 
