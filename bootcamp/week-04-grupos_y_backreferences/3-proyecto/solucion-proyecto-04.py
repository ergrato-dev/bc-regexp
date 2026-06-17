"""
============================================
Solución: Proyecto Semana 04
Parser de Logs con Grupos
============================================
"""

import json
import re

# ============================================
# DATOS DE PRUEBA
# ============================================

logs_apache = """
192.168.1.100 - - [15/Jan/2024:14:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234
10.0.0.50 - admin [15/Jan/2024:14:31:00 +0000] "POST /api/login HTTP/1.1" 401 89
192.168.1.101 - - [15/Jan/2024:14:32:15 +0000] "GET /images/logo.png HTTP/1.1" 304 0
192.168.1.100 - - [15/Jan/2024:14:33:00 +0000] "DELETE /api/users/5 HTTP/1.1" 500 256
"""

logs_nginx = """
2024/01/15 14:30:45 [error] 1234#5678: *9999 open() "/var/www/missing.html" failed client: 192.168.1.100
2024/01/15 14:31:00 [warn] 1234#5678: *9998 upstream timed out client: 10.0.0.50
2024/01/15 14:32:15 [info] 1234#5678: *9997 request completed client: 192.168.1.101
"""

logs_app = """
[2024-01-15T14:30:45.123Z] [INFO] [UserService] User 'admin' logged in from 192.168.1.100
[2024-01-15T14:31:00.456Z] [ERROR] [AuthService] Failed login attempt for 'hacker' from 10.0.0.50
[2024-01-15T14:32:15.789Z] [DEBUG] [CacheService] Cache hit for key 'user:123'
"""

# ============================================
# PATRONES DE LOG
# ============================================

# Patrón: Apache Access Log
#
# ¿Por qué? El formato Apache Combined Log es un estándar de la industria
# ¿Para qué? Extraer métricas de tráfico, detectar errores, análisis de uso
#
# Formato: IP - user [fecha] "método ruta HTTP/version" status bytes
apache_pattern = re.compile(
    r'^(?P<ip>[\d.]+)\s+-\s+(?P<user>\S+)\s+\[(?P<fecha>[^\]]+)\]\s+"'
    r'(?P<metodo>\w+)\s+(?P<ruta>\S+)\s+HTTP/(?P<version>[\d.]+)"\s+'
    r'(?P<status>\d+)\s+(?P<bytes>\d+)'
)

# Patrón: Nginx Error Log
#
# ¿Por qué? Nginx tiene su propio formato de logs de error
# ¿Para qué? Diagnosticar problemas del servidor, monitorear conexiones
#
# Formato: fecha hora [nivel] pid#tid: *conexion mensaje client: ip
nginx_pattern = re.compile(
    r'^(?P<fecha>[\d/]+\s[\d:]+)\s+\[(?P<nivel>\w+)\]\s+'
    r'(?P<pid>\d+)#(?P<tid>\d+):\s+\*(?P<conexion>\d+)\s+'
    r'(?P<mensaje>.+?)\s+client:\s+(?P<ip>[\d.]+)'
)

# Patrón: Application Log
#
# ¿Por qué? Los logs de aplicación siguen un formato consistente
# ¿Para qué? Monitorear comportamiento, detectar errores de negocio
#
# Formato: [timestamp] [NIVEL] [Servicio] mensaje
app_pattern = re.compile(
    r'^\[(?P<timestamp>[^\]]+)\]\s+\[(?P<nivel>\w+)\]\s+'
    r'\[(?P<servicio>\w+)\]\s+(?P<mensaje>.+)$'
)

# ============================================
# FUNCIONES DE PARSING
# ============================================


def parsear_fecha_apache(fecha_str):
    """Parsea fecha Apache a ISO.

    ¿Por qué? El formato Apache no es estándar
    ¿Para qué? Normalizar fechas para comparación
    """
    # Formato: 15/Jan/2024:14:30:45 +0000
    meses = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
    }

    pattern = re.compile(
        r'(?P<dia>\d{2})/(?P<mes>\w{3})/(?P<anio>\d{4}):'
        r'(?P<hora>\d{2}):(?P<min>\d{2}):(?P<seg>\d{2})'
    )
    match = pattern.search(fecha_str)
    if not match:
        return fecha_str

    dia = match.group('dia')
    mes = match.group('mes')
    anio = match.group('anio')
    hora = match.group('hora')
    min = match.group('min')
    seg = match.group('seg')
    return f"{anio}-{meses[mes]}-{dia}T{hora}:{min}:{seg}Z"


def parse_apache(linea):
    """Parsea una línea de log Apache.

    ¿Por qué? Convertir texto a estructura de datos
    ¿Para qué? Facilitar análisis y agregación

    Args:
        linea: Línea de log Apache

    Returns:
        dict or None: Datos parseados o None si no coincide
    """
    match = apache_pattern.search(linea.strip())
    if not match:
        return None

    ip = match.group('ip')
    user = match.group('user')
    fecha = match.group('fecha')
    metodo = match.group('metodo')
    ruta = match.group('ruta')
    version = match.group('version')
    status = int(match.group('status'))
    bytes_enviados = int(match.group('bytes'))

    return {
        'formato': 'apache',
        'ip': ip,
        'user': None if user == '-' else user,
        'fecha': parsear_fecha_apache(fecha),
        'metodo': metodo,
        'ruta': ruta,
        'httpVersion': version,
        'status': status,
        'bytes': bytes_enviados,
        'esError': status >= 400,
    }


def parsear_fecha_nginx(fecha_str):
    """Parsea fecha Nginx a ISO."""
    # Formato: 2024/01/15 14:30:45
    return fecha_str.replace('/', '-').replace(' ', 'T') + 'Z'


def parse_nginx(linea):
    """Parsea una línea de log Nginx.

    Args:
        linea: Línea de log Nginx

    Returns:
        dict or None: Datos parseados o None
    """
    match = nginx_pattern.search(linea.strip())
    if not match:
        return None

    fecha = match.group('fecha')
    nivel = match.group('nivel')
    pid = int(match.group('pid'))
    tid = int(match.group('tid'))
    conexion = int(match.group('conexion'))
    mensaje = match.group('mensaje')
    ip = match.group('ip')

    return {
        'formato': 'nginx',
        'fecha': parsear_fecha_nginx(fecha),
        'nivel': nivel.lower(),
        'pid': pid,
        'tid': tid,
        'conexion': conexion,
        'mensaje': mensaje.strip(),
        'ip': ip,
        'esError': nivel.lower() == 'error',
    }


def parse_app(linea):
    """Parsea una línea de log de aplicación.

    Args:
        linea: Línea de log

    Returns:
        dict or None: Datos parseados o None
    """
    match = app_pattern.search(linea.strip())
    if not match:
        return None

    timestamp = match.group('timestamp')
    nivel = match.group('nivel')
    servicio = match.group('servicio')
    mensaje = match.group('mensaje')

    # Extraer IP del mensaje si existe
    ip_match = re.search(
        r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', mensaje
    )

    return {
        'formato': 'app',
        'fecha': timestamp,
        'nivel': nivel.lower(),
        'servicio': servicio,
        'mensaje': mensaje,
        'ip': ip_match.group('ip') if ip_match else None,
        'esError': nivel.lower() == 'error',
    }


# ============================================
# DETECTOR DE FORMATO
# ============================================


def detectar_y_parsear(linea):
    """Detecta el formato de log y lo parsea automáticamente.

    ¿Por qué? Los logs pueden venir mezclados
    ¿Para qué? Procesar cualquier formato sin configuración

    Args:
        linea: Línea de log

    Returns:
        dict or None: Datos parseados o None
    """
    # Intentar cada parser en orden
    parsers = [
        {'nombre': 'apache', 'fn': parse_apache},
        {'nombre': 'nginx', 'fn': parse_nginx},
        {'nombre': 'app', 'fn': parse_app},
    ]

    for parser in parsers:
        resultado = parser['fn'](linea)
        if resultado:
            return resultado

    return None


# ============================================
# ANALIZADOR DE LOGS
# ============================================


def analizar_logs(logs):
    """Analiza un conjunto de logs y genera estadísticas.

    ¿Por qué? Los datos crudos no son útiles sin agregación
    ¿Para qué? Obtener métricas y detectar problemas

    Args:
        logs: Múltiples líneas de log

    Returns:
        dict: Estadísticas
    """
    lineas = [l for l in logs.strip().split('\n') if l.strip()]
    resultado = {
        'total': 0,
        'parseados': 0,
        'fallidos': 0,
        'porFormato': {'apache': 0, 'nginx': 0, 'app': 0},
        'porNivel': {'error': 0, 'warn': 0, 'info': 0, 'debug': 0},
        'porStatus': {},
        'ips': set(),
        'errores': [],
        'logsParsed': [],
    }

    for linea in lineas:
        resultado['total'] += 1

        parsed = detectar_y_parsear(linea)
        if not parsed:
            resultado['fallidos'] += 1
            continue

        resultado['parseados'] += 1
        resultado['logsParsed'].append(parsed)
        resultado['porFormato'][parsed['formato']] += 1

        # Contar por nivel
        if 'nivel' in parsed and parsed['nivel']:
            nivel = parsed['nivel']
            resultado['porNivel'][nivel] = (
                resultado['porNivel'].get(nivel, 0) + 1
            )

        # Contar por status (solo Apache)
        if 'status' in parsed:
            status = parsed['status']
            resultado['porStatus'][status] = (
                resultado['porStatus'].get(status, 0) + 1
            )

        # Recolectar IPs
        if parsed.get('ip'):
            resultado['ips'].add(parsed['ip'])

        # Recolectar errores
        if parsed.get('esError'):
            resultado['errores'].append({
                'fecha': parsed['fecha'],
                'formato': parsed['formato'],
                'mensaje': parsed.get('mensaje') or f"Status {parsed['status']}",
                'ip': parsed['ip'],
            })

    # Convertir Set a list
    resultado['ips'] = list(resultado['ips'])

    return resultado


# ============================================
# FUNCIONES AUXILIARES
# ============================================


def filtrar_por_ip(logs, ip):
    """Filtra logs por IP.

    Args:
        logs: Array de logs parseados
        ip: IP a filtrar

    Returns:
        list: Logs de esa IP
    """
    return [log for log in logs if log['ip'] == ip]


def agrupar_por_ip(logs):
    """Agrupa logs por IP con conteo.

    Args:
        logs: Array de logs parseados

    Returns:
        dict: { ip: count }
    """
    resultado = {}
    for log in logs:
        if log.get('ip'):
            ip = log['ip']
            resultado[ip] = resultado.get(ip, 0) + 1
    return resultado


def detectar_anomalias(logs, umbral_errores=3):
    """Detecta IPs con comportamiento sospechoso.

    Args:
        logs: Array de logs parseados
        umbral_errores: Número de errores para alertar

    Returns:
        list: IPs sospechosas con detalles
    """
    por_ip = {}

    for log in logs:
        if not log.get('ip'):
            continue

        ip = log['ip']
        if ip not in por_ip:
            por_ip[ip] = {'total': 0, 'errores': 0, 'ultimoError': None}

        por_ip[ip]['total'] += 1
        if log.get('esError'):
            por_ip[ip]['errores'] += 1
            por_ip[ip]['ultimoError'] = log['fecha']

    # Filtrar IPs sospechosas
    return [
        {
            'ip': ip,
            'totalRequests': stats['total'],
            'errores': stats['errores'],
            'porcentajeErrores': format(
                (stats['errores'] / stats['total']) * 100, '.1f'
            ),
            'ultimoError': stats['ultimoError'],
        }
        for ip, stats in por_ip.items()
        if stats['errores'] >= umbral_errores
    ]


def generar_reporte(stats):
    """Genera reporte en formato texto.

    Args:
        stats: Estadísticas de analizar_logs

    Returns:
        str: Reporte formateado
    """
    def p8(val):
        return str(val).rjust(8)

    ips_str = ', '.join(stats['ips'])
    ips_line = ips_str[:54].ljust(54)

    errores_lines = '\n'.join(
        f"║   [{e['formato']}] {e['ip']}: {e['mensaje'][:40]}"
        for e in stats['errores']
    )

    return f"""
╔══════════════════════════════════════════════════════════════╗
║                    REPORTE DE LOGS                           ║
╠══════════════════════════════════════════════════════════════╣
║ RESUMEN                                                      ║
║   Total de líneas:     {p8(stats['total'])}                           ║
║   Parseadas:           {p8(stats['parseados'])}                           ║
║   Fallidas:            {p8(stats['fallidos'])}                           ║
╠══════════════════════════════════════════════════════════════╣
║ POR FORMATO                                                  ║
║   Apache:              {p8(stats['porFormato']['apache'])}                           ║
║   Nginx:               {p8(stats['porFormato']['nginx'])}                           ║
║   App:                 {p8(stats['porFormato']['app'])}                           ║
╠══════════════════════════════════════════════════════════════╣
║ POR NIVEL                                                    ║
║   Error:               {p8(stats['porNivel'].get('error', 0))}                           ║
║   Warn:                {p8(stats['porNivel'].get('warn', 0))}                           ║
║   Info:                {p8(stats['porNivel'].get('info', 0))}                           ║
║   Debug:               {p8(stats['porNivel'].get('debug', 0))}                           ║
╠══════════════════════════════════════════════════════════════╣
║ IPs ÚNICAS: {len(stats['ips'])}                                              ║
║   {ips_line} ║
╠══════════════════════════════════════════════════════════════╣
║ ERRORES: {len(stats['errores'])}                                                 ║
{errores_lines}
╚══════════════════════════════════════════════════════════════╝
    """.strip()


# ============================================
# EJECUCIÓN Y TESTS
# ============================================

if __name__ == '__main__':
    print('=== Test de Parsers Individuales ===\n')

    # Test Apache
    linea_apache = (
        '192.168.1.100 - - [15/Jan/2024:14:30:45 +0000] '
        '"GET /api/users HTTP/1.1" 200 1234'
    )
    print('Apache:', json.dumps(parse_apache(linea_apache), indent=2))

    # Test Nginx
    linea_nginx = (
        '2024/01/15 14:30:45 [error] 1234#5678: *9999 '
        'open() "/var/www/missing.html" failed client: 192.168.1.100'
    )
    print('\nNginx:', json.dumps(parse_nginx(linea_nginx), indent=2))

    # Test App
    linea_app = (
        "[2024-01-15T14:30:45.123Z] [INFO] [UserService] "
        "User 'admin' logged in from 192.168.1.100"
    )
    print('\nApp:', json.dumps(parse_app(linea_app), indent=2))

    print('\n=== Análisis Completo ===\n')

    # Combinar todos los logs
    todos_los_logs = logs_apache + '\n' + logs_nginx + '\n' + logs_app
    stats = analizar_logs(todos_los_logs)

    print(generar_reporte(stats))

    print('\n=== Detección de Anomalías ===\n')
    anomalias = detectar_anomalias(stats['logsParsed'], 1)
    print('IPs sospechosas:', anomalias)

    print('\n=== Logs por IP ===\n')
    print('Agrupados:', agrupar_por_ip(stats['logsParsed']))
