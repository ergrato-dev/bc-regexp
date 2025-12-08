/**
 * ============================================
 * Solución: Proyecto Semana 06
 * Buscador de Texto Avanzado
 * ============================================
 */

// ============================================
// CONFIGURACIÓN
// ============================================

const SearchConfig = {
  caseSensitive: false,
  wholeWord: false,
  multiline: true,
  dotAll: false,
  unicode: true,
  showIndices: true,
};

// ============================================
// UTILIDADES
// ============================================

/**
 * Escapar caracteres especiales de regex
 *
 * ¿Por qué? Los caracteres como . * + tienen significado especial
 * ¿Para qué? Buscar literalmente el texto del usuario
 */
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Construir string de flags según configuración
 *
 * @param {object} config - Configuración de búsqueda
 * @returns {string} Flags para regex
 */
function buildFlags(config) {
  let flags = 'g'; // Siempre global

  if (!config.caseSensitive) flags += 'i';
  if (config.multiline) flags += 'm';
  if (config.dotAll) flags += 's';
  if (config.unicode) flags += 'u';
  if (config.showIndices) flags += 'd';

  return flags;
}

/**
 * Construir patrón regex
 *
 * @param {string} query - Término de búsqueda
 * @param {object} config - Configuración
 * @returns {RegExp} Expresión regular
 */
function buildPattern(query, config) {
  let pattern = escapeRegExp(query);

  if (config.wholeWord) {
    // \b para límites de palabra
    pattern = `\\b${pattern}\\b`;
  }

  const flags = buildFlags(config);

  return new RegExp(pattern, flags);
}

// ============================================
// MOTOR DE BÚSQUEDA
// ============================================

/**
 * Motor de búsqueda principal
 *
 * ¿Por qué? Centralizar toda la lógica de búsqueda
 * ¿Para qué? Reutilización y mantenibilidad
 *
 * @param {string} texto - Texto donde buscar
 * @param {string} query - Término de búsqueda
 * @param {object} opciones - Configuración
 * @returns {object} Resultados
 */
function buscar(texto, query, opciones = {}) {
  const config = { ...SearchConfig, ...opciones };

  if (!query || !texto) {
    return {
      matches: [],
      total: 0,
      positions: [],
      highlighted: texto || '',
      stats: { duration: 0 },
    };
  }

  const startTime = performance.now();

  try {
    const pattern = buildPattern(query, config);
    const matches = [];
    const positions = [];

    // Usar matchAll para obtener toda la info
    for (const match of texto.matchAll(pattern)) {
      matches.push(match[0]);

      if (config.showIndices && match.indices) {
        positions.push({
          start: match.indices[0][0],
          end: match.indices[0][1],
          value: match[0],
        });
      } else {
        positions.push({
          start: match.index,
          end: match.index + match[0].length,
          value: match[0],
        });
      }
    }

    const highlighted = highlight(texto, pattern);
    const duration = performance.now() - startTime;

    return {
      matches,
      total: matches.length,
      positions,
      highlighted,
      stats: {
        duration: duration.toFixed(2) + 'ms',
        textLength: texto.length,
        pattern: pattern.toString(),
      },
    };
  } catch (error) {
    return {
      matches: [],
      total: 0,
      positions: [],
      highlighted: texto,
      stats: { error: error.message },
    };
  }
}

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

/**
 * Convertir marcadores a HTML
 */
function highlightToHTML(texto) {
  return texto
    .replace(/\[\[MATCH\]\]/g, '<mark class="highlight">')
    .replace(/\[\[\/MATCH\]\]/g, '</mark>');
}

// ============================================
// BÚSQUEDA AVANZADA
// ============================================

/**
 * Parsear query con sintaxis avanzada
 *
 * Soporta:
 * - "frase exacta"
 * - palabra1 palabra2 (AND implícito)
 * - palabra1 OR palabra2
 * - -excluir
 * - palabra* (wildcard)
 *
 * @param {string} queryString - Query del usuario
 * @returns {object} Componentes parseados
 */
function parseQuery(queryString) {
  const parts = {
    exact: [],
    include: [],
    exclude: [],
    wildcard: [],
    or: [],
  };

  let remaining = queryString;

  // 1. Extraer frases exactas "..."
  const exactPattern = /"([^"]+)"/g;
  for (const match of remaining.matchAll(exactPattern)) {
    parts.exact.push(match[1]);
  }
  remaining = remaining.replace(exactPattern, ' ');

  // 2. Extraer exclusiones -palabra
  const excludePattern = /-(\w+)/g;
  for (const match of remaining.matchAll(excludePattern)) {
    parts.exclude.push(match[1]);
  }
  remaining = remaining.replace(excludePattern, ' ');

  // 3. Extraer wildcards palabra*
  const wildcardPattern = /(\w+)\*/g;
  for (const match of remaining.matchAll(wildcardPattern)) {
    parts.wildcard.push(match[1]);
  }
  remaining = remaining.replace(wildcardPattern, ' ');

  // 4. Procesar OR
  const orPattern = /(\w+)\s+OR\s+(\w+)/gi;
  for (const match of remaining.matchAll(orPattern)) {
    parts.or.push([match[1], match[2]]);
  }
  remaining = remaining.replace(orPattern, ' ');

  // 5. El resto son palabras a incluir (AND)
  const words = remaining.trim().split(/\s+/).filter(Boolean);
  parts.include.push(...words);

  return parts;
}

/**
 * Búsqueda avanzada con sintaxis especial
 *
 * @param {string} texto - Texto donde buscar
 * @param {string} queryString - Query con sintaxis
 * @param {object} opciones - Configuración base
 * @returns {object} Resultados
 */
function busquedaAvanzada(texto, queryString, opciones = {}) {
  const config = { ...SearchConfig, ...opciones };
  const parsed = parseQuery(queryString);
  const resultados = [];
  let textoFiltrado = texto;

  // Verificar exclusiones primero
  for (const excluir of parsed.exclude) {
    const pattern = new RegExp(`\\b${escapeRegExp(excluir)}\\b`, 'gi');
    if (pattern.test(texto)) {
      // Si contiene palabra excluida, podría filtrar líneas
      const lineas = texto.split('\n');
      textoFiltrado = lineas.filter((linea) => !pattern.test(linea)).join('\n');
    }
  }

  // Buscar frases exactas
  for (const frase of parsed.exact) {
    const resultado = buscar(textoFiltrado, frase, config);
    if (resultado.total > 0) {
      resultados.push({
        type: 'exact',
        query: frase,
        ...resultado,
      });
    }
  }

  // Buscar wildcards
  for (const base of parsed.wildcard) {
    const pattern = new RegExp(`\\b${escapeRegExp(base)}\\w*\\b`, 'gi');
    const matches = textoFiltrado.match(pattern) || [];
    resultados.push({
      type: 'wildcard',
      query: base + '*',
      matches: [...new Set(matches)],
      total: matches.length,
    });
  }

  // Buscar OR
  for (const [a, b] of parsed.or) {
    const pattern = new RegExp(
      `\\b(?:${escapeRegExp(a)}|${escapeRegExp(b)})\\b`,
      'gi'
    );
    const matches = textoFiltrado.match(pattern) || [];
    resultados.push({
      type: 'or',
      query: `${a} OR ${b}`,
      matches,
      total: matches.length,
    });
  }

  // Buscar palabras individuales (AND)
  for (const palabra of parsed.include) {
    const resultado = buscar(textoFiltrado, palabra, {
      ...config,
      wholeWord: true,
    });
    if (resultado.total > 0) {
      resultados.push({
        type: 'include',
        query: palabra,
        ...resultado,
      });
    }
  }

  // Verificar que todas las palabras include estén presentes (AND)
  const todasPresentes = parsed.include.every((palabra) => {
    const pattern = new RegExp(`\\b${escapeRegExp(palabra)}\\b`, 'gi');
    return pattern.test(textoFiltrado);
  });

  return {
    parsed,
    resultados,
    todasPresentes,
    textoFiltrado,
  };
}

// ============================================
// UTILIDADES ADICIONALES
// ============================================

/**
 * Obtener contexto alrededor de un match
 *
 * @param {string} texto - Texto completo
 * @param {number} posicion - Posición del match
 * @param {number} caracteres - Caracteres de contexto
 * @returns {string} Fragmento con contexto
 */
function getContexto(texto, posicion, caracteres = 50) {
  const start = Math.max(0, posicion - caracteres);
  const end = Math.min(texto.length, posicion + caracteres);

  let contexto = texto.slice(start, end);

  if (start > 0) contexto = '...' + contexto;
  if (end < texto.length) contexto = contexto + '...';

  return contexto;
}

/**
 * Obtener líneas alrededor de un match
 *
 * @param {string} texto - Texto completo
 * @param {number} posicion - Posición del match
 * @param {number} lineas - Líneas de contexto
 * @returns {object} Líneas con contexto
 */
function getLineasContexto(texto, posicion, lineas = 2) {
  const todasLineas = texto.split('\n');

  // Encontrar número de línea
  let charCount = 0;
  let lineaActual = 0;

  for (let i = 0; i < todasLineas.length; i++) {
    charCount += todasLineas[i].length + 1; // +1 por \n
    if (charCount > posicion) {
      lineaActual = i;
      break;
    }
  }

  const inicio = Math.max(0, lineaActual - lineas);
  const fin = Math.min(todasLineas.length, lineaActual + lineas + 1);

  return {
    lineas: todasLineas.slice(inicio, fin),
    numeroLineaMatch: lineaActual,
    rango: [inicio, fin],
  };
}

// ============================================
// TESTS
// ============================================

const textoEjemplo = `JavaScript es un lenguaje de programación.
JavaScript se usa para desarrollo web.
También se usa en Node.js para backend.
Python es otro lenguaje popular.
javascript puede ejecutarse en el navegador.
Los frameworks como React usan JavaScript.`;

console.log('=== Búsqueda Simple ===\n');

const resultado1 = buscar(textoEjemplo, 'JavaScript');
console.log("Buscar 'JavaScript':", resultado1.total, 'coincidencias');
console.log('Matches:', resultado1.matches);

console.log('\n=== Búsqueda Case-Sensitive ===\n');

const resultado2 = buscar(textoEjemplo, 'JavaScript', { caseSensitive: true });
console.log("Buscar 'JavaScript' (case-sensitive):", resultado2.total);

const resultado3 = buscar(textoEjemplo, 'javascript', { caseSensitive: true });
console.log("Buscar 'javascript' (case-sensitive):", resultado3.total);

console.log('\n=== Búsqueda Palabra Completa ===\n');

const resultado4 = buscar(textoEjemplo, 'Java', { wholeWord: true });
console.log("Buscar 'Java' (whole word):", resultado4.total);

const resultado5 = buscar(textoEjemplo, 'Java', { wholeWord: false });
console.log("Buscar 'Java' (parcial):", resultado5.total);

console.log('\n=== Búsqueda Avanzada ===\n');

const query1 = '"desarrollo web" JavaScript -Python';
console.log(`Query: ${query1}`);
console.log(busquedaAvanzada(textoEjemplo, query1));

console.log('\n=== Contexto de Matches ===\n');

const resultado6 = buscar(textoEjemplo, 'Node.js');
if (resultado6.positions.length > 0) {
  const pos = resultado6.positions[0].start;
  console.log('Contexto:', getContexto(textoEjemplo, pos, 30));
  console.log('Líneas:', getLineasContexto(textoEjemplo, pos, 1));
}

console.log('\n=== Unicode ===\n');

const textoUnicode = 'Hola 👋 mundo! Привет мир! 你好世界!';
const resultado7 = buscar(textoUnicode, 'мир', { unicode: true });
console.log("Buscar 'мир' en texto Unicode:", resultado7);
