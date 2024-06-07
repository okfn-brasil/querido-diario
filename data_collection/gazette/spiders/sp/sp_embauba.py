from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpEmbaubaSpider(DospGazetteSpider):
    TERRITORY_ID = "3514957"
    name = "sp_embauba"
    code = 4816
    start_date = date(2021, 6, 2)
