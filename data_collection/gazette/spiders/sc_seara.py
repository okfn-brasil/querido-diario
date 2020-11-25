from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSearaSpider(FecamGazetteSpider):
    name = "sc_seara"
    FECAM_QUERY = "cod_entidade:262"
    TERRITORY_ID = "4217501"
