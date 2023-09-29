from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCunhaPoraSpider(FecamGazetteSpider):
    name = "sc_cunha_pora"
    FECAM_QUERY = "cod_entidade:80"
    TERRITORY_ID = "4204707"
