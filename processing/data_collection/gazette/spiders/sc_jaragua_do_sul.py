from gazette.spiders.base import FecamGazetteSpider


class ScJaraguaDoSulSpider(FecamGazetteSpider):
    name = "sc_jaragua_do_sul"
    FECAM_QUERY = "cod_entidade:138"
    TERRITORY_ID = "4208906"
