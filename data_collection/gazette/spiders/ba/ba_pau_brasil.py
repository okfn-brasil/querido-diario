from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPauBrasilSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923902"
    name = "ba_pau_brasil"
    allowed_domains = ["paubrasil.ba.gov.br"]
    base_url = "https://www.paubrasil.ba.gov.br"
    start_date = date(2007, 3, 8)
