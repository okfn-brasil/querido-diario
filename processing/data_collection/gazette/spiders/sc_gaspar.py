from gazette.spiders.base import FecamGazetteSpider


class ScGasparSpider(FecamGazetteSpider):
    name = "sc_gaspar"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Gaspar"'
    TERRITORY_ID = "4205902"
