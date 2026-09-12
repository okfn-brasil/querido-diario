import datetime as dt
import json
import re
from typing import Any, Generator, Optional

import urllib.parse

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
    1. Sessão inicial dinâmica para cookies e extração de versão do módulo OutSystems;
    2. Coleta metadados via API REST do SERPRO;
    3. Emite os binários do PDF através do handler nativo RFC 2397 Data URI (RFC 2397).
    www.bagetransparente.com.br
    """

    TERRITORY_ID = "4301602"
    name = "rs_bage"
    allowed_domains = ["cidadesdoe.serpro.gov.br"]

    # Data da edição inaugural do DOE eletrônico de Bagé no SERPRO
    start_date = dt.date(2024, 11, 8)

    BASE_URL = "https://cidadesdoe.serpro.gov.br/govbrcidades_doe"
    HASH_PREFEITURA = "eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="

    # Tokens e versões de fallback validados caso o endpoint de manifesto oscile
    DEFAULT_CSRF_TOKEN = "T6C+9iB49TLra4jEsMeSckDMNhQ="
    DEFAULT_MODULE_VERSION = "n+Mjd8q_ahkeNIkyYfbTNA"
    DEFAULT_API_VERSION_SEARCH = "zRAHqBwfWZSZQDXDYGpfWg"
    DEFAULT_API_VERSION_DOWNLOAD = "p6Pwyi8dX2Lf8E0FKxeCTw"

    # URL inicial para abertura de sessão e inicialização de cookies via Scrapy
    start_urls = [
        f"https://cidadesdoe.serpro.gov.br/govbrcidades_doe/DoeConsultaCidadao?&Hash=eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="
    ]

    def parse(self, response: scrapy.http.Response) -> Generator[scrapy.Request, None, None]:
        """
        Recebe a resposta da página inicial pública, preservando os cookies da sessão
        no CookieJar do Scrapy e requisita o manifesto para validação dinâmica de versão.
        """
        csrf_token = self.DEFAULT_CSRF_TOKEN
        set_cookies = response.headers.getlist("Set-Cookie")
        for cookie_raw in set_cookies:
            cookie_str = urllib.parse.unquote(cookie_raw.decode("utf-8", errors="ignore"))
            match = re.search(r"crf=([^;]+)", cookie_str)
            if match:
                csrf_token = match.group(1)
                break

        manifest_url = f"{self.BASE_URL}/moduleservices/moduleinfo"
        yield scrapy.Request(
            url=manifest_url,
            callback=self.parse_module_info,
            meta={"csrf_token": csrf_token},
            dont_filter=True,
        )

    def parse_module_info(
        self, response: scrapy.http.Response
    ) -> Generator[scrapy.Request, None, None]:
        """
        Extrai dinamicamente o versionToken do OutSystems e inicia a listagem de diários.
        """
        csrf_token = response.meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)
        module_version = self.DEFAULT_MODULE_VERSION

        try:
            info = json.loads(response.text)
            token = info.get("manifest", {}).get("versionToken")
            if token:
                module_version = token
        except Exception:
            self.logger.warning(
                "Falha ao decodificar moduleinfo do SERPRO. Utilizando versão padrão validada."
            )

        yield self._build_page_request(
            start_index=0,
            module_version=module_version,
            csrf_token=csrf_token,
        )

    def _build_page_request(
        self, start_index: int, module_version: str, csrf_token: str
    ) -> scrapy.Request:
        """Monta a requisição POST de busca com paginação e parâmetros validados."""
        endpoint = (
            f"{self.BASE_URL}/screenservices/govbrcidades_doe/Cidadao/"
            f"DOEConsultaCidadao/ScreenDataSetGetTBDadosPublicacaoByDapIdHashPrefeitura"
        )

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "X-CSRFToken": csrf_token,
            "Origin": "https://cidadesdoe.serpro.gov.br",
            "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        }

        payload = {
            "versionInfo": {
                "moduleVersion": module_version,
                "apiVersion": self.DEFAULT_API_VERSION_SEARCH,
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
            callback=self.parse_gazette_list,
            meta={
                "start_index": start_index,
                "module_version": module_version,
                "csrf_token": csrf_token,
            },
            dont_filter=True,
        )

    def parse_gazette_list(
        self, response: scrapy.http.Response
    ) -> Generator[Any, None, None]:
        """Processa a resposta JSON do SERPRO com a lista de diários oficiais."""
        module_version = response.meta.get("module_version", self.DEFAULT_MODULE_VERSION)
        csrf_token = response.meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("Resposta inválida (não JSON) recebida na listagem do SERPRO.")
            return

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

            # Parsing seguro da data (formato ISO 8601 UTC) com proteção contra falhas
            try:
                date_part = str(raw_date).split("T")[0]
                gazette_date = dt.datetime.strptime(date_part, "%Y-%m-%d").date()
            except (ValueError, IndexError, AttributeError):
                self.logger.warning(f"Formato de data inválido para publicação #{pub_id}: {raw_date}")
                continue

            # Encerra paginação imediatamente se atingir datas anteriores ao start_date
            if gazette_date < self.start_date:
                return
            if gazette_date > self.end_date:
                continue

            edition_number = self._extract_edition_number(title)
            is_extra = "extra" in title.lower() or "extra" in summary.lower()

            download_url = (
                f"{self.BASE_URL}/screenservices/govbrcidades_doe/"
                f"ActionBuscaArquivoPublicacao"
            )
            download_payload = {
                "versionInfo": {
                    "moduleVersion": module_version,
                    "apiVersion": self.DEFAULT_API_VERSION_DOWNLOAD,
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

            # Prioridade alta (priority=20) para descarregar o PDF da memória antes de ler mais páginas
            yield scrapy.Request(
                url=download_url,
                method="POST",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Accept": "application/json",
                    "X-CSRFToken": csrf_token,
                    "Origin": "https://cidadesdoe.serpro.gov.br",
                    "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
                },
                body=json.dumps(download_payload),
                callback=self.parse_gazette_file,
                meta=gazette_meta,
                priority=20,
                dont_filter=True,
            )

        # Paginação com prioridade padrão (priority=1) para evitar acúmulo de requisições na fila
        current_index = response.meta.get("start_index", 0)
        next_index = current_index + 50
        if next_index < total_count:
            yield self._build_page_request(
                start_index=next_index,
                module_version=module_version,
                csrf_token=csrf_token,
            )

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

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error(
                f"Resposta corrompida (não JSON) ao baixar publicação #{meta.get('pub_id')}."
            )
            return

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
