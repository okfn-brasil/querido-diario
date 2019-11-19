from gazette.spiders.base import FecamGazetteSpider


class ScCriciumaSpider(FecamGazetteSpider):
    name = "sc_criciuma"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Criciúma"'
    TERRITORY_ID = "4204608"