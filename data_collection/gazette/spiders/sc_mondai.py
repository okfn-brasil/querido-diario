from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMondaiSpider(FecamGazetteSpider):
    name = "sc_mondai"
    FECAM_QUERY = "cod_entidade:168"
    TERRITORY_ID = "4211009"
