# Glosario - Semana 06: Flags y Modificadores

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### C

#### Case-Insensitive

**Descripción:** Modo de búsqueda que ignora diferencias entre mayúsculas y minúsculas. Se activa con el flag `i`.

```javascript
/**
 * ¿Por qué? Los usuarios escriben con diferente capitalización
 * ¿Para qué? Búsquedas flexibles
 */
/hello/i.test('HELLO'); // true
/hello/i.test('Hello'); // true
/hello/i.test('HeLLo'); // true
```

---

### D

#### DotAll

**Descripción:** Modo donde el punto `.` coincide con CUALQUIER carácter, incluyendo saltos de línea. Se activa con el flag `s`.

```javascript
/**
 * ¿Por qué? Por defecto, . no coincide con \n, \r
 * ¿Para qué? Capturar bloques multilínea
 */

// Sin flag s
/a.b/.test('a\nb'); // false

// Con flag s
/a.b/s.test('a\nb'); // true
```

---

### F

#### Flag

**Descripción:** Modificador que cambia el comportamiento de una expresión regular. Se coloca después del delimitador de cierre.

```javascript
// Sintaxis literal
const regex = /patrón/flags;

// Sintaxis constructor
const regex = new RegExp("patrón", "flags");

// Flags disponibles: g, i, m, s, u, y, d
```

---

### G

#### Global

**Descripción:** Modo que encuentra todas las coincidencias, no solo la primera. Se activa con el flag `g`.

```javascript
/**
 * ¿Por qué? Por defecto solo se encuentra la primera coincidencia
 * ¿Para qué? Encontrar o reemplazar todas las ocurrencias
 */

'abc abc abc'.match(/abc/); // ['abc'] - solo primera
'abc abc abc'.match(/abc/g); // ['abc', 'abc', 'abc'] - todas
```

---

### H

#### hasIndices

**Descripción:** Modo que incluye los índices de inicio y fin de cada grupo en el resultado. Se activa con el flag `d`.

```javascript
/**
 * ¿Por qué? A veces necesitamos las posiciones exactas
 * ¿Para qué? Resaltado de sintaxis, editores
 */
const match = 'test@example.com'.match(/(\w+)@(\w+)/d);

console.log(match.indices);
// [[0, 12], [0, 4], [5, 12]]
//  match    $1      $2
```

**Nota:** Disponible desde ES2022.

---

### M

#### Multiline

**Descripción:** Modo donde `^` y `$` aplican a cada línea, no solo al inicio/fin del string. Se activa con el flag `m`.

```javascript
/**
 * ¿Por qué? Procesar archivos con múltiples líneas
 * ¿Para qué? Validar o extraer por línea
 */
const texto = `Línea 1
Línea 2`;

// Sin flag m
texto.match(/^Línea/g); // ['Línea'] - solo inicio del string

// Con flag m
texto.match(/^Línea/gm); // ['Línea', 'Línea'] - inicio de cada línea
```

---

### S

#### Sticky

**Descripción:** Modo que busca solo en la posición exacta indicada por `lastIndex`. Se activa con el flag `y`.

```javascript
/**
 * ¿Por qué? Necesitamos búsqueda posicional exacta
 * ¿Para qué? Tokenizers, parsers, lexers
 */
const pattern = /\d+/y;
const texto = 'abc123';

pattern.lastIndex = 0;
pattern.exec(texto); // null (no hay dígito en posición 0)

pattern.lastIndex = 3;
pattern.exec(texto); // ['123'] (dígitos en posición 3)
```

---

### U

#### Unicode

**Descripción:** Modo que habilita soporte completo de Unicode. Se activa con el flag `u`.

```javascript
/**
 * ¿Por qué? JavaScript usa UTF-16, algunos caracteres ocupan 2 code units
 * ¿Para qué? Manejar emojis, caracteres especiales, idiomas diversos
 */

// Sin flag u
'😀'.match(/./g); // ['�', '�'] - ¡Incorrecto!

// Con flag u
'😀'.match(/./gu); // ['😀'] - Correcto

// Propiedades Unicode
'Hola 你好'.match(/\p{Letter}+/gu); // ['Hola', '你好']
```

---

## Tabla de Compatibilidad

| Flag | Nombre     | ES Version | Chrome | Firefox | Safari |
| ---- | ---------- | ---------- | ------ | ------- | ------ |
| `g`  | global     | ES3        | ✅     | ✅      | ✅     |
| `i`  | ignoreCase | ES3        | ✅     | ✅      | ✅     |
| `m`  | multiline  | ES3        | ✅     | ✅      | ✅     |
| `u`  | unicode    | ES2015     | 50+    | 46+     | 10+    |
| `y`  | sticky     | ES2015     | 49+    | 3+      | 10+    |
| `s`  | dotAll     | ES2018     | 62+    | 78+     | 11.1+  |
| `d`  | hasIndices | ES2022     | 90+    | 88+     | 15+    |

---

## Propiedades del Objeto RegExp

```javascript
const regex = /patrón/gimu;

// Propiedades booleanas
regex.global; // true - flag g
regex.ignoreCase; // true - flag i
regex.multiline; // true - flag m
regex.unicode; // true - flag u
regex.sticky; // false
regex.dotAll; // false
regex.hasIndices; // false

// String con todos los flags
regex.flags; // "gimu"

// Otras propiedades
regex.source; // "patrón"
regex.lastIndex; // 0 (usado con g, y)
```

---

## Combinaciones Comunes de Flags

| Combinación | Uso Típico                                 |
| ----------- | ------------------------------------------ |
| `g`         | Encontrar/reemplazar todas las ocurrencias |
| `gi`        | Búsqueda global sin distinguir mayúsculas  |
| `gm`        | Procesar archivo línea por línea           |
| `gs`        | Capturar bloques multilínea                |
| `gu`        | Procesar texto internacional               |
| `gim`       | Búsqueda flexible en múltiples líneas      |
| `gimu`      | Búsqueda completa con Unicode              |

---

## Propiedades Unicode Importantes

### Categorías Generales

| Propiedad | Descripción | Ejemplo            |
| --------- | ----------- | ------------------ |
| `\p{L}`   | Letras      | `Hola`, `你好`     |
| `\p{N}`   | Números     | `123`, `①②③`       |
| `\p{P}`   | Puntuación  | `.`, `,`, `!`      |
| `\p{S}`   | Símbolos    | `$`, `€`, `→`      |
| `\p{Z}`   | Separadores | espacios           |
| `\p{C}`   | Control     | caracteres ocultos |

### Scripts (Sistemas de Escritura)

| Propiedad               | Idiomas                     |
| ----------------------- | --------------------------- |
| `\p{Script=Latin}`      | Español, Inglés, Francés... |
| `\p{Script=Cyrillic}`   | Ruso, Ucraniano...          |
| `\p{Script=Han}`        | Chino, Japonés (kanji)...   |
| `\p{Script=Arabic}`     | Árabe, Persa...             |
| `\p{Script=Devanagari}` | Hindi, Sánscrito...         |

---

**Próxima semana:** Patrones Avanzados y Optimización
