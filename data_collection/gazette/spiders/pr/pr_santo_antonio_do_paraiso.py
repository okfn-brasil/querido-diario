from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrSantoAntonioDoParaisoSpider(BaseInstarSpider):
    TERRITORY_ID = "4124301"
    name = "pr_santo_antonio_do_paraiso"
    allowed_domains = ["pmsantoantoniodoparaiso.pr.gov.br"]
    base_url = "https://www.pmsantoantoniodoparaiso.pr.gov.br/portal/diario-oficial"
    start_date = date(2012, 12, 27)
