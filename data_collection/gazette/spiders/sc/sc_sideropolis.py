from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSideropolisSpider(FecamGazetteSpider):
    name = "sc_sideropolis"
    FECAM_QUERY = "cod_entidade:264"
    TERRITORY_ID = "4217600"
