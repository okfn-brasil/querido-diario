from gazette.spiders.base import FecamGazetteSpider


class ScBalnearioPicarrasSpider(FecamGazetteSpider):
    name = "sc_balneario_picarras"
    FECAM_QUERY = "cod_entidade:33"
    TERRITORY_ID = "4212809"
