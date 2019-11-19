from gazette.spiders.base import FecamGazetteSpider


class ScImaruiSpider(FecamGazetteSpider):
    name = "sc_imarui"
    FECAM_QUERY = 'cod_entidade:115'
    TERRITORY_ID = "4207205"