# Recursos - Semana 08: Proyecto Final

## 🖼️ Assets de la Semana

| Archivo     | Descripción                 | Vista                        |
| ----------- | --------------------------- | ---------------------------- |
| `final.svg` | Resumen visual del bootcamp | [Ver](../0-assets/final.svg) |

## 📖 Cheatsheet Completo

### Metacaracteres

| Símbolo | Descripción                                    |
| ------- | ---------------------------------------------- |
| `.`     | Cualquier carácter (excepto `\n` sin flag `s`) |
| `^`     | Inicio del string/línea                        |
| `$`     | Fin del string/línea                           |
| `\`     | Escape                                         |
| `\|`    | Alternativa (OR)                               |

### Clases de Caracteres

| Sintaxis | Descripción         |
| -------- | ------------------- |
| `[abc]`  | a, b, o c           |
| `[^abc]` | NO a, b, ni c       |
| `[a-z]`  | Rango a-z           |
| `\d`     | Dígito `[0-9]`      |
| `\D`     | No dígito           |
| `\w`     | Word `[a-zA-Z0-9_]` |
| `\W`     | No word             |
| `\s`     | Whitespace          |
| `\S`     | No whitespace       |
| `\b`     | Word boundary       |
| `\B`     | No word boundary    |

### Cuantificadores

| Greedy  | Lazy     | Descripción   |
| ------- | -------- | ------------- |
| `*`     | `*?`     | 0 o más       |
| `+`     | `+?`     | 1 o más       |
| `?`     | `??`     | 0 o 1         |
| `{n}`   | -        | Exactamente n |
| `{n,}`  | `{n,}?`  | n o más       |
| `{n,m}` | `{n,m}?` | Entre n y m   |

### Grupos

| Sintaxis       | Descripción         |
| -------------- | ------------------- |
| `(...)`        | Capture group       |
| `(?:...)`      | Non-capturing group |
| `(?<name>...)` | Named group         |
| `\1`           | Backreference       |
| `\k<name>`     | Named backreference |

### Lookaround

| Sintaxis   | Descripción         |
| ---------- | ------------------- |
| `(?=...)`  | Positive lookahead  |
| `(?!...)`  | Negative lookahead  |
| `(?<=...)` | Positive lookbehind |
| `(?<!...)` | Negative lookbehind |

### Flags

| Flag | Nombre     | Descripción             |
| ---- | ---------- | ----------------------- |
| `g`  | global     | Todas las coincidencias |
| `i`  | ignoreCase | Ignora mayúsculas       |
| `m`  | multiline  | ^$ por línea            |
| `s`  | dotAll     | . incluye \n            |
| `u`  | unicode    | Soporte Unicode         |
| `y`  | sticky     | Solo en lastIndex       |
| `d`  | hasIndices | Índices de grupos       |

## 🔧 Patrones Útiles de Producción

### Validación

```javascript
// Email (simplificado pero robusto)
/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

// URL
/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_+.~#?&/=]*$/

// Contraseña fuerte
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/

// UUID v4
/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

// IPv4
/^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$/

// Semver
/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([\da-zA-Z-]+(?:\.[\da-zA-Z-]+)*))?(?:\+([\da-zA-Z-]+(?:\.[\da-zA-Z-]+)*))?$/
```

### Extracción

```javascript
// Emails en texto
/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g

// URLs en texto
/https?:\/\/[^\s<>"{}|\\^`\[\]]+/g

// Hashtags
/#[a-zA-Z_]\w*/g

// Menciones
/@[a-zA-Z_]\w*/g

// Fechas ISO
/\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])/g
```

### Transformación

```javascript
// Limpiar HTML
str.replace(/<[^>]+>/g, '');

// Normalizar espacios
str.replace(/\s+/g, ' ').trim();

// camelCase a snake_case
str.replace(/[A-Z]/g, (m) => '_' + m.toLowerCase());

// Escapar HTML
str.replace(
  /[&<>"']/g,
  (m) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m])
);

// Slugify
str
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-|-$/g, '');
```

## 📚 Recursos de Aprendizaje Continuo

### Documentación

- [MDN Regular Expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)
- [JavaScript.info RegExp](https://javascript.info/regular-expressions)
- [Regular-Expressions.info](https://www.regular-expressions.info/)

### Herramientas Online

| Herramienta | URL          | Uso                 |
| ----------- | ------------ | ------------------- |
| regex101    | regex101.com | Testing y debugging |
| RegExr      | regexr.com   | Aprendizaje visual  |
| Debuggex    | debuggex.com | Visualización NFA   |
| RegexPal    | regexpal.com | Testing rápido      |

### Libros

- "Mastering Regular Expressions" - Jeffrey Friedl
- "Regular Expressions Cookbook" - Jan Goyvaerts

## ⚠️ Recordatorios de Seguridad

```javascript
// ❌ Patrones peligrosos
/(a+)+$/           // Catastrophic backtracking
/(.+)+$/           // Exponencial
/(a|aa)+/          // Alternativas solapadas

// ✅ Buenas prácticas
// 1. Limitar longitud del input
if (input.length > MAX_LENGTH) reject();

// 2. Usar timeout
const controller = new AbortController();
setTimeout(() => controller.abort(), 1000);

// 3. Evitar cuantificadores anidados
// 4. Usar anclas cuando sea posible
// 5. Preferir [^x] sobre .*
```

---

**¡Felicitaciones por completar el Bootcamp de Expresiones Regulares!** 🎉
