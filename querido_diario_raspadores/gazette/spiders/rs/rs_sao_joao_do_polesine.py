from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsSaoJoaoDoPolesineSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4318432"
    name = "rs_sao_joao_do_polesine"
    city_subdomain = "saojoaodopolesine"
    start_date = date(2021, 5, 28)
