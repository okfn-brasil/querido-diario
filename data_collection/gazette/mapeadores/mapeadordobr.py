from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDOBR(MapeadorSemantico):
    name = "mapeadordobr"

    def pattern_name(self):
        return "DOBR"

    def valid_urls(self):
        return "vDOBR"

    def current_status(self):
        return "DOBR_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://tocantinia.diariooficialbr.com.br/
        # https://diariooficial.aguiarnopolis.to.gov.br/
        # https://miracema.diariooficialbr.com.br/

        lista = [
            f"{protocol}://diariooficial.{city}.{state_code}.gov.br/",
            f"{protocol}://{city}.diariooficialbr.com.br",
        ]
        return lista

    def validation(self, response):
        if "ooka.com.br" in response.text:
            return True
        return False

    def is_current(self, response):
        raw = response.xpath(
            '//*[@class="pr-0 mb-8 text-base text-black-700 sm:text-lg xl:text-xl"]/text()'
        ).get()

        if raw is None:
            return "verificar"
        elif "2024" in raw:
            return "atual"
        elif "20" in raw or "19" in raw:
            return "descontinuado"
        else:
            return "vazio"
