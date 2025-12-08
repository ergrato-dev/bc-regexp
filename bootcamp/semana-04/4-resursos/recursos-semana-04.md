# Recursos - Semana 04: Grupos y Capturas

## 🖼️ Assets de la Semana

| Archivo      | Descripción                         | Vista                         |
| ------------ | ----------------------------------- | ----------------------------- |
| `groups.svg` | Diagrama de grupos y backreferences | [Ver](../0-assets/groups.svg) |

## 🔧 Herramientas Online

### Visualizadores de Grupos

| Herramienta  | URL                                  | Destacado                                |
| ------------ | ------------------------------------ | ---------------------------------------- |
| **regex101** | [regex101.com](https://regex101.com) | Muestra grupos y capturas en tiempo real |
| **Debuggex** | [debuggex.com](https://debuggex.com) | Visualiza grupos anidados                |
| **RegViz**   | [regviz.org](http://regviz.org)      | Diagramas interactivos                   |

## 📚 Documentación Específica

### Grupos en MDN

- [Groups and Backreferences](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Groups_and_Backreferences)
- [Named Capture Groups](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Named_capturing_group)

### JavaScript.info

- [Capturing Groups](https://javascript.info/regexp-groups)
- [Backreferences](https://javascript.info/regexp-backreferences)

## 📖 Referencia Rápida

### Tipos de Grupos

```
┌──────────────────┬──────────────────┬────────────────────────────────┐
│ Tipo             │ Sintaxis         │ Descripción                    │
├──────────────────┼──────────────────┼────────────────────────────────┤
│ Capture Group    │ (...)            │ Captura y guarda el contenido  │
│ Non-Capturing    │ (?:...)          │ Agrupa sin capturar            │
│ Named Group      │ (?<nombre>...)   │ Captura con nombre             │
└──────────────────┴──────────────────┴────────────────────────────────┘
```

### Backreferences

```
┌──────────────────┬──────────────────┬────────────────────────────────┐
│ Contexto         │ Sintaxis         │ Ejemplo                        │
├──────────────────┼──────────────────┼────────────────────────────────┤
│ En patrón        │ \1, \2, ...      │ /(\w+)\s+\1/                   │
│ En patrón (name) │ \k<nombre>       │ /(?<x>\w+)\s+\k<x>/            │
│ En replace       │ $1, $2, ...      │ .replace(/(a)/, "$1b")         │
│ En replace (name)│ $<nombre>        │ .replace(/(?<x>a)/, "$<x>b")   │
└──────────────────┴──────────────────┴────────────────────────────────┘
```

### Métodos de JavaScript

```
┌──────────────────┬─────────────────────────────────────────────────────┐
│ Método           │ Comportamiento con grupos                           │
├──────────────────┼─────────────────────────────────────────────────────┤
│ .match()         │ Retorna array con grupos (sin flag g)               │
│ .match(/g/)      │ Solo matches, pierde grupos                         │
│ .matchAll(/g/)   │ Iterador con grupos para cada match                 │
│ .exec()          │ Match + grupos + index + input                      │
│ .replace()       │ Usa $1, $2 o $<nombre> en reemplazo                 │
│ .split()         │ Si hay grupo, incluye capturas en resultado         │
└──────────────────┴─────────────────────────────────────────────────────┘
```

## 🎓 Tutoriales Específicos

| Recurso                  | Tema   | URL                                                            |
| ------------------------ | ------ | -------------------------------------------------------------- |
| RegexOne                 | Groups | [Lesson 9-11](https://regexone.com/)                           |
| Regular-Expressions.info | Groups | [Groups](https://www.regular-expressions.info/refcapture.html) |
| JavaScript.info          | Groups | [Capturing Groups](https://javascript.info/regexp-groups)      |

## 🧪 Práctica Adicional

### Ejercicios Recomendados

1. **HackerRank** - [Capturing Groups](https://www.hackerrank.com/challenges/capturing-groups)
2. **RegexOne** - Lecciones 9, 10, 11
3. **Regex Crossword** - Puzzles con grupos

### Patrones Comunes

| Uso             | Patrón                         | Descripción              |
| --------------- | ------------------------------ | ------------------------ |
| Email partes    | `([\w.-]+)@([\w.-]+)`          | Usuario y dominio        |
| Fecha partes    | `(\d{2})\/(\d{2})\/(\d{4})`    | Día, mes, año            |
| URL partes      | `(https?):\/\/([^\/]+)(\/.*)?` | Protocolo, host, path    |
| Nombre completo | `(\w+)\s+(\w+)`                | Nombre, apellido         |
| HTML tag        | `<(\w+)>.*?<\/\1>`             | Etiqueta con cierre      |
| Duplicados      | `\b(\w+)\s+\1\b`               | Palabra repetida         |
| Comillas        | `(['"])[^'"]*\1`               | Contenido entre comillas |

## ⚠️ Errores Comunes

### 1. Perder grupos con flag `g`

```javascript
// ❌ Con flag g, match pierde grupos
'a@b.com, c@d.com'.match(/(\w+)@(\w+)/g);
// ['a@b.com', 'c@d.com'] - sin grupos

// ✅ Usar matchAll
for (const m of 'a@b.com, c@d.com'.matchAll(/(\w+)@(\w+)/g)) {
  console.log(m[1], m[2]); // a b, c d
}
```

### 2. Índice incorrecto con grupos anidados

```javascript
// Los grupos se numeran por paréntesis de apertura
/((a)(b))/.exec('ab');
// [0]: "ab"  - match completo
// [1]: "ab"  - grupo 1 (externo)
// [2]: "a"   - grupo 2 (primer interno)
// [3]: "b"   - grupo 3 (segundo interno)
```

### 3. Backreference antes de definir grupo

```javascript
// ❌ No funciona en JavaScript
/\1(\w+)/   // Referencia antes de definición

// ✅ Grupo primero, referencia después
/(\w+)\s+\1/
```

### 4. Olvidar escapar en replace

```javascript
// ❌ Esto no funciona como esperas
str.replace(/(a)/, '\1'); // \1 literal

// ✅ Usar $1
str.replace(/(a)/, '$1');
```

## 🔗 Artículos Útiles

- [ES2018 Named Capture Groups](https://2ality.com/2017/05/regexp-named-capture-groups.html)
- [Replace with Function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace#specifying_a_function_as_the_replacement)
- [matchAll](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll)

## 💡 Tips de Rendimiento

```javascript
// ✅ Usar non-capturing cuando no necesitas el valor
/(?:https?):\/\/([\w.]+)/  // Solo captura el dominio

// ✅ Named groups para código mantenible
/(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/

// ✅ Destructuring con named groups
const { year, month, day } = match.groups;

// ✅ Reusar patrón compilado
const pattern = /(\w+)/g;  // Definir una vez
texto1.match(pattern);
texto2.match(pattern);
```

---

**Próxima semana:** Lookahead y Lookbehind (`(?=)`, `(?!)`, `(?<=)`, `(?<!)`)
