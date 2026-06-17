"""
============================================
Solución: Proyecto Semana 07
Linter de Código Simple (Python Edition)
============================================
"""

import re
import json

# ============================================
# REGLAS
# ============================================

rules = {
    # Regla: no-print
    #
    # ¿Por qué? print() no debe estar en producción
    # ¿Para qué? Código limpio y sin logs de debug
    'no-print': {
        'id': 'no-print',
        'description': 'Unexpected print() call',
        'severity': 'warning',
        'pattern': re.compile(r'\bprint\s*\('),
    },

    # Regla: is-comparison
    #
    # ¿Por qué? == con None/True/False no verifica identidad
    # ¿Para qué? Usar 'is' para comparar con singleton
    'is-comparison': {
        'id': 'is-comparison',
        'description': "Use 'is' instead of '==' with None/True/False",
        'severity': 'error',
        'pattern': re.compile(r'==\s*(?:None|True|False)\b'),
        'fix': lambda m: m.replace('==', 'is'),
    },

    # Regla: isnot-comparison
    #
    # ¿Por qué? != con None/True/False no verifica identidad
    # ¿Para qué? Usar 'is not' para comparar con singleton
    'isnot-comparison': {
        'id': 'isnot-comparison',
        'description': "Use 'is not' instead of '!=' with None/True/False",
        'severity': 'error',
        'pattern': re.compile(r'!=\s*(?:None|True|False)\b'),
        'fix': lambda m: m.replace('!=', 'is not'),
    },

    # Regla: no-magic-numbers
    #
    # ¿Por qué? Números sin contexto son difíciles de entender
    # ¿Para qué? Código más legible
    'no-magic-numbers': {
        'id': 'no-magic-numbers',
        'description': 'Magic number detected',
        'severity': 'warning',
        'pattern': re.compile(r'(?<=[+\-*/%<>=])\s*(?!0|1|-1|2)\d{2,}(?!\d)'),
    },

    # Regla: no-todo
    #
    # ¿Por qué? TODOs pendientes indican trabajo incompleto
    # ¿Para qué? Tracking de deuda técnica
    'no-todo': {
        'id': 'no-todo',
        'description': 'Unresolved TODO/FIXME comment',
        'severity': 'info',
        'pattern': re.compile(r'#\s*(TODO|FIXME|HACK|XXX):?\s*.*', re.IGNORECASE),
    },

    # Regla: no-eval
    #
    # ¿Por qué? eval()/exec() es peligroso y lento
    # ¿Para qué? Seguridad del código
    'no-eval': {
        'id': 'no-eval',
        'description': 'Dangerous use of eval() or exec()',
        'severity': 'error',
        'pattern': re.compile(r'\b(?:eval|exec)\s*\('),
    },

    # Regla: max-line-length
    #
    # ¿Por qué? Líneas largas son difíciles de leer
    # ¿Para qué? Legibilidad (PEP 8: 79 caracteres)
    'max-line-length': {
        'id': 'max-line-length',
        'description': 'Line exceeds maximum length',
        'severity': 'warning',
        'max_length': 79,
    },

    # Regla: no-debugger
    #
    # ¿Por qué? breakpoint() no debe estar en producción
    # ¿Para qué? Código limpio
    'no-debugger': {
        'id': 'no-debugger',
        'description': 'Unexpected breakpoint() call',
        'severity': 'error',
        'pattern': re.compile(r'\b(?:breakpoint\s*\(|pdb\.set_trace\s*\()'),
    },

    # Regla: no-global
    #
    # ¿Por qué? global tiene scoping problemático
    # ¿Para qué? Evitar efectos secundarios globales
    'no-global': {
        'id': 'no-global',
        'description': 'Unexpected global, avoid global state',
        'severity': 'warning',
        'pattern': re.compile(r'\bglobal\s+\w+'),
    },

    # Regla: bare-except
    #
    # ¿Por qué? except: captura todas las excepciones, incluida SystemExit
    # ¿Para qué? Mejor especificar el tipo de excepción
    'bare-except': {
        'id': 'bare-except',
        'description': 'Bare except clause',
        'severity': 'warning',
        'pattern': re.compile(r'\bexcept\s*:'),
    },
}

# ============================================
# UTILIDADES
# ============================================

def get_position(code, index):
    """
    Obtener posición (línea y columna) desde índice.

    Args:
        code: Código fuente.
        index: Índice del match.

    Returns:
        dict con 'line' y 'column'.
    """
    before = code[:index]
    lines = before.split('\n')
    return {
        'line': len(lines),
        'column': len(lines[-1]) + 1,
    }


def is_in_comment(code, index):
    """
    Verificar si posición está en comentario.

    Args:
        code: Código fuente.
        index: Índice a verificar.

    Returns:
        True si la posición está dentro de un comentario.
    """
    # Buscar # antes en la misma línea
    line_start = code.rfind('\n', 0, index) + 1
    before_on_line = code[line_start:index]

    if '#' in before_on_line:
        return True

    # Buscar triple quotes (docstrings / comentarios multilínea)
    before = code[:index]
    triple_single = before.count("'''")
    triple_double = before.count('"""')

    return (triple_single % 2 == 1) or (triple_double % 2 == 1)


def is_in_string(code, index):
    """
    Verificar si posición está en string literal.

    Args:
        code: Código fuente.
        index: Índice a verificar.

    Returns:
        True si la posición está dentro de un string.
    """
    before = code[:index]
    single_quotes = before.count("'")
    double_quotes = before.count('"')

    return single_quotes % 2 == 1 or double_quotes % 2 == 1


def has_ignore_comment(code, line):
    """
    Verificar si hay ignore comment en la línea anterior.

    Args:
        code: Código fuente.
        line: Número de línea (1-based).

    Returns:
        True si la línea anterior tiene # linter-ignore-next-line.
    """
    lines = code.splitlines()
    if line < 2:
        return False

    prev_line = lines[line - 2]  # line es 1-based
    return bool(re.search(r'#\s*linter-ignore-next-line', prev_line))


# ============================================
# LINTER
# ============================================

def lint(code, options=None):
    """
    Linter principal.

    Args:
        code: Código a analizar.
        options: Configuración opcional (dict con 'rules', 'max_line_length').

    Returns:
        Lista de resultados (dicts con rule_id, message, severity, line, column,
        source, match).
    """
    if options is None:
        options = {}

    results = []
    enabled_rules = options.get('rules', list(rules.keys()))
    lines = code.splitlines()

    # Reglas que ignoran matches dentro de comentarios o strings
    codependent_rules = [
        'no-print', 'is-comparison', 'isnot-comparison',
        'no-eval', 'no-debugger', 'no-global', 'bare-except',
    ]

    for rule_id in enabled_rules:
        rule = rules.get(rule_id)
        if not rule:
            continue

        # Regla especial: max-line-length
        if rule_id == 'max-line-length':
            max_length = options.get('max_line_length', rule['max_length'])

            for idx, line in enumerate(lines):
                if len(line) > max_length:
                    line_num = idx + 1
                    if not has_ignore_comment(code, line_num):
                        results.append({
                            'ruleId': rule['id'],
                            'message': f"{rule['description']} ({len(line)} > {max_length})",
                            'severity': rule['severity'],
                            'line': line_num,
                            'column': max_length + 1,
                            'source': line[:50] + '...',
                        })
            continue

        # Reglas con patrón
        pattern = rule.get('pattern')
        if not pattern:
            continue

        for match in pattern.finditer(code):
            index = match.start()

            # Ignorar si está en comentario o string (según regla)
            if rule_id in codependent_rules:
                if is_in_comment(code, index) or is_in_string(code, index):
                    continue

            pos = get_position(code, index)

            # Verificar ignore comment
            if has_ignore_comment(code, pos['line']):
                continue

            # Obtener línea fuente
            source_line = lines[pos['line'] - 1]

            results.append({
                'ruleId': rule['id'],
                'message': rule['description'],
                'severity': rule['severity'],
                'line': pos['line'],
                'column': pos['column'],
                'source': source_line.strip(),
                'match': match.group(),
            })

    # Ordenar por línea
    results.sort(key=lambda r: (r['line'], r['column']))

    return results


# ============================================
# FORMATEO
# ============================================

def format_results(results, filename='input.py'):
    """
    Formatear resultados para consola.

    Args:
        results: Resultados del linter.
        filename: Nombre del archivo.

    Returns:
        String formateado con los resultados.
    """
    if not results:
        return f'✓ {filename}: No problems found'

    output_lines = [f'\n{filename}']

    severity_icons = {
        'error': '🔴',
        'warning': '🟡',
        'info': '🔵',
    }

    for result in results:
        icon = severity_icons[result['severity']]
        location = f"{result['line']}:{result['column']}".ljust(8)
        severity = result['severity'].ljust(8)
        message = result['message'].ljust(40)
        rule = result['ruleId']

        output_lines.append(
            f'  {location} {icon} {severity} {message} {rule}'
        )

    errors = sum(1 for r in results if r['severity'] == 'error')
    warnings = sum(1 for r in results if r['severity'] == 'warning')

    output_lines.append('')
    output_lines.append(
        f'✖ {len(results)} problems ({errors} errors, {warnings} warnings)'
    )

    return '\n'.join(output_lines)


def format_json(results, filename):
    """
    Formatear resultados como JSON.

    Args:
        results: Resultados del linter.
        filename: Nombre del archivo.

    Returns:
        String JSON con los resultados.
    """
    return json.dumps(
        {
            'filename': filename,
            'problems': results,
            'summary': {
                'total': len(results),
                'errors': sum(1 for r in results if r['severity'] == 'error'),
                'warnings': sum(1 for r in results if r['severity'] == 'warning'),
                'info': sum(1 for r in results if r['severity'] == 'info'),
            },
        },
        indent=2,
        ensure_ascii=False,
    )


# ============================================
# AUTO-FIX
# ============================================

def auto_fix(code, results):
    """
    Aplicar correcciones automáticas.

    Args:
        code: Código original.
        results: Resultados del linter.

    Returns:
        dict con 'code' (código corregido) y 'fixed' (número de correcciones).
    """
    fixed = 0
    new_code = code

    fixable_rules = ['is-comparison', 'isnot-comparison']

    for rule_id in fixable_rules:
        rule = rules.get(rule_id)
        if not rule or 'fix' not in rule:
            continue

        # Procesar matches en reversa para preservar índices
        matches = list(rule['pattern'].finditer(new_code))
        for match in reversed(matches):
            idx = match.start()
            if is_in_comment(code, idx) or is_in_string(code, idx):
                continue
            fixed += 1
            replacement = rule['fix'](match.group())
            new_code = new_code[:idx] + replacement + new_code[match.end():]

    return {'code': new_code, 'fixed': fixed}


# ============================================
# DEMO
# ============================================

if __name__ == '__main__':
    test_code = '''
# TODO: Refactor this function
def calculate_total(items):
    """Calculate totals with tax."""
    global total
    total = 0
    
    for i in range(len(items)):
        if items[i].price == None:
            continue
        
        total = total + items[i].price * 42  # Magic number: tax multiplier
        
        print("Item:", items[i])
    
    if total != None:
        # linter-ignore-next-line
        print("Total:", total)
    
    breakpoint()
    
    try:
        risky()
    except:
        pass
    
    eval("alert('done')")
    
    return total

# This line is intentionally very long to trigger the max-line-length rule because it exceeds seventy nine characters
'''

    print('=== Linter Demo ===\n')
    print('Input Code:')
    print('-' * 50)
    print(test_code)
    print('-' * 50)

    results = lint(test_code)
    print(format_results(results, 'demo.py'))

    print('\n\n=== Auto-Fix Demo ===\n')
    fix_result = auto_fix(test_code, results)
    print(f"Fixed {fix_result['fixed']} problems")
    print('-' * 50)
    print(fix_result['code'])
    print('-' * 50)

    # Verificar mejoras
    new_results = lint(fix_result['code'])
    print(f"\nProblems: {len(results)} → {len(new_results)}")
