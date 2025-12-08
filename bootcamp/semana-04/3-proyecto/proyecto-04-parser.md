# Proyecto Semana 04: Parser de Logs con Grupos

## 🎯 Objetivo

Crear un **parser de logs** que extraiga información estructurada de diferentes formatos de log usando grupos de captura y backreferences.

## 📋 Descripción

Los logs de servidor vienen en formatos específicos. Tu tarea es crear un parser que:

1. Identifique el formato del log
2. Extraiga todos los componentes
3. Normalice la información
4. Genere reportes

## 🗂️ Formatos de Log

### 1. Apache Access Log

```
192.168.1.100 - - [15/Jan/2024:14:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234
```

**Componentes:**

- IP del cliente
- Fecha y hora
- Método HTTP
- Ruta
- Versión HTTP
- Código de estado
- Bytes transferidos

### 2. Nginx Error Log

```
2024/01/15 14:30:45 [error] 1234#5678: *9999 message "archivo no encontrado" client: 192.168.1.100
```

**Componentes:**

- Fecha y hora
- Nivel (error, warn, info)
- PID#TID
- ID de conexión
- Mensaje
- IP del cliente

### 3. Application Log (JSON-like)

```
[2024-01-15T14:30:45.123Z] [INFO] [UserService] User 'admin' logged in from 192.168.1.100
```

**Componentes:**

- Timestamp ISO
- Nivel
- Servicio
- Mensaje completo

## 🛠️ Instrucciones

### Paso 1: Datos de Prueba

```javascript
const logsApache = `
192.168.1.100 - - [15/Jan/2024:14:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234
10.0.0.50 - admin [15/Jan/2024:14:31:00 +0000] "POST /api/login HTTP/1.1" 401 89
192.168.1.101 - - [15/Jan/2024:14:32:15 +0000] "GET /images/logo.png HTTP/1.1" 304 0
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
```

### Paso 2: Definir Patrones

```javascript
/**
 * Patrón: Apache Access Log
 *
 * ¿Por qué? El formato Apache es estándar y predecible
 * ¿Para qué? Extraer métricas de tráfico web
 *
 * Desglose:
 * (?<ip>...)           → IP del cliente
 * \[(?<fecha>...)\]    → Fecha entre corchetes
 * "(?<metodo>...) ..." → Request entre comillas
 */
const apachePattern = /???/;

/**
 * Patrón: Nginx Error Log
 *
 * ¿Por qué? Nginx usa su propio formato de error
 * ¿Para qué? Diagnosticar problemas del servidor
 */
const nginxPattern = /???/;

/**
 * Patrón: Application Log
 *
 * ¿Por qué? Los logs de aplicación tienen estructura consistente
 * ¿Para qué? Monitorear comportamiento de la aplicación
 */
const appPattern = /???/;
```

### Paso 3: Crear Parsers

```javascript
/**
 * Parsea una línea de log Apache
 *
 * @param {string} linea - Línea de log
 * @returns {object|null} Datos parseados o null
 */
function parseApache(linea) {
  // Tu implementación
}

/**
 * Parsea una línea de log Nginx
 */
function parseNginx(linea) {
  // Tu implementación
}

/**
 * Parsea una línea de log de aplicación
 */
function parseApp(linea) {
  // Tu implementación
}
```

### Paso 4: Detector de Formato

```javascript
/**
 * Detecta el formato de log y lo parsea
 *
 * ¿Por qué? No siempre sabemos qué formato viene
 * ¿Para qué? Procesar logs mixtos automáticamente
 *
 * @param {string} linea - Línea de log
 * @returns {object} { formato: string, datos: object }
 */
function detectarYParsear(linea) {
  // Intenta cada patrón
  // Retorna el primero que coincida
}
```

### Paso 5: Analizador de Logs

```javascript
/**
 * Analiza un conjunto de logs y genera estadísticas
 *
 * @param {string} logs - Múltiples líneas de log
 * @returns {object} Estadísticas
 */
function analizarLogs(logs) {
  return {
    total: 0,
    porFormato: { apache: 0, nginx: 0, app: 0 },
    porNivel: { error: 0, warn: 0, info: 0, debug: 0 },
    ips: [],
    errores: [],
  };
}
```

## 💡 Hints

<details>
<summary>Hint: Patrón Apache</summary>

```javascript
const apachePattern =
  /^(?<ip>[\d.]+)\s+-\s+(?<user>\S+)\s+\[(?<fecha>[^\]]+)\]\s+"(?<metodo>\w+)\s+(?<ruta>\S+)\s+HTTP\/(?<version>[\d.]+)"\s+(?<status>\d+)\s+(?<bytes>\d+)/;
```

</details>

<details>
<summary>Hint: Patrón Nginx</summary>

```javascript
const nginxPattern =
  /^(?<fecha>[\d\/]+\s[\d:]+)\s+\[(?<nivel>\w+)\]\s+(?<pid>\d+)#(?<tid>\d+):\s+\*(?<conexion>\d+)\s+(?<mensaje>.+?)\s+client:\s+(?<ip>[\d.]+)/;
```

</details>

<details>
<summary>Hint: Patrón App</summary>

```javascript
const appPattern =
  /^\[(?<timestamp>[^\]]+)\]\s+\[(?<nivel>\w+)\]\s+\[(?<servicio>\w+)\]\s+(?<mensaje>.+)$/;
```

</details>

## 🚀 Extensiones

### Extensión 1: Filtro por IP

```javascript
function logsPorIP(logs, ip) {
  // Filtra logs de una IP específica
}
```

### Extensión 2: Alertas de Error

```javascript
function detectarAnomalias(logs) {
  // Detecta:
  // - Más de 5 errores de la misma IP
  // - Códigos 4xx o 5xx consecutivos
  // - Picos de errores en ventana de tiempo
}
```

### Extensión 3: Exportador

```javascript
function exportarCSV(logsParsed) {
  // Genera CSV con los datos
}

function exportarJSON(logsParsed) {
  // Genera JSON estructurado
}
```

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-04-parser.md         (este archivo)
├── log-parser.js                  (tu solución)
├── test-parser.js                 (tests)
└── datos/
    ├── apache.log
    ├── nginx.log
    └── app.log
```

## ✅ Criterios de Evaluación

| Criterio                   | Puntos |
| -------------------------- | ------ |
| Patrones regex correctos   | 25%    |
| Funciones de parsing       | 25%    |
| Detector de formato        | 20%    |
| Analizador de estadísticas | 20%    |
| Manejo de edge cases       | 10%    |

## 📝 Reflexión

Después de completar el proyecto, responde:

1. ¿Por qué usamos named groups en lugar de índices numéricos?
2. ¿Cómo manejarías logs con formato incorrecto o corrupto?
3. ¿Qué ventajas tiene usar non-capturing groups en estos patrones?
4. ¿Cómo modificarías los patrones para ser más flexibles con espacios?

---

**Solución:** Disponible en `solucion-proyecto-04.js`
