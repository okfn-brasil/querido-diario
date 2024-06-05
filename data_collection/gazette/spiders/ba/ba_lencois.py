from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaLencoisSpider(SaiGazetteSpider):
    TERRITORY_ID = "2919306"
    name = "ba_lencois"
    allowed_domains = ["lencois.ba.gov.br"]
    base_url = "https://www.lencois.ba.gov.br"
    start_date = date(2007, 2, 6)
