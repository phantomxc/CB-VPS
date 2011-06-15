import unittest
from unittest import TestCase
from storm.locals import *
from webpy.dark import *

from model.company import *
from model.trans2 import *
from model.users import *
from model.report import Report

import datetime

import sys
from storm.tracer import debug
debug(True, stream=sys.stdout)

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
        return;
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
        t1.trans_type = u'New Lease'

        t2 = self.fstore(Transaction())
        t2.company_id = self.comp1.id
        t2.division_id = 23
        t2.trans_type = u'New Lease'

    
        t3 = self.fstore(Transaction())
        t3.company_id = self.comp1.id
        t3.division_id = self.div1.id
        t3.region_id = self.reg1.id
        t3.trans_type = u'New Lease'

        self.store.commit()

        r = Report(companies=[self.comp1.id], divisions=[self.div1.id])
        r.buildReport()
        self.assertEqual(r.trans.count(), 2)

        r = Report(companies=[self.comp1.id])
        r.buildReport()
        self.assertEqual(r.trans.count(), 3)

        r = Report(companies=[self.comp1.id], divisions=[self.div1.id], regions=[self.reg1.id])
        r.buildReport()
        self.assertEqual(r.trans.count(), 1)

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
            'objects':['Transaction'],
            'fields':['ttpe'], 
            'constraints':['=='], 
            'args':['New Lease'],
            'operators':['none']}


        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()
        
        self.assertEqual(r.transactions.count(), 2)
        # TWO FILTERS
        filters = {
            'objects':['Transaction', 'Transaction'],
            'fields':['ttpe', 'tman'], 
            'constraints':['==', '=='], 
            'args':['New Lease', '1'],
            'operators':['none','and']}

        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
        # THREE FILTERS NO RESULTS
        filters = {
            'objects':['Transaction', 'Transaction', 'Transaction'],
            'fields':['ttpe', 'tman', 'eda'], 
            'constraints':['==', '==', '=='], 
            'args':['New Lease', '1', '05-15-2011'],
            'operators':['none','and', 'and']}

        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()

        self.assertEqual(r.transactions.count(), 0)
        
        
        # THREE FILTERS
        filters = {
            'objects':['Transaction', 'Transaction', 'Transaction'],
            'fields':['ttpe', 'tman', 'eda'], 
            'constraints':['==', '==', '=='], 
            'args':['New Lease', '1', '05-15-2011'],
            'operators':['none','and', 'and']}
        
        t2.engage_date = '05-15-2011'
        self.store.commit()

        r = Report(companies=[self.comp1.id], filters=filters)
        r.buildReport()
        self.assertEqual(r.transactions.count(), 1)

        
        # SINGLE FILTER < CONSTRAINT
        filters = {
            'objects':['Transaction'],
            'fields':['eda'], 
            'constraints':['<'], 
            'args':['05-20-2011'],
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
        nl1 = self.fstore(NewLease())
        self.store.commit()
        t1.company_id = self.comp1.id
        t1.trans_type = 'New Lease'
        t1.trans_manager = 3
        nl1.old_sqft = 100
        nl1.trans_id = t1.id
        
        t2 = self.fstore(Transaction())
        nl2 = self.fstore(NewLease())
        self.store.commit()
        t2.company_id = self.comp1.id
        t2.trans_type = 'New Lease'
        t2.trans_manager = 1
        nl2.old_sqft = 200
        nl2.trans_id = t2.id

        t3 = self.fstore(Transaction())
        le1 = self.fstore(LeaseExtension())
        self.store.commit()
        t3.company_id = self.comp1.id
        t3.trans_type = 'Lease Extension'
        t3.trans_manager = 1

        le1.market_survey_date = '05-15-2011'
        le1.old_sqft = 100
        le1.trans_id = t3.id
        

        self.store.commit()
        
        # ONE FILTER == CONSTRAINT
        filters = {
            'objects':['New Lease'],
            'fields':['nl2'], 
            'constraints':['=='], 
            'args':['100'],
            'operators':['none']}


        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()
        self.assertEqual(r.transactions.count(), 1)

        # TWO FILTERS
        filters = {
            'objects':['New Lease', 'New Lease'],
            'fields':['nl2', 'nl2'], 
            'constraints':['>', '>'], 
            'args':['500', '101'],
            'operators':['none','or']}


        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
        
        # FOUR FILTERS TWO OBJECTS
        filters = {
            'objects':['Transaction', 'Transaction', 'New Lease', 'New Lease'],
            'fields':['ttpe', 'tman', 'nl6', 'nl2'], 
            'constraints':['==', '==', '==', '<'], 
            'args':['New Lease', '1', '05-15-2011', '300'],
            'operators':['none','and', 'and', 'and']}

        nl2.market_survey_date = '05-15-2011'
        self.store.commit()

        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.transactions.count(), 1)
        
        # FOUR FILTERS TWO OBJECTS
        filters = {
            'objects':[
                'Transaction', 'Transaction', 'Transaction', 
                'New Lease', 'Lease Extension', 'New Lease',
                'Lease Extension'],
            'fields':['ttpe', 'ttpe', 'tman', 'nl6', 'le6', 'nl2', 'le2'], 
            'constraints':['==', '==', '==', '==', '==', '<', '<'], 
            'args':['New Lease', 'Lease Extension', '1', '05-15-2011', '05-15-2011', '300', '300'],
            'operators':['none','or', 'and', 'and', 'or', 'and', 'or']}

        r = Report(companies=[self.comp1.id], filters=filters, trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.transactions.count(), 2)
if __name__ == '__main__':
    unittest.main() 
