from gazette.spiders.base.fecam import FecamGazetteSpider


class ScFraiburgoSpider(FecamGazetteSpider):
    name = "sc_fraiburgo"
    FECAM_QUERY = "cod_entidade:95"
    TERRITORY_ID = "4205506"
