from gazette.spiders.base import FecamGazetteSpider


class ScTimbeDoSulSpider(FecamGazetteSpider):
    name = "sc_timbe_do_sul"
    FECAM_QUERY = 'cod_entidade:271'
    TERRITORY_ID = "4218103"