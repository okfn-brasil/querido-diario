from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class AlSaoLuisDoQuitundeSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2708501"
    name = "al_sao_luis_do_quitunde"
    url_uf = "al"
    url_city = "saoluisdoquitunde"
    start_date = date(2020, 7, 29)
