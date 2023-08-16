from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorIweb(MapeadorSemantico):
    name = "mapeadoriweb"

    def pattern_name(self):
        return "IWEB"

    def valid_urls(self):
        return "vIWEB"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.caboverde.mg.gov.br/
        # https://www.muzambinho.mg.gov.br/

        return [
            f"{protocol}://www.{city}.{state_code}.gov.br/transparencia/diario-oficial-eletronico"
        ]

    def validation(self, response):
        if "Invicta Web" in response.text:
            return True
        return False
