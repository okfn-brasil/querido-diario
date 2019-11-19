from gazette.spiders.base import FecamGazetteSpider


class ScBalnearioGaivotaSpider(FecamGazetteSpider):
    name = "sc_balneario_gaivota"
    FECAM_QUERY = 'cod_entidade:32'
    TERRITORY_ID = "4202073"