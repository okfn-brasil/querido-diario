from gazette.spiders.base import FecamGazetteSpider


class ScTrombudoCentralSpider(FecamGazetteSpider):
    name = "sc_trombudo_central"
    FECAM_QUERY = "cod_entidade:278"
    TERRITORY_ID = "4218608"
