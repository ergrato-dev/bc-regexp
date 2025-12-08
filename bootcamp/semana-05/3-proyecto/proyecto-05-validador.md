# Proyecto Semana 05: Validador de Formularios Avanzado

## 🎯 Objetivo

Crear un **sistema de validación de formularios** usando lookarounds para:

- Validar passwords con múltiples requisitos
- Validar tarjetas de crédito
- Validar nombres de usuario
- Extraer información contextual

## 📋 Descripción

Construirás un validador completo que puede usarse en aplicaciones reales.

## 🛠️ Instrucciones

### Paso 1: Definir Reglas de Validación

```javascript
/**
 * Reglas de validación para cada campo
 */
const REGLAS = {
  password: {
    minLength: 8,
    maxLength: 128,
    requireUppercase: true,
    requireLowercase: true,
    requireDigit: true,
    requireSpecial: true,
    noSpaces: true,
    noConsecutiveRepeats: true,
  },
  username: {
    minLength: 3,
    maxLength: 20,
    allowedChars: /^[a-zA-Z0-9_]+$/,
    mustStartWithLetter: true,
    noConsecutiveUnderscores: true,
  },
  creditCard: {
    validFormats: ['visa', 'mastercard', 'amex'],
    requireLuhn: true,
  },
};
```

### Paso 2: Validador de Password

```javascript
/**
 * Patrón de password con todos los requisitos
 *
 * ¿Por qué? Múltiples reglas deben cumplirse simultáneamente
 * ¿Para qué? Seguridad de cuentas de usuario
 *
 * Requisitos:
 * - 8-128 caracteres
 * - Al menos una mayúscula
 * - Al menos una minúscula
 * - Al menos un dígito
 * - Al menos un carácter especial (!@#$%^&*()_+-=)
 * - Sin espacios
 * - Sin 3 caracteres consecutivos iguales
 */
function crearPatternPassword() {
  // Tu implementación
}

function validarPassword(password) {
  const resultado = {
    valido: false,
    errores: [],
    fortaleza: 0, // 0-100
  };

  // Tu implementación

  return resultado;
}
```

### Paso 3: Validador de Username

```javascript
/**
 * Validar nombre de usuario
 *
 * Requisitos:
 * - 3-20 caracteres
 * - Solo letras, números y guión bajo
 * - Debe empezar con letra
 * - Sin guiones bajos consecutivos
 * - Sin palabras prohibidas
 */
const PALABRAS_PROHIBIDAS = ['admin', 'root', 'system', 'null', 'undefined'];

function validarUsername(username) {
  const resultado = {
    valido: false,
    errores: [],
    sugerencias: [],
  };

  // Tu implementación

  return resultado;
}
```

### Paso 4: Validador de Tarjeta de Crédito

```javascript
/**
 * Validar número de tarjeta de crédito
 *
 * Formatos:
 * - Visa: empieza con 4, 16 dígitos
 * - MasterCard: empieza con 51-55 o 2221-2720, 16 dígitos
 * - Amex: empieza con 34 o 37, 15 dígitos
 *
 * También aplicar algoritmo de Luhn
 */
function validarTarjeta(numero) {
  const resultado = {
    valido: false,
    tipo: null,
    errores: [],
  };

  // Tu implementación

  return resultado;
}

// Algoritmo de Luhn (verificación de tarjetas)
function verificarLuhn(numero) {
  // Tu implementación
}
```

### Paso 5: Extractor de Información Contextual

```javascript
/**
 * Extraer información usando lookarounds
 *
 * - Precios solo en euros
 * - Fechas solo en formato europeo
 * - Menciones de usuarios (@username)
 * - Hashtags (#tema)
 */
function extraerInformacion(texto) {
  return {
    precios: [], // Valores numéricos de precios en €
    fechas: [], // Fechas en formato DD/MM/YYYY
    menciones: [], // Usernames mencionados
    hashtags: [], // Hashtags
  };
}
```

## 💡 Hints

<details>
<summary>Hint: Password Pattern</summary>

```javascript
const passwordPattern = /^
  (?=.*[A-Z])           // Al menos una mayúscula
  (?=.*[a-z])           // Al menos una minúscula
  (?=.*\d)              // Al menos un dígito
  (?=.*[!@#$%^&*])      // Al menos un especial
  (?!.*\s)              // Sin espacios
  (?!.*(.)\1{2})        // Sin 3 consecutivos iguales
  .{8,128}              // 8-128 caracteres
$/x;

// En JavaScript (sin flag x):
/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])(?!.*\s)(?!.*(.)\1{2}).{8,128}$/
```

</details>

<details>
<summary>Hint: Username Pattern</summary>

```javascript
// Empezar con letra, 3-20 chars, sin __ consecutivos
/^(?!.*__)[a-zA-Z]\w{2,19}$/;
```

</details>

<details>
<summary>Hint: Tarjetas</summary>

```javascript
const patrones = {
  visa: /^4\d{15}$/,
  mastercard:
    /^(?:5[1-5]\d{14}|2(?:2[2-9]\d{12}|[3-6]\d{13}|7[01]\d{12}|720\d{12}))$/,
  amex: /^3[47]\d{13}$/,
};
```

</details>

<details>
<summary>Hint: Algoritmo de Luhn</summary>

```javascript
function luhn(numero) {
  const digits = numero.replace(/\D/g, '').split('').reverse().map(Number);
  const sum = digits.reduce((acc, digit, i) => {
    if (i % 2 === 1) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    return acc + digit;
  }, 0);
  return sum % 10 === 0;
}
```

</details>

## 🚀 Extensiones

### Extensión 1: Medidor de Fortaleza Visual

```javascript
function calcularFortaleza(password) {
  // Retorna 0-100 basado en:
  // - Longitud (+10 por cada 4 caracteres sobre 8)
  // - Variedad de caracteres
  // - Ausencia de patrones comunes
}
```

### Extensión 2: Sugerencias de Username

```javascript
function sugerirUsernames(base, cantidad = 5) {
  // Genera alternativas cuando el username está tomado
}
```

### Extensión 3: Formateo de Tarjeta

```javascript
function formatearTarjeta(numero) {
  // Retorna "4111 1111 1111 1111" o "3411 111111 11111"
  // según el tipo de tarjeta
}
```

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-05-validador.md      (este archivo)
├── validador.js                   (tu solución)
├── test-validador.js              (tests)
└── demo.html                      (opcional: demo visual)
```

## ✅ Criterios de Evaluación

| Criterio                             | Puntos |
| ------------------------------------ | ------ |
| Password validator completo          | 25%    |
| Username validator con sugerencias   | 20%    |
| Tarjeta con detección de tipo + Luhn | 25%    |
| Extractor de información contextual  | 20%    |
| Manejo de errores y edge cases       | 10%    |

## 📝 Reflexión

1. ¿Por qué los lookaheads son ideales para validar passwords?
2. ¿Qué ventajas tiene usar múltiples lookaheads vs validaciones separadas?
3. ¿Cómo manejarías internacionalización (otros idiomas)?
4. ¿Qué limitaciones tiene la validación con regex vs validación programática?

---

**Solución:** Disponible en `solucion-proyecto-05.js`
