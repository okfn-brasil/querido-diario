from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAndorinhaSpider(BaseSaiSpider):
    TERRITORY_ID = "2901353"
    name = "ba_andorinha"
    allowed_domains = ["andorinha.ba.gov.br"]
    base_url = "https://www.andorinha.ba.gov.br"
    start_date = date(2013, 1, 2)
