from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsSantaRosaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4317202"
    name = "rs_santa_rosa"
    start_date = date(2022, 8, 23)  # Edição 1
    city_subdomain = "santarosa"
