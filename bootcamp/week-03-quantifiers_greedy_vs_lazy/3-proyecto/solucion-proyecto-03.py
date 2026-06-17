"""
============================================
Solución: Proyecto Semana 03
Extractor de Datos de Texto
============================================
"""

import re
import json
from datetime import date

# ============================================
# DOCUMENTO DE PRUEBA
# ============================================

documento = """
FACTURA #2024-0042
Fecha: 15/01/2024
Cliente: Juan Pérez (cliente@empresa.com)
Teléfono: 612 345 678

PRODUCTOS:
- Laptop Dell XPS 15        $1299.99
- Mouse Logitech MX         $79.50
- Teclado mecánico          $149
- Monitor 27" 4K            $450.00

SUBTOTAL: $1978.49
IVA (21%): $415.48
TOTAL: $2393.97

Referencia de pago: REF-20240115001
Contacto alternativo: soporte@tienda.es, 91 234 56 78

Gracias por su compra.
"""

# ============================================
# PATRONES DE EXTRACCIÓN
# ============================================

# Patrón: Precios
# Formato: $XXX.XX o $XXX (decimales opcionales)
#
# ¿Por qué? Los precios pueden o no incluir centavos
# ¿Para qué? Extraer valores monetarios para cálculos
#
# Desglose:
# \$       → Símbolo de dólar literal
# \d+      → Uno o más dígitos (parte entera)
# (\.\d{2})? → Opcional: punto + exactamente 2 dígitos (centavos)
precio_pattern = re.compile(r'\$\d+(?:\.\d{2})?')

# Patrón: Fechas
# Formato: DD/MM/YYYY
#
# ¿Por qué? Formato europeo estándar en documentos
# ¿Para qué? Identificar y parsear fechas
#
# Desglose:
# \d{2}  → Día (2 dígitos)
# \/     → Barra literal
# \d{2}  → Mes (2 dígitos)
# \/     → Barra literal
# \d{4}  → Año (4 dígitos)
fecha_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')

# Patrón: Emails
# Formato: usuario@dominio.extension
#
# ¿Por qué? Los emails tienen estructura predecible
# ¿Para qué? Extraer direcciones de contacto
#
# Desglose:
# [\w.-]+   → Usuario: letras, números, guión bajo, punto, guión
# @         → Arroba literal
# [\w.-]+   → Dominio: mismos caracteres
# \.        → Punto literal
# \w{2,}    → Extensión: 2 o más letras
email_pattern = re.compile(r'[\w.-]+@[\w.-]+\.\w{2,}')

# Patrón: Teléfonos españoles
# Formato: 9 dígitos con espacios/guiones opcionales
#
# ¿Por qué? Los teléfonos vienen en varios formatos visuales
# ¿Para qué? Normalizar y extraer números de contacto
#
# Desglose:
# [6-9]     → Primer dígito (móvil 6-7, fijo 9, servicios 8)
# \d        → Segundo dígito
# [\d\s-]{7,9} → 7-9 caracteres más (dígitos, espacios o guiones)
telefono_pattern = re.compile(r'[6-9]\d[\d\s-]{7,9}')

# Patrón: Referencias de pago
# Formato: REF-XXXXX (5 o más dígitos)
#
# ¿Por qué? Las referencias identifican transacciones
# ¿Para qué? Tracking y reconciliación de pagos
#
# Desglose:
# REF-   → Prefijo literal
# \d{5,} → 5 o más dígitos
referencia_pattern = re.compile(r'REF-\d{5,}')

# Patrón: Número de factura
# Formato: #YYYY-XXXX
#
# ¿Por qué? Las facturas tienen numeración secuencial
# ¿Para qué? Identificar documentos
factura_pattern = re.compile(r'#\d{4}-\d{4}')

# ============================================
# FUNCIONES DE EXTRACCIÓN
# ============================================


def extraer_datos(texto):
    """
    Extrae todos los datos de un documento

    ¿Por qué? Centralizar toda la lógica de extracción
    ¿Para qué? Procesar documentos de forma consistente

    Args:
        texto (str): El documento a procesar

    Returns:
        dict: Objeto con todos los datos extraídos
    """
    return {
        'facturas': factura_pattern.findall(texto),
        'precios': precio_pattern.findall(texto),
        'fechas': fecha_pattern.findall(texto),
        'emails': email_pattern.findall(texto),
        'telefonos': telefono_pattern.findall(texto),
        'referencias': referencia_pattern.findall(texto),
    }


# ============================================
# FUNCIONES DE UTILIDAD
# ============================================


def precio_a_numero(precio_str):
    """
    Convierte string de precio a número

    ¿Por qué? Los precios vienen como "$99.99"
    ¿Para qué? Hacer cálculos matemáticos

    Args:
        precio_str (str): Precio como string

    Returns:
        float: Precio como número
    """
    return float(precio_str.replace('$', ''))


def sumar_precios(precios):
    """
    Suma todos los precios extraídos

    ¿Por qué? Calcular totales es operación común
    ¿Para qué? Verificar sumas, generar reportes

    Args:
        precios (list): Lista de strings de precios

    Returns:
        float: Suma total
    """
    return sum(precio_a_numero(p) for p in precios)


def normalizar_telefonos(telefonos):
    """
    Normaliza teléfonos eliminando espacios y guiones

    ¿Por qué? Los teléfonos vienen en formatos variados
    ¿Para qué? Almacenar en formato uniforme

    Args:
        telefonos (list): Lista de teléfonos

    Returns:
        list: Teléfonos normalizados (solo dígitos)
    """
    return [re.sub(r'[\s-]', '', tel) for tel in telefonos]


def parsear_fecha(fecha_str):
    """
    Parsea fecha en formato DD/MM/YYYY a objeto date

    ¿Por qué? Las fechas como string no son útiles para cálculos
    ¿Para qué? Ordenar, comparar, formatear fechas

    Args:
        fecha_str (str): Fecha en formato DD/MM/YYYY

    Returns:
        date: Objeto date
    """
    dia, mes, anio = list(map(int, fecha_str.split('/')))
    return date(anio, mes, dia)


def validar_email(email):
    """
    Valida que un email tenga formato correcto

    ¿Por qué? La extracción puede capturar falsos positivos
    ¿Para qué? Validar antes de usar/almacenar

    Args:
        email (str): Email a validar

    Returns:
        bool: Si es válido
    """
    # Patrón más estricto
    email_estricto = re.compile(r'^[\w.-]+@[\w-]+\.[\w]{2,}(\.[\w]{2,})?$')
    return email_estricto.search(email) is not None


def validar_fecha(fecha_str):
    """
    Valida que una fecha tenga valores lógicos

    ¿Por qué? El patrón acepta fechas inválidas como 99/99/9999
    ¿Para qué? Asegurar integridad de datos

    Args:
        fecha_str (str): Fecha a validar

    Returns:
        bool: Si es válida
    """
    dia, mes, anio = list(map(int, fecha_str.split('/')))

    if mes < 1 or mes > 12:
        return False
    if dia < 1 or dia > 31:
        return False
    if anio < 1900 or anio > 2100:
        return False

    # Validación más precisa con date
    try:
        fecha = date(anio, mes, dia)
        return (
            fecha.day == dia
            and fecha.month == mes
            and fecha.year == anio
        )
    except ValueError:
        return False


# ============================================
# GENERADOR DE REPORTE
# ============================================


def generar_reporte(datos):
    """
    Genera un reporte legible de los datos extraídos

    ¿Por qué? Los datos crudos no son amigables
    ¿Para qué? Presentar información al usuario

    Args:
        datos (dict): Datos extraídos

    Returns:
        str: Reporte formateado
    """
    total_precios = sumar_precios(datos['precios'])
    telefonos_norm = normalizar_telefonos(datos['telefonos'])

    return f"""
╔══════════════════════════════════════════════════════════════╗
║              REPORTE DE EXTRACCIÓN DE DATOS                 ║
╠══════════════════════════════════════════════════════════════╣
║ FACTURAS: {', '.join(datos['facturas']) or 'Ninguna'}
║ FECHAS: {', '.join(datos['fechas']) or 'Ninguna'}
╠══════════════════════════════════════════════════════════════╣
║ PRECIOS ENCONTRADOS: {len(datos['precios'])}
║   {'  '.join(datos['precios'])}
║ TOTAL: ${total_precios:.2f}
╠══════════════════════════════════════════════════════════════╣
║ CONTACTOS:
║   Emails: {', '.join(datos['emails']) or 'Ninguno'}
║   Teléfonos: {', '.join(telefonos_norm) or 'Ninguno'}
╠══════════════════════════════════════════════════════════════╣
║ REFERENCIAS: {', '.join(datos['referencias']) or 'Ninguna'}
╚══════════════════════════════════════════════════════════════╝
    """.strip()


# ============================================
# EJECUCIÓN Y TESTS
# ============================================

print('=== Extracción de Datos ===\n')

datos = extraer_datos(documento)

print('Datos extraídos:')
print(json.dumps(datos, indent=2, ensure_ascii=False))

print('\n=== Reporte ===\n')
print(generar_reporte(datos))

print('\n=== Validaciones ===\n')

# Validar emails
print('Validación de emails:')
for email in datos['emails']:
    valido = validar_email(email)
    print(f"  {email}: {'✅' if valido else '❌'}")

# Validar fechas
print('\nValidación de fechas:')
for fecha in datos['fechas']:
    valido = validar_fecha(fecha)
    print(f"  {fecha}: {'✅' if valido else '❌'}")

# Cálculos
print('\n=== Cálculos ===\n')
print(f"Número de precios: {len(datos['precios'])}")
print(f"Suma total: ${sumar_precios(datos['precios']):.2f}")
print(f"Teléfonos normalizados: {normalizar_telefonos(datos['telefonos'])}")

# ============================================
# CASOS EDGE
# ============================================

print('\n=== Tests de Casos Edge ===\n')

casos_edge = [
    # Sin decimales
    {'texto': 'Precio: $100', 'esperado': ['$100']},
    # Con decimales
    {'texto': 'Total: $99.99', 'esperado': ['$99.99']},
    # Múltiples en línea
    {'texto': '$10 + $20 = $30', 'esperado': ['$10', '$20', '$30']},
    # Fecha inválida (el patrón la captura, la validación la rechaza)
    {'texto': 'Fecha: 99/99/9999', 'esperado': ['99/99/9999']},
    # Email con subdominio
    {'texto': 'mail@sub.dominio.com', 'esperado': ['mail@sub.dominio.com']},
]

for caso in casos_edge:
    texto = caso['texto']
    esperado = caso['esperado']
    precios = precio_pattern.findall(texto)
    fechas = fecha_pattern.findall(texto)
    emails = email_pattern.findall(texto)
    resultado = precios + fechas + emails
    ok = json.dumps(resultado) == json.dumps(esperado)
    print(f"{'✅' if ok else '❌'} \"{texto}\" → {json.dumps(resultado)}")
