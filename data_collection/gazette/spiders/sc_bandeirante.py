from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBandeiranteSpider(FecamGazetteSpider):
    name = "sc_bandeirante"
    FECAM_QUERY = "cod_entidade:34"
    TERRITORY_ID = "4202081"
