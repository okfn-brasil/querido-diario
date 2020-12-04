from gazette.spiders.base.fecam import FecamGazetteSpider


class ScGravatalSpider(FecamGazetteSpider):
    name = "sc_gravatal"
    FECAM_QUERY = "cod_entidade:103"
    TERRITORY_ID = "4206207"
