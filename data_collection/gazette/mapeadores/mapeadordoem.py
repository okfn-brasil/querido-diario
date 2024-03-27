from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDoem(MapeadorSemantico):
    name = "mapeadordoem"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "DOEM"

    def valid_urls(self):
        return "vDOEM"

    def current_status(self):
        return "DOEM_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://doem.org.br/ba/acajutiba
        # https://doem.org.br/ba/mascote

        return [f"{protocol}://doem.org.br/{state_code}/{city}"]

    def validation(self, response):
        if "doem.org.br" in response.text:
            if "está Indisponível" not in response.text:
                if "Não foi possível carregar o diário" not in response.text:
                    if "404 - Página não encontrada" not in response.text:
                        if "ibdm.org.br" not in response.url:
                            return True
        return False

    def is_current(self, response):
        if "Não foi possível carregar o diário" in response.text:
            return "vazio"

        # modelo 1 de pagina inicial: https://doem.org.br/ba/sentose
        indice = response.text.find("og:description")
        trecho = response.text[indice : indice + 200]

        # modelo 2 de pagina inicial: https://doem.org.br/ba/acajutiba
        rawdate = response.xpath(
            '//*[@id="wrapper"]/div[1]/div/div/div/div[1]/h3/text()'
        ).get()
        if rawdate is None:
            rawdate = ""

        # verifica sempre nas duas possibilidades
        if "2024" in trecho or "2024" in rawdate:
            return "atual"
        elif "20" in trecho or "19" in trecho or "20" in rawdate or "19" in rawdate:
            return "descontinuado"
        else:
            return "vazio"
