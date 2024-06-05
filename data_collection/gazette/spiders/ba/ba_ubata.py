from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaUbataSpider(SaiGazetteSpider):
    TERRITORY_ID = "2932309"
    name = "ba_ubata"
    allowed_domains = ["ubata.ba.gov.br"]
    base_url = "https://www.ubata.ba.gov.br"
    start_date = date(2005, 5, 30)
