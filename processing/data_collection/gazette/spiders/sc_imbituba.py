from gazette.spiders.base import FecamGazetteSpider


class ScImbitubaSpider(FecamGazetteSpider):
    name = "sc_imbituba"
    FECAM_QUERY = 'cod_entidade:116'
    TERRITORY_ID = "4207304"