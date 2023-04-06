from datetime import datetime, date
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpTaboaoDaSerraSpider(BaseGazetteSpider):

    """
    Raspador para as Publicaçoes dos Diarios Oficiais de Taboão da Serra.
    Atualmente Publicando apenas em uma unica pagina.
    """

    TERRITORY_ID = "3552809"
    name = "sp_taboao_da_serra"
    allowed_domains = ["ts.sp.gov.br"]
    start_urls = ["https://prefeitura.ts.sp.gov.br/imprensa-oficial/"]
    start_date = date(2021, 1, 4)
    end_date = datetime.today().date()

    def parse(self, response):

        links = self.filtro_links(divs=response.css('div[class*=elementor-button-wrapper]'))
        datas_edits = response.css('div[class*=jet-listing-dynamic-field__content]::text').getall()
        datas, edits = datas_edits[::2], datas_edits[1::2]

        for info in range(len(links)):
            data = datetime.strptime(datas[info], "%d/%m/%Y").date()
            edition_number = edits[info].replace("Edição ", "")
            if self.start_date <= data <= self.end_date:
                yield Gazette(
                    date=data,
                    edition_number=edition_number,
                    file_urls=[
                        links[info],
                    ],
                    is_extra_edition=edits[info][-1] in "Ee",
                    power="legislative",
                )

    @staticmethod
    def filtro_links(divs):

        """
        :param divs: Recebe uma lista de Tags Div para extrair links do PDF
        :return: Lista com links PDF
        """

        listas = {
            "Lista Principal": [],
            "Lista Complemento": []
        }

        for links in divs:
            if links.css('span[class*=elementor-button-text]::text').get() == "Link externo":
                listas["Lista Principal"].append(links.css('a::attr(href)').get())
            if links.css('i').get():
                listas["Lista Complemento"].append(links.css('a::attr(href)').get())

        for filtro in range(len(listas["Lista Principal"])):
            if str(listas["Lista Principal"][filtro]).find("pdf") == -1:
                listas["Lista Principal"][filtro] = listas["Lista Complemento"][filtro]

        return listas["Lista Principal"]
