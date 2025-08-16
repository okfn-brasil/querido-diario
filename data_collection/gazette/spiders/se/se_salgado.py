from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeSalgadoSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2806206"
    name = "se_salgado"
    url_uf = "se"
    url_city = "salgado"
    start_date = date(2023, 1, 2)
