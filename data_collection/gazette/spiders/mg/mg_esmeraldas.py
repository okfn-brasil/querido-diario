from datetime import date

from gazette.spiders.base.rgsites import BaseRgSites


class MgEsmeraldasSpider(BaseRgSites):
    name = "mg_esmeraldas"
    TERRITORY_ID = "3124104"
    allowed_domains = ["www.esmeraldas.mg.gov.br"]
    BASE_URL = "https://www.esmeraldas.mg.gov.br/diario-oficial-eletronico"
<<<<<<< HEAD
<<<<<<< HEAD
    start_date = date(2021, 8, 12)
=======
    start_date = date(2021, 6, 12)
>>>>>>> 2d239c1 (Cria spider base rgsites #1245)
=======
    start_date = date(2021, 8, 12)
>>>>>>> 30a1d25 (ajeitando nome da classe e data inicial)
