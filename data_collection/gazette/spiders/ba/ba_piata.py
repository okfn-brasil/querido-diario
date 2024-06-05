from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPiataSpider(SaiGazetteSpider):
    TERRITORY_ID = "2924306"
    name = "ba_piata"
    allowed_domains = ["piata.ba.gov.br"]
    base_url = "https://www.piata.ba.gov.br"
    start_date = date(2017, 1, 5)
