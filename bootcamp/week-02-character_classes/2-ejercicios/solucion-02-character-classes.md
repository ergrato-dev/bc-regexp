# Soluciones - Ejercicios Semana 02

> ⚠️ **Importante:** Intenta resolver los ejercicios antes de ver las soluciones.

---

## Ejercicio 01: Character Classes Básicas

### Soluciones

```javascript
/**
 * Tarea 1: Vocales minúsculas entre 'c' y 'sa'
 *
 * ¿Por qué? Solo queremos las variantes con vocales minúsculas
 * ¿Para qué? Filtrar resultados específicos
 */
const pattern1 = /c[aeiou]sa/g;
// Matches: casa, cosa, cesa, cisa, cusa

/**
 * Tarea 2: Vocales mayúsculas O minúsculas
 *
 * ¿Por qué? Queremos ser case-insensitive para las vocales
 * ¿Para qué? Capturar todas las variantes
 */
const pattern2 = /c[aeiouAEIOU]sa/g;
// Matches: casa, cosa, cesa, cisa, cusa, cAsa, cOsa, cEsa

/**
 * Tarea 3: Cualquier cosa EXCEPTO vocales
 *
 * ¿Por qué? La negación [^...] excluye los caracteres listados
 * ¿Para qué? Encontrar las variantes "raras"
 */
const pattern3 = /c[^aeiouAEIOU]sa/g;
// Matches: c1sa, c@sa, c-sa
```

---

## Ejercicio 02: Rangos

### Soluciones

```javascript
/**
 * Tarea 1: Letra mayúscula + dígito
 *
 * ¿Por qué? Combinamos dos character classes consecutivas
 * ¿Para qué? Encontrar códigos tipo "A1", "B2"
 */
const pattern1 = /[A-Z]\d/g;
// o: /[A-Z][0-9]/g
// Matches: A1, B2, C3, Z9, M5

/**
 * Tarea 2: Dígito + letra mayúscula
 *
 * ¿Por qué? El orden importa en regex
 * ¿Para qué? Encontrar formatos invertidos
 */
const pattern2 = /\d[A-Z]/g;
// Matches: 1A, 2B, 3C

/**
 * Tarea 3: NO letra ni dígito
 *
 * ¿Por qué? Buscamos caracteres especiales
 * ¿Para qué? Detectar símbolos
 */
const pattern3 = /[^a-zA-Z0-9]/g;
// Matches: @, #, $, %, ^, &, espacios

/**
 * Tarea 4: Minúscula + dígito
 *
 * ¿Por qué? Similar a tarea 1 pero con minúsculas
 * ¿Para qué? Patrones case-sensitive
 */
const pattern4 = /[a-z]\d/g;
// Matches: a1, b2, c3, z9, m5
```

---

## Ejercicio 03: Shorthand Classes

### Soluciones

```javascript
/**
 * Tarea 1: Solo word characters (de inicio a fin)
 *
 * ¿Por qué? \w+ captura uno o más word characters
 * ¿Para qué? Validar usernames simples
 */
const pattern1 = /^\w+$/;
// Matches: usuario123, user_name, 12345

/**
 * Tarea 2: Contiene whitespace
 *
 * ¿Por qué? \s detecta cualquier espacio en blanco
 * ¿Para qué? Identificar strings con espacios
 */
const pattern2 = /\s/;
// Matches en: "user name", "   espacios   "

/**
 * Tarea 3: Solo dígitos
 *
 * ¿Por qué? \d+ solo dígitos de inicio a fin
 * ¿Para qué? Validar números enteros
 */
const pattern3 = /^\d+$/;
// Matches: 12345

/**
 * Tarea 4: Contiene caracteres NO word
 *
 * ¿Por qué? \W es la negación de \w
 * ¿Para qué? Detectar caracteres especiales
 */
const pattern4 = /\W/;
// Matches en: user-name, user name, user@name, "   espacios   "
```

---

## Ejercicio 04: Word Boundaries

### Soluciones

```javascript
/**
 * Tarea 1: "cat" como palabra completa
 *
 * ¿Por qué? \b marca los límites de palabra
 * ¿Para qué? Evitar matches dentro de otras palabras
 */
const pattern1 = /\bcat\b/gi;
// Matches: "cat" (línea 1), "Cat" (línea 4)

/**
 * Tarea 2: "the" como palabra completa
 *
 * ¿Por qué? Misma lógica, aplicada a "the"
 * ¿Para qué? Contar artículos, no "there", "theater"
 */
const pattern2 = /\bthe\b/gi;
// Matches: "The" (línea 1), "the" x2 (línea 2), "the" (línea 3)

/**
 * Tarea 3: "cat" DENTRO de otra palabra
 *
 * ¿Por qué? \B es el opuesto de \b (non-boundary)
 * ¿Para qué? Encontrar substrings embebidos
 */
const pattern3 = /\Bcat\B/gi;
// Matches en: "Concatenate" (el 'cat' del medio)

// Nota: \Bcat\B requiere que NO haya boundary en ningún lado
// "category" tiene cat al inicio, así que \Bcat no matchea
// Para encontrar cat que no esté solo, mejor:
const pattern3b = /\Bcat|cat\B/gi;
// Esto encuentra cat con boundary ausente en al menos un lado

/**
 * Tarea 4: Palabras que EMPIEZAN con "cat"
 *
 * ¿Por qué? \b al inicio, sin \b al final
 * ¿Para qué? Buscar palabras por prefijo
 */
const pattern4 = /\bcat/gi;
// Matches: "cat", "Cat", "category", "caterpillar", "categories"
// También matchea "cat" en "Concatenate" porque hay \b antes de C
// Mejor versión si queremos palabras que inicien:
const pattern4b = /\bcat\w*/gi;
```

---

## Ejercicio 05: Validaciones Prácticas

### Soluciones

```javascript
/**
 * 1. Código postal español (5 dígitos)
 *
 * ¿Por qué? Exactamente 5 dígitos, nada más
 * ¿Para qué? Validar direcciones españolas
 */
const codigoPostal = /^\d\d\d\d\d$/;
// o en semana 03: /^\d{5}$/

codigoPostal.test('28001'); // true
codigoPostal.test('08080'); // true
codigoPostal.test('2800'); // false
codigoPostal.test('2800A'); // false

/**
 * 2. Inicial + número de 2 dígitos (A-99)
 *
 * ¿Por qué? Una mayúscula, guión, dos dígitos
 * ¿Para qué? Códigos de sección/categoría
 */
const inicialNumero = /^[A-Z]-\d\d$/;

inicialNumero.test('A-01'); // true
inicialNumero.test('Z-99'); // true
inicialNumero.test('AB-01'); // false
inicialNumero.test('a-01'); // false

/**
 * 3. Código hexadecimal de 3 caracteres
 *
 * ¿Por qué? Colores cortos como #F00 (sin el #)
 * ¿Para qué? Validar valores hex
 */
const hex3 = /^[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]$/;
// o: /^[0-9a-fA-F]{3}$/ en semana 03

hex3.test('F00'); // true
hex3.test('ABC'); // true
hex3.test('1a2'); // true
hex3.test('GGG'); // false
hex3.test('XYZ'); // false

/**
 * 4. Nombre simple (mayúscula inicial + minúsculas)
 *
 * ¿Por qué? Formato típico de nombre propio
 * ¿Para qué? Normalizar y validar nombres
 */
const nombre = /^[A-Z][a-z]+$/; // + requiere al menos 1 minúscula

nombre.test('Juan'); // true
nombre.test('Ana'); // true
nombre.test('juan'); // false (no empieza mayúscula)
nombre.test('JUAN'); // false (resto en mayúscula)
nombre.test('J'); // false (sin minúsculas después)
```

---

## Ejercicio 06: Caracteres Especiales en Classes

### Soluciones

```javascript
/**
 * 1. Encontrar $
 *
 * ¿Por qué? $ no es especial dentro de []
 * ¿Para qué? Buscar símbolos de moneda
 */
const dolar = /[$]/; // o simplemente /\$/
// Match: "$100"

/**
 * 2. Encontrar guión -
 *
 * ¿Por qué? El guión es especial (define rangos)
 * ¿Para qué? Buscar guiones literales
 */
const guion = /[-]/; // Al inicio
// o: /[a-z-]/            // Al final del rango
// o: /[a\-z]/            // Escapado (entre caracteres)
// Match: "1-10"

/**
 * 3. Encontrar [ o ]
 *
 * ¿Por qué? ] cierra la clase, necesita escape
 * ¿Para qué? Buscar sintaxis de arrays
 */
const corchetes = /[\[\]]/g;
// Match: "[", "]" en "array[0]"

/**
 * 4. Encontrar ^
 *
 * ¿Por qué? ^ al inicio de [] significa negación
 * ¿Para qué? Buscar el símbolo literal
 */
const circunflejo = /[\^]/; // Escapado
// o: /[a^]/               // No al inicio
// Match: "a^b"

/**
 * 5. Encontrar \
 *
 * ¿Por qué? \ siempre necesita escape
 * ¿Para qué? Buscar paths de Windows
 */
const backslash = /[\\]/;
// Match: "C:\Users"
```

---

## Desafío Extra 🔥

### Solución

```javascript
/**
 * Teléfono móvil español (9 dígitos, empieza con 6, 7, 8, 9)
 * Sin espacios
 *
 * ¿Por qué? Los móviles españoles empiezan con 6 o 7
 *           Los fijos con 9, y algunos servicios con 8
 * ¿Para qué? Validar números de contacto
 */
const movilSinEspacios = /^[6789]\d\d\d\d\d\d\d\d$/;

movilSinEspacios.test('612345678'); // true
movilSinEspacios.test('912345678'); // true
movilSinEspacios.test('12345678'); // false (no empieza bien)

/**
 * Móvil con espacios (formato: 6XX XXX XXX)
 *
 * ¿Por qué? Es un formato común de escritura
 * ¿Para qué? Aceptar input formateado
 */
const movilConEspacios = /^[67]\d\d \d\d\d \d\d\d$/;

movilConEspacios.test('612 345 678'); // true
movilConEspacios.test('612345678'); // false (sin espacios)

/**
 * Fijo con espacios (formato: 9X XXX XX XX)
 *
 * ¿Por qué? Fijos españoles tienen otro formato visual
 * ¿Para qué? Validar teléfonos de empresa
 */
const fijoConEspacios = /^9\d \d\d\d \d\d \d\d$/;

fijoConEspacios.test('91 234 56 78'); // true

/**
 * Validador combinado (sin cuantificadores avanzados)
 *
 * ¿Por qué? En la práctica queremos aceptar varios formatos
 * ¿Para qué? Una única función de validación
 */
function validarTelefono(tel) {
  const sinEspacios = /^[6789]\d\d\d\d\d\d\d\d$/;
  const movilEsp = /^[67]\d\d \d\d\d \d\d\d$/;
  const fijoEsp = /^9\d \d\d\d \d\d \d\d$/;

  return sinEspacios.test(tel) || movilEsp.test(tel) || fijoEsp.test(tel);
}

console.log(validarTelefono('612345678')); // true
console.log(validarTelefono('612 345 678')); // true
console.log(validarTelefono('91 234 56 78')); // true
console.log(validarTelefono('12345678')); // false
```

### Nota

Con los cuantificadores de la semana 03, podremos escribir patrones mucho más elegantes:

```javascript
// Semana 03 preview:
const telefono = /^[6-9]\d{8}$/; // 9 dígitos
const conEspacios = /^[6-9](\d{2,3}\s?)+$/; // Con espacios opcionales
```

---

## Resumen de Patrones Aprendidos

| Concepto        | Sintaxis | Ejemplo      | Descripción           |
| --------------- | -------- | ------------ | --------------------- |
| Character class | `[abc]`  | `/[aeiou]/`  | Uno de estos          |
| Negación        | `[^abc]` | `/[^0-9]/`   | Ninguno de estos      |
| Rango           | `[a-z]`  | `/[A-Za-z]/` | Rango de caracteres   |
| Dígito          | `\d`     | `/\d\d\d/`   | Un dígito             |
| Word char       | `\w`     | `/\w+/`      | Letra, dígito, \_     |
| Whitespace      | `\s`     | `/\s/`       | Espacio, tab, newline |
| Word boundary   | `\b`     | `/\bcat\b/`  | Límite de palabra     |

---

**Siguiente:** Proyecto de la semana en `3-proyecto/`
