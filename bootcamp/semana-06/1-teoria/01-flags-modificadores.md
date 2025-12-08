# Flags y Modificadores

## ¿Qué son los Flags?

Los **flags** (también llamados modificadores) cambian el comportamiento global de una expresión regular. Se colocan después de la barra de cierre `/patrón/flags`.

## Flags Disponibles en JavaScript

| Flag | Nombre           | Descripción                       | ES     |
| ---- | ---------------- | --------------------------------- | ------ |
| `g`  | Global           | Encuentra todas las coincidencias | ES3    |
| `i`  | Case-Insensitive | Ignora mayúsculas/minúsculas      | ES3    |
| `m`  | Multiline        | `^` y `$` aplican a cada línea    | ES3    |
| `s`  | DotAll           | `.` incluye saltos de línea       | ES2018 |
| `u`  | Unicode          | Soporte Unicode completo          | ES2015 |
| `y`  | Sticky           | Busca desde posición específica   | ES2015 |
| `d`  | hasIndices       | Incluye índices de grupos         | ES2022 |

## Flag `g` - Global

El flag más común. Encuentra **todas** las coincidencias, no solo la primera.

```javascript
/**
 * Flag g: búsqueda global
 *
 * ¿Por qué? Por defecto, regex solo encuentra la primera coincidencia
 * ¿Para qué? Encontrar, contar o reemplazar todas las ocurrencias
 */

// Sin flag g: solo primera coincidencia
'abc abc abc'.match(/abc/);
// ['abc', index: 0]

// Con flag g: todas las coincidencias
'abc abc abc'.match(/abc/g);
// ['abc', 'abc', 'abc']
```

### ⚠️ Advertencia: `match()` con `g` pierde información

```javascript
// Sin g: tienes grupos y metadatos
'ana@test.com'.match(/(\w+)@(\w+)\.(\w+)/);
// ['ana@test.com', 'ana', 'test', 'com', index: 0, ...]

// Con g: solo los matches, sin grupos
'ana@a.com, bob@b.com'.match(/(\w+)@(\w+)\.(\w+)/g);
// ['ana@a.com', 'bob@b.com']

// Solución: usar matchAll
for (const m of 'ana@a.com, bob@b.com'.matchAll(/(\w+)@(\w+)\.(\w+)/g)) {
  console.log(m[1], m[2], m[3]); // ana a com, bob b com
}
```

## Flag `i` - Case-Insensitive

Ignora diferencias entre mayúsculas y minúsculas.

```javascript
/**
 * Flag i: case-insensitive
 *
 * ¿Por qué? Los usuarios escriben con diferente capitalización
 * ¿Para qué? Búsquedas flexibles, validación tolerante
 */

// Sin flag i: sensible a mayúsculas
/hello/.test('Hello'); // false
/hello/.test('hello'); // true

// Con flag i: ignora mayúsculas
/hello/i.test('Hello'); // true
/hello/i.test('HELLO'); // true
/hello/i.test('hElLo'); // true
```

### Ejemplo Práctico

```javascript
/**
 * Buscar palabras clave en texto
 */
const keywords = /error|warning|critical/gi;

const log = 'Error: Connection failed. WARNING: Retry limit. critical failure';
console.log(log.match(keywords));
// ['Error', 'WARNING', 'critical']
```

## Flag `m` - Multiline

Cambia el comportamiento de `^` y `$` para que apliquen a cada línea.

```javascript
/**
 * Flag m: multiline
 *
 * ¿Por qué? Por defecto, ^ y $ solo aplican a inicio/fin del STRING
 * ¿Para qué? Procesar archivos con múltiples líneas
 */

const texto = `Línea 1
Línea 2
Línea 3`;

// Sin flag m: ^ solo coincide al inicio del string
texto.match(/^Línea/g);
// ['Línea']  - Solo la primera

// Con flag m: ^ coincide al inicio de cada línea
texto.match(/^Línea/gm);
// ['Línea', 'Línea', 'Línea']
```

### Ejemplo Práctico

```javascript
/**
 * Extraer líneas que empiezan con #
 */
const config = `# Comentario 1
nombre=valor
# Comentario 2
otro=dato`;

const comentarios = config.match(/^#.+$/gm);
console.log(comentarios);
// ['# Comentario 1', '# Comentario 2']
```

### Diferencia entre `^$` y `\A\Z`

En JavaScript no hay `\A` y `\Z`, pero puedes simularlos:

```javascript
// ^ siempre inicio de string (sin m)
// $ siempre fin de string (sin m)

// Con m:
// ^ inicio de línea
// $ fin de línea
```

## Flag `s` - DotAll (ES2018)

Hace que `.` coincida con **cualquier** carácter, incluyendo saltos de línea.

```javascript
/**
 * Flag s: dotall
 *
 * ¿Por qué? Por defecto, . no coincide con \n, \r
 * ¿Para qué? Capturar bloques multilínea
 */

const html = `<div>
  Contenido
  multilínea
</div>`;

// Sin flag s: . no cruza líneas
html.match(/<div>.*<\/div>/);
// null

// Con flag s: . incluye saltos de línea
html.match(/<div>.*<\/div>/s);
// ['<div>\n  Contenido\n  multilínea\n</div>']
```

### Alternativa sin flag `s`

```javascript
// Antes de ES2018, se usaba [\s\S] en lugar de .
html.match(/<div>[\s\S]*<\/div>/);
// Funciona igual
```

## Flag `u` - Unicode (ES2015)

Habilita soporte completo de Unicode.

```javascript
/**
 * Flag u: unicode
 *
 * ¿Por qué? JavaScript usa UTF-16, algunos caracteres son 2 code units
 * ¿Para qué? Manejar emojis, caracteres especiales, idiomas diversos
 */

// Sin flag u: emoji cuenta como 2 caracteres
'😀'.match(/./g);
// ['�', '�']  - ¡Incorrecto!

// Con flag u: emoji es 1 carácter
'😀'.match(/./gu);
// ['😀']  - Correcto
```

### Propiedades Unicode

Con el flag `u`, puedes usar `\p{...}` para propiedades Unicode:

```javascript
/**
 * Propiedades Unicode
 */

// Letras de cualquier idioma
/\p{Letter}/gu
/\p{L}/gu  // Forma corta

// Ejemplos
"Hola 你好 مرحبا".match(/\p{L}+/gu);
// ['Hola', '你好', 'مرحبا']

// Emojis
"Hello 👋 World 🌍".match(/\p{Emoji}/gu);
// ['👋', '🌍']

// Dígitos de cualquier sistema
"123 ١٢٣ 一二三".match(/\p{Number}+/gu);
// ['123', '١٢٣']
```

### Propiedades Comunes

| Propiedad                   | Descripción       |
| --------------------------- | ----------------- |
| `\p{L}` / `\p{Letter}`      | Cualquier letra   |
| `\p{N}` / `\p{Number}`      | Cualquier número  |
| `\p{P}` / `\p{Punctuation}` | Puntuación        |
| `\p{S}` / `\p{Symbol}`      | Símbolos          |
| `\p{Emoji}`                 | Emojis            |
| `\p{Script=Latin}`          | Escritura latina  |
| `\p{Script=Han}`            | Caracteres chinos |

## Flag `y` - Sticky (ES2015)

Busca solo en la posición exacta indicada por `lastIndex`.

```javascript
/**
 * Flag y: sticky
 *
 * ¿Por qué? Necesitamos búsquedas posicionales exactas
 * ¿Para qué? Tokenizers, parsers, lexers
 */

const pattern = /\d+/y;
const texto = 'abc123def456';

pattern.lastIndex = 0;
console.log(pattern.exec(texto)); // null (no hay dígito en posición 0)

pattern.lastIndex = 3;
console.log(pattern.exec(texto)); // ['123'] (hay dígitos en posición 3)

pattern.lastIndex = 6;
console.log(pattern.exec(texto)); // null (hay 'def', no dígitos)

pattern.lastIndex = 9;
console.log(pattern.exec(texto)); // ['456'] (dígitos en posición 9)
```

### Diferencia entre `g` y `y`

```javascript
const gPattern = /\d+/g;
const yPattern = /\d+/y;
const texto = 'abc123';

gPattern.lastIndex = 0;
gPattern.exec(texto); // ['123'] - busca en todo el string

yPattern.lastIndex = 0;
yPattern.exec(texto); // null - solo busca en posición 0
```

## Flag `d` - hasIndices (ES2022)

Incluye índices de inicio y fin para cada grupo.

```javascript
/**
 * Flag d: hasIndices
 *
 * ¿Por qué? A veces necesitamos saber dónde está cada grupo
 * ¿Para qué? Resaltado de sintaxis, herramientas de edición
 */

const pattern = /(\d+)-(\d+)/d;
const match = 'Rango: 10-20'.match(pattern);

console.log(match.indices);
// [[7, 12], [7, 9], [10, 12]]
//  ↑         ↑       ↑
//  match     $1      $2
//  completo
```

## Combinando Flags

Los flags se pueden combinar libremente:

```javascript
// Global + case-insensitive
/hello/gi

// Global + multiline
/^start/gm

// Global + dotall + unicode
/./gsu

// Todos juntos
const allFlags = /patrón/gimsuy;
```

## Flags en el Constructor

Cuando usas `new RegExp()`, los flags van como segundo argumento:

```javascript
// Literal
const regex1 = /patrón/gi;

// Constructor
const regex2 = new RegExp('patrón', 'gi');

// Dinámico
const searchTerm = 'hello';
const pattern = new RegExp(searchTerm, 'gi');
```

## Acceder a los Flags

```javascript
const regex = /abc/gimu;

// Propiedades booleanas
regex.global; // true
regex.ignoreCase; // true
regex.multiline; // true
regex.unicode; // true
regex.sticky; // false
regex.dotAll; // false
regex.hasIndices; // false

// String con todos los flags
regex.flags; // "gimu"
```

---

**Siguiente:** [Ejercicios de Flags](../2-ejercicios/ejercicio-06-flags.md)
