from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsEstrelaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4307807"
    name = "rs_estrela"
    start_date = date(2021, 3, 29)  # Edição 1
    city_subdomain = "estrela"
