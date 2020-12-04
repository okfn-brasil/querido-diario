from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSulBrasilSpider(FecamGazetteSpider):
    name = "sc_sul_brasil"
    FECAM_QUERY = "cod_entidade:266"
    TERRITORY_ID = "4217758"
