from gazette.spiders.base import FecamGazetteSpider


class ScUrupemaSpider(FecamGazetteSpider):
    name = "sc_urupema"
    FECAM_QUERY = "cod_entidade:284"
    TERRITORY_ID = "4218954"
