from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPedrasGrandesSpider(FecamGazetteSpider):
    name = "sc_pedras_grandes"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Pedras Grandes"'
    TERRITORY_ID = "4212403"
