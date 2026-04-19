# Semana 07: Patrones Avanzados y Optimización

## 🎯 Objetivos

- Dominar técnicas avanzadas de regex
- Optimizar patrones para rendimiento
- Evitar catastrophic backtracking
- Aplicar patrones en casos reales complejos

---

## 1. Named Capture Groups

Los **named capture groups** permiten asignar nombres a los grupos para código más legible.

### Sintaxis

```javascript
/**
 * ¿Por qué? Los números de grupo ($1, $2) son difíciles de recordar
 * ¿Para qué? Código más legible y mantenible
 */

// Sintaxis: (?<nombre>patrón)
const pattern = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;

const match = '2024-03-15'.match(pattern);
console.log(match.groups);
// { year: '2024', month: '03', day: '15' }

// Acceso individual
console.log(match.groups.year); // '2024'
console.log(match.groups.month); // '03'
console.log(match.groups.day); // '15'
```

### Backreference con Nombres

```javascript
/**
 * ¿Por qué? Referenciar grupos por nombre es más claro
 * ¿Para qué? Verificar valores duplicados
 */

// Sintaxis: \k<nombre>
const duplicados = /(?<palabra>\w+)\s+\k<palabra>/;

duplicados.test('hello hello'); // true
duplicados.test('hello world'); // false
```

### Replace con Named Groups

```javascript
/**
 * ¿Por qué? Reorganizar datos con nombres es más intuitivo
 * ¿Para qué? Transformar formatos
 */

const fecha = '2024-03-15';
const pattern = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;

// Usando $<nombre>
fecha.replace(pattern, '$<day>/$<month>/$<year>');
// "15/03/2024"

// Usando función
fecha.replace(pattern, (match, p1, p2, p3, offset, string, groups) => {
  return `${groups.day}/${groups.month}/${groups.year}`;
});
```

---

## 2. Atomic Groups (Simulación)

JavaScript no soporta atomic groups nativamente, pero podemos simularlos.

### ¿Qué es un Atomic Group?

```javascript
/**
 * ¿Por qué? Prevenir backtracking innecesario
 * ¿Para qué? Mejorar rendimiento en patrones complejos
 *
 * Un atomic group no permite que el motor "retroceda"
 * una vez que ha hecho match.
 */

// En otros lenguajes: (?>patrón)
// En JavaScript: No existe nativamente

// Simulación con lookahead + backreference
// (?=(patrón))\1

const atomicSimulado = /(?=(\d+))\1X/;
//                      │   │    │
//                      │   │    └─ Referencia al grupo capturado
//                      │   └────── Captura los dígitos
//                      └────────── Lookahead "bloquea" el match
```

### Ejemplo Práctico

```javascript
/**
 * Sin atomic group: backtracking excesivo
 */

// Problema: muchos dígitos seguidos de X
const texto = '123456789X';

// Este patrón puede causar backtracking
const malo = /\d+X/;

// Versión "atomic" simulada
const bueno = /(?=(\d+))\1X/;

// Ambos funcionan, pero el segundo no retrocede
```

---

## 3. Possessive Quantifiers (Simulación)

Similar a atomic groups, previenen backtracking.

```javascript
/**
 * En otros lenguajes:
 * *+ (possessive star)
 * ++ (possessive plus)
 * ?+ (possessive optional)
 *
 * En JavaScript: No existe nativamente
 * Simulación: Igual que atomic groups
 */

// Ejemplo: matching de string con comillas
const texto = '"Hola mundo" y "otro texto"';

// Possessive simulado para contenido de string
const stringPattern = /"(?=([^"]*))(?:\1)"/g;

texto.match(stringPattern);
// ['"Hola mundo"', '"otro texto"']
```

---

## 4. Catastrophic Backtracking

### El Problema

```javascript
/**
 * ¿Por qué? Ciertos patrones causan tiempo exponencial
 * ¿Para qué? Evitar que regex "cuelgue" el navegador
 */

// ⚠️ PELIGRO: Este patrón es exponencialmente lento
const peligroso = /(a+)+$/;

// Con un string largo de 'a' seguido de 'X':
// "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaX"
// El motor prueba millones de combinaciones
```

### Patrones Problemáticos

```javascript
// ❌ Patrones que causan catastrophic backtracking

// 1. Cuantificadores anidados
/(a+)+/       // a+ dentro de ()+
/(a*)*$/      // a* dentro de ()*
/(\w+\s*)+/   // palabras opcionales

// 2. Alternativas que se solapan
/(a|aa)+/     // 'a' o 'aa' repetido
/(.+)+/       // cualquier cosa repetida

// 3. Opcional + repetición
/(x+x+)+y/    // múltiples x's antes de y
```

### Soluciones

```javascript
/**
 * Técnicas para evitar catastrophic backtracking
 */

// 1. Usar cuantificadores posesivos (simulados)
// Malo:  /(a+)+$/
// Bueno: /(?=(a+))\1$/

// 2. Hacer alternativas mutuamente exclusivas
// Malo:  /(a|ab)*/
// Bueno: /a(b|(?!b))*/

// 3. Usar negación en lugar de repetición abierta
// Malo:  /".*"/
// Bueno: /"[^"]*"/

// 4. Agregar anclas cuando sea posible
// Malo:  /pattern/
// Bueno: /^pattern$/

// 5. Limitar repeticiones
// Malo:  /\w+/
// Bueno: /\w{1,100}/
```

### Ejemplo Real: Validación de Email

```javascript
// ❌ Email regex peligroso (simplificado)
const emailMalo = /^(\w+\.)*\w+@(\w+\.)*\w+$/;

// Con input malicioso:
// "aaaaaaaaaaaaaaaaaaaaaaaaa@" puede colgar

// ✅ Email regex seguro
const emailSeguro = /^[\w.-]{1,64}@[\w.-]{1,255}$/;
// Limita longitud para prevenir ataques
```

---

## 5. Optimización de Patrones

### Principios de Rendimiento

```javascript
/**
 * 1. Fallar rápido
 * ¿Por qué? Detectar no-matches temprano
 * ¿Para qué? Reducir trabajo del motor
 */

// Malo: verifica todo el email antes de fallar
/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

// Mejor: ancla y caracter común primero
/^[a-z][a-z0-9._%+-]*@/i  // Falla rápido si no empieza con letra

/**
 * 2. Evitar alternativas innecesarias
 */

// Malo: muchas alternativas
/(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)/

// Mejor: clase de caracteres cuando sea posible
/(Mon|Tue|Wed|Thu|Fri|Sat|Sun)day/

/**
 * 3. Usar non-capturing groups
 */

// Si no necesitas capturar:
/(?:abc)+/  // ✅ Non-capturing
/(abc)+/    // ❌ Capturing innecesario

/**
 * 4. Ordenar alternativas por frecuencia
 */

// Si 'the' es más común, ponerlo primero
/the|a|an/  // ✅
/an|a|the/  // ❌
```

### Benchmarking

```javascript
/**
 * Medir rendimiento de regex
 */
function benchmarkRegex(pattern, texto, iteraciones = 10000) {
  const start = performance.now();

  for (let i = 0; i < iteraciones; i++) {
    pattern.test(texto);
  }

  const end = performance.now();
  return (end - start).toFixed(2) + 'ms';
}

const texto = 'usuario@ejemplo.com';

console.log(benchmarkRegex(/^[\w.-]+@[\w.-]+\.\w+$/, texto));
console.log(benchmarkRegex(/^\w+@\w+\.\w+$/, texto));
```

---

## 6. Patrones de Validación Robustos

### Email (RFC 5322 Simplificado)

```javascript
/**
 * ¿Por qué? El RFC completo es extremadamente complejo
 * ¿Para qué? Balance entre precisión y rendimiento
 */
const emailPattern =
  /^(?=[a-z0-9])[a-z0-9.!#$%&'*+/=?^_`{|}~-]{0,63}[a-z0-9]@(?=[a-z0-9])(?:[a-z0-9-]{0,61}[a-z0-9]\.)+[a-z]{2,}$/i;
//                    │           │                                        │  │           │                        │
//                    │           │                                        │  │           │                        └─ TLD (2+ letras)
//                    │           │                                        │  │           └─ Subdominio: letras/dígitos/guión
//                    │           │                                        │  └─ Lookahead: debe empezar con alfanum
//                    │           │                                        └─ Debe terminar con alfanum antes de @
//                    │           └─ Caracteres válidos en local-part
//                    └─ Lookahead: debe empezar con alfanum
```

### URL

```javascript
/**
 * URL pattern con validación de componentes
 */
const urlPattern =
  /^(?<protocol>https?):\/\/(?<host>(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,})(?::(?<port>\d{1,5}))?(?<path>\/[^\s?#]*)?(?:\?(?<query>[^\s#]*))?(?:#(?<hash>\S*))?$/i;

const url = 'https://example.com:8080/path/to/page?query=value#section';
const match = url.match(urlPattern);

console.log(match.groups);
// {
//   protocol: 'https',
//   host: 'example.com',
//   port: '8080',
//   path: '/path/to/page',
//   query: 'query=value',
//   hash: 'section'
// }
```

### Número de Tarjeta de Crédito

```javascript
/**
 * Validación básica de formato (no Luhn checksum)
 */
const tarjetaPattern =
  /^(?<tipo>4\d{3}|5[1-5]\d{2}|3[47]\d{2}|6(?:011|5\d{2}))[- ]?(?<grupo1>\d{4})[- ]?(?<grupo2>\d{4})[- ]?(?<grupo3>\d{4}|\d{3})$/;
//                      │                                                     │        │              │              │
//                      └─ Detecta tipo de tarjeta:                           │        │              │              └─ 4 o 3 dígitos (Amex)
//                         4xxx = Visa                                        │        │              └─ 4 dígitos
//                         51-55xx = Mastercard                               │        └─ 4 dígitos
//                         34/37xx = American Express                         └─ Separador opcional
//                         6011/65xx = Discover

const tarjeta = '4532-1234-5678-9012';
const match = tarjeta.match(tarjetaPattern);

console.log(match.groups.tipo); // '4532' -> Visa
```

---

## 7. Recursión y Balanced Matching

JavaScript no soporta recursión en regex, pero podemos simular casos simples.

### Paréntesis Balanceados (Nivel Fijo)

```javascript
/**
 * ¿Por qué? Regex no puede contar niveles arbitrarios
 * ¿Para qué? Validar expresiones hasta cierto nivel
 */

// Hasta 1 nivel de anidación
const nivel1 = /\([^()]*\)/g;

// Hasta 2 niveles
const nivel2 = /\((?:[^()]|\([^()]*\))*\)/g;

// Hasta 3 niveles
const nivel3 = /\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)/g;

const texto = 'a(b(c(d)e)f)g';

texto.match(nivel1); // ['(d)']
texto.match(nivel2); // ['(c(d)e)']
texto.match(nivel3); // ['(b(c(d)e)f)']
```

### Solución con Código

```javascript
/**
 * Para anidación arbitraria, usar código JavaScript
 */
function matchBalanced(str, open = '(', close = ')') {
  const results = [];
  let depth = 0;
  let start = -1;

  for (let i = 0; i < str.length; i++) {
    if (str[i] === open) {
      if (depth === 0) start = i;
      depth++;
    } else if (str[i] === close) {
      depth--;
      if (depth === 0 && start !== -1) {
        results.push(str.slice(start, i + 1));
        start = -1;
      }
    }
  }

  return results;
}

matchBalanced('a(b(c)d)e(f)g');
// ['(b(c)d)', '(f)']
```

---

## 8. Conditional Patterns (Simulación)

```javascript
/**
 * En otros lenguajes: (?(condition)then|else)
 * En JavaScript: Simular con lookaheads
 */

// Ejemplo: Número con o sin paréntesis
// Si empieza con (, debe terminar con )

// Simulación:
const condicional = /(?:(\()\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}/;
//                   │   │        │      │
//                   │   │        │      └─ Formato sin paréntesis
//                   │   │        └──────── Alternativa: con paréntesis
//                   │   └───────────────── Captura el paréntesis abierto
//                   └───────────────────── Non-capturing wrapper

'(555) 123-4567'.match(condicional); // Match
'555-123-4567'.match(condicional); // Match
'(555 123-4567'.match(condicional); // No match (paréntesis no balanceado)
```

---

## 9. Patrones para Parsing

### Tokenizer Simple

```javascript
/**
 * ¿Por qué? Muchos lenguajes se pueden tokenizar con regex
 * ¿Para qué? Primer paso en compilación/interpretación
 */
const tokens = [
  { type: 'NUMBER', pattern: /\d+(?:\.\d+)?/ },
  { type: 'STRING', pattern: /"[^"]*"|'[^']*'/ },
  { type: 'KEYWORD', pattern: /\b(?:if|else|while|for|function|return)\b/ },
  { type: 'IDENT', pattern: /[a-zA-Z_]\w*/ },
  { type: 'OPERATOR', pattern: /[+\-*/=<>!&|]+/ },
  { type: 'PAREN', pattern: /[()]/ },
  { type: 'BRACE', pattern: /[{}]/ },
  { type: 'SEMICOLON', pattern: /;/ },
  { type: 'WHITESPACE', pattern: /\s+/ },
];

function tokenize(code) {
  const result = [];
  let remaining = code;

  while (remaining.length > 0) {
    let matched = false;

    for (const { type, pattern } of tokens) {
      const match = remaining.match(new RegExp(`^${pattern.source}`));
      if (match) {
        if (type !== 'WHITESPACE') {
          result.push({ type, value: match[0] });
        }
        remaining = remaining.slice(match[0].length);
        matched = true;
        break;
      }
    }

    if (!matched) {
      throw new Error(`Unexpected character: ${remaining[0]}`);
    }
  }

  return result;
}

tokenize('if (x > 5) { return x * 2; }');
// [
//   { type: 'KEYWORD', value: 'if' },
//   { type: 'PAREN', value: '(' },
//   { type: 'IDENT', value: 'x' },
//   { type: 'OPERATOR', value: '>' },
//   { type: 'NUMBER', value: '5' },
//   ...
// ]
```

### Extractor de Comentarios

```javascript
/**
 * Extraer todos los comentarios de código
 */
const comentarioPattern = /\/\/[^\n]*|\/\*[\s\S]*?\*\//g;
//                         │           │
//                         │           └─ Comentario multilínea /* ... */
//                         └─────────── Comentario de línea // ...

const codigo = `
function hello() {
  // Saludo simple
  console.log("Hello"); /* inline */
  /*
   * Comentario
   * multilínea
   */
}
`;

codigo.match(comentarioPattern);
// ['// Saludo simple', '/* inline */', '/*\n   * Comentario\n   * multilínea\n   */']
```

---

## 10. Resumen

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PATRONES AVANZADOS                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Named Groups          (?<nombre>patrón)    Grupos con nombre       │
│  Backreference         \k<nombre>           Referenciar por nombre  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  OPTIMIZACIÓN                                                       │
│  ──────────────────────────────────────────────────────────────     │
│  • Evitar cuantificadores anidados: (a+)+                          │
│  • Usar [^x] en lugar de .*                                         │
│  • Agregar anclas ^ $                                              │
│  • Limitar repeticiones {1,n}                                      │
│  • Non-capturing cuando no se necesita captura                     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PATRONES PELIGROSOS                                                │
│  ──────────────────────────────────────────────────────────────     │
│  /(a+)+$/        Catastrophic backtracking                         │
│  /(.+)+/         Tiempo exponencial                                 │
│  /(a|aa)+/       Alternativas solapadas                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

**Siguiente:** [Ejercicios Semana 07](../2-ejercicios/ejercicio-07-avanzados.md)
