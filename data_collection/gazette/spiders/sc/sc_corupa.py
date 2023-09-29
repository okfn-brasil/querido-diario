from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCorupaSpider(FecamGazetteSpider):
    name = "sc_corupa"
    FECAM_QUERY = "cod_entidade:78"
    TERRITORY_ID = "4204509"
