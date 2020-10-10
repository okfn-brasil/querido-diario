from gazette.spiders.base import FecamGazetteSpider


class ScSerraAltaSpider(FecamGazetteSpider):
    name = "sc_serra_alta"
    FECAM_QUERY = "cod_entidade:263"
    TERRITORY_ID = "4217550"
