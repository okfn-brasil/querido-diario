from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrCampoLargoSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4104204"
    name = "pr_campo_largo"
    start_date = date(2006, 1, 20)  # Edição 1
    city_subdomain = "campolargo"
