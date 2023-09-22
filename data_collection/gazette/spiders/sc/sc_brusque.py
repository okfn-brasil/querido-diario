from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBrusqueSpider(FecamGazetteSpider):
    name = "sc_brusque"
    FECAM_QUERY = "cod_entidade:52"
    TERRITORY_ID = "4202909"
