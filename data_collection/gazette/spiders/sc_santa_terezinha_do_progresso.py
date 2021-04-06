from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSantaTerezinhaDoProgressoSpider(FecamGazetteSpider):
    name = "sc_santa_terezinha_do_progresso"
    FECAM_QUERY = "cod_entidade:236"
    TERRITORY_ID = "4215687"
