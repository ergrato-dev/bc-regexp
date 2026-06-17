"""
============================================
Solución: Proyecto Semana 02
Validador de Datos de Contacto
============================================
"""

import re

# ============================================
# PATRONES DE VALIDACIÓN
# ============================================

# Patrón: Código de empleado
# Formato: 2 letras mayúsculas + 4 dígitos
#
# ¿Por qué? El código identifica únicamente a cada empleado en el sistema
# ¿Para qué? Validar antes de consultas a BD, evitar errores de formato
#
# Desglose:
# ^        → Inicio del string
# [A-Z]    → Primera letra mayúscula
# [A-Z]    → Segunda letra mayúscula
# \d       → Primer dígito
# \d       → Segundo dígito
# \d       → Tercer dígito
# \d       → Cuarto dígito
# $        → Fin del string
patron_codigo_empleado = re.compile(r'^[A-Z][A-Z]\d\d\d\d$')

# Patrón: Extensión telefónica (3 dígitos)
#
# ¿Por qué? Las extensiones cortas son para departamentos principales
# ¿Para qué? Routing de llamadas internas
patron_extension_3 = re.compile(r'^\d\d\d$')

# Patrón: Extensión telefónica (4 dígitos)
#
# ¿Por qué? Las extensiones largas son para empleados individuales
# ¿Para qué? Llamadas directas a escritorio
patron_extension_4 = re.compile(r'^\d\d\d\d$')

# Patrón: Departamento
# Formato: 3 letras mayúsculas
#
# ¿Por qué? Los códigos de departamento son abreviaturas estándar
# ¿Para qué? Categorización y reportes
patron_departamento = re.compile(r'^[A-Z][A-Z][A-Z]$')

# Patrón: Inicial del nombre
# Formato: 1 letra mayúscula + punto
#
# ¿Por qué? Formato estándar para iniciales
# ¿Para qué? Identificación rápida en listados
patron_inicial = re.compile(r'^[A-Z]\.$')

# ============================================
# FUNCIONES DE VALIDACIÓN INDIVIDUALES
# ============================================


def validar_codigo_empleado(codigo):
    """Valida código de empleado.

    ¿Por qué? Centralizar la lógica de validación del código
    ¿Para qué? Reutilizar en formularios, APIs, imports

    Args:
        codigo: El código a validar

    Returns:
        dict: Resultado con valido, mensaje y detalles
    """
    if not codigo:
        return {
            'valido': False,
            'mensaje': 'El código es requerido',
            'campo': 'codigo',
        }

    if patron_codigo_empleado.search(codigo):
        return {
            'valido': True,
            'mensaje': 'Código válido',
            'campo': 'codigo',
            'partes': {
                'letras': codigo[:2],
                'numero': codigo[2:],
            },
        }

    # Detectar el error específico
    detalle = ''
    if len(codigo) != 6:
        detalle = f'Longitud incorrecta: {len(codigo)} (esperado: 6)'
    elif not re.search(r'^[A-Z][A-Z]', codigo):
        detalle = 'Debe comenzar con 2 letras mayúsculas'
    elif not re.search(r'\d\d\d\d$', codigo):
        detalle = 'Debe terminar con 4 dígitos'

    return {
        'valido': False,
        'mensaje': 'Código inválido',
        'campo': 'codigo',
        'detalle': detalle,
    }


def validar_extension(extension):
    """Valida extensión telefónica.

    ¿Por qué? Las extensiones deben ser 3 o 4 dígitos exactos
    ¿Para qué? Asegurar compatibilidad con el sistema telefónico

    Args:
        extension: La extensión a validar

    Returns:
        dict: Resultado de validación
    """
    if not extension:
        return {
            'valido': False,
            'mensaje': 'La extensión es requerida',
            'campo': 'extension',
        }

    es_3_digitos = bool(patron_extension_3.search(extension))
    es_4_digitos = bool(patron_extension_4.search(extension))

    if es_3_digitos or es_4_digitos:
        return {
            'valido': True,
            'mensaje': 'Extensión válida',
            'campo': 'extension',
            'tipo': 'departamento' if es_3_digitos else 'individual',
        }

    detalle = ''
    if len(extension) < 3:
        detalle = 'Muy corta (mínimo 3 dígitos)'
    elif len(extension) > 4:
        detalle = 'Muy larga (máximo 4 dígitos)'
    elif re.search(r'[^\d]', extension):
        detalle = 'Solo debe contener dígitos'

    return {
        'valido': False,
        'mensaje': 'Extensión inválida',
        'campo': 'extension',
        'detalle': detalle,
    }


def validar_departamento(depto):
    """Valida código de departamento.

    ¿Por qué? Los departamentos usan códigos estandarizados
    ¿Para qué? Categorización consistente en reportes

    Args:
        depto: El código de departamento

    Returns:
        dict: Resultado de validación
    """
    if not depto:
        return {
            'valido': False,
            'mensaje': 'El departamento es requerido',
            'campo': 'departamento',
        }

    if patron_departamento.search(depto):
        return {
            'valido': True,
            'mensaje': 'Departamento válido',
            'campo': 'departamento',
        }

    detalle = ''
    if len(depto) != 3:
        detalle = f'Longitud incorrecta: {len(depto)} (esperado: 3)'
    elif re.search(r'[^A-Z]', depto):
        detalle = 'Solo letras mayúsculas permitidas'

    return {
        'valido': False,
        'mensaje': 'Departamento inválido',
        'campo': 'departamento',
        'detalle': detalle,
    }


def validar_inicial(inicial):
    """Valida inicial del nombre.

    ¿Por qué? Las iniciales tienen formato específico
    ¿Para qué? Consistencia en listados y documentos

    Args:
        inicial: La inicial a validar

    Returns:
        dict: Resultado de validación
    """
    if not inicial:
        return {
            'valido': False,
            'mensaje': 'La inicial es requerida',
            'campo': 'inicial',
        }

    if patron_inicial.search(inicial):
        return {
            'valido': True,
            'mensaje': 'Inicial válida',
            'campo': 'inicial',
            'letra': inicial[0],
        }

    detalle = ''
    if len(inicial) != 2:
        detalle = 'Debe ser 1 letra mayúscula seguida de punto'
    elif not re.search(r'^[A-Z]', inicial):
        detalle = 'Debe comenzar con letra mayúscula'
    elif not inicial.endswith('.'):
        detalle = 'Debe terminar con punto "."'

    return {
        'valido': False,
        'mensaje': 'Inicial inválida',
        'campo': 'inicial',
        'detalle': detalle,
    }


# ============================================
# VALIDADOR INTEGRADO
# ============================================


def validar_contacto(contacto):
    """Valida un registro completo de contacto.

    ¿Por qué? Los formularios envían múltiples campos a la vez
    ¿Para qué? Validación completa antes de guardar en BD

    Args:
        contacto: Objeto con los datos del contacto

    Returns:
        dict: Resultado con todos los errores encontrados
    """
    resultados = {
        'codigo': validar_codigo_empleado(contacto['codigo']),
        'extension': validar_extension(contacto['extension']),
        'departamento': validar_departamento(contacto['departamento']),
        'inicial': validar_inicial(contacto['inicial']),
    }

    errores = [r for r in resultados.values() if not r['valido']]

    return {
        'valido': len(errores) == 0,
        'errores': errores,
        'resultados': resultados,
        'datos': contacto,
    }


# ============================================
# EXTENSIONES
# ============================================


def detectar_caracteres_invalidos(codigo):
    """Detecta caracteres inválidos en un código.

    ¿Por qué? Ayuda al usuario a entender qué corregir
    ¿Para qué? Mejor UX con mensajes específicos

    Args:
        codigo: El código a analizar

    Returns:
        list: Lista de caracteres inválidos
    """
    # Para código de empleado: solo A-Z y 0-9
    invalidos = re.findall(r'[^A-Z0-9]', codigo, re.IGNORECASE)
    return invalidos


def sugerir_correccion(codigo):
    """Sugiere corrección para un código.

    ¿Por qué? Reducir fricción para el usuario
    ¿Para qué? Auto-corrección de errores comunes

    Args:
        codigo: El código a corregir

    Returns:
        str: Código sugerido
    """
    return re.sub(r'[^A-Z0-9]', '', codigo.upper())[:6]


def encontrar_codigos_en_texto(texto):
    """Encuentra códigos de empleado en un texto.

    ¿Por qué? Extraer datos de documentos o mensajes
    ¿Para qué? Parsing automático de información

    Args:
        texto: Texto a analizar

    Returns:
        list: Lista de códigos encontrados
    """
    # Usar word boundary para encontrar códigos completos
    patron = re.compile(r'\b[A-Z][A-Z]\d\d\d\d\b')
    return patron.findall(texto)


# ============================================
# TESTS
# ============================================

print('=== Tests de Validación Individual ===\n')

# Código de empleado
print('Código de empleado:')
print(validar_codigo_empleado('AB1234'))  # ✅ válido
print(validar_codigo_empleado('A1234'))   # ❌ solo 1 letra
print(validar_codigo_empleado('ab1234'))  # ❌ minúsculas

# Extensión
print('\nExtensión:')
print(validar_extension('123'))   # ✅ válido (3 dígitos)
print(validar_extension('4567'))  # ✅ válido (4 dígitos)
print(validar_extension('12'))    # ❌ muy corta

# Departamento
print('\nDepartamento:')
print(validar_departamento('TIC'))  # ✅ válido
print(validar_departamento('IT'))   # ❌ muy corto
print(validar_departamento('tic'))  # ❌ minúsculas

# Inicial
print('\nInicial:')
print(validar_inicial('J.'))   # ✅ válido
print(validar_inicial('JJ.'))  # ❌ 2 letras
print(validar_inicial('J'))    # ❌ sin punto

print('\n=== Test de Validación Integrada ===\n')

# Contacto válido
contacto_valido = {
    'codigo': 'AB1234',
    'extension': '456',
    'departamento': 'TIC',
    'inicial': 'J.',
}
print('Contacto válido:')
print(validar_contacto(contacto_valido))

# Contacto con errores
contacto_invalido = {
    'codigo': 'A123',
    'extension': '12',
    'departamento': 'IT',
    'inicial': 'JJ.',
}
print('\nContacto con errores:')
print(validar_contacto(contacto_invalido))

print('\n=== Tests de Extensiones ===\n')

# Detectar inválidos
print("Caracteres inválidos en 'AB@123#':")
print(detectar_caracteres_invalidos('AB@123#'))  # ['@', '#']

# Sugerir corrección
print("\nSugerencia para 'ab-1234':")
print(sugerir_correccion('ab-1234'))  # 'AB1234'

# Encontrar en texto
texto_ejemplo = (
    'El empleado AB1234 reporta a XY5678 en el depto TIC. '
    'El código ZZ no es válido.'
)
print('\nCódigos en texto:')
print(encontrar_codigos_en_texto(texto_ejemplo))  # ['AB1234', 'XY5678']
