# Glosario Final - Semana 08

## Términos del Bootcamp Completo

> **Nota:** La nomenclatura técnica se mantiene en inglés.

---

### A

#### Anchor

Metacarácter que define posición sin consumir caracteres.

- `^` - Inicio
- `$` - Fin
- `\b` - Word boundary

#### Assertion

Ver **Lookaround**.

#### Atomic Group

Grupo que no permite backtracking. No nativo en JavaScript.

---

### B

#### Backreference

Referencia a un grupo capturado anteriormente: `\1`, `\2`, `\k<name>`

#### Backtracking

Mecanismo del motor que retrocede para probar alternativas.

#### Boundary

Límite de posición: `\b` (word), `^` (inicio), `$` (fin).

---

### C

#### Capture Group

Grupo que almacena su contenido: `(pattern)`

#### Character Class

Conjunto de caracteres: `[abc]`, `\d`, `\w`, `\s`

#### Catastrophic Backtracking

Backtracking exponencial que causa DoS.

---

### D

#### DotAll

Flag `s` que permite a `.` coincidir con `\n`.

---

### F

#### Flag

Modificador de comportamiento: `g`, `i`, `m`, `s`, `u`, `y`, `d`

---

### G

#### Global

Flag `g` que encuentra todas las coincidencias.

#### Greedy

Cuantificador que consume lo máximo: `*`, `+`, `?`

#### Group

Agrupación de patrones: `()`, `(?:)`, `(?<name>)`

---

### I

#### IgnoreCase

Flag `i` que ignora mayúsculas/minúsculas.

---

### L

#### Lazy

Cuantificador que consume lo mínimo: `*?`, `+?`, `??`

#### Lookahead

Aserción que mira adelante: `(?=)`, `(?!)`

#### Lookbehind

Aserción que mira atrás: `(?<=)`, `(?<!)`

#### Lookaround

Término general para lookahead y lookbehind.

---

### M

#### Match

Coincidencia encontrada por el patrón.

#### Metacharacter

Carácter con significado especial: `.`, `^`, `$`, `*`, `+`, etc.

#### Multiline

Flag `m` que hace que `^$` apliquen a cada línea.

---

### N

#### Named Capture Group

Grupo con nombre: `(?<name>pattern)`

#### Named Backreference

Referencia a grupo por nombre: `\k<name>`

#### Negation

Clase negada: `[^abc]`

#### Non-capturing Group

Grupo sin captura: `(?:pattern)`

---

### P

#### Pattern

La expresión regular completa.

#### Possessive Quantifier

Cuantificador sin backtracking. No nativo en JavaScript.

#### Positive/Negative

Tipo de lookaround: positive = debe existir, negative = no debe existir.

---

### Q

#### Quantifier

Especifica repeticiones: `*`, `+`, `?`, `{n}`, `{n,m}`

---

### R

#### Range

Rango de caracteres: `[a-z]`, `[0-9]`

#### ReDoS

Regular Expression Denial of Service.

---

### S

#### Sticky

Flag `y` que busca solo en `lastIndex`.

---

### U

#### Unicode

Flag `u` para soporte Unicode completo.

---

### W

#### Word Boundary

Límite entre word y no-word: `\b`

#### Word Character

Letra, dígito o guión bajo: `\w` = `[a-zA-Z0-9_]`

---

## Tabla de Referencia Rápida

| Concepto         | Sintaxis    | Ejemplo            |
| ---------------- | ----------- | ------------------ |
| Literal          | `abc`       | `/hello/`          |
| Cualquier char   | `.`         | `/h.t/`            |
| Inicio           | `^`         | `/^start/`         |
| Fin              | `$`         | `/end$/`           |
| Clase            | `[abc]`     | `/[aeiou]/`        |
| Negación         | `[^abc]`    | `/[^0-9]/`         |
| Dígito           | `\d`        | `/\d{3}/`          |
| Word             | `\w`        | `/\w+/`            |
| Espacio          | `\s`        | `/\s*/`            |
| 0+               | `*`         | `/a*/`             |
| 1+               | `+`         | `/a+/`             |
| 0-1              | `?`         | `/colou?r/`        |
| Exacto           | `{n}`       | `/\d{4}/`          |
| Rango            | `{n,m}`     | `/\d{2,4}/`        |
| Grupo            | `(...)`     | `/(ab)+/`          |
| Non-capture      | `(?:...)`   | `/(?:ab)+/`        |
| Named            | `(?<n>...)` | `/(?<year>\d{4})/` |
| Backref          | `\1`        | `/(a)\1/`          |
| Named ref        | `\k<n>`     | `/\k<year>/`       |
| Lookahead +      | `(?=...)`   | `/a(?=b)/`         |
| Lookahead -      | `(?!...)`   | `/a(?!b)/`         |
| Lookbehind +     | `(?<=...)`  | `/(?<=a)b/`        |
| Lookbehind -     | `(?<!...)`  | `/(?<!a)b/`        |
| Global           | `g`         | `/pattern/g`       |
| Case-insensitive | `i`         | `/pattern/i`       |
| Multiline        | `m`         | `/pattern/m`       |
| DotAll           | `s`         | `/pattern/s`       |
| Unicode          | `u`         | `/pattern/u`       |
| Sticky           | `y`         | `/pattern/y`       |
| Indices          | `d`         | `/pattern/d`       |

---

## ¡Bootcamp Completado! 🎉

Has aprendido:

- ✅ Fundamentos de regex
- ✅ Clases de caracteres
- ✅ Cuantificadores (greedy y lazy)
- ✅ Grupos y capturas
- ✅ Lookahead y lookbehind
- ✅ Flags y modificadores
- ✅ Patrones avanzados y optimización
- ✅ Casos reales de la industria

**¡Ahora eres un experto en expresiones regulares!**
