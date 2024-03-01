from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorVale(Mapeador):
    name = "mapeadorvale"

    custom_settings = {
        "CONCURRENT_REQUESTS": 50,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "VALE"

    def valid_urls(self):
        return "vVALE"

    def current_status(self):
        return "VALE_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://diario.cristalandia.to.gov.br/
        # https://dom.novaolinda.to.gov.br/

        return [
            f"{protocol}://diario.{city}.{state_code}.gov.br/",
            f"{protocol}://dom.{city}.{state_code}.gov.br/",
        ]

    def validation(self, response):
        if "Termos de uso |" in response.text:
            if "vale-solucoes" in response.text:
                if (
                    not response.xpath('//*[@class="home-editions-content"]').get()
                    is None
                ):
                    return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@class="last-edition-date"]/text()').get()

        if raw is None:
            return "verificar"
        elif "2024" in raw:
            return "atual"
        elif "20" in raw or "19" in raw:
            return "descontinuado"
        else:
            return "vazio"
