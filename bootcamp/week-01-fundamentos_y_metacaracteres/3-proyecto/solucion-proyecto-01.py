"""
============================================
Solución: Proyecto Semana 01
Validador de Código de Producto
============================================
"""
import re

"""
Patrón para validar código de producto
Formato: XX-000 (2 caracteres, guión, 3 caracteres)

¿Por qué? Los códigos de producto siguen un formato estándar
          que debemos validar antes de procesarlos
¿Para qué? Evitar errores en búsquedas, imports y registro de productos

Desglose del patrón:
^     → Inicio del string (anchor)
..    → Exactamente 2 caracteres (cualquiera)
-     → Guión literal
...   → Exactamente 3 caracteres (cualquiera)
$     → Fin del string (anchor)
"""
CODIGO_PATTERN = re.compile(r'^..-...$')


def validar_codigo(codigo):
    """
    Valida si un código de producto tiene el formato correcto

    ¿Por qué? Centralizar la lógica de validación en una función
    ¿Para qué? Reutilizar en múltiples partes de la aplicación

    Args:
        codigo (str): El código a validar

    Returns:
        dict: Objeto con resultado de validación
    """
    es_valido = bool(CODIGO_PATTERN.fullmatch(codigo))

    return {
        'codigo': codigo,
        'valido': es_valido,
        'mensaje': '✅ Formato correcto' if es_valido else '❌ Formato inválido',
    }


def validar_codigo_detallado(codigo):
    """
    Versión mejorada con mensajes específicos

    ¿Por qué? El usuario necesita saber QUÉ está mal, no solo que está mal
    ¿Para qué? Mejor UX y debugging más fácil

    Args:
        codigo (str): El código a validar

    Returns:
        dict: Objeto con resultado detallado
    """
    # Validar que no esté vacío
    if not codigo or len(codigo) == 0:
        return {
            'codigo': codigo,
            'valido': False,
            'mensaje': '❌ El código no puede estar vacío',
        }

    # Validar longitud total (XX-000 = 6 caracteres)
    if len(codigo) != 6:
        return {
            'codigo': codigo,
            'valido': False,
            'mensaje': f'❌ Longitud incorrecta: {len(codigo)} (esperado: 6)',
        }

    # Validar que tenga guión en posición correcta
    if codigo[2] != '-':
        return {
            'codigo': codigo,
            'valido': False,
            'mensaje': '❌ Falta el guión en la posición 3',
        }

    # Si pasa todas las validaciones
    return {
        'codigo': codigo,
        'valido': True,
        'mensaje': '✅ Formato correcto',
        'partes': {
            'prefijo': codigo[0:2],
            'numero': codigo[3:],
        },
    }


# ============================================
# CASOS DE PRUEBA
# ============================================

print('=== Validación Básica ===\n')

# Casos válidos
print(validar_codigo('AB-123'))  # ✅
print(validar_codigo('XY-999'))  # ✅
print(validar_codigo('ZZ-000'))  # ✅

print('\n--- Casos inválidos ---\n')

# Casos inválidos
print(validar_codigo('ABC-123'))  # ❌ 3 letras
print(validar_codigo('A-123'))    # ❌ 1 letra
print(validar_codigo('AB123'))    # ❌ sin guión
print(validar_codigo('AB-12'))    # ❌ 2 dígitos
print(validar_codigo('AB-1234'))  # ❌ 4 dígitos
print(validar_codigo(''))         # ❌ vacío

print('\n=== Validación Detallada ===\n')

# Pruebas con versión detallada
print(validar_codigo_detallado('AB-123'))
print(validar_codigo_detallado(''))
print(validar_codigo_detallado('ABC-123'))
print(validar_codigo_detallado('AB123'))

# ============================================
# EXTENSIÓN: Validadores adicionales
# ============================================

"""
Validador de código de categoría
Formato: CAT-00

¿Por qué? Las categorías tienen su propio formato
¿Para qué? Diferenciar categorías de productos
"""
CATEGORIA_PATTERN = re.compile(r'^CAT-..$')

"""
Validador de código de sucursal
Formato: S-000

¿Por qué? Las sucursales usan un formato más corto
¿Para qué? Identificar ubicaciones de inventario
"""
SUCURSAL_PATTERN = re.compile(r'^S-...$')


def validar_codigo_universal(codigo):
    """
    Validador universal que detecta el tipo

    ¿Por qué? A veces recibimos códigos mixtos
    ¿Para qué? Clasificar y validar en un solo paso
    """
    if CODIGO_PATTERN.fullmatch(codigo):
        return {'tipo': 'producto', 'valido': True, 'codigo': codigo}
    if CATEGORIA_PATTERN.fullmatch(codigo):
        return {'tipo': 'categoria', 'valido': True, 'codigo': codigo}
    if SUCURSAL_PATTERN.fullmatch(codigo):
        return {'tipo': 'sucursal', 'valido': True, 'codigo': codigo}
    return {'tipo': 'desconocido', 'valido': False, 'codigo': codigo}


print('\n=== Validador Universal ===\n')
print(validar_codigo_universal('AB-123'))  # producto
print(validar_codigo_universal('CAT-05'))  # categoria
print(validar_codigo_universal('S-001'))   # sucursal
print(validar_codigo_universal('XYZ'))     # desconocido
