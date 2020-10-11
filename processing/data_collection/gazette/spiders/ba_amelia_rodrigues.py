from datetime import date
from gazette.spiders.base import ImprensaOficialSpider


class BaAmeliaRodriguesSpider(ImprensaOficialSpider):

    name = "ba_amelia_rodrigues"
    allowed_domains = ["pmameliarodriguesba.imprensaoficial.org"]
    start_date = date(2020, 9, 1)  # FIXME
    url_base = "http://pmameliarodriguesba.imprensaoficial.org/{}/"
    TERRITORY_ID = "2901106"
