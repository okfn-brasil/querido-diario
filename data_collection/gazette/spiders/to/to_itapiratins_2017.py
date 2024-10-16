from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToItapiratinsSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1710904"
    name = "to_itapiratins_2017"
    allowed_domains = ["itapiratins.diariooficialbr.com.br"]
    BASE_URL = "https://itapiratins.diariooficialbr.com.br"
    start_date = date(2017, 4, 3)
    end_date = date(
        2024, 1, 10
    )  # Alert: Discontinued this date! (Verified in 2024-09-24)
