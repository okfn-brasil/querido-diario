from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeItabaianaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2802908"
    name = "se_itabaiana"
    url_uf = "se"
    url_city = "itabaiana"
    start_date = date(2023, 1, 2)
