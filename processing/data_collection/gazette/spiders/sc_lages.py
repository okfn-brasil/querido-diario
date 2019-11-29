from gazette.spiders.base import FecamGazetteSpider


class ScLagesSpider(FecamGazetteSpider):
    name = "sc_lages"
    FECAM_QUERY = "cod_entidade:145"
    TERRITORY_ID = "4209300"
