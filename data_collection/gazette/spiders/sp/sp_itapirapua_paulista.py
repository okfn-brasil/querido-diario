from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpItapirapuaPaulistaSpider(BaseInstarSpider):
    TERRITORY_ID = "3522653"
    name = "sp_itapirapua_paulista"
    allowed_domains = ["itapirapuapaulista.sp.gov.br"]
    base_url = "https://www.itapirapuapaulista.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 5, 24)
