/**
 * ============================================
 * Solución: Proyecto Final
 * RegEx Toolkit - Librería Completa
 * ============================================
 */

// ============================================
// VALIDATORS
// ============================================

const Validators = {
  /**
   * Validar email
   *
   * ¿Por qué? Email tiene formato RFC 5322
   * ¿Para qué? Validación de formularios
   */
  email(value) {
    if (!value || value.length > 254) return false;
    return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(
      value
    );
  },

  /**
   * Validar URL
   *
   * ¿Por qué? URLs tienen estructura específica
   * ¿Para qué? Validar enlaces antes de usarlos
   */
  url(value, options = {}) {
    const { protocols = ['http', 'https'] } = options;
    const protocolPart = protocols.join('|');
    const pattern = new RegExp(
      `^(?:${protocolPart}):\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b[-a-zA-Z0-9()@:%_+.~#?&/=]*$`
    );
    return pattern.test(value);
  },

  /**
   * Validar teléfono
   *
   * ¿Por qué? Formatos varían por país
   * ¿Para qué? Aceptar múltiples formatos
   */
  phone(value, countryCode = 'US') {
    const patterns = {
      US: /^(\+1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/,
      ES: /^(\+34)?[-.\s]?\d{9}$/,
      MX: /^(\+52)?[-.\s]?\d{10}$/,
      INT: /^\+?[1-9]\d{1,14}$/, // E.164
    };
    return (patterns[countryCode] || patterns.INT).test(
      value.replace(/\s/g, '')
    );
  },

  /**
   * Validar contraseña
   *
   * ¿Por qué? Seguridad requiere complejidad
   * ¿Para qué? Cumplir políticas de seguridad
   */
  password(value, policy = {}) {
    const {
      minLength = 8,
      requireUppercase = true,
      requireLowercase = true,
      requireNumber = true,
      requireSpecial = true,
    } = policy;

    const errors = [];

    if (value.length < minLength) {
      errors.push(`Mínimo ${minLength} caracteres`);
    }
    if (requireUppercase && !/[A-Z]/.test(value)) {
      errors.push('Requiere mayúscula');
    }
    if (requireLowercase && !/[a-z]/.test(value)) {
      errors.push('Requiere minúscula');
    }
    if (requireNumber && !/\d/.test(value)) {
      errors.push('Requiere número');
    }
    if (requireSpecial && !/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
      errors.push('Requiere carácter especial');
    }

    return { valid: errors.length === 0, errors };
  },

  /**
   * Validar tarjeta de crédito
   *
   * ¿Por qué? Detectar tipo y formato
   * ¿Para qué? UX mejorada en pagos
   */
  creditCard(value) {
    const cleaned = value.replace(/[\s-]/g, '');

    const types = [
      { name: 'Visa', pattern: /^4\d{12}(?:\d{3})?$/ },
      { name: 'Mastercard', pattern: /^5[1-5]\d{14}$/ },
      { name: 'Amex', pattern: /^3[47]\d{13}$/ },
      { name: 'Discover', pattern: /^6(?:011|5\d{2})\d{12}$/ },
    ];

    for (const { name, pattern } of types) {
      if (pattern.test(cleaned)) {
        return { valid: true, type: name };
      }
    }

    return { valid: false, type: null };
  },

  /**
   * Validar UUID
   */
  uuid(value) {
    return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
      value
    );
  },

  /**
   * Validar IPv4
   */
  ipv4(value) {
    return /^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$/.test(
      value
    );
  },

  /**
   * Validar semver
   */
  semver(value) {
    return /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/.test(
      value
    );
  },

  /**
   * Validar slug
   */
  slug(value) {
    return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value);
  },
};

// ============================================
// EXTRACTORS
// ============================================

const Extractors = {
  /**
   * Extraer emails
   */
  emails(text, options = {}) {
    const { unique = true } = options;
    const pattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
    const matches = text.match(pattern) || [];
    return unique ? [...new Set(matches)] : matches;
  },

  /**
   * Extraer URLs
   */
  urls(text, options = {}) {
    const { unique = true } = options;
    const pattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/g;
    const matches = text.match(pattern) || [];
    return unique ? [...new Set(matches)] : matches;
  },

  /**
   * Extraer hashtags
   */
  hashtags(text, options = {}) {
    const { unique = true, withSymbol = false } = options;
    const pattern = /#([a-zA-Z_]\w*)/g;
    const matches = [];
    for (const match of text.matchAll(pattern)) {
      matches.push(withSymbol ? match[0] : match[1]);
    }
    return unique ? [...new Set(matches)] : matches;
  },

  /**
   * Extraer menciones
   */
  mentions(text, options = {}) {
    const { unique = true, withSymbol = false } = options;
    const pattern = /@([a-zA-Z_]\w*)/g;
    const matches = [];
    for (const match of text.matchAll(pattern)) {
      matches.push(withSymbol ? match[0] : match[1]);
    }
    return unique ? [...new Set(matches)] : matches;
  },

  /**
   * Extraer fechas ISO
   */
  dates(text) {
    const pattern =
      /\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?:T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)?)?/g;
    const matches = text.match(pattern) || [];
    return matches.map((d) => new Date(d));
  },

  /**
   * Extraer IPs
   */
  ips(text) {
    const pattern =
      /\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b/g;
    return [...new Set(text.match(pattern) || [])];
  },

  /**
   * Extraer precios
   */
  prices(text) {
    const pattern = /(?<currency>[$€£¥])\s*(?<amount>\d+(?:[.,]\d{1,2})?)/g;
    const results = [];
    for (const match of text.matchAll(pattern)) {
      results.push({
        currency: match.groups.currency,
        amount: parseFloat(match.groups.amount.replace(',', '.')),
      });
    }
    return results;
  },
};

// ============================================
// PARSERS
// ============================================

const Parsers = {
  /**
   * Parsear User Agent
   */
  userAgent(ua) {
    const result = {
      browser: null,
      browserVersion: null,
      os: null,
      osVersion: null,
      mobile: false,
    };

    // OS
    const osPatterns = [
      { pattern: /Windows NT ([\d.]+)/, name: 'Windows' },
      { pattern: /Mac OS X ([\d_]+)/, name: 'macOS' },
      { pattern: /Android ([\d.]+)/, name: 'Android' },
      { pattern: /iPhone OS ([\d_]+)/, name: 'iOS' },
      { pattern: /Linux/, name: 'Linux' },
    ];

    for (const { pattern, name } of osPatterns) {
      const match = ua.match(pattern);
      if (match) {
        result.os = name;
        result.osVersion = match[1]?.replace(/_/g, '.') || null;
        break;
      }
    }

    // Browser
    const browserPatterns = [
      { pattern: /Edg(?:e)?\/([\d.]+)/, name: 'Edge' },
      { pattern: /Chrome\/([\d.]+)/, name: 'Chrome' },
      { pattern: /Firefox\/([\d.]+)/, name: 'Firefox' },
      { pattern: /Version\/([\d.]+).*Safari/, name: 'Safari' },
    ];

    for (const { pattern, name } of browserPatterns) {
      const match = ua.match(pattern);
      if (match) {
        result.browser = name;
        result.browserVersion = match[1];
        break;
      }
    }

    result.mobile = /Mobile|iPhone|Android.*Mobile/i.test(ua);

    return result;
  },

  /**
   * Parsear Query String
   */
  queryString(qs) {
    const result = {};
    const pattern = /[?&]([^=]+)=([^&]*)/g;

    for (const match of qs.matchAll(pattern)) {
      const key = decodeURIComponent(match[1]);
      const value = decodeURIComponent(match[2]);
      result[key] = value;
    }

    return result;
  },

  /**
   * Parsear URL
   */
  url(url) {
    const pattern =
      /^(?<protocol>https?):\/\/(?:(?<user>[^:@]+)(?::(?<password>[^@]+))?@)?(?<host>[^/:]+)(?::(?<port>\d+))?(?<path>\/[^?#]*)?(?:\?(?<query>[^#]*))?(?:#(?<hash>.*))?$/;

    const match = url.match(pattern);
    if (!match) return null;

    return {
      ...match.groups,
      port: match.groups.port ? parseInt(match.groups.port) : null,
      queryParams: match.groups.query
        ? this.queryString('?' + match.groups.query)
        : {},
    };
  },

  /**
   * Parsear CSV línea
   */
  csvLine(line, delimiter = ',') {
    const pattern = new RegExp(
      `(?:^|${delimiter})(?:"([^"]*(?:""[^"]*)*)"|([^${delimiter}"]*))`,
      'g'
    );

    const fields = [];
    for (const match of line.matchAll(pattern)) {
      let value =
        match[1] !== undefined ? match[1].replace(/""/g, '"') : match[2];
      fields.push(value);
    }

    return fields;
  },
};

// ============================================
// TRANSFORMERS
// ============================================

const Transformers = {
  /**
   * camelCase a snake_case
   */
  camelToSnake(str) {
    return str.replace(/[A-Z]/g, (m) => '_' + m.toLowerCase());
  },

  /**
   * snake_case a camelCase
   */
  snakeToCamel(str) {
    return str.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
  },

  /**
   * A kebab-case
   */
  toKebab(str) {
    return str
      .replace(/([a-z])([A-Z])/g, '$1-$2')
      .replace(/[\s_]+/g, '-')
      .toLowerCase();
  },

  /**
   * A PascalCase
   */
  toPascal(str) {
    return str
      .replace(/(?:^|[\s_-])(\w)/g, (_, c) => c.toUpperCase())
      .replace(/[\s_-]/g, '');
  },

  /**
   * Eliminar HTML
   */
  stripHtml(str) {
    return str.replace(/<[^>]+>/g, '');
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
   * Escapar regex
   */
  escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  },

  /**
   * Normalizar espacios
   */
  normalizeSpaces(str) {
    return str.replace(/\s+/g, ' ').trim();
  },

  /**
   * Crear slug
   */
  slugify(str) {
    return str
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // Remover acentos
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  },

  /**
   * Formatear teléfono
   */
  formatPhone(str, format = '(###) ###-####') {
    const digits = str.replace(/\D/g, '');
    let i = 0;
    return format.replace(/#/g, () => digits[i++] || '');
  },

  /**
   * Formatear tarjeta
   */
  formatCreditCard(str) {
    const digits = str.replace(/\D/g, '');
    return digits.replace(/(\d{4})(?=\d)/g, '$1 ');
  },

  /**
   * Truncar texto
   */
  truncate(str, length, suffix = '...') {
    if (str.length <= length) return str;
    return str.slice(0, length - suffix.length) + suffix;
  },
};

// ============================================
// EXPORTS & DEMO
// ============================================

const RegexToolkit = {
  validators: Validators,
  extractors: Extractors,
  parsers: Parsers,
  transformers: Transformers,
};

// Demo
console.log('=== RegEx Toolkit Demo ===\n');

console.log('-- Validators --');
console.log('Email:', Validators.email('user@example.com'));
console.log('Password:', Validators.password('Weak'));
console.log('Credit Card:', Validators.creditCard('4532-1234-5678-9012'));

console.log('\n-- Extractors --');
const text =
  'Contact us at hello@example.com or visit https://example.com #regex @mention';
console.log('Emails:', Extractors.emails(text));
console.log('URLs:', Extractors.urls(text));
console.log('Hashtags:', Extractors.hashtags(text));
console.log('Mentions:', Extractors.mentions(text));

console.log('\n-- Parsers --');
console.log('Query:', Parsers.queryString('?name=John&age=30'));
console.log(
  'URL:',
  Parsers.url('https://user:pass@example.com:8080/path?q=1#hash')
);

console.log('\n-- Transformers --');
console.log('camelToSnake:', Transformers.camelToSnake('helloWorld'));
console.log('slugify:', Transformers.slugify('Hola Mundo! Café'));
console.log('formatPhone:', Transformers.formatPhone('5551234567'));

// module.exports = RegexToolkit;
