"""
============================================
Solución: Proyecto Semana 06
Buscador de Texto Avanzado
============================================
"""

import re
import time

# ============================================
# CONFIGURACIÓN
# ============================================

SEARCH_CONFIG = {
    'case_sensitive': False,
    'whole_word': False,
    'multiline': True,
    'dot_all': False,
    'unicode': True,
    'show_indices': True,
}

# ============================================
# UTILIDADES
# ============================================

def escape_regex(string: str) -> str:
    """
    Escapar caracteres especiales de regex

    ¿Por qué? Los caracteres como . * + tienen significado especial
    ¿Para qué? Buscar literalmente el texto del usuario
    """
    return re.sub(r'[.*+?^${}()|[\]\\]', r'\\\g<0>', string)


def build_flags(config: dict) -> int:
    """
    Construir bitmask de flags según configuración

    :param config: Configuración de búsqueda
    :returns: Flags para regex como entero bitmask
    """
    flags = 0  # No existe flag 'g' en Python; se usa findall/finditer en su lugar

    if not config['case_sensitive']:
        flags |= re.IGNORECASE
    if config['multiline']:
        flags |= re.MULTILINE
    if config['dot_all']:
        flags |= re.DOTALL
    if config['unicode']:
        flags |= re.UNICODE
    if config['show_indices']:
        # Python siempre expone .start() / .end() — no se necesita flag 'd'
        pass

    return flags


def build_pattern(query: str, config: dict) -> re.Pattern:
    """
    Construir patrón regex

    :param query: Término de búsqueda
    :param config: Configuración
    :returns: Expresión regular compilada
    """
    pattern = escape_regex(query)

    if config['whole_word']:
        # \b para límites de palabra
        pattern = rf'\b{pattern}\b'

    flags = build_flags(config)

    return re.compile(pattern, flags)


# ============================================
# MOTOR DE BÚSQUEDA
# ============================================

def buscar(texto: str, query: str, opciones: dict | None = None) -> dict:
    """
    Motor de búsqueda principal

    ¿Por qué? Centralizar toda la lógica de búsqueda
    ¿Para qué? Reutilización y mantenibilidad

    :param texto: Texto donde buscar
    :param query: Término de búsqueda
    :param opciones: Configuración
    :returns: Resultados
    """
    if opciones is None:
        opciones = {}

    config = {**SEARCH_CONFIG, **opciones}

    if not query or not texto:
        return {
            'matches': [],
            'total': 0,
            'positions': [],
            'highlighted': texto or '',
            'stats': {'duration': 0},
        }

    start_time = time.perf_counter()

    try:
        pattern = build_pattern(query, config)
        matches = []
        positions = []

        # Usar finditer para obtener toda la info (equivalente a matchAll)
        for match in pattern.finditer(texto):
            matches.append(match.group())

            if config['show_indices']:
                # Python siempre tiene .start()/.end() — no requiere flag 'd'
                positions.append({
                    'start': match.start(),
                    'end': match.end(),
                    'value': match.group(),
                })
            else:
                positions.append({
                    'start': match.start(),
                    'end': match.end(),
                    'value': match.group(),
                })

        highlighted = highlight(texto, pattern)
        duration = time.perf_counter() - start_time

        return {
            'matches': matches,
            'total': len(matches),
            'positions': positions,
            'highlighted': highlighted,
            'stats': {
                'duration': f'{duration * 1000:.2f}ms',
                'text_length': len(texto),
                'pattern': pattern.pattern,
            },
        }
    except re.error as error:
        return {
            'matches': [],
            'total': 0,
            'positions': [],
            'highlighted': texto,
            'stats': {'error': str(error)},
        }


def highlight(texto: str, pattern: re.Pattern) -> str:
    """
    Resaltar coincidencias en el texto

    :param texto: Texto original
    :param pattern: Patrón de búsqueda
    :returns: Texto con marcadores
    """
    return pattern.sub(r'[[MATCH]]\g<0>[[/MATCH]]', texto)


def highlight_to_html(texto: str) -> str:
    """
    Convertir marcadores a HTML
    """
    return (
        texto
        .replace('[[MATCH]]', '<mark class="highlight">')
        .replace('[[/MATCH]]', '</mark>')
    )


# ============================================
# BÚSQUEDA AVANZADA
# ============================================

def parse_query(query_string: str) -> dict:
    """
    Parsear query con sintaxis avanzada

    Soporta:
    - "frase exacta"
    - palabra1 palabra2 (AND implícito)
    - palabra1 OR palabra2
    - -excluir
    - palabra* (wildcard)

    :param query_string: Query del usuario
    :returns: Componentes parseados
    """
    parts = {
        'exact': [],
        'include': [],
        'exclude': [],
        'wildcard': [],
        'or': [],
    }

    remaining = query_string

    # 1. Extraer frases exactas "..."
    exact_pattern = re.compile(r'"([^"]+)"')
    for match in exact_pattern.finditer(remaining):
        parts['exact'].append(match.group(1))
    remaining = exact_pattern.sub(' ', remaining)

    # 2. Extraer exclusiones -palabra
    exclude_pattern = re.compile(r'-(\w+)')
    for match in exclude_pattern.finditer(remaining):
        parts['exclude'].append(match.group(1))
    remaining = exclude_pattern.sub(' ', remaining)

    # 3. Extraer wildcards palabra*
    wildcard_pattern = re.compile(r'(\w+)\*')
    for match in wildcard_pattern.finditer(remaining):
        parts['wildcard'].append(match.group(1))
    remaining = wildcard_pattern.sub(' ', remaining)

    # 4. Procesar OR
    or_pattern = re.compile(r'(\w+)\s+OR\s+(\w+)', re.IGNORECASE)
    for match in or_pattern.finditer(remaining):
        parts['or'].append([match.group(1), match.group(2)])
    remaining = or_pattern.sub(' ', remaining)

    # 5. El resto son palabras a incluir (AND)
    words = [w for w in remaining.strip().split() if w]
    parts['include'].extend(words)

    return parts


def busqueda_avanzada(texto: str, query_string: str, opciones: dict | None = None) -> dict:
    """
    Búsqueda avanzada con sintaxis especial

    :param texto: Texto donde buscar
    :param query_string: Query con sintaxis
    :param opciones: Configuración base
    :returns: Resultados
    """
    if opciones is None:
        opciones = {}

    config = {**SEARCH_CONFIG, **opciones}
    parsed = parse_query(query_string)
    resultados = []
    texto_filtrado = texto

    # Verificar exclusiones primero
    for excluir in parsed['exclude']:
        pattern = re.compile(rf'\b{escape_regex(excluir)}\b', re.IGNORECASE)
        if pattern.search(texto):
            # Si contiene palabra excluida, podría filtrar líneas
            lineas = texto.splitlines()
            texto_filtrado = '\n'.join(
                linea for linea in lineas if not pattern.search(linea)
            )

    # Buscar frases exactas
    for frase in parsed['exact']:
        resultado = buscar(texto_filtrado, frase, config)
        if resultado['total'] > 0:
            resultados.append({
                'type': 'exact',
                'query': frase,
                **resultado,
            })

    # Buscar wildcards
    for base in parsed['wildcard']:
        pattern = re.compile(rf'\b{escape_regex(base)}\w*\b', re.IGNORECASE)
        found = pattern.findall(texto_filtrado)
        resultados.append({
            'type': 'wildcard',
            'query': base + '*',
            'matches': list(set(found)),
            'total': len(found),
        })

    # Buscar OR
    for a, b in parsed['or']:
        pattern = re.compile(
            rf'\b(?:{escape_regex(a)}|{escape_regex(b)})\b',
            re.IGNORECASE,
        )
        found = pattern.findall(texto_filtrado)
        resultados.append({
            'type': 'or',
            'query': f'{a} OR {b}',
            'matches': found,
            'total': len(found),
        })

    # Buscar palabras individuales (AND)
    for palabra in parsed['include']:
        resultado = buscar(texto_filtrado, palabra, {
            **config,
            'whole_word': True,
        })
        if resultado['total'] > 0:
            resultados.append({
                'type': 'include',
                'query': palabra,
                **resultado,
            })

    # Verificar que todas las palabras include estén presentes (AND)
    todas_presentes = all(
        re.compile(rf'\b{escape_regex(palabra)}\b', re.IGNORECASE).search(texto_filtrado)
        for palabra in parsed['include']
    )

    return {
        'parsed': parsed,
        'resultados': resultados,
        'todas_presentes': todas_presentes,
        'texto_filtrado': texto_filtrado,
    }


# ============================================
# UTILIDADES ADICIONALES
# ============================================

def get_contexto(texto: str, posicion: int, caracteres: int = 50) -> str:
    """
    Obtener contexto alrededor de un match

    :param texto: Texto completo
    :param posicion: Posición del match
    :param caracteres: Caracteres de contexto
    :returns: Fragmento con contexto
    """
    start = max(0, posicion - caracteres)
    end = min(len(texto), posicion + caracteres)

    contexto = texto[start:end]

    if start > 0:
        contexto = '...' + contexto
    if end < len(texto):
        contexto = contexto + '...'

    return contexto


def get_lineas_contexto(texto: str, posicion: int, lineas: int = 2) -> dict:
    """
    Obtener líneas alrededor de un match

    :param texto: Texto completo
    :param posicion: Posición del match
    :param lineas: Líneas de contexto
    :returns: Líneas con contexto
    """
    todas_lineas = texto.splitlines()

    # Encontrar número de línea
    char_count = 0
    linea_actual = 0

    for i, linea in enumerate(todas_lineas):
        char_count += len(linea) + 1  # +1 por \n
        if char_count > posicion:
            linea_actual = i
            break

    inicio = max(0, linea_actual - lineas)
    fin = min(len(todas_lineas), linea_actual + lineas + 1)

    return {
        'lineas': todas_lineas[inicio:fin],
        'numero_linea_match': linea_actual,
        'rango': [inicio, fin],
    }


# ============================================
# TESTS
# ============================================

texto_ejemplo = """JavaScript es un lenguaje de programación.
JavaScript se usa para desarrollo web.
También se usa en Node.js para backend.
Python es otro lenguaje popular.
javascript puede ejecutarse en el navegador.
Los frameworks como React usan JavaScript."""

print('=== Búsqueda Simple ===\n')

resultado1 = buscar(texto_ejemplo, 'JavaScript')
print(f"Buscar 'JavaScript': {resultado1['total']} coincidencias")
print(f"Matches: {resultado1['matches']}")

print('\n=== Búsqueda Case-Sensitive ===\n')

resultado2 = buscar(texto_ejemplo, 'JavaScript', {'case_sensitive': True})
print(f"Buscar 'JavaScript' (case-sensitive): {resultado2['total']}")

resultado3 = buscar(texto_ejemplo, 'javascript', {'case_sensitive': True})
print(f"Buscar 'javascript' (case-sensitive): {resultado3['total']}")

print('\n=== Búsqueda Palabra Completa ===\n')

resultado4 = buscar(texto_ejemplo, 'Java', {'whole_word': True})
print(f"Buscar 'Java' (whole word): {resultado4['total']}")

resultado5 = buscar(texto_ejemplo, 'Java', {'whole_word': False})
print(f"Buscar 'Java' (parcial): {resultado5['total']}")

print('\n=== Búsqueda Avanzada ===\n')

query1 = '"desarrollo web" JavaScript -Python'
print(f'Query: {query1}')
print(busqueda_avanzada(texto_ejemplo, query1))

print('\n=== Contexto de Matches ===\n')

resultado6 = buscar(texto_ejemplo, 'Node.js')
if resultado6['positions']:
    pos = resultado6['positions'][0]['start']
    print(f"Contexto: {get_contexto(texto_ejemplo, pos, 30)}")
    print(f"Líneas: {get_lineas_contexto(texto_ejemplo, pos, 1)}")

print('\n=== Unicode ===\n')

texto_unicode = 'Hola 👋 mundo! Привет мир! 你好世界!'
resultado7 = buscar(texto_unicode, 'мир', {'unicode': True})
print(f"Buscar 'мир' en texto Unicode: {resultado7}")
