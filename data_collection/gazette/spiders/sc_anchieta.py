from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAnchietaSpider(FecamGazetteSpider):
    name = "sc_anchieta"
    FECAM_QUERY = "cod_entidade:14"
    TERRITORY_ID = "4200804"
