import re

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
                self.update_value(record)
                self.update_contracted(record)
            record.is_parsed = True

    def update_value(self, record):
        keywords = ['VALOR', 'ORÇAMENTO', 'PREÇO']
        value_str = self._value_for_partial_key(record.data, keywords)
        if value_str:
            if value_str.startswith('R$ 660,00,00'):
                value_str = 'R$ 660,00'
            matches = re.search(r'R\$ ?([\d\.,]+)', value_str)
            if matches:
                value_str = matches[1].replace('.', '').replace(',', '.')
                if value_str[-1] == '.':
                    value_str = value_str[:-1]
                record.value = float(value_str)

    def update_contracted(self, record):
        keywords = ['CONTRATAD', 'EMPRESA', 'FORNECEDOR', 'LOCADOR']
        record.contracted = self._value_for_partial_key(record.data, keywords)

    def _value_for_partial_key(self, dictionary, keywords):
        for key, value in dictionary.items():
            for partial_key in keywords:
                if partial_key in key:
                    return value
