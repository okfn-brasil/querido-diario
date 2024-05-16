from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsSaoJoaoDoPolesineSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4318432"
    name = "rs_sao_joao_do_polesine"
    start_date = date(2021, 5, 28)  # Edição 1
    city_subdomain = "saojoaodopolesine"
