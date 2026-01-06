from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeIlhaDasFloresSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2802700"
    name = "se_ilha_das_flores"
    url_uf = "se"
    url_city = "ilhadasflores"
    start_date = date(2017, 1, 11)
