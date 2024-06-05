from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaTaperoaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2931202"
    name = "ba_taperoa"
    allowed_domains = ["taperoa.ba.gov.br"]
    base_url = "https://www.taperoa.ba.gov.br"
    start_date = date(2007, 7, 11)
