from gazette.spiders.base.fecam import FecamGazetteSpider


class ScVargeaoSpider(FecamGazetteSpider):
    name = "sc_vargeao"
    FECAM_QUERY = "cod_entidade:286"
    TERRITORY_ID = "4219101"
