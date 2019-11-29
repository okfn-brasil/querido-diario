from gazette.spiders.base import FecamGazetteSpider


class ScGravatalSpider(FecamGazetteSpider):
    name = "sc_gravatal"
    FECAM_QUERY = "cod_entidade:103"
    TERRITORY_ID = "4206207"
