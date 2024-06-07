from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPromissaoSpider(DospGazetteSpider):
    TERRITORY_ID = "3541604"
    name = "sp_promissao"
    code = 5117
    start_date = date(2015, 7, 30)
