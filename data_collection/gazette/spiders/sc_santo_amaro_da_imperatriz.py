from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSantoAmaroDaImperatrizSpider(FecamGazetteSpider):
    name = "sc_santo_amaro_da_imperatriz"
    FECAM_QUERY = "cod_entidade:238"
    TERRITORY_ID = "4215703"
