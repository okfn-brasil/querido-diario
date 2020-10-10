from gazette.spiders.base import FecamGazetteSpider


class ScSaoFranciscoDoSulSpider(FecamGazetteSpider):
    name = "sc_sao_francisco_do_sul"
    FECAM_QUERY = "cod_entidade:245"
    TERRITORY_ID = "4216206"
