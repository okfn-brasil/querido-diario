from gazette.spiders.base import FecamGazetteSpider


class ScAnitaGaribaldiSpider(FecamGazetteSpider):
    name = "sc_anita_garibaldi"
    FECAM_QUERY = "cod_entidade:16"
    TERRITORY_ID = "4201000"
