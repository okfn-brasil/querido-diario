from gazette.spiders.base.fecam import FecamGazetteSpider


class ScVargemSpider(FecamGazetteSpider):
    name = "sc_vargem"
    FECAM_QUERY = "cod_entidade:287"
    TERRITORY_ID = "4219150"
