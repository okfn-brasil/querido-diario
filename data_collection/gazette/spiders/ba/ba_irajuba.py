from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIrajubaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2914208"
    name = "ba_irajuba"
    allowed_domains = ["irajuba.ba.gov.br"]
    base_url = "https://www.irajuba.ba.gov.br"
    start_date = date(2006, 12, 14)
