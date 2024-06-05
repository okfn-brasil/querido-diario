from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaHeliopolisSpider(SaiGazetteSpider):
    TERRITORY_ID = "2911857"
    name = "ba_heliopolis"
    allowed_domains = ["heliopolis.ba.gov.br"]
    base_url = "https://www.heliopolis.ba.gov.br"
    start_date = date(2009, 2, 17)
