import datetime as dt
import json
import re
from typing import Any, Generator, Optional

import scrapy
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RsBageSpider(BaseGazetteSpider):
    """
    Raspador de diários oficiais da Prefeitura Municipal de Bagé - RS.

    Município: Bagé - RS
    Código IBGE: 4301602
    Plataforma de publicação: SERPRO Gov.br Cidades (Sistema de Documentos Oficiais Eletrônicos - DOE)
    Contribuição desenvolvida no âmbito do projeto Bagé Transparente.

    Execução 100% autônoma na infraestrutura do Scrapy Cloud (OKBR):
    Coleta metadados via API REST do SERPRO e emite os binários do PDF
    através do handler nativo RFC 2397 Data URI (RFC 2397) 
    www.bagetransparente.com.br
    """

    TERRITORY_ID = "4301602"
    name = "rs_bage"
    allowed_domains = ["cidadesdoe.serpro.gov.br"]

    # Data da edição inaugural do DOE eletrônico de Bagé no SERPRO
    start_date = dt.date(2024, 11, 8)

    BASE_URL = "https://cidadesdoe.serpro.gov.br/govbrcidades_doe"
    HASH_PREFEITURA = "eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="
    CSRF_TOKEN = "T6C+9iB49TLra4jEsMeSckDMNhQ="
    COOKIE_HEADER = "nr2AcessoGov_web=crf%3dT6C%2b9iB49TLra4jEsMeSckDMNhQ%3d%3buid%3d0%3bunm%3d"

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """Inicia a consulta à listagem do SERPRO DOE."""
        yield self._build_page_request(start_index=0)

    def _build_page_request(self, start_index: int) -> scrapy.Request:
        """Monta a requisição POST com payload de busca e paginação."""
        endpoint = (
            f"{self.BASE_URL}/screenservices/govbrcidades_doe/Cidadao/"
            f"DOEConsultaCidadao/ScreenDataSetGetTBDadosPublicacaoByDapIdHashPrefeitura"
        )

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "X-CSRFToken": self.CSRF_TOKEN,
            "Cookie": self.COOKIE_HEADER,
            "Origin": "https://cidadesdoe.serpro.gov.br",
            "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        }

        payload = {
            "versionInfo": {
                "moduleVersion": "n+Mjd8q_ahkeNIkyYfbTNA",
                "apiVersion": "zRAHqBwfWZSZQDXDYGpfWg",
            },
            "viewName": "Cidadao.DOEConsultaCidadao",
            "screenData": {
                "variables": {
                    "Filtro": {
                        "IdHashPrefeitura": "",
                        "TermoTitulo": "",
                        "TermoResumo": "",
                        "OrgaoId": "0",
                        "DataInicio": self.start_date.isoformat(),
                        "DataFim": self.end_date.isoformat(),
                        "TipoDocumento": "0",
                    },
                    "ExibirDownloadConfirmacao": False,
                    "TableSort": "",
                    "StrPaginacao": {
                        "MaxRecord": 50,
                        "StartIndex": start_index,
                        "IndexPagAtual": 1,
                        "NumPaginas": "1",
                        "TotalCount": 0,
                        "TextItens": "",
                        "ListRegPagPaginacao": {"List": []},
                        "SelNumRegPorPagina": 50,
                        "SelPagPaginacao": 1,
                    },
                    "DownloadArquivo": {
                        "NomeArquivo": "",
                        "TamanhoArquivo": "",
                        "ConteudoArquivo": None,
                        "IdDadosPublicacao": "0",
                    },
                    "LimpaPesquisa": False,
                    "DataSiteKey": "",
                    "Secret": "",
                    "DadosPublicacao_Id": "0",
                    "EnableButtonPesquisar": False,
                    "ShowSpinner": False,
                    "ShowOrgao": True,
                    "Hash": self.HASH_PREFEITURA,
                    "_hashInDataFetchStatus": 1,
                }
            },
            "inputParameters": {
                "StartIndex": start_index,
                "MaxRecords": 50,
            },
            "clientVariables": {
                "CpfLogado": "",
                "Perfil": "",
                "NomeUsuario": "",
                "IsLogado": False,
                "HashEntidade": self.HASH_PREFEITURA,
                "NomePrefeitura": "",
                "ResponseToken": "",
                "PrefeituraId": "7",
                "PerfilOriginal": "",
                "IsEntidadePublica": False,
            },
        }

        return scrapy.Request(
            url=endpoint,
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse,
            meta={"start_index": start_index},
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response) -> Generator[Any, None, None]:
        """Processa a resposta JSON do SERPRO com a lista de diários oficiais."""
        data = json.loads(response.text)
        data_block = data.get("data", {})
        total_count = data_block.get("Count", 0)

        raw_list = data_block.get("List", {})
        if isinstance(raw_list, dict):
            items = raw_list.get("List", [])
        else:
            items = raw_list or []

        for item in items:
            pub = item.get("TB_DadosPublicacao", {})
            pub_id = pub.get("Id")
            raw_date = pub.get("Dap_DataPublicacao")
            title = pub.get("Dap_Titulo", "")
            summary = pub.get("Dap_ResumoPublicacao", "")

            if not pub_id or not raw_date:
                continue

            # Parsing seguro da data (formato ISO 8601 UTC)
            date_part = raw_date.split("T")[0]
            gazette_date = dt.datetime.strptime(date_part, "%Y-%m-%d").date()

            # Encerra paginação se atingir datas anteriores ao start_date solicitado
            if gazette_date < self.start_date:
                return
            if gazette_date > self.end_date:
                continue

            edition_number = self._extract_edition_number(title)
            is_extra = "extra" in title.lower() or "extra" in summary.lower()

            # Dispara requisição direta ao endpoint de arquivo do SERPRO
            download_url = (
                f"{self.BASE_URL}/screenservices/govbrcidades_doe/"
                f"ActionBuscaArquivoPublicacao"
            )
            download_payload = {
                "versionInfo": {
                    "moduleVersion": "n+Mjd8q_ahkeNIkyYfbTNA",
                    "apiVersion": "p6Pwyi8dX2Lf8E0FKxeCTw",
                },
                "viewName": "Cidadao.DOEConsultaCidadao",
                "inputParameters": {
                    "TB_DadosPublicacaoIdentifier_Input": str(pub_id),
                    "HashPrefeitura_Input": self.HASH_PREFEITURA,
                },
            }

            gazette_meta = {
                "date": gazette_date,
                "edition_number": edition_number,
                "is_extra_edition": is_extra,
                "power": "executive",
                "pub_id": pub_id,
            }

            yield scrapy.Request(
                url=download_url,
                method="POST",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Accept": "application/json",
                    "X-CSRFToken": self.CSRF_TOKEN,
                    "Cookie": self.COOKIE_HEADER,
                    "Origin": "https://cidadesdoe.serpro.gov.br",
                    "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
                },
                body=json.dumps(download_payload),
                callback=self.parse_gazette_file,
                meta=gazette_meta,
                dont_filter=True,
            )

        # Paginação sequencial de 50 em 50 registros
        current_index = response.meta.get("start_index", 0)
        next_index = current_index + 50
        if next_index < total_count:
            yield self._build_page_request(start_index=next_index)

    def parse_gazette_file(
        self, response: scrapy.http.Response
    ) -> Generator[Gazette, None, None]:
        """
        Extrai o Base64 retornado pelo SERPRO e gera o Gazette com Data URI.
        O DataURIDownloadHandler nativo do Scrapy decodifica os bytes em memória
        e entrega o binário puro %PDF-1.7 ao QueridoDiarioFilesPipeline sem
        necessidade de infraestrutura intermediária.
        """
        meta = response.meta
        data = json.loads(response.text)
        b64_content = (
            data.get("data", {}).get("FileContent")
            or data.get("data", {}).get("Arquivo_Output")
            or ""
        )

        if not b64_content:
            self.logger.warning(
                f"Publicação #{meta['pub_id']} de {meta['date']} não retornou conteúdo de arquivo no SERPRO."
            )
            return

        pdf_data_uri = f"data:application/pdf;base64,{b64_content}"

        yield Gazette(
            date=meta["date"],
            edition_number=meta["edition_number"],
            is_extra_edition=meta["is_extra_edition"],
            power=meta["power"],
            file_urls=[pdf_data_uri],
        )

    def _extract_edition_number(self, title: str) -> Optional[str]:
        """Extrai o número da edição a partir do título."""
        match = re.search(r"n[º°\.\s]*(\d+)", title, re.IGNORECASE)
        return match.group(1) if match else None
