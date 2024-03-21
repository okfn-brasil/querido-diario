from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrCampoMouraoSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4104303"
    name = "pr_campo_mourao"
    start_date = date(2012, 2, 3)  # Edição 1511
    city_subdomain = "campomourao"
