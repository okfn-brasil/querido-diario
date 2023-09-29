from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMeleiroSpider(FecamGazetteSpider):
    name = "sc_meleiro"
    FECAM_QUERY = "cod_entidade:165"
    TERRITORY_ID = "4210803"
