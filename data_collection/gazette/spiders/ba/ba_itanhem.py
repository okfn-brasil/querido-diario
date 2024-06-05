from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class BaItanhemSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2916005"
    name = "ba_itanhem"
    url_uf = "ba"
    url_city = "itanhem"
    start_date = date(2021, 1, 5)
