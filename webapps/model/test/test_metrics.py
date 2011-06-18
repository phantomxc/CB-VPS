import unittest
from unittest import TestCase
from storm.locals import *
from webpy.dark import *

from model.company import *
from model.trans2 import *
from model.users import *
from model.report import Report

import datetime
from decimal import Decimal as Dec
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

        self.t1 = self.fstore(Transaction())
        self.nl1 = self.fstore(NewLease())
        self.store.flush()
        self.nl1.trans_id = self.t1.id

        self.t1.company_id = self.comp1.id
        self.t1.division_id = self.div1.id
        self.t1.trans_type = u'New Lease'

        self.t2 = self.fstore(Transaction())
        self.nl2 = self.fstore(NewLease())
        self.store.flush()
        self.nl2.trans_id = self.t2.id

        self.t2.company_id = self.comp1.id
        self.t2.division_id = 23
        self.t2.trans_type = u'New Lease'

    
        self.t3 = self.fstore(Transaction())
        self.nl3 = self.fstore(NewLease())
        self.store.flush()
        self.nl3.trans_id = self.t3.id

        self.t3.company_id = self.comp1.id
        self.t3.division_id = self.div1.id
        self.t3.region_id = self.reg1.id
        self.t3.trans_type = u'New Lease'

        self.store.commit()

    def tearDown(self):
        for x in self.objs:
            self.store.remove(x) 
        self.store.commit()


    def test_build_report(self):
        """
        testing the report finds the correct amount of transactions
        """

        r = Report(trans_obj='acquisition')
        r.buildReport()
        self.assertEqual(r.trans.count(), 3)

    
    def test_avg_value_add(self):
        """
        Testing the average value added of all transactions in the report
        """
        self.nl1.value_add = 25
        self.nl2.value_add = 50
        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.avg_value_add, Dec('37.5'))


    def test_sqft_reduction(self):
        """
        testing the net difference btween old sqft and new sqft
        """

        self.nl1.old_sqft = 100
        self.nl1.new_sqft = 75
        
        self.nl2.old_sqft = 400
        self.nl2.new_sqft = 200
        
        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.sqft_reduction, 225)

        #missing data from one transaction, result should not be affected.

        self.nl3.old_sqft = 400
        self.store.commit()

        self.assertEqual(r.sqft_reduction, 225)


    def test_avg_days_business_terms(self):
        """
        Test the avg days to business terms. Difference btween engagement date and loi date.
        """
        pass


    def test_avg_deal_close(self):
        """
        Tracks the days bewteen engagement date and deal closing
        """

        self.t1.engage_date = '2011-05-01'
        self.nl1.lease_execution_date = '2011-05-02'

        self.t2.engage_date = '2011-05-01'
        self.nl2.lease_execution_date = '2011-05-03'

        self.store.commit()
        
        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.avg_days_deal_close, Dec('1.5'))

       
        #missing data from one transaction, result should not be affectd.

        self.t3.engage_date = '2011-05-01'
        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()
        
        self.assertEqual(r.avg_days_deal_close, Dec('1.5'))


    def test_market_survey_ontime(self):
        """
        Test that the market survey on time percentage is correct
        """
        self.t1.engage_date = '2011-05-01'
        self.t2.engage_date = '2011-05-01'

        self.nl1.market_survey = True
        self.nl1.market_survey_date = '2011-05-03'

        self.nl2.market_survey = True
        self.nl2.market_survey_date = '2011-06-15'

        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.market_survey_ontime, Dec('50.0'))


    def test_rfp_on_time(self):
        """
        checks the percentage of rfps on time
        """
        
        self.nl1.rfp_on_time = True
        self.nl2.rfp_on_time = True
        self.nl3.rfp_on_time = False

        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.rfp_ontime, Dec('66.67'))



    def test_avg_base_rent(self):
        """
        Determines the avg base rent across transactions
        """
        
        self.nl1.average_base_rent = 1523.34
        self.nl2.average_base_rent = 32152.56

        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.avg_base_rent, Dec('16837.95'))


    def test_avg_time_on_market(self):
        """
        This smells like a duplicate to me
        """

        self.t1.engage_date = '2011-05-01'
        self.nl1.lease_execution_date = '2011-05-02'

        self.t2.engage_date = '2011-05-01'
        self.nl2.lease_execution_date = '2011-05-03'

        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.avg_time_on_market, 2)

    def test_num_of_surveys(self):
        """
        Total count of surveys from transactions
        """

        self.t1.survey_id = '1'
        self.t2.survey_id = '2'

        self.store.commit()

        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.num_survey_responses, 2)

    def test_survey_ratio(self):
        """
        ratio of transactions with surveys
        """

        self.t1.survey_sent = '2011-05-01'
        self.t1.survey_id = 1

        self.t2.survey_sent = '2011-05-01'

        self.store.commit()
        
        r = Report(trans_obj='acquisition')
        r.buildReport()

        self.assertEqual(r.survey_resp_ratio, Dec('50.0'))



# DISPOSITIONS
    def build_disp(self):
        self.sl1 = self.fstore(SubLease())
        self.t1.trans_type = 'Sublease'
        self.sl1.trans_id = self.t1.id
        
        self.sl2 = self.fstore(SubLease())
        self.t2.trans_type = 'Sublease'
        self.sl2.trans_id = self.t2.id
        
        self.sl3 = self.fstore(SubLease())
        self.t3.trans_type = 'Sublease'
        self.sl3.trans_id = self.t3.id
        self.store.commit()
        

    def test_bov_on_time(self):
        """
        Number of BOVs compared to BOVs ontime
        """

        self.build_disp()

        print self.t1.trans_type

        self.sl1.bov_ontime = True
        self.sl2.bov_ontime = False
        self.sl3.bov_ontime = True

        self.sl1.bov_date = '2011-05-11'
        self.sl2.bov_date = '2011-05-11'
        self.sl3.bov_date = '2011-05-11'

        self.store.commit()
        print self.t1.tchild.bov_ontime

        r = Report(trans_obj='disposition')
        r.buildReport()

        self.assertEqual(r.bov_on_time, Dec('66.67'))

    
    def test_meet_bov(self):
        """
        Test percentage of bov timing that meet or exceeded expectations
        """

        


if __name__ == '__main__':
    unittest.main() 
