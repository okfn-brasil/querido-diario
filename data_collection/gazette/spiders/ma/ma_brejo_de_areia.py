import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaBrejoDeAreia(BaseSiganetSpider):
    TERRITORY_ID = "2102150"
    name = "ma_brejo_de_areia"
    start_date = datetime.date(2020, 7, 21)
    allowed_domains = ["brejodeareia.ma.gov.br"]
    BASE_URL = "https://brejodeareia.ma.gov.br/diario/diario"
