from gazette.spiders.base import FecamGazetteSpider


class ScAtalantaSpider(FecamGazetteSpider):
    name = "sc_atalanta"
    FECAM_QUERY = "cod_entidade:27"
    TERRITORY_ID = "4201802"
