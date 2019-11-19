from gazette.spiders.base import FecamGazetteSpider


class ScSaoJoseDoCerritoSpider(FecamGazetteSpider):
    name = "sc_sao_jose_do_cerrito"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de São José do Cerrito"'
    TERRITORY_ID = "4216800"