from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorInstar(MapeadorSemantico):
    name = "mapeadorinstar"

    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "DOWNLOAD_DELAY": 1,
    }

    def pattern_name(self):
        return "INSTAR"

    def valid_urls(self):
        return "vINSTAR"

    def current_status(self):
        return "INSTAR_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.valinhos.sp.gov.br/portal/diario-oficial
        # https://www.prefeituradecrucilandia.mg.gov.br/portal/diario-oficial
        # https://www.montealto.instaridc.com.br/portal/diario-oficial
        # https://www.portal.contagem.mg.gov.br/portal/diario-oficial
        # https://www.ibitinga.instarbr.com.br/portal/diario-oficial
        # https://web.santoandre.sp.gov.br/portal/diario-oficial

        return [
            f"{protocol}://www.{city}.{state_code}.gov.br/portal/diario-oficial",
            f"{protocol}://www.prefeiturade{city}.{state_code}.gov.br/portal/diario-oficial",
            f"{protocol}://www.{city}.instaridc.com.br/portal/diario-oficial",
            f"{protocol}://www.{city}.instarbr.com.br/portal/diario-oficial",
            f"{protocol}://web.{city}.{state_code}.gov.br/portal/diario-oficial",
            f"{protocol}://www.portal.{city}.{state_code}.gov.br/portal/diario-oficial",
        ]

    def validation(self, response):
        if "Instar Tecnologia" in response.text or "instar.com.br" in response.text:
            if "Nenhum diário oficial encontrado" not in response.text:
                if "diario-oficial" in response.url:
                    return True
        return False

    def is_current(self, response):
        rawdate = response.xpath(
            '//*[@id="dof_conteudo"]/div[3]/div[1]/div[2]/div[2]/div[2]/span/text()'
        ).get()
        if "2024" in rawdate:
            return "atual"
        else:
            return "descontinuado"
