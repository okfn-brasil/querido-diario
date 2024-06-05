from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMiranteSpider(SaiGazetteSpider):
    TERRITORY_ID = "2921450"
    name = "ba_mirante"
    allowed_domains = ["mirante.ba.gov.br"]
    base_url = "https://www.mirante.ba.gov.br"
    start_date = date(2006, 2, 11)
