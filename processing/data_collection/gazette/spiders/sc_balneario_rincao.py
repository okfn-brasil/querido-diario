from gazette.spiders.base import FecamGazetteSpider


class ScBalnearioRincaoSpider(FecamGazetteSpider):
    name = "sc_balneario_rincao"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Balneário Rincão"'
    TERRITORY_ID = "4220000"
