from gazette.spiders.base.fecam import FecamGazetteSpider


class ScIlhotaSpider(FecamGazetteSpider):
    name = "sc_ilhota"
    FECAM_QUERY = "cod_entidade:114"
    TERRITORY_ID = "4207106"
