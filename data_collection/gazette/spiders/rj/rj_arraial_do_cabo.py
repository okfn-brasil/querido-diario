import datetime

from gazette.spiders.base.instar import BaseInstarSpider


class RjArraialdoCabopider(BaseInstarSpider):
    TERRITORY_ID = "3300258"
    name = "rj_arraial_do_cabo"
    allowed_domains = ["arraial.rj.gov.br"]
    base_url = "https://www.arraial.rj.gov.br/portal/diario-oficial"
    start_date = datetime.date(2019, 2, 7)
