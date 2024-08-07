from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrCampoLargoSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4104204"
    name = "pr_campo_largo"
    city_subdomain = "campolargo"
    start_date = date(2006, 1, 20)
