from gazette.spiders.base import FecamGazetteSpider


class ScSantaHelenaSpider(FecamGazetteSpider):
    name = "sc_santa_helena"
    FECAM_QUERY = "cod_entidade:232"
    TERRITORY_ID = "4215554"
