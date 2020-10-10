from gazette.spiders.base import FecamGazetteSpider


class ScAnitapolisSpider(FecamGazetteSpider):
    name = "sc_anitapolis"
    FECAM_QUERY = "cod_entidade:17"
    TERRITORY_ID = "4201109"
