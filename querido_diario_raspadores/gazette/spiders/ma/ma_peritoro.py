import datetime as dt

from gazette.spiders.base.administracaopublica import BaseAdministracaoPublicaSpider


class MaPeritoroSpider(BaseAdministracaoPublicaSpider):
    TERRITORY_ID = "2108454"
    name = "ma_peritoro"
    start_date = dt.date(2017, 1, 2)
    token = "9de645b503b922df799865ffcb07a6ec7b9cb53e"
