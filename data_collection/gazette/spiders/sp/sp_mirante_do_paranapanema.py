from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMiranteDoParanapanemaSpider(BaseInstarSpider):
    TERRITORY_ID = "3530201"
    name = "sp_mirante_do_paranapanema"
    base_url = "https://www.mirantedoparanapanema.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 5, 7)
