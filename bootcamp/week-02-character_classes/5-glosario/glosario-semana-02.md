# Glosario - Semana 02: Character Classes

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### C

#### Character Class

**Descripción:** Conjunto de caracteres entre corchetes que define qué caracteres son válidos en una posición.

```javascript
// Character class personalizada
/[aeiou]/ / // Coincide con cualquier vocal
  // Con rango
  [a - z] / // Cualquier minúscula
  // Con negación
  /[^0-9]/; // Cualquier cosa excepto dígitos
```

**Uso:** Definir conjuntos específicos de caracteres válidos.

---

### N

#### Negated Character Class

**Descripción:** Character class precedida por `^` que excluye los caracteres listados.

```javascript
/[^abc]/   // Cualquier carácter EXCEPTO a, b, c
/[^0-9]/   // Cualquier carácter que NO sea dígito
```

**Uso:** Definir caracteres no permitidos.

---

### R

#### Range

**Descripción:** Especificación de un rango de caracteres usando guión dentro de character class.

```javascript
/[a-z]/    // Letras minúsculas (a hasta z)
/[A-Z]/    // Letras mayúsculas
/[0-9]/    // Dígitos (equivale a \d)
/[a-zA-Z]/ // Cualquier letra
```

**Uso:** Definir rangos de caracteres de forma concisa.

---

### S

#### Shorthand Character Class

**Descripción:** Atajos predefinidos para character classes comunes.

```javascript
\d  // [0-9]          - Dígito
\D  // [^0-9]         - NO dígito
\w  // [a-zA-Z0-9_]   - Word character
\W  // [^a-zA-Z0-9_]  - NO word character
\s  // Whitespace (espacio, tab, newline)
\S  // NO whitespace
```

**Uso:** Escribir patrones más concisos y legibles.

---

### W

#### Word Boundary (`\b`)

**Descripción:** Anchor que coincide con la posición entre un word character y un non-word character.

```javascript
/\bcat\b/  // "cat" como palabra completa
/\bcat/    // Palabras que empiezan con "cat"
/cat\b/    // Palabras que terminan con "cat"
```

**Uso:** Encontrar palabras completas, evitar matches parciales.

#### Word Character

**Descripción:** Caracteres que forman "palabras": letras, dígitos y guión bajo.

```javascript
// Word characters: a-z, A-Z, 0-9, _
\w.test("a");  // true
\w.test("5");  // true
\w.test("_");  // true
\w.test("@");  // false (no es word character)
```

**Uso:** Validar identificadores, variables, usernames.

---

## Tabla de Shorthand Classes

| Shorthand | Nombre         | Equivalente      | Descripción               |
| --------- | -------------- | ---------------- | ------------------------- |
| `\d`      | Digit          | `[0-9]`          | Cualquier dígito          |
| `\D`      | Non-digit      | `[^0-9]`         | NO dígito                 |
| `\w`      | Word           | `[a-zA-Z0-9_]`   | Letra, dígito, guión bajo |
| `\W`      | Non-word       | `[^a-zA-Z0-9_]`  | NO word character         |
| `\s`      | Whitespace     | `[ \t\n\r\f\v]`  | Espacio en blanco         |
| `\S`      | Non-whitespace | `[^ \t\n\r\f\v]` | NO whitespace             |
| `\b`      | Boundary       | -                | Límite de palabra         |
| `\B`      | Non-boundary   | -                | NO límite de palabra      |

---

## Sintaxis de Character Classes

### Estructura Básica

```
[caracteres]     → Cualquiera de estos caracteres
[^caracteres]    → Ninguno de estos caracteres
[a-z]            → Rango de a hasta z
[a-zA-Z0-9]      → Múltiples rangos combinados
```

### Caracteres Especiales Dentro de `[]`

| Carácter | Significado               | Escape necesario       |
| -------- | ------------------------- | ---------------------- |
| `^`      | Negación (solo al inicio) | `\^` o no al inicio    |
| `-`      | Rango (entre caracteres)  | `\-` o al inicio/final |
| `]`      | Cierra la clase           | `\]` siempre           |
| `\`      | Escape                    | `\\` siempre           |
| `.`      | Punto literal             | No necesita escape     |
| `$`      | Dólar literal             | No necesita escape     |

---

## Comparación de Metacaracteres

### Semana 01 vs Semana 02

| Semana 01            | Semana 02                   | Diferencia       |
| -------------------- | --------------------------- | ---------------- |
| `.` (cualquier char) | `[abc]` (chars específicos) | Especificidad    |
| `^` (inicio)         | `[^...]` (negación)         | Contexto         |
| `$` (fin)            | `\b` (word boundary)        | Tipo de posición |

---

## Ejemplos de Uso Común

### Validaciones Típicas

```javascript
// Solo dígitos
/^\d+$/

// Solo letras
/^[a-zA-Z]+$/

// Alfanumérico
/^[a-zA-Z0-9]+$/

// Username (letras, números, guión bajo)
/^\w+$/

// Sin espacios
/^\S+$/
```

### Detección

```javascript
// Tiene dígitos
/\d/

// Tiene espacios
/\s/

// Tiene caracteres especiales
/[^a-zA-Z0-9]/

// Palabra completa
/\bpalabra\b/
```

---

## Errores Frecuentes

### 1. `^` dentro vs fuera de `[]`

```javascript
// ❌ Confusión común
/^[abc]/    // Empieza con a, b, o c
/[^abc]/    // Cualquiera EXCEPTO a, b, c
```

### 2. Guión no escapado

```javascript
// ❌ Crea rango accidentalmente
/[a-z-0]/   // ¿Rango de z a 0? Error!

// ✅ Correcto
/[a-z\-0]/  // a-z, guión, o 0
/[-a-z0]/   // Guión al inicio
```

### 3. Olvidar que `\w` incluye `_`

```javascript
// ❌ Si no quieres guión bajo
/\w+/.test('user_name'); // true

// ✅ Si quieres excluirlo
/[a-zA-Z0-9]+/.test('user_name'); // false para el _
```

---

**Próxima semana:** Quantifiers (`*`, `+`, `?`, `{n,m}`) y greedy vs lazy
