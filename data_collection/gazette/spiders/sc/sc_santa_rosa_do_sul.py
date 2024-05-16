from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSantaRosaDoSulSpider(FecamGazetteSpider):
    name = "sc_santa_rosa_do_sul"
    FECAM_QUERY = "cod_entidade:234"
    TERRITORY_ID = "4215653"
