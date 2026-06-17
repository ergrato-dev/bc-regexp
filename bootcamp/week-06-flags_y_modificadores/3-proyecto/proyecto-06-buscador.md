# Proyecto Semana 06: Buscador de Texto Avanzado

> **Lenguaje:** Elige **JavaScript** o **Python** para tu implementación.
> - **JavaScript:** `/patron/gi` — flags inline. Métodos: `.match()`, `.matchAll()`, `.replace()`
> - **Python:** `re.compile(r'patron', re.IGNORECASE | re.MULTILINE)` — flags como constantes. Métodos: `.findall()`, `.finditer()`, `.sub()`

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

**JavaScript:**
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

**Python:**
```python
import re

SearchConfig = {
    'caseSensitive': False,   # re.IGNORECASE
    'wholeWord': False,       # \b word boundaries
    'multiline': True,        # re.MULTILINE
    'dotAll': False,          # re.DOTALL
    'unicode': True,          # Python 3 re es Unicode por defecto
    'showIndices': True,      # match.start() / match.end()
}
```

### Paso 2: Motor de Búsqueda

**JavaScript:**
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

**Python:**
```python
def buscar(texto, query, opciones=None):
    config = {**SearchConfig, **(opciones or {})}
    return {
        'matches': [],    # Array de coincidencias
        'total': 0,       # Número total
        'positions': [],  # Posiciones [start, end]
        'highlighted': '',# Texto con resaltado
        'stats': {},      # Estadísticas
    }
```

### Paso 3: Construir el Patrón

**JavaScript:**
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

**Python:**
```python
import re

def build_pattern(query, config):
    pattern = re.escape(query)
    if config['wholeWord']:
        pattern = rf'\b{pattern}\b'
    flags = 0  # Siempre global en findall/finditer
    if not config['caseSensitive']:
        flags |= re.IGNORECASE
    if config['multiline']:
        flags |= re.MULTILINE
    if config['dotAll']:
        flags |= re.DOTALL
    return re.compile(pattern, flags)
```

### Paso 4: Resaltador de Texto

**JavaScript:**
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

**Python:**
```python
def highlight(texto, pattern):
    return pattern.sub(r'[[MATCH]]\g<0>[[/MATCH]]', texto)
```

### Paso 5: Búsqueda Avanzada

**JavaScript:**
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

**Python:**
```python
def busqueda_avanzada(texto, query_string):
    # Tu implementación
    pass
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
├── buscador.js                   (solución JavaScript)
├── buscador.py                   (solución Python)
├── test-buscador.js              (tests JavaScript)
├── test_buscador.py              (tests Python)
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

**Solución JavaScript:** Disponible en `solucion-proyecto-06.js`
**Solución Python:** Disponible en `solucion-proyecto-06.py`
