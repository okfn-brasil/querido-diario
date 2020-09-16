from gazette.spiders.base import FecamGazetteSpider


class ScAguaDoceSpider(FecamGazetteSpider):
    name = "sc_agua_doce"
    FECAM_QUERY = "cod_entidade:8"
    TERRITORY_ID = "4200408"
