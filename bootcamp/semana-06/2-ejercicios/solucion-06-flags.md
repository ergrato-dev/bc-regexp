# Soluciones - Semana 06: Flags y Modificadores

## Ejercicio 1: Contador de Palabras

```javascript
/**
 * Contar ocurrencias de una palabra (case-insensitive)
 *
 * ¿Por qué? Los usuarios escriben con diferente capitalización
 * ¿Para qué? Análisis de frecuencia de términos
 *
 * Flags:
 * g - encontrar todas las coincidencias
 * i - ignorar mayúsculas/minúsculas
 */

const texto = `JavaScript is a programming language. javascript is used for web development.
Many developers love JavaScript. JAVASCRIPT powers many websites.`;

function contarPalabra(texto, palabra) {
  // Escapar caracteres especiales de regex
  const escapada = palabra.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // Crear patrón con word boundaries
  const pattern = new RegExp(`\\b${escapada}\\b`, 'gi');

  const matches = texto.match(pattern);
  return matches ? matches.length : 0;
}

console.log(contarPalabra(texto, 'javascript')); // 4
console.log(contarPalabra(texto, 'is')); // 2
console.log(contarPalabra(texto, 'PYTHON')); // 0
```

---

## Ejercicio 2: Extraer Comentarios Multilínea

```javascript
/**
 * Extraer comentarios /* ... * / que cruzan líneas
 *
 * ¿Por qué? Los comentarios pueden ocupar múltiples líneas
 * ¿Para qué? Documentación, parsing de código
 *
 * Flags:
 * g - encontrar todos
 * s - hacer que . incluya \n
 */

const codigo = `const x = 1;
/* Este es un
   comentario
   multilínea */
const y = 2;
/* Otro comentario */
const z = 3;`;

// Con flag s (ES2018+)
const patternModerno = /\/\*.*?\*\//gs;

// Sin flag s (compatibilidad)
const patternCompat = /\/\*[\s\S]*?\*\//g;

console.log(codigo.match(patternModerno));
// [
//   '/* Este es un\n   comentario\n   multilínea */',
//   '/* Otro comentario */'
// ]

// Función para extraer solo el contenido (sin /* */)
function extraerComentarios(code) {
  const pattern = /\/\*(.*?)\*\//gs;
  const comentarios = [];

  for (const match of code.matchAll(pattern)) {
    comentarios.push(match[1].trim());
  }

  return comentarios;
}

console.log(extraerComentarios(codigo));
// ['Este es un\n   comentario\n   multilínea', 'Otro comentario']
```

---

## Ejercicio 3: Procesar Archivo de Configuración

```javascript
/**
 * Parsear archivo de configuración clave=valor
 *
 * ¿Por qué? Los archivos config tienen líneas independientes
 * ¿Para qué? Cargar configuración de aplicaciones
 *
 * Flags:
 * g - procesar todas las líneas
 * m - ^ y $ aplican a cada línea
 */

const config = `# Configuración de la app
nombre=MiApp
version=1.0.0
# Puerto del servidor
puerto=3000
debug=true`;

/**
 * Desglose del patrón:
 * ^           → Inicio de línea (con flag m)
 * (?!#)       → Negative lookahead: no empieza con #
 * (\w+)       → Grupo 1: clave
 * =           → Separador
 * (.+)        → Grupo 2: valor
 * $           → Fin de línea (con flag m)
 */
const pattern = /^(?!#)(\w+)=(.+)$/gm;

function parseConfig(texto) {
  const config = {};

  for (const match of texto.matchAll(pattern)) {
    config[match[1]] = match[2];
  }

  return config;
}

console.log(parseConfig(config));
// {
//   nombre: 'MiApp',
//   version: '1.0.0',
//   puerto: '3000',
//   debug: 'true'
// }
```

---

## Ejercicio 4: Validar Texto Internacional

```javascript
/**
 * Validar nombres en cualquier idioma
 *
 * ¿Por qué? Los nombres pueden estar en cualquier script
 * ¿Para qué? Formularios internacionales
 *
 * Flags:
 * u - habilitar propiedades Unicode
 */

const nombres = [
  'José García',
  '北京市',
  'Москва',
  'محمد أحمد',
  'João',
  '123Invalid',
  '',
];

/**
 * Desglose:
 * ^                → Inicio
 * [\p{Letter}\s]+  → Una o más letras (cualquier idioma) o espacios
 * $                → Fin
 */
const pattern = /^[\p{Letter}\s]+$/u;

function validarNombre(nombre) {
  if (!nombre) return false;
  return pattern.test(nombre);
}

nombres.forEach((nombre) => {
  console.log(`"${nombre}": ${validarNombre(nombre)}`);
});
// "José García": true
// "北京市": true
// "Москва": true
// "محمد أحمد": true
// "João": true
// "123Invalid": false
// "": false

// Variante: solo letras latinas
const latinPattern = /^[\p{Script=Latin}\s]+$/u;
console.log(latinPattern.test('José García')); // true
console.log(latinPattern.test('北京市')); // false
```

---

## Ejercicio 5: Tokenizer con Sticky

```javascript
/**
 * Tokenizer usando flag sticky
 *
 * ¿Por qué? Necesitamos extraer tokens en secuencia exacta
 * ¿Para qué? Parsers, lexers, intérpretes
 *
 * Flags:
 * y - sticky: solo coincide en lastIndex exacto
 */

const expresion = '123 + 456 * 789';

const tokenDefs = [
  { type: 'number', pattern: /\d+/y },
  { type: 'operator', pattern: /[+\-*/]/y },
  { type: 'space', pattern: /\s+/y },
];

function tokenize(input) {
  const tokens = [];
  let pos = 0;

  while (pos < input.length) {
    let matched = false;

    for (const def of tokenDefs) {
      def.pattern.lastIndex = pos;
      const match = def.pattern.exec(input);

      if (match) {
        tokens.push({
          type: def.type,
          value: match[0],
        });
        pos += match[0].length;
        matched = true;
        break;
      }
    }

    if (!matched) {
      throw new Error(`Token inesperado en posición ${pos}: "${input[pos]}"`);
    }
  }

  return tokens;
}

console.log(tokenize(expresion));
// [
//   { type: 'number', value: '123' },
//   { type: 'space', value: ' ' },
//   { type: 'operator', value: '+' },
//   { type: 'space', value: ' ' },
//   { type: 'number', value: '456' },
//   { type: 'space', value: ' ' },
//   { type: 'operator', value: '*' },
//   { type: 'space', value: ' ' },
//   { type: 'number', value: '789' }
// ]

// Filtrar espacios si no son necesarios
const tokensNoSpace = tokenize(expresion).filter((t) => t.type !== 'space');
console.log(tokensNoSpace);
```

---

## Ejercicio 6: Índices de Grupos

```javascript
/**
 * Obtener posiciones exactas de cada grupo
 *
 * ¿Por qué? Necesitamos saber dónde está cada parte
 * ¿Para qué? Resaltado de sintaxis, editores
 *
 * Flags:
 * d - incluir índices en el resultado
 */

const texto = 'Email: usuario@dominio.com';

/**
 * Desglose:
 * (\w+)   → Grupo 1: usuario
 * @       → Literal
 * (\w+)   → Grupo 2: dominio
 * \.      → Literal (escapado)
 * (\w+)   → Grupo 3: extensión
 */
const pattern = /(\w+)@(\w+)\.(\w+)/d;

const match = texto.match(pattern);

console.log('Match completo:', match[0]);
console.log('Indices:', match.indices);

function extraerPosiciones(texto) {
  const match = texto.match(pattern);

  if (!match) return null;

  return {
    usuario: {
      valor: match[1],
      start: match.indices[1][0],
      end: match.indices[1][1],
    },
    dominio: {
      valor: match[2],
      start: match.indices[2][0],
      end: match.indices[2][1],
    },
    extension: {
      valor: match[3],
      start: match.indices[3][0],
      end: match.indices[3][1],
    },
  };
}

console.log(extraerPosiciones(texto));
// {
//   usuario: { valor: 'usuario', start: 7, end: 14 },
//   dominio: { valor: 'dominio', start: 15, end: 22 },
//   extension: { valor: 'com', start: 23, end: 26 }
// }
```

---

## Ejercicio 7: Búsqueda con Emojis

```javascript
/**
 * Encontrar y analizar emojis
 *
 * ¿Por qué? Los emojis son caracteres Unicode especiales
 * ¿Para qué? Análisis de sentimiento, filtrado
 *
 * Flags:
 * g - encontrar todos
 * u - soporte Unicode completo
 */

const texto = 'Hola 👋 amigo! Cómo estás? 😀 Espero que bien 🎉 Nos vemos 👍';

// Patrón para emojis
const emojiPattern = /\p{Extended_Pictographic}/gu;

function analizarEmojis(texto) {
  const matches = texto.match(emojiPattern) || [];
  const unicos = [...new Set(matches)];

  return {
    total: matches.length,
    emojis: matches,
    unicos: unicos.length,
    frecuencia: matches.reduce((acc, emoji) => {
      acc[emoji] = (acc[emoji] || 0) + 1;
      return acc;
    }, {}),
  };
}

console.log(analizarEmojis(texto));
// {
//   total: 4,
//   emojis: ['👋', '😀', '🎉', '👍'],
//   unicos: 4,
//   frecuencia: { '👋': 1, '😀': 1, '🎉': 1, '👍': 1 }
// }

// Reemplazar emojis con texto
function emojiToText(texto) {
  const map = {
    '👋': ':wave:',
    '😀': ':smile:',
    '🎉': ':party:',
    '👍': ':thumbsup:',
  };

  return texto.replace(emojiPattern, (emoji) => map[emoji] || emoji);
}

console.log(emojiToText(texto));
// "Hola :wave: amigo! Cómo estás? :smile: Espero que bien :party: Nos vemos :thumbsup:"
```

---

## Desafío: Log Parser Avanzado

```javascript
/**
 * Parser de logs completo
 *
 * ¿Por qué? Los logs tienen formato estructurado pero flexible
 * ¿Para qué? Monitoreo, debugging, análisis
 */

const logs = `2024-01-15 10:30:45 [INFO] Server started on port 3000
2024-01-15 10:30:46 [DEBUG] Loading config file...
/* Multi-line
   debug info */
2024-01-15 10:30:47 [ERROR] Connection failed:
  Host: localhost
  Port: 5432
2024-01-15 10:30:48 [warning] Low memory
2024-01-15 10:30:49 [INFO] Retrying connection...`;

/**
 * Desglose del patrón principal:
 * ^(\d{4}-\d{2}-\d{2})  → Fecha YYYY-MM-DD
 * \s+                    → Espacios
 * (\d{2}:\d{2}:\d{2})   → Hora HH:MM:SS
 * \s+                    → Espacios
 * \[(\w+)\]             → Nivel entre corchetes
 * \s+                    → Espacios
 * (.+?)                  → Mensaje (non-greedy)
 * (?=^\\d{4}|$)          → Hasta la siguiente fecha o fin
 *
 * Flags: g, i, m, s
 */

function parseLogs(texto) {
  // Primero, remover comentarios multilínea
  const sinComentarios = texto.replace(/\/\*[\s\S]*?\*\//g, '');

  // Patrón para cada entrada de log
  const pattern =
    /^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+([\s\S]+?)(?=^\d{4}-\d{2}-\d{2}|$)/gim;

  const entries = [];

  for (const match of sinComentarios.matchAll(pattern)) {
    entries.push({
      date: match[1],
      time: match[2],
      level: match[3].toUpperCase(),
      message: match[4].trim().replace(/\n\s+/g, ' '),
    });
  }

  return entries;
}

const parsed = parseLogs(logs);
console.log(parsed);

// Filtrar por nivel
function filterByLevel(logs, level) {
  return logs.filter((l) => l.level === level.toUpperCase());
}

console.log('\n=== ERRORES ===');
console.log(filterByLevel(parsed, 'error'));

console.log('\n=== INFO ===');
console.log(filterByLevel(parsed, 'info'));

// Buscar en mensajes
function searchLogs(logs, term) {
  const pattern = new RegExp(term, 'i');
  return logs.filter((l) => pattern.test(l.message));
}

console.log("\n=== Logs con 'connection' ===");
console.log(searchLogs(parsed, 'connection'));
```

---

**Siguiente:** [Proyecto Semana 06](../3-proyecto/proyecto-06-buscador.md)
