import datetime as dt

from gazette.spiders.base.administracaopublica import BaseAdministracaoPublicaSpider


class MaNovaIorqueSpider(BaseAdministracaoPublicaSpider):
    TERRITORY_ID = "2107308"
    name = "ma_nova_iorque"
    start_date = dt.date(2017, 2, 15)
    token = "4f1cf16edf5d73feaad4fec2a03c7c9e1cf536aa"
