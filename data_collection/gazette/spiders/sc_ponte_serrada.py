from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPonteSerradaSpider(FecamGazetteSpider):
    name = "sc_ponte_serrada"
    FECAM_QUERY = "cod_entidade:205"
    TERRITORY_ID = "4213401"
