from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaCandeiasSpider(BaseBrTransparenciaSpider):
    name = "ba_candeias"
    TERRITORY_ID = "2906501"
    allowed_domains = ["www.camaraibicoara.ba.gov.br", "api.brtransparencia.com.br"]
    start_urls = ["https://www.camaraibicoara.ba.gov.br/diario.html"]
    start_date = date(2022, 12, 29)
    power = "legislative"
