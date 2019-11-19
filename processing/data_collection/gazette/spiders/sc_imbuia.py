from gazette.spiders.base import FecamGazetteSpider


class ScImbuiaSpider(FecamGazetteSpider):
    name = "sc_imbuia"
    FECAM_QUERY = 'cod_entidade:117'
    TERRITORY_ID = "4207403"