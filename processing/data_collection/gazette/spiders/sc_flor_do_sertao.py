from gazette.spiders.base import FecamGazetteSpider


class ScFlorDoSertaoSpider(FecamGazetteSpider):
    name = "sc_flor_do_sertao"
    FECAM_QUERY = "cod_entidade:91"
    TERRITORY_ID = "4205357"
