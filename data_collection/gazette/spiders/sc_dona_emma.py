from gazette.spiders.base.fecam import FecamGazetteSpider


class ScDonaEmmaSpider(FecamGazetteSpider):
    name = "sc_dona_emma"
    FECAM_QUERY = "cod_entidade:85"
    TERRITORY_ID = "4205100"
