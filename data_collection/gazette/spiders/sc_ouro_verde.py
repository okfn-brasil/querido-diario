from gazette.spiders.base import FecamGazetteSpider


class ScOuroVerdeSpider(FecamGazetteSpider):
    name = "sc_ouro_verde"
    FECAM_QUERY = "cod_entidade:182"
    TERRITORY_ID = "4211850"
