from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIguaiSpider(SaiGazetteSpider):
    TERRITORY_ID = "2913507"
    name = "ba_iguai"
    allowed_domains = ["iguai.ba.gov.br"]
    base_url = "https://www.iguai.ba.gov.br"
    start_date = date(2005, 3, 24)
