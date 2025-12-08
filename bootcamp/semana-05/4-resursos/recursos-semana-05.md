# Recursos - Semana 05: Lookahead y Lookbehind

## 🖼️ Assets de la Semana

| Archivo           | Descripción                        | Vista                              |
| ----------------- | ---------------------------------- | ---------------------------------- |
| `lookarounds.svg` | Diagrama de lookahead y lookbehind | [Ver](../0-assets/lookarounds.svg) |

## 🔧 Herramientas Online

### Visualizadores de Lookarounds

| Herramienta  | URL                                      | Destacado                       |
| ------------ | ---------------------------------------- | ------------------------------- |
| **regex101** | [regex101.com](https://regex101.com)     | Explica lookarounds paso a paso |
| **Debuggex** | [debuggex.com](https://debuggex.com)     | Visualiza aserciones            |
| **Regulex**  | [jex.im/regulex](https://jex.im/regulex) | Diagramas de railroad           |

## 📚 Documentación Específica

### Lookarounds en MDN

- [Assertions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Assertions)
- [Lookahead](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Lookahead_assertion)
- [Lookbehind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Lookbehind_assertion)

### JavaScript.info

- [Lookahead and Lookbehind](https://javascript.info/regexp-lookahead-lookbehind)

## 📖 Referencia Rápida

### Tipos de Lookarounds

```
┌──────────────────────┬────────────┬────────────────────────────────┐
│ Tipo                 │ Sintaxis   │ Descripción                    │
├──────────────────────┼────────────┼────────────────────────────────┤
│ Positive Lookahead   │ (?=...)    │ Debe seguir esto               │
│ Negative Lookahead   │ (?!...)    │ NO debe seguir esto            │
│ Positive Lookbehind  │ (?<=...)   │ Debe preceder esto             │
│ Negative Lookbehind  │ (?<!...)   │ NO debe preceder esto          │
└──────────────────────┴────────────┴────────────────────────────────┘
```

### Características

```
┌────────────────────┬─────────────────────────────────────────────────┐
│ Característica     │ Comportamiento                                  │
├────────────────────┼─────────────────────────────────────────────────┤
│ Consume texto      │ No - son "zero-width"                           │
│ Incluido en match  │ No - solo verifican                             │
│ Pueden anidar      │ Sí                                              │
│ Soporte            │ Lookahead: ES3+, Lookbehind: ES2018+            │
└────────────────────┴─────────────────────────────────────────────────┘
```

## 🎓 Tutoriales Específicos

| Recurso                  | Tema                 | URL                                                                |
| ------------------------ | -------------------- | ------------------------------------------------------------------ |
| Regular-Expressions.info | Lookaround           | [Lookaround](https://www.regular-expressions.info/lookaround.html) |
| JavaScript.info          | Lookahead/Lookbehind | [Lookahead](https://javascript.info/regexp-lookahead-lookbehind)   |
| Rexegg                   | Mastering Lookahead  | [Lookahead](https://www.rexegg.com/regex-lookarounds.html)         |

## 🧪 Práctica Adicional

### Ejercicios Recomendados

1. **HackerRank** - [Lookahead and Lookbehind](https://www.hackerrank.com/challenges/positive-lookbehind)
2. **RegexOne** - Lecciones avanzadas
3. **Regex Crossword** - Puzzles expertos

### Patrones Comunes

| Uso                | Patrón                                  | Descripción          |
| ------------------ | --------------------------------------- | -------------------- |
| Password fuerte    | `^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$` | Múltiples requisitos |
| No @ al final      | `\w+(?!@)$`                             | Email sin dominio    |
| Precio sin símbolo | `(?<=\$)\d+`                            | Solo el número       |
| Palabra no negada  | `\b(?!un)\w+\b`                         | Sin prefijo "un"     |
| Separador miles    | `\B(?=(\d{3})+(?!\d))`                  | Para insertar comas  |
| Valor de atributo  | `(?<=id=")[^"]+(?=")`                   | Sin id= ni comillas  |

## ⚠️ Errores Comunes

### 1. Olvidar que no consumen texto

```javascript
// ❌ Esperar que lookahead esté en el match
'100€'.match(/\d+(?=€)/); // ['100'], no ['100€']

// ✅ Si quieres incluirlo, no uses lookahead
'100€'.match(/\d+€/); // ['100€']
```

### 2. Lookbehind en navegadores antiguos

```javascript
// ❌ Lookbehind no funciona en IE, Safari < 16.4
/(?<=\$)\d+/

// ✅ Alternativa: usar grupo y acceder a él
/\$(\d+)/.exec("$100")[1]  // "100"
```

### 3. Confundir dirección

```javascript
// Lookahead: mira ADELANTE (a la derecha)
/foo(?=bar)/  // "foo" seguido de "bar"

// Lookbehind: mira ATRÁS (a la izquierda)
/(?<=foo)bar/ // "bar" precedido de "foo"
```

### 4. Asumir longitud variable en lookbehind

```javascript
// ⚠️ En algunos engines, lookbehind debe ser longitud fija
// JavaScript ES2018+ soporta longitud variable

// ✅ Funciona en JavaScript moderno
/(?<=\w+)\d+/;
```

## 🔗 Artículos Útiles

- [Password Validation Best Practices](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/07-Testing_for_Weak_Password_Policy)
- [Luhn Algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm)
- [Zero-Width Assertions](https://www.regular-expressions.info/refadv.html)

## 💡 Tips de Rendimiento

```javascript
// ✅ Lookarounds son eficientes para validación
/^(?=.*[A-Z])(?=.*\d).{8,}$/  // Valida en una pasada

// ❌ Evitar lookarounds excesivos
/(?=a)(?=b)(?=c)(?=d)/  // Cuatro checks en cada posición

// ✅ Combinar cuando sea posible
/(?=.*[A-Z].*\d)/  // Combina mayúscula y dígito

// ✅ Usar negación para excluir
/\b(?!\d)\w+\b/  // Palabras que no empiezan con dígito
```

---

**Próxima semana:** Flags y Modificadores (`g`, `i`, `m`, `s`, `u`)
