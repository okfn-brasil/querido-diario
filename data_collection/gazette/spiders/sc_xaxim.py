from gazette.spiders.base.fecam import FecamGazetteSpider


class ScXaximSpider(FecamGazetteSpider):
    name = "sc_xaxim"
    FECAM_QUERY = "cod_entidade:295"
    TERRITORY_ID = "4219705"
