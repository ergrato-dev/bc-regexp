# Ejercicios - Semana 05: Lookahead y Lookbehind

## Ejercicio 1: Precios en Diferentes Monedas

**Objetivo:** Extraer solo el número de precios en dólares.

**Texto de prueba:**

```
Producto A: $99.99
Producto B: €85.00
Producto C: $149.99
Producto D: £120.00
Producto E: $25.50
```

**Requisitos:**

1. Usar positive lookbehind para `$`
2. Capturar solo el número (incluyendo decimales)
3. Ignorar otras monedas

**Resultado esperado:**

```javascript
['99.99', '149.99', '25.50'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// Lookbehind para $ + dígitos con punto decimal
/(?<=\$)\d+\.\d{2}/g;
```

</details>

---

## Ejercicio 2: Palabras Sin Prefijo "un"

**Objetivo:** Encontrar palabras que NO empiecen con "un".

**Texto de prueba:**

```
The task was undone but the work was complete.
He was unhappy but she was happy.
The box was unopened while another was opened.
```

**Requisitos:**

1. Usar negative lookbehind
2. Encontrar palabras completas
3. Case insensitive

**Resultado esperado:**

- Excluir: undone, unhappy, unopened
- Incluir: task, was, but, work, complete, he, she, happy, box, while, another, opened, The

<details>
<summary>💡 Hint</summary>

```javascript
// Word boundary + negative lookbehind para "un"
/\b(?!un)\w+\b/gi;
```

</details>

---

## Ejercicio 3: Números Seguidos de Unidades

**Objetivo:** Extraer números solo si van seguidos de unidades específicas.

**Texto de prueba:**

```
Velocidad: 120km/h
Peso: 75kg
Altura: 180cm
Temperatura: 25
Distancia: 500m
Precio: 99
```

**Requisitos:**

1. Usar positive lookahead
2. Unidades válidas: km, kg, cm, m
3. El número NO debe incluir la unidad

**Resultado esperado:**

```javascript
['120', '75', '180', '500'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// Dígitos + lookahead para unidades
/\d+(?=(?:km|kg|cm|m)\b)/g;
```

</details>

---

## Ejercicio 4: Validar Email Corporativo

**Objetivo:** Validar emails que NO sean de dominios públicos.

**Texto de prueba:**

```
empleado@empresa.com
personal@gmail.com
trabajo@corporacion.es
amigo@hotmail.com
jefe@compania.net
contacto@yahoo.com
```

**Requisitos:**

1. Excluir: gmail.com, hotmail.com, yahoo.com, outlook.com
2. Usar negative lookahead
3. Capturar el email completo si es válido

**Resultado esperado:**

```javascript
['empleado@empresa.com', 'trabajo@corporacion.es', 'jefe@compania.net'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// Email + negative lookahead para dominios públicos
/[\w.-]+@(?!(?:gmail|hotmail|yahoo|outlook)\.com)[\w.-]+\.\w{2,}/g;
```

</details>

---

## Ejercicio 5: Extraer Valores de Atributos HTML

**Objetivo:** Extraer valores de atributos `id` y `class` de HTML.

**Texto de prueba:**

```html
<div id="main" class="container">
  <span id="title" class="header-text">
  <a href="/link" class="nav-link">
  <button id="submit" type="submit">
</div>
```

**Requisitos:**

1. Extraer el valor de `id="..."` (sin el `id=`)
2. Extraer el valor de `class="..."` (sin el `class=`)
3. Usar lookbehind

**Resultado esperado:**

```javascript
ids: ['main', 'title', 'submit'];
classes: ['container', 'header-text', 'nav-link'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// Para id
/(?<=id=["'])[^"']+(?=["'])/g

// Para class
/(?<=class=["'])[^"']+(?=["'])/g
```

</details>

---

## Ejercicio 6: Password Validator

**Objetivo:** Validar contraseñas con múltiples requisitos.

**Contraseñas de prueba:**

```
Abc12345    → válida
abcdefgh    → inválida (sin mayúscula)
ABC12345    → inválida (sin minúscula)
Abcdefgh    → inválida (sin dígito)
Abc123      → inválida (menos de 8)
Abc123!@#   → válida
abc123!@    → inválida (sin mayúscula)
```

**Requisitos:**

- Mínimo 8 caracteres
- Al menos una mayúscula
- Al menos una minúscula
- Al menos un dígito

**Resultado esperado:**

```javascript
validar('Abc12345'); // true
validar('abcdefgh'); // false
validar('ABC12345'); // false
validar('Abcdefgh'); // false
validar('Abc123'); // false
validar('Abc123!@#'); // true
```

<details>
<summary>💡 Hint</summary>

```javascript
// Múltiples lookaheads al inicio
/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/;
```

</details>

---

## Ejercicio 7: Formatear Números con Separadores

**Objetivo:** Añadir separadores de miles a números.

**Números de prueba:**

```
1234 → 1,234
1234567 → 1,234,567
1000000 → 1,000,000
123 → 123
12345678901 → 12,345,678,901
```

**Requisitos:**

1. Usar lookahead para detectar grupos de 3
2. Insertar comas en las posiciones correctas
3. No afectar números menores a 1000

**Resultado esperado:**

```javascript
formatear(1234567); // "1,234,567"
formatear(1000000); // "1,000,000"
formatear(123); // "123"
```

<details>
<summary>💡 Hint</summary>

```javascript
// La posición debe tener grupos de 3 dígitos hasta el final
/\B(?=(\d{3})+(?!\d))/g;
```

</details>

---

## Desafío: Syntax Highlighter

**Objetivo:** Crear un resaltador de sintaxis básico para JavaScript.

**Código de prueba:**

```javascript
const greeting = 'Hello World';
let count = 42;
function sayHello() {
  return greeting;
}
// This is a comment
const result = sayHello();
```

**Requisitos:**

1. Resaltar keywords: `const`, `let`, `function`, `return`
2. Resaltar strings entre comillas
3. Resaltar números
4. Resaltar comentarios `//`
5. No resaltar keywords dentro de strings o comentarios
6. Usar lookarounds para evitar matches parciales

**Formato de salida:**

```javascript
{
  keywords: ['const', 'let', 'function', 'return', 'const'],
  strings: ['"Hello World"'],
  numbers: ['42'],
  comments: ['// This is a comment']
}
```

<details>
<summary>💡 Hint 1: Keywords</summary>

```javascript
// Keyword como palabra completa (no parte de otra)
/(?<![a-zA-Z_])(?:const|let|function|return)(?![a-zA-Z_])/g;
```

</details>

<details>
<summary>💡 Hint 2: Strings</summary>

```javascript
// Strings entre comillas dobles o simples
/["'][^"']*["']/g;
```

</details>

<details>
<summary>💡 Hint 3: Comentarios</summary>

```javascript
// Comentario de línea
/\/\/.*$/gm;
```

</details>

---

## Recursos

- [MDN: Lookahead/Lookbehind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Assertions)
- [regex101.com](https://regex101.com) - Visualiza lookarounds

---

**Soluciones:** [solucion-05-lookarounds.md](solucion-05-lookarounds.md)
