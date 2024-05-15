from datetime import date

from gazette.spiders.base.atende_layoutdois import BaseAtendeL2Spider


class RsDoisIrmaosSpider(BaseAtendeL2Spider):
    TERRITORY_ID = "4306403"
    name = "rs_dois_irmaos"
    start_date = date(2020, 1, 7)  # Edição 1
    city_subdomain = "doisirmaos"
