from gazette.spiders.base import FecamGazetteSpider


class ScPinhalzinhoSpider(FecamGazetteSpider):
    name = "sc_pinhalzinho"
    FECAM_QUERY = "cod_entidade:198"
    TERRITORY_ID = "4212908"
