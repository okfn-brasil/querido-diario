from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeDivinaPastoraSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2802007"
    name = "se_divina_pastora"
    url_uf = "se"
    url_city = "divinapastora"
    start_date = date(2019, 1, 10)
