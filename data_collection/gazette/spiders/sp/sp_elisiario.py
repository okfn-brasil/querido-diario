from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpElisiarioSpider(DospGazetteSpider):
    TERRITORY_ID = "3514924"
    name = "sp_elisiario"
    code = 4815
    start_date = date(2019, 2, 15)
