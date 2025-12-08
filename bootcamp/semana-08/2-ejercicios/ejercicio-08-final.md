# Ejercicios Finales - Semana 08

## Instrucciones

Estos ejercicios integran todos los conceptos del bootcamp. Cada ejercicio representa un caso real de la industria.

---

## Ejercicio 1: Parser de User Agent

### Objetivo

Extraer información de strings de User Agent de navegadores.

### Texto de Prueba

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15
Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36
```

### Requisitos

Extraer con named groups:

- `platform`: Windows, Macintosh, iPhone, Android, Linux
- `platformVersion`: versión del OS
- `browser`: Chrome, Safari, Firefox, Edge
- `browserVersion`: versión del navegador
- `mobile`: boolean (si es móvil)

### Resultado Esperado

```javascript
{
  platform: "Windows",
  platformVersion: "10.0",
  browser: "Chrome",
  browserVersion: "120.0.0.0",
  mobile: false
}
```

---

## Ejercicio 2: Validador de Markdown

### Objetivo

Detectar y extraer elementos de Markdown.

### Elementos a Detectar

````markdown
# Heading 1

## Heading 2

### Heading 3

**bold text**
_italic text_
**_bold italic_**
~~strikethrough~~
`inline code`

[link text](url)
![alt text](image-url)

- list item

* list item

1. numbered item

> blockquote

`code block`
````

### Requisitos

1. Crear patrones para cada elemento
2. Extraer contenido y metadatos
3. Clasificar por tipo

### Resultado Esperado

```javascript
[
  { type: 'heading', level: 1, content: 'Heading 1' },
  { type: 'bold', content: 'bold text' },
  { type: 'link', text: 'link text', url: 'url' },
  // ...
];
```

---

## Ejercicio 3: Analizador de SQL

### Objetivo

Parsear queries SQL simples.

### Queries de Prueba

```sql
SELECT id, name, email FROM users WHERE active = 1
SELECT * FROM products WHERE price > 100 ORDER BY name
INSERT INTO logs (timestamp, message) VALUES ('2024-03-15', 'Test')
UPDATE users SET status = 'active' WHERE id = 42
DELETE FROM sessions WHERE expires < NOW()
```

### Requisitos

Detectar y extraer:

- Tipo de query (SELECT, INSERT, UPDATE, DELETE)
- Tablas involucradas
- Columnas seleccionadas/modificadas
- Condiciones WHERE

---

## Ejercicio 4: Validador de Configuración

### Objetivo

Parsear archivos de configuración tipo `.env` o `.ini`.

### Texto de Prueba

```ini
# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=admin
DB_PASSWORD="my secret password"

# API Configuration
API_KEY=sk-123abc456def
API_URL=https://api.example.com/v1
DEBUG=true
MAX_RETRIES=3

[production]
DB_HOST=prod-db.example.com
DEBUG=false
```

### Requisitos

1. Ignorar comentarios
2. Parsear secciones `[section]`
3. Extraer pares key=value
4. Manejar valores con comillas
5. Validar tipos (boolean, number, string)

---

## Ejercicio 5: Extractor de Metadatos de Código

### Objetivo

Extraer metadatos de archivos de código.

### Texto de Prueba

```javascript
/**
 * @file User Authentication Module
 * @author John Doe <john@example.com>
 * @version 2.0.0
 * @since 1.0.0
 * @license MIT
 */

// TODO: Implement password reset
// FIXME: Handle edge case for expired tokens
// NOTE: This uses JWT for authentication

/**
 * Authenticate user with credentials
 * @param {string} username - The username
 * @param {string} password - The password
 * @returns {Promise<User>} The authenticated user
 * @throws {AuthError} If authentication fails
 */
async function authenticate(username, password) {
  // Implementation
}

/**
 * @deprecated Use authenticate() instead
 */
function login(user, pass) {
  // Legacy
}
```

### Requisitos

Extraer:

- File metadata (@file, @author, @version, etc.)
- TODO, FIXME, NOTE comments
- JSDoc de funciones (@param, @returns, @throws)
- Funciones deprecadas

---

## Ejercicio 6: Parser de Commits de Git

### Objetivo

Parsear mensajes de commit de Git según Conventional Commits.

### Commits de Prueba

```
feat(auth): add login with Google OAuth
fix(api): handle null response from server
docs: update README with installation instructions
style: format code according to prettier config
refactor(user): extract validation to separate module
test(auth): add unit tests for login flow
chore(deps): bump lodash from 4.17.20 to 4.17.21
feat!: remove deprecated API endpoints

BREAKING CHANGE: The /v1/users endpoint is no longer available

fix(ui): correct button alignment on mobile

Closes #123
Fixes #456, #789
```

### Requisitos

Extraer:

- type: feat, fix, docs, etc.
- scope (opcional)
- breaking: boolean
- description
- body (opcional)
- footer: issues referenced

---

## Ejercicio 7: Validador de Semver

### Objetivo

Validar y comparar versiones semánticas.

### Versiones de Prueba

```
1.0.0
2.1.3
0.0.1
1.0.0-alpha
1.0.0-alpha.1
1.0.0-beta.2
1.0.0-rc.1
2.0.0-beta.1+build.123
1.2.3+build.456
10.20.30
```

### Requisitos

1. Validar formato semver completo
2. Extraer: major, minor, patch, prerelease, build
3. Crear función de comparación (>, <, =)
4. Detectar versiones prerelease

---

## Desafío Final: Motor de Plantillas

### Objetivo

Crear un motor de plantillas simple tipo Handlebars/Mustache.

### Sintaxis de Template

```handlebars
<h1>{{title}}</h1>

{{#if user}}
  <p>Welcome, {{user.name}}!</p>

  {{#each items}}
    <li>{{name}} - ${{price}}</li>
  {{/each}}
{{else}}
  <p>Please login</p>
{{/if}}

{{#with settings}}
  <p>Theme: {{theme}}</p>
{{/with}}

{{> partialName}}

{{{unescapedHtml}}}
```

### Requisitos

1. Variables: `{{variable}}`
2. Variables con path: `{{object.property}}`
3. Condicionales: `{{#if}}...{{else}}...{{/if}}`
4. Loops: `{{#each}}...{{/each}}`
5. Context: `{{#with}}...{{/with}}`
6. Partials: `{{> name}}`
7. HTML no escapado: `{{{html}}}`
8. Comentarios: `{{! comment }}`

### Implementación

```javascript
function parseTemplate(template) {
  // Retornar AST del template
}

function render(template, data) {
  // Renderizar template con datos
}

// Uso
const template = 'Hello, {{name}}!';
const result = render(template, { name: 'World' });
// "Hello, World!"
```

---

## Formato de Entrega

````markdown
## Ejercicio X

### Patrón

```javascript
const pattern = /tu-regex-aquí/;
```
````

### Explicación

¿Por qué? [razón]
¿Para qué? [propósito]

### Tests

```javascript
// Casos válidos
// Casos inválidos
```

### Función completa

```javascript
// Implementación
```

```

---

**Soluciones:** [solucion-08-final.md](solucion-08-final.md)
```
