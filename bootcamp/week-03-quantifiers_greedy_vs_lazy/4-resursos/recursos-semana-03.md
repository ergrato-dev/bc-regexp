# Recursos - Semana 03: Quantifiers

## 🖼️ Assets de la Semana

| Archivo           | Descripción             | Vista                              |
| ----------------- | ----------------------- | ---------------------------------- |
| `quantifiers.svg` | Diagrama de quantifiers | [Ver](../0-assets/quantifiers.svg) |

## 🔧 Herramientas Online

### Visualizadores de Quantifiers

| Herramienta  | URL                                      | Destacado                                  |
| ------------ | ---------------------------------------- | ------------------------------------------ |
| **regex101** | [regex101.com](https://regex101.com)     | Muestra el proceso de matching paso a paso |
| **Debuggex** | [debuggex.com](https://debuggex.com)     | Visualiza loops y repeticiones             |
| **Regulex**  | [jex.im/regulex](https://jex.im/regulex) | Diagramas de railroad claros               |

## 📚 Documentación Específica

### Quantifiers en MDN

- [Quantifiers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Quantifiers)
- [Greedy and Non-Greedy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Quantifier#greedy_versus_non-greedy)

### JavaScript.info

- [Quantifiers +, \*, ? and {n}](https://javascript.info/regexp-quantifiers)
- [Greedy and Lazy Quantifiers](https://javascript.info/regexp-greedy-and-lazy)

## 📖 Referencia Rápida

### Quantifiers

```
┌────────────┬────────────────┬────────────────────────────────┐
│ Quantifier │ Equivalente    │ Significado                    │
├────────────┼────────────────┼────────────────────────────────┤
│ *          │ {0,}           │ Cero o más                     │
│ +          │ {1,}           │ Uno o más                      │
│ ?          │ {0,1}          │ Cero o uno (opcional)          │
│ {n}        │ {n,n}          │ Exactamente n                  │
│ {n,m}      │ -              │ Entre n y m (inclusivo)        │
│ {n,}       │ -              │ Al menos n (sin máximo)        │
│ {0,m}      │ -              │ Hasta m (máximo)               │
└────────────┴────────────────┴────────────────────────────────┘
```

### Greedy vs Lazy

```
┌─────────┬─────────┬──────────────────────────────────────────┐
│ Greedy  │ Lazy    │ Comportamiento                           │
├─────────┼─────────┼──────────────────────────────────────────┤
│ *       │ *?      │ Cero o más (mínimo)                      │
│ +       │ +?      │ Uno o más (mínimo)                       │
│ ?       │ ??      │ Cero o uno (prefiere cero)               │
│ {n,m}   │ {n,m}?  │ Entre n y m (prefiere n)                 │
└─────────┴─────────┴──────────────────────────────────────────┘
```

## 🎓 Tutoriales Específicos

| Recurso                  | Tema        | URL                                                               |
| ------------------------ | ----------- | ----------------------------------------------------------------- |
| RegexOne                 | Repetition  | [Lesson 6-8](https://regexone.com/)                               |
| Regular-Expressions.info | Repetition  | [Repetition](https://www.regular-expressions.info/repeat.html)    |
| JavaScript.info          | Greedy/Lazy | [Greedy and Lazy](https://javascript.info/regexp-greedy-and-lazy) |

## 🧪 Práctica Adicional

### Ejercicios Recomendados

1. **HackerRank** - [Matching {x} Repetitions](https://www.hackerrank.com/challenges/matching-x-repetitions)
2. **RegexOne** - Lecciones 6, 7, 8
3. **Regex Crossword** - Puzzles intermedios

### Patrones Comunes

| Uso              | Patrón                            | Descripción             |
| ---------------- | --------------------------------- | ----------------------- |
| Teléfono ES      | `[6-9]\d{8}`                      | 9 dígitos               |
| Código Postal ES | `\d{5}`                           | 5 dígitos               |
| DNI              | `\d{8}[A-Z]`                      | 8 dígitos + letra       |
| Email básico     | `[\w.-]+@[\w.-]+\.\w{2,}`         | Formato simple          |
| URL              | `https?://[\w.-]+\.\w{2,}(/\S*)?` | Con path opcional       |
| Precio           | `\$\d+(\.\d{2})?`                 | Con centavos opcionales |
| Fecha            | `\d{2}/\d{2}/\d{4}`               | DD/MM/YYYY              |
| Hora             | `\d{2}:\d{2}(:\d{2})?`            | HH:MM(:SS)              |

## ⚠️ Errores Comunes

### 1. Olvidar que quantifiers son greedy

```javascript
// ❌ Captura más de lo esperado
'"hola" y "mundo"'.match(/".*"/); // ['"hola" y "mundo"']

// ✅ Usar lazy
'"hola" y "mundo"'.match(/".*?"/g); // ['"hola"', '"mundo"']
```

### 2. Confundir `*` con `+`

```javascript
// * = cero o más (puede no haber ninguno)
/ab*c/.test('ac'); // true

// + = uno o más (debe haber al menos uno)
/ab+c/.test('ac'); // false
```

### 3. `{n,m}` sin espacio

```javascript
// ❌ Con espacio no funciona
/\d{3, 5}/   // Error de sintaxis

// ✅ Sin espacio
/\d{3,5}/    // Correcto
```

### 4. Quantifier sin elemento previo

```javascript
// ❌ Error
/+abc/   // Error: nada que cuantificar

// ✅ Correcto
/a+bc/   // 'a' una o más veces
```

## 🔗 Artículos Útiles

- [Catastrophic Backtracking](https://www.regular-expressions.info/catastrophic.html)
- [Regex Performance](https://www.loggly.com/blog/regexes-the-bad-the-better-and-the-best/)
- [Possessive Quantifiers](https://www.regular-expressions.info/possessive.html) (no en JS)

## 💡 Tips de Rendimiento

```javascript
// ❌ Potencialmente lento (backtracking excesivo)
/(a+)+$/

// ✅ Más específico
/a+$/

// ❌ Lazy con mucho backtracking
/.*?texto/

// ✅ Negación más eficiente
/[^t]*texto/
```

---

**Próxima semana:** Grupos y capturas (`()`, `(?:)`, backreferences)
