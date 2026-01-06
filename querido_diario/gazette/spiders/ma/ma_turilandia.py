import datetime as dt

from gazette.spiders.base.administracaopublica import BaseAdministracaoPublicaSpider


class MaTurilandiaSpider(BaseAdministracaoPublicaSpider):
    TERRITORY_ID = "2112456"
    name = "ma_turilandia"
    start_date = dt.date(2021, 3, 11)
    token = "9664abfc624b73571a05e874f98fd6d114834924"
