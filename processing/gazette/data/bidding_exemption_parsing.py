from database import MUNICIPALITIES
from database.models import BiddingExemption
from gazette import locations


class BiddingExemptionParsing:

    def __init__(self, session):
        self.session = session

    def condition(self):
        return 'is_parsed = FALSE'

    def update(self, records):
        for record in records:
            municipality = MUNICIPALITIES.get(record.gazette.municipality_id)
            if municipality:
                record.object = record.data.get('OBJETO')
            record.is_parsed = True
