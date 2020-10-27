from gazette.spiders.base import FecamGazetteSpider


class ScTigrinhosSpider(FecamGazetteSpider):
    name = "sc_tigrinhos"
    FECAM_QUERY = 'entidade:"Prefeitura Municipal de Tigrinhos"'
    TERRITORY_ID = "4217956"
