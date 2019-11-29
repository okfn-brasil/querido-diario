from gazette.spiders.base import FecamGazetteSpider


class ScFormosaDoSulSpider(FecamGazetteSpider):
    name = "sc_formosa_do_sul"
    FECAM_QUERY = "cod_entidade:93"
    TERRITORY_ID = "4205431"
