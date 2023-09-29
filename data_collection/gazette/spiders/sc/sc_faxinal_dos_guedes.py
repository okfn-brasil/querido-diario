from gazette.spiders.base.fecam import FecamGazetteSpider


class ScFaxinalDosGuedesSpider(FecamGazetteSpider):
    name = "sc_faxinal_dos_guedes"
    FECAM_QUERY = "cod_entidade:90"
    TERRITORY_ID = "4205308"
