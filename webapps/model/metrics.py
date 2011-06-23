from storm.locals import *
from webpy.dark import *

from model.users import *


class Metrics(Storm):
    """
    I represent a clients metrics
    """

    __storm_table__ = "metrics"

    #IDs
    id = Int(primary=True)
    client_id = Int(validator=intify)

    #Text
    field = Unicode(validator=unicoder)
    title = Unicode(validator=unicoder)
    operator = Unicode(validator=unicoder)
    
    #Numbers
    warn_amount = Decimal(validator=decimify)
    bad_amount = Decimal(validator=decimify)

    @classmethod
    def createMetrics(self, client_id):
        store = get_store()
        client = store.find(Client, Client.id == client_id).one()

        field_list = [
            'avg_survey_score', 'avg_value_add',
            'avg_days_business_terms', 'avg_days_deal_close', 'market_survey_ontime',
            'rfp_ontime', 'avg_time_on_market', 'survey_resp_ratio',
            'bov_on_time', 'meet_bov_timing', 'meet_bov_recovery',
            'avg_days_loi_to_deal_close'
        ]

        for f in field_list:
            m = store.add(Metrics())
            m.client_id = client.id
            m.field = f
            store.commit()


