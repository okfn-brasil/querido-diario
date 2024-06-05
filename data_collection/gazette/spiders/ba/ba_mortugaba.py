from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMortugabaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2921807"
    name = "ba_mortugaba"
    allowed_domains = ["mortugaba.ba.gov.br"]
    base_url = "https://www.mortugaba.ba.gov.br"
    start_date = date(2007, 1, 5)
