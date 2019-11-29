from gazette.spiders.base import FecamGazetteSpider


class ScMonteCarloSpider(FecamGazetteSpider):
    name = "sc_monte_carlo"
    FECAM_QUERY = "cod_entidade:169"
    TERRITORY_ID = "4211058"
