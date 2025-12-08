# Soluciones Finales - Semana 08

---

## Ejercicio 1: Parser de User Agent

```javascript
/**
 * ¿Por qué? User agents son complejos con múltiples formatos
 * ¿Para qué? Analytics, compatibilidad, detección de dispositivos
 */

function parseUserAgent(ua) {
  const result = {
    platform: null,
    platformVersion: null,
    browser: null,
    browserVersion: null,
    mobile: false,
  };

  // Detectar plataforma
  const platformPatterns = [
    { pattern: /Windows NT (?<version>[\d.]+)/, name: 'Windows' },
    { pattern: /Mac OS X (?<version>[\d_]+)/, name: 'Macintosh' },
    { pattern: /iPhone OS (?<version>[\d_]+)/, name: 'iPhone' },
    { pattern: /Android (?<version>[\d.]+)/, name: 'Android' },
    { pattern: /Linux/, name: 'Linux' },
  ];

  for (const { pattern, name } of platformPatterns) {
    const match = ua.match(pattern);
    if (match) {
      result.platform = name;
      result.platformVersion =
        match.groups?.version?.replace(/_/g, '.') || null;
      break;
    }
  }

  // Detectar navegador (orden importa - más específico primero)
  const browserPatterns = [
    { pattern: /Edg(?:e)?\/(?<version>[\d.]+)/, name: 'Edge' },
    { pattern: /Chrome\/(?<version>[\d.]+)/, name: 'Chrome' },
    { pattern: /Firefox\/(?<version>[\d.]+)/, name: 'Firefox' },
    { pattern: /Version\/(?<version>[\d.]+).*Safari/, name: 'Safari' },
    { pattern: /Safari\/(?<version>[\d.]+)/, name: 'Safari' },
  ];

  for (const { pattern, name } of browserPatterns) {
    const match = ua.match(pattern);
    if (match) {
      result.browser = name;
      result.browserVersion = match.groups?.version || null;
      break;
    }
  }

  // Detectar móvil
  result.mobile = /Mobile|iPhone|Android.*Mobile/i.test(ua);

  return result;
}

// Tests
const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 Version/17.2 Mobile Safari/604.1',
];

userAgents.forEach((ua) => {
  console.log(parseUserAgent(ua));
});
```

---

## Ejercicio 2: Validador de Markdown

````javascript
/**
 * ¿Por qué? Markdown tiene sintaxis específica para cada elemento
 * ¿Para qué? Renderizado, validación, transformación
 */

const markdownPatterns = {
  heading: /^(?<hashes>#{1,6})\s+(?<content>.+)$/gm,
  bold: /\*\*(?<content>[^*]+)\*\*/g,
  italic: /(?<!\*)\*(?<content>[^*]+)\*(?!\*)/g,
  boldItalic: /\*\*\*(?<content>[^*]+)\*\*\*/g,
  strikethrough: /~~(?<content>[^~]+)~~/g,
  inlineCode: /`(?<content>[^`]+)`/g,
  link: /\[(?<text>[^\]]+)\]\((?<url>[^)]+)\)/g,
  image: /!\[(?<alt>[^\]]*)\]\((?<url>[^)]+)\)/g,
  listItem: /^(?<indent>\s*)(?<marker>[-*]|\d+\.)\s+(?<content>.+)$/gm,
  blockquote: /^>\s*(?<content>.+)$/gm,
  codeBlock: /```(?<lang>\w*)?\n(?<code>[\s\S]*?)```/g,
};

function parseMarkdown(text) {
  const elements = [];

  // Headings
  for (const match of text.matchAll(markdownPatterns.heading)) {
    elements.push({
      type: 'heading',
      level: match.groups.hashes.length,
      content: match.groups.content,
      index: match.index,
    });
  }

  // Bold
  for (const match of text.matchAll(markdownPatterns.bold)) {
    elements.push({
      type: 'bold',
      content: match.groups.content,
      index: match.index,
    });
  }

  // Links
  for (const match of text.matchAll(markdownPatterns.link)) {
    elements.push({
      type: 'link',
      text: match.groups.text,
      url: match.groups.url,
      index: match.index,
    });
  }

  // Images
  for (const match of text.matchAll(markdownPatterns.image)) {
    elements.push({
      type: 'image',
      alt: match.groups.alt,
      url: match.groups.url,
      index: match.index,
    });
  }

  // Code blocks
  for (const match of text.matchAll(markdownPatterns.codeBlock)) {
    elements.push({
      type: 'codeBlock',
      language: match.groups.lang || null,
      code: match.groups.code,
      index: match.index,
    });
  }

  // Ordenar por posición
  elements.sort((a, b) => a.index - b.index);

  return elements;
}

// Test
const markdown = `# Title
This is **bold** and *italic*.
[Link](https://example.com)
![Image](image.png)
`;

console.log(parseMarkdown(markdown));
````

---

## Ejercicio 3: Analizador de SQL

```javascript
/**
 * ¿Por qué? SQL tiene estructura predecible
 * ¿Para qué? Validación, logging, análisis de queries
 */

const sqlPatterns = {
  select:
    /^SELECT\s+(?<columns>.+?)\s+FROM\s+(?<table>\w+)(?:\s+WHERE\s+(?<where>.+?))?(?:\s+ORDER\s+BY\s+(?<orderBy>.+?))?(?:\s+LIMIT\s+(?<limit>\d+))?$/i,

  insert:
    /^INSERT\s+INTO\s+(?<table>\w+)\s*\((?<columns>[^)]+)\)\s*VALUES\s*\((?<values>.+)\)$/i,

  update:
    /^UPDATE\s+(?<table>\w+)\s+SET\s+(?<sets>.+?)(?:\s+WHERE\s+(?<where>.+))?$/i,

  delete: /^DELETE\s+FROM\s+(?<table>\w+)(?:\s+WHERE\s+(?<where>.+))?$/i,
};

function parseSQL(query) {
  query = query.trim();

  // Detectar tipo
  const type = query.split(/\s+/)[0].toUpperCase();

  const pattern = sqlPatterns[type.toLowerCase()];
  if (!pattern) {
    return { error: 'Unsupported query type', type };
  }

  const match = query.match(pattern);
  if (!match) {
    return { error: 'Invalid query syntax', type };
  }

  const result = {
    type,
    ...match.groups,
  };

  // Parsear columnas si es SELECT
  if (type === 'SELECT' && result.columns) {
    result.columns =
      result.columns === '*'
        ? ['*']
        : result.columns.split(',').map((c) => c.trim());
  }

  return result;
}

// Tests
const queries = [
  'SELECT id, name, email FROM users WHERE active = 1',
  "INSERT INTO logs (timestamp, message) VALUES ('2024-03-15', 'Test')",
  "UPDATE users SET status = 'active' WHERE id = 42",
  'DELETE FROM sessions WHERE expires < NOW()',
];

queries.forEach((q) => console.log(parseSQL(q)));
```

---

## Ejercicio 4: Validador de Configuración

```javascript
/**
 * ¿Por qué? Archivos de config tienen formato consistente
 * ¿Para qué? Cargar configuración en aplicaciones
 */

function parseConfig(text) {
  const config = { _default: {} };
  let currentSection = '_default';

  const patterns = {
    comment: /^\s*[#;]/,
    section: /^\s*\[(?<name>\w+)\]\s*$/,
    keyValue: /^\s*(?<key>[\w.]+)\s*=\s*(?<value>.+?)\s*$/,
  };

  const lines = text.split('\n');

  for (const line of lines) {
    // Ignorar vacías y comentarios
    if (!line.trim() || patterns.comment.test(line)) {
      continue;
    }

    // Sección
    const sectionMatch = line.match(patterns.section);
    if (sectionMatch) {
      currentSection = sectionMatch.groups.name;
      if (!config[currentSection]) {
        config[currentSection] = {};
      }
      continue;
    }

    // Key=Value
    const kvMatch = line.match(patterns.keyValue);
    if (kvMatch) {
      let { key, value } = kvMatch.groups;

      // Remover comillas
      if (/^["'].*["']$/.test(value)) {
        value = value.slice(1, -1);
      }
      // Parsear tipos
      else if (value === 'true') value = true;
      else if (value === 'false') value = false;
      else if (/^\d+$/.test(value)) value = parseInt(value);
      else if (/^\d+\.\d+$/.test(value)) value = parseFloat(value);

      config[currentSection][key] = value;
    }
  }

  return config;
}

// Test
const configText = `
# Database settings
DB_HOST=localhost
DB_PORT=5432
DEBUG=true

[production]
DB_HOST=prod-db.example.com
DEBUG=false
`;

console.log(parseConfig(configText));
```

---

## Ejercicio 5: Extractor de Metadatos de Código

```javascript
/**
 * ¿Por qué? JSDoc y comentarios contienen metadata valiosa
 * ¿Para qué? Documentación, análisis estático
 */

const metadataPatterns = {
  fileBlock: /\/\*\*[\s\S]*?@file\s+(?<description>.+?)[\s\S]*?\*\//,
  author: /@author\s+(?<name>[^<\n]+)(?:<(?<email>[^>]+)>)?/g,
  version: /@version\s+(?<version>[\d.]+)/,
  since: /@since\s+(?<version>[\d.]+)/,
  license: /@license\s+(?<license>\w+)/,

  todo: /\/\/\s*(?<type>TODO|FIXME|NOTE|HACK|XXX):?\s*(?<message>.+)/gi,

  jsdoc: /\/\*\*[\s\S]*?\*\/\s*(?:async\s+)?function\s+(?<funcName>\w+)/g,
  param: /@param\s+\{(?<type>[^}]+)\}\s+(?<name>\w+)\s*-?\s*(?<desc>.*)/g,
  returns: /@returns?\s+\{(?<type>[^}]+)\}\s*(?<desc>.*)/,
  throws: /@throws?\s+\{(?<type>[^}]+)\}\s*(?<desc>.*)/,
  deprecated: /@deprecated\s*(?<message>.*)?/,
};

function extractMetadata(code) {
  const metadata = {
    file: null,
    authors: [],
    version: null,
    todos: [],
    functions: [],
  };

  // File metadata
  const fileMatch = code.match(metadataPatterns.fileBlock);
  if (fileMatch) {
    metadata.file = fileMatch.groups.description;

    const versionMatch = fileMatch[0].match(metadataPatterns.version);
    if (versionMatch) metadata.version = versionMatch.groups.version;
  }

  // Authors
  for (const match of code.matchAll(metadataPatterns.author)) {
    metadata.authors.push({
      name: match.groups.name.trim(),
      email: match.groups.email || null,
    });
  }

  // TODOs
  for (const match of code.matchAll(metadataPatterns.todo)) {
    metadata.todos.push({
      type: match.groups.type.toUpperCase(),
      message: match.groups.message,
    });
  }

  return metadata;
}

// Test
const code = `
/**
 * @file User Authentication
 * @author John Doe <john@example.com>
 * @version 2.0.0
 */

// TODO: Implement password reset
// FIXME: Handle expired tokens
`;

console.log(extractMetadata(code));
```

---

## Ejercicio 6: Parser de Commits de Git

```javascript
/**
 * ¿Por qué? Conventional Commits tiene formato estándar
 * ¿Para qué? Changelog automático, versionado semántico
 */

const commitPattern =
  /^(?<type>feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(?:\((?<scope>[^)]+)\))?(?<breaking>!)?: (?<description>.+)$/;

const footerPatterns = {
  breakingChange: /^BREAKING CHANGE:\s*(?<message>.+)$/m,
  closes: /(?:Closes?|Fixes?|Resolves?)\s+#(?<issue>\d+)/gi,
};

function parseCommit(message) {
  const lines = message.trim().split('\n');
  const headerLine = lines[0];

  const headerMatch = headerLine.match(commitPattern);
  if (!headerMatch) {
    return { error: 'Invalid commit format', raw: message };
  }

  const result = {
    type: headerMatch.groups.type,
    scope: headerMatch.groups.scope || null,
    breaking: headerMatch.groups.breaking === '!',
    description: headerMatch.groups.description,
    body: null,
    issues: [],
  };

  // Body (líneas 2+, hasta footer)
  if (lines.length > 1) {
    const bodyLines = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i];

      // Check BREAKING CHANGE
      const breakingMatch = line.match(footerPatterns.breakingChange);
      if (breakingMatch) {
        result.breaking = true;
        result.breakingMessage = breakingMatch.groups.message;
        continue;
      }

      // Check issue references
      for (const match of line.matchAll(footerPatterns.closes)) {
        result.issues.push(parseInt(match.groups.issue));
      }

      if (line.trim() && !footerPatterns.closes.test(line)) {
        bodyLines.push(line);
      }
    }

    if (bodyLines.length > 0) {
      result.body = bodyLines.join('\n').trim();
    }
  }

  return result;
}

// Tests
const commits = [
  'feat(auth): add login with Google OAuth',
  'fix!: remove deprecated API\n\nBREAKING CHANGE: The old API is gone\n\nCloses #123',
];

commits.forEach((c) => console.log(parseCommit(c)));
```

---

## Ejercicio 7: Validador de Semver

```javascript
/**
 * ¿Por qué? Semver es el estándar de versionado
 * ¿Para qué? Gestión de dependencias, comparación de versiones
 */

const semverPattern =
  /^(?<major>0|[1-9]\d*)\.(?<minor>0|[1-9]\d*)\.(?<patch>0|[1-9]\d*)(?:-(?<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/;

function parseSemver(version) {
  const match = version.match(semverPattern);
  if (!match) return null;

  return {
    major: parseInt(match.groups.major),
    minor: parseInt(match.groups.minor),
    patch: parseInt(match.groups.patch),
    prerelease: match.groups.prerelease || null,
    build: match.groups.build || null,
    isPrerelease: !!match.groups.prerelease,
  };
}

function compareSemver(a, b) {
  const va = parseSemver(a);
  const vb = parseSemver(b);

  if (!va || !vb) return NaN;

  // Compare major.minor.patch
  if (va.major !== vb.major) return va.major - vb.major;
  if (va.minor !== vb.minor) return va.minor - vb.minor;
  if (va.patch !== vb.patch) return va.patch - vb.patch;

  // Prerelease has lower precedence
  if (va.prerelease && !vb.prerelease) return -1;
  if (!va.prerelease && vb.prerelease) return 1;

  return 0;
}

// Tests
console.log(parseSemver('1.2.3-alpha.1+build.123'));
console.log(compareSemver('1.0.0', '2.0.0')); // -1
console.log(compareSemver('1.0.0', '1.0.0-alpha')); // 1
```
