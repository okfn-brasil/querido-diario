from gazette.spiders.base import FecamGazetteSpider


class ScIporaDoOesteSpider(FecamGazetteSpider):
    name = "sc_ipora_do_oeste"
    FECAM_QUERY = 'cod_entidade:121'
    TERRITORY_ID = "4207650"