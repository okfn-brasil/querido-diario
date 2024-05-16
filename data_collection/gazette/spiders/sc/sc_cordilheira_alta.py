from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCordilheiraAltaSpider(FecamGazetteSpider):
    name = "sc_cordilheira_alta"
    FECAM_QUERY = "cod_entidade:74"
    TERRITORY_ID = "4204350"
