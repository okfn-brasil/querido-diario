from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorJdown(MapeadorSemantico):
    name = "mapeadorjdown"

    def pattern_name(self):
        return "JDOWN"

    def valid_urls(self):
        return "vJDOWN"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://diariooficial.taipas.to.gov.br/index.php/publicacoes

        return [
            f"{protocol}://diariooficial.{city}.{state_code}.gov.br/index.php/publicacoes"
        ]

    def validation(self, response):
        if "jDownloads.com" in response.text or "jdownloads.com" in response.text:
            return True
        return False
