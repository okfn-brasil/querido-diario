"""
Módulo para mapeamento de nomes de municípios para códigos IBGE.

Este módulo carrega o arquivo territories.csv e fornece funções para
normalizar nomes de municípios e encontrar seus códigos IBGE correspondentes.
"""
import csv
import os
import re
import unicodedata
from typing import Dict, Optional, List, Tuple


def remove_accents(text: str) -> str:
    """
    Remove acentos de uma string.
    
    Examples
    --------
    >>> remove_accents("São José")
    'Sao Jose'
    """
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')


def normalize_municipality_name(name: str) -> str:
    """
    Normaliza o nome de um município para facilitar matching.
    
    - Remove acentos
    - Converte para minúsculas
    - Remove espaços extras
    - Remove artigos e preposições comuns
    
    Parameters
    ----------
    name : str
        Nome do município
        
    Returns
    -------
    str
        Nome normalizado
        
    Examples
    --------
    >>> normalize_municipality_name("São José do Cedro")
    'sao jose cedro'
    >>> normalize_municipality_name("Morro da Fumaça")
    'morro fumaca'
    """
    # Remove acentos
    normalized = remove_accents(name)
    
    # Minúsculas
    normalized = normalized.lower()
    
    # Remove pontuação
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    # Remove artigos e preposições curtas (mas não "do sul", "do norte", etc)
    # Mantém "do", "da", "de" quando fazem parte de direções
    words = normalized.split()
    filtered_words = []
    
    for i, word in enumerate(words):
        # Pula artigos/preposições apenas se não forem seguidos de direções
        if word in ['da', 'de', 'do', 'dos', 'das']:
            # Verifica se a próxima palavra é uma direção
            if i + 1 < len(words) and words[i + 1] in ['sul', 'norte', 'oeste', 'leste', 'serra', 'boa']:
                filtered_words.append(word)
        else:
            filtered_words.append(word)
    
    return ' '.join(filtered_words)


def load_sc_municipalities() -> Dict[str, Dict[str, str]]:
    """
    Carrega todos os municípios de Santa Catarina do arquivo territories.csv.
    
    Returns
    -------
    Dict[str, Dict[str, str]]
        Dicionário com nome normalizado como chave e info do município como valor
        {
            'agua doce': {
                'id': '4200408',
                'name': 'Água Doce',
                'normalized': 'agua doce'
            },
            ...
        }
        
    Raises
    ------
    FileNotFoundError
        Se o arquivo territories.csv não for encontrado
    """
    # Caminho para o arquivo territories.csv
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, '..', 'resources', 'territories.csv')
    
    municipalities = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['state_code'] == 'SC':
                normalized = normalize_municipality_name(row['name'])
                municipalities[normalized] = {
                    'id': row['id'],
                    'name': row['name'],
                    'normalized': normalized
                }
    
    return municipalities


def find_territory_id(municipality_name: str, 
                     sc_territories: Optional[Dict[str, Dict[str, str]]] = None) -> Optional[str]:
    """
    Encontra o código IBGE de um município a partir de seu nome.
    
    Faz matching normalizado para lidar com variações de escrita.
    
    Parameters
    ----------
    municipality_name : str
        Nome do município como aparece no sumário do PDF
    sc_territories : Optional[Dict[str, Dict[str, str]]]
        Dicionário de territórios. Se None, carrega automaticamente
        
    Returns
    -------
    Optional[str]
        Código IBGE do município ou None se não encontrado
        
    Examples
    --------
    >>> find_territory_id("Água Doce")
    '4200408'
    >>> find_territory_id("agua doce")
    '4200408'
    >>> find_territory_id("São José")
    '4216602'
    """
    if sc_territories is None:
        sc_territories = load_sc_municipalities()
    
    normalized = normalize_municipality_name(municipality_name)
    
    # Matching exato
    if normalized in sc_territories:
        return sc_territories[normalized]['id']
    
    # Matching fuzzy - tenta sem algumas palavras
    # Útil para casos como "Morro da Fumaça" vs "Morro Fumaça"
    words = normalized.split()
    if len(words) > 2:
        # Tenta combinações menores
        for i in range(len(words)):
            partial = ' '.join(words[:i] + words[i+1:])
            if partial in sc_territories:
                return sc_territories[partial]['id']
    
    return None


def get_municipality_info(municipality_name: str,
                         sc_territories: Optional[Dict[str, Dict[str, str]]] = None) -> Optional[Dict[str, str]]:
    """
    Retorna informações completas de um município.
    
    Parameters
    ----------
    municipality_name : str
        Nome do município
    sc_territories : Optional[Dict[str, Dict[str, str]]]
        Dicionário de territórios. Se None, carrega automaticamente
        
    Returns
    -------
    Optional[Dict[str, str]]
        Dicionário com 'id', 'name', 'normalized' ou None se não encontrado
    """
    if sc_territories is None:
        sc_territories = load_sc_municipalities()
    
    normalized = normalize_municipality_name(municipality_name)
    
    return sc_territories.get(normalized)


def match_municipalities_from_summary(summary_municipalities: List[str],
                                     sc_territories: Optional[Dict[str, Dict[str, str]]] = None
                                     ) -> Tuple[Dict[str, str], List[str]]:
    """
    Faz matching de uma lista de municípios do sumário com os códigos IBGE.
    
    Parameters
    ----------
    summary_municipalities : List[str]
        Lista de nomes de municípios como aparecem no sumário
    sc_territories : Optional[Dict[str, Dict[str, str]]]
        Dicionário de territórios. Se None, carrega automaticamente
        
    Returns
    -------
    Tuple[Dict[str, str], List[str]]
        Tupla com:
        - Dicionário {nome_sumario: territory_id}
        - Lista de municípios não encontrados
        
    Examples
    --------
    >>> municipalities = ["Água Doce", "Chapecó", "Município Inexistente"]
    >>> matched, not_found = match_municipalities_from_summary(municipalities)
    >>> len(matched)
    2
    >>> len(not_found)
    1
    """
    if sc_territories is None:
        sc_territories = load_sc_municipalities()
    
    matched = {}
    not_found = []
    
    for municipality in summary_municipalities:
        territory_id = find_territory_id(municipality, sc_territories)
        if territory_id:
            matched[municipality] = territory_id
        else:
            not_found.append(municipality)
    
    return matched, not_found


# Cache para evitar recarregar o CSV múltiplas vezes
_sc_territories_cache = None


def get_cached_sc_territories() -> Dict[str, Dict[str, str]]:
    """
    Retorna municípios de SC com cache para evitar recarregar o CSV.
    
    Alias para get_cached_sc_municipalities() para manter compatibilidade.
    """
    return get_cached_sc_municipalities()


def get_cached_sc_municipalities() -> Dict[str, Dict[str, str]]:
    """
    Retorna municípios de SC com cache para evitar recarregar o CSV.
    """
    global _sc_territories_cache
    if _sc_territories_cache is None:
        _sc_territories_cache = load_sc_municipalities()
    return _sc_territories_cache


if __name__ == "__main__":
    # Testes
    print("=== Testando mapeamento de territórios ===\n")
    
    territories = load_sc_municipalities()
    print(f"Total de municípios de SC carregados: {len(territories)}\n")
    
    # Testar alguns municípios
    test_cases = [
        "Água Doce",
        "Águas de Chapecó",
        "São José",
        "São José do Cedro",
        "Morro da Fumaça",
        "Balneário Camboriú"
    ]
    
    print("Testes de matching:")
    for municipality in test_cases:
        territory_id = find_territory_id(municipality, territories)
        if territory_id:
            info = get_municipality_info(municipality, territories)
            print(f"✓ {municipality:30s} -> {territory_id} ({info['name']})")
        else:
            print(f"✗ {municipality:30s} -> NÃO ENCONTRADO")
