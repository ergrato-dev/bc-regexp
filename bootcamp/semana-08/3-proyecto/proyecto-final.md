# Proyecto Final: RegEx Toolkit

## 🎯 Objetivo

Crear una **librería completa de expresiones regulares** con patrones reutilizables, validadores, extractores y transformadores.

## 📋 Descripción

Este proyecto final integra todo lo aprendido en el bootcamp. Crearás un toolkit que pueda usarse en proyectos reales.

## 🛠️ Estructura del Proyecto

```
regex-toolkit/
├── src/
│   ├── validators/
│   │   ├── email.js
│   │   ├── url.js
│   │   ├── phone.js
│   │   ├── password.js
│   │   ├── creditCard.js
│   │   └── index.js
│   │
│   ├── extractors/
│   │   ├── emails.js
│   │   ├── urls.js
│   │   ├── hashtags.js
│   │   ├── mentions.js
│   │   ├── dates.js
│   │   └── index.js
│   │
│   ├── parsers/
│   │   ├── userAgent.js
│   │   ├── log.js
│   │   ├── csv.js
│   │   ├── markdown.js
│   │   └── index.js
│   │
│   ├── transformers/
│   │   ├── case.js
│   │   ├── sanitize.js
│   │   ├── format.js
│   │   └── index.js
│   │
│   └── index.js
│
├── tests/
│   └── *.test.js
│
├── docs/
│   └── api.md
│
└── README.md
```

## 📦 Módulos a Implementar

### 1. Validators

```javascript
// validators/index.js
export const validators = {
  email: (value) => boolean,
  url: (value, options) => boolean,
  phone: (value, countryCode) => boolean,
  password: (value, policy) => { valid: boolean, errors: string[] },
  creditCard: (value) => { valid: boolean, type: string },
  postalCode: (value, country) => boolean,
  username: (value, options) => boolean,
  ipv4: (value) => boolean,
  ipv6: (value) => boolean,
  uuid: (value) => boolean,
  semver: (value) => boolean,
  slug: (value) => boolean
};
```

### 2. Extractors

```javascript
// extractors/index.js
export const extractors = {
  emails: (text) => string[],
  urls: (text) => string[],
  hashtags: (text) => string[],
  mentions: (text) => string[],
  phones: (text) => string[],
  dates: (text) => Date[],
  prices: (text) => { amount: number, currency: string }[],
  ips: (text) => string[],
  versions: (text) => { major, minor, patch }[]
};
```

### 3. Parsers

```javascript
// parsers/index.js
export const parsers = {
  userAgent: (ua) => { browser, version, os, mobile },
  log: (line, format) => { timestamp, level, message, ... },
  csv: (text, options) => array[],
  queryString: (qs) => object,
  url: (url) => { protocol, host, path, query, ... },
  cookie: (str) => object,
  jwt: (token) => { header, payload, signature },
  cron: (expr) => { minute, hour, day, month, weekday }
};
```

### 4. Transformers

```javascript
// transformers/index.js
export const transformers = {
  // Case conversion
  camelToSnake: (str) => string,
  snakeToCamel: (str) => string,
  toKebab: (str) => string,
  toPascal: (str) => string,

  // Sanitization
  stripHtml: (str) => string,
  escapeHtml: (str) => string,
  escapeRegex: (str) => string,
  normalizeSpaces: (str) => string,
  removeAccents: (str) => string,

  // Formatting
  formatPhone: (str, format) => string,
  formatCreditCard: (str) => string,
  formatCurrency: (num, locale) => string,
  slugify: (str) => string,
  truncate: (str, length) => string,
};
```

## ✅ Requisitos Mínimos

| Módulo       | Funciones | Tests |
| ------------ | --------- | ----- |
| Validators   | 8+        | ✓     |
| Extractors   | 6+        | ✓     |
| Parsers      | 4+        | ✓     |
| Transformers | 8+        | ✓     |

## 💡 Ejemplo de Implementación

```javascript
// validators/email.js

/**
 * Validar formato de email
 *
 * ¿Por qué? Email tiene formato RFC 5322
 * ¿Para qué? Validación de formularios
 *
 * @param {string} email - Email a validar
 * @param {object} options - Opciones de validación
 * @returns {boolean}
 */
export function validateEmail(email, options = {}) {
  const {
    allowSubaddress = true, // user+tag@domain
    allowIp = false, // user@[192.168.1.1]
    maxLength = 254,
  } = options;

  if (!email || email.length > maxLength) {
    return false;
  }

  // Patrón base
  let pattern =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

  if (!allowSubaddress) {
    // No permitir + en local-part
    if (email.includes('+')) return false;
  }

  return pattern.test(email);
}

// Tests
console.assert(validateEmail('user@example.com') === true);
console.assert(validateEmail('user+tag@example.com') === true);
console.assert(validateEmail('invalid') === false);
```

## 🚀 Extensiones Opcionales

### CLI Tool

```bash
# Validar email
$ regex-toolkit validate email "user@example.com"
✓ Valid email

# Extraer URLs
$ regex-toolkit extract urls < input.txt
https://example.com
https://another.com

# Transformar
$ echo "helloWorld" | regex-toolkit transform snake
hello_world
```

### Web Demo

Crear una página HTML con:

- Input de texto
- Selector de operación
- Resultado en tiempo real
- Explicación del patrón usado

### TypeScript Types

```typescript
interface ValidationResult {
  valid: boolean;
  errors?: string[];
  warnings?: string[];
}

interface ExtractorOptions {
  unique?: boolean;
  limit?: number;
}

type Validator = (value: string, options?: object) => ValidationResult;
type Extractor = (text: string, options?: ExtractorOptions) => string[];
```

## 📝 Documentación Requerida

Cada función debe incluir:

1. **JSDoc** con @param y @returns
2. **¿Por qué?** - Razón del patrón
3. **¿Para qué?** - Caso de uso
4. **Ejemplos** de uso
5. **Limitaciones** conocidas

## ✅ Criterios de Evaluación

| Criterio                                     | Puntos |
| -------------------------------------------- | ------ |
| Funcionalidad (todos los módulos funcionan)  | 30%    |
| Tests (cobertura mínima 80%)                 | 20%    |
| Documentación                                | 15%    |
| Código limpio y organizado                   | 15%    |
| Optimización (sin catastrophic backtracking) | 10%    |
| Extras (CLI, web demo, TypeScript)           | 10%    |

---

**Solución de referencia:** [solucion-proyecto-final.js](solucion-proyecto-final.js)
