from gazette.spiders.base import FecamGazetteSpider


class ScDoutorPedrinhoSpider(FecamGazetteSpider):
    name = "sc_doutor_pedrinho"
    FECAM_QUERY = "cod_entidade:86"
    TERRITORY_ID = "4205159"
