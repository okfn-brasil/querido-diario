from gazette.spiders.base import FecamGazetteSpider


class ScBalnearioCamboriuSpider(FecamGazetteSpider):
    name = "sc_balneario_camboriu"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Balneário Camboriú"'
    TERRITORY_ID = "4202008"
