from storm.locals import *
from storm.expr import And, LeftJoin, Avg

from webpy.dark import *
from model.company import *
from model.trans2 import *
from model.users import *
from model.metrics import *

from itertools import izip
from datetime import date
import sys

from decimal import Decimal as Dec

sys.stdout = sys.stderr


class Report(Storm):
    """
    I represent a report generated off the Dashboard
    """

    def __init__(self, client_id=None, companies=[], divisions=[], regions=[], areas=[], trans_obj='acquisition', **kwargs):
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


        self.client = self.store.find(Client, Client.id == int(client_id)).one()
        self.metrics = self.client.metrics
        
        # REPORT TITLE
        if len(self.companies) == 1:
            company = self.store.find(Company, Company.id == int(self.companies[0])).one()
            self.title = company.title

        if len(self.divisions) == 1:
            div = self.store.find(CompanyDivision, CompanyDivision.id == int(self.divisions[0])).one()
            self.title = div.company.title
            self.title += ' &#187 ' + div.title

        if len(self.regions) == 1:
            reg = self.store.find(CompanyRegion, CompanyRegion.id == int(self.regions[0])).one()
            self.title = reg.division.title
            self.title += ' &#187 ' + reg.title

        if len(self.areas) == 1:
            area = self.store.find(companyArea, CompanyArea.id == int(self.areas[0])).one()
            self.title = area.region.title
            self.title += ' &#187 ' + area.title

        today = date.today()
        if today.month < 10:
            year = int(today.year)
            year = year -1
            current_fiscal_year = '%s-10-01' % year
            self.fy = year
            past_1_year = '%s-10-01' % (int(year) - 1)
            past_2_year = '%s-10-01' % (int(year) - 2)
        else:
            current_fiscal_year = '%s-10-01' % today.year
            self.fy = today.year
            past_1_year = '%s-10-01' % int(today.year) - 1
            past_2_year = '%s-10-01' % int(today.year) - 2

        def buildPreviousYear():
            """
            Build a report for 1 fiscal year ago
            """
            tmpfilters = {
                'objects':['Transaction', 'Transaction'],
                'fields':['cda', 'cda'],
                'constraints':['<=', '>='],
                'args':[current_fiscal_year, past_1_year],
                'operators':['none', 'and']
            }
            self.year1 = Report(client_id=client_id, companies=companies, divisions=divisions, regions=regions, areas=areas, trans_obj=trans_obj, filters=tmpfilters)
            self.year1.buildReport()
            self.year1.fy1 = int(self.fy) - 1

        def buildPreviousYear2():
            """
            Build a report for 2 fiscal years ago
            """
            tmpfilters = {
                'objects':['Transaction', 'Transaction'],
                'fields':['cda', 'cda'],
                'constraints':['<', '>='],
                'args':[past_1_year, past_2_year],
                'operators':['none', 'and']
            }
            self.year2 = Report(client_id=client_id, companies=companies, divisions=divisions, regions=regions, areas=areas, trans_obj=trans_obj, filters=tmpfilters)
            self.year2.buildReport()
            self.year2.fy2 = int(self.fy) - 2

            
        # Fiscal Comparison
        if 'fiscal' in kwargs.keys():
            f = kwargs['fiscal']
            if f == '1':
                buildPreviousYear()
            elif f == '1p':
                pass
            elif f =='2p':
                pass
            elif f =='2':
                buildPreviousYear()
                buildPreviousYear2()
                pass
            else:
                pass

        
        #FILTERS
        if 'filters' in kwargs.keys():
            self.filters = kwargs['filters']
        else:
            self.filters = {
                'objects':['Transaction'],
                'fields':['cda'],
                'constraints':['>='],
                'args':[current_fiscal_year],
                'operators':['none']
            }

    def returnMetric(self, field):
        """
        take a field name (one of the metrics) and determine its status
        """
        
        m = self.metrics.find(Metrics.field == unicode(field)).one()
        amount = getattr(self, field)
        operator = m.operator
        if amount == 'N/A':
            return ('', amount)
        if operator == '<=':
            if Dec(amount) <= m.bad_amount:
                return ('red', amount)
            if Dec(amount) <= m.warn_amount:
                return ('yellow', amount)
        elif operator == '>=':
            if Dec(amount) >= m.bad_amount:
                return ('red', amount)
            if Dec(amount) >= m.warn_amount:
                return ('yellow', amount)
            
        return ('', amount)


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
            origin = self.buildJoin(self.filters['objects']) 
            self.trans = self.store.using(*origin).find(Transaction, And(*self.exp),
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
            
            elif c == '>=':
                expressions = self.buildAndOr(o, expressions, [ fieldObj >= a ])

            elif c == '<=':
                expressions = self.buildAndOr(o, expressions, [ fieldObj <= a ])
                

        return expressions


    def buildExcelData(self):
        """
        return a tuple of data to export to excel
        """
        if self.trans_obj == 'acquisition':
            data = [
                ['Average Survey Score', self.avg_survey_score],
                ['Average Days to Business Terms', self.avg_days_business_terms],
                ['Average Days to Deal Closing', self.avg_days_deal_close],
                ['Days between Business Terms & Closing', self.avg_days_loi_to_deal_close],
                ['Market Survey On Time %', self.market_survey_ontime],
                ['Average Value Add %', self.avg_value_add],
                ['Engagement %', '']
            ]
        title = self.title.replace('&#187', ' ')
        title = title.replace(' ', '')
        return (title, data, ['a', 'b'])




    # METRICS

    @property
    def avg_survey_score(self):
        """
        Average Survey Score of all transactions with a attached survey
        """
        survey_count = 0
        survey_scores = []
        for tran in self.trans:
            if tran.survey:
                survey_count += 1
                answers = [qa.answer for qa in tran.survey.qa]
                scores = []
                for a in answers:
                    try:
                        scores.append(int(a))
                    except:
                        pass
                s_score = Dec(sum(scores)) / Dec(len(scores))
                survey_scores.append(s_score)
        if survey_scores:
            avg = Dec(sum(survey_scores)) / Dec(len(survey_scores))
            avg = "%.2f" % avg
            return avg
        return 'N/A'

    
    @property
    def avg_value_add(self):
        """
        Determine the average value added of all selected transactions
        """
        value_amounts = []
        for tran in self.trans:
            if tran.tchild:
                value = tran.tchild.value_add
                if value:
                    value_amounts.append(value)
        
        if value_amounts:
            avg = Dec(sum(value_amounts)) / Dec(len(value_amounts))
            avg = "%.2f" % avg
            return avg
        return 'N/A'


    @property
    def sqft_reduction(self):
        """
        This is the net difference between old sqft and new sqft across the portfolio
        """
        sqft_amounts = []
        for tran in self.trans:
            old_sqft = tran.tchild.old_sqft
            new_sqft = tran.tchild.new_sqft
            if old_sqft and new_sqft:
                sqft = old_sqft - new_sqft
                sqft_amounts.append(sqft)
        if sqft_amounts:
            return sum(sqft_amounts)
        return 'N/A'

    
    @property
    def avg_days_business_terms(self):
        """
        Tracks the days between engagement date and loi date. This tells how long it takes
        to negotiate.
        """
        days = []
        for tran in self.trans:
            engage = tran.engage_date
            loi = tran.loi_date
            
            if not engage:
                continue
            if not loi:
                continue
            diff = loi - engage
            days.append(diff.days)

        if days:
            avg = Dec(sum(days)) / Dec(len(days))
            avg = "%.2f" % avg
            return avg
        return 'N/A'

    
    
    @property
    def avg_days_deal_close(self):
        """
        Tracks the days between engagement date and deal closing (or execution date 
        in the case of dispositions). 
        """
        
        days = []
        for tran in self.trans:
           
            engage = tran.engage_date
            close = tran.closing_date
            
            if not engage:
                continue
            
            if not close:
                continue

            diff = close - engage
            days.append(diff.days)
        
        if days:
            avg = Dec(sum(days)) / Dec(len(days))
            avg = "%.2f" % avg
            return avg

        return 'N/A'
    
    @property
    def avg_days_loi_to_deal_close(self):
        """
        Tracks the days between loi and deal closing (or execution date 
        in the case of dispositions). 
        """
        
        days = []
        for tran in self.trans:
           
            loi = tran.loi_date
            close = tran.closing_date
            
            if not loi:
                continue
            
            if not close:
                continue

            diff = close - loi
            days.append(diff.days)
        
        if days:
            avg = Dec(sum(days)) / Dec(len(days))
            avg = "%.2f" % avg
            return avg
        return 'N/A'
    

    @property
    def market_survey_ontime(self):
        """
        Should be done within 2 weeks of when a client engages cbre. %
        """
        ontime = 0
        not_ontime = 0

        for tran in self.trans:
            if tran.tchild.market_survey:
                engage = tran.engage_date
                if not engage:
                    continue
                market = tran.tchild.market_survey_date
                if not market:
                    continue
                diff = market - engage
                if diff.days <= 14:
                    ontime += 1
                else:
                    not_ontime += 1

        if ontime or not_ontime:
            p = (Dec(ontime) / Dec(ontime + not_ontime)) * 100
            p = "%.2f" % p
            return p
        return 'N/A'
    
    
    @property
    def rfp_ontime(self):
        """
        Boolean yes or no, if no answer defaults to no.
        """
        
        ontime = 0
        not_ontime = 0

        for tran in self.trans:
            if not hasattr(tran.tchild, 'rfp_on_time'):
                continue
            if not tran.tchild.rfp_on_time:
                not_ontime += 1
                continue
            ontime += 1
        if ontime or not_ontime: 
            p = (Dec(ontime) / Dec(ontime + not_ontime)) * 100
            p = "%.2f" % p
            return Dec(p)
        return 'N/A'


    @property
    def engagement(self):
        """
        I think this will be manually input on metrics definition
        """
        return


    @property
    def avg_base_rent(self):
        """
        Average base rent of all transactions...
        """

        rent_amounts = []
        for tran in self.trans:
            if not hasattr(tran.tchild, 'average_base_rent'):
                continue
            rent = tran.tchild.average_base_rent
            if not rent:
                continue
            rent_amounts.append(rent)

        if rent_amounts:
            p = Dec(sum(rent_amounts)) / Dec(len(rent_amounts))
            p = "%.2f" % p
            return Dec(p)
        return 'N/A'


    @property
    def avg_time_on_market(self):
        """
        This is duplicate data with a different titile for the bosses
        """
        return self.avg_days_deal_close
        


    @property
    def num_survey_responses(self):
        """
        Total number of surveys received
        """

        count = 0
        for tran in self.trans:
            if tran.survey_id:
                count += 1
        if count:
            return count
        return 'N/A'


    @property
    def survey_resp_ratio(self):
        """
        Ratio of surveys received compared to surveys sent
        """
        
        sent = 0
        received = 0

        for tran in self.trans:
            if tran.survey_sent:
                sent += 1
            else:
                continue
            if tran.survey_id:
                received += 1
        if sent:
            p = (Dec(received) / Dec(sent)) * 100
            p = "%.2f" % p
            return p
        return 'N/A'

    ##
    ## DISPOSITIONS
    ##

    @property
    def bov_on_time(self):
        bov = 0
        ontime = 0

        for tran in self.trans:
            if tran.tchild.bov_date:
                bov += 1
            if tran.tchild.bov_ontime:
                ontime += 1

        if bov:
            p = (Dec(ontime) / Dec(bov)) * 100
            p = "%.2f" % p
            return Dec(p)

    @property
    def meet_bov_timing(self):
        """
        Percentage of bov timing that meet or exceeded expectations
        """
        exceed = 0
        below = 0
        for tran in self.trans:
            if tran.tchild.bov_date:
                expected = tran.tchild.bov_expected_timing
                if not expected:
                    continue
                actual = tran.tchild.bov_actual_timing

                if not actual:
                    continue

                if actual - expected > 0:
                    below += 1
                else:
                    exceed += 1
        if exceed or below:
            p = (Dec(exceed) / Dec(exceed + below)) * 100
            p = "%.2f" % p
            return Dec(p)
            

    
    @property
    def total_recovery(self):
        """
        Total recovery from all dispositions. 
        (actual_recovery, total_savings, sale_price)
        """

        amounts = []

        for tran in self.trans:
            recovery = tran.tchild.recovery
            if not recovery:
                continue
            amounts.append(recovery)
        if amounts:
            return sum(amounts)

    @property
    def meet_bov_recovery(self):
        """
        Percentage of bov recovery that meet or exceeded expectations
        """
        
        exceed = 0
        below = 0

        for tran in self.trans:
            expected = tran.tchild.exp_recovery
            actual = tran.tchild.recovery 
            if not expected:
                continue
            if not actual:
                continue

            if actual - expected > 0:
                below += 1
            else:
                exceed += 1
        
        if exceed or below:
            p = (Dec(exceed) / Dec(exceed + below)) * 100
            p = "%.2f" % p
            return Dec(p)


