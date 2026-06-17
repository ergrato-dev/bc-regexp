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

**Python:**

```python
import re

texto = """JavaScript is a programming language. javascript is used for web development.
Many developers love JavaScript. JAVASCRIPT powers many websites."""

def contar_palabra(texto, palabra):
    escapada = re.escape(palabra)
    pattern = re.compile(rf'\b{escapada}\b', re.IGNORECASE)
    matches = pattern.findall(texto)
    return len(matches) if matches else 0

print(contar_palabra(texto, 'javascript'))  # 4
print(contar_palabra(texto, 'is'))          # 2
print(contar_palabra(texto, 'PYTHON'))      # 0
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

**Python:**

```python
import re

codigo = """const x = 1;
/* Este es un
   comentario
   multilínea */
const y = 2;
/* Otro comentario */
const z = 3;"""

# Con flag DOTALL (equivalente a s)
pattern = re.compile(r'/\*.*?\*/', re.DOTALL)

print(pattern.findall(codigo))
# [
#   '/* Este es un\n   comentario\n   multilínea */',
#   '/* Otro comentario */'
# ]

# Función para extraer solo el contenido (sin /* */)
def extraer_comentarios(code):
    pattern = re.compile(r'/\*(.*?)\*/', re.DOTALL)
    comentarios = []
    for match in pattern.finditer(code):
        comentarios.append(match.group(1).strip())
    return comentarios

print(extraer_comentarios(codigo))
# ['Este es un\n   comentario\n   multilínea', 'Otro comentario']
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

**Python:**

```python
import re

config = """# Configuración de la app
nombre=MiApp
version=1.0.0
# Puerto del servidor
puerto=3000
debug=true"""

pattern = re.compile(r'^(?!#)(\w+)=(.+)$', re.MULTILINE)

def parse_config(texto):
    config = {}
    for match in pattern.finditer(texto):
        config[match.group(1)] = match.group(2)
    return config

print(parse_config(config))
# {'nombre': 'MiApp', 'version': '1.0.0', 'puerto': '3000', 'debug': 'true'}
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

**Python:**

```python
import re

nombres = [
    'José García', '北京市', 'Москва', 'محمد أحمد',
    'João', '123Invalid', ''
]

# Python 3 usa Unicode por defecto, no necesita flag u
pattern = re.compile(r'^[\p{Letter}\s]+$')  # ⚠️ `\p{Letter}` no es soportado por re
# Alternativa: usar regex module (pip install regex)
# import regex
# pattern = regex.compile(r'^[\p{Letter}\s]+$')
# O usar categorías Unicode con re:
# pattern = re.compile(r'^[^\W\d_\s][\w\s-]*$', re.UNICODE)

def validar_nombre(nombre):
    if not nombre:
        return False
    return bool(pattern.search(nombre)) if pattern else False

# Nota: para Unicode property escapes (\p{...}) en Python,
# instala `regex` (pip install regex) que es compatible con PCRE/JS
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

**Python:**

```python
import re

expresion = '123 + 456 * 789'

# Python no tiene flag sticky (y), se simula con posición
def tokenize(inp):
    token_defs = [
        ('NUMBER', r'\d+'),
        ('OPERATOR', r'[+\-*/]'),
        ('SPACE', r'\s+'),
    ]
    tokens = []
    pos = 0
    while pos < len(inp):
        matched = False
        for ttype, tpat in token_defs:
            m = re.compile(tpat).match(inp, pos)
            if m:
                tokens.append({'type': ttype, 'value': m.group()})
                pos += len(m.group())
                matched = True
                break
        if not matched:
            raise ValueError(f'Token inesperado en posición {pos}: "{inp[pos]}"')
    return tokens

print(tokenize(expresion))
# [
#   {'type': 'NUMBER', 'value': '123'},
#   {'type': 'SPACE', 'value': ' '},
#   {'type': 'OPERATOR', 'value': '+'},
#   ...
# ]
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

**Python:**

```python
import re

texto = 'Email: usuario@dominio.com'

pattern = re.compile(r'(\w+)@(\w+)\.(\w+)')

match = pattern.search(texto)

print('Match completo:', match.group(0))
print('Posiciones:', match.span())

def extraer_posiciones(texto):
    match = pattern.search(texto)
    if not match:
        return None
    return {
        'usuario': {
            'valor': match.group(1),
            'start': match.start(1),
            'end': match.end(1),
        },
        'dominio': {
            'valor': match.group(2),
            'start': match.start(2),
            'end': match.end(2),
        },
        'extension': {
            'valor': match.group(3),
            'start': match.start(3),
            'end': match.end(3),
        },
    }

print(extraer_posiciones(texto))
# {
#   'usuario': {'valor': 'usuario', 'start': 7, 'end': 14},
#   'dominio': {'valor': 'dominio', 'start': 15, 'end': 22},
#   'extension': {'valor': 'com', 'start': 23, 'end': 26}
# }
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

**Python:**

```python
import re

texto = 'Hola 👋 amigo! Cómo estás? 😀 Espero que bien 🎉 Nos vemos 👍'

# ⚠️ \p{Extended_Pictographic} requiere módulo `regex`
# pip install regex
import regex  # noqa: E402

emoji_pattern = regex.compile(r'\p{Extended_Pictographic}')

def analizar_emojis(texto):
    matches = emoji_pattern.findall(texto) or []
    unicos = list(set(matches))
    return {
        'total': len(matches),
        'emojis': matches,
        'unicos': len(unicos),
        'frecuencia': {e: matches.count(e) for e in unicos},
    }

print(analizar_emojis(texto))
# {'total': 4, 'emojis': ['👋', '😀', '🎉', '👍'], 'unicos': 4, ...}

def emoji_to_text(texto):
    mapa = {'👋': ':wave:', '😀': ':smile:', '🎉': ':party:', '👍': ':thumbsup:'}
    return emoji_pattern.sub(lambda m: mapa.get(m.group(), m.group()), texto)

print(emoji_to_text(texto))
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

**Python:**

```python
import re

logs = """2024-01-15 10:30:45 [INFO] Server started on port 3000
2024-01-15 10:30:46 [DEBUG] Loading config file...
/* Multi-line
   debug info */
2024-01-15 10:30:47 [ERROR] Connection failed:
  Host: localhost
  Port: 5432
2024-01-15 10:30:48 [warning] Low memory
2024-01-15 10:30:49 [INFO] Retrying connection..."""

def parse_logs(texto):
    # Remover comentarios multilínea
    sin_comentarios = re.sub(r'/\*[\s\S]*?\*/', '', texto)

    pattern = re.compile(
        r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+'
        r'([\s\S]+?)(?=^\d{4}-\d{2}-\d{2}|\Z)',
        re.IGNORECASE | re.MULTILINE
    )

    entries = []
    for match in pattern.finditer(sin_comentarios):
        entries.append({
            'date': match.group(1),
            'time': match.group(2),
            'level': match.group(3).upper(),
            'message': re.sub(r'\n\s+', ' ', match.group(4).strip()),
        })
    return entries

parsed = parse_logs(logs)
print(parsed)

def filter_by_level(logs, level):
    return [l for l in logs if l['level'] == level.upper()]

print('\n=== ERRORES ===')
print(filter_by_level(parsed, 'error'))

def search_logs(logs, term):
    pattern = re.compile(term, re.IGNORECASE)
    return [l for l in logs if pattern.search(l['message'])]

print("\n=== Logs con 'connection' ===")
print(search_logs(parsed, 'connection'))
```

---

**Siguiente:** [Proyecto Semana 06](../3-proyecto/proyecto-06-buscador.md)
