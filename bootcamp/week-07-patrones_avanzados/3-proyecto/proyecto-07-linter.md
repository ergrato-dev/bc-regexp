# Proyecto Semana 07: Linter de Código Simple

> **Lenguaje:** Elige **JavaScript** o **Python** para tu implementación.
> - **JavaScript:** El linter analiza código JavaScript (detecta `console.log`, `==` vs `===`, `eval()`, etc.)
> - **Python:** El linter analiza código Python (detecta `print()` en producción, `is` vs `==`, `eval()`/`exec()`, etc.)
> - Las regex y la estructura del linter son las mismas; solo cambian las reglas según el lenguaje objetivo.

## 🎯 Objetivo

Crear un **linter de código** que use expresiones regulares avanzadas para detectar problemas comunes en código.

## 📋 Descripción

Construirás una herramienta que analice código JavaScript y detecte:

- Errores de estilo
- Patrones problemáticos
- Código potencialmente peligroso
- Malas prácticas comunes

## 🛠️ Instrucciones

### Paso 1: Estructura del Linter

**JavaScript:**
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

**Python:**
```python
import re

# Regla del linter
class Rule:
    def __init__(self, id, description, severity, pattern, fix=None):
        self.id = id
        self.description = description
        self.severity = severity  # "error" | "warning" | "info"
        self.pattern = pattern    # re.compile(...)
        self.fix = fix            # Función de corrección (opcional)

# Resultado de análisis
class LintResult:
    def __init__(self, rule_id, message, severity, line, column, source):
        self.ruleId = rule_id
        self.message = message
        self.severity = severity
        self.line = line
        self.column = column
        self.source = source
```

### Paso 2: Reglas a Implementar

> **JavaScript:** Reglas para JS | **Python:** Reglas para Python (adaptadas al lenguaje)

#### Regla 1: console.log / print en producción

**JavaScript:**
```javascript
// Detectar: console.log, console.warn, console.error
// Excepto: en comentarios
```

**Python:**
```python
# Detectar: print() en código de producción
# Excepto: en comentarios o docstrings
```

#### Regla 2: == en lugar de === (JS) / is vs == (Python)

**JavaScript:**
```javascript
// Detectar: == o != (no estrictos)
// Excepto: comparación con null
```

**Python:**
```python
# Detectar: == None en lugar de is None, == True/False
# Sugerir: usar is None, is True, is False
```

#### Regla 3: Números mágicos

**JavaScript:**
```javascript
// Detectar: números literales excepto 0, 1, -1
// En: operaciones aritméticas
```

**Python:**
```python
# Detectar: números literales excepto 0, 1, -1
# En: operaciones aritméticas y comparaciones
```

#### Regla 4: TODO/FIXME sin resolver

**JavaScript:**
```javascript
// Detectar: TODO, FIXME, HACK, XXX en comentarios
```

**Python:**
```python
# Detectar: TODO, FIXME, HACK, XXX en comentarios
```

#### Regla 5: Funciones muy largas

```javascript
// Detectar: funciones con más de N líneas
// Default: 50 líneas
```

**Python:**
```python
# Detectar: funciones (def) con más de N líneas
# Default: 50 líneas
```

#### Regla 6: Líneas muy largas

```javascript
// Detectar: líneas con más de N caracteres
// Default: 120 caracteres
```

**Python:**
```python
# Detectar: líneas con más de N caracteres
# Default: 120 caracteres (PEP 8 recomienda 79)
```

#### Regla 7: eval() y código dinámico peligroso

**JavaScript:**
```javascript
// Detectar: uso de eval, new Function, setTimeout(string)
```

**Python:**
```python
# Detectar: uso de eval(), exec(), compile(), __import__()
```

### Paso 3: Motor del Linter

**JavaScript:**
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

**Python:**
```python
def lint(code, options=None):
    """Linter principal.
    Args:
        code: Código Python a analizar.
        options: Diccionario de configuración.
    Returns:
        Lista de LintResult con los problemas encontrados.
    """
    results = []
    lines = code.split('\n')
    # Tu implementación
    return results
```

### Paso 4: Reporte de Resultados

**JavaScript:**
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

**Python:**
```python
def format_results(results, filename):
    """Formatear resultados para consola.
    Formato:
        filename.py
          10:5  error  Unexpected print() call  no-print
          15:8  warn   Magic number: 42         no-magic-numbers
    """
    pass
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
├── linter.js                   (solución JavaScript)
├── linter.py                   (solución Python)
├── rules/                      (reglas individuales)
│   ├── no-console.js
│   ├── no-print.py
│   └── ...
├── test-files/                 (archivos para probar)
│   ├── bad-code.js
│   ├── bad_code.py
│   ├── good-code.js
│   └── good_code.py
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

**Solución JavaScript:** Disponible en `solucion-proyecto-07.js`
**Solución Python:** Disponible en `solucion-proyecto-07.py`
