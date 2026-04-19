/**
 * ============================================
 * Solución: Proyecto Semana 07
 * Linter de Código Simple
 * ============================================
 */

// ============================================
// TIPOS
// ============================================

/**
 * @typedef {Object} Rule
 * @property {string} id - Identificador único
 * @property {string} description - Descripción del problema
 * @property {"error"|"warning"|"info"} severity - Severidad
 * @property {RegExp} pattern - Patrón para detectar
 * @property {function} [fix] - Función de corrección
 */

/**
 * @typedef {Object} LintResult
 * @property {string} ruleId
 * @property {string} message
 * @property {"error"|"warning"|"info"} severity
 * @property {number} line
 * @property {number} column
 * @property {string} source
 */

// ============================================
// REGLAS
// ============================================

const rules = {
  /**
   * Regla: no-console
   *
   * ¿Por qué? console.log no debe estar en producción
   * ¿Para qué? Código limpio y sin logs de debug
   */
  'no-console': {
    id: 'no-console',
    description: 'Unexpected console statement',
    severity: 'warning',
    pattern: /\bconsole\.(log|warn|error|info|debug|trace)\s*\(/g,
    // Excluir comentarios se maneja en el linter
  },

  /**
   * Regla: eqeqeq
   *
   * ¿Por qué? == hace coerción de tipos
   * ¿Para qué? Comparaciones predecibles
   */
  eqeqeq: {
    id: 'eqeqeq',
    description: "Expected '===' but found '=='",
    severity: 'error',
    // Negative lookbehind: no ! antes
    // Negative lookahead: no = después, no null
    pattern: /(?<![!=])={2}(?!=)/g,
    fix: (match) => match.replace('==', '==='),
  },

  /**
   * Regla: no-neq
   *
   * ¿Por qué? != hace coerción de tipos
   * ¿Para qué? Comparaciones predecibles
   */
  'no-neq': {
    id: 'no-neq',
    description: "Expected '!==' but found '!='",
    severity: 'error',
    pattern: /!=(?!=)/g,
    fix: (match) => match.replace('!=', '!=='),
  },

  /**
   * Regla: no-magic-numbers
   *
   * ¿Por qué? Números sin contexto son difíciles de entender
   * ¿Para qué? Código más legible
   */
  'no-magic-numbers': {
    id: 'no-magic-numbers',
    description: 'Magic number detected',
    severity: 'warning',
    // Números que no son 0, 1, -1, 2
    // En contexto de operación
    pattern: /(?<=[+\-*/%<>=])\s*(?!0|1|-1|2)\d{2,}(?!\d)/g,
  },

  /**
   * Regla: no-todo
   *
   * ¿Por qué? TODOs pendientes indican trabajo incompleto
   * ¿Para qué? Tracking de deuda técnica
   */
  'no-todo': {
    id: 'no-todo',
    description: 'Unresolved TODO/FIXME comment',
    severity: 'info',
    pattern: /\/\/\s*(TODO|FIXME|HACK|XXX):?\s*.*/gi,
  },

  /**
   * Regla: no-eval
   *
   * ¿Por qué? eval() es peligroso y lento
   * ¿Para qué? Seguridad del código
   */
  'no-eval': {
    id: 'no-eval',
    description: 'Dangerous use of eval() or similar',
    severity: 'error',
    pattern: /\b(eval|Function)\s*\(|setTimeout\s*\(\s*["'`]/g,
  },

  /**
   * Regla: max-line-length
   *
   * ¿Por qué? Líneas largas son difíciles de leer
   * ¿Para qué? Legibilidad
   */
  'max-line-length': {
    id: 'max-line-length',
    description: 'Line exceeds maximum length',
    severity: 'warning',
    maxLength: 120,
    // Pattern generado dinámicamente
  },

  /**
   * Regla: no-debugger
   *
   * ¿Por qué? debugger no debe estar en producción
   * ¿Para qué? Código limpio
   */
  'no-debugger': {
    id: 'no-debugger',
    description: 'Unexpected debugger statement',
    severity: 'error',
    pattern: /\bdebugger\b/g,
  },

  /**
   * Regla: no-alert
   *
   * ¿Por qué? alert() bloquea la UI
   * ¿Para qué? Mejor UX
   */
  'no-alert': {
    id: 'no-alert',
    description: 'Unexpected alert statement',
    severity: 'warning',
    pattern: /\b(alert|confirm|prompt)\s*\(/g,
  },

  /**
   * Regla: no-var
   *
   * ¿Por qué? var tiene scoping problemático
   * ¿Para qué? Usar let/const es mejor práctica
   */
  'no-var': {
    id: 'no-var',
    description: 'Unexpected var, use let or const instead',
    severity: 'warning',
    pattern: /\bvar\s+\w+/g,
    fix: (match) => match.replace('var', 'let'),
  },
};

// ============================================
// UTILIDADES
// ============================================

/**
 * Obtener posición (línea y columna) desde índice
 *
 * @param {string} code - Código fuente
 * @param {number} index - Índice del match
 * @returns {{line: number, column: number}}
 */
function getPosition(code, index) {
  const before = code.slice(0, index);
  const lines = before.split('\n');
  return {
    line: lines.length,
    column: lines[lines.length - 1].length + 1,
  };
}

/**
 * Verificar si posición está en comentario
 *
 * @param {string} code - Código fuente
 * @param {number} index - Índice a verificar
 * @returns {boolean}
 */
function isInComment(code, index) {
  // Buscar // antes en la misma línea
  const lineStart = code.lastIndexOf('\n', index) + 1;
  const beforeOnLine = code.slice(lineStart, index);

  if (beforeOnLine.includes('//')) {
    return true;
  }

  // Buscar /* ... */ que contenga el índice
  const beforeMatch = code.slice(0, index);
  const lastOpen = beforeMatch.lastIndexOf('/*');
  const lastClose = beforeMatch.lastIndexOf('*/');

  return lastOpen > lastClose;
}

/**
 * Verificar si posición está en string
 *
 * @param {string} code - Código fuente
 * @param {number} index - Índice a verificar
 * @returns {boolean}
 */
function isInString(code, index) {
  // Simplificado: contar comillas antes
  const before = code.slice(0, index);

  // Contar comillas no escapadas
  const singleQuotes = (before.match(/(?<!\\)'/g) || []).length;
  const doubleQuotes = (before.match(/(?<!\\)"/g) || []).length;
  const backticks = (before.match(/(?<!\\)`/g) || []).length;

  return (
    singleQuotes % 2 === 1 || doubleQuotes % 2 === 1 || backticks % 2 === 1
  );
}

/**
 * Verificar si hay ignore comment antes
 *
 * @param {string} code - Código fuente
 * @param {number} line - Número de línea
 * @returns {boolean}
 */
function hasIgnoreComment(code, line) {
  const lines = code.split('\n');
  if (line < 2) return false;

  const prevLine = lines[line - 2]; // line es 1-based
  return /\/\/\s*linter-ignore-next-line/.test(prevLine);
}

// ============================================
// LINTER
// ============================================

/**
 * Linter principal
 *
 * @param {string} code - Código a analizar
 * @param {Object} options - Configuración
 * @returns {LintResult[]}
 */
function lint(code, options = {}) {
  const results = [];
  const enabledRules = options.rules || Object.keys(rules);
  const lines = code.split('\n');

  // Aplicar cada regla
  for (const ruleId of enabledRules) {
    const rule = rules[ruleId];
    if (!rule) continue;

    // Regla especial: max-line-length
    if (ruleId === 'max-line-length') {
      const maxLength = options.maxLineLength || rule.maxLength;

      lines.forEach((line, idx) => {
        if (line.length > maxLength) {
          const lineNum = idx + 1;
          if (!hasIgnoreComment(code, lineNum)) {
            results.push({
              ruleId: rule.id,
              message: `${rule.description} (${line.length} > ${maxLength})`,
              severity: rule.severity,
              line: lineNum,
              column: maxLength + 1,
              source: line.slice(0, 50) + '...',
            });
          }
        }
      });
      continue;
    }

    // Reglas con patrón
    if (!rule.pattern) continue;

    // Reset pattern
    rule.pattern.lastIndex = 0;

    let match;
    while ((match = rule.pattern.exec(code)) !== null) {
      const index = match.index;

      // Ignorar si está en comentario o string (según regla)
      if (
        [
          'no-console',
          'no-eval',
          'no-alert',
          'no-debugger',
          'no-var',
          'eqeqeq',
          'no-neq',
        ].includes(ruleId)
      ) {
        if (isInComment(code, index) || isInString(code, index)) {
          continue;
        }
      }

      const pos = getPosition(code, index);

      // Verificar ignore comment
      if (hasIgnoreComment(code, pos.line)) {
        continue;
      }

      // Obtener línea fuente
      const sourceLine = lines[pos.line - 1];

      results.push({
        ruleId: rule.id,
        message: rule.description,
        severity: rule.severity,
        line: pos.line,
        column: pos.column,
        source: sourceLine.trim(),
        match: match[0],
      });
    }
  }

  // Ordenar por línea
  results.sort((a, b) => a.line - b.line || a.column - b.column);

  return results;
}

// ============================================
// FORMATEO
// ============================================

/**
 * Formatear resultados para consola
 *
 * @param {LintResult[]} results - Resultados del linter
 * @param {string} filename - Nombre del archivo
 * @returns {string}
 */
function formatResults(results, filename = 'input.js') {
  if (results.length === 0) {
    return `✓ ${filename}: No problems found`;
  }

  const lines = [`\n${filename}`];

  const severityColors = {
    error: '🔴',
    warning: '🟡',
    info: '🔵',
  };

  for (const result of results) {
    const icon = severityColors[result.severity];
    const location = `${result.line}:${result.column}`.padEnd(8);
    const severity = result.severity.padEnd(8);
    const message = result.message.padEnd(40);
    const rule = result.ruleId;

    lines.push(`  ${location} ${icon} ${severity} ${message} ${rule}`);
  }

  const errors = results.filter((r) => r.severity === 'error').length;
  const warnings = results.filter((r) => r.severity === 'warning').length;

  lines.push('');
  lines.push(
    `✖ ${results.length} problems (${errors} errors, ${warnings} warnings)`
  );

  return lines.join('\n');
}

/**
 * Formatear resultados como JSON
 */
function formatJSON(results, filename) {
  return JSON.stringify(
    {
      filename,
      problems: results,
      summary: {
        total: results.length,
        errors: results.filter((r) => r.severity === 'error').length,
        warnings: results.filter((r) => r.severity === 'warning').length,
        info: results.filter((r) => r.severity === 'info').length,
      },
    },
    null,
    2
  );
}

// ============================================
// AUTO-FIX
// ============================================

/**
 * Aplicar correcciones automáticas
 *
 * @param {string} code - Código original
 * @param {LintResult[]} results - Resultados del linter
 * @returns {{code: string, fixed: number}}
 */
function autoFix(code, results) {
  let fixed = 0;
  let newCode = code;

  // Solo aplicar fixes para reglas que tienen fix
  const fixableRules = ['eqeqeq', 'no-neq', 'no-var'];

  for (const ruleId of fixableRules) {
    const rule = rules[ruleId];
    if (!rule || !rule.fix) continue;

    // Reset pattern
    rule.pattern.lastIndex = 0;

    newCode = newCode.replace(rule.pattern, (match, ...args) => {
      // Verificar que no esté en comentario/string
      const offset = args[args.length - 2]; // penúltimo arg es offset
      if (isInComment(code, offset) || isInString(code, offset)) {
        return match;
      }
      fixed++;
      return rule.fix(match);
    });
  }

  return { code: newCode, fixed };
}

// ============================================
// DEMO
// ============================================

const testCode = `
// TODO: Refactor this function
function calculateTotal(items) {
  var total = 0;
  
  for (var i = 0; i < items.length; i++) {
    if (items[i].price == null) {
      continue;
    }
    
    total = total + items[i].price * 1.21; // Magic number: tax
    
    console.log("Item:", items[i]);
  }
  
  if (total != 0) {
    // linter-ignore-next-line
    console.log("Total:", total);
  }
  
  debugger;
  
  eval("alert('done')");
  
  return total;
}

// This line is intentionally very long to trigger the max-line-length rule because it exceeds one hundred twenty characters
`;

console.log('=== Linter Demo ===\n');
console.log('Input Code:');
console.log('-'.repeat(50));
console.log(testCode);
console.log('-'.repeat(50));

const results = lint(testCode);
console.log(formatResults(results, 'demo.js'));

console.log('\n\n=== Auto-Fix Demo ===\n');
const { code: fixedCode, fixed } = autoFix(testCode, results);
console.log(`Fixed ${fixed} problems`);
console.log('-'.repeat(50));
console.log(fixedCode);
console.log('-'.repeat(50));

// Verificar mejoras
const newResults = lint(fixedCode);
console.log(`\nProblems: ${results.length} → ${newResults.length}`);

// ============================================
// EXPORTS
// ============================================

// Para uso como módulo:
// module.exports = { lint, formatResults, formatJSON, autoFix, rules };
