from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPresidenteGetulioSpider(FecamGazetteSpider):
    name = "sc_presidente_getulio"
    FECAM_QUERY = "cod_entidade:211"
    TERRITORY_ID = "4214003"
