from gazette.spiders.base import FecamGazetteSpider


class ScRioRufinoSpider(FecamGazetteSpider):
    name = "sc_rio_rufino"
    FECAM_QUERY = "cod_entidade:223"
    TERRITORY_ID = "4215059"
