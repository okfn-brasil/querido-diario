from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsCandelariaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4304200"
    name = "rs_candelaria"
    city_subdomain = "candelaria"
<<<<<<< HEAD
    start_date = date(2023, 5, 7)
=======
    start_date = date(2024, 5, 7)
>>>>>>> Consolida padrão ATENDE v2 - com alteração de start_date
