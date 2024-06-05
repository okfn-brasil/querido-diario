from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRibeiraDoAmparoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2926509"
    name = "ba_ribeira_do_amparo"
    allowed_domains = ["ribeiradoamparo.ba.gov.br"]
    base_url = "https://www.ribeiradoamparo.ba.gov.br"
    start_date = date(2007, 12, 13)
