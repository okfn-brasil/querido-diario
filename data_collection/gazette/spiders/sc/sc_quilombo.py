from gazette.spiders.base.fecam import FecamGazetteSpider


class ScQuilomboSpider(FecamGazetteSpider):
    name = "sc_quilombo"
    FECAM_QUERY = "cod_entidade:214"
    TERRITORY_ID = "4214201"
