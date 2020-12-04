from gazette.spiders.base.fecam import FecamGazetteSpider


class ScWitmarsumSpider(FecamGazetteSpider):
    name = "sc_witmarsum"
    FECAM_QUERY = "cod_entidade:292"
    TERRITORY_ID = "4219408"
