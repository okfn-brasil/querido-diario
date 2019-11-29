from gazette.spiders.base import FecamGazetteSpider


class ScCaxambuDoSulSpider(FecamGazetteSpider):
    name = "sc_caxambu_do_sul"
    FECAM_QUERY = "cod_entidade:67"
    TERRITORY_ID = "4204103"
