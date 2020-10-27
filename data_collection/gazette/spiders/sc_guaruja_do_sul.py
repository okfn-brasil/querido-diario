from gazette.spiders.base import FecamGazetteSpider


class ScGuarujaDoSulSpider(FecamGazetteSpider):
    name = "sc_guaruja_do_sul"
    FECAM_QUERY = "cod_entidade:107"
    TERRITORY_ID = "4206603"
