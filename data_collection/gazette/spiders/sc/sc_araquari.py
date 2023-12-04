from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class ScAraquariSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4201307"
    name = "sc_araquari"
    start_date = date(2018, 1, 2)  # Edição 1
    city_subdomain = "araquari"
