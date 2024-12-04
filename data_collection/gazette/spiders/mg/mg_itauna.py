from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgItaunaSpider(BaseInstarSpider):
    TERRITORY_ID = "3133808"
    name = "mg_itauna"
    allowed_domains = ["itauna.mg.gov.br"]
    base_url = "https://www.itauna.mg.gov.br/portal/diario-oficial"
    start_date = date(2013, 6, 20)
