from gazette.spiders.base.fecam import FecamGazetteSpider


class ScLagunaSpider(FecamGazetteSpider):
    name = "sc_laguna"
    FECAM_QUERY = "cod_entidade:146"
    TERRITORY_ID = "4209409"
