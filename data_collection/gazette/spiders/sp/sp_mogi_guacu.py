from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMogiGuacuSpider(DospGazetteSpider):
    TERRITORY_ID = "3530706"
    name = "sp_mogi_guacu"
    code = 4995
    start_date = date(2022, 1, 20)
