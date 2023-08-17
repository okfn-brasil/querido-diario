from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorAdminLTE(Mapeador):
    name = "mapeadoradminlte"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "ADMINLTE"

    def valid_urls(self):
        return "vADMINLTE"

    def current_status(self):
        return "ADMINLTE_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://diariooficial.gurupi.to.gov.br/
        # https://diariooficial.pmsaraguaia.pa.gov.br/

        lista = [
            f"{protocol}://diariooficial.{city}.{state_code}.gov.br/",
            f"{protocol}://diariooficial.pm{city}.{state_code}.gov.br/",
        ]
        return lista

    def validation(self, response):
        if "PRE-LOADER" in response.text:
            if "col-sm-5" in response.text:
                if "col-sm-7" in response.text:
                    if (
                        'data-original-title="Baixar a Última Edição Normal">Acessar</a>'
                        in response.text
                    ):
                        return True
        return False

    def is_current(self, response):
        rawdateslist = response.xpath('//*[@style="font-weight: bold"]').getall()

        if "2024" in rawdateslist[1]:
            return "atual"

        else:
            return "descontinuado"
