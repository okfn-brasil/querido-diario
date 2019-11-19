from gazette.spiders.base import FecamGazetteSpider


class ScItapemaSpider(FecamGazetteSpider):
    name = "sc_itapema"
    FECAM_QUERY = 'cod_entidade:131'
    TERRITORY_ID = "4208302"