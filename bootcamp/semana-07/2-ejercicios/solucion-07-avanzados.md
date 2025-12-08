# Soluciones - Semana 07: Patrones Avanzados

---

## Ejercicio 1: Parser de Log con Named Groups

```javascript
/**
 * ¿Por qué? Los logs tienen estructura predefinida
 * ¿Para qué? Extraer componentes para análisis y alertas
 */
const logPattern =
  /^\[(?<date>\d{4}-\d{2}-\d{2})\s+(?<time>\d{2}:\d{2}:\d{2})\]\s+(?<level>ERROR|WARN|INFO|DEBUG)\s+(?<service>[\w-]+):\s+(?<message>.+)$/gm;
//                   │ │                        │  │                        │   │                            │   │             │   │
//                   │ │                        │  │                        │   │                            │   │             │   └─ Mensaje: todo el resto
//                   │ │                        │  │                        │   │                            │   └─────────────── : y espacio
//                   │ │                        │  │                        │   │                            └─ Servicio: alfanum + guiones
//                   │ │                        │  │                        │   └─ Nivel: solo valores válidos
//                   │ │                        │  │                        └─ Espacio
//                   │ │                        │  └─ Hora: HH:MM:SS
//                   │ │                        └─ Espacio(s)
//                   │ └─ Fecha: YYYY-MM-DD
//                   └─ Corchete abierto

const logs = `[2024-03-15 10:30:45] ERROR servidor-web: Connection timeout
[2024-03-15 10:31:02] INFO auth-service: User login successful
[2024-03-15 10:31:15] WARN database: High memory usage (85%)
[2024-03-15 10:32:00] DEBUG api-gateway: Request processed in 45ms`;

for (const match of logs.matchAll(logPattern)) {
  console.log(match.groups);
}
// { date: '2024-03-15', time: '10:30:45', level: 'ERROR', service: 'servidor-web', message: 'Connection timeout' }
// { date: '2024-03-15', time: '10:31:02', level: 'INFO', service: 'auth-service', message: 'User login successful' }
// ...
```

---

## Ejercicio 2: Validador de Contraseña Segura

```javascript
/**
 * ¿Por qué? Las contraseñas débiles son vulnerables
 * ¿Para qué? Garantizar seguridad mínima en autenticación
 */
const passwordPattern =
  /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])(?!.*\s)(?!.*(.)\1{3,}).{8,}$/;
//                        │           │           │       │               │        │             │
//                        │           │           │       │               │        │             └─ Mínimo 8 caracteres
//                        │           │           │       │               │        └─ Negative lookahead: no 4+ caracteres iguales
//                        │           │           │       │               └─ Negative lookahead: sin espacios
//                        │           │           │       └─ Al menos un especial
//                        │           │           └─ Al menos un dígito
//                        │           └─ Al menos una minúscula
//                        └─ Al menos una mayúscula

// Tests
console.log(passwordPattern.test('Passw0rd!')); // true
console.log(passwordPattern.test('MyStr0ng#Pass')); // true
console.log(passwordPattern.test('C0mpl3x!ty')); // true

console.log(passwordPattern.test('password')); // false - sin mayúscula, número, especial
console.log(passwordPattern.test('PASSWORD1!')); // false - sin minúscula
console.log(passwordPattern.test('Passw0rd')); // false - sin especial
console.log(passwordPattern.test('Pass 0rd!')); // false - tiene espacio
console.log(passwordPattern.test('Passsword1!')); // true - solo 3 's' (permitido)
console.log(passwordPattern.test('Passssword1!')); // false - 4 's' consecutivas

/**
 * Versión con función para feedback detallado
 */
function validatePassword(password) {
  const checks = [
    { test: /.{8,}/, message: 'Mínimo 8 caracteres' },
    { test: /[A-Z]/, message: 'Al menos una mayúscula' },
    { test: /[a-z]/, message: 'Al menos una minúscula' },
    { test: /\d/, message: 'Al menos un número' },
    { test: /[!@#$%^&*]/, message: 'Al menos un carácter especial' },
    { test: /^\S+$/, message: 'Sin espacios' },
    { test: /^(?!.*(.)\1{3,})/, message: 'Sin 4+ caracteres repetidos' },
  ];

  const failed = checks.filter((c) => !c.test.test(password));

  return {
    valid: failed.length === 0,
    errors: failed.map((c) => c.message),
  };
}
```

---

## Ejercicio 3: Extractor de URLs con Componentes

```javascript
/**
 * ¿Por qué? Las URLs tienen estructura compleja pero definida
 * ¿Para qué? Validar, normalizar y extraer partes de URLs
 */
const urlPattern =
  /^(?<protocol>https?|ftp):\/\/(?:(?<subdomain>[\w-]+)\.)?(?<domain>[\w-]+)\.(?<tld>[a-z]{2,})(?::(?<port>\d+))?(?<path>\/[^\s?#]*)?(?:\?(?<query>[^\s#]*))?(?:#(?<fragment>\S*))?$/i;
//                   │                          │                          │                  │              │              │                    │                       │
//                   │                          │                          │                  │              │              │                    │                       └─ Fragment opcional
//                   │                          │                          │                  │              │              │                    └─ Query string opcional
//                   │                          │                          │                  │              │              └─ Path opcional
//                   │                          │                          │                  │              └─ Puerto opcional
//                   │                          │                          │                  └─ TLD (2+ letras)
//                   │                          │                          └─ Dominio principal
//                   │                          └─ Subdominio opcional
//                   └─ Protocolo: http, https, ftp

const urls = [
  'https://www.example.com:8080/path/to/page?id=123&name=test#section',
  'http://api.service.io/v2/users',
  'ftp://files.server.net/downloads/file.zip',
  'https://sub.domain.example.org/search?q=regex',
];

for (const url of urls) {
  const match = url.match(urlPattern);
  if (match) {
    console.log(url);
    console.log(match.groups);
    console.log('---');
  }
}

// Ejemplo de salida:
// {
//   protocol: 'https',
//   subdomain: 'www',
//   domain: 'example',
//   tld: 'com',
//   port: '8080',
//   path: '/path/to/page',
//   query: 'id=123&name=test',
//   fragment: 'section'
// }
```

---

## Ejercicio 4: Detector de SQL Injection

```javascript
/**
 * ¿Por qué? SQL injection es una vulnerabilidad crítica
 * ¿Para qué? Detectar y bloquear inputs maliciosos
 */
const sqlInjectionPatterns = [
  // Comentarios SQL
  /--\s*$/,
  /\/\*.*\*\//,

  // OR/AND con condiciones siempre verdaderas
  /['"]?\s*(?:OR|AND)\s+['"]?\d+['"]\s*=\s*['"]\d+/i,
  /['"]?\s*(?:OR|AND)\s+\d+\s*=\s*\d+/i,

  // UNION SELECT
  /UNION\s+(?:ALL\s+)?SELECT/i,

  // Comandos peligrosos después de ;
  /;\s*(?:DROP|DELETE|INSERT|UPDATE|CREATE|ALTER|TRUNCATE)/i,

  // Comilla seguida de palabras clave
  /'\s*;\s*(?:DROP|DELETE)/i,
];

function detectSQLInjection(input) {
  for (const pattern of sqlInjectionPatterns) {
    if (pattern.test(input)) {
      return {
        detected: true,
        pattern: pattern.toString(),
        input: input,
      };
    }
  }
  return { detected: false };
}

// Tests - Ataques
console.log(detectSQLInjection("' OR '1'='1")); // detected: true
console.log(detectSQLInjection("'; DROP TABLE users; --")); // detected: true
console.log(detectSQLInjection('1; DELETE FROM products')); // detected: true
console.log(detectSQLInjection('UNION SELECT * FROM users')); // detected: true
console.log(detectSQLInjection("' AND 1=1 --")); // detected: true

// Tests - Seguros
console.log(detectSQLInjection("John's Pizza")); // detected: false
console.log(detectSQLInjection('SELECT menu items')); // detected: false
console.log(detectSQLInjection('Hello world')); // detected: false

/**
 * Patrón combinado más completo
 */
const sqlInjectionCombined =
  /(?:--\s*$|\/\*[\s\S]*?\*\/|['"]?\s*(?:OR|AND)\s+['"]?\d+['"]?\s*=\s*['"]?\d+|UNION\s+(?:ALL\s+)?SELECT|;\s*(?:DROP|DELETE|INSERT|UPDATE|CREATE|ALTER|TRUNCATE))/i;
```

---

## Ejercicio 5: Parser de CSV Robusto

```javascript
/**
 * ¿Por qué? CSV parece simple pero tiene casos complejos
 * ¿Para qué? Importar datos de hojas de cálculo
 */

// Patrón para un campo CSV
const csvFieldPattern = /(?:^|,)(?:"((?:[^"]|"")*)"|([^",\n]*))/g;
//                       │       │  │              │ │
//                       │       │  │              │ └─ Campo sin comillas
//                       │       │  │              └─ O
//                       │       │  └─ Contenido entre comillas (con "" escapado)
//                       │       └─ Campo entre comillas
//                       └─ Inicio o coma

function parseCSVLine(line) {
  const fields = [];
  let match;

  // Reset lastIndex
  csvFieldPattern.lastIndex = 0;

  while ((match = csvFieldPattern.exec(line)) !== null) {
    // match[1] = campo entre comillas, match[2] = campo sin comillas
    let value = match[1] !== undefined ? match[1] : match[2];

    // Desescapar comillas dobles
    if (match[1] !== undefined) {
      value = value.replace(/""/g, '"');
    }

    fields.push(value);
  }

  return fields;
}

function parseCSV(csv) {
  return csv.trim().split('\n').map(parseCSVLine);
}

const csvData = `nombre,edad,ciudad
"García, Juan",35,"Madrid, España"
Ana,28,Barcelona
"El ""Maestro"" López",45,Sevilla
,25,Valencia
Pedro,,Bilbao`;

console.log(parseCSV(csvData));
// [
//   ['nombre', 'edad', 'ciudad'],
//   ['García, Juan', '35', 'Madrid, España'],
//   ['Ana', '28', 'Barcelona'],
//   ['El "Maestro" López', '45', 'Sevilla'],
//   ['', '25', 'Valencia'],
//   ['Pedro', '', 'Bilbao']
// ]
```

---

## Ejercicio 6: Optimizar Patrón Problemático

```javascript
/**
 * ¿Por qué? Patrones mal diseñados causan backtracking catastrófico
 * ¿Para qué? Prevenir DoS y mejorar rendimiento
 */

// 1. Email problemático
// ❌ Malo: /^(\w+\.?)+@(\w+\.?)+\.\w+$/
// Problema: (\w+\.?)+ permite backtracking exponencial
// Input malo: "aaaaaaaaaaaaaaaaaaa@"

// ✅ Solución:
const emailSeguro = /^[\w.]{1,64}@[\w.]{1,255}\.[a-z]{2,}$/i;
//                   │           │              │
//                   │           │              └─ TLD fijo
//                   │           └─ Dominio con límite
//                   └─ Local-part con límite

// 2. HTML tag problemático
// ❌ Malo: /<(\w+)>.*<\/\1>/
// Problema: .* es greedy y backtrackea
// Input malo: "<div>a</div><div>b</div>" con texto largo entre tags

// ✅ Solución:
const htmlTagSeguro = /<(\w+)>[^<]*<\/\1>/;
//                            │
//                            └─ [^<]* no puede pasar del siguiente <

// O para contenido con tags anidados:
const htmlTagNested = /<(\w+)>(?:(?!<\/\1>).)*<\/\1>/s;
//                              │
//                              └─ Lookahead negativo previene overreach

// 3. Número con separadores
// ❌ Malo: /^[\d,]+$/
// Problema: permite ",,,," o "1,,2"
// No es backtracking pero es semánticamente incorrecto

// ✅ Solución:
const numeroConSeparadores = /^\d{1,3}(?:,\d{3})*$/;
//                            │       │
//                            │       └─ Grupos de 3 dígitos después de coma
//                            └─ 1-3 dígitos iniciales

// Tests
console.log(emailSeguro.test('user@example.com')); // true
console.log(emailSeguro.test('a'.repeat(100) + '@')); // false (muy largo)

console.log(htmlTagSeguro.test('<div>content</div>')); // true

console.log(numeroConSeparadores.test('1,234,567')); // true
console.log(numeroConSeparadores.test('1,,234')); // false
console.log(numeroConSeparadores.test(',234')); // false
```

---

## Ejercicio 7: Tokenizer Aritmético

```javascript
/**
 * ¿Por qué? Los tokenizers son la base de parsers y compiladores
 * ¿Para qué? Convertir texto en estructuras procesables
 */

const tokenDefinitions = [
  { type: 'NUMBER', pattern: /\d+(?:\.\d+)?/ },
  { type: 'POWER', pattern: /\*\*|\^/ },
  { type: 'PLUS', pattern: /\+/ },
  { type: 'MINUS', pattern: /-/ },
  { type: 'MULT', pattern: /\*/ },
  { type: 'DIV', pattern: /\// },
  { type: 'LPAREN', pattern: /\(/ },
  { type: 'RPAREN', pattern: /\)/ },
  { type: 'IDENT', pattern: /[a-zA-Z_]\w*/ },
  { type: 'WS', pattern: /\s+/ },
];

// Construir regex combinado
const combinedPattern = new RegExp(
  tokenDefinitions
    .map(({ type, pattern }) => `(?<${type}>${pattern.source})`)
    .join('|'),
  'g'
);

function tokenize(expression) {
  const tokens = [];

  for (const match of expression.matchAll(combinedPattern)) {
    // Encontrar qué grupo capturó
    for (const [type, value] of Object.entries(match.groups)) {
      if (value !== undefined && type !== 'WS') {
        tokens.push({ type, value });
        break;
      }
    }
  }

  return tokens;
}

// Tests
console.log(tokenize('3 + 4 * 2'));
// [
//   { type: 'NUMBER', value: '3' },
//   { type: 'PLUS', value: '+' },
//   { type: 'NUMBER', value: '4' },
//   { type: 'MULT', value: '*' },
//   { type: 'NUMBER', value: '2' }
// ]

console.log(tokenize('(10 - 5) / 2.5'));
// [
//   { type: 'LPAREN', value: '(' },
//   { type: 'NUMBER', value: '10' },
//   { type: 'MINUS', value: '-' },
//   { type: 'NUMBER', value: '5' },
//   { type: 'RPAREN', value: ')' },
//   { type: 'DIV', value: '/' },
//   { type: 'NUMBER', value: '2.5' }
// ]

console.log(tokenize('x^2 + 2*x + 1'));
// [
//   { type: 'IDENT', value: 'x' },
//   { type: 'POWER', value: '^' },
//   { type: 'NUMBER', value: '2' },
//   { type: 'PLUS', value: '+' },
//   { type: 'NUMBER', value: '2' },
//   { type: 'MULT', value: '*' },
//   { type: 'IDENT', value: 'x' },
//   { type: 'PLUS', value: '+' },
//   { type: 'NUMBER', value: '1' }
// ]

console.log(tokenize('sin(x) ** 2'));
// [
//   { type: 'IDENT', value: 'sin' },
//   { type: 'LPAREN', value: '(' },
//   { type: 'IDENT', value: 'x' },
//   { type: 'RPAREN', value: ')' },
//   { type: 'POWER', value: '**' },
//   { type: 'NUMBER', value: '2' }
// ]
```

---

## Desafío: Parser de Template Strings

```javascript
/**
 * ¿Por qué? Template strings son comunes en frameworks modernos
 * ¿Para qué? Implementar sistemas de plantillas
 */

function parseTemplate(template) {
  const result = [];

  // Patrón: texto o ${expresión}
  const templatePattern = /(?<text>[^$]+)|\$\{(?<expr>[^}]+)\}/g;
  //                       │              │   │
  //                       │              │   └─ Expresión entre {}
  //                       │              └─ ${
  //                       └─ Texto (cualquier cosa excepto $)

  for (const match of template.matchAll(templatePattern)) {
    if (match.groups.text !== undefined) {
      // Puede haber $ sueltos que no son interpolación
      const text = match.groups.text;
      if (text.length > 0) {
        result.push({ type: 'TEXT', value: text });
      }
    } else if (match.groups.expr !== undefined) {
      result.push({ type: 'EXPR', value: match.groups.expr.trim() });
    }
  }

  return result;
}

// Versión más robusta que maneja $ sueltos
function parseTemplateRobust(template) {
  const result = [];
  let lastIndex = 0;

  const exprPattern = /\$\{([^}]+)\}/g;

  for (const match of template.matchAll(exprPattern)) {
    // Texto antes de la expresión
    if (match.index > lastIndex) {
      result.push({
        type: 'TEXT',
        value: template.slice(lastIndex, match.index),
      });
    }

    // La expresión
    result.push({
      type: 'EXPR',
      value: match[1].trim(),
    });

    lastIndex = match.index + match[0].length;
  }

  // Texto restante
  if (lastIndex < template.length) {
    result.push({
      type: 'TEXT',
      value: template.slice(lastIndex),
    });
  }

  return result;
}

// Tests
console.log(parseTemplateRobust('Hello, ${name}!'));
// [
//   { type: 'TEXT', value: 'Hello, ' },
//   { type: 'EXPR', value: 'name' },
//   { type: 'TEXT', value: '!' }
// ]

console.log(
  parseTemplateRobust('Hello, ${name}! You have ${items.length} items.')
);
// [
//   { type: 'TEXT', value: 'Hello, ' },
//   { type: 'EXPR', value: 'name' },
//   { type: 'TEXT', value: '! You have ' },
//   { type: 'EXPR', value: 'items.length' },
//   { type: 'TEXT', value: ' items.' }
// ]

console.log(parseTemplateRobust('Price: $${price} (${tax}% tax)'));
// [
//   { type: 'TEXT', value: 'Price: $' },
//   { type: 'EXPR', value: 'price' },
//   { type: 'TEXT', value: ' (' },
//   { type: 'EXPR', value: 'tax' },
//   { type: 'TEXT', value: '% tax)' }
// ]

/**
 * Versión con soporte para anidación básica
 */
function parseTemplateNested(template) {
  const result = [];
  let lastIndex = 0;
  let depth = 0;
  let exprStart = -1;

  for (let i = 0; i < template.length; i++) {
    if (template[i] === '$' && template[i + 1] === '{') {
      if (depth === 0) {
        // Texto antes
        if (i > lastIndex) {
          result.push({
            type: 'TEXT',
            value: template.slice(lastIndex, i),
          });
        }
        exprStart = i + 2;
      }
      depth++;
      i++; // Saltar {
    } else if (template[i] === '}' && depth > 0) {
      depth--;
      if (depth === 0) {
        result.push({
          type: 'EXPR',
          value: template.slice(exprStart, i).trim(),
        });
        lastIndex = i + 1;
      }
    }
  }

  // Texto restante
  if (lastIndex < template.length) {
    result.push({
      type: 'TEXT',
      value: template.slice(lastIndex),
    });
  }

  return result;
}

console.log(parseTemplateNested('${a ? ${b} : c}'));
// [{ type: 'EXPR', value: 'a ? ${b} : c' }]
```

---

## Resumen de Técnicas Aprendidas

```
┌──────────────────────────────────────────────────────────────┐
│                 TÉCNICAS AVANZADAS                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Named Groups       (?<nombre>...)     Grupos con nombre    │
│  Backreference      \k<nombre>         Ref. por nombre      │
│  Replace            $<nombre>          En reemplazo         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  OPTIMIZACIÓN                                                │
│  ────────────────────────────────────────────────────        │
│  • [^x]* en lugar de .*                                     │
│  • Límites de longitud {1,n}                                │
│  • Anclas ^$ cuando sea posible                             │
│  • Evitar (a+)+ y patrones anidados                         │
│  • Lookahead negativo para prevenir overreach               │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  TOKENIZACIÓN                                                │
│  ────────────────────────────────────────────────────        │
│  • Combinar patrones con alternación                         │
│  • Usar named groups para tipos                              │
│  • Ordenar por especificidad (más específico primero)       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
