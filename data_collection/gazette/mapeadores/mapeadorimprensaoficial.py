import scrapy

from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorImprensaOficial(MapeadorSemantico):
    name = "mapeadorimprensaoficial"

    def pattern_name(self):
        return "IMPOFICIAL"

    def valid_urls(self):
        return "vIMPOFICIAL"

    def current_status(self):
        return "IMPOFICIAL_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://sapeacu.ba.gov.br/ultimos-diarios/
        # http://pmgongogiba.imprensaoficial.org/ultimos-diarios/

        lista = [
            f"{protocol}://{city}.{state_code}.gov.br/ultimos-diarios/",
            f"{protocol}://pm{city}{state_code}.imprensaoficial.org/ultimos-diarios/",
        ]
        return lista

    def validation(self, response):
        if "imprensaoficial.org" in response.text:
            if "Edição" in response.text:
                return True
        return False

    def is_current(self, response, index):
        if "Oops" not in response.text:
            iscurrent = "atual"

        elif ".org/20" in response.text or ".org/19" in response.text:
            iscurrent = "descontinuado"

        else:
            iscurrent = "verificar"

        self.territories[index][self.current_status()].append(iscurrent)

    def parse(self, response, index):
        if self.validation(response):
            if response.url not in self.territories[index][self.pattern_name()]:
                self.territories[index][self.pattern_name()].append(response.url)

            link = response.url[:-16] + "2024/01"
            yield scrapy.Request(
                link,
                callback=self.is_current,
                cb_kwargs=dict(index=index),
            )

        elif response.url not in self.territories[index][self.valid_urls()]:
            self.territories[index][self.valid_urls()].append(response.url)
