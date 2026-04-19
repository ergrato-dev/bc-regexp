# Semana 03: Quantifiers (Cuantificadores)

<p align="center">
  <img src="../0-assets/quantifiers.svg" alt="Quantifiers" width="100%">
</p>

## Introducción

Hasta ahora, cada elemento de nuestros patrones coincide con **exactamente un carácter**. Los **quantifiers** nos permiten especificar cuántas veces debe aparecer un elemento.

```javascript
// Semana 02: repetimos \d manualmente
/^\d\d\d\d\d$/  // 5 dígitos

// Semana 03: usamos quantifiers
/^\d{5}$/       // 5 dígitos (más elegante)
```

## Quantifiers Básicos

### `*` - Cero o Más

```javascript
/**
 * ¿Por qué? A veces un elemento puede no aparecer o aparecer muchas veces
 * ¿Para qué? Patrones opcionales que pueden repetirse
 */
const pattern = /ab*c/;
//               │││
//               ││└─ 'c' literal
//               │└── 'b' cero o más veces
//               └─── 'a' literal

pattern.test('ac'); // true  (0 b's)
pattern.test('abc'); // true  (1 b)
pattern.test('abbc'); // true  (2 b's)
pattern.test('abbbbbc'); // true  (5 b's)
pattern.test('adc'); // false (d no es b)
```

### `+` - Uno o Más

```javascript
/**
 * ¿Por qué? El elemento debe aparecer al menos una vez
 * ¿Para qué? Asegurar que algo existe, aunque se repita
 */
const pattern = /ab+c/;
//               │││
//               ││└─ 'c' literal
//               │└── 'b' uno o más veces
//               └─── 'a' literal

pattern.test('ac'); // false (necesita al menos 1 b)
pattern.test('abc'); // true  (1 b)
pattern.test('abbc'); // true  (2 b's)
pattern.test('abbbbbc'); // true  (5 b's)
```

### `?` - Cero o Uno (Opcional)

```javascript
/**
 * ¿Por qué? El elemento es opcional pero no debe repetirse
 * ¿Para qué? Hacer partes del patrón opcionales
 */
const pattern = /colou?r/;
//               │││││
//               ││││└─ 'r' literal
//               │││└── 'u' opcional (0 o 1)
//               ││└─── 'o' literal
//               │└──── 'l' literal
//               └───── 'c' literal... (continúa)

pattern.test('color'); // true  (sin u - americano)
pattern.test('colour'); // true  (con u - británico)
pattern.test('colouur'); // false (2 u's)
```

## Quantifiers con Llaves `{}`

### `{n}` - Exactamente n veces

```javascript
/**
 * ¿Por qué? Necesitamos una cantidad exacta
 * ¿Para qué? Validar longitudes fijas (códigos, IDs)
 */
const codigoPostal = /^\d{5}$/;

codigoPostal.test('28001'); // true
codigoPostal.test('2800'); // false (4 dígitos)
codigoPostal.test('280011'); // false (6 dígitos)
```

### `{n,m}` - Entre n y m veces

```javascript
/**
 * ¿Por qué? Aceptamos un rango de repeticiones
 * ¿Para qué? Longitudes variables con límites
 */
const password = /^[a-zA-Z0-9]{8,16}$/;
//                              ^^^^
//                              Mínimo 8, máximo 16 caracteres

password.test('abc1234'); // false (7 chars)
password.test('abc12345'); // true  (8 chars)
password.test('mySecurePass123'); // true  (15 chars)
password.test('thisIsWayTooLongPassword'); // false (24 chars)
```

### `{n,}` - Al menos n veces

```javascript
/**
 * ¿Por qué? Mínimo requerido, sin máximo
 * ¿Para qué? Validar longitud mínima
 */
const alMenos3 = /^\w{3,}$/;

alMenos3.test('ab'); // false (2 chars)
alMenos3.test('abc'); // true  (3 chars)
alMenos3.test('abcdef'); // true  (6 chars)
```

## Tabla de Equivalencias

```
┌────────────┬────────────────┬────────────────────────────────┐
│ Quantifier │ Equivalente    │ Significado                    │
├────────────┼────────────────┼────────────────────────────────┤
│ *          │ {0,}           │ Cero o más                     │
│ +          │ {1,}           │ Uno o más                      │
│ ?          │ {0,1}          │ Cero o uno (opcional)          │
│ {n}        │ {n,n}          │ Exactamente n                  │
│ {n,m}      │ -              │ Entre n y m (inclusivo)        │
│ {n,}       │ -              │ Al menos n                     │
│ {0,m}      │ -              │ Hasta m (máximo)               │
└────────────┴────────────────┴────────────────────────────────┘
```

## Ejemplos Prácticos

### Validar Teléfono

```javascript
/**
 * Teléfono español: 9 dígitos, empieza con 6, 7, 8 o 9
 *
 * ¿Por qué? Los móviles empiezan con 6/7, fijos con 9
 * ¿Para qué? Validar campo de teléfono en formulario
 */
const telefono = /^[6-9]\d{8}$/;
//                 │   │ └─── Exactamente 8 dígitos más
//                 │   └───── \d = dígito
//                 └───────── Primer dígito: 6, 7, 8 o 9

telefono.test('612345678'); // true
telefono.test('912345678'); // true
telefono.test('512345678'); // false (empieza con 5)
telefono.test('61234567'); // false (8 dígitos total)
```

### Validar Email (Simplificado)

```javascript
/**
 * Email básico: usuario@dominio.ext
 *
 * ¿Por qué? Los emails tienen estructura predecible
 * ¿Para qué? Primera validación antes de verificar
 */
const email = /^[\w.-]+@[\w.-]+\.\w{2,}$/;
//              │     │ │     │ │ │
//              │     │ │     │ │ └─ Extensión (2+ chars)
//              │     │ │     │ └─── Punto literal
//              │     │ │     └───── Dominio (1+ chars)
//              │     │ └─────────── @ literal
//              │     └───────────── Usuario (1+ chars)
//              └─────────────────── Inicio del string

email.test('user@example.com'); // true
email.test('user.name@mail.co.uk'); // true
email.test('user@.com'); // false
email.test('@example.com'); // false
```

### Validar URL

```javascript
/**
 * URL básica: http(s)://dominio.ext(/path)
 *
 * ¿Por qué? Las URLs tienen protocolo, dominio y path opcional
 * ¿Para qué? Validar enlaces en contenido
 */
const url = /^https?:\/\/[\w.-]+\.\w{2,}(\/\S*)?$/;
//           │    │ │    │      │ │     │     │
//           │    │ │    │      │ │     │     └─ Fin
//           │    │ │    │      │ │     └─────── Path opcional
//           │    │ │    │      │ └───────────── Ext (2+ chars)
//           │    │ │    │      └─────────────── Punto literal
//           │    │ │    └────────────────────── Dominio
//           │    │ └─────────────────────────── :// literal
//           │    └───────────────────────────── 's' opcional
//           └────────────────────────────────── http

url.test('http://example.com'); // true
url.test('https://example.com/path'); // true
url.test('ftp://example.com'); // false
```

## Quantifiers Aplicados a Grupos

Los quantifiers se aplican al elemento **inmediatamente anterior**:

```javascript
// Cuantifica solo la 'a'
/ba+/     // "ba", "baa", "baaa"...

// Cuantifica el grupo completo
/(ba)+/   // "ba", "baba", "bababa"...

// Ejemplo práctico
const risas = /^(ja)+$/i;
risas.test("ja");       // true
risas.test("jaja");     // true
risas.test("jajaja");   // true
risas.test("jaj");      // false
```

## Consideraciones de Rendimiento

```javascript
/**
 * ⚠️ Cuidado con patrones ambiguos
 *
 * ¿Por qué? Los quantifiers pueden causar backtracking excesivo
 * ¿Para qué? Evitar regex que tardan mucho en ejecutar
 */

// ❌ Potencialmente lento con strings largos
const malo = /(.+)+$/;

// ✅ Más específico, más rápido
const bueno = /\w+$/;
```

---

## Próximo Paso

Continúa con [02-greedy-vs-lazy.md](02-greedy-vs-lazy.md) para entender el comportamiento greedy y lazy de los quantifiers.
