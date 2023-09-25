from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoLourencoDoOesteSpider(FecamGazetteSpider):
    name = "sc_sao_lourenco_do_oeste"
    FECAM_QUERY = "cod_entidade:254"
    TERRITORY_ID = "4216909"
