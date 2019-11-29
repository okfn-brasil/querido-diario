from gazette.spiders.base import FecamGazetteSpider


class ScIbiramaSpider(FecamGazetteSpider):
    name = "sc_ibirama"
    FECAM_QUERY = "cod_entidade:112"
    TERRITORY_ID = "4206900"
