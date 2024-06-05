from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJucurucuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918456"
    name = "ba_jucurucu"
    allowed_domains = ["jucurucu.ba.gov.br"]
    base_url = "https://www.jucurucu.ba.gov.br"
    start_date = date(2006, 1, 26)
