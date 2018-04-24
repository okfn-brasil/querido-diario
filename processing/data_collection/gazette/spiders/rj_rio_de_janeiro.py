import datetime as dt
import re
import scrapy
from gazette.items import Gazette

class RjRioDeJaneiroSpider(scrapy.Spider):
    MUNICIPALITY_ID = '3304557'
    name = 'rj_rio_de_janeiro'
    allowed_domains = ['doweb.rio.rj.gov.br']
    start_urls = ['http://doweb.rio.rj.gov.br']
    search_gazette_url = 'http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca={}' # '20%2F04%2F2018' => 20/04/2018

    def parse(self, response):
        start_date = dt.date(2018, 1, 1)
        delta = dt.timedelta(days=1)
        while start_date <= dt.date.today():
            url = self.search_gazette_url.format(start_date.strftime('%d/%m/%Y'))
            print(url)
            yield scrapy.Request(url, self.parse_search_result)

        # 1) a partir de 2015-1-1, fazer um get em "http://doweb.rio.rj.gov.br/?buscar_diario=ok&data_busca=20%2F04%2F2018&tipo=1" (data no format 20/04/2018)
        # 2) vários resultados:
        # 2.1) caso o DO exista e seja a única edição, existirá o seguinte trecho de código:
        # '#conteudo_principal > #conteudo_home > #conteudo_erro script' (testar seletor)
        #<script>window.location = 'visualizar_pdf.php?edi_id=3734&page=1';</script>
        # 2.1.1) da URL acima, a informação que precisamos é apenas o 'edi_id', extrair com uma regex
        # 2.1.2) url para download do pdf: 'http://doweb.rio.rj.gov.br/ler_pdf.php?download=ok&edi_id={}'
        # 2.1.3) sabemos a data, não é uma edição extra e podemos montar a url para download do pdf

        # 2.2) caso existam 2 edições:
        # 2.2.1) seletor '#dialog-message' conterá o texto: 'Existe mais de uma publicação para esta data.'
        # 2.2.2) '#dialog-message a' retornará N (2?) elementos
        # 2.2.3) obter o href e extrair o 'edi_id', conforme item 2.1.1
        # 2.2.4) se o texto do link (a) contiver a string 'Suplemento', está é uma edição extra
        # 2.2.5) proceder para o download conforme 2.1.2

        # 2.3) caso não exista DO (fds e etc):
        # 2.3.1) '#dialog-message' conterá o texto 'Não existe publicação para esta data'
        # 2.3.2) apenas ignorar

            start_date += delta

    def parse_search_result(self, response):
        print("================> " + response.url)

        one_gazette = response.css('#conteudo_principal > #conteudo_home > #conteudo_erro script').extract_first()
        if one_gazette:
            match = re.search('.*edi_id=([0-9]+).*', one_gazette)
            if match:
                # caso 2.1
                #print("================> " + match.group(1))
                return

        multiple_gazettes = response.css('#dialog-message').extract_first()
        if multiple_gazettes and 'Existe mais de uma publicação para esta data' in multiple_gazettes:
            # caso 2.2
            #print("================> " + multiple_gazettes)
            return
        
        no_gazettes = response.css('#dialog-message').extract_first()
        if no_gazettes and 'Não existe publicação para esta data' in no_gazettes:
            # caso 2.3
            #print("================> " + no_gazettes)
            return

        print("================> CASO NAO IDENTIFICADO!!! url = " + response.url)
        import ipdb; ipdb.set_trace()
        # casos não identificados
        # http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca=18/04/2018
        # http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca=11/04/2018
        # http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca=12/04/2018
        # http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca=20/04/2018
        # http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca=17/04/2018
        # http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca=19/04/2018

        """
        is_extra_edition = False
        items.append(
            Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive',
                scraped_at=dt.datetime.utcnow(),
            )
        )
        return items
        """