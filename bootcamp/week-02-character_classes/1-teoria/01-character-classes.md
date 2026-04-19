# Semana 02: Character Classes (Clases de Caracteres)

<p align="center">
  <img src="../0-assets/character-classes.svg" alt="Character Classes" width="100%">
</p>

## Introducción

En la semana anterior usamos el dot (`.`) como comodín para "cualquier carácter". Pero, ¿qué pasa si queremos ser más específicos? Por ejemplo, solo dígitos, solo letras, o un conjunto específico de caracteres.

Las **character classes** nos permiten definir exactamente qué caracteres son válidos en una posición.

## Character Classes Personalizadas: `[...]`

### Sintaxis Básica

```javascript
/**
 * ¿Por qué? Necesitamos restringir qué caracteres son válidos
 * ¿Para qué? Validar que solo aparezcan caracteres específicos
 */

// Coincidir con 'a', 'e', 'i', 'o', 'u'
const vocales = /[aeiou]/;

vocales.test('hola'); // true (tiene 'o' y 'a')
vocales.test('xyz'); // false (no tiene vocales)
```

### Cómo Funciona

```
[abc]  →  Coincide con UN carácter que sea 'a', 'b', o 'c'
 │││
 ││└─ o 'c'
 │└── o 'b'
 └─── 'a'
```

### Ejemplos Prácticos

```javascript
/**
 * Validar respuesta sí/no
 *
 * ¿Por qué? El usuario puede responder con 's', 'S', 'n', 'N'
 * ¿Para qué? Aceptar variaciones de una respuesta simple
 */
const siNo = /^[sSnN]$/;

siNo.test('s'); // true
siNo.test('S'); // true
siNo.test('n'); // true
siNo.test('x'); // false

/**
 * Validar vocal en una posición específica
 *
 * ¿Por qué? Algunas palabras requieren vocal en cierta posición
 * ¿Para qué? Patrones de palabras específicos
 */
const palabraConVocal = /^c[aeiou]sa$/;

palabraConVocal.test('casa'); // true
palabraConVocal.test('cesa'); // true
palabraConVocal.test('cxsa'); // false
```

## Rangos: `[a-z]`, `[0-9]`

En lugar de escribir todos los caracteres, podemos usar rangos.

```javascript
/**
 * ¿Por qué? Escribir [abcdefghijklmnopqrstuvwxyz] es muy largo
 * ¿Para qué? Definir rangos de caracteres de forma concisa
 */

// Letras minúsculas
const minusculas = /[a-z]/;

// Letras mayúsculas
const mayusculas = /[A-Z]/;

// Dígitos
const digitos = /[0-9]/;

// Combinaciones
const alfanumerico = /[a-zA-Z0-9]/;
```

### Múltiples Rangos

```javascript
/**
 * Validar carácter hexadecimal
 *
 * ¿Por qué? Los colores hex usan 0-9 y A-F (o a-f)
 * ¿Para qué? Validar códigos de color como #FF6B35
 */
const hexChar = /[0-9a-fA-F]/;

hexChar.test('F'); // true
hexChar.test('9'); // true
hexChar.test('G'); // false (no es hex)
```

## Negación: `[^...]`

El caret (`^`) **dentro** de una character class significa "NOT" (negación).

> ⚠️ **Cuidado:** `^` tiene dos significados:
>
> - Fuera de `[]`: anchor de inicio
> - Dentro de `[]` al principio: negación

```javascript
/**
 * ¿Por qué? A veces es más fácil definir lo que NO queremos
 * ¿Para qué? Excluir caracteres específicos
 */

// Cualquier cosa que NO sea vocal
const noVocal = /[^aeiou]/;

noVocal.test('x'); // true (x no es vocal)
noVocal.test('a'); // false (a ES vocal)

// Cualquier cosa que NO sea dígito
const noDigito = /[^0-9]/;

noDigito.test('a'); // true
noDigito.test('5'); // false
```

### Ejemplo: Limpiar Input

```javascript
/**
 * Encontrar caracteres no permitidos en un nombre de usuario
 *
 * ¿Por qué? Los usernames solo deben tener letras, números y guión bajo
 * ¿Para qué? Detectar y rechazar caracteres inválidos
 */
const caracterInvalido = /[^a-zA-Z0-9_]/;

caracterInvalido.test('usuario123'); // false (todo válido)
caracterInvalido.test('usuario@123'); // true (@ no es válido)
caracterInvalido.test('user name'); // true (espacio no es válido)
```

## Caracteres Especiales Dentro de `[]`

Dentro de una character class, la mayoría de metacaracteres pierden su significado especial:

```javascript
/**
 * ¿Por qué? Dentro de [] las reglas cambian
 * ¿Para qué? Poder incluir caracteres que normalmente son especiales
 */

// El punto es literal dentro de []
const puntoOcoma = /[.,]/;
puntoOcoma.test('.'); // true
puntoOcoma.test(','); // true

// Pero estos SÍ necesitan escape:
// - ] → cierra la clase
// - \ → escape
// - ^ → negación (solo al inicio)
// - - → rango (solo entre caracteres)

// Ejemplo: incluir el guión literal
const conGuion = /[a-z\-]/; // Escapado
const conGuion2 = /[-a-z]/; // Al inicio (no es rango)
const conGuion3 = /[a-z-]/; // Al final (no es rango)
```

## Shorthand Character Classes

JavaScript proporciona atajos para las clases más comunes:

### `\d` - Dígitos

```javascript
/**
 * ¿Por qué? [0-9] es muy común
 * ¿Para qué? Escribir patrones más concisos
 */
const digito = /\d/; // Equivale a [0-9]

digito.test('5'); // true
digito.test('a'); // false

// Negación: \D = NO dígito = [^0-9]
const noDigito = /\D/;
noDigito.test('a'); // true
noDigito.test('5'); // false
```

### `\w` - Word Characters

```javascript
/**
 * ¿Por qué? Letras, números y guión bajo son muy comunes
 * ¿Para qué? Validar identificadores, variables, usernames
 */
const wordChar = /\w/; // Equivale a [a-zA-Z0-9_]

wordChar.test('a'); // true
wordChar.test('5'); // true
wordChar.test('_'); // true
wordChar.test('@'); // false

// Negación: \W = NO word character = [^a-zA-Z0-9_]
const noWordChar = /\W/;
noWordChar.test('@'); // true
noWordChar.test('a'); // false
```

### `\s` - Whitespace

```javascript
/**
 * ¿Por qué? Espacios, tabs y newlines son comunes en texto
 * ¿Para qué? Detectar o limpiar espacios en blanco
 */
const espacio = /\s/; // Espacio, tab, newline, etc.

espacio.test(' '); // true
espacio.test('\t'); // true
espacio.test('\n'); // true
espacio.test('a'); // false

// Negación: \S = NO whitespace
const noEspacio = /\S/;
noEspacio.test('a'); // true
noEspacio.test(' '); // false
```

## Tabla Resumen

```
┌─────────────────────────────────────────────────────────────┐
│                   CHARACTER CLASSES                         │
├──────────┬────────────────┬─────────────────────────────────┤
│ Sintaxis │ Equivalente    │ Descripción                     │
├──────────┼────────────────┼─────────────────────────────────┤
│ [abc]    │ -              │ 'a', 'b', o 'c'                 │
│ [^abc]   │ -              │ Cualquiera EXCEPTO 'a','b','c'  │
│ [a-z]    │ -              │ Letra minúscula                 │
│ [A-Z]    │ -              │ Letra mayúscula                 │
│ [0-9]    │ -              │ Dígito                          │
│ [a-zA-Z] │ -              │ Cualquier letra                 │
├──────────┼────────────────┼─────────────────────────────────┤
│ \d       │ [0-9]          │ Dígito                          │
│ \D       │ [^0-9]         │ NO dígito                       │
│ \w       │ [a-zA-Z0-9_]   │ Word character                  │
│ \W       │ [^a-zA-Z0-9_]  │ NO word character               │
│ \s       │ [ \t\n\r\f\v]  │ Whitespace                      │
│ \S       │ [^ \t\n\r\f\v] │ NO whitespace                   │
└──────────┴────────────────┴─────────────────────────────────┘
```

## Ejemplos Integrados

### Validar Código Postal (5 dígitos)

```javascript
/**
 * ¿Por qué? Los códigos postales tienen exactamente 5 dígitos
 * ¿Para qué? Validar input de dirección
 */
const codigoPostal = /^\d\d\d\d\d$/;
//                    │ │ │ │ │ │
//                    │ └─┴─┴─┴─┴── 5 dígitos
//                    └──────────── Inicio y fin exacto

codigoPostal.test('12345'); // true
codigoPostal.test('1234'); // false (4 dígitos)
codigoPostal.test('1234a'); // false (tiene letra)
```

> **Nota:** En la próxima semana aprenderemos cuantificadores para escribir esto como `/^\d{5}$/`

### Validar Inicial + Número

```javascript
/**
 * Formato: Una letra mayúscula seguida de 3 dígitos
 * Ejemplo: A123, B456, Z999
 *
 * ¿Por qué? Códigos de empleado usan este formato
 * ¿Para qué? Validar IDs en sistema de RRHH
 */
const codigoEmpleado = /^[A-Z]\d\d\d$/;

codigoEmpleado.test('A123'); // true
codigoEmpleado.test('a123'); // false (minúscula)
codigoEmpleado.test('AB23'); // false (dos letras)
```

### Detectar Caracteres Problemáticos

```javascript
/**
 * Encontrar caracteres que podrían causar problemas en nombres de archivo
 *
 * ¿Por qué? Algunos caracteres no son válidos en sistemas de archivos
 * ¿Para qué? Sanitizar nombres antes de guardar
 */
const caracterProblematico = /[<>:"/\\|?*]/;

caracterProblematico.test('archivo.txt'); // false (ok)
caracterProblematico.test('archivo?.txt'); // true (problemático)
caracterProblematico.test('mi:archivo.txt'); // true (problemático)
```

---

## Próximo Paso

Continúa con [02-shorthand-avanzado.md](02-shorthand-avanzado.md) para explorar más usos de las character classes.
