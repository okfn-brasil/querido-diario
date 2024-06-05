from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgCarmoDoRioClaroSpider(BaseInstarSpider):
    TERRITORY_ID = "3114402"
    name = "mg_carmo_do_rio_claro"
    allowed_domains = ["carmodorioclaro.mg.gov.br"]
    base_url = "https://www.carmodorioclaro.mg.gov.br/portal/diario-oficial"
    start_date = date(2021, 5, 14)
