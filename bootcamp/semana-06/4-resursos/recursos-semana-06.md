# Recursos - Semana 06: Flags y Modificadores

## 🖼️ Assets de la Semana

| Archivo     | Descripción                 | Vista                        |
| ----------- | --------------------------- | ---------------------------- |
| `flags.svg` | Diagrama de todos los flags | [Ver](../0-assets/flags.svg) |

## 📖 Referencia Rápida de Flags

```
┌──────┬──────────────────┬────────────────────────────────┬─────────┐
│ Flag │ Nombre           │ Descripción                    │ ES      │
├──────┼──────────────────┼────────────────────────────────┼─────────┤
│ g    │ global           │ Encontrar todas las coinciden. │ ES3     │
│ i    │ ignoreCase       │ Ignorar mayúsculas/minúsculas  │ ES3     │
│ m    │ multiline        │ ^ y $ aplican a cada línea     │ ES3     │
│ s    │ dotAll           │ . incluye \n                   │ ES2018  │
│ u    │ unicode          │ Soporte Unicode completo       │ ES2015  │
│ y    │ sticky           │ Buscar solo en lastIndex       │ ES2015  │
│ d    │ hasIndices       │ Incluir índices de grupos      │ ES2022  │
└──────┴──────────────────┴────────────────────────────────┴─────────┘
```

## 📚 Documentación

### MDN

- [Regular expression flags](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#advanced_searching_with_flags)
- [Unicode property escapes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Unicode_character_class_escape)
- [hasIndices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/hasIndices)

### JavaScript.info

- [Flags](https://javascript.info/regexp-introduction#flags)
- [Multiline mode](https://javascript.info/regexp-multiline-mode)

## 🔧 Propiedades Unicode Comunes

```
┌────────────────────────┬────────────────────────────────────────────┐
│ Propiedad              │ Descripción                                │
├────────────────────────┼────────────────────────────────────────────┤
│ \p{L} / \p{Letter}     │ Cualquier letra de cualquier idioma       │
│ \p{N} / \p{Number}     │ Cualquier tipo de número                  │
│ \p{P} / \p{Punctuation}│ Signos de puntuación                      │
│ \p{S} / \p{Symbol}     │ Símbolos matemáticos, moneda, etc.        │
│ \p{Emoji}              │ Caracteres emoji                          │
│ \p{Script=Latin}       │ Caracteres del alfabeto latino            │
│ \p{Script=Cyrillic}    │ Caracteres cirílicos                      │
│ \p{Script=Han}         │ Caracteres chinos (Han)                   │
│ \p{Script=Arabic}      │ Caracteres árabes                         │
└────────────────────────┴────────────────────────────────────────────┘
```

## ⚠️ Errores Comunes

### 1. Flag `g` con `match()` pierde grupos

```javascript
// ❌ Pierdes información de grupos
'a@b.com, c@d.com'.match(/(\w+)@(\w+)/g);
// ['a@b.com', 'c@d.com']

// ✅ Usa matchAll
for (const m of 'a@b.com, c@d.com'.matchAll(/(\w+)@(\w+)/g)) {
  console.log(m[1], m[2]);
}
```

### 2. Olvidar flag `m` para multilínea

```javascript
const texto = 'Línea 1\nLínea 2';

// ❌ Solo primera línea
texto.match(/^Línea/g); // ['Línea']

// ✅ Todas las líneas
texto.match(/^Línea/gm); // ['Línea', 'Línea']
```

### 3. Emojis sin flag `u`

```javascript
// ❌ Emoji se rompe en dos
'😀'.match(/./g); // ['�', '�']

// ✅ Emoji correcto
'😀'.match(/./gu); // ['😀']
```

### 4. Compatibilidad de `s` y `d`

```javascript
// ⚠️ Flag s: ES2018+ (Chrome 62+, Firefox 78+)
// ⚠️ Flag d: ES2022 (Chrome 90+, Firefox 88+)

// Alternativa para s:
/[\s\S]*/; // En lugar de /.*/s
```

## 💡 Tips

```javascript
// Acceder a flags de una regex
const regex = /patrón/gimu;
regex.flags; // "gimu"
regex.global; // true
regex.ignoreCase; // true

// Combinar flags en constructor
new RegExp('patrón', 'gi');

// Copiar regex con flags diferentes
const original = /test/i;
const nuevo = new RegExp(original.source, 'gi');

// Verificar soporte de flag
const supportsLookbehind = (() => {
  try {
    new RegExp('(?<=a)b');
    return true;
  } catch {
    return false;
  }
})();
```

## 🧪 Práctica Adicional

### Ejercicios Recomendados

1. Crear un buscador de texto con todas las opciones de flags
2. Parser de archivo de configuración (INI, YAML simple)
3. Tokenizer para un mini-lenguaje

### Patrones Útiles

| Uso               | Patrón              | Flags |
| ----------------- | ------------------- | ----- |
| Palabras global   | `/\w+/`             | `g`   |
| Buscar insensible | `/hello/`           | `gi`  |
| Inicio de línea   | `/^#.+$/`           | `gm`  |
| HTML multilínea   | `/<div>.*?<\/div>/` | `gs`  |
| Letras Unicode    | `/\p{Letter}+/`     | `gu`  |
| Token en posición | `/\d+/`             | `y`   |
| Con posiciones    | `/(\w+)/`           | `gd`  |

## 🔗 Artículos Útiles

- [ES2018 dotAll flag](https://v8.dev/features/regexp-dotall-mode)
- [Named capture groups](https://v8.dev/features/regexp-named-captures)
- [Unicode property escapes](https://v8.dev/features/regexp-unicode-property-escapes)
- [Match indices](https://v8.dev/features/regexp-match-indices)

---

**Próxima semana:** Patrones Avanzados y Optimización
