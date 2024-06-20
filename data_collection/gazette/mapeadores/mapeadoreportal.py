from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorEPortal(MapeadorSemantico):
    name = "mapeadoreportal"

    def pattern_name(self):
        return "EPORTAL"

    def valid_urls(self):
        return "vEPORTAL"

    def current_status(self):
        return "EPORTAL_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.riodosbois.to.gov.br/diariooficial
        # https://www.piraque.to.gov.br/diariooficial
        # https://diario.augustinopolis.to.gov.br/

        return [
            f"{protocol}://www.{city}.{state_code}.gov.br/diariooficial",
            f"{protocol}://diario.{city}.{state_code}.gov.br/",
        ]

    def validation(self, response):
        if (
            "pratica-logo" in response.text
            or "dkc-logo" in response.text
            or "vale-solucoes" in response.text
        ):
            if not response.xpath('//*[@class="main_last_edition"]').get() is None:
                return True
        return False

    def is_current(self, response):
        rawdate = response.xpath(
            "/html/body/section[1]/div/div/div[1]/div/div[1]/p[1]/text()"
        ).get()

        if "2024" in rawdate:
            return "atual"
        else:
            return "descontinuado"
