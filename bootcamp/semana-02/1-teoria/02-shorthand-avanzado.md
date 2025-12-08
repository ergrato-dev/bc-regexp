# Semana 02: Shorthand Classes y Word Boundaries

## Word Boundary: `\b`

El **word boundary** es un anchor especial que coincide con la posición entre un word character (`\w`) y un non-word character (`\W`), o al inicio/fin del string.

```javascript
/**
 * ¿Por qué? Queremos encontrar palabras completas, no substrings
 * ¿Para qué? Evitar matches parciales no deseados
 */

// Problema de la semana 01: "Java" matchea dentro de "JavaScript"
const java = /Java/;
java.test('JavaScript'); // true 😱

// Solución con word boundary
const javaExacto = /\bJava\b/;
javaExacto.test('JavaScript'); // false ✅
javaExacto.test('Java es cool'); // true ✅
javaExacto.test('Java'); // true ✅
```

### Visualización

```
"JavaScript es genial"
 │         │
 └─────────┴─ \b está entre espacios y letras

/\bJava\b/ busca:
  - boundary ANTES de 'J'
  - "Java"
  - boundary DESPUÉS de 'a'

En "JavaScript":
  J-a-v-a-S-c-r-i-p-t
  ↑       ↑
  \b      NO hay \b aquí (a→S son ambos \w)
```

### Casos de Uso

```javascript
/**
 * Encontrar la palabra "the" sin capturar "there", "other", etc.
 *
 * ¿Por qué? "the" aparece dentro de muchas palabras
 * ¿Para qué? Contar ocurrencias del artículo en un texto
 */
const theWord = /\bthe\b/gi;

const texto = 'The other day, there was the cat';
texto.match(theWord); // ['The', 'the'] (no "there" ni "other")
```

### `\B` - Non-Word Boundary

```javascript
/**
 * ¿Por qué? A veces queremos lo opuesto: matches DENTRO de palabras
 * ¿Para qué? Encontrar substrings que no estén al borde
 */
const dentroDepalabra = /\Bcat\B/;

dentroDepalabra.test('education'); // true (cat está en medio)
dentroDepalabra.test('cat'); // false (cat está en los bordes)
dentroDepalabra.test('category'); // false (cat está al inicio)
```

## Combinando Character Classes

### Patrones Comunes

```javascript
/**
 * Username válido: letras, números, guión bajo
 * Longitud: por ahora sin restricción (semana 03)
 *
 * ¿Por qué? Los usernames tienen restricciones de caracteres
 * ¿Para qué? Primera capa de validación
 */
const usernameChars = /^\w+$/; // + = uno o más (adelanto semana 03)

// Solo word characters de inicio a fin
usernameChars.test('usuario_123'); // true
usernameChars.test('user@name'); // false (@ no es \w)
```

```javascript
/**
 * Solo letras (sin números ni guión bajo)
 *
 * ¿Por qué? Nombres propios solo tienen letras
 * ¿Para qué? Validar campos de nombre/apellido
 */
const soloLetras = /^[a-zA-Z]+$/;

soloLetras.test('Juan'); // true
soloLetras.test('Juan123'); // false
soloLetras.test('María'); // false (con tilde - ver nota Unicode)
```

> **Nota sobre Unicode:** `[a-zA-Z]` no incluye caracteres acentuados. Para soporte completo de español, necesitarías incluir: `[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]` o usar flags Unicode (semana 06).

### Validación de Formato

```javascript
/**
 * Validar placa de vehículo (formato ejemplo: ABC-1234)
 *
 * ¿Por qué? Las placas tienen formato específico por país
 * ¿Para qué? Validar registro de vehículos
 */
const placa = /^[A-Z][A-Z][A-Z]-\d\d\d\d$/;

placa.test('ABC-1234'); // true
placa.test('AB-1234'); // false (2 letras)
placa.test('ABC1234'); // false (sin guión)
placa.test('abc-1234'); // false (minúsculas)
```

## Casos Especiales

### El Punto Dentro de Character Class

```javascript
/**
 * ¿Por qué? Dentro de [] el punto pierde su significado especial
 * ¿Para qué? Incluir punto literal sin escapar
 */

// Fuera de []: punto = cualquier carácter
/a.c/.test('abc'); // true
/a.c/.test('a.c'); // true

// Dentro de []: punto = punto literal
/a[.]c/.test('abc'); // false
/a[.]c/.test('a.c'); // true
```

### Rangos Invertidos

```javascript
/**
 * ¿Por qué? A veces la negación es más clara
 * ¿Para qué? Definir lo que NO queremos en vez de lo que sí
 */

// Todo excepto dígitos y espacios
const sinDigitosNiEspacios = /[^\d\s]/;

sinDigitosNiEspacios.test('a'); // true
sinDigitosNiEspacios.test('5'); // false
sinDigitosNiEspacios.test(' '); // false
sinDigitosNiEspacios.test('!'); // true
```

## Comparación: `.` vs `\w` vs `\S`

```javascript
/**
 * Entender las diferencias entre comodines
 */

const texto = 'a 5 @ \n';

// . = cualquier carácter excepto newline
/a./.test('a '); // true
/a./.test('a\n'); // false

// \w = solo word characters [a-zA-Z0-9_]
/\w/.test('a'); // true
/\w/.test(' '); // false
/\w/.test('@'); // false

// \S = cualquier cosa que no sea whitespace
/\S/.test('a'); // true
/\S/.test('@'); // true
/\S/.test(' '); // false
```

### Tabla Comparativa

```
┌─────────┬───────────────────────────────────────────────────┐
│ Pattern │ Coincide con                                      │
├─────────┼───────────────────────────────────────────────────┤
│ .       │ Cualquier carácter excepto \n                     │
│ \d      │ Solo dígitos: 0-9                                 │
│ \w      │ Letras, dígitos, guión bajo: a-zA-Z0-9_          │
│ \s      │ Espacios en blanco: espacio, tab, newline        │
│ \S      │ Cualquier cosa excepto whitespace                 │
│ \D      │ Cualquier cosa excepto dígitos                    │
│ \W      │ Cualquier cosa excepto word characters            │
│ \b      │ Límite de palabra (posición, no carácter)        │
└─────────┴───────────────────────────────────────────────────┘
```

## Ejercicio Mental

Antes de pasar a los ejercicios, intenta predecir el resultado:

```javascript
// ¿Cuáles son true?
/\d/.test('abc'); // ???
/\D/.test('abc'); // ???
/\w/.test('@'); // ???
/\W/.test('@'); // ???
/\bcat\b/.test('cat'); // ???
/\bcat\b/.test('cats'); // ???
/[^a-z]/.test('A'); // ???
/[a-z^]/.test('^'); // ???
```

<details>
<summary>Ver respuestas</summary>

```javascript
/\d/.test('abc'); // false - no hay dígitos
/\D/.test('abc'); // true  - 'a' no es dígito
/\w/.test('@'); // false - @ no es word char
/\W/.test('@'); // true  - @ no es word char
/\bcat\b/.test('cat'); // true  - palabra completa
/\bcat\b/.test('cats'); // false - tiene 's' después
/[^a-z]/.test('A'); // true  - A no es minúscula
/[a-z^]/.test('^'); // true  - ^ literal al final
```

</details>

---

**Siguiente:** Ejercicios prácticos en `2-ejercicios/`
