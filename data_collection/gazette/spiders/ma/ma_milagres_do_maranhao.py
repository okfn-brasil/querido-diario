import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaMilagresDoMaranhao(BaseSiganetSpider):
    TERRITORY_ID = "2106672"
    name = "ma_milagres_do_maranhao"
    start_date = datetime.date(2016, 1, 7)
    allowed_domains = ["milagresdomaranhao.ma.gov.br"]
    BASE_URL = "https://milagresdomaranhao.ma.gov.br/diario/diario"
