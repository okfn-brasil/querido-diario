from datetime import date

from gazette.spiders.base.base_RG_sites import Base_RgSites


class UFMunicipioSpider(Base_RgSites):
    name = "rj_cantagalo"
    TERRITORY_ID = "3301108"
    allowed_domains = ["www.cantagalo.rj.gov.br"]
    start_urls = ["https://www.cantagalo.rj.gov.br/transparencia/diario-oficial"]
    start_date = date(2024, 10, 1)
    end_date = date(2024, 12, 10)
