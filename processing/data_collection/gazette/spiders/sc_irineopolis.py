from gazette.spiders.base import FecamGazetteSpider


class ScIrineopolisSpider(FecamGazetteSpider):
    name = "sc_irineopolis"
    FECAM_QUERY = "cod_entidade:127"
    TERRITORY_ID = "4207908"
