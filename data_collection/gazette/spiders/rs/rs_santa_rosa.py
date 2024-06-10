from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsSantaRosaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4317202"
    name = "rs_santa_rosa"
    city_subdomain = "santarosa"
<<<<<<< HEAD
    start_date = date(2022, 8, 23)
=======
    start_date = date(2024, 5, 17)
>>>>>>> Consolida padrão ATENDE v2 - com alteração de start_date
