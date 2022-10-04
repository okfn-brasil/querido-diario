from datetime import date

from gazette.spiders.base import BaseGazetteSpider


class MgEsmeraldasSpider(BaseGazetteSpider):
    name = "mg_esmeraldas"
    allowed_domains = ["esmeraldas.mg.gov.br"]
    start_date = date(2021, 8, 12)
    url_base = "https://www.esmeraldas.mg.gov.br/diario-oficial-eletronico"
    TERRITORY_ID = "3124104"
