from gazette.spiders.base.fecam import FecamGazetteSpider


class ScDoutorPedrinhoSpider(FecamGazetteSpider):
    name = "sc_doutor_pedrinho"
    FECAM_QUERY = "cod_entidade:86"
    TERRITORY_ID = "4205159"
