from gazette.spiders.base import FecamGazetteSpider


class ScDionisioCerqueiraSpider(FecamGazetteSpider):
    name = "sc_dionisio_cerqueira"
    FECAM_QUERY = 'cod_entidade:84'
    TERRITORY_ID = "4205001"