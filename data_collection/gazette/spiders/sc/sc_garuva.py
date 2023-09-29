from gazette.spiders.base.fecam import FecamGazetteSpider


class ScGaruvaSpider(FecamGazetteSpider):
    name = "sc_garuva"
    FECAM_QUERY = "cod_entidade:99"
    TERRITORY_ID = "4205803"
