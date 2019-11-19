from gazette.spiders.base import FecamGazetteSpider


class ScCorreiaPintoSpider(FecamGazetteSpider):
    name = "sc_correia_pinto"
    FECAM_QUERY = 'cod_entidade:77'
    TERRITORY_ID = "4204558"