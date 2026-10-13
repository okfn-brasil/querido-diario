from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeItaporangaDajudaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2803203"
    name = "se_itaporanga_dajuda"
    url_uf = "se"
    url_city = "itaporangadajuda"
    start_date = date(2017, 1, 26)
