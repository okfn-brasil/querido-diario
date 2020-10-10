from gazette.spiders.base import FecamGazetteSpider


class ScPonteSerradaSpider(FecamGazetteSpider):
    name = "sc_ponte_serrada"
    FECAM_QUERY = "cod_entidade:205"
    TERRITORY_ID = "4213401"
