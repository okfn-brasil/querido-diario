from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpParanapanemaSpider(BaseInstarSpider):
    TERRITORY_ID = "3535804"
    name = "sp_paranapanema"
    allowed_domains = ["paranapanema.sp.gov.br"]
    base_url = "https://www.paranapanema.sp.gov.br/portal/diario-oficial"
    start_date = date(2018, 9, 17)
