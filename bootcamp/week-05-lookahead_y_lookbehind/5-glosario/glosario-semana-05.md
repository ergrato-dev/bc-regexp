# Glosario - Semana 05: Lookahead y Lookbehind

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### A

#### Assertion

**Descripción:** Condición que debe cumplirse en una posición sin consumir caracteres. Los lookarounds son un tipo de assertion.

```javascript
/**
 * ¿Por qué? Necesitamos verificar contexto sin incluirlo en el match
 * ¿Para qué? Validaciones complejas, extracción condicional
 */

// Assertions de posición
^    // Inicio de string
$    // Fin de string
\b   // Word boundary

// Assertions de lookaround
(?=...)   // Positive lookahead
(?!...)   // Negative lookahead
(?<=...)  // Positive lookbehind
(?<!...)  // Negative lookbehind
```

---

### L

#### Lookahead

**Descripción:** Assertion que verifica si un patrón existe **adelante** (a la derecha) de la posición actual.

```javascript
/**
 * Positive lookahead: (?=...)
 * ¿Por qué? Verificar que algo sigue sin incluirlo
 * ¿Para qué? Capturar condicionalmente
 */
/\d+(?=€)/g.exec('100€'); // ['100'] - sin el €

/**
 * Negative lookahead: (?!...)
 * ¿Por qué? Excluir cuando algo sigue
 * ¿Para qué? Filtrar matches no deseados
 */
/Java(?!Script)/g; // "Java" pero NO "JavaScript"
```

---

#### Lookbehind

**Descripción:** Assertion que verifica si un patrón existe **atrás** (a la izquierda) de la posición actual.

```javascript
/**
 * Positive lookbehind: (?<=...)
 * ¿Por qué? Verificar que algo precede sin incluirlo
 * ¿Para qué? Extraer valores por contexto
 */
/(?<=\$)\d+/g.exec('$100'); // ['100'] - sin el $

/**
 * Negative lookbehind: (?<!...)
 * ¿Por qué? Excluir cuando algo precede
 * ¿Para qué? Filtrar por contexto anterior
 */
/(?<!\$)\d+/g; // Números NO precedidos de $
```

**Nota:** Lookbehind fue añadido en ES2018.

---

### Z

#### Zero-Width

**Descripción:** Característica de los lookarounds: no consumen caracteres del string, solo verifican una condición.

```javascript
/**
 * ¿Por qué? Queremos verificar sin alterar el match
 * ¿Para qué? Validaciones múltiples en la misma posición
 */

// Los lookarounds son "zero-width"
'100€'.match(/\d+(?=€)/); // ['100'] - € no está en el match
'100€'.match(/\d+€/); // ['100€'] - € sí está en el match
```

---

## Tabla Comparativa

### Lookahead vs Lookbehind

| Característica    | Lookahead    | Lookbehind   |
| ----------------- | ------------ | ------------ |
| Dirección         | Adelante (→) | Atrás (←)    |
| Sintaxis positiva | `(?=...)`    | `(?<=...)`   |
| Sintaxis negativa | `(?!...)`    | `(?<!...)`   |
| Soporte           | Desde ES3    | Desde ES2018 |
| Consume texto     | No           | No           |

### Positive vs Negative

| Tipo       | Positive                | Negative                   |
| ---------- | ----------------------- | -------------------------- |
| Lookahead  | `(?=...)` debe existir  | `(?!...)` NO debe existir  |
| Lookbehind | `(?<=...)` debe existir | `(?<!...)` NO debe existir |
| Uso        | Incluir si...           | Excluir si...              |

---

## Patrones de Validación con Lookarounds

### Password con Múltiples Requisitos

```javascript
/**
 * Patrón: Validación completa de password
 *
 * ¿Por qué? Múltiples condiciones simultáneas
 * ¿Para qué? Seguridad de cuentas
 */
const passwordPattern = /^
  (?=.*[A-Z])        // Al menos una mayúscula
  (?=.*[a-z])        // Al menos una minúscula
  (?=.*\d)           // Al menos un dígito
  (?=.*[!@#$%])      // Al menos un especial
  (?!.*\s)           // Sin espacios
  .{8,}              // Mínimo 8 caracteres
$/;
```

### Número con Formato

```javascript
/**
 * Insertar separadores de miles
 *
 * ¿Por qué? Los números grandes son difíciles de leer
 * ¿Para qué? Formateo visual
 */
const separadorPattern = /\B(?=(\d{3})+(?!\d))/g;

'1234567'.replace(separadorPattern, ','); // "1,234,567"
```

### Extracción Contextual

```javascript
/**
 * Extraer valores por contexto
 *
 * ¿Por qué? Solo queremos datos en un contexto específico
 * ¿Para qué? Parsing inteligente
 */

// Precio en euros (solo el número)
/\d+(?:,\d{2})?(?=\s*€)/g

// ID después de "id="
/(?<=id=["'])[^"']+(?=["'])/g
```

---

## Casos de Uso Comunes

### 1. Validación Sin Captura

```javascript
// Verificar formato sin capturar partes
/^(?=.*@)(?=.*\.).+$/; // Tiene @ y . (email básico)
```

### 2. Exclusión de Patrones

```javascript
// Palabras que NO sean artículos
/\b(?!the|a|an)\w+\b/gi;
```

### 3. Reemplazo Condicional

```javascript
// Añadir prefijo solo si no existe
texto.replace(/(?<!https?:\/\/)www\./g, 'https://www.');
```

### 4. Validación Multi-Requisito

```javascript
// Username válido
/^(?!.*__)(?!.*\.\.)(?![._])[a-zA-Z][a-zA-Z0-9._]{2,19}(?<![._])$/;
```

---

## Errores Frecuentes

### 1. Esperar que consuman texto

```javascript
// ❌ Esperando que € esté en el match
/\d+(?=€)/.exec('100€'); // ['100'], no ['100€']

// ✅ Si quieres incluirlo, no uses lookahead
/\d+€/.exec('100€'); // ['100€']
```

### 2. Compatibilidad

```javascript
// ❌ Lookbehind en navegadores antiguos
/(?<=\$)\d+/; // Error en IE, Safari < 16.4

// ✅ Alternativa con grupo
const match = /\$(\d+)/.exec('$100');
const valor = match ? match[1] : null; // "100"
```

### 3. Confundir dirección

```javascript
// Lookahead: mira ADELANTE (derecha)
/foo(?=bar)/   // "foo" si le sigue "bar"

// Lookbehind: mira ATRÁS (izquierda)
/(?<=foo)bar/  // "bar" si le precede "foo"
```

---

## Visualización

```
Texto: "Precio: $100 USD"

Posición del cursor:        ↓
                    Precio: $100 USD
                              ↑
                           cursor

Lookbehind (?<=\$)          Lookahead (?=\s)
     ←                           →
    mira                        mira
   atrás                      adelante
```

---

**Próxima semana:** Flags y Modificadores (`g`, `i`, `m`, `s`, `u`)
