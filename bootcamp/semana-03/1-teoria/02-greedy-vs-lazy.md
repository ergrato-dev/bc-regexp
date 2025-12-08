# Semana 03: Greedy vs Lazy Quantifiers

## El Comportamiento por Defecto: Greedy

Por defecto, los quantifiers son **greedy** (codiciosos): intentan capturar **la mayor cantidad posible** de caracteres.

```javascript
/**
 * ¿Por qué? El motor de regex intenta maximizar el match
 * ¿Para qué? Entender por qué a veces capturamos más de lo esperado
 */
const texto = '<div>Hola</div><div>Mundo</div>';

// Greedy: captura todo lo posible
const greedy = /<div>.*<\/div>/;
texto.match(greedy);
// ['<div>Hola</div><div>Mundo</div>']
// ↑ Capturó TODO, no solo el primer <div>

// ¿Por qué pasó esto?
// .* = "cualquier carácter, cuantos más mejor"
// Captura hasta el ÚLTIMO </div>
```

### Visualización del Proceso Greedy

```
Texto:    <div>Hola</div><div>Mundo</div>
Patrón:   <div>.*</div>

Paso 1: <div> coincide ✓
Paso 2: .* captura TODO: "Hola</div><div>Mundo</div>"
Paso 3: Busca </div>... ¡no queda nada!
Paso 4: Backtrack: .* suelta un carácter a la vez
Paso 5: .* = "Hola</div><div>Mundo</div" (soltó ">")
Paso 6: Busca </div>... no coincide
...
Paso N: .* = "Hola</div><div>Mundo"
Paso N+1: </div> coincide ✓

Resultado: "<div>Hola</div><div>Mundo</div>"
```

## La Solución: Lazy (Non-Greedy)

Añadiendo `?` después del quantifier, lo convertimos en **lazy** (perezoso): captura **la menor cantidad posible**.

```javascript
/**
 * ¿Por qué? Queremos el match más corto posible
 * ¿Para qué? Capturar elementos individuales, no todo
 */
const texto = '<div>Hola</div><div>Mundo</div>';

// Lazy: captura lo mínimo
const lazy = /<div>.*?<\/div>/;
texto.match(lazy);
// ['<div>Hola</div>']
// ↑ Solo el primer <div>

// Con flag 'g' captura todos
const lazyGlobal = /<div>.*?<\/div>/g;
texto.match(lazyGlobal);
// ['<div>Hola</div>', '<div>Mundo</div>']
```

### Visualización del Proceso Lazy

```
Texto:    <div>Hola</div><div>Mundo</div>
Patrón:   <div>.*?</div>

Paso 1: <div> coincide ✓
Paso 2: .*? intenta capturar NADA (0 caracteres)
Paso 3: Busca </div>... "Hola" no coincide
Paso 4: .*? captura "H"
Paso 5: Busca </div>... "ola<" no coincide
Paso 6: .*? captura "Ho"
...
Paso N: .*? captura "Hola"
Paso N+1: </div> coincide ✓

Resultado: "<div>Hola</div>"
```

## Sintaxis de Lazy Quantifiers

| Greedy  | Lazy     | Significado                |
| ------- | -------- | -------------------------- |
| `*`     | `*?`     | Cero o más (mínimo)        |
| `+`     | `+?`     | Uno o más (mínimo)         |
| `?`     | `??`     | Cero o uno (prefiere cero) |
| `{n,m}` | `{n,m}?` | Entre n y m (prefiere n)   |
| `{n,}`  | `{n,}?`  | Al menos n (prefiere n)    |

## Ejemplos Comparativos

### Ejemplo 1: Capturar Strings entre Comillas

```javascript
const texto = 'Dijo "hola" y luego "adiós"';

// Greedy: captura de la primera " a la última "
const greedy = /".*"/;
texto.match(greedy); // ['"hola" y luego "adiós"']

// Lazy: captura cada string individual
const lazy = /".*?"/g;
texto.match(lazy); // ['"hola"', '"adiós"']
```

### Ejemplo 2: Extraer Tags HTML

```javascript
const html = '<p>Párrafo 1</p><p>Párrafo 2</p>';

// Greedy: un solo match gigante
/<p>.*<\/p>/.exec(html)[0];
// '<p>Párrafo 1</p><p>Párrafo 2</p>'

// Lazy: cada tag individual
html.match(/<p>.*?<\/p>/g);
// ['<p>Párrafo 1</p>', '<p>Párrafo 2</p>']
```

### Ejemplo 3: Números con Decimales Opcionales

```javascript
const texto = 'Precio: 99.99 euros o 100 euros';

// Greedy en dígitos después del punto
const greedy = /\d+\.?\d*/g;
texto.match(greedy); // ['99.99', '100']

// Ambos funcionan igual aquí, pero...
const texto2 = '99.99.88';

// Sin lazy, captura todo
/\d+\.?\d*/.exec(texto2)[0]; // '99.99' (para en el segundo punto)
```

## Cuándo Usar Cada Uno

### Usa Greedy cuando:

```javascript
/**
 * ✅ Quieres capturar todo hasta el ÚLTIMO delimitador
 * ✅ No hay ambigüedad en el patrón
 * ✅ El rendimiento no es crítico
 */

// Ejemplo: capturar todo el path de una URL
const url = 'https://example.com/path/to/file.html';
url.match(/.*\//)[0]; // 'https://example.com/path/to/'
```

### Usa Lazy cuando:

```javascript
/**
 * ✅ Hay delimitadores repetidos
 * ✅ Quieres el match más corto
 * ✅ Estás extrayendo múltiples elementos
 */

// Ejemplo: extraer variables de template
const template = 'Hola {{nombre}}, tu código es {{codigo}}';
template.match(/\{\{.*?\}\}/g); // ['{{nombre}}', '{{codigo}}']
```

## Alternativa: Negación en Character Class

A veces, en lugar de lazy, puedes usar **negación** para ser más explícito:

```javascript
const texto = 'Dijo "hola" y "adiós"';

// Lazy
/".*?"/g

// Alternativa: cualquier cosa EXCEPTO comillas
/"[^"]*"/g

// La alternativa es:
// - Más explícita (claro qué caracteres acepta)
// - Más eficiente (sin backtracking)
// - A veces más difícil de escribir
```

### Comparación de Rendimiento

```javascript
/**
 * ¿Por qué? Lazy usa backtracking, negación no
 * ¿Para qué? Optimizar patrones en textos grandes
 */

// Lazy: el motor prueba y retrocede
/".*?"/

// Negación: el motor avanza directamente
/"[^"]*"/

// En textos pequeños: diferencia imperceptible
// En textos grandes: negación puede ser más rápida
```

## Caso Especial: `??` (Lazy Optional)

```javascript
/**
 * ¿Por qué? A veces queremos que algo sea opcional Y preferir no tenerlo
 * ¿Para qué? Casos específicos de parsing
 */

// ? normal (greedy): prefiere tener el carácter
const greedy = /colou?r/;
// Ambos "color" y "colour" coinciden igual

// ?? (lazy): prefiere NO tener el carácter
// Útil en combinación con grupos y alternativas
const lazy = /colou??r/;
// Técnicamente funciona igual en este caso simple
// Pero en casos complejos, afecta qué grupo captura
```

## Ejercicio Mental

Predice el resultado:

```javascript
const texto = 'aaa bbb ccc';

// ¿Qué captura cada uno?
/a+/.exec(texto)[0]; // ???
/a+?/.exec(texto)[0]; // ???
/.+/.exec(texto)[0]; // ???
/.+?/.exec(texto)[0]; // ???
/\w+\s+\w+/.exec(texto)[0]; // ???
/\w+?\s+?\w+?/.exec(texto)[0]; // ???
```

<details>
<summary>Ver respuestas</summary>

```javascript
/a+/.exec(texto)[0]; // "aaa" (todas las a's)
/a+?/.exec(texto)[0]; // "a" (solo una a)
/.+/.exec(texto)[0]; // "aaa bbb ccc" (todo)
/.+?/.exec(texto)[0]; // "a" (un carácter)
/\w+\s+\w+/.exec(texto)[0]; // "aaa bbb" (greedy en ambos \w+)
/\w+?\s+?\w+?/.exec(texto)[0]; // "aaa b" (lazy: mínimo en cada parte)
```

</details>

## Resumen Visual

```
GREEDY (por defecto)          LAZY (con ?)
────────────────────          ──────────────
Captura lo MÁXIMO             Captura lo MÍNIMO
Retrocede si falla            Avanza si falla
.*  .+  .?  {n,m}             .*?  .+?  .??  {n,m}?

Ejemplo: "abc def ghi"
/.+/  → "abc def ghi"         /.+?/ → "a"
/\w+/ → "abc"                 /\w+?/ → "a"
```

---

**Siguiente:** Ejercicios prácticos en `2-ejercicios/`
