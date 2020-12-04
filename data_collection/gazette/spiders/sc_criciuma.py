from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCriciumaSpider(FecamGazetteSpider):
    name = "sc_criciuma"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Criciúma"'
    TERRITORY_ID = "4204608"
