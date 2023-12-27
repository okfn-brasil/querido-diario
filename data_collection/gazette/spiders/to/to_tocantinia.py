import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficinalBRSpider


class ToAguiarnopolisSpider(BaseDiarioOficinalBRSpider):
    TERRITORY_ID = "1721109"
    name = "to_tocantinia"
    allowed_domains = ["tocantinia.diariooficialbr.com.br"]
    start_date = datetime.date(2017, 3, 21)
    city_domain = "tocantinia.diariooficialbr.com.br"
    url_base = "https://tocantinia.diariooficialbr.com.br"
