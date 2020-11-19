from gazette.spiders.base import FecamGazetteSpider


class ScPauloLopesSpider(FecamGazetteSpider):
    name = "sc_paulo_lopes"
    FECAM_QUERY = "cod_entidade:193"
    TERRITORY_ID = "4212304"
