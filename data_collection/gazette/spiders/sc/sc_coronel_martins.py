from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCoronelMartinsSpider(FecamGazetteSpider):
    name = "sc_coronel_martins"
    FECAM_QUERY = "cod_entidade:76"
    TERRITORY_ID = "4204459"
