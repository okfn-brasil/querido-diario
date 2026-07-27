#!/usr/bin/env python
"""
Script para analisar a estrutura do PDF da edição geral do CIGA/SC
e extrair informações sobre os municípios que publicaram.
"""
import pdfplumber
import re
import sys


def extract_municipalities_from_summary(pdf_path):
    """
    Extrai a lista de municípios e suas respectivas páginas do sumário.
    
    O sumário do DOM/SC lista todos os municípios que publicaram naquela
    edição, com o nome do município seguido de pontos e o número da página.
    """
    with pdfplumber.open(pdf_path) as pdf:
        # O sumário está nas primeiras páginas (geralmente 1-2)
        sumario_text = ""
        for i in range(min(3, len(pdf.pages))):
            page_text = pdf.pages[i].extract_text()
            if "SUMÁRIO" in page_text:
                sumario_text += page_text
        
        # Padrão para capturar: Nome do município ... Número da página
        # Exemplo: "Água Doce .........3"
        pattern = r'([A-ZÀÁÂÃÇÉÊÍÓÔÕÚ][a-zàáâãçéêíóôõú]+(?:\s+[A-ZÀÁÂÃÇÉÊÍÓÔÕÚ]?[a-zàáâãçéêíóôõú]+)*)\s+\.+\s*(\d+)'
        
        municipios = re.findall(pattern, sumario_text)
        
        # Limpar e organizar
        municipios_dict = {}
        for nome, pagina in municipios:
            nome_limpo = nome.strip()
            # Filtrar entradas que não são municípios (como "Florianópolis/SC")
            if '/' not in nome_limpo and len(nome_limpo) > 2:
                municipios_dict[nome_limpo] = int(pagina)
        
        return municipios_dict


def get_municipality_from_page(page_text):
    """
    Extrai o nome do município de uma página de conteúdo.
    
    O nome do município aparece isolado em uma linha, geralmente
    após o cabeçalho com data e número da edição.
    """
    lines = page_text.split('\n')
    for i, line in enumerate(lines):
        # O nome do município geralmente aparece nas primeiras linhas
        # após a data e número da edição
        if re.match(r'^[A-Z][a-zà-ú]+(?:\s+[A-Z]?[a-zà-ú]+)*$', line.strip()):
            if i < 10:  # Nas primeiras linhas
                return line.strip()
    return None


if __name__ == "__main__":
    pdf_path = '1768412435_edicao_5040_assinada.pdf'
    
    print("="*70)
    print("ANÁLISE DA ESTRUTURA DO PDF - DOM/SC EDIÇÃO GERAL")
    print("="*70)
    
    municipios = extract_municipalities_from_summary(pdf_path)
    
    print(f"\n=== MUNICÍPIOS EXTRAÍDOS DO SUMÁRIO ===")
    print(f"\nTotal de municípios: {len(municipios)}\n")
    
    # Mostrar todos organizados
    sorted_municipios = sorted(municipios.items(), key=lambda x: x[1])
    for nome, pagina in sorted_municipios:
        print(f"  {nome:40s} -> Página {pagina:4d}")
    
    print(f"\n\n=== VERIFICAÇÃO DE ALGUMAS PÁGINAS ===\n")
    
    # Verificar algumas páginas específicas
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in [3, 50, 100, 200]:
            if page_num <= len(pdf.pages):
                text = pdf.pages[page_num-1].extract_text()
                mun = get_municipality_from_page(text)
                print(f"Página {page_num:4d}: Município identificado = {mun}")
    
    print("\n" + "="*70)
    print("CONCLUSÃO:")
    print("="*70)
    print("""
O PDF da Edição Geral do DOM/SC possui a seguinte estrutura:

1. PÁGINAS 1-2: SUMÁRIO
   - Lista todos os municípios que publicaram naquela edição
   - Formato: Nome do Município ........... Número da Página
   
2. PÁGINAS 3+: CONTEÚDO DAS PUBLICAÇÕES
   - Cada município tem uma seção começando com seu nome
   - Seguido de "Prefeitura" ou "Câmara"
   - Depois as publicações oficiais (decretos, leis, editais, etc.)

ESTRATÉGIA DE EXTRAÇÃO:
- Baixar o PDF da edição geral
- Extrair o sumário das primeiras páginas
- Parsear a lista de municípios usando regex
- Para cada município, podemos:
  a) Apenas listar quais municípios publicaram naquele dia
  b) Extrair o conteúdo específico de cada município (páginas indicadas)
  c) Dividir o PDF em arquivos separados por município
""")
