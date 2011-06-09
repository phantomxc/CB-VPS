from webpy.dark import *
from storm.locals import *

class Company(Storm):
    """
    A company can have many divisions with many regions
    """
    __storm_table__ = 'company'
    
    # ID's
    id = Int(primary=True)
    client_id = Int()
    
    #Text
    title = Unicode(validator=unicoder)
    
    #References
    divisions = ReferenceSet(id, 'CompanyDivision.company_id')
    
class CompanyDivision(Storm):
    """
    A Division can only have one company but multiple regions
    """
    __storm_table__ = 'divisions'

    # ID's
    id = Int(primary=True)
    company_id = Int()
    
    #Text
    title = Unicode(validator=unicoder)
    
    #References
    company = Reference(company_id, 'Company.id')
    regions = ReferenceSet(id, 'CompanyRegion.division_id')

class CompanyRegion(Storm):
    """
    A region can only have one division
    """
    __storm_table__ = 'regions'
    
    #ID's
    id = Int(primary=True)
    division_id = Int()
    
    #Text
    title = Unicode(validator=unicoder)

    #References
    division = Reference(division_id, 'CompanyDivision.id')


