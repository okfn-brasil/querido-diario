import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaNinaRodriguesSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2107209"
    name = "ma_nina_rodrigues"
    start_date = datetime.date(2019, 2, 7)
    allowed_domains = ["transparencia.ninarodrigues.ma.gov.br"]
    BASE_URL = (
        "https://transparencia.ninarodrigues.ma.gov.br/acessoInformacao/diario/diario"
    )
