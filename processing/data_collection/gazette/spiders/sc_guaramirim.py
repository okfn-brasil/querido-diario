from gazette.spiders.base import FecamGazetteSpider


class ScGuaramirimSpider(FecamGazetteSpider):
    name = "sc_guaramirim"
    FECAM_QUERY = "cod_entidade:106"
    TERRITORY_ID = "4206504"
