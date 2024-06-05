from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIramaiaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2914307"
    name = "ba_iramaia"
    allowed_domains = ["iramaia.ba.gov.br"]
    base_url = "https://www.iramaia.ba.gov.br"
    start_date = date(2005, 10, 11)
