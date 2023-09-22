from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAbdonBatistaSpider(FecamGazetteSpider):
    name = "sc_abdon_batista"
    FECAM_QUERY = "cod_entidade:4"
    TERRITORY_ID = "4200051"
