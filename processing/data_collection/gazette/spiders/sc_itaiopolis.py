from gazette.spiders.base import FecamGazetteSpider


class ScItaiopolisSpider(FecamGazetteSpider):
    name = "sc_itaiopolis"
    FECAM_QUERY = 'cod_entidade:129'
    TERRITORY_ID = "4208104"