from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMassarandubaSpider(FecamGazetteSpider):
    name = "sc_massaranduba"
    FECAM_QUERY = "cod_entidade:163"
    TERRITORY_ID = "4210605"
