from gazette.spiders.base import FecamGazetteSpider


class ScCampoAlegreSpider(FecamGazetteSpider):
    name = "sc_campo_alegre"
    FECAM_QUERY = "cod_entidade:57"
    TERRITORY_ID = "4203303"
