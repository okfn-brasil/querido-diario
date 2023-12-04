from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrCastroSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4104907"
    name = "pr_castro"
    start_date = date(2010, 6, 4)  # Edição 222
    city_subdomain = "castro"
