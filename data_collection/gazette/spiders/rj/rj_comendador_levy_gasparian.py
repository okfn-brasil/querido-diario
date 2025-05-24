from datetime import date

from gazette.spiders.base.ptio import BasePtioSpider


class RjComendadorLevyGasparianSpider(BasePtioSpider):
    name = "rj_comendador_levy_gasparian"
    TERRITORY_ID = "3300951"
    BASE_URL = (
        "http://rj.portaldatransparencia.com.br/prefeitura/comendadorlevygasparian/"
    )
    start_date = date(2013, 11, 26)
