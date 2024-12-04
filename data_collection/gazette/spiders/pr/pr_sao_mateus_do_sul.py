from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrSaoMateusDoSulSpider(BaseInstarSpider):
    TERRITORY_ID = "4125605"
    name = "pr_sao_mateus_do_sul"
    allowed_domains = ["saomateusdosul.pr.gov.br"]
    base_url = "https://www.saomateusdosul.pr.gov.br/portal/diario-oficial"
    start_date = date(2010, 12, 10)
