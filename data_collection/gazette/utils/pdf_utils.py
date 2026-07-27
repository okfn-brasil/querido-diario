"""
Utilidades para extração de informações de PDFs do DOM/SC (CIGA).

Este módulo fornece funções para extrair informações da "Edição Geral"
do Diário Oficial dos Municípios de Santa Catarina (DOM/SC), que consolida
publicações de diversos municípios em um único PDF.
"""
import io
import os
import re
import tempfile
from typing import Dict, Optional, List, Tuple

try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from pypdf import PdfReader, PdfWriter
    PYPDF_SUPPORT = True
except ImportError:
    PYPDF_SUPPORT = False


def extract_municipalities_from_pdf(pdf_path: str) -> Dict[str, int]:
    """
    Extrai a lista de municípios e suas respectivas páginas do sumário
    do PDF da Edição Geral do DOM/SC.
    
    A Edição Geral do DOM/SC contém um sumário nas primeiras páginas
    listando todos os municípios que publicaram naquela edição, no formato:
    "Nome do Município ........... Número da Página"
    
    Parameters
    ----------
    pdf_path : str
        Caminho para o arquivo PDF
        
    Returns
    -------
    Dict[str, int]
        Dicionário com nome do município como chave e número da página como valor
        
    Raises
    ------
    ImportError
        Se pdfplumber não estiver instalado
    FileNotFoundError
        Se o arquivo PDF não for encontrado
        
    Examples
    --------
    >>> municipalities = extract_municipalities_from_pdf('edicao_5040.pdf')
    >>> print(municipalities)
    {'Água Doce': 3, 'Águas de Chapecó': 29, ...}
    """
    if not PDF_SUPPORT:
        raise ImportError(
            "pdfplumber is required for PDF extraction. "
            "Install it with: pip install pdfplumber"
        )
    
    with pdfplumber.open(pdf_path) as pdf:
        # O sumário está nas primeiras páginas (geralmente 1-2)
        sumario_text = ""
        for i in range(min(3, len(pdf.pages))):
            page_text = pdf.pages[i].extract_text()
            if page_text and "SUMÁRIO" in page_text:
                sumario_text += page_text
        
        if not sumario_text:
            return {}
        
        # Padrão para capturar: Nome do município ... Número da página
        # Exemplo: "Água Doce .........3" ou "Faxinal dos Guedes.....473" (sem espaço antes dos pontos)
        # O padrão captura:
        # - Primeira letra maiúscula
        # - Seguida de letras minúsculas (incluindo acentuadas)
        # - Opcionalmente seguida de mais palavras (nome composto)
        # - Opcionalmente seguido de espaço(s)
        # - Seguido de pontos (pelo menos 2)
        # - Seguido do número da página
        pattern = r'([A-ZÀÁÂÃÇÉÊÍÓÔÕÚ][a-zàáâãçéêíóôõú]+(?:\s+[A-ZÀÁÂÃÇÉÊÍÓÔÕÚ]?[a-zàáâãçéêíóôõú]+)*)\s*\.{2,}\s*(\d+)'
        
        municipios = re.findall(pattern, sumario_text)
        
        # Limpar e organizar
        municipios_dict = {}
        for nome, pagina in municipios:
            nome_limpo = nome.strip()
            # Filtrar entradas que não são municípios
            # (como "Florianópolis/SC" que aparece no cabeçalho)
            if '/' not in nome_limpo and len(nome_limpo) > 2:
                municipios_dict[nome_limpo] = int(pagina)
        
        return municipios_dict


def get_municipality_from_page(page_text: str) -> Optional[str]:
    """
    Extrai o nome do município de uma página de conteúdo do PDF.
    
    O nome do município geralmente aparece isolado em uma linha,
    logo após o cabeçalho com data e número da edição.
    
    Parameters
    ----------
    page_text : str
        Texto extraído de uma página do PDF
        
    Returns
    -------
    Optional[str]
        Nome do município ou None se não encontrado
        
    Examples
    --------
    >>> text = pdf.pages[2].extract_text()
    >>> municipality = get_municipality_from_page(text)
    >>> print(municipality)
    'Água Doce'
    """
    if not page_text:
        return None
    
    lines = page_text.split('\n')
    for i, line in enumerate(lines):
        # O nome do município geralmente aparece nas primeiras 10 linhas
        # após o cabeçalho (data, edição, etc.)
        if i >= 10:
            break
        
        line_stripped = line.strip()
        
        # Verifica se a linha contém apenas o nome de um município
        # (primeira letra maiúscula, pode ter múltiplas palavras)
        if re.match(r'^[A-ZÀÁÂÃÇÉÊÍÓÔÕÚ][a-zàáâãçéêíóôõú]+(?:\s+[A-ZÀÁÂÃÇÉÊÍÓÔÕÚ]?[a-zàáâãçéêíóôõú]+)*$', line_stripped):
            # Não considerar palavras muito comuns que aparecem mas não são municípios
            if line_stripped not in ['Prefeitura', 'Câmara', 'Municipal', 'Estado']:
                return line_stripped
    
    return None


def extract_municipality_pages(pdf_path: str, municipality: str, 
                               start_page: int, end_page: Optional[int] = None) -> bytes:
    """
    Extrai as páginas de um município específico do PDF da Edição Geral.
    
    Esta função cria um novo PDF contendo apenas as páginas de publicações
    de um município específico.
    
    Parameters
    ----------
    pdf_path : str
        Caminho para o arquivo PDF completo
    municipality : str
        Nome do município
    start_page : int
        Página inicial do município (1-indexed)
    end_page : Optional[int]
        Página final do município. Se None, vai até a próxima seção
        
    Returns
    -------
    bytes
        Conteúdo do PDF extraído em bytes
        
    Raises
    ------
    ImportError
        Se pypdf não estiver instalado
        
    Notes
    -----
    Esta funcionalidade requer que o pypdf esteja instalado
    para manipulação de PDFs.
    """
    if not PYPDF_SUPPORT:
        raise ImportError(
            "pypdf is required for PDF extraction. "
            "Install it with: pip install pypdf"
        )
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    # Converter para 0-indexed
    start_idx = start_page - 1
    end_idx = end_page if end_page is None else end_page - 1
    
    # Se end_page não foi especificado, vai até o final
    if end_idx is None:
        end_idx = len(reader.pages) - 1
    
    # Adicionar páginas ao novo PDF
    for page_num in range(start_idx, end_idx + 1):
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    # Retornar como bytes
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()


def split_pdf_by_municipalities(pdf_path: str, 
                                municipalities_pages: Dict[str, int],
                                temp_dir: Optional[str] = None,
                                save_to_disk: bool = False) -> List[Tuple[str, int, int, bytes]]:
    """
    Fatia o PDF da Edição Geral em múltiplos PDFs, um para cada município.
    
    Esta é a função principal para processar a Edição Geral e gerar
    PDFs individuais por município.
    
    Parameters
    ----------
    pdf_path : str
        Caminho para o arquivo PDF completo da Edição Geral
    municipalities_pages : Dict[str, int]
        Dicionário com nome do município e página inicial
        Exemplo: {'Água Doce': 3, 'Chapecó': 29, ...}
    temp_dir : Optional[str]
        Diretório para salvar PDFs temporários. Se None, usa tempfile
    save_to_disk : bool
        Se True, salva os PDFs em disco (modo debug) com formato temporário.
        Se False, mantém apenas em memória (modo produção).
        **Nota:** O spider salva os PDFs com formato final correto. Este parâmetro
        deve ser False na maioria dos casos para evitar arquivos duplicados.
        
    Returns
    -------
    List[Tuple[str, int, int, bytes]]
        Lista de tuplas com:
        - nome do município
        - página inicial
        - página final
        - conteúdo do PDF em bytes
        
    Raises
    ------
    ImportError
        Se pdfplumber ou pypdf não estiverem instalados
    FileNotFoundError
        Se o arquivo PDF não for encontrado
        
    Examples
    --------
    >>> municipalities = {'Água Doce': 3, 'Chapecó': 29}
    >>> results = split_pdf_by_municipalities('edicao_5040.pdf', municipalities)
    >>> len(results)
    2
    >>> municipality, start, end, pdf_bytes = results[0]
    >>> municipality
    'Água Doce'
    """
    if not PDF_SUPPORT:
        raise ImportError(
            "pdfplumber is required for PDF extraction. "
            "Install it with: pip install pdfplumber"
        )
    
    if not PYPDF_SUPPORT:
        raise ImportError(
            "pypdf is required for PDF manipulation. "
            "Install it with: pip install pypdf"
        )
    
    # Criar diretório temporário se necessário
    if save_to_disk and temp_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="ciga_sc_split_")
    
    # Ordenar municípios por página
    sorted_municipalities = sorted(municipalities_pages.items(), key=lambda x: x[1])
    
    results = []
    
    # Processar cada município
    for i, (municipality, start_page) in enumerate(sorted_municipalities):
        # Determinar página final (início do próximo município - 1)
        if i + 1 < len(sorted_municipalities):
            end_page = sorted_municipalities[i + 1][1] - 1
        else:
            # Último município vai até o final do PDF
            with pdfplumber.open(pdf_path) as pdf:
                end_page = len(pdf.pages)
        
        # Extrair páginas do município
        pdf_bytes = extract_municipality_pages(pdf_path, municipality, start_page, end_page)
        
        # Salvar em disco se modo debug
        if save_to_disk and temp_dir:
            # Normalizar nome do arquivo
            safe_name = re.sub(r'[^\w\s-]', '', municipality).strip().replace(' ', '_')
            output_path = os.path.join(temp_dir, f"{safe_name}_{start_page}-{end_page}.pdf")
            
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
        
        results.append((municipality, start_page, end_page, pdf_bytes))
    
    return results
