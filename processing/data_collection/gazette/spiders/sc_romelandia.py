from gazette.spiders.base import FecamGazetteSpider


class ScRomelandiaSpider(FecamGazetteSpider):
    name = "sc_romelandia"
    FECAM_QUERY = "cod_entidade:226"
    TERRITORY_ID = "4215208"
