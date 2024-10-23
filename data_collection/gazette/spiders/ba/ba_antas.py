from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAntasSpider(BaseSaiSpider):
    TERRITORY_ID = "2901601"
    name = "ba_antas"
    allowed_domains = ["antas.ba.gov.br"]
    base_url = "https://www.antas.ba.gov.br"
    start_date = date(2013, 2, 21)
