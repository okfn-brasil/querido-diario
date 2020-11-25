from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPortoUniaoSpider(FecamGazetteSpider):
    name = "sc_porto_uniao"
    FECAM_QUERY = "cod_entidade:207"
    TERRITORY_ID = "4213609"
