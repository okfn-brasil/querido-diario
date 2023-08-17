import scrapy

from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorSiganet(Mapeador):
    name = "mapeadorsiganet"

    custom_settings = {
        "CONCURRENT_REQUESTS": 50,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "SIGANET"

    def valid_urls(self):
        return "vSIGANET"

    def current_status(self):
        return "SIGANET_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://balsas.ma.gov.br/diario/diario
        # https://transparencia.beneditoleite.ma.gov.br/acessoInformacao/diario/diario

        lista = [
            f"{protocol}://{city}.{state_code}.gov.br/diario/diario",
            f"{protocol}://transparencia.{city}.{state_code}.gov.br/acessoInformacao/diario/diario",
        ]
        return lista

    def validation(self, response):
        if "siganet" in response.text:
            if ".org" not in response.url:
                return True
        return False

    def is_current(self, response, index):
        if '"TDI_DT_PUBLICACAO":"2024-' in response.text:
            iscurrent = "atual"
        elif (
            '"TDI_DT_PUBLICACAO":"20' in response.text
            or '"TDI_DT_PUBLICACAO":"19' in response.text
        ):
            iscurrent = "descontinuado"
        else:
            iscurrent = "vazio"

        self.territories[index][self.current_status()].append(iscurrent)

    def parse(self, response, index):
        if self.validation(response):
            if response.url not in self.territories[index][self.pattern_name()]:
                self.territories[index][self.pattern_name()].append(response.url)

            yield scrapy.Request(
                f"{response.url}/listarDiario",
                callback=self.is_current,
                cb_kwargs=dict(index=index),
            )

        elif response.url not in self.territories[index][self.valid_urls()]:
            self.territories[index][self.valid_urls()].append(response.url)
