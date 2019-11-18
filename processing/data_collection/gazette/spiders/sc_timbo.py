from gazette.spiders.base import FecamGazetteSpider


class ScTimboSpider(FecamGazetteSpider):
    name = "sc_timbo"
    FECAM_QUERY = 'cod_entidade:272'
    TERRITORY_ID = "4218202"