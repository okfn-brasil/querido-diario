from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItagibaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2915205"
    name = "ba_itagiba"
    allowed_domains = ["itagiba.ba.gov.br"]
    base_url = "https://www.itagiba.ba.gov.br"
    start_date = date(2005, 3, 30)
