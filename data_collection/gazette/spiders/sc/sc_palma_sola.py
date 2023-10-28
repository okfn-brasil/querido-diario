from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPalmaSolaSpider(FecamGazetteSpider):
    name = "sc_palma_sola"
    FECAM_QUERY = "cod_entidade:186"
    TERRITORY_ID = "4212007"
