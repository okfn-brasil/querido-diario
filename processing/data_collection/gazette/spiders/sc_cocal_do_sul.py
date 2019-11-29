from gazette.spiders.base import FecamGazetteSpider


class ScCocalDoSulSpider(FecamGazetteSpider):
    name = "sc_cocal_do_sul"
    FECAM_QUERY = "cod_entidade:72"
    TERRITORY_ID = "4204251"
