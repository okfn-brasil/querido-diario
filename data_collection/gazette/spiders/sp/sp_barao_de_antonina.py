from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpBaraoDeAntoninaSpider(BaseInstarSpider):
    TERRITORY_ID = "3505005"
    name = "sp_barao_de_antonina"
    allowed_domains = ["baraodeantonina.sp.gov.br"]
    base_url = "https://www.baraodeantonina.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 1, 3)
