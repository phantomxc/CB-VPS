from webpy.dark import *
from storm.locals import *

class Transaction(Storm):
    """
    I represent a client transaction
    """
    __storm_table__ = "transactions"
    # IDs    
    id = Int(primary=True)
    client_id = Int()
    company_id = Int()
    division_id = Int()
    region_id = Int()
    area_id = Int()
    trans_manager = Int()
    property_id = Int()
    survey_id = Int()
    
    #Text
    client_trans_manager = Unicode(validator=unicoder)
    trans_type = Unicode(validator=unicoder)
    
    #Dates
    engage_date = Date()
    rebc_entry_date = Date()    
    
    #References
    prop = Reference(property_id, 'Property.id')
    survey = Reference(survey_id, 'Zoom.id')
    

class Acquisition(Transaction):
    """
    I am a type of transaction
    """
    __storm_table__ = "acquisition"

    #IDs
    id = Int(primary=True)
    trans_id = Int()
    
    # Numbers
    old_sqft = Int()
    new_sqft = Int()
    value_add = Int()

    # Dates
    market_survey_date = Date()

    # Bools    
    market_survey = Bool()

    # NEW LEASE / LEASE EXTENSION
    lease_execution_date = Date()
    rfp_on_time = Bool()
    average_base_rent = Decimal()
    
    # PURCHASE   
    purchase_price = Decimal()
    purchase_close_date = Date()
    
    # References
    transaction = Reference(trans_id, 'Transaction.id')

class Disposition(Transaction):
    """
    I am a type of transaction
    """
    __storm_table__ = "disposition"

    #IDs
    id = Int(primary=True)
    trans_id = Int()

    # Numbers
    sqft = Int()
    bov_expected_timing
    bov_actual_timing

    # Dates
    bov_date = Date

    # Bools

    # Text
    notes = Unicode(validator=unicoder)

    
    #Sublease
    expected_recovery = Decimal()
    actual_recovery = Decimal()
    sublease_execution_date = Date()
    
    #Lease Termination
    expected_savings = Decimal()
    total_savings = Decimal()
    ltd_execution_date = Date()

    
    #Sale
    expected_sale_price = Decimal()
    sale_price = Decimal()
    sale_closing_date = Date()


    # References
    transaction = Reference(trans_id, 'Transaction.id')
    
