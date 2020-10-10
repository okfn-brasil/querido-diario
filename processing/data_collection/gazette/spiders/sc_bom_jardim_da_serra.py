from gazette.spiders.base import FecamGazetteSpider


class ScBomJardimDaSerraSpider(FecamGazetteSpider):
    name = "sc_bom_jardim_da_serra"
    FECAM_QUERY = "cod_entidade:43"
    TERRITORY_ID = "4202503"
