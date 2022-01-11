from gazette.spiders.base.fecam import FecamGazetteSpider


class ScJaboraSpider(FecamGazetteSpider):
    name = "sc_jabora"
    FECAM_QUERY = "cod_entidade:135"
    TERRITORY_ID = "4208609"
