from gazette.spiders.base.fecam import FecamGazetteSpider


class ScItaiopolisSpider(FecamGazetteSpider):
    name = "sc_itaiopolis"
    FECAM_QUERY = "cod_entidade:129"
    TERRITORY_ID = "4208104"
