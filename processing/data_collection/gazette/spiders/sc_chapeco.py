from gazette.spiders.base import FecamGazetteSpider


class ScChapecoSpider(FecamGazetteSpider):
    name = "sc_chapeco"
    FECAM_QUERY = "cod_entidade:71"
    TERRITORY_ID = "4204202"
