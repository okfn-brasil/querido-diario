from datetime import date

from gazette.spiders.base.base_RG_sites import Base_RgSites


class UFMunicipioSpider(Base_RgSites):
    name = "mg_esmeraldas"
    TERRITORY_ID = "3124104"
    allowed_domains = ["www.esmeraldas.mg.gov.br"]
    start_urls = ["https://www.esmeraldas.mg.gov.br/diario-oficial-eletronico"]
    start_date = date(2024, 12, 9)
    # end_date = date(2021, 12, 10)
