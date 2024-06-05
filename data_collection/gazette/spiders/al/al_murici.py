from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class AlMuriciSpider(SaiGazetteSpider):
    TERRITORY_ID = "2705507"
    name = "al_murici"
    allowed_domains = ["murici.al.gov.br"]
    base_url = "https://www.murici.al.gov.br"
    start_date = date(2016, 8, 25)
