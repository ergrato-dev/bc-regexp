"""
============================================
Solución: Proyecto Semana 05
Validador de Formularios Avanzado
============================================
"""

import re
import random

# ============================================
# REGLAS DE VALIDACIÓN
# ============================================

REGLAS = {
    'password': {
        'minLength': 8,
        'maxLength': 128,
        'requireUppercase': True,
        'requireLowercase': True,
        'requireDigit': True,
        'requireSpecial': True,
        'noSpaces': True,
        'noConsecutiveRepeats': 3,
    },
    'username': {
        'minLength': 3,
        'maxLength': 20,
        'mustStartWithLetter': True,
        'noConsecutiveUnderscores': True,
    },
}

PALABRAS_PROHIBIDAS = [
    'admin',
    'root',
    'system',
    'null',
    'undefined',
    'test',
    'user',
]

# ============================================
# VALIDADOR DE PASSWORD
# ============================================

# Patrón de password con todos los requisitos
#
# ¿Por qué? Múltiples reglas deben cumplirse simultáneamente
# ¿Para qué? Seguridad de cuentas de usuario
#
# Desglose:
# (?=.*[A-Z])       → Lookahead: al menos una mayúscula
# (?=.*[a-z])       → Lookahead: al menos una minúscula
# (?=.*\d)          → Lookahead: al menos un dígito
# (?=.*[!@#$%^&*]) → Lookahead: al menos un carácter especial
# (?!.*\s)          → Negative lookahead: sin espacios
# (?!.*(.)\1{2})    → Negative lookahead: sin 3 caracteres consecutivos iguales
# .{8,128}          → 8 a 128 caracteres
password_pattern = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=])'
    r'(?!.*\s)(?!.*(.)\1{2}).{8,128}$'
)


def validar_password(password: str) -> dict:
    """Valida una contraseña y retorna resultado detallado.

    Args:
        password: La contraseña a validar.

    Returns:
        Resultado con validez, errores y fortaleza.
    """
    resultado = {
        'valido': False,
        'errores': [],
        'fortaleza': 0,
    }

    # Validaciones individuales para mensajes específicos
    if len(password) < REGLAS['password']['minLength']:
        resultado['errores'].append(
            f"Debe tener al menos {REGLAS['password']['minLength']} caracteres"
        )

    if len(password) > REGLAS['password']['maxLength']:
        resultado['errores'].append(
            f"No debe superar {REGLAS['password']['maxLength']} caracteres"
        )

    if not re.search(r'[A-Z]', password):
        resultado['errores'].append('Debe contener al menos una mayúscula')

    if not re.search(r'[a-z]', password):
        resultado['errores'].append('Debe contener al menos una minúscula')

    if not re.search(r'\d', password):
        resultado['errores'].append('Debe contener al menos un dígito')

    if not re.search(r'[!@#$%^&*()_+\-=]', password):
        resultado['errores'].append(
            'Debe contener al menos un carácter especial (!@#$%^&*()_+-=)'
        )

    if re.search(r'\s', password):
        resultado['errores'].append('No debe contener espacios')

    # Caracteres consecutivos repetidos
    if re.search(r'(.)\1{2}', password):
        resultado['errores'].append(
            'No debe tener 3 o más caracteres consecutivos iguales'
        )

    # Patrón común (123, abc, qwerty)
    if re.search(r'(?:123|abc|qwerty|password)', password, re.IGNORECASE):
        resultado['errores'].append('No debe contener patrones comunes')

    resultado['valido'] = len(resultado['errores']) == 0
    resultado['fortaleza'] = calcular_fortaleza(password)

    return resultado


def calcular_fortaleza(password: str) -> int:
    """Calcula la fortaleza de una contraseña (0-100).

    Args:
        password: La contraseña.

    Returns:
        Fortaleza de 0 a 100.
    """
    fortaleza = 0

    # Longitud base
    fortaleza += min(len(password) * 4, 40)

    # Variedad de caracteres
    if re.search(r'[a-z]', password):
        fortaleza += 10
    if re.search(r'[A-Z]', password):
        fortaleza += 10
    if re.search(r'\d', password):
        fortaleza += 10
    if re.search(r'[!@#$%^&*()_+\-=]', password):
        fortaleza += 15

    # Penalizaciones
    if re.search(r'(.)\1{2}', password):
        fortaleza -= 10
    if re.search(r'^[a-zA-Z]+$', password):
        fortaleza -= 10
    if re.search(r'^\d+$', password):
        fortaleza -= 20

    return max(0, min(100, fortaleza))


# ============================================
# VALIDADOR DE USERNAME
# ============================================

# Patrón de username
#
# ¿Por qué? Los usernames tienen reglas específicas de formato
# ¿Para qué? Consistencia y seguridad en identificadores
#
# Desglose:
# ^              → Inicio
# (?!.*__)       → Negative lookahead: sin __ consecutivos
# [a-zA-Z]       → Primer carácter debe ser letra
# \w{2,19}       → 2-19 caracteres más (word chars)
# $              → Fin
username_pattern = re.compile(r'^(?!.*__)[a-zA-Z]\w{2,19}$')


def validar_username(username: str) -> dict:
    """Valida un nombre de usuario.

    Args:
        username: El username a validar.

    Returns:
        Resultado con validez, errores y sugerencias.
    """
    resultado = {
        'valido': False,
        'errores': [],
        'sugerencias': [],
    }

    # Longitud
    if len(username) < REGLAS['username']['minLength']:
        resultado['errores'].append(
            f"Debe tener al menos {REGLAS['username']['minLength']} caracteres"
        )

    if len(username) > REGLAS['username']['maxLength']:
        resultado['errores'].append(
            f"No debe superar {REGLAS['username']['maxLength']} caracteres"
        )

    # Caracteres permitidos
    if not re.search(r'^[a-zA-Z0-9_]+$', username):
        resultado['errores'].append(
            'Solo se permiten letras, números y guión bajo'
        )

    # Empezar con letra
    if not re.search(r'^[a-zA-Z]', username):
        resultado['errores'].append('Debe empezar con una letra')

    # Guiones bajos consecutivos
    if re.search(r'__', username):
        resultado['errores'].append('No debe tener guiones bajos consecutivos')

    # Palabras prohibidas
    palabra_prohibida = next(
        (
            palabra
            for palabra in PALABRAS_PROHIBIDAS
            if palabra in username.lower()
        ),
        None,
    )
    if palabra_prohibida:
        resultado['errores'].append(
            f'No puede contener "{palabra_prohibida}"'
        )

    resultado['valido'] = len(resultado['errores']) == 0

    # Generar sugerencias si no es válido
    if not resultado['valido']:
        resultado['sugerencias'] = generar_sugerencias(username)

    return resultado


def generar_sugerencias(base: str) -> list:
    """Genera sugerencias de usernames alternativos.

    Args:
        base: Username base.

    Returns:
        Array de sugerencias.
    """
    sugerencias = []

    # Limpiar el base
    limpio = base
    limpio = re.sub(r'[^a-zA-Z0-9_]', '', limpio)
    limpio = re.sub(r'__+', '_', limpio)
    limpio = re.sub(r'^[^a-zA-Z]+', '', limpio)

    # Si está vacío, usar genérico
    if not limpio or len(limpio) < 3:
        limpio = 'user'

    # Generar variantes
    def random_n():
        return random.randint(0, 999)

    sugerencias.append(f'{limpio}{random_n()}')
    sugerencias.append(f'{limpio}_{random_n()}')
    sugerencias.append(f'the_{limpio}')
    sugerencias.append(f'{limpio[0]}{limpio[1:]}{random_n()}')
    sugerencias.append(f'real_{limpio}')

    return sugerencias[:5]


# ============================================
# VALIDADOR DE TARJETA DE CRÉDITO
# ============================================

# Patrones de tarjetas
#
# ¿Por qué? Cada emisor tiene un formato específico
# ¿Para qué? Detectar tipo de tarjeta y validar formato
TARJETAS = {
    'visa': {
        'pattern': re.compile(r'^4\d{15}$'),
        'nombre': 'Visa',
        'longitud': 16,
    },
    'mastercard': {
        'pattern': re.compile(
            r'^(?:5[1-5]\d{14}|2(?:2[2-9]\d{12}|[3-6]\d{13}|7[01]\d{12}|720\d{12}))$'
        ),
        'nombre': 'MasterCard',
        'longitud': 16,
    },
    'amex': {
        'pattern': re.compile(r'^3[47]\d{13}$'),
        'nombre': 'American Express',
        'longitud': 15,
    },
}


def validar_tarjeta(numero: str) -> dict:
    """Valida un número de tarjeta de crédito.

    Args:
        numero: Número de tarjeta (con o sin espacios).

    Returns:
        Resultado con validez, tipo y errores.
    """
    resultado = {
        'valido': False,
        'tipo': None,
        'formateado': None,
        'errores': [],
    }

    # Limpiar: solo dígitos
    limpio = re.sub(r'\D', '', numero)

    if not limpio:
        resultado['errores'].append('El número de tarjeta está vacío')
        return resultado

    # Detectar tipo
    for tipo, config in TARJETAS.items():
        if config['pattern'].search(limpio):
            resultado['tipo'] = config['nombre']
            break

    if not resultado['tipo']:
        resultado['errores'].append('Número de tarjeta no reconocido')
        return resultado

    # Validar Luhn
    if not verificar_luhn(limpio):
        resultado['errores'].append('Número de tarjeta inválido (Luhn)')
        return resultado

    resultado['valido'] = True
    resultado['formateado'] = formatear_tarjeta(limpio, resultado['tipo'])

    return resultado


def verificar_luhn(numero: str) -> bool:
    """Verifica el dígito de control usando algoritmo de Luhn.

    ¿Por qué? Es el estándar de la industria para validar tarjetas
    ¿Para qué? Detectar errores de tipeo

    Args:
        numero: Solo dígitos.

    Returns:
        Si pasa la validación.
    """
    digits = [int(d) for d in reversed(numero)]

    total = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


def formatear_tarjeta(numero: str, tipo: str) -> str:
    """Formatea el número de tarjeta según su tipo.

    Args:
        numero: Solo dígitos.
        tipo: Tipo de tarjeta.

    Returns:
        Número formateado.
    """
    if tipo == 'American Express':
        # Formato: 3411 111111 11111
        return re.sub(r'(\d{4})(\d{6})(\d{5})', r'\1 \2 \3', numero)
    # Formato estándar: 4111 1111 1111 1111
    return re.sub(r'(\d{4})(\d{4})(\d{4})(\d{4})', r'\1 \2 \3 \4', numero)


# ============================================
# EXTRACTOR DE INFORMACIÓN CONTEXTUAL
# ============================================


def extraer_informacion(texto: str) -> dict:
    """Extrae información usando lookarounds.

    Args:
        texto: Texto a analizar.

    Returns:
        Información extraída.
    """
    return {
        # Precios en euros (solo el número)
        'precios': [
            float(p.replace(',', '.'))
            for p in re.findall(r'\d+(?:[.,]\d{2})?(?=\s*€)', texto)
        ],
        # Fechas en formato europeo DD/MM/YYYY
        'fechas': re.findall(r'\b\d{2}/\d{2}/\d{4}\b', texto),
        # Menciones de usuarios @username
        'menciones': [m.lower() for m in re.findall(r'(?<=@)\w+', texto)],
        # Hashtags #tema
        'hashtags': [h.lower() for h in re.findall(r'(?<=#)\w+', texto)],
        # Emails
        'emails': re.findall(r'[\w.-]+@[\w.-]+\.\w{2,}', texto),
        # URLs
        'urls': re.findall(r'https?://[^\s<>"{}|\\^`[\]]+', texto),
    }


# ============================================
# EJECUCIÓN Y TESTS
# ============================================

print('=== Test de Password ===\n')

passwords = [
    'Abc12345!',
    'abc12345!',
    'ABC12345!',
    'Abcdefgh!',
    'Abc123!',
    'Abc12 345!',
    'Abc111111!',
    'Abcqwerty!',
]

for pwd in passwords:
    result = validar_password(pwd)
    icono = '✅' if result['valido'] else '❌'
    print(f"{pwd:<15} → {icono} Fortaleza: {result['fortaleza']}%")
    if result['errores']:
        print(f"   Errores: {', '.join(result['errores'])}")

print('\n=== Test de Username ===\n')

usernames = [
    'johnDoe',
    'john_doe',
    '123john',
    'john__doe',
    'jo',
    'admin_user',
    'valid_user_123',
]

for user in usernames:
    result = validar_username(user)
    icono = '✅' if result['valido'] else '❌'
    print(f"{user:<15} → {icono}")
    if result['errores']:
        print(f"   Errores: {', '.join(result['errores'])}")
    if result['sugerencias']:
        print(f"   Sugerencias: {', '.join(result['sugerencias'])}")

print('\n=== Test de Tarjetas ===\n')

tarjetas = [
    '4111111111111111',
    '4111 1111 1111 1111',
    '5500000000000004',
    '371449635398431',
    '1234567890123456',
    '4111111111111112',
]

for card in tarjetas:
    result = validar_tarjeta(card)
    icono = '✅' if result['valido'] else '❌'
    print(f"{card:<20} → {icono} {result['tipo'] or ''}")
    if result['formateado']:
        print(f"   Formateado: {result['formateado']}")
    if result['errores']:
        print(f"   Errores: {', '.join(result['errores'])}")

print('\n=== Test de Extracción ===\n')

texto_ejemplo = """
Hola @juan y @maria!
El precio es 99,99€ más 21€ de IVA.
Evento el 15/03/2024 y 20/04/2024.
Contacto: info@ejemplo.com
Más info en https://ejemplo.com/info
Usa #oferta #descuento
"""

print(extraer_informacion(texto_ejemplo))
