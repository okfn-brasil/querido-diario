from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgVarzeaDaPalmaSpider(BaseInstarSpider):
    TERRITORY_ID = "3170800"
    name = "mg_varzea_da_palma"
    allowed_domains = ["varzeadapalma.mg.gov.br"]
    base_url = "https://www.varzeadapalma.mg.gov.br/portal/diario-oficial"
    start_date = date(2022, 9, 30)
