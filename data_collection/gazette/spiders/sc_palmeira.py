from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPalmeiraSpider(FecamGazetteSpider):
    name = "sc_palmeira"
    FECAM_QUERY = "cod_entidade:187"
    TERRITORY_ID = "4212056"
