from datetime import date

from gazette.spiders.base.rgsites import BaseRgSites


class MgEsmeraldasSpider(BaseRgSites):
    name = "mg_esmeraldas"
    TERRITORY_ID = "3124104"
    allowed_domains = ["www.esmeraldas.mg.gov.br"]
    BASE_URL = "https://www.esmeraldas.mg.gov.br/diario-oficial-eletronico"
    start_date = date(2021, 6, 12)
