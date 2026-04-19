# Grupos de Captura

## ¿Qué son los Grupos?

Los **grupos** en regex permiten:

1. **Agrupar elementos** para aplicar quantifiers
2. **Capturar partes** del match para uso posterior
3. **Crear alternativas** dentro del patrón

Los grupos se crean con paréntesis: `( )`

## Grupos de Captura: `( )`

### Concepto Básico

Un **capture group** captura y guarda el texto que coincide, permitiendo acceder a él después.

```javascript
/**
 * Patrón: Capturar nombre y extensión de archivo
 *
 * ¿Por qué? Los archivos tienen nombre y extensión separados
 * ¿Para qué? Extraer ambas partes independientemente
 *
 * Desglose:
 * (\w+)   → Grupo 1: nombre del archivo
 * \.      → Punto literal
 * (\w+)   → Grupo 2: extensión
 */
const archivoPattern = /(\w+)\.(\w+)/;

const match = 'documento.pdf'.match(archivoPattern);
console.log(match);
// [
//   'documento.pdf',  // match[0]: Match completo
//   'documento',      // match[1]: Grupo 1 (nombre)
//   'pdf'             // match[2]: Grupo 2 (extensión)
// ]
```

### Accediendo a Grupos

```javascript
const texto = 'Juan tiene 25 años';

/**
 * Patrón: Nombre y edad
 *
 * ¿Por qué? La información está en formato conocido
 * ¿Para qué? Extraer datos estructurados del texto
 */
const pattern = /(\w+) tiene (\d+) años/;
const match = texto.match(pattern);

console.log(match[0]); // "Juan tiene 25 años" (match completo)
console.log(match[1]); // "Juan" (grupo 1)
console.log(match[2]); // "25" (grupo 2)
```

### Grupos con `exec()`

El método `exec()` devuelve más información que `match()`:

```javascript
const pattern = /(\w+)@(\w+)\.(\w+)/;
const texto = 'Contacto: ana@empresa.com';

const result = pattern.exec(texto);

console.log(result.index); // 10 (posición del match)
console.log(result.input); // "Contacto: ana@empresa.com"
console.log(result[0]); // "ana@empresa.com"
console.log(result[1]); // "ana"
console.log(result[2]); // "empresa"
console.log(result[3]); // "com"
```

### Grupos con Flag `g` (matchAll)

Con `match()` y flag `g`, los grupos **se pierden**. Usa `matchAll()`:

```javascript
const texto = 'a@b.com, c@d.org, e@f.net';
const pattern = /(\w+)@(\w+)\.(\w+)/g;

// ❌ match con flag g pierde los grupos
console.log(texto.match(pattern));
// ['a@b.com', 'c@d.org', 'e@f.net'] - sin grupos

// ✅ matchAll mantiene los grupos
for (const match of texto.matchAll(pattern)) {
  console.log(`Usuario: ${match[1]}, Dominio: ${match[2]}.${match[3]}`);
}
// Usuario: a, Dominio: b.com
// Usuario: c, Dominio: d.org
// Usuario: e, Dominio: f.net
```

## Grupos para Agrupar

Además de capturar, los grupos sirven para **agrupar elementos**:

### Quantifiers en Grupos

```javascript
/**
 * Patrón: Repetir un grupo completo
 *
 * ¿Por qué? Queremos repetir una secuencia, no un solo carácter
 * ¿Para qué? Validar patrones repetitivos
 */

// Sin grupo: solo 'a' se repite
/abc+/     // abcc, abccc, abcccc...

// Con grupo: 'abc' completo se repite
/(abc)+/   // abc, abcabc, abcabcabc...

// Ejemplo práctico: direcciones IP
/**
 * ¿Por qué? Cada octeto es un grupo de dígitos seguido de punto
 * ¿Para qué? Validar estructura de IP
 */
/(\d{1,3}\.){3}\d{1,3}/
// Repite "dígitos + punto" 3 veces, luego dígitos finales
```

### Alternativas con `|`

El operador `|` (OR) funciona a nivel de grupo:

```javascript
/**
 * ¿Por qué? Las URLs pueden tener http o https
 * ¿Para qué? Aceptar ambos protocolos
 */

// Sin grupo: | aplica a todo
/http|https/   // "http" O "https"

// Con grupo: controla el alcance del |
/(http|https):\/\//   // "http://" O "https://"

// Más conciso con ?
/https?:\/\//         // Mismo resultado
```

### Grupos Anidados

Los grupos pueden **anidarse**:

```javascript
/**
 * Patrón: Fecha con hora opcional
 *
 * ¿Por qué? A veces la fecha viene sola, a veces con hora
 * ¿Para qué? Capturar todas las partes
 *
 * Desglose:
 * (\d{2}/\d{2}/\d{4})  → Grupo 1: fecha completa
 * ((\d{2}):(\d{2}))?   → Grupo 2: hora completa (opcional)
 *    (\d{2})           → Grupo 3: horas
 *    (\d{2})           → Grupo 4: minutos
 */
const pattern = /(\d{2}\/\d{2}\/\d{4})( (\d{2}):(\d{2}))?/;

'15/01/2024 14:30'.match(pattern);
// [0]: '15/01/2024 14:30' (match completo)
// [1]: '15/01/2024'       (fecha)
// [2]: ' 14:30'           (hora con espacio)
// [3]: '14'               (horas)
// [4]: '30'               (minutos)
```

## Grupos No Capturadores: `(?:)`

A veces necesitas **agrupar sin capturar**. Usa `(?:)`:

```javascript
/**
 * ¿Por qué? Solo nos interesa capturar el dominio, no el protocolo
 * ¿Para qué? Simplificar los grupos resultantes
 */

// Con grupo normal: captura el protocolo (no lo necesitamos)
const pattern1 = /(https?):\/\/(\w+\.\w+)/;
'https://google.com'.match(pattern1);
// [0]: 'https://google.com'
// [1]: 'https'       ← No nos interesa
// [2]: 'google.com'

// Con non-capturing group: no captura el protocolo
const pattern2 = /(?:https?):\/\/(\w+\.\w+)/;
'https://google.com'.match(pattern2);
// [0]: 'https://google.com'
// [1]: 'google.com'  ← Solo lo que nos interesa
```

### Cuándo Usar Non-Capturing Groups

```javascript
// ✅ Agrupar para quantifier sin capturar
/(?:abc)+/    // Repite abc, no captura

// ✅ Agrupar alternativas sin capturar
/(?:http|https|ftp):\/\//

// ✅ Cuando solo necesitas algunos grupos
const phonePattern = /(?:\+34)?(\d{9})/;
// Solo captura el número, no el prefijo opcional
```

## Named Capture Groups: `(?<nombre>)`

JavaScript soporta **grupos con nombre** para mayor legibilidad:

```javascript
/**
 * Patrón: Email con grupos nombrados
 *
 * ¿Por qué? Los índices numéricos son difíciles de recordar
 * ¿Para qué? Código más legible y mantenible
 */
const emailPattern = /(?<usuario>\w+)@(?<dominio>\w+)\.(?<extension>\w+)/;

const match = 'ana@empresa.com'.match(emailPattern);

// Acceso por índice (funciona igual)
console.log(match[1]); // "ana"

// Acceso por nombre (más legible)
console.log(match.groups.usuario); // "ana"
console.log(match.groups.dominio); // "empresa"
console.log(match.groups.extension); // "com"
```

### Destructuring con Named Groups

```javascript
const fechaPattern = /(?<dia>\d{2})\/(?<mes>\d{2})\/(?<anio>\d{4})/;

const match = '15/01/2024'.match(fechaPattern);
const { dia, mes, anio } = match.groups;

console.log(`Día: ${dia}, Mes: ${mes}, Año: ${anio}`);
// Día: 15, Mes: 01, Año: 2024
```

## Comparación de Tipos de Grupos

| Tipo          | Sintaxis         | Captura         | Uso Principal            |
| ------------- | ---------------- | --------------- | ------------------------ |
| Capture Group | `(...)`          | Sí              | Extraer partes del match |
| Non-Capturing | `(?:...)`        | No              | Agrupar sin capturar     |
| Named Group   | `(?<nombre>...)` | Sí (con nombre) | Código legible           |

## Ejercicio Práctico

```javascript
/**
 * Ejercicio: Parser de URL
 *
 * URL: https://www.ejemplo.com:8080/ruta/pagina?query=valor
 *
 * Grupos a extraer:
 * - protocolo: https
 * - dominio: www.ejemplo.com
 * - puerto: 8080 (opcional)
 * - path: /ruta/pagina (opcional)
 * - query: query=valor (opcional)
 */
const urlPattern =
  /(?<protocolo>https?):\/\/(?<dominio>[\w.-]+)(?::(?<puerto>\d+))?(?<path>\/[^?]*)?(?:\?(?<query>.*))?/;

const url = 'https://www.ejemplo.com:8080/ruta/pagina?query=valor';
const { groups } = url.match(urlPattern);

console.log(groups);
// {
//   protocolo: 'https',
//   dominio: 'www.ejemplo.com',
//   puerto: '8080',
//   path: '/ruta/pagina',
//   query: 'query=valor'
// }
```

---

**Siguiente:** [Backreferences](02-backreferences.md)
