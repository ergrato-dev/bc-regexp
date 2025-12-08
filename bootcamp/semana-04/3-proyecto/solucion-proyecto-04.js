/**
 * ============================================
 * Solución: Proyecto Semana 04
 * Parser de Logs con Grupos
 * ============================================
 */

// ============================================
// DATOS DE PRUEBA
// ============================================

const logsApache = `
192.168.1.100 - - [15/Jan/2024:14:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234
10.0.0.50 - admin [15/Jan/2024:14:31:00 +0000] "POST /api/login HTTP/1.1" 401 89
192.168.1.101 - - [15/Jan/2024:14:32:15 +0000] "GET /images/logo.png HTTP/1.1" 304 0
192.168.1.100 - - [15/Jan/2024:14:33:00 +0000] "DELETE /api/users/5 HTTP/1.1" 500 256
`;

const logsNginx = `
2024/01/15 14:30:45 [error] 1234#5678: *9999 open() "/var/www/missing.html" failed client: 192.168.1.100
2024/01/15 14:31:00 [warn] 1234#5678: *9998 upstream timed out client: 10.0.0.50
2024/01/15 14:32:15 [info] 1234#5678: *9997 request completed client: 192.168.1.101
`;

const logsApp = `
[2024-01-15T14:30:45.123Z] [INFO] [UserService] User 'admin' logged in from 192.168.1.100
[2024-01-15T14:31:00.456Z] [ERROR] [AuthService] Failed login attempt for 'hacker' from 10.0.0.50
[2024-01-15T14:32:15.789Z] [DEBUG] [CacheService] Cache hit for key 'user:123'
`;

// ============================================
// PATRONES DE LOG
// ============================================

/**
 * Patrón: Apache Access Log
 *
 * ¿Por qué? El formato Apache Combined Log es un estándar de la industria
 * ¿Para qué? Extraer métricas de tráfico, detectar errores, análisis de uso
 *
 * Formato: IP - user [fecha] "método ruta HTTP/version" status bytes
 */
const apachePattern =
  /^(?<ip>[\d.]+)\s+-\s+(?<user>\S+)\s+\[(?<fecha>[^\]]+)\]\s+"(?<metodo>\w+)\s+(?<ruta>\S+)\s+HTTP\/(?<version>[\d.]+)"\s+(?<status>\d+)\s+(?<bytes>\d+)/;

/**
 * Patrón: Nginx Error Log
 *
 * ¿Por qué? Nginx tiene su propio formato de logs de error
 * ¿Para qué? Diagnosticar problemas del servidor, monitorear conexiones
 *
 * Formato: fecha hora [nivel] pid#tid: *conexion mensaje client: ip
 */
const nginxPattern =
  /^(?<fecha>[\d/]+\s[\d:]+)\s+\[(?<nivel>\w+)\]\s+(?<pid>\d+)#(?<tid>\d+):\s+\*(?<conexion>\d+)\s+(?<mensaje>.+?)\s+client:\s+(?<ip>[\d.]+)/;

/**
 * Patrón: Application Log
 *
 * ¿Por qué? Los logs de aplicación siguen un formato consistente
 * ¿Para qué? Monitorear comportamiento, detectar errores de negocio
 *
 * Formato: [timestamp] [NIVEL] [Servicio] mensaje
 */
const appPattern =
  /^\[(?<timestamp>[^\]]+)\]\s+\[(?<nivel>\w+)\]\s+\[(?<servicio>\w+)\]\s+(?<mensaje>.+)$/;

// ============================================
// FUNCIONES DE PARSING
// ============================================

/**
 * Parsea una línea de log Apache
 *
 * ¿Por qué? Convertir texto a estructura de datos
 * ¿Para qué? Facilitar análisis y agregación
 *
 * @param {string} linea - Línea de log Apache
 * @returns {object|null} Datos parseados o null si no coincide
 */
function parseApache(linea) {
  const match = linea.trim().match(apachePattern);
  if (!match) return null;

  const { ip, user, fecha, metodo, ruta, version, status, bytes } =
    match.groups;

  return {
    formato: 'apache',
    ip,
    user: user === '-' ? null : user,
    fecha: parsearFechaApache(fecha),
    metodo,
    ruta,
    httpVersion: version,
    status: parseInt(status),
    bytes: parseInt(bytes),
    esError: parseInt(status) >= 400,
  };
}

/**
 * Parsea fecha Apache a ISO
 *
 * ¿Por qué? El formato Apache no es estándar
 * ¿Para qué? Normalizar fechas para comparación
 */
function parsearFechaApache(fechaStr) {
  // Formato: 15/Jan/2024:14:30:45 +0000
  const meses = {
    Jan: '01',
    Feb: '02',
    Mar: '03',
    Apr: '04',
    May: '05',
    Jun: '06',
    Jul: '07',
    Aug: '08',
    Sep: '09',
    Oct: '10',
    Nov: '11',
    Dec: '12',
  };

  const pattern =
    /(?<dia>\d{2})\/(?<mes>\w{3})\/(?<anio>\d{4}):(?<hora>\d{2}):(?<min>\d{2}):(?<seg>\d{2})/;
  const match = fechaStr.match(pattern);
  if (!match) return fechaStr;

  const { dia, mes, anio, hora, min, seg } = match.groups;
  return `${anio}-${meses[mes]}-${dia}T${hora}:${min}:${seg}Z`;
}

/**
 * Parsea una línea de log Nginx
 *
 * @param {string} linea - Línea de log Nginx
 * @returns {object|null} Datos parseados o null
 */
function parseNginx(linea) {
  const match = linea.trim().match(nginxPattern);
  if (!match) return null;

  const { fecha, nivel, pid, tid, conexion, mensaje, ip } = match.groups;

  return {
    formato: 'nginx',
    fecha: parsearFechaNginx(fecha),
    nivel: nivel.toLowerCase(),
    pid: parseInt(pid),
    tid: parseInt(tid),
    conexion: parseInt(conexion),
    mensaje: mensaje.trim(),
    ip,
    esError: nivel.toLowerCase() === 'error',
  };
}

/**
 * Parsea fecha Nginx a ISO
 */
function parsearFechaNginx(fechaStr) {
  // Formato: 2024/01/15 14:30:45
  return fechaStr.replace(/\//g, '-').replace(' ', 'T') + 'Z';
}

/**
 * Parsea una línea de log de aplicación
 *
 * @param {string} linea - Línea de log
 * @returns {object|null} Datos parseados o null
 */
function parseApp(linea) {
  const match = linea.trim().match(appPattern);
  if (!match) return null;

  const { timestamp, nivel, servicio, mensaje } = match.groups;

  // Extraer IP del mensaje si existe
  const ipMatch = mensaje.match(/(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/);

  return {
    formato: 'app',
    fecha: timestamp,
    nivel: nivel.toLowerCase(),
    servicio,
    mensaje,
    ip: ipMatch ? ipMatch.groups.ip : null,
    esError: nivel.toLowerCase() === 'error',
  };
}

// ============================================
// DETECTOR DE FORMATO
// ============================================

/**
 * Detecta el formato de log y lo parsea automáticamente
 *
 * ¿Por qué? Los logs pueden venir mezclados
 * ¿Para qué? Procesar cualquier formato sin configuración
 *
 * @param {string} linea - Línea de log
 * @returns {object|null} { formato, datos } o null
 */
function detectarYParsear(linea) {
  // Intentar cada parser en orden
  const parsers = [
    { nombre: 'apache', fn: parseApache },
    { nombre: 'nginx', fn: parseNginx },
    { nombre: 'app', fn: parseApp },
  ];

  for (const { nombre, fn } of parsers) {
    const resultado = fn(linea);
    if (resultado) {
      return resultado;
    }
  }

  return null;
}

// ============================================
// ANALIZADOR DE LOGS
// ============================================

/**
 * Analiza un conjunto de logs y genera estadísticas
 *
 * ¿Por qué? Los datos crudos no son útiles sin agregación
 * ¿Para qué? Obtener métricas y detectar problemas
 *
 * @param {string} logs - Múltiples líneas de log
 * @returns {object} Estadísticas
 */
function analizarLogs(logs) {
  const lineas = logs.trim().split('\n').filter(Boolean);
  const resultado = {
    total: 0,
    parseados: 0,
    fallidos: 0,
    porFormato: { apache: 0, nginx: 0, app: 0 },
    porNivel: { error: 0, warn: 0, info: 0, debug: 0 },
    porStatus: {},
    ips: new Set(),
    errores: [],
    logsParsed: [],
  };

  for (const linea of lineas) {
    resultado.total++;

    const parsed = detectarYParsear(linea);
    if (!parsed) {
      resultado.fallidos++;
      continue;
    }

    resultado.parseados++;
    resultado.logsParsed.push(parsed);
    resultado.porFormato[parsed.formato]++;

    // Contar por nivel
    if (parsed.nivel) {
      resultado.porNivel[parsed.nivel] =
        (resultado.porNivel[parsed.nivel] || 0) + 1;
    }

    // Contar por status (solo Apache)
    if (parsed.status) {
      resultado.porStatus[parsed.status] =
        (resultado.porStatus[parsed.status] || 0) + 1;
    }

    // Recolectar IPs
    if (parsed.ip) {
      resultado.ips.add(parsed.ip);
    }

    // Recolectar errores
    if (parsed.esError) {
      resultado.errores.push({
        fecha: parsed.fecha,
        formato: parsed.formato,
        mensaje: parsed.mensaje || `Status ${parsed.status}`,
        ip: parsed.ip,
      });
    }
  }

  // Convertir Set a Array
  resultado.ips = Array.from(resultado.ips);

  return resultado;
}

// ============================================
// FUNCIONES AUXILIARES
// ============================================

/**
 * Filtra logs por IP
 *
 * @param {object[]} logs - Array de logs parseados
 * @param {string} ip - IP a filtrar
 * @returns {object[]} Logs de esa IP
 */
function filtrarPorIP(logs, ip) {
  return logs.filter((log) => log.ip === ip);
}

/**
 * Agrupa logs por IP con conteo
 *
 * @param {object[]} logs - Array de logs parseados
 * @returns {object} { ip: count }
 */
function agruparPorIP(logs) {
  return logs.reduce((acc, log) => {
    if (log.ip) {
      acc[log.ip] = (acc[log.ip] || 0) + 1;
    }
    return acc;
  }, {});
}

/**
 * Detecta IPs con comportamiento sospechoso
 *
 * @param {object[]} logs - Array de logs parseados
 * @param {number} umbralErrores - Número de errores para alertar
 * @returns {object[]} IPs sospechosas con detalles
 */
function detectarAnomalias(logs, umbralErrores = 3) {
  const porIP = {};

  for (const log of logs) {
    if (!log.ip) continue;

    if (!porIP[log.ip]) {
      porIP[log.ip] = { total: 0, errores: 0, ultimoError: null };
    }

    porIP[log.ip].total++;
    if (log.esError) {
      porIP[log.ip].errores++;
      porIP[log.ip].ultimoError = log.fecha;
    }
  }

  // Filtrar IPs sospechosas
  return Object.entries(porIP)
    .filter(([ip, stats]) => stats.errores >= umbralErrores)
    .map(([ip, stats]) => ({
      ip,
      totalRequests: stats.total,
      errores: stats.errores,
      porcentajeErrores: ((stats.errores / stats.total) * 100).toFixed(1),
      ultimoError: stats.ultimoError,
    }));
}

/**
 * Genera reporte en formato texto
 *
 * @param {object} stats - Estadísticas de analizarLogs
 * @returns {string} Reporte formateado
 */
function generarReporte(stats) {
  return `
╔══════════════════════════════════════════════════════════════╗
║                    REPORTE DE LOGS                           ║
╠══════════════════════════════════════════════════════════════╣
║ RESUMEN                                                      ║
║   Total de líneas:     ${stats.total
    .toString()
    .padStart(8)}                           ║
║   Parseadas:           ${stats.parseados
    .toString()
    .padStart(8)}                           ║
║   Fallidas:            ${stats.fallidos
    .toString()
    .padStart(8)}                           ║
╠══════════════════════════════════════════════════════════════╣
║ POR FORMATO                                                  ║
║   Apache:              ${stats.porFormato.apache
    .toString()
    .padStart(8)}                           ║
║   Nginx:               ${stats.porFormato.nginx
    .toString()
    .padStart(8)}                           ║
║   App:                 ${stats.porFormato.app
    .toString()
    .padStart(8)}                           ║
╠══════════════════════════════════════════════════════════════╣
║ POR NIVEL                                                    ║
║   Error:               ${(stats.porNivel.error || 0)
    .toString()
    .padStart(8)}                           ║
║   Warn:                ${(stats.porNivel.warn || 0)
    .toString()
    .padStart(8)}                           ║
║   Info:                ${(stats.porNivel.info || 0)
    .toString()
    .padStart(8)}                           ║
║   Debug:               ${(stats.porNivel.debug || 0)
    .toString()
    .padStart(8)}                           ║
╠══════════════════════════════════════════════════════════════╣
║ IPs ÚNICAS: ${stats.ips.length}                                              ║
║   ${stats.ips.join(', ').substring(0, 54).padEnd(54)} ║
╠══════════════════════════════════════════════════════════════╣
║ ERRORES: ${
    stats.errores.length
  }                                                 ║
${stats.errores
  .map((e) => `║   [${e.formato}] ${e.ip}: ${e.mensaje.substring(0, 40)}`)
  .join('\n')}
╚══════════════════════════════════════════════════════════════╝
  `.trim();
}

// ============================================
// EJECUCIÓN Y TESTS
// ============================================

console.log('=== Test de Parsers Individuales ===\n');

// Test Apache
const lineaApache =
  '192.168.1.100 - - [15/Jan/2024:14:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234';
console.log('Apache:', JSON.stringify(parseApache(lineaApache), null, 2));

// Test Nginx
const lineaNginx =
  '2024/01/15 14:30:45 [error] 1234#5678: *9999 open() "/var/www/missing.html" failed client: 192.168.1.100';
console.log('\nNginx:', JSON.stringify(parseNginx(lineaNginx), null, 2));

// Test App
const lineaApp =
  "[2024-01-15T14:30:45.123Z] [INFO] [UserService] User 'admin' logged in from 192.168.1.100";
console.log('\nApp:', JSON.stringify(parseApp(lineaApp), null, 2));

console.log('\n=== Análisis Completo ===\n');

// Combinar todos los logs
const todosLosLogs = logsApache + '\n' + logsNginx + '\n' + logsApp;
const stats = analizarLogs(todosLosLogs);

console.log(generarReporte(stats));

console.log('\n=== Detección de Anomalías ===\n');
const anomalias = detectarAnomalias(stats.logsParsed, 1);
console.log('IPs sospechosas:', anomalias);

console.log('\n=== Logs por IP ===\n');
console.log('Agrupados:', agruparPorIP(stats.logsParsed));
