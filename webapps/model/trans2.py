from webpy.dark import *
from storm.locals import *
from model.client_prop import ClientProperty

class Transaction(Storm):
    """
    I represent a client transaction
    """
    __storm_table__ = "transactions"
    # IDs    
    id = Int(primary=True)
    client_id = Int(validator=intify)
    company_id = Int(validator=intify)
    division_id = Int(validator=intify)
    region_id = Int(validator=intify)
    area_id = Int(validator=intify)
    trans_manager = Int(validator=intify)
    property_id = Int(validator=intify)
    survey_id = Int(validator=intify)
    
    #Text
    client_trans_manager = Unicode(validator=unicoder)
    trans_type = Unicode(validator=unicoder)
    
    #Dates
    engage_date = Date(validator=datify)
    rebc_entry_date = Date(validator=datify)    
    
    #References
    prop = Reference(property_id, 'ClientProperty.id')
    survey = Reference(survey_id, 'Zoom.id')
        
        #Acquisitions
    newlease = Reference(id, 'NewLease.trans_id')
    leaseext = Reference(id, 'LeaseExtension.trans_id')
    purchase = Reference(id, 'Purchase.trans_id')

        #Dispositions
    sublease = Reference(id, 'SubLease.trans_id')
    leasetermination = Reference(id, 'LeaseTermination.trans_id')
    sale = Reference(id, 'Sale.trans_id')

    @property    
    def tchild(self):
        """
        I create an easy link to the transactions child
        """
        if self.trans_type == 'New Lease':
            return self.newlease
        elif self.trans_type == 'Lease Extension':
            return self.leaseext
        elif self.trans_type == 'Purchase':
            return self.purchase
        elif self.trans_type == 'Sublease':
            return self.sublease
        elif self.trans_type == 'Lease Termination':
            return self.leasetermination
        elif self.trans_type == 'Sale':
            return self.sale
        else:
            return None
    
    imap = {
        'cid':'client_id', 'coid':'company_id',
        'did':'division_id', 'rid':'region_id',
        'aid':'area_id', 'tman':'trans_manager',
        'pid':'property_id', 'sid':'survey_id',
        'ctman':'client_trans_manager', 'ttpe':'trans_type',
        'eda':'engage_date', 'rebc':'rebc_entry_date',
    }


    def create(self, **kwargs):
        """
        Create a new transaction from kwargs
        """
        for k, v in kwargs.items():
            if k in self.imap:
                ik = self.interfaceMap(k)
                if hasattr(self, ik):
                    setattr(self, ik, v)

    
    def interfaceMap(self, key):
        """
        Return the appropriate attribute name for the key provided
        """
        return self.imap[key]



class NewLease(Storm):
    """
    I am a type of transaction
    """
    __storm_table__ = "new_lease"

    #IDs
    id = Int(primary=True)
    trans_id = Int(validator=intify)
    
    # Numbers
    old_sqft = Int(validator=intify)
    new_sqft = Int(validator=intify)
    value_add = Int(validator=intify)
    average_base_rent = Decimal(validator=decimify)

    # Dates
    market_survey_date = Date(validator=datify)
    lease_execution_date = Date(validator=datify)

    # Bools    
    market_survey = Bool(validator=boolify)
    rfp_on_time = Bool(validator=boolify)
    
    # Text
    notes = Unicode(validator=unicoder)

    # References
    transaction = Reference(trans_id, 'Transaction.id')

    imap = {
        'trans_id':'trans_id',
        'nl2':'old_sqft',
        'nl3':'new_sqft',
        'nl4':'value_add',
        'nl5':'average_base_rent',
        'nl6':'market_survey_date',
        'nl7':'lease_execution_date',
        'nl8':'market_survey',
        'nl9':'rfp_on_time',
        'nl10':'notes'
    }

class LeaseExtension(Storm):
    """
    I am a type of transaction
    """
    __storm_table__ = "lease_extension"

    #IDs
    id = Int(primary=True)
    trans_id = Int(validator=intify)
    
    # Numbers
    old_sqft = Int(validator=intify)
    new_sqft = Int(validator=intify)
    value_add = Int(validator=intify)
    average_base_rent = Decimal(validator=decimify)

    # Dates
    market_survey_date = Date(validator=datify)
    lease_execution_date = Date(validator=datify)

    # Bools    
    market_survey = Bool(validator=boolify)
    rfp_on_time = Bool(validator=boolify)

    # Text
    notes = Unicode(validator=unicoder)

    # References
    transaction = Reference(trans_id, 'Transaction.id')

    imap = {
        'trans_id':'trans_id',
        'le2':'old_sqft',
        'le3':'new_sqft',
        'le4':'value_add',
        'le5':'average_base_rent',
        'le6':'market_survey_date',
        'le7':'lease_execution_date',
        'le8':'market_survey',
        'le9':'rfp_on_time',
        'le10':'notes'
    }


class Purchase(Storm):
    """
    I am a type of transaction
    """
    __storm_table__ = "purchase"

    #IDs
    id = Int(primary=True)
    trans_id = Int(validator=intify)
    
    # Numbers
    old_sqft = Int(validator=intify)
    new_sqft = Int(validator=intify)
    value_add = Int(validator=intify)
    purchase_price = Decimal(validator=decimify)

    # Dates
    market_survey_date = Date(validator=datify)
    purchase_close_date = Date(validator=datify)

    # Text
    notes = Unicode(validator=unicoder)

    # Bools    
    market_survey = Bool(validator=boolify)
    
    # References
    transaction = Reference(trans_id, 'Transaction.id')

    imap = {
        'trans_id':'trans_id',
        'p2':'old_sqft',
        'p3':'new_sqft',
        'p4':'value_add',
        'p5':'purchase_price',
        'p6':'market_survey_date',
        'p7':'purchase_close_date',
        'p8':'notes',
        'p9':'market_survey',
    }


class SubLease(Storm):
    """
    I am a type of transaction
    """
    __storm_table__ = "sub_lease"

    #IDs
    id = Int(primary=True)
    trans_id = Int(validator=intify)

    # Numbers
    sqft = Int(validator=intify)
    bov_expected_timing = Int(validator=intify)
    bov_actual_timing = Int(validator=intify)
    expected_recovery = Decimal(validator=decimify)
    actual_recovery = Decimal(validator=decimify)

    # Dates
    bov_date = Date
    sublease_execution_date = Date(validator=datify)

    # Text
    notes = Unicode(validator=unicoder)

    #bools 
    bov_ontime = Bool(validator=boolify)

    # References
    transaction = Reference(trans_id, 'Transaction.id')
   
    imap = {
        'trans_id':'trans_id',
        'sl2':'sqft',
        'sl3':'bov_expected_timing',
        'sl4':'bov_actual_timing',
        'sl5':'expected_recovery',
        'sl6':'actual_recovery',
        'sl7':'bov_date',
        'sl8':'sublease_execution_date',
        'sl9':'notes',
        'sl10':'bov_ontime'
    }


class LeaseTermination(Storm):
    """
    I am a type of transaction
    """
    __storm_table__ = "lease_termination"

    #IDs
    id = Int(primary=True)
    trans_id = Int(validator=intify)

    # Numbers
    sqft = Int(validator=intify)
    bov_expected_timing = Int(validator=intify)
    bov_actual_timing = Int(validator=intify)
    expected_savings = Decimal(validator=decimify)
    total_savings = Decimal(validator=decimify)

    # Dates
    bov_date = Date
    ltd_execution_date = Date(validator=datify)

    # Text
    notes = Unicode(validator=unicoder)

    #bools 
    bov_ontime = Bool(validator=boolify)

    # References
    transaction = Reference(trans_id, 'Transaction.id')
    
    imap = {
        'trans_id':'trans_id',
        'lt2':'sqft',
        'lt3':'bov_expected_timing',
        'lt4':'bov_actual_timing',
        'lt5':'expected_savings',
        'lt6':'total_savings',
        'lt7':'bov_date',
        'lt8':'ltd_execution_date',
        'lt9':'notes',
        'lt10':'bov_ontime'
    }


class Sale(Storm):
    """
    I am a type of transaction
    """
    __storm_table__ = "sale"

    #IDs
    id = Int(primary=True)
    trans_id = Int(validator=intify)

    # Numbers
    sqft = Int(validator=intify)
    bov_expected_timing = Int(validator=intify)
    bov_actual_timing = Int(validator=intify)
    expected_sale_price = Decimal(validator=decimify)
    sale_price = Decimal(validator=decimify)

    # Dates
    bov_date = Date(validator=datify)
    sale_closing_date = Date(validator=datify)

    # Text
    notes = Unicode(validator=unicoder)

    #bools 
    bov_ontime = Bool(validator=boolify)

    # References
    transaction = Reference(trans_id, 'Transaction.id')
    
    imap = {
        'trans_id':'trans_id',
        's2':'sqft',
        's3':'bov_expected_timing',
        's4':'bov_actual_timing',
        's5':'expected_sale_price',
        's6':'sale_price',
        's7':'bov_date',
        's8':'sale_closing_date',
        's9':'notes',
        's10':'bov_ontime'
    }

