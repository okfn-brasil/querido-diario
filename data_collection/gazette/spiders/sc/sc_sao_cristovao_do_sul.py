from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoCristovaoDoSulSpider(FecamGazetteSpider):
    name = "sc_sao_cristovao_do_sul"
    FECAM_QUERY = "cod_entidade:243"
    TERRITORY_ID = "4216057"
