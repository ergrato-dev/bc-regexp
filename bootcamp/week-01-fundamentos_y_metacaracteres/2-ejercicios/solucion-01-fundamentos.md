# Soluciones - Ejercicios Semana 01

> ⚠️ **Importante:** Intenta resolver los ejercicios antes de ver las soluciones.

---

## Ejercicio 01: Literales Básicos

### Soluciones

```javascript
/**
 * Tarea 1: Encuentra "JavaScript"
 *
 * ¿Por qué? Buscamos el nombre exacto del lenguaje
 * ¿Para qué? Contar menciones o resaltar el término
 */
const pattern1 = /JavaScript/g;
// Matches: 2 (línea 1 y línea 3)

/**
 * Tarea 2: Encuentra "Java"
 *
 * ¿Por qué? El literal "Java" aparece como substring
 * ¿Para qué? Demostrar que los literales no respetan límites de palabra
 */
const pattern2 = /Java/g;
// Matches: 3 (en "JavaScript" x2, y en "Java" x1)
// ⚠️ Esto demuestra un problema común: matches no deseados

/**
 * Tarea 3: Encuentra "Script"
 *
 * ¿Por qué? "Script" aparece en JavaScript y TypeScript
 * ¿Para qué? Mostrar cómo los literales encuentran substrings
 */
const pattern3 = /Script/g;
// Matches: 3 (JavaScript x2, TypeScript x1)
```

### Lección Aprendida

Los literales encuentran el texto **en cualquier parte** del string, no solo palabras completas. En semanas futuras aprenderemos a usar `\b` (word boundary) para evitar esto.

---

## Ejercicio 02: El Metacharacter Dot

### Solución

```javascript
/**
 * Patrón para c + cualquier carácter + sa
 *
 * ¿Por qué? El dot actúa como comodín para un carácter
 * ¿Para qué? Crear patrones flexibles que acepten variaciones
 */
const pattern = /c.sa/g;

// Resultados:
// ✅ casa  → . = 'a'
// ✅ cosa  → . = 'o'
// ✅ cesa  → . = 'e'
// ✅ cisa  → . = 'i'
// ✅ cusa  → . = 'u'
// ✅ c@sa  → . = '@'
// ✅ c1sa  → . = '1'
// ✅ cssa  → . = 's' (¡sí coincide!)
```

### Respuestas

1. **¿Coincide con "cssa"?** SÍ, porque el dot coincide con 's' (el primer 's'), y luego sigue "sa".

2. **¿Coincide con "ca"?** NO, porque el dot necesita UN carácter entre 'c' y 'sa'. "ca" no tiene nada entre 'c' y 'a'.

---

## Ejercicio 03: Anchors de Inicio y Fin

### Soluciones

```javascript
/**
 * Tarea 1: Empieza con "Hola"
 *
 * ¿Por qué? Queremos verificar el inicio del string
 * ¿Para qué? Validar saludos, prefijos, encabezados
 */
const pattern1 = /^Hola/;

/**
 * Tarea 2: Termina con "mundo"
 *
 * ¿Por qué? Queremos verificar el final del string
 * ¿Para qué? Validar extensiones, sufijos, terminaciones
 */
const pattern2 = /mundo$/;

/**
 * Tarea 3: Exactamente "Hola"
 *
 * ¿Por qué? El string completo debe ser solo "Hola"
 * ¿Para qué? Validaciones estrictas de input
 */
const pattern3 = /^Hola$/;

/**
 * Tarea 4: Exactamente "Hola mundo"
 *
 * ¿Por qué? Validar el string completo con espacio
 * ¿Para qué? Match exacto de frases
 */
const pattern4 = /^Hola mundo$/;
```

### Tabla de Resultados

| Patrón           | "Hola mundo" | "mundo Hola" | "Hola" | "mundo" |
| ---------------- | ------------ | ------------ | ------ | ------- |
| `/^Hola/`        | ✅           | ❌           | ✅     | ❌      |
| `/mundo$/`       | ✅           | ❌           | ❌     | ✅      |
| `/^Hola$/`       | ❌           | ❌           | ✅     | ❌      |
| `/^Hola mundo$/` | ✅           | ❌           | ❌     | ❌      |

---

## Ejercicio 04: Escapando Metacaracteres

### Soluciones

```javascript
/**
 * Tarea 1: Encuentra "$9.99"
 *
 * ¿Por qué? $ y . son metacaracteres que debemos escapar
 * ¿Para qué? Buscar precios en texto
 */
const pattern1 = /\$9\.99/;

/**
 * Tarea 2: Encuentra extensiones de archivo
 *
 * ¿Por qué? El punto antes de la extensión es literal
 * ¿Para qué? Identificar tipos de archivo
 */
const pattern2a = /\.txt/g;
const pattern2b = /\.json/g;
// O combinado (adelanto de alternation):
// const pattern2 = /\.(txt|json)/g;

/**
 * Tarea 3: $ al inicio de línea
 *
 * ¿Por qué? Buscamos variables que empiezan con $
 * ¿Para qué? Identificar variables en ciertos lenguajes
 */
const pattern3 = /^\$/;

/**
 * Tarea 4: Símbolo %
 *
 * ¿Por qué? % no es metacharacter, no necesita escape
 * ¿Para qué? Mostrar qué caracteres SÍ necesitan escape
 */
const pattern4 = /%/;
// Nota: % funciona sin escape porque NO es un metacaracter
```

### Metacaracteres que Necesitan Escape

```
. ^ $ * + ? { } [ ] \ | ( )
```

### Caracteres que NO Necesitan Escape

```
% @ # ! , ; : ' " < >
```

---

## Ejercicio 05: Combinando Todo

### Soluciones

```javascript
/**
 * Tarea 1: Archivos que terminan en .js
 *
 * ¿Por qué? Queremos filtrar solo archivos JavaScript
 * ¿Para qué? Listar, procesar, o buscar archivos de un tipo
 */
const pattern1 = /\.js$/;
// Matches: app.js, test.spec.js

/**
 * Tarea 2: Empiezan con letra y terminan en .md
 *
 * ¿Por qué? Filtrar archivos markdown que no son ocultos
 * ¿Para qué? Encontrar documentación
 */
const pattern2 = /^.+\.md$/;
// Matches: README.md
// Nota: .+ = uno o más de cualquier carácter (adelanto)
// Con lo aprendido: /^.\.md$/ solo encontraría "X.md" (1 char)

/**
 * Tarea 3: Archivos con exactamente un punto
 *
 * ¿Por qué? Excluir archivos con múltiples extensiones
 * ¿Para qué? Filtrar archivos simples vs. compuestos
 *
 * ⚠️ Con las herramientas actuales es complejo.
 * Por ahora, una aproximación:
 */
const pattern3 = /^[^.]+\.[^.]+$/; // Esto es adelanto de character classes
// Solución real requiere semana 2

/**
 * Tarea 4: Archivos ocultos (empiezan con .)
 *
 * ¿Por qué? En Unix, archivos que empiezan con . son ocultos
 * ¿Para qué? Encontrar archivos de configuración
 */
const pattern4 = /^\./;
// Matches: .gitignore
```

---

## Desafío Extra 🔥

### Solución

```javascript
/**
 * Validar formato DD.MM.AAAA
 *
 * ¿Por qué? Las fechas vienen en formato europeo con puntos
 * ¿Para qué? Validar input de usuario antes de procesar
 *
 * Limitación: Solo valida formato, no valores lógicos
 */
const fechaPattern = /^..\..\...\.....$/;
//                    ││││ ││ ││ ││││││
//                    ││││ ││ ││ │└┴┴┴┴─ 4 chars para año
//                    ││││ ││ ││ └─────── punto literal
//                    ││││ ││ └┴──────── 2 chars para mes
//                    ││││ │└──────────── punto literal
//                    └┴┴┴─┴───────────── 2 chars para día + anclas

// Más legible (mismo resultado):
const fechaPatternV2 = /^..\..\.....$/;
// Aún mejor (semana 2 con \d):
// const fechaPatternV3 = /^\d{2}\.\d{2}\.\d{4}$/;

// Tests:
fechaPattern.test('25.12.2024'); // true ✅
fechaPattern.test('1.1.2024'); // false ❌ (falta padding)
fechaPattern.test('25-12-2024'); // false ❌ (separador incorrecto)
```

### Nota Importante

Este patrón acepta "XX.XX.XXXX" donde X es **cualquier carácter**, no solo dígitos. Por ejemplo, "ab.cd.efgh" también sería válido.

En la **Semana 02** aprenderemos character classes (`\d`) para validar correctamente que sean dígitos.

---

## Resumen de Patrones Aprendidos

| Concepto      | Símbolo | Ejemplo    | Descripción        |
| ------------- | ------- | ---------- | ------------------ |
| Literal       | `abc`   | `/gato/`   | Texto exacto       |
| Dot           | `.`     | `/c.sa/`   | Cualquier carácter |
| Anchor inicio | `^`     | `/^Hola/`  | Inicio del string  |
| Anchor fin    | `$`     | `/mundo$/` | Fin del string     |
| Match exacto  | `^...$` | `/^Hola$/` | Todo el string     |
| Escape        | `\`     | `/\./`     | Carácter literal   |

---

**Siguiente:** Proyecto de la semana en `3-proyecto/`
