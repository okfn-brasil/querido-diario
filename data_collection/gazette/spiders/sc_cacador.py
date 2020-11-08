from gazette.spiders.base import FecamGazetteSpider


class ScCacadorSpider(FecamGazetteSpider):
    name = "sc_cacador"
    FECAM_QUERY = "cod_entidade:53"
    TERRITORY_ID = "4203006"
