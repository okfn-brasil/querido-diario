from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMafraSpider(FecamGazetteSpider):
    name = "sc_mafra"
    FECAM_QUERY = "cod_entidade:157"
    TERRITORY_ID = "4210100"
