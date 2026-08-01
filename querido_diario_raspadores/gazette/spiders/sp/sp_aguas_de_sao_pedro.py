from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAguasDeSaoPedroSpider(BaseInstarSpider):
    TERRITORY_ID = "3500600"
    name = "sp_aguas_de_sao_pedro"
    base_url = "https://www.aguasdesaopedro.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 5, 18)
