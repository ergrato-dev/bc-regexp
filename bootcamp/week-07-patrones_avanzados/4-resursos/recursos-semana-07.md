# Recursos - Semana 07: Patrones Avanzados y Optimización

## 🖼️ Assets de la Semana

| Archivo        | Descripción                    | Vista                           |
| -------------- | ------------------------------ | ------------------------------- |
| `advanced.svg` | Diagrama de técnicas avanzadas | [Ver](../0-assets/advanced.svg) |

## 📖 Referencia Rápida

### Named Capture Groups

```javascript
// Definición
const pattern = /(?<name>patrón)/;

// Acceso
match.groups.name

// Backreference
/(?<word>\w+)\s+\k<word>/

// Replace
str.replace(/(?<a>\w+)-(?<b>\w+)/, "$<b>-$<a>");
```

### Optimización

```
┌────────────────────────────────────────────────────────────────┐
│                     GUÍA DE OPTIMIZACIÓN                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ HACER                        ❌ EVITAR                     │
│  ─────────────────────────────────────────────────────────     │
│  [^x]* (negación)                .* (greedy abierto)           │
│  \w{1,50} (limitado)             \w+ (sin límite)              │
│  ^pattern$ (anclas)              pattern (sin anclas)          │
│  (?:...) (non-capturing)         (...) si no capturas          │
│  Alternativas específicas        (a|ab|abc) solapadas          │
│  Lookahead para validar          Backtracking complejo         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## ⚠️ Patrones Peligrosos

```javascript
// 1. Cuantificadores anidados
/(a+)+$/              // ❌ Exponencial
/(?=(a+))\1$/         // ✅ "Atomic" simulado

// 2. Alternativas solapadas
/(a|aa)+/             // ❌ Backtracking
/a+/                  // ✅ Simplificado

// 3. Greedy sin límites
/.*end/               // ❌ Puede ser lento
/[^e]*end|(?:[^n]|n(?!d))*end/  // ✅ Más específico
/.*?end/              // ✅ Lazy como alternativa

// 4. Sin anclas
/pattern/             // ❌ Busca en todo el string
/^pattern$/           // ✅ Falla rápido
```

## 🔧 Utilidades

### Benchmark de Regex

```javascript
function benchRegex(pattern, text, iterations = 10000) {
  const start = performance.now();
  for (let i = 0; i < iterations; i++) {
    pattern.test(text);
  }
  return performance.now() - start;
}

// Uso
const time = benchRegex(/pattern/, 'test text');
console.log(`${time.toFixed(2)}ms for ${iterations} iterations`);
```

### Validador de Seguridad

```javascript
function isPatternSafe(pattern) {
  const dangerous = [
    /\(\[?\w\+\]\+\)\+/, // (a+)+
    /\(\.\+\)\+/, // (.+)+
    /\(\.\*\)\+/, // (.*)+
  ];

  const source = pattern.source;
  return !dangerous.some((d) => d.test(source));
}
```

## 📚 Documentación

### MDN

- [Named capturing groups](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Named_capturing_group)
- [Backreference: \k](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Named_backreference)

### Artículos Útiles

- [Runaway Regular Expressions](https://www.regular-expressions.info/catastrophic.html)
- [ReDoS - Wikipedia](https://en.wikipedia.org/wiki/ReDoS)
- [V8 Blog: Regex Improvements](https://v8.dev/blog/regexp-tier-up)

## 💡 Patrones Útiles

### Tokenizer Base

```javascript
const tokens = [
  { type: 'KEYWORD', pattern: /\b(if|else|while|for)\b/ },
  { type: 'IDENT', pattern: /[a-zA-Z_]\w*/ },
  { type: 'NUMBER', pattern: /\d+(?:\.\d+)?/ },
  { type: 'STRING', pattern: /"[^"]*"|'[^']*'/ },
  { type: 'OP', pattern: /[+\-*/=<>!&|]+/ },
  { type: 'PUNCT', pattern: /[{}()\[\];,.]/ },
  { type: 'WS', pattern: /\s+/ },
];
```

### Extractor de Comentarios

```javascript
const comments = /\/\/[^\n]*|\/\*[\s\S]*?\*\//g;
```

### Validación de JSON Key

```javascript
const jsonKey = /^"(?:[^"\\]|\\.)*"$/;
```

### Parser de Query String

```javascript
const queryParam = /[?&](?<key>[^=]+)=(?<value>[^&]*)/g;

const url = '?name=John&age=30';
for (const m of url.matchAll(queryParam)) {
  console.log(m.groups.key, '=', m.groups.value);
}
```

## 🧪 Herramientas de Testing

| Herramienta              | URL                            | Uso              |
| ------------------------ | ------------------------------ | ---------------- |
| regex101                 | regex101.com                   | Debugging visual |
| RegExr                   | regexr.com                     | Aprendizaje      |
| Debuggex                 | debuggex.com                   | Diagramas NFA    |
| RegExp Denial of Service | github.com/davisjam/safe-regex | Seguridad        |

## 📊 Complejidad Típica

| Patrón         | Complejidad | Notas                        |
| -------------- | ----------- | ---------------------------- |
| `/abc/`        | O(n)        | Literal simple               |
| `/a+/`         | O(n)        | Cuantificador simple         |
| `/a*b*c*/`     | O(n)        | Secuencia de cuantificadores |
| `/(a+)+$/`     | O(2^n)      | ⚠️ Exponencial               |
| `/([a-z]+)*$/` | O(2^n)      | ⚠️ Exponencial               |

---

**Próxima semana:** Proyecto Final + Casos Reales
