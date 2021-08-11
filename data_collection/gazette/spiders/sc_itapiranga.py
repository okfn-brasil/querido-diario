from gazette.spiders.base.fecam import FecamGazetteSpider


class ScItapirangaSpider(FecamGazetteSpider):
    name = "sc_itapiranga"
    FECAM_QUERY = "cod_entidade:132"
    TERRITORY_ID = "4208401"
