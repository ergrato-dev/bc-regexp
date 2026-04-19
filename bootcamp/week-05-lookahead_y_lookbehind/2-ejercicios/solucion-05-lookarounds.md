# Soluciones - Semana 05: Lookahead y Lookbehind

## Ejercicio 1: Precios en Diferentes Monedas

```javascript
/**
 * Patrón: Extraer números después de $
 *
 * ¿Por qué? Solo queremos precios en dólares
 * ¿Para qué? Calcular totales en una moneda
 *
 * Desglose:
 * (?<=\$)    → Lookbehind: debe haber $ antes
 * \d+        → Uno o más dígitos (parte entera)
 * \.         → Punto decimal
 * \d{2}      → Exactamente 2 dígitos (centavos)
 */
const precioPattern = /(?<=\$)\d+\.\d{2}/g;

const texto = `Producto A: $99.99
Producto B: €85.00
Producto C: $149.99
Producto D: £120.00
Producto E: $25.50`;

console.log(texto.match(precioPattern));
// ['99.99', '149.99', '25.50']

// Convertir a números y sumar
const total = texto
  .match(precioPattern)
  .map(parseFloat)
  .reduce((a, b) => a + b, 0);
console.log(`Total: $${total.toFixed(2)}`);
// Total: $274.98
```

---

## Ejercicio 2: Palabras Sin Prefijo "un"

```javascript
/**
 * Patrón: Palabras que NO empiecen con "un"
 *
 * ¿Por qué? Filtrar palabras negativas/prefijadas
 * ¿Para qué? Análisis de texto, filtrado
 *
 * Desglose:
 * \b         → Word boundary (inicio de palabra)
 * (?!un)     → Negative lookahead: no debe seguir "un"
 * \w+        → Uno o más caracteres de palabra
 * \b         → Word boundary (fin de palabra)
 */
const pattern = /\b(?!un)\w+\b/gi;

const texto = `The task was undone but the work was complete.
He was unhappy but she was happy.
The box was unopened while another was opened.`;

const palabras = texto.match(pattern);
console.log(palabras);
// ['The', 'task', 'was', 'but', 'the', 'work', 'was', 'complete',
//  'He', 'was', 'but', 'she', 'was', 'happy',
//  'The', 'box', 'was', 'while', 'another', 'was', 'opened']

// Verificar que las palabras "un..." fueron excluidas
const excluidas = texto.match(/\bun\w+\b/gi);
console.log('Excluidas:', excluidas);
// ['undone', 'unhappy', 'unopened']
```

---

## Ejercicio 3: Números Seguidos de Unidades

```javascript
/**
 * Patrón: Números seguidos de unidades específicas
 *
 * ¿Por qué? Solo queremos medidas, no otros números
 * ¿Para qué? Extraer datos para conversión/cálculo
 *
 * Desglose:
 * \d+             → Uno o más dígitos
 * (?=             → Positive lookahead
 *   (?:km|kg|cm|m) → Unidades válidas (non-capturing)
 *   \b            → Seguido de word boundary (evita "mm" en "km")
 * )
 */
const pattern = /\d+(?=(?:km|kg|cm|m)\b)/g;

const texto = `Velocidad: 120km/h
Peso: 75kg
Altura: 180cm
Temperatura: 25
Distancia: 500m
Precio: 99`;

console.log(texto.match(pattern));
// ['120', '75', '180', '500']

// Para obtener también las unidades (separadas)
const conUnidades = /(\d+)(km|kg|cm|m)\b/g;
for (const match of texto.matchAll(conUnidades)) {
  console.log(`Valor: ${match[1]}, Unidad: ${match[2]}`);
}
// Valor: 120, Unidad: km
// Valor: 75, Unidad: kg
// Valor: 180, Unidad: cm
// Valor: 500, Unidad: m
```

---

## Ejercicio 4: Validar Email Corporativo

```javascript
/**
 * Patrón: Email que NO sea de dominio público
 *
 * ¿Por qué? Filtrar emails personales
 * ¿Para qué? Validar emails corporativos
 *
 * Desglose:
 * [\w.-]+          → Usuario
 * @                → Arroba
 * (?!              → Negative lookahead
 *   (?:gmail|...)  → Dominios a excluir
 *   \.com          → Con .com
 * )
 * [\w.-]+          → Dominio aceptado
 * \.\w{2,}         → TLD
 */
const pattern =
  /[\w.-]+@(?!(?:gmail|hotmail|yahoo|outlook)\.com\b)[\w.-]+\.\w{2,}/gi;

const texto = `empleado@empresa.com
personal@gmail.com
trabajo@corporacion.es
amigo@hotmail.com
jefe@compania.net
contacto@yahoo.com`;

console.log(texto.match(pattern));
// ['empleado@empresa.com', 'trabajo@corporacion.es', 'jefe@compania.net']

// Función de validación
function esEmailCorporativo(email) {
  return pattern.test(email);
}

console.log(esEmailCorporativo('test@gmail.com')); // false
console.log(esEmailCorporativo('test@empresa.com')); // true
```

---

## Ejercicio 5: Extraer Valores de Atributos HTML

```javascript
/**
 * Patrones: Valores de atributos id y class
 *
 * ¿Por qué? Necesitamos los valores sin el nombre del atributo
 * ¿Para qué? Parsing de HTML para manipulación
 */
const idPattern = /(?<=id=["'])[^"']+(?=["'])/g;
const classPattern = /(?<=class=["'])[^"']+(?=["'])/g;

const html = `<div id="main" class="container">
  <span id="title" class="header-text">
  <a href="/link" class="nav-link">
  <button id="submit" type="submit">
</div>`;

const ids = html.match(idPattern);
const classes = html.match(classPattern);

console.log('IDs:', ids);
// ['main', 'title', 'submit']

console.log('Classes:', classes);
// ['container', 'header-text', 'nav-link']

// Función genérica
function extraerAtributo(html, atributo) {
  const pattern = new RegExp(`(?<=${atributo}=["'])[^"']+(?=["'])`, 'g');
  return html.match(pattern) || [];
}

console.log(extraerAtributo(html, 'href'));
// ['/link']
```

---

## Ejercicio 6: Password Validator

```javascript
/**
 * Patrón: Validación de contraseña con múltiples requisitos
 *
 * ¿Por qué? Múltiples condiciones deben cumplirse simultáneamente
 * ¿Para qué? Seguridad de cuentas de usuario
 *
 * Desglose:
 * ^              → Inicio del string
 * (?=.*[A-Z])    → Debe contener al menos una mayúscula
 * (?=.*[a-z])    → Debe contener al menos una minúscula
 * (?=.*\d)       → Debe contener al menos un dígito
 * .{8,}          → Mínimo 8 caracteres
 * $              → Fin del string
 */
const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/;

function validar(password) {
  return passwordPattern.test(password);
}

// Tests
console.log(validar('Abc12345')); // true
console.log(validar('abcdefgh')); // false (sin mayúscula)
console.log(validar('ABC12345')); // false (sin minúscula)
console.log(validar('Abcdefgh')); // false (sin dígito)
console.log(validar('Abc123')); // false (menos de 8)
console.log(validar('Abc123!@#')); // true
console.log(validar('abc123!@')); // false (sin mayúscula)

// Con requisitos adicionales
const strongPattern =
  /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])(?!.*\s).{8,20}$/;

function validarFuerte(password) {
  const result = {
    valido: strongPattern.test(password),
    requisitos: {
      longitud: password.length >= 8 && password.length <= 20,
      mayuscula: /[A-Z]/.test(password),
      minuscula: /[a-z]/.test(password),
      digito: /\d/.test(password),
      especial: /[!@#$%^&*]/.test(password),
      sinEspacios: !/\s/.test(password),
    },
  };
  return result;
}

console.log(validarFuerte('Abc123!@'));
// { valido: true, requisitos: { longitud: true, ... } }
```

---

## Ejercicio 7: Formatear Números con Separadores

```javascript
/**
 * Patrón: Insertar comas cada 3 dígitos
 *
 * ¿Por qué? Los números grandes son difíciles de leer
 * ¿Para qué? Mejorar legibilidad
 *
 * Desglose:
 * \B              → No al inicio de palabra (evita coma al inicio)
 * (?=             → Positive lookahead
 *   (\d{3})+      → Grupos de 3 dígitos
 *   (?!\d)        → NO seguido de más dígitos (fin del número)
 * )
 */
function formatear(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

console.log(formatear(1234)); // "1,234"
console.log(formatear(1234567)); // "1,234,567"
console.log(formatear(1000000)); // "1,000,000"
console.log(formatear(123)); // "123"
console.log(formatear(12345678901)); // "12,345,678,901"

// Versión para decimales
function formatearDecimal(num) {
  const [entero, decimal] = num.toString().split('.');
  const enteroFormateado = entero.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return decimal ? `${enteroFormateado}.${decimal}` : enteroFormateado;
}

console.log(formatearDecimal(1234567.89)); // "1,234,567.89"
```

---

## Desafío: Syntax Highlighter

```javascript
/**
 * Syntax Highlighter para JavaScript básico
 *
 * ¿Por qué? Resaltar diferentes elementos del código
 * ¿Para qué? Mejorar legibilidad del código
 */

const codigo = `const greeting = "Hello World";
let count = 42;
function sayHello() {
  return greeting;
}
// This is a comment
const result = sayHello();`;

/**
 * Extrae todos los elementos sintácticos
 *
 * @param {string} code - Código fuente
 * @returns {object} Elementos categorizados
 */
function analizarCodigo(code) {
  // Primero extraer comentarios y strings (para excluirlos después)
  const comentarios = code.match(/\/\/.*$/gm) || [];
  const strings = code.match(/["'][^"']*["']/g) || [];

  // Crear versión sin comentarios ni strings para buscar keywords
  let codigoLimpio = code
    .replace(/\/\/.*$/gm, '___COMMENT___')
    .replace(/["'][^"']*["']/g, '___STRING___');

  // Keywords (solo como palabras completas)
  const keywordPattern =
    /\b(?:const|let|var|function|return|if|else|for|while)\b/g;
  const keywords = codigoLimpio.match(keywordPattern) || [];

  // Números (no dentro de strings)
  const numeros = codigoLimpio.match(/\b\d+\b/g) || [];

  return {
    keywords,
    strings,
    numbers: numeros,
    comments: comentarios,
  };
}

console.log(analizarCodigo(codigo));
// {
//   keywords: ['const', 'let', 'function', 'return', 'const'],
//   strings: ['"Hello World"'],
//   numbers: ['42'],
//   comments: ['// This is a comment']
// }

/**
 * Versión avanzada: resalta en HTML
 */
function resaltarHTML(code) {
  let resultado = code
    // Escapar HTML
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Comentarios primero (para que no afecten el resto)
    .replace(/\/\/.*$/gm, '<span class="comment">$&</span>')
    // Strings
    .replace(/["'][^"']*["']/g, '<span class="string">$&</span>')
    // Keywords (con lookarounds para evitar parciales)
    .replace(
      /\b(const|let|var|function|return|if|else|for|while)\b/g,
      '<span class="keyword">$1</span>'
    )
    // Números
    .replace(/\b(\d+)\b/g, '<span class="number">$1</span>');

  return resultado;
}

console.log(resaltarHTML(codigo));
```

---

**Siguiente:** [Proyecto Semana 05](../3-proyecto/proyecto-05-validador.md)
