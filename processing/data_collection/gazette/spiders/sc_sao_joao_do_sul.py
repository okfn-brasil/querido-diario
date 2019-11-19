from gazette.spiders.base import FecamGazetteSpider


class ScSaoJoaoDoSulSpider(FecamGazetteSpider):
    name = "sc_sao_joao_do_sul"
    FECAM_QUERY = 'cod_entidade:249'
    TERRITORY_ID = "4216404"