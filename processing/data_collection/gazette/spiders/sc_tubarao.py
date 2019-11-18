from gazette.spiders.base import FecamGazetteSpider


class ScTubaraoSpider(FecamGazetteSpider):
    name = "sc_tubarao"
    FECAM_QUERY = 'cod_entidade:279'
    TERRITORY_ID = "4218707"