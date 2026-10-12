from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeNossaSenhoraDaGloriaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804508"
    name = "se_nossa_senhora_da_gloria"
    url_uf = "se"
    url_city = "nossasenhoradagloria"
    start_date = date(2022, 2, 10)
