from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeItabaianinhaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2803005"
    name = "se_itabaianinha"
    start_date = date(2017, 1, 2)
    url_uf = "se"
    url_city = "itabaianinha"
