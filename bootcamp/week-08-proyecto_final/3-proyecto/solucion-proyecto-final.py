"""
============================================
Solución: Proyecto Final
RegEx Toolkit - Librería Completa
============================================
"""

import re
import unicodedata
import urllib.parse
from datetime import datetime


# ============================================
# VALIDATORS
# ============================================

class Validators:
    """
    Colección de validadores basados en regex.

    ¿Por qué? Validar formatos comunes de datos de entrada.
    ¿Para qué? Formularios, APIs, ETLs, y validación general.

    Métodos estáticos: todos son independientes del estado.
    """

    @staticmethod
    def email(value):
        """
        Validar email.

        ¿Por qué? Email tiene formato RFC 5322.
        ¿Para qué? Validación de formularios.
        """
        if not value or len(value) > 254:
            return False
        return bool(
            re.search(
                r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
                value,
            )
        )

    @staticmethod
    def url(value, options=None):
        """
        Validar URL.

        ¿Por qué? URLs tienen estructura específica.
        ¿Para qué? Validar enlaces antes de usarlos.
        """
        if options is None:
            options = {}
        protocols = options.get('protocols', ['http', 'https'])
        protocol_part = '|'.join(protocols)
        pattern = re.compile(
            rf'^(?:{protocol_part}):\/\/(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{{1,256}}\.[a-zA-Z0-9()]{{1,6}}\b[-a-zA-Z0-9()@:%_+.~#?&/=]*$'
        )
        return bool(pattern.search(value))

    @staticmethod
    def phone(value, country_code='US'):
        """
        Validar teléfono.

        ¿Por qué? Formatos varían por país.
        ¿Para qué? Aceptar múltiples formatos.
        """
        patterns = {
            'US': r'^(\+1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$',
            'ES': r'^(\+34)?[-.\s]?\d{9}$',
            'MX': r'^(\+52)?[-.\s]?\d{10}$',
            'INT': r'^\+?[1-9]\d{1,14}$',  # E.164
        }
        chosen = patterns.get(country_code, patterns['INT'])
        return bool(re.search(chosen, re.sub(r'\s', '', value)))

    @staticmethod
    def password(value, policy=None):
        """
        Validar contraseña.

        ¿Por qué? Seguridad requiere complejidad.
        ¿Para qué? Cumplir políticas de seguridad.
        """
        if policy is None:
            policy = {}
        min_length = policy.get('minLength', 8)
        require_uppercase = policy.get('requireUppercase', True)
        require_lowercase = policy.get('requireLowercase', True)
        require_number = policy.get('requireNumber', True)
        require_special = policy.get('requireSpecial', True)

        errors = []

        if len(value) < min_length:
            errors.append(f'Mínimo {min_length} caracteres')
        if require_uppercase and not re.search(r'[A-Z]', value):
            errors.append('Requiere mayúscula')
        if require_lowercase and not re.search(r'[a-z]', value):
            errors.append('Requiere minúscula')
        if require_number and not re.search(r'\d', value):
            errors.append('Requiere número')
        if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            errors.append('Requiere carácter especial')

        return {'valid': len(errors) == 0, 'errors': errors}

    @staticmethod
    def credit_card(value):
        """
        Validar tarjeta de crédito.

        ¿Por qué? Detectar tipo y formato.
        ¿Para qué? UX mejorada en pagos.
        """
        cleaned = re.sub(r'[\s-]', '', value)

        types = [
            {'name': 'Visa', 'pattern': r'^4\d{12}(?:\d{3})?$'},
            {'name': 'Mastercard', 'pattern': r'^5[1-5]\d{14}$'},
            {'name': 'Amex', 'pattern': r'^3[47]\d{13}$'},
            {'name': 'Discover', 'pattern': r'^6(?:011|5\d{2})\d{12}$'},
        ]

        for cc_type in types:
            if re.search(cc_type['pattern'], cleaned):
                return {'valid': True, 'type': cc_type['name']}

        return {'valid': False, 'type': None}

    @staticmethod
    def uuid(value):
        """Validar UUID."""
        return bool(
            re.search(
                r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
                value,
                re.IGNORECASE,
            )
        )

    @staticmethod
    def ipv4(value):
        """Validar IPv4."""
        return bool(
            re.search(
                r'^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$',
                value,
            )
        )

    @staticmethod
    def semver(value):
        """Validar semver."""
        return bool(
            re.search(
                r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$',
                value,
            )
        )

    @staticmethod
    def slug(value):
        """Validar slug."""
        return bool(re.search(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', value))


# ============================================
# EXTRACTORS
# ============================================

class Extractors:
    """
    Colección de extractores basados en regex.

    ¿Por qué? Extraer entidades de texto libre.
    ¿Para qué? Web scraping, NLP ligero, y parsing de contenido.

    Métodos estáticos: todos son independientes del estado.
    """

    @staticmethod
    def emails(text, options=None):
        """
        Extraer emails.

        ¿Por qué? Los emails siguen un patrón reconocible.
        ¿Para qué? Extraer direcciones de contacto de documentos.
        """
        if options is None:
            options = {}
        unique = options.get('unique', True)
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(pattern, text)
        return list(dict.fromkeys(matches)) if unique else matches

    @staticmethod
    def urls(text, options=None):
        """
        Extraer URLs.

        ¿Por qué? Las URLs tienen formato reconocible http/https.
        ¿Para qué? Extraer enlaces de texto libre.
        """
        if options is None:
            options = {}
        unique = options.get('unique', True)
        pattern = r'https?:\/\/[^\s<>"{}|\\^`\[\]]+'
        matches = re.findall(pattern, text)
        return list(dict.fromkeys(matches)) if unique else matches

    @staticmethod
    def hashtags(text, options=None):
        """
        Extraer hashtags.

        ¿Por qué? Redes sociales usan # para etiquetar.
        ¿Para qué? Análisis de tendencias y clasificación.
        """
        if options is None:
            options = {}
        unique = options.get('unique', True)
        with_symbol = options.get('withSymbol', False)
        pattern = r'#([a-zA-Z_]\w*)'
        matches = []
        for m in re.finditer(pattern, text):
            matches.append(m.group(0) if with_symbol else m.group(1))
        return list(dict.fromkeys(matches)) if unique else matches

    @staticmethod
    def mentions(text, options=None):
        """
        Extraer menciones.

        ¿Por qué? Redes sociales usan @ para mencionar.
        ¿Para qué? Análisis de interacciones y grafos sociales.
        """
        if options is None:
            options = {}
        unique = options.get('unique', True)
        with_symbol = options.get('withSymbol', False)
        pattern = r'@([a-zA-Z_]\w*)'
        matches = []
        for m in re.finditer(pattern, text):
            matches.append(m.group(0) if with_symbol else m.group(1))
        return list(dict.fromkeys(matches)) if unique else matches

    @staticmethod
    def dates(text):
        """
        Extraer fechas ISO.

        ¿Por qué? ISO 8601 es el estándar de intercambio.
        ¿Para qué? Extraer timestamps de logs y APIs.
        """
        pattern = (
            r'\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])'
            r'(?:T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?'
            r'(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)?)?'
        )
        matches = re.findall(pattern, text)
        return [datetime.fromisoformat(d) for d in matches]

    @staticmethod
    def ips(text):
        """
        Extraer IPs.

        ¿Por qué? Las IPv4 usan formato dotted-decimal.
        ¿Para qué? Extraer direcciones de logs y configuraciones.
        """
        pattern = (
            r'\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}'
            r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b'
        )
        matches = re.findall(pattern, text)
        return list(dict.fromkeys(matches))

    @staticmethod
    def prices(text):
        """
        Extraer precios.

        ¿Por qué? Precios siguen patrón moneda+cantidad.
        ¿Para qué? Extraer información de comercio electrónico y facturas.
        """
        pattern = re.compile(r'(?P<currency>[$€£¥])\s*(?P<amount>\d+(?:[.,]\d{1,2})?)')
        results = []
        for m in pattern.finditer(text):
            results.append({
                'currency': m.group('currency'),
                'amount': float(m.group('amount').replace(',', '.')),
            })
        return results


# ============================================
# PARSERS
# ============================================

class Parsers:
    """
    Colección de parsers basados en regex.

    ¿Por qué? Descomponer cadenas estructuradas en objetos.
    ¿Para qué? Procesar headers HTTP, URLs, CSV, y más.

    Métodos estáticos: todos son independientes del estado.
    """

    @staticmethod
    def user_agent(ua):
        """
        Parsear User Agent.

        ¿Por qué? Cada navegador/envío tiene formato propio.
        ¿Para qué? Analíticas web y detección de dispositivo.
        """
        result = {
            'browser': None,
            'browserVersion': None,
            'os': None,
            'osVersion': None,
            'mobile': False,
        }

        # OS
        os_patterns = [
            (r'Windows NT ([\d.]+)', 'Windows'),
            (r'Mac OS X ([\d_]+)', 'macOS'),
            (r'Android ([\d.]+)', 'Android'),
            (r'iPhone OS ([\d_]+)', 'iOS'),
            (r'Linux', 'Linux'),
        ]

        for pattern, name in os_patterns:
            m = re.search(pattern, ua)
            if m:
                result['os'] = name
                result['osVersion'] = (
                    m.group(1).replace('_', '.') if m.groups() else None
                )
                break

        # Browser
        browser_patterns = [
            (r'Edg(?:e)?\/([\d.]+)', 'Edge'),
            (r'Chrome\/([\d.]+)', 'Chrome'),
            (r'Firefox\/([\d.]+)', 'Firefox'),
            (r'Version\/([\d.]+).*Safari', 'Safari'),
        ]

        for pattern, name in browser_patterns:
            m = re.search(pattern, ua)
            if m:
                result['browser'] = name
                result['browserVersion'] = m.group(1)
                break

        result['mobile'] = bool(re.search(r'Mobile|iPhone|Android.*Mobile', ua, re.IGNORECASE))

        return result

    @staticmethod
    def query_string(qs):
        """
        Parsear Query String.

        ¿Por qué? Las query strings codifican pares clave=valor.
        ¿Para qué? Procesar parámetros de URL.
        """
        result = {}
        pattern = r'[?&]([^=]+)=([^&]*)'

        for m in re.finditer(pattern, qs):
            key = urllib.parse.unquote(m.group(1))
            value = urllib.parse.unquote(m.group(2))
            result[key] = value

        return result

    @staticmethod
    def url(url_str):
        """
        Parsear URL.

        ¿Por qué? Las URLs tienen componentes bien definidos (RFC 3986).
        ¿Para qué? Descomponer URLs para routing, analytics, o validación.
        """
        pattern = re.compile(
            r'^(?P<protocol>https?):\/\/'
            r'(?:(?P<user>[^:@]+)(?::(?P<password>[^@]+))?@)?'
            r'(?P<host>[^/:]+)'
            r'(?::(?P<port>\d+))?'
            r'(?P<path>\/[^?#]*)?'
            r'(?:\?(?P<query>[^#]*))?'
            r'(?:#(?P<hash>.*))?$'
        )

        m = pattern.search(url_str)
        if not m:
            return None

        result = m.groupdict()
        result['port'] = int(m.group('port')) if m.group('port') else None
        result['queryParams'] = (
            Parsers.query_string('?' + m.group('query'))
            if m.group('query')
            else {}
        )
        return result

    @staticmethod
    def csv_line(line, delimiter=','):
        """
        Parsear CSV línea.

        ¿Por qué? CSV es el formato de intercambio tabular más común.
        ¿Para qué? Procesar archivos CSV respetando quoting y escapes.
        """
        escaped = re.escape(delimiter)
        pattern = re.compile(
            rf'(?:^|{escaped})'
            rf'(?:"([^"]*(?:""[^"]*)*)"|([^{escaped}"]*))'
        )

        fields = []
        for m in pattern.finditer(line):
            value = (
                m.group(1).replace('""', '"')
                if m.group(1) is not None
                else m.group(2)
            )
            fields.append(value)

        return fields


# ============================================
# TRANSFORMERS
# ============================================

class Transformers:
    """
    Colección de transformadores basados en regex.

    ¿Por qué? Transformar texto entre formatos.
    ¿Para qué? Normalización, limpieza y formateo de datos.

    Métodos estáticos: todos son independientes del estado.
    """

    @staticmethod
    def camel_to_snake(s):
        """
        camelCase a snake_case.

        ¿Por qué? Convención de nomenclatura varía por lenguaje.
        ¿Para qué? Convertir identificadores JS a Python.
        """
        return re.sub(r'[A-Z]', lambda m: '_' + m.group(0).lower(), s)

    @staticmethod
    def snake_to_camel(s):
        """
        snake_case a camelCase.

        ¿Por qué? Convención de nomenclatura varía por lenguaje.
        ¿Para qué? Convertir identificadores Python a JS.
        """
        return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)

    @staticmethod
    def to_kebab(s):
        """
        A kebab-case.

        ¿Por qué? Convención usada en URLs y CSS.
        ¿Para qué? Normalizar identificadores a kebab-case.
        """
        result = re.sub(r'([a-z])([A-Z])', r'\1-\2', s)
        result = re.sub(r'[\s_]+', '-', result)
        return result.lower()

    @staticmethod
    def to_pascal(s):
        """
        A PascalCase.

        ¿Por qué? Convención usada en nombres de clase.
        ¿Para qué? Normalizar a PascalCase.
        """
        result = re.sub(r'(?:^|[\s_-])(\w)', lambda m: m.group(1).upper(), s)
        return re.sub(r'[\s_-]', '', result)

    @staticmethod
    def strip_html(s):
        """
        Eliminar HTML.

        ¿Por qué? A veces se necesita texto plano.
        ¿Para qué? Sanitizar contenido para display o NLP.
        """
        return re.sub(r'<[^>]+>', '', s)

    @staticmethod
    def escape_html(s):
        """
        Escapar HTML.

        ¿Por qué? Prevenir XSS.
        ¿Para qué? Mostrar texto con caracteres especiales en HTML.
        """
        entities = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
        }
        return re.sub(r'[&<>"\']', lambda m: entities[m.group(0)], s)

    @staticmethod
    def escape_regex(s):
        """
        Escapar regex.

        ¿Por qué? Caracteres especiales en regex deben escaparse.
        ¿Para qué? Construir patrones dinámicos de forma segura.
        """
        return re.escape(s)

    @staticmethod
    def normalize_spaces(s):
        """
        Normalizar espacios.

        ¿Por qué? Espacios múltiples son ruido.
        ¿Para qué? Limpiar entrada de usuario.
        """
        return re.sub(r'\s+', ' ', s).strip()

    @staticmethod
    def slugify(s):
        """
        Crear slug.

        ¿Por qué? URLs necesitan identificadores limpios.
        ¿Para qué? Generar slugs para CMS, blogs, o rutas.
        """
        result = s.lower()
        result = unicodedata.normalize('NFD', result)
        result = re.sub(r'[\u0300-\u036f]', '', result)  # Remover acentos
        result = re.sub(r'[^a-z0-9]+', '-', result)
        result = re.sub(r'^-+|-+$', '', result)
        return result

    @staticmethod
    def format_phone(s, fmt='(###) ###-####'):
        """
        Formatear teléfono.

        ¿Por qué? Números sin formato son difíciles de leer.
        ¿Para qué? Mostrar teléfonos con formato consistente.
        """
        digits = re.sub(r'\D', '', s)
        result = []
        i = 0
        for ch in fmt:
            if ch == '#':
                result.append(digits[i] if i < len(digits) else '')
                i += 1
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def format_credit_card(s):
        """
        Formatear tarjeta.

        ¿Por qué? Agrupar dígitos mejora legibilidad.
        ¿Para qué? Mostrar números de tarjeta en UI.
        """
        digits = re.sub(r'\D', '', s)
        return re.sub(r'(\d{4})(?=\d)', r'\1 ', digits)

    @staticmethod
    def truncate(s, length, suffix='...'):
        """
        Truncar texto.

        ¿Por qué? Mostrar resúmenes en interfaces limitadas.
        ¿Para qué? Previews de contenido sin desbordar layout.
        """
        if len(s) <= length:
            return s
        return s[: length - len(suffix)] + suffix


# ============================================
# EXPORTS & DEMO
# ============================================

class RegexToolkit:
    """
    RegEx Toolkit — librería completa de expresiones regulares.

    Agrupa Validators, Extractors, Parsers y Transformers
    en un solo punto de acceso.
    """

    def __init__(self):
        self.validators = Validators
        self.extractors = Extractors
        self.parsers = Parsers
        self.transformers = Transformers


if __name__ == '__main__':
    print('=== RegEx Toolkit Demo ===\n')

    print('-- Validators --')
    print('Email:', Validators.email('user@example.com'))
    print('Password:', Validators.password('Weak'))
    print('Credit Card:', Validators.credit_card('4532-1234-5678-9012'))

    print('\n-- Extractors --')
    text = (
        'Contact us at hello@example.com or visit https://example.com '
        '#regex @mention'
    )
    print('Emails:', Extractors.emails(text))
    print('URLs:', Extractors.urls(text))
    print('Hashtags:', Extractors.hashtags(text))
    print('Mentions:', Extractors.mentions(text))

    print('\n-- Parsers --')
    print('Query:', Parsers.query_string('?name=John&age=30'))
    print(
        'URL:',
        Parsers.url('https://user:pass@example.com:8080/path?q=1#hash'),
    )

    print('\n-- Transformers --')
    print('camelToSnake:', Transformers.camel_to_snake('helloWorld'))
    print('slugify:', Transformers.slugify('Hola Mundo! Café'))
    print('formatPhone:', Transformers.format_phone('5551234567'))
