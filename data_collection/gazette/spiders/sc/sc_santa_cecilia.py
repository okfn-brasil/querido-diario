from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSantaCeciliaSpider(FecamGazetteSpider):
    name = "sc_santa_cecilia"
    FECAM_QUERY = "cod_entidade:231"
    TERRITORY_ID = "4215505"
