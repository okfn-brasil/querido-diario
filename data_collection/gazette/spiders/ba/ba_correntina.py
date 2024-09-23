from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaCorrentinaSpider(BaseSaiSpider):
    TERRITORY_ID = "2909307"
    name = "ba_correntina"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/correntina"
    start_date = date(2007, 11, 30)
