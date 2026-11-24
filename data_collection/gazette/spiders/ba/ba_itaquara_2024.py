from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaItaquaraSpider(BaseBrTransparenciaSpider):
    name = "ba_itaquara_2024"
    TERRITORY_ID = "2916708"
    allowed_domains = ["www.itaquara.ba.gov.br", "api.brtransparencia.com.br"]
    start_urls = ["https://www.itaquara.ba.gov.br/diario.html"]
    start_date = date(2019, 1, 1)
