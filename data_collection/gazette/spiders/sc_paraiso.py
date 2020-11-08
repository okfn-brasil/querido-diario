from gazette.spiders.base import FecamGazetteSpider


class ScParaisoSpider(FecamGazetteSpider):
    name = "sc_paraiso"
    FECAM_QUERY = "cod_entidade:190"
    TERRITORY_ID = "4212239"
