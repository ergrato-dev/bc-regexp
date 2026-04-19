# Proyecto Semana 07: Linter de Código Simple

## 🎯 Objetivo

Crear un **linter de código** que use expresiones regulares avanzadas para detectar problemas comunes en código JavaScript.

## 📋 Descripción

Construirás una herramienta que analice código JavaScript y detecte:

- Errores de estilo
- Patrones problemáticos
- Código potencialmente peligroso
- Malas prácticas comunes

## 🛠️ Instrucciones

### Paso 1: Estructura del Linter

```javascript
/**
 * Regla del linter
 */
const Rule = {
  id: '', // Identificador único
  description: '', // Descripción del problema
  severity: '', // "error" | "warning" | "info"
  pattern: null, // RegExp para detectar
  fix: null, // Función de corrección (opcional)
};

/**
 * Resultado de análisis
 */
const LintResult = {
  ruleId: '',
  message: '',
  severity: '',
  line: 0,
  column: 0,
  source: '',
};
```

### Paso 2: Reglas a Implementar

#### Regla 1: Variables no usadas (simplificado)

```javascript
// Detectar: var, let, const sin uso posterior
// Patrón: declaración al inicio de línea sin uso
```

#### Regla 2: console.log en producción

```javascript
// Detectar: console.log, console.warn, console.error
// Excepto: en comentarios
```

#### Regla 3: == en lugar de ===

```javascript
// Detectar: == o != (no estrictos)
// Excepto: comparación con null
```

#### Regla 4: Números mágicos

```javascript
// Detectar: números literales excepto 0, 1, -1
// En: operaciones aritméticas
```

#### Regla 5: TODO/FIXME sin resolver

```javascript
// Detectar: TODO, FIXME, HACK, XXX en comentarios
```

#### Regla 6: Funciones muy largas

```javascript
// Detectar: funciones con más de N líneas
// Default: 50 líneas
```

#### Regla 7: Líneas muy largas

```javascript
// Detectar: líneas con más de N caracteres
// Default: 120 caracteres
```

#### Regla 8: eval() y Function()

```javascript
// Detectar: uso de eval, new Function, setTimeout(string)
```

### Paso 3: Motor del Linter

```javascript
/**
 * Linter principal
 *
 * @param {string} code - Código a analizar
 * @param {object} options - Configuración
 * @returns {LintResult[]} Problemas encontrados
 */
function lint(code, options = {}) {
  const results = [];
  const lines = code.split('\n');

  // Tu implementación

  return results;
}
```

### Paso 4: Reporte de Resultados

```javascript
/**
 * Formatear resultados para consola
 */
function formatResults(results, filename) {
  // Formato:
  // filename.js
  //   10:5  error  Unexpected console.log  no-console
  //   15:8  warn   Magic number: 42        no-magic-numbers
}
```

## 💡 Hints

<details>
<summary>Hint: Detectar console.log (no en comentarios)</summary>

```javascript
const consolePattern =
  /^(?!.*\/\/.*console)(?!.*\/\*[\s\S]*console[\s\S]*\*\/).*\bconsole\.(log|warn|error|info)\b/gm;
```

</details>

<details>
<summary>Hint: Detectar == no estricto</summary>

```javascript
// Detectar == pero no === ni !== ni ==null
const equalityPattern = /(?<![!=])={2}(?!=)(?!\s*null)/g;
```

</details>

<details>
<summary>Hint: Encontrar línea y columna</summary>

```javascript
function getPosition(code, index) {
  const before = code.slice(0, index);
  const lines = before.split('\n');
  return {
    line: lines.length,
    column: lines[lines.length - 1].length + 1,
  };
}
```

</details>

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-07-linter.md      (este archivo)
├── linter.js                   (tu solución)
├── rules/                      (reglas individuales)
│   ├── no-console.js
│   ├── eqeqeq.js
│   └── ...
├── test-files/                 (archivos para probar)
│   ├── bad-code.js
│   └── good-code.js
└── demo.js                     (demo de uso)
```

## ✅ Criterios de Evaluación

| Criterio                           | Puntos |
| ---------------------------------- | ------ |
| Detectar console.log correctamente | 15%    |
| Detectar == vs ===                 | 15%    |
| Detectar números mágicos           | 15%    |
| Detectar TODO/FIXME                | 10%    |
| Detectar eval()                    | 15%    |
| Reportar línea y columna           | 15%    |
| Formateo de resultados             | 15%    |

## 🚀 Extensiones

### Extensión 1: Auto-fix

```javascript
// Corregir automáticamente problemas simples
function fix(code, results) {
  // == → ===
  // console.log → // console.log
}
```

### Extensión 2: Configuración por archivo

```javascript
// .lintrc.json
{
  "rules": {
    "no-console": "warn",
    "eqeqeq": "error",
    "max-line-length": ["error", 100]
  }
}
```

### Extensión 3: Ignore patterns

```javascript
// Ignorar líneas con comentario especial
// linter-ignore-next-line
console.log('Esto está permitido');
```

---

**Solución:** Disponible en `solucion-proyecto-07.js`
