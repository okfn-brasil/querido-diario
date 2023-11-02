import datetime

from gazette.spiders.base.instar import BaseInstarSpider


class PrSaoMateusdoSUlSpider(BaseInstarSpider):
    TERRITORY_ID = "4125605"
    name = "pr_sao_mateus_do_sul"
    allowed_domains = ["saomateusdosul.pr.gov.br"]
    base_url = "https://www.saomateusdosul.pr.gov.br/portal/diario-oficial"
    start_date = datetime.date(2010, 12, 10)  # edition_number 01
