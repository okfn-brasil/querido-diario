from gazette.spiders.base import FecamGazetteSpider


class ScSaoJoaoDoOesteSpider(FecamGazetteSpider):
    name = "sc_sao_joao_do_oeste"
    FECAM_QUERY = 'entidade:"Prefeitura Municipal de São João do Oeste"'
    TERRITORY_ID = "4216255"
