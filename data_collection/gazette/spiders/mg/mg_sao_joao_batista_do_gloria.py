from datetime import date

from gazette.spiders.base.base_RG_sites import Base_RgSites


class UFMunicipioSpider(Base_RgSites):
    name = "mg_sao_joao_batista_do_gloria"
    TERRITORY_ID = "3162203"
    allowed_domains = ["www.gloria.mg.gov.br"]
    start_urls = ["https://www.gloria.mg.gov.br/diario-oficial"]
    start_date = date(2019, 1, 3)
