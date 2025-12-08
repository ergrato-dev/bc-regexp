# Recursos - Semana 02: Character Classes

## 🖼️ Assets de la Semana

| Archivo                 | Descripción                   | Vista                                    |
| ----------------------- | ----------------------------- | ---------------------------------------- |
| `character-classes.svg` | Diagrama de character classes | [Ver](../0-assets/character-classes.svg) |

## 🔧 Herramientas Online

### Testers con Explicación de Character Classes

| Herramienta  | URL                                  | Destacado                        |
| ------------ | ------------------------------------ | -------------------------------- |
| **regex101** | [regex101.com](https://regex101.com) | Explica cada `\d`, `\w`, `[a-z]` |
| **RegExr**   | [regexr.com](https://regexr.com)     | Panel lateral con referencia     |
| **Debuggex** | [debuggex.com](https://debuggex.com) | Visualiza rangos en diagrama     |

## 📚 Documentación Específica

### Character Classes en MDN

- [Character Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Character_Classes)
- [Assertions (incluyendo \b)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Assertions)

### Unicode y Character Classes

- [Unicode Property Escapes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Unicode_character_class_escape) - Para español: `\p{L}`

## 🎓 Tutoriales Específicos

| Recurso                  | Tema              | URL                                                                         |
| ------------------------ | ----------------- | --------------------------------------------------------------------------- |
| RegexOne                 | Character Classes | [Lesson 3-5](https://regexone.com/)                                         |
| JavaScript.info          | Sets and Ranges   | [Sets and Ranges](https://javascript.info/regexp-character-sets-and-ranges) |
| Regular-Expressions.info | Character Classes | [Character Class](https://www.regular-expressions.info/charclass.html)      |

## 📖 Referencia Rápida

### Shorthand Classes

```
┌──────────┬────────────────┬──────────────────────────────┐
│ Shorthand│ Equivalente    │ Descripción                  │
├──────────┼────────────────┼──────────────────────────────┤
│ \d       │ [0-9]          │ Dígito                       │
│ \D       │ [^0-9]         │ NO dígito                    │
│ \w       │ [a-zA-Z0-9_]   │ Word character               │
│ \W       │ [^a-zA-Z0-9_]  │ NO word character            │
│ \s       │ [\t\n\r\f\v ]  │ Whitespace                   │
│ \S       │ [^\t\n\r\f\v ] │ NO whitespace                │
│ \b       │ -              │ Word boundary (posición)     │
│ \B       │ -              │ NO word boundary             │
└──────────┴────────────────┴──────────────────────────────┘
```

### Caracteres Especiales en `[...]`

```
┌────────┬─────────────────────────────────────────────────┐
│ Char   │ Comportamiento dentro de []                     │
├────────┼─────────────────────────────────────────────────┤
│ .      │ Literal (no necesita escape)                    │
│ ^      │ Negación si está al inicio, literal si no       │
│ -      │ Rango si está entre chars, literal si no        │
│ ]      │ Siempre necesita escape: \]                     │
│ \      │ Siempre necesita escape: \\                     │
│ $*+?   │ Literales (no necesitan escape)                 │
└────────┴─────────────────────────────────────────────────┘
```

## 🧪 Práctica Adicional

### Ejercicios Recomendados

1. **RegexOne** - Completa lecciones 3, 4 y 5
2. **HackerRank** - [Matching Specific Characters](https://www.hackerrank.com/challenges/matching-specific-characters)
3. **Regex Crossword** - Puzzles de nivel "Beginner"

### Desafíos

| Desafío             | Descripción     |
| ------------------- | --------------- |
| Validar NIF español | `\d{8}[A-Z]`    |
| Validar matrícula   | `\d{4}[A-Z]{3}` |
| Detectar hashtags   | `#\w+`          |
| Detectar menciones  | `@\w+`          |

## 🔗 Artículos Útiles

- [The Complete Guide to Regular Expressions](https://coderpad.io/blog/development/the-complete-guide-to-regular-expressions-regex/)
- [Word Boundaries Explained](https://www.regular-expressions.info/wordboundaries.html)
- [Unicode in JavaScript Regular Expressions](https://mathiasbynens.be/notes/javascript-unicode)

## ⚠️ Errores Comunes

### 1. Confundir `^` dentro y fuera de `[]`

```javascript
// Fuera: anchor de inicio
/^abc/   // "abc" al inicio

// Dentro al inicio: negación
/[^abc]/ // Cualquiera EXCEPTO a, b, c

// Dentro no al inicio: literal
/[a^bc]/ // a, ^, b, o c
```

### 2. El guión en medio crea rango

```javascript
// Esto es un rango de a hasta z:
/[a-z]/

// Esto incluye guión literal:
/[-az]/  // Al inicio
/[az-]/  // Al final
/[a\-z]/ // Escapado
```

### 3. `\w` incluye guión bajo

```javascript
// \w = [a-zA-Z0-9_]
/\w/.test('_'); // true!

// Si NO quieres guión bajo:
/[a-zA-Z0-9]/;
```

---

**Siguiente semana:** Cuantificadores (`*`, `+`, `?`, `{n,m}`)
