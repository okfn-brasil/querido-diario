from gazette.spiders.base import FecamGazetteSpider


class ScPenhaSpider(FecamGazetteSpider):
    name = "sc_penha"
    FECAM_QUERY = "cod_entidade:195"
    TERRITORY_ID = "4212502"
