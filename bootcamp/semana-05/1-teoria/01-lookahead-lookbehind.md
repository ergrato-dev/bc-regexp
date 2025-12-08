# Lookahead y Lookbehind

## ¿Qué son los Lookarounds?

Los **lookarounds** son aserciones de ancho cero que comprueban si un patrón existe antes o después de la posición actual, **sin consumir caracteres** del texto.

A diferencia de los grupos normales, los lookarounds:

- ✅ Verifican que existe un patrón
- ❌ No incluyen ese patrón en el match
- ❌ No avanzan el cursor de matching

## Tipos de Lookarounds

| Tipo                | Sintaxis   | Descripción                    |
| ------------------- | ---------- | ------------------------------ |
| Positive Lookahead  | `(?=...)`  | Lo que sigue debe coincidir    |
| Negative Lookahead  | `(?!...)`  | Lo que sigue NO debe coincidir |
| Positive Lookbehind | `(?<=...)` | Lo anterior debe coincidir     |
| Negative Lookbehind | `(?<!...)` | Lo anterior NO debe coincidir  |

## Lookahead: `(?=...)` y `(?!...)`

### Positive Lookahead: `(?=...)`

**"Mira adelante y verifica que exista esto"**

```javascript
/**
 * Patrón: Encontrar "Java" solo si le sigue "Script"
 *
 * ¿Por qué? Queremos "JavaScript" pero solo la parte "Java"
 * ¿Para qué? Extraer prefijos condicionalmente
 *
 * Desglose:
 * Java     → Texto literal a capturar
 * (?=Script) → Lookahead: debe seguir "Script" (no se captura)
 */
const pattern = /Java(?=Script)/g;

const texto = 'JavaScript, Java, JavaBeans, JavaFX';
console.log(texto.match(pattern));
// ['Java'] - Solo el "Java" de "JavaScript"

// El match es solo "Java", no "JavaScript"
console.log('JavaScript'.match(pattern)[0]); // "Java"
```

### Ejemplo Práctico: Precios

```javascript
/**
 * Encontrar números seguidos de €
 *
 * ¿Por qué? Queremos el número pero no el símbolo
 * ¿Para qué? Extraer valores para cálculos
 */
const precioPattern = /\d+(?=€)/g;

const texto = 'Precio: 99€, IVA: 21%, Total: 120€';
console.log(texto.match(precioPattern));
// ['99', '120'] - Solo los números, sin el €
```

### Negative Lookahead: `(?!...)`

**"Mira adelante y verifica que NO exista esto"**

```javascript
/**
 * Patrón: Encontrar "Java" que NO le siga "Script"
 *
 * ¿Por qué? Queremos excluir JavaScript
 * ¿Para qué? Filtrar matches no deseados
 */
const pattern = /Java(?!Script)/g;

const texto = 'JavaScript, Java, JavaBeans, JavaFX';
console.log(texto.match(pattern));
// ['Java', 'Java', 'Java'] - De "Java", "JavaBeans", "JavaFX"
```

### Ejemplo Práctico: Validación

```javascript
/**
 * Palabra que NO termine en "ing"
 *
 * ¿Por qué? Excluir gerundios
 * ¿Para qué? Filtrar verbos en forma base
 */
const pattern = /\b\w+(?!ing)\b/g;

// Más preciso: palabra que no termine en "ing"
const pattern2 = /\b\w+\b(?!ing)/g;

// Aún mejor:
const pattern3 = /\b(?!\w*ing\b)\w+\b/g;

const texto = 'running walking jump talk singing dance';
console.log(texto.match(pattern3));
// ['jump', 'talk', 'dance']
```

## Lookbehind: `(?<=...)` y `(?<!...)`

> **Nota:** Lookbehind fue añadido en ES2018. No funciona en navegadores muy antiguos.

### Positive Lookbehind: `(?<=...)`

**"Mira atrás y verifica que exista esto"**

```javascript
/**
 * Patrón: Encontrar números precedidos de $
 *
 * ¿Por qué? Solo queremos precios en dólares
 * ¿Para qué? Filtrar valores por contexto
 */
const pattern = /(?<=\$)\d+/g;

const texto = 'Precio: $99, €85, $120';
console.log(texto.match(pattern));
// ['99', '120'] - Solo los números después de $
```

### Ejemplo Práctico: Extraer Valor de Atributo

```javascript
/**
 * Extraer el valor de un atributo class="..."
 *
 * ¿Por qué? Solo queremos el valor, no 'class='
 * ¿Para qué? Parsing de HTML
 */
const pattern = /(?<=class=["'])[^"']+(?=["'])/g;

const html = '<div class="container"> <span class="text"> </span></div>';
console.log(html.match(pattern));
// ['container', 'text']
```

### Negative Lookbehind: `(?<!...)`

**"Mira atrás y verifica que NO exista esto"**

```javascript
/**
 * Patrón: Números que NO estén precedidos de $
 *
 * ¿Por qué? Excluir precios
 * ¿Para qué? Encontrar otros números
 */
const pattern = /(?<!\$)\b\d+\b/g;

const texto = 'Cantidad: 5, Precio: $99, Items: 3';
console.log(texto.match(pattern));
// ['5', '3'] - Excluye el 99
```

### Ejemplo Práctico: Palabras No Después de Artículo

```javascript
/**
 * Sustantivos que no estén después de "the"
 *
 * ¿Por qué? Filtrar por contexto gramatical
 * ¿Para qué? Análisis de texto
 */
const pattern = /(?<!the\s)\b[A-Z][a-z]+\b/g;

const texto = 'The Cat sat. A Dog ran. Max jumped.';
console.log(texto.match(pattern));
// ['Dog', 'Max'] - "Cat" excluido por estar después de "The"
```

## Combinando Lookarounds

Los lookarounds se pueden combinar para validaciones complejas:

### Password Validation

```javascript
/**
 * Password que cumpla:
 * - Al menos 8 caracteres
 * - Al menos una mayúscula
 * - Al menos una minúscula
 * - Al menos un dígito
 *
 * ¿Por qué? Múltiples requisitos simultáneos
 * ¿Para qué? Validación de seguridad
 */
const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/;

console.log(passwordPattern.test('Abc12345')); // true
console.log(passwordPattern.test('abcdefgh')); // false (sin mayúscula)
console.log(passwordPattern.test('ABC12345')); // false (sin minúscula)
console.log(passwordPattern.test('Abcdefgh')); // false (sin dígito)
console.log(passwordPattern.test('Abc123')); // false (menos de 8)
```

### Explicación del Patrón

```javascript
/^               // Inicio
  (?=.*[A-Z])    // Lookahead: debe haber una mayúscula en algún lugar
  (?=.*[a-z])    // Lookahead: debe haber una minúscula en algún lugar
  (?=.*\d)       // Lookahead: debe haber un dígito en algún lugar
  .{8,}          // El match real: 8+ caracteres cualesquiera
$/               // Fin
```

### Password con Más Requisitos

```javascript
/**
 * Password más estricta:
 * - 8-20 caracteres
 * - Al menos una mayúscula
 * - Al menos una minúscula
 * - Al menos un dígito
 * - Al menos un carácter especial
 * - Sin espacios
 */
const strongPassword =
  /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])(?!.*\s).{8,20}$/;

console.log(strongPassword.test('Abc123!@')); // true
console.log(strongPassword.test('Abc 123!@')); // false (tiene espacio)
```

## Lookarounds vs Grupos

| Característica    | Grupo `()` | Lookaround                    |
| ----------------- | ---------- | ----------------------------- |
| Consume texto     | ✅ Sí      | ❌ No                         |
| Incluido en match | ✅ Sí      | ❌ No                         |
| Captura para `\1` | ✅ Sí      | ❌ No                         |
| Afecta posición   | ✅ Sí      | ❌ No                         |
| Puede negar       | ❌ No      | ✅ Sí (`(?!...)`, `(?<!...)`) |

### Ejemplo Comparativo

```javascript
const texto = '100€';

// Con grupo: incluye € en el match
/(\d+)(€)/.exec(texto);
// ['100€', '100', '€']

// Con lookahead: NO incluye € en el match
/(\d+)(?=€)/.exec(texto);
// ['100', '100']
```

## Aplicaciones Prácticas

### 1. Separador de Miles

```javascript
/**
 * Añadir comas como separador de miles
 *
 * ¿Por qué? Los números grandes son difíciles de leer
 * ¿Para qué? Formateo visual
 */
const formatearNumero = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

console.log(formatearNumero(1234567)); // "1,234,567"
console.log(formatearNumero(1000000000)); // "1,000,000,000"
```

### 2. Resaltar Palabras Clave

```javascript
/**
 * Envolver palabras clave en tags, pero solo si son palabras completas
 *
 * ¿Por qué? Evitar matches parciales
 * ¿Para qué? Syntax highlighting
 */
const keywords = ['function', 'const', 'let', 'return'];
const pattern = new RegExp(`(?<![\\w])(?:${keywords.join('|')})(?![\\w])`, 'g');

const code = 'const funcConstant = function() { return functional; }';
const highlighted = code.replace(pattern, '<keyword>$&</keyword>');
console.log(highlighted);
// "<keyword>const</keyword> funcConstant = <keyword>function</keyword>() { <keyword>return</keyword> functional; }"
```

### 3. Validar Formato Sin Capturar

```javascript
/**
 * Verificar que una URL es HTTPS sin capturar el protocolo
 *
 * ¿Por qué? Solo queremos validar, no extraer el protocolo
 * ¿Para qué? Validación de seguridad
 */
const httpsOnly = /(?<=^https:\/\/)\S+/;

console.log(httpsOnly.test('https://secure.com')); // true
console.log(httpsOnly.test('http://insecure.com')); // false
```

---

**Siguiente:** [Ejercicios de Lookarounds](../2-ejercicios/ejercicio-05-lookarounds.md)
