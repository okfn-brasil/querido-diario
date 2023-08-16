from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorSaiio(MapeadorSemantico):
    name = "mapeadorsaiio"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 25,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "SAIIO"

    def valid_urls(self):
        return "vSAIIO"

    def current_status(self):
        return "SAIIO_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://sai.io.org.br/al/penedo/Site/DiarioOficial
        # https://diariooficial.ourolandia.ba.gov.br/Site/DiarioOficial
        # https://www.medeirosneto.ba.gov.br/site/diariooficial

        lista = [
            f"{protocol}://sai.io.org.br/{state_code}/{city}/Site/DiarioOficial",
            f"{protocol}://diariooficial.{city}.{state_code}.gov.br/Site/DiarioOficial",
            f"{protocol}://www.{city}.{state_code}.gov.br/site/diariooficial",
        ]
        return lista

    def validation(self, response):
        if "imap.org.br" in response.text:
            if "Nenhuma Edição Encontrada" not in response.text:
                if "Prefeitura Municipal" in response.text:
                    return True
        return False

    def is_current(self, response):
        rawdate = response.xpath(
            '//*[@id="main"]/div/div/div[4]/div/section/article/ul/li[1]/h4/text()'
        ).get()

        if "2024" in rawdate:
            return "atual"
        else:
            return "descontinuado"
