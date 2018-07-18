import re

from database import PARSABLE_TERRITORIES
from database.models import BiddingExemption
from gazette import locations


class BiddingExemptionParsing:
    CNPJ_REGEXP = r"([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2})"
    VALUE_REGEXP = r"R\$ ?([\d\.,]+)"

    def __init__(self, session):
        self.session = session

    def condition(self):
        return "is_parsed = FALSE"

    def update(self, records):
        for record in records:
            territory = PARSABLE_TERRITORIES.get(record.gazette.territory_id)
            if territory:
                self.update_object(record)
                self.update_value(record)
                self.update_contracted(record)
                self.update_contracted_code(record)
                record.is_parsed = True

    def update_object(self, record):
        value_str = record.data.get("OBJETO")
        if value_str and ("objeto" in value_str):
            value_str = value_str[value_str.index("objeto") :]
            value_str = value_str.split(" ")[1:]
            if value_str[:3] == ["a", "aquisição", "de"]:
                value_str = value_str[3:]
            elif value_str[:2] == ["aquisição", "de"]:
                value_str = value_str[2:]
            value_str = " ".join(value_str)
        record.object = value_str

    def update_value(self, record):
        keywords = ["VALOR", "ORÇAMENTO", "PREÇO"]
        value_str = self._value_for_partial_key(record.data, keywords)
        if not value_str:
            value_str = record.source_text
        elif value_str.startswith("R$ 660,00,00"):
            value_str = "R$ 660,00"
        matches = re.findall(self.VALUE_REGEXP, value_str)
        if matches and (len(matches) == 1):
            value_str = matches[0].replace(".", "").replace(",", ".")
            if value_str[-1] == ".":
                value_str = value_str[:-1]
            record.value = float(value_str)

    def update_contracted(self, record):
        keywords = ["CONTRATAD", "EMPRESA", "FORNECEDOR", "LOCADOR"]
        record.contracted = self._value_for_partial_key(record.data, keywords)

    def update_contracted_code(self, record):
        value_str = record.contracted or ""
        matches = re.findall(self.CNPJ_REGEXP, value_str)
        if not matches:
            matches = re.findall(self.CNPJ_REGEXP, record.source_text)

        if matches and (len(matches) == 1):
            record.contracted_code = re.sub(r"\D", "", matches[0])

    def _value_for_partial_key(self, dictionary, keywords):
        for key, value in dictionary.items():
            for partial_key in keywords:
                if partial_key in key:
                    return value
