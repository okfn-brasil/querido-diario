from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaRioRealSpider(BaseBrTransparenciaSpider):
    name = "ba_rio_real"
    TERRITORY_ID = "2927002"
    allowed_domains = ["cmriorealba.brtransparencia.com.br"]
    start_urls = ["https://http://cmriorealba.brtransparencia.com.br/diario.html"]
    start_date = date(2022, 12, 29)
    br_tranparencia_entity = "45ae0af7-71a7-436e-9a8e-d41a68215062"
    br_tranparencia_code = "COD_ENT_CM208"
    power = "legislative"
