from gazette.spiders.base import FecamGazetteSpider


class ScAguasFriasSpider(FecamGazetteSpider):
    name = "sc_aguas_frias"
    FECAM_QUERY = "cod_entidade:10"
    TERRITORY_ID = "4200556"
