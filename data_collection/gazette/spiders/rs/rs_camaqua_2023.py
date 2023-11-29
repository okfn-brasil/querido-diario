from datetime import date

from gazette.spiders.base.atende import BaseAtendeT1Spider


class RsCamaqua2023Spider(BaseAtendeT1Spider):
    TERRITORY_ID = "4303509"
    name = "rs_camaqua_2023"
    start_date = date(2023, 7, 20)  # Edição 333
    city_subdomain = "camaqua"
    perm_url = "diario-oficial"
    start_edition = 333
