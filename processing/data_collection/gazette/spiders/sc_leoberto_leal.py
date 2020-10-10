from gazette.spiders.base import FecamGazetteSpider


class ScLeobertoLealSpider(FecamGazetteSpider):
    name = "sc_leoberto_leal"
    FECAM_QUERY = "cod_entidade:151"
    TERRITORY_ID = "4209805"
