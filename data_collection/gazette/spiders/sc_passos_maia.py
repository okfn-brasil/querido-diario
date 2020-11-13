from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPassosMaiaSpider(FecamGazetteSpider):
    name = "sc_passos_maia"
    FECAM_QUERY = "cod_entidade:192"
    TERRITORY_ID = "4212270"
