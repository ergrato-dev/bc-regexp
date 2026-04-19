# Proyecto Semana 06: Buscador de Texto Avanzado

## 🎯 Objetivo

Crear un **buscador de texto avanzado** que utilice todos los flags disponibles para ofrecer búsquedas flexibles y potentes.

## 📋 Descripción

Construirás un motor de búsqueda que pueda:

- Buscar palabras exactas o parciales
- Ignorar mayúsculas/minúsculas
- Buscar en múltiples líneas
- Soportar caracteres Unicode
- Resaltar coincidencias con posiciones exactas

## 🛠️ Instrucciones

### Paso 1: Configuración Base

```javascript
/**
 * Configuración del buscador
 */
const SearchConfig = {
  caseSensitive: false, // i flag
  wholeWord: false, // \b word boundaries
  multiline: true, // m flag
  dotAll: false, // s flag
  unicode: true, // u flag
  showIndices: true, // d flag
};
```

### Paso 2: Motor de Búsqueda

```javascript
/**
 * Motor de búsqueda principal
 *
 * @param {string} texto - Texto donde buscar
 * @param {string} query - Término de búsqueda
 * @param {object} opciones - Configuración
 * @returns {object} Resultados de la búsqueda
 */
function buscar(texto, query, opciones = {}) {
  const config = { ...SearchConfig, ...opciones };

  return {
    matches: [], // Array de coincidencias
    total: 0, // Número total
    positions: [], // Posiciones [start, end]
    highlighted: '', // Texto con resaltado
    stats: {}, // Estadísticas
  };
}
```

### Paso 3: Construir el Patrón

```javascript
/**
 * Construir regex con flags apropiados
 *
 * @param {string} query - Término de búsqueda
 * @param {object} config - Configuración
 * @returns {RegExp} Expresión regular
 */
function buildPattern(query, config) {
  // Escapar caracteres especiales
  let pattern = escapeRegExp(query);

  // Aplicar word boundaries si es necesario
  if (config.wholeWord) {
    pattern = `\\b${pattern}\\b`;
  }

  // Construir flags
  let flags = 'g'; // Siempre global

  // Tu implementación: agregar flags según config

  return new RegExp(pattern, flags);
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
```

### Paso 4: Resaltador de Texto

```javascript
/**
 * Resaltar coincidencias en el texto
 *
 * @param {string} texto - Texto original
 * @param {RegExp} pattern - Patrón de búsqueda
 * @returns {string} Texto con marcadores
 */
function highlight(texto, pattern) {
  return texto.replace(pattern, '[[MATCH]]$&[[/MATCH]]');
}
```

### Paso 5: Búsqueda Avanzada

```javascript
/**
 * Búsqueda con sintaxis avanzada
 *
 * Soporta:
 * - "frase exacta"
 * - palabra1 palabra2 (AND)
 * - palabra1 OR palabra2
 * - -excluir
 * - palabra*  (wildcard)
 */
function busquedaAvanzada(texto, queryString) {
  // Tu implementación
}
```

## 💡 Hints

<details>
<summary>Hint: Construcción de Flags</summary>

```javascript
function buildFlags(config) {
  let flags = 'g';
  if (!config.caseSensitive) flags += 'i';
  if (config.multiline) flags += 'm';
  if (config.dotAll) flags += 's';
  if (config.unicode) flags += 'u';
  if (config.showIndices) flags += 'd';
  return flags;
}
```

</details>

<details>
<summary>Hint: Parsear Query Avanzada</summary>

```javascript
function parseQuery(queryString) {
  const parts = {
    exact: [], // Frases exactas
    include: [], // Palabras a incluir
    exclude: [], // Palabras a excluir
    wildcard: [], // Patrones con *
  };

  // Extraer frases exactas
  const exactPattern = /"([^"]+)"/g;
  for (const match of queryString.matchAll(exactPattern)) {
    parts.exact.push(match[1]);
  }

  // Continuar con el resto...
  return parts;
}
```

</details>

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-06-buscador.md      (este archivo)
├── buscador.js                   (tu solución)
├── test-buscador.js              (tests)
└── demo.html                     (opcional: demo visual)
```

## ✅ Criterios de Evaluación

| Criterio                               | Puntos |
| -------------------------------------- | ------ |
| Búsqueda básica con flags              | 25%    |
| Word boundaries y case sensitivity     | 20%    |
| Resaltado con posiciones               | 20%    |
| Búsqueda avanzada (AND, OR, exclusión) | 25%    |
| Manejo de Unicode                      | 10%    |

## 🚀 Extensiones

### Extensión 1: Búsqueda Fuzzy

```javascript
// Permitir errores tipográficos
function busquedaFuzzy(texto, query, maxErrores = 1) {
  // Implementar distancia de Levenshtein con regex
}
```

### Extensión 2: Contexto de Resultados

```javascript
// Mostrar líneas alrededor del match
function getContexto(texto, posicion, lineas = 2) {
  // Retornar líneas antes y después
}
```

### Extensión 3: Caché de Búsquedas

```javascript
// Cachear resultados para búsquedas repetidas
const cache = new Map();
function buscarConCache(texto, query, opciones) {
  const key = `${query}:${JSON.stringify(opciones)}`;
  if (cache.has(key)) return cache.get(key);
  // ...
}
```

---

**Solución:** Disponible en `solucion-proyecto-06.js`
