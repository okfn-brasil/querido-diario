import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaSaoJoseDosBasiliosSpider(BaseSiganetSpider):
    TERRITORY_ID = "2111250"
    name = "ma_sao_jose_dos_basilios"
    start_date = datetime.date(2015, 11, 27)
    allowed_domains = ["transparencia.saojosedosbasilios.ma.gov.br"]
    BASE_URL = "https://transparencia.saojosedosbasilios.ma.gov.br/acessoInformacao/diario/diario"
