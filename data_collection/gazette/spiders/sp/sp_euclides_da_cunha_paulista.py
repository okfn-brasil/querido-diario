from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpEuclidesDaCunhaPaulistaSpider(DospGazetteSpider):
    TERRITORY_ID = "3515350"
    name = "sp_euclides_da_cunha_paulista"
    code = 4826
    start_date = date(2018, 10, 23)
