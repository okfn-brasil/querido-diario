from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeNossaSenhoraDasDoresSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804607"
    name = "se_nossa_senhora_das_dores"
    url_uf = "se"
    url_city = "nossasenhoradasdores"
    start_date = date(2017, 1, 2)
