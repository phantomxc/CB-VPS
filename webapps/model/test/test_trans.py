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


    def test_transaction_child(self):
        """
        I test that a transaction obj child property links properly
        """
        t1 = self.fstore(Transaction())  
        nl1 = self.fstore(NewLease())
        self.store.commit()
        t1.trans_type = 'New Lease'
        nl1.trans_id = t1.id

        self.store.commit()
       
        self.assertEqual(t1.tchild, nl1)

if __name__ == '__main__':
    unittest.main() 
