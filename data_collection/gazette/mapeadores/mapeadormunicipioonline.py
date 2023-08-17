from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorMunicipioonline(Mapeador):
    name = "mapeadormunicipioonline"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "MunicipioOnline"

    def valid_urls(self):
        return "vMunicipioOnline"

    def current_status(self):
        return "MunicipioOnline_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://aquidaba.se.gov.br/portaltransparencia/?servico=cidadao/diariooficial
        # https://www.municipioonline.com.br/se/prefeitura/japaratuba/cidadao/diariooficial

        return [
            f"{protocol}://{city}.{state_code}.gov.br/portaltransparencia/?servico=cidadao/diariooficial",
            f"{protocol}://www.municipioonline.com.br/{state_code}/prefeitura/{city}/cidadao/diariooficial",
        ]

    def validation(self, response):
        if "3tecnos.com.br" in response.text or "3Tecnos.com.br" in response.text:
            if "indisponivel" not in response.url:
                if "serviço solicitado está indisponível" not in response.text:
                    return True
        return False

    def is_current(self, response):
        rawdate = response.xpath('//*[@id="body_pnUltimaEdicao"]/div/div/div[2]').get()

        if rawdate is None:
            return "vazio"

        if "2024" in rawdate:
            return "atual"

        else:
            return "descontinuado"
