# Glosario - Semana 03: Quantifiers

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### B

#### Backtracking

**Descripción:** Proceso donde el motor de regex "retrocede" para probar alternativas cuando un match falla.

```javascript
// Con .*? el motor avanza poco a poco
/".*?"/
// Prueba "", luego "a", luego "ab"... hasta encontrar "

// Con .* el motor captura todo y retrocede
/".*"/
// Captura todo, luego suelta caracteres uno a uno
```

**Uso:** Entender el rendimiento y comportamiento de los patrones.

---

### G

#### Greedy

**Descripción:** Comportamiento por defecto de quantifiers: capturan la **mayor cantidad posible** de caracteres.

```javascript
const texto = '<div>A</div><div>B</div>';

// Greedy: captura todo
/<div>.*<\/div>/.exec(texto)[0];
// '<div>A</div><div>B</div>'
```

**Uso:** Cuando quieres capturar hasta el último delimitador.

---

### L

#### Lazy (Non-Greedy)

**Descripción:** Modificador de quantifiers (`?`) que captura la **menor cantidad posible** de caracteres.

```javascript
const texto = '<div>A</div><div>B</div>';

// Lazy: captura lo mínimo
/<div>.*?<\/div>/.exec(texto)[0];
// '<div>A</div>'
```

**Uso:** Cuando quieres capturar hasta el primer delimitador.

---

### Q

#### Quantifier

**Descripción:** Especificador que indica cuántas veces debe aparecer el elemento anterior.

```javascript
*     // Cero o más
+     // Uno o más
?     // Cero o uno
{n}   // Exactamente n
{n,m} // Entre n y m
{n,}  // Al menos n
```

**Uso:** Controlar repeticiones en patrones.

---

## Tabla de Quantifiers

### Quantifiers Básicos

| Quantifier | Nombre   | Mínimo | Máximo | Ejemplo                      |
| ---------- | -------- | ------ | ------ | ---------------------------- |
| `*`        | Asterisk | 0      | ∞      | `ab*c` → ac, abc, abbc...    |
| `+`        | Plus     | 1      | ∞      | `ab+c` → abc, abbc...        |
| `?`        | Question | 0      | 1      | `colou?r` → color, colour    |
| `{n}`      | Exact    | n      | n      | `\d{5}` → 12345              |
| `{n,m}`    | Range    | n      | m      | `\d{3,5}` → 123, 1234, 12345 |
| `{n,}`     | Minimum  | n      | ∞      | `\d{3,}` → 123, 1234...      |

### Equivalencias

| Símbolo | Equivalente | Descripción |
| ------- | ----------- | ----------- |
| `*`     | `{0,}`      | Cero o más  |
| `+`     | `{1,}`      | Uno o más   |
| `?`     | `{0,1}`     | Opcional    |

### Versiones Lazy

| Greedy  | Lazy     | Comportamiento             |
| ------- | -------- | -------------------------- |
| `*`     | `*?`     | Cero o más (mínimo)        |
| `+`     | `+?`     | Uno o más (mínimo)         |
| `?`     | `??`     | Cero o uno (prefiere cero) |
| `{n,m}` | `{n,m}?` | Entre n y m (prefiere n)   |
| `{n,}`  | `{n,}?`  | Al menos n (prefiere n)    |

---

## Patrones Comunes

### Validación de Longitud

```javascript
// Exactamente 5 caracteres
/^\w{5}$/

// Entre 8 y 16 caracteres
/^\w{8,16}$/

// Al menos 3 caracteres
/^\w{3,}$/

// Máximo 10 caracteres
/^\w{0,10}$/
```

### Elementos Opcionales

```javascript
// Protocolo http o https
/https?/

// Número con signo opcional
/[+-]?\d+/

// Decimales opcionales
/\d+(\.\d+)?/

// Plural opcional
/colou?rs?/  // color, colors, colour, colours
```

### Repeticiones

```javascript
// Uno o más dígitos
/\d+/

// Cero o más espacios
/\s*/

// Una o más palabras separadas por espacios
/\w+(\s+\w+)*/
```

---

## Greedy vs Lazy: Cuándo Usar Cada Uno

### Usa Greedy cuando:

- Quieres capturar hasta el **último** delimitador
- No hay ambigüedad en el patrón
- Estás capturando bloques completos

```javascript
// Capturar todo el path
/.*\//.exec('a/b/c/d')[0]; // "a/b/c/"
```

### Usa Lazy cuando:

- Hay **múltiples** delimitadores iguales
- Quieres el match **más corto**
- Estás extrayendo **varios elementos**

```javascript
// Capturar cada string entre comillas
/".*?"/g; // Cada par de comillas
```

### Usa Negación como Alternativa:

```javascript
// En lugar de lazy
/".*?"/

// Usa negación (más eficiente)
/"[^"]*"/
```

---

## Errores Frecuentes

### 1. Quantifier sin elemento

```javascript
// ❌ Error
/*abc/    // Error: * no tiene elemento previo
/+abc/    // Error: + no tiene elemento previo

// ✅ Correcto
/a*bc/    // 'a' cero o más veces
/a+bc/    // 'a' una o más veces
```

### 2. Espacio en `{n,m}`

```javascript
// ❌ Error
/\d{3, 5}/   // Espacio causa error

// ✅ Correcto
/\d{3,5}/    // Sin espacio
```

### 3. Confundir greedy y lazy

```javascript
const html = '<b>uno</b><b>dos</b>';

// ❌ Greedy captura de más
/<b>.*<\/b>/.exec(html)[0]; // '<b>uno</b><b>dos</b>'

// ✅ Lazy captura individual
/<b>.*?<\/b>/.exec(html)[0]; // '<b>uno</b>'
```

### 4. Olvidar el flag `g` con lazy

```javascript
const texto = '"a" "b" "c"';

// Sin flag g: solo primer match
/".*?"/.exec(texto); // ['"a"']

// Con flag g: todos los matches
texto.match(/".*?"/g); // ['"a"', '"b"', '"c"']
```

---

## Rendimiento

### Patrones Problemáticos

```javascript
// ⚠️ Backtracking catastrófico
/(a+)+$/  // Muy lento con "aaaaaaaaaaaaaaaaX"

// ⚠️ Ambiguo
/.*.*/.exec(texto);  // Dos greedy compiten
```

### Patrones Optimizados

```javascript
// ✅ Específico
/a+$/

// ✅ Sin ambigüedad
/.+/.exec(texto);

// ✅ Negación en lugar de lazy
/[^"]*/ en lugar de /.*?/
```

---

**Próxima semana:** Groups y Captures (`()`, `(?:)`, `\1`)
