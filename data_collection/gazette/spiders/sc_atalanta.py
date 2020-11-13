from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAtalantaSpider(FecamGazetteSpider):
    name = "sc_atalanta"
    FECAM_QUERY = "cod_entidade:27"
    TERRITORY_ID = "4201802"
