from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorGeddoem(Mapeador):
    name = "mapeadorgeddoem"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 25,
        "CONCURRENT_REQUESTS": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "GEDDOEM"

    def valid_urls(self):
        return "vGEDDOEM"

    def current_status(self):
        return "GEDDOEM_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.acessoinformacao.com.br/ba/jacobina/
        # https://acessoainformacao.coaraci.ba.gov.br/
        # https://transparencia.capimgrosso.ba.gov.br/
        # http://tapiramuta.ba.gov.br

        lista = [
            f"{protocol}://www.acessoinformacao.com.br/{state_code}/{city}",
            f"{protocol}://acessoainformacao.{city}.{state_code}.gov.br",
            f"{protocol}://transparencia.{city}.{state_code}.gov.br",
            f"{protocol}://{city}.{state_code}.gov.br",
        ]
        return lista

    def validation(self, response):
        if (
            "ibdm" in response.text
            or "GEDDOEM" in response.text
            or "doem-container" in response.text
        ):
            return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@id="doem-container"]/div[2]/h5').get()

        if raw is None:
            return "vazio"
        elif "2024" in raw:
            return "atual"
        elif "20" in raw or "19" in raw:
            return "descontinuado"
