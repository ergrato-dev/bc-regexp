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

**Python:**

```python
import re

precio_pattern = re.compile(r'(?<=\$)\d+\.\d{2}')

texto = """Producto A: $99.99
Producto B: €85.00
Producto C: $149.99
Producto D: £120.00
Producto E: $25.50"""

print(precio_pattern.findall(texto))
# ['99.99', '149.99', '25.50']

# Convertir a números y sumar
precios = [float(p) for p in precio_pattern.findall(texto)]
total = sum(precios)
print(f'Total: ${total:.2f}')
# Total: $274.98
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

**Python:**

```python
import re

pattern = re.compile(r'\b(?!un)\w+\b', re.IGNORECASE)

texto = """The task was undone but the work was complete.
He was unhappy but she was happy.
The box was unopened while another was opened."""

palabras = pattern.findall(texto)
print(palabras)
# ['The', 'task', 'was', 'but', 'the', 'work', 'was', 'complete',
#  'He', 'was', 'but', 'she', 'was', 'happy',
#  'The', 'box', 'was', 'while', 'another', 'was', 'opened']

# Verificar que las palabras "un..." fueron excluidas
excluidas = re.findall(r'\bun\w+\b', texto, re.IGNORECASE)
print('Excluidas:', excluidas)
# ['undone', 'unhappy', 'unopened']
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

**Python:**

```python
import re

pattern = re.compile(r'\d+(?=(?:km|kg|cm|m)\b)')

texto = """Velocidad: 120km/h
Peso: 75kg
Altura: 180cm
Temperatura: 25
Distancia: 500m
Precio: 99"""

print(pattern.findall(texto))
# ['120', '75', '180', '500']

# Para obtener también las unidades (separadas)
con_unidades = re.compile(r'(\d+)(km|kg|cm|m)\b')
for match in con_unidades.finditer(texto):
    print(f'Valor: {match.group(1)}, Unidad: {match.group(2)}')
# Valor: 120, Unidad: km
# Valor: 75, Unidad: kg
# Valor: 180, Unidad: cm
# Valor: 500, Unidad: m
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

**Python:**

```python
import re

pattern = re.compile(
    r'[\w.-]+@(?!(?:gmail|hotmail|yahoo|outlook)\.com\b)[\w.-]+\.\w{2,}',
    re.IGNORECASE
)

texto = """empleado@empresa.com
personal@gmail.com
trabajo@corporacion.es
amigo@hotmail.com
jefe@compania.net
contacto@yahoo.com"""

print(pattern.findall(texto))
# ['empleado@empresa.com', 'trabajo@corporacion.es', 'jefe@compania.net']

# Función de validación
def es_email_corporativo(email):
    return bool(pattern.search(email))

print(es_email_corporativo('test@gmail.com'))  # False
print(es_email_corporativo('test@empresa.com'))  # True
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

**Python:**

```python
import re

id_pattern = re.compile(r'(?<=id=["\'])[^"\']+(?=["\'])')
class_pattern = re.compile(r'(?<=class=["\'])[^"\']+(?=["\'])')

html = """<div id="main" class="container">
  <span id="title" class="header-text">
  <a href="/link" class="nav-link">
  <button id="submit" type="submit">
</div>"""

ids = id_pattern.findall(html)
classes = class_pattern.findall(html)

print('IDs:', ids)      # ['main', 'title', 'submit']
print('Classes:', classes)  # ['container', 'header-text', 'nav-link']

# Función genérica
def extraer_atributo(html, atributo):
    pattern = re.compile(rf'(?<={atributo}=["\'])[^"\']+(?=["\'])')
    return pattern.findall(html) or []

print(extraer_atributo(html, 'href'))
# ['/link']
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

**Python:**

```python
import re

password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$')

def validar(password):
    return bool(password_pattern.search(password))

# Tests
print(validar('Abc12345'))   # True
print(validar('abcdefgh'))   # False (sin mayúscula)
print(validar('ABC12345'))   # False (sin minúscula)
print(validar('Abcdefgh'))   # False (sin dígito)
print(validar('Abc123'))     # False (menos de 8)
print(validar('Abc123!@#'))  # True
print(validar('abc123!@'))   # False (sin mayúscula)

# Con requisitos adicionales
strong_pattern = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])(?!.*\s).{8,20}$'
)

def validar_fuerte(password):
    return {
        'valido': bool(strong_pattern.search(password)),
        'requisitos': {
            'longitud': 8 <= len(password) <= 20,
            'mayuscula': bool(re.search(r'[A-Z]', password)),
            'minuscula': bool(re.search(r'[a-z]', password)),
            'digito': bool(re.search(r'\d', password)),
            'especial': bool(re.search(r'[!@#$%^&*]', password)),
            'sin_espacios': not bool(re.search(r'\s', password)),
        }
    }

print(validar_fuerte('Abc123!@'))
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

**Python:**

```python
import re

def formatear(num):
    return re.sub(r'\B(?=(\d{3})+(?!\d))', ',', str(num))

print(formatear(1234))          # "1,234"
print(formatear(1234567))       # "1,234,567"
print(formatear(1000000))       # "1,000,000"
print(formatear(123))           # "123"
print(formatear(12345678901))   # "12,345,678,901"

# Versión para decimales
def formatear_decimal(num):
    entero, *resto = str(num).split('.')
    entero_formateado = formatear(entero)
    return f"{entero_formateado}.{resto[0]}" if resto else entero_formateado

print(formatear_decimal(1234567.89))  # "1,234,567.89"
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

**Python:**

```python
import re

codigo = """const greeting = "Hello World";
let count = 42;
function sayHello() {
  return greeting;
}
// This is a comment
const result = sayHello();"""

def analizar_codigo(code):
    # Primero extraer comentarios y strings (para excluirlos después)
    comentarios = re.findall(r'//.*$', code, re.MULTILINE) or []
    strings = re.findall(r'["\'][^"\']*["\']', code) or []

    # Crear versión sin comentarios ni strings para buscar keywords
    codigo_limpio = re.sub(r'//.*$', '___COMMENT___', code, flags=re.MULTILINE)
    codigo_limpio = re.sub(r'["\'][^"\']*["\']', '___STRING___', codigo_limpio)

    # Keywords (solo como palabras completas)
    keywords = re.findall(
        r'\b(?:const|let|var|function|return|if|else|for|while)\b',
        codigo_limpio
    ) or []

    # Números (no dentro de strings)
    numeros = re.findall(r'\b\d+\b', codigo_limpio) or []

    return {
        'keywords': keywords,
        'strings': strings,
        'numbers': numeros,
        'comments': comentarios,
    }

print(analizar_codigo(codigo))
# {
#   'keywords': ['const', 'let', 'function', 'return', 'const'],
#   'strings': ['"Hello World"'],
#   'numbers': ['42'],
#   'comments': ['// This is a comment']
# }

# Versión avanzada: resalta en HTML
def resaltar_html(code):
    import re
    resultado = code
    # Escapar HTML
    resultado = resultado.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Comentarios primero
    resultado = re.sub(r'//.*$', r'<span class="comment">\g<0></span>', resultado, flags=re.MULTILINE)
    # Strings
    resultado = re.sub(r'["\'][^"\']*["\']', r'<span class="string">\g<0></span>', resultado)
    # Keywords
    resultado = re.sub(
        r'\b(const|let|var|function|return|if|else|for|while)\b',
        r'<span class="keyword">\1</span>', resultado
    )
    # Números
    resultado = re.sub(r'\b(\d+)\b', r'<span class="number">\1</span>', resultado)
    return resultado

print(resaltar_html(codigo))
```

---

**Siguiente:** [Proyecto Semana 05](../3-proyecto/proyecto-05-validador.md)
