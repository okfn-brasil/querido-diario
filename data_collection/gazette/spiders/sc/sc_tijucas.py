from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTijucasSpider(FecamGazetteSpider):
    name = "sc_tijucas"
    FECAM_QUERY = "cod_entidade:270"
    TERRITORY_ID = "4218004"
