from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPlanaltinoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2924900"
    name = "ba_planaltino"
    allowed_domains = ["planaltino.ba.gov.br"]
    base_url = "https://www.planaltino.ba.gov.br"
    start_date = date(2008, 5, 30)
