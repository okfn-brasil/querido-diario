from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJussariSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918555"
    name = "ba_jussari"
    allowed_domains = ["jussari.ba.gov.br"]
    base_url = "https://www.jussari.ba.gov.br"
    start_date = date(2008, 2, 28)
