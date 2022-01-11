from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPalhocaSpider(FecamGazetteSpider):
    name = "sc_palhoca"
    FECAM_QUERY = "cod_entidade:185"
    TERRITORY_ID = "4211900"
