# Proyecto Semana 05: Validador de Formularios Avanzado

> **Lenguaje:** Elige **JavaScript** o **Python** para tu implementación. La lógica de regex es idéntica; solo cambia la sintaxis del lenguaje.
> - **JavaScript:** `/patron/flags` con `.test()`, `.match()`, `.replace()`
> - **Python:** `re.compile(r'patron')` con `.search()`, `.findall()`, `.sub()`

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

**JavaScript:**
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

**Python:**
```python
import re

REGLAS = {
    'password': {
        'minLength': 8,
        'maxLength': 128,
        'requireUppercase': True,
        'requireLowercase': True,
        'requireDigit': True,
        'requireSpecial': True,
        'noSpaces': True,
        'noConsecutiveRepeats': True,
    },
    'username': {
        'minLength': 3,
        'maxLength': 20,
        'allowedChars': re.compile(r'^[a-zA-Z0-9_]+$'),
        'mustStartWithLetter': True,
        'noConsecutiveUnderscores': True,
    },
    'creditCard': {
        'validFormats': ['visa', 'mastercard', 'amex'],
        'requireLuhn': True,
    },
}
```

### Paso 2: Validador de Password

**JavaScript:**
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

**Python:**
```python
def crear_pattern_password():
    # Tu implementación
    pass

def validar_password(password):
    resultado = {
        'valido': False,
        'errores': [],
        'fortaleza': 0,  # 0-100
    }
    # Tu implementación
    return resultado
```

### Paso 3: Validador de Username

**JavaScript:**
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

**Python:**
```python
PALABRAS_PROHIBIDAS = ['admin', 'root', 'system', 'null', 'undefined']

def validar_username(username):
    resultado = {
        'valido': False,
        'errores': [],
        'sugerencias': [],
    }
    # Tu implementación
    return resultado
```

### Paso 4: Validador de Tarjeta de Crédito

**JavaScript:**
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

**Python:**
```python
def validar_tarjeta(numero):
    resultado = {
        'valido': False,
        'tipo': None,
        'errores': [],
    }
    # Tu implementación
    return resultado

def verificar_luhn(numero):
    # Tu implementación
    pass
```

### Paso 5: Extractor de Información Contextual

**JavaScript:**
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

**Python:**
```python
def extraer_informacion(texto):
    return {
        'precios': [],   # Valores numéricos de precios en €
        'fechas': [],    # Fechas en formato DD/MM/YYYY
        'menciones': [], # Usernames mencionados
        'hashtags': [],  # Hashtags
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
├── validador.js                   (solución JavaScript)
├── validador.py                   (solución Python)
├── test-validador.js              (tests JavaScript)
├── test_validador.py              (tests Python)
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

**Solución JavaScript:** Disponible en `solucion-proyecto-05.js`
**Solución Python:** Disponible en `solucion-proyecto-05.py`
