# Glosario - Semana 01: Fundamentos de RegExp

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### A

#### Anchor

**Descripción:** Elemento que coincide con una posición, no con un carácter.

```javascript
// ^ (caret) - anchor de inicio
// $ (dollar) - anchor de fin
/^inicio/   // Coincide al principio
/final$/    // Coincide al final
```

**Uso:** Validar que un patrón esté en una posición específica.

---

### B

#### Backslash (`\`)

**Descripción:** Carácter de escape que modifica el significado del siguiente carácter.

```javascript
// Escapar metacaracteres
/\./   // Punto literal, no metacaracter
/\$/   // Dólar literal, no anchor

// Crear secuencias especiales
/\d/   // Cualquier dígito
/\n/   // Nueva línea
```

**Uso:** Buscar caracteres especiales literalmente o crear atajos.

---

### C

#### Caret (`^`)

**Descripción:** Metacharacter que indica el inicio del string o línea.

```javascript
/^Hola/; // "Hola" debe estar al inicio
```

**Uso:** Validar que algo esté al principio.

---

### D

#### Dollar (`$`)

**Descripción:** Metacharacter que indica el fin del string o línea.

```javascript
/mundo$/; // "mundo" debe estar al final
```

**Uso:** Validar que algo esté al final.

#### Dot (`.`)

**Descripción:** Metacharacter que coincide con cualquier carácter excepto nueva línea.

```javascript
/c.sa/; // casa, cosa, cesa, c@sa, c1sa...
```

**Uso:** Comodín para un carácter desconocido.

---

### E

#### Escape

**Descripción:** Proceso de usar `\` para cambiar el significado de un carácter.

```javascript
// Sin escape: . = cualquier carácter
// Con escape: \. = punto literal
```

**Uso:** Buscar metacaracteres como caracteres normales.

---

### F

#### Flag

**Descripción:** Modificador que cambia el comportamiento del pattern.

```javascript
/patrón/g / // g = global (todas las coincidencias)
  patrón /
  i / // i = case-insensitive
  patrón /
  m; // m = multiline
```

**Uso:** Ajustar cómo se ejecuta la búsqueda.

---

### L

#### Literal

**Descripción:** Carácter que se busca exactamente como se escribe.

```javascript
/gato/; // Busca literalmente "gato"
```

**Uso:** Búsqueda de texto exacto.

---

### M

#### Match

**Descripción:** Coincidencia encontrada entre el pattern y el texto.

```javascript
const texto = 'El gato negro';
const pattern = /gato/;
// Match: "gato" (posición 3-6)
```

#### Metacharacter

**Descripción:** Carácter con significado especial en regex.

```
. ^ $ * + ? { } [ ] \ | ( )
```

**Uso:** Construir patrones flexibles y poderosos.

---

### P

#### Pattern

**Descripción:** La expresión regular completa que define qué buscar.

```javascript
const pattern = /^[a-z]+@\w+\.\w{2,}$/;
//              └────────────────────┘
//                    El pattern
```

---

### R

#### RegExp / Regex / Regular Expression

**Descripción:** Secuencia de caracteres que define un patrón de búsqueda.

```javascript
// Notación literal
const regex = /patrón/flags;

// Constructor
const regex = new RegExp("patrón", "flags");
```

---

### T

#### Test

**Descripción:** Método que verifica si hay coincidencia (retorna boolean).

```javascript
/gato/.test('El gato duerme'); // true
```

---

## Tabla de Metacaracteres - Semana 01

| Símbolo | Nombre    | Descripción                       | Ejemplo                 |
| ------- | --------- | --------------------------------- | ----------------------- |
| `.`     | Dot       | Cualquier carácter (excepto `\n`) | `/c.sa/` → casa, cosa   |
| `^`     | Caret     | Inicio del string                 | `/^Hola/` → "Hola..."   |
| `$`     | Dollar    | Fin del string                    | `/mundo$/` → "...mundo" |
| `\`     | Backslash | Escape                            | `/\./` → punto literal  |

---

## Métodos Importantes - Semana 01

| Método      | Objeto | Retorna       | Uso                 |
| ----------- | ------ | ------------- | ------------------- |
| `test()`    | RegExp | `boolean`     | ¿Existe el match?   |
| `exec()`    | RegExp | `Array\|null` | Info del match      |
| `match()`   | String | `Array\|null` | Encontrar matches   |
| `search()`  | String | `number`      | Posición del match  |
| `replace()` | String | `string`      | Buscar y reemplazar |
| `split()`   | String | `Array`       | Dividir por patrón  |

---

## Conceptos Clave

### Match Exacto vs Parcial

```javascript
// Match parcial (el pattern está DENTRO del string)
/gato/.test('El gato negro'); // true

// Match exacto (el pattern ES todo el string)
/^gato$/.test('gato'); // true
/^gato$/.test('El gato'); // false
```

### Sensibilidad a Mayúsculas

```javascript
// Por defecto, regex es case-sensitive
/Gato/.test('gato'); // false
/Gato/.test('Gato'); // true

// Con flag 'i', ignora mayúsculas
/Gato/i.test('gato'); // true
```

---

**Próxima semana:** Character classes (`[abc]`, `\d`, `\w`, `\s`)
