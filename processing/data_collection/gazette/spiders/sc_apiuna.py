from gazette.spiders.base import FecamGazetteSpider


class ScApiunaSpider(FecamGazetteSpider):
    name = "sc_apiuna"
    FECAM_QUERY = "cod_entidade:19"
    TERRITORY_ID = "4201257"
