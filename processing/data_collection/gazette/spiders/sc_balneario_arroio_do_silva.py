from gazette.spiders.base import FecamGazetteSpider


class ScBalnearioArroioDoSilvaSpider(FecamGazetteSpider):
    name = "sc_balneario_arroio_do_silva"
    FECAM_QUERY = "cod_entidade:29"
    TERRITORY_ID = "4201950"
