# Semana 08: Proyecto Final + Casos Reales

## 🎯 Objetivos

- Aplicar todo lo aprendido en un proyecto integral
- Resolver casos reales de la industria
- Crear una librería de patrones reutilizable
- Dominar debugging y testing de regex

---

## 1. Resumen del Bootcamp

### Semana 1: Fundamentos

```javascript
// Literales y metacaracteres
/hello/              // Literal
/./                  // Cualquier carácter
/^start/             // Inicio
/end$/               // Fin
/\./                 // Escape
```

### Semana 2: Clases de Caracteres

```javascript
// Character classes
/[abc]/              // a, b, o c
/[^abc]/             // NO a, b, ni c
/[a-z]/              // Rango
/\d/                 // Dígito
/\w/                 // Word character
/\s/                 // Whitespace
```

### Semana 3: Cuantificadores

```javascript
// Quantifiers
/a*/                 // 0 o más
/a+/                 // 1 o más
/a?/                 // 0 o 1
/a{3}/               // Exactamente 3
/a{2,5}/             // Entre 2 y 5
/a+?/                // Lazy
```

### Semana 4: Grupos y Capturas

```javascript
// Groups
/(abc)/              // Capture group
/(?:abc)/            // Non-capturing
/(a)(b)\1\2/         // Backreference
```

### Semana 5: Lookahead y Lookbehind

```javascript
// Assertions
/(?=abc)/            // Positive lookahead
/(?!abc)/            // Negative lookahead
/(?<=abc)/           // Positive lookbehind
/(?<!abc)/           // Negative lookbehind
```

### Semana 6: Flags

```javascript
// Flags
/pattern/g / // Global
  pattern /
  i / // Case-insensitive
  pattern /
  m / // Multiline
  pattern /
  s / // DotAll
  pattern /
  u / // Unicode
  pattern /
  y / // Sticky
  pattern /
  d; // Indices
```

### Semana 7: Patrones Avanzados

```javascript
// Advanced
/(?<name>abc)/       // Named group
/\k<name>/           // Named backreference
// Optimización y seguridad
```

---

## 2. Casos Reales de la Industria

### 2.1 Validación de Formularios

```javascript
/**
 * Colección de validadores para formularios
 */
const Validators = {
  /**
   * Email (RFC 5322 simplificado)
   *
   * ¿Por qué? Validar formato de email antes de enviar al servidor
   * ¿Para qué? Feedback inmediato al usuario
   */
  email:
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,

  /**
   * Teléfono internacional
   *
   * ¿Por qué? Los teléfonos varían por país
   * ¿Para qué? Aceptar formatos comunes
   */
  phone: /^\+?[1-9]\d{1,14}$/, // E.164 format

  /**
   * Contraseña fuerte
   *
   * ¿Por qué? Seguridad de cuentas
   * ¿Para qué? Cumplir políticas de seguridad
   */
  password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/,

  /**
   * URL
   *
   * ¿Por qué? Validar enlaces antes de procesarlos
   * ¿Para qué? Prevenir errores y ataques
   */
  url: /^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_+.~#?&/=]*$/,

  /**
   * Tarjeta de crédito (formato básico)
   *
   * ¿Por qué? Validación rápida antes de enviar a payment gateway
   * ¿Para qué? UX mejorada, menos errores
   */
  creditCard:
    /^(?:4\d{12}(?:\d{3})?|5[1-5]\d{14}|3[47]\d{13}|6(?:011|5\d{2})\d{12})$/,

  /**
   * Código postal (múltiples países)
   */
  postalCode: {
    ES: /^\d{5}$/, // España
    US: /^\d{5}(-\d{4})?$/, // Estados Unidos
    UK: /^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$/i, // Reino Unido
    CA: /^[A-Z]\d[A-Z]\s*\d[A-Z]\d$/i, // Canadá
  },
};
```

### 2.2 Procesamiento de Logs

```javascript
/**
 * Parsers de logs comunes
 */
const LogParsers = {
  /**
   * Apache Combined Log Format
   *
   * ¿Por qué? Es el formato estándar de servidores web
   * ¿Para qué? Análisis de tráfico, debugging
   */
  apache:
    /^(?<ip>\S+) \S+ \S+ \[(?<datetime>[^\]]+)\] "(?<method>\w+) (?<url>\S+) (?<protocol>[^"]+)" (?<status>\d+) (?<bytes>\d+|-) "(?<referer>[^"]*)" "(?<useragent>[^"]*)"/,

  /**
   * Nginx Access Log
   */
  nginx:
    /^(?<ip>\S+) - (?<user>\S+) \[(?<datetime>[^\]]+)\] "(?<request>[^"]+)" (?<status>\d+) (?<bytes>\d+) "(?<referer>[^"]*)" "(?<useragent>[^"]*)"/,

  /**
   * Syslog
   */
  syslog:
    /^(?<priority><\d+>)?(?<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) (?<host>\S+) (?<process>\w+)(?:\[(?<pid>\d+)\])?: (?<message>.+)$/,

  /**
   * Application Log (genérico)
   */
  appLog:
    /^\[(?<timestamp>[\d\-T:.Z]+)\]\s*(?<level>DEBUG|INFO|WARN|ERROR|FATAL)\s*\[(?<source>[^\]]+)\]\s*(?<message>.+)$/,
};

// Uso
const logLine =
  '192.168.1.1 - - [15/Mar/2024:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"';
const match = logLine.match(LogParsers.apache);
console.log(match.groups);
// { ip: "192.168.1.1", datetime: "15/Mar/2024:10:30:45 +0000", ... }
```

### 2.3 Extracción de Datos

```javascript
/**
 * Extractores de datos comunes
 */
const Extractors = {
  /**
   * Extraer emails de texto
   */
  emails: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,

  /**
   * Extraer URLs de texto
   */
  urls: /https?:\/\/[^\s<>"{}|\\^`\[\]]+/g,

  /**
   * Extraer hashtags
   */
  hashtags: /#[a-zA-Z_]\w*/g,

  /**
   * Extraer menciones (@usuario)
   */
  mentions: /@[a-zA-Z_]\w*/g,

  /**
   * Extraer números de versión (semver)
   */
  versions:
    /\bv?(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)(?:-(?<prerelease>[\w.]+))?(?:\+(?<build>[\w.]+))?\b/g,

  /**
   * Extraer direcciones IP
   */
  ipv4: /\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b/g,

  /**
   * Extraer fechas ISO
   */
  isoDate:
    /\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?:T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)?)?/g,

  /**
   * Extraer precios
   */
  prices:
    /[$€£¥]\s*\d+(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?\s*(?:USD|EUR|GBP|JPY)/g,
};
```

### 2.4 Transformación de Texto

```javascript
/**
 * Transformadores de texto
 */
const Transformers = {
  /**
   * Convertir camelCase a snake_case
   */
  camelToSnake(str) {
    return str.replace(/[A-Z]/g, (m) => '_' + m.toLowerCase());
  },

  /**
   * Convertir snake_case a camelCase
   */
  snakeToCamel(str) {
    return str.replace(/_([a-z])/g, (_, char) => char.toUpperCase());
  },

  /**
   * Limpiar HTML (básico)
   */
  stripHtml(str) {
    return str.replace(/<[^>]+>/g, '');
  },

  /**
   * Normalizar espacios
   */
  normalizeSpaces(str) {
    return str.replace(/\s+/g, ' ').trim();
  },

  /**
   * Censurar palabras
   */
  censor(str, words) {
    const pattern = new RegExp(`\\b(${words.join('|')})\\b`, 'gi');
    return str.replace(pattern, (m) => '*'.repeat(m.length));
  },

  /**
   * Escapar HTML
   */
  escapeHtml(str) {
    const entities = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    };
    return str.replace(/[&<>"']/g, (m) => entities[m]);
  },

  /**
   * Formatear número de teléfono
   */
  formatPhone(str) {
    const digits = str.replace(/\D/g, '');
    return digits.replace(/^(\d{3})(\d{3})(\d{4})$/, '($1) $2-$3');
  },
};
```

---

## 3. Debugging de Regex

### 3.1 Técnicas de Debugging

```javascript
/**
 * Herramienta de debugging para regex
 */
function debugRegex(pattern, text) {
  console.log('Pattern:', pattern.toString());
  console.log('Flags:', pattern.flags);
  console.log('Text:', text);
  console.log('Length:', text.length);
  console.log('-'.repeat(50));

  // Test simple
  console.log('test():', pattern.test(text));

  // Reset lastIndex
  pattern.lastIndex = 0;

  // Match
  const match = text.match(pattern);
  console.log('match():', match);

  // Si es global, usar matchAll
  if (pattern.global) {
    pattern.lastIndex = 0;
    console.log('matchAll():');
    for (const m of text.matchAll(pattern)) {
      console.log('  Index:', m.index);
      console.log('  Match:', m[0]);
      if (m.groups) {
        console.log('  Groups:', m.groups);
      }
    }
  }

  // Exec paso a paso
  console.log('-'.repeat(50));
  console.log('exec() step by step:');
  pattern.lastIndex = 0;
  let execMatch;
  let count = 0;
  while ((execMatch = pattern.exec(text)) !== null && count < 10) {
    console.log(`  [${count}] at ${execMatch.index}:`, execMatch[0]);
    count++;
    if (!pattern.global) break;
  }
}
```

### 3.2 Visualización

```javascript
/**
 * Visualizar matches en texto
 */
function visualizeMatches(pattern, text) {
  const lines = [];
  let lastIndex = 0;

  pattern.lastIndex = 0;

  for (const match of text.matchAll(pattern)) {
    // Texto antes del match
    if (match.index > lastIndex) {
      lines.push(text.slice(lastIndex, match.index));
    }
    // El match resaltado
    lines.push(`【${match[0]}】`);
    lastIndex = match.index + match[0].length;
  }

  // Texto restante
  if (lastIndex < text.length) {
    lines.push(text.slice(lastIndex));
  }

  return lines.join('');
}

// Ejemplo
const text = 'Los emails son user@example.com y admin@test.org';
const pattern = /[\w.-]+@[\w.-]+\.\w+/g;
console.log(visualizeMatches(pattern, text));
// "Los emails son 【user@example.com】 y 【admin@test.org】"
```

---

## 4. Testing de Regex

### 4.1 Framework de Testing

```javascript
/**
 * Framework simple para testing de regex
 */
class RegexTest {
  constructor(pattern) {
    this.pattern = pattern;
    this.results = [];
  }

  shouldMatch(text, description = '') {
    const result = this.pattern.test(text);
    this.results.push({
      type: 'match',
      text,
      expected: true,
      actual: result,
      passed: result === true,
      description,
    });
    return this;
  }

  shouldNotMatch(text, description = '') {
    this.pattern.lastIndex = 0;
    const result = this.pattern.test(text);
    this.results.push({
      type: 'no-match',
      text,
      expected: false,
      actual: result,
      passed: result === false,
      description,
    });
    return this;
  }

  shouldCapture(text, expected, description = '') {
    this.pattern.lastIndex = 0;
    const match = text.match(this.pattern);
    const groups = match?.groups || {};
    const passed = JSON.stringify(groups) === JSON.stringify(expected);
    this.results.push({
      type: 'capture',
      text,
      expected,
      actual: groups,
      passed,
      description,
    });
    return this;
  }

  run() {
    console.log(`Testing: ${this.pattern}`);
    console.log('-'.repeat(50));

    let passed = 0;
    let failed = 0;

    for (const r of this.results) {
      const icon = r.passed ? '✅' : '❌';
      const desc = r.description ? ` (${r.description})` : '';
      console.log(`${icon} ${r.type}: "${r.text}"${desc}`);

      if (!r.passed) {
        console.log(`   Expected: ${JSON.stringify(r.expected)}`);
        console.log(`   Actual:   ${JSON.stringify(r.actual)}`);
        failed++;
      } else {
        passed++;
      }
    }

    console.log('-'.repeat(50));
    console.log(`Results: ${passed} passed, ${failed} failed`);

    return failed === 0;
  }
}

// Uso
new RegexTest(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)
  .shouldMatch('user@example.com', 'email simple')
  .shouldMatch('user.name+tag@sub.domain.org', 'email complejo')
  .shouldNotMatch('@example.com', 'sin local part')
  .shouldNotMatch('user@', 'sin domain')
  .shouldNotMatch('user@.com', 'domain vacío')
  .run();
```

### 4.2 Casos Edge

```javascript
/**
 * Generador de casos edge para testing
 */
const EdgeCases = {
  strings: [
    '', // Vacío
    ' ', // Solo espacio
    '   ', // Múltiples espacios
    '\t\n\r', // Whitespace especial
    'a', // Un carácter
    'a'.repeat(1000), // Muy largo
  ],

  emails: {
    valid: [
      'simple@example.com',
      'very.common@example.com',
      'disposable.style.email.with+symbol@example.com',
      'other.email-with-dash@example.com',
      'x@example.com',
      '"much.more unusual"@example.com',
      'example-indeed@strange-example.com',
      'test/test@test.com',
      'admin@mailserver1',
      "#!$%&'*+-/=?^_`{}|~@example.org",
      '"()<>[]:,;@\\"!#$%&\'*+-/=?^_`{}| ~.a"@example.org',
      'example@s.example',
      'user.name+tag+sorting@example.com',
    ],
    invalid: [
      'plainaddress',
      '@example.com',
      'email.example.com',
      'email@example@example.com',
      '.email@example.com',
      'email.@example.com',
      'email..email@example.com',
      'email@example.com (Joe Smith)',
      'email@example',
      'email@-example.com',
      'email@111.222.333.44444',
      'email@example..com',
      'Abc..123@example.com',
    ],
  },

  unicode: [
    'Hello 世界',
    'Привет мир',
    'مرحبا بالعالم',
    '😀🎉🚀',
    'café',
    'naïve',
    'résumé',
    '北京',
  ],
};
```

---

## 5. Best Practices

### 5.1 Documentación

```javascript
/**
 * Patrón: Validador de URL con named groups
 *
 * ¿Por qué?
 * Las URLs tienen estructura compleja con múltiples componentes
 * opcionales (puerto, query, fragment).
 *
 * ¿Para qué?
 * - Validar URLs antes de usarlas
 * - Extraer componentes para procesamiento
 * - Normalizar URLs
 *
 * Componentes:
 * - protocol: http o https
 * - host: dominio o IP
 * - port: puerto (opcional)
 * - path: ruta (opcional)
 * - query: parámetros (opcional)
 * - fragment: ancla (opcional)
 *
 * Limitaciones:
 * - No soporta URLs de data:, file:, etc.
 * - No valida TLDs contra lista oficial
 * - IPv6 no soportado
 *
 * @example
 * const match = url.match(urlPattern);
 * console.log(match.groups.host); // "example.com"
 */
const urlPattern =
  /^(?<protocol>https?):\/\/(?<host>[^/:]+)(?::(?<port>\d+))?(?<path>\/[^?#]*)?(?:\?(?<query>[^#]*))?(?:#(?<fragment>.*))?$/;
```

### 5.2 Performance

```javascript
/**
 * Consejos de rendimiento
 */

// 1. Compilar una vez, usar muchas veces
// ❌ Malo
for (const item of items) {
  if (/pattern/.test(item)) {
  } // Compila en cada iteración
}

// ✅ Bueno
const pattern = /pattern/;
for (const item of items) {
  if (pattern.test(item)) {
  }
}

// 2. Usar test() para verificación simple
// ❌ Innecesario
if (text.match(/pattern/)) {
}

// ✅ Más eficiente
if (/pattern/.test(text)) {
}

// 3. Evitar captura innecesaria
// ❌ Captura sin usar
text.replace(/(foo|bar)/g, 'baz');

// ✅ Non-capturing
text.replace(/(?:foo|bar)/g, 'baz');

// 4. Anclas cuando sea posible
// ❌ Busca en todo el string
if (/^prefix/.test(text)) {
}

// Ya es óptimo con ^, pero recordar usar $ también cuando aplique

// 5. Limitar repeticiones en input no confiable
const MAX_LEN = 1000;
if (input.length <= MAX_LEN && /pattern/.test(input)) {
}
```

---

## 6. Recursos Finales

### Cheatsheet Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                     REGEX CHEATSHEET                            │
├─────────────────────────────────────────────────────────────────┤
│ METACARACTERES                                                  │
│ .   Cualquier carácter (excepto \n sin flag s)                 │
│ ^   Inicio del string (o línea con flag m)                     │
│ $   Fin del string (o línea con flag m)                        │
│ \   Escape                                                      │
├─────────────────────────────────────────────────────────────────┤
│ CLASES                                                          │
│ [abc]    a, b, o c                                              │
│ [^abc]   No a, b, ni c                                          │
│ [a-z]    Rango a-z                                              │
│ \d       Dígito [0-9]                                           │
│ \D       No dígito                                              │
│ \w       Word [a-zA-Z0-9_]                                      │
│ \W       No word                                                │
│ \s       Whitespace                                             │
│ \S       No whitespace                                          │
│ \b       Word boundary                                          │
├─────────────────────────────────────────────────────────────────┤
│ CUANTIFICADORES                                                 │
│ *        0 o más (greedy)                                       │
│ +        1 o más (greedy)                                       │
│ ?        0 o 1 (greedy)                                         │
│ {n}      Exactamente n                                          │
│ {n,}     n o más                                                │
│ {n,m}    Entre n y m                                            │
│ *? +? ?? Lazy                                                   │
├─────────────────────────────────────────────────────────────────┤
│ GRUPOS                                                          │
│ (abc)        Capture group                                      │
│ (?:abc)      Non-capturing group                                │
│ (?<name>abc) Named group                                        │
│ \1           Backreference                                      │
│ \k<name>     Named backreference                                │
├─────────────────────────────────────────────────────────────────┤
│ LOOKAROUND                                                      │
│ (?=abc)      Positive lookahead                                 │
│ (?!abc)      Negative lookahead                                 │
│ (?<=abc)     Positive lookbehind                                │
│ (?<!abc)     Negative lookbehind                                │
├─────────────────────────────────────────────────────────────────┤
│ FLAGS                                                           │
│ g    Global                                                     │
│ i    Case-insensitive                                           │
│ m    Multiline                                                  │
│ s    DotAll                                                     │
│ u    Unicode                                                    │
│ y    Sticky                                                     │
│ d    Indices                                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

**Siguiente:** [Proyecto Final](../3-proyecto/proyecto-final.md)
