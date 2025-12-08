# Semana 01: Introducción a las Expresiones Regulares

## ¿Qué son las Expresiones Regulares?

Las **expresiones regulares** (Regular Expressions o **RegExp**) son patrones de búsqueda que describen conjuntos de cadenas de texto. Son una herramienta fundamental en programación para:

- Buscar texto específico
- Validar formatos (emails, teléfonos, URLs)
- Extraer información de strings
- Reemplazar texto de forma inteligente

## Anatomía de una RegExp

```
/patrón/flags
 │       │
 │       └─ Modificadores opcionales (g, i, m, etc.)
 └───────── El pattern que queremos encontrar
```

### Ejemplo Básico

```javascript
/**
 * ¿Por qué? Necesitamos encontrar la palabra "hola" en un texto
 * ¿Para qué? Verificar si el usuario saluda en su mensaje
 */
const pattern = /hola/;
const texto = '¡hola mundo!';
const resultado = pattern.test(texto); // true
```

## Literales vs Metacaracteres

### Literales

Son caracteres que se buscan **exactamente** como se escriben.

```javascript
/**
 * ¿Por qué? Los literales representan texto exacto
 * ¿Para qué? Buscar palabras o frases específicas sin ambigüedad
 */
const pattern = /gato/;

// Matches:
// ✅ "El gato negro"
// ✅ "gato"
// ✅ "gatoazo" (contiene "gato")

// No matches:
// ❌ "Gato" (G mayúscula)
// ❌ "perro"
```

### Metacaracteres

Son caracteres con **significado especial** en regex. Los metacaracteres básicos son:

| Metacharacter | Nombre    | Descripción                            |
| ------------- | --------- | -------------------------------------- |
| `.`           | Dot       | Cualquier carácter excepto nueva línea |
| `^`           | Caret     | Inicio del string o línea              |
| `$`           | Dollar    | Fin del string o línea                 |
| `\`           | Backslash | Escapa el siguiente carácter           |

## El Metacharacter Dot (`.`)

El punto coincide con **cualquier carácter** (excepto `\n` por defecto).

```javascript
/**
 * ¿Por qué? A veces no sabemos exactamente qué carácter habrá en una posición
 * ¿Para qué? Crear patrones flexibles que acepten variaciones
 */
const pattern = /c.sa/;

// Matches:
// ✅ "casa"    → el . coincide con 'a'
// ✅ "cosa"    → el . coincide con 'o'
// ✅ "cesa"    → el . coincide con 'e'
// ✅ "c@sa"    → el . coincide con '@'
// ✅ "c1sa"    → el . coincide con '1'

// No matches:
// ❌ "csa"     → falta un carácter entre 'c' y 's'
// ❌ "caasa"   → hay dos caracteres entre 'c' y 's'
```

### Escapando el Dot

```javascript
/**
 * ¿Por qué? A veces necesitamos buscar un punto literal
 * ¿Para qué? Validar extensiones de archivo, URLs, IPs, etc.
 */
const patternDotLiteral = /archivo\.txt/;

// Matches:
// ✅ "archivo.txt"

// No matches:
// ❌ "archivoXtxt"  → el \. solo coincide con punto literal
```

## Los Anchors: `^` y `$`

Los **anchors** no coinciden con caracteres, sino con **posiciones**.

### Anchor de Inicio (`^`)

```javascript
/**
 * ¿Por qué? Queremos asegurarnos de que algo esté AL INICIO
 * ¿Para qué? Validar que un string comience con cierto patrón
 */
const pattern = /^Hola/;

// Matches:
// ✅ "Hola mundo"
// ✅ "Hola"

// No matches:
// ❌ "Digo Hola"     → "Hola" no está al inicio
// ❌ "hola mundo"    → minúscula no coincide
```

### Anchor de Fin (`$`)

```javascript
/**
 * ¿Por qué? Queremos asegurarnos de que algo esté AL FINAL
 * ¿Para qué? Validar extensiones de archivo o terminaciones específicas
 */
const pattern = /mundo$/;

// Matches:
// ✅ "Hola mundo"
// ✅ "mundo"

// No matches:
// ❌ "mundo feliz"   → "mundo" no está al final
```

### Combinando `^` y `$`

```javascript
/**
 * ¿Por qué? Queremos coincidir con el string COMPLETO
 * ¿Para qué? Validar que todo el input coincida exactamente
 */
const pattern = /^exacto$/;

// Matches:
// ✅ "exacto"

// No matches:
// ❌ "exacto pero largo"
// ❌ "no exacto"
// ❌ "exacto\n"
```

## El Backslash (`\`) - Escape

El backslash tiene dos funciones principales:

### 1. Escapar Metacaracteres

```javascript
/**
 * ¿Por qué? Los metacaracteres tienen significado especial
 * ¿Para qué? Buscar el carácter literal en lugar de su función especial
 */

// Buscar un punto literal
const puntoLiteral = /\./;

// Buscar un signo de dólar literal
const dolarLiteral = /\$/;

// Buscar el precio "$9.99"
const precio = /\$\d+\.\d{2}/;
```

### 2. Crear Secuencias Especiales

```javascript
/**
 * ¿Por qué? Algunos patrones son muy comunes y necesitan atajos
 * ¿Para qué? Escribir regex más legibles y concisas
 */

// \d = cualquier dígito (equivale a [0-9])
const digito = /\d/;

// \w = cualquier carácter de palabra (equivale a [a-zA-Z0-9_])
const palabra = /\w/;

// \s = cualquier espacio en blanco (espacio, tab, newline)
const espacio = /\s/;
```

## Resumen Visual

```
┌─────────────────────────────────────────────────────────┐
│                    METACARACTERES BÁSICOS               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   .   →  Cualquier carácter (excepto \n)               │
│   ^   →  Inicio del string                              │
│   $   →  Fin del string                                 │
│   \   →  Escapa el siguiente carácter                   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                      EJEMPLOS                           │
├─────────────────────────────────────────────────────────┤
│   /^Hola$/      →  Solo "Hola" exacto                   │
│   /a.b/         →  "a" + cualquier char + "b"          │
│   /archivo\.js/ →  "archivo.js" literal                │
│   /^[A-Z]/      →  Empieza con mayúscula               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Próximo Paso

En el siguiente módulo exploraremos más ejemplos prácticos y comenzaremos con los ejercicios.

---

**Recursos:**

- [regex101.com](https://regex101.com) - Prueba tus patrones aquí
