# Backreferences (Retro-referencias)

## ¿Qué son las Backreferences?

Las **backreferences** permiten hacer referencia a un grupo de captura **dentro del mismo patrón**. Esto es útil para encontrar texto repetido o validar que dos partes coincidan.

## Sintaxis

```javascript
\1  // Referencia al grupo 1
\2  // Referencia al grupo 2
\n  // Referencia al grupo n
```

Con named groups:

```javascript
\k<nombre>  // Referencia al grupo con ese nombre
```

## Ejemplo Básico

```javascript
/**
 * Patrón: Encontrar palabras duplicadas
 *
 * ¿Por qué? Los errores tipográficos incluyen palabras repetidas
 * ¿Para qué? Detectar errores como "el el" o "que que"
 *
 * Desglose:
 * (\w+)  → Grupo 1: captura una palabra
 * \s+    → Uno o más espacios
 * \1     → Backreference: la misma palabra del grupo 1
 */
const duplicadaPattern = /(\w+)\s+\1/gi;

const texto = 'El el gato gato saltó sobre la la cerca';
console.log(texto.match(duplicadaPattern));
// ['El el', 'gato gato', 'la la']
```

## Casos de Uso

### 1. Validar Etiquetas HTML

```javascript
/**
 * Patrón: Etiqueta HTML con cierre correcto
 *
 * ¿Por qué? La etiqueta de cierre debe coincidir con la de apertura
 * ¿Para qué? Validar HTML básico
 *
 * Desglose:
 * <(\w+)>     → Grupo 1: nombre de etiqueta de apertura
 * .*?         → Contenido (lazy)
 * <\/\1>      → Backreference: misma etiqueta en cierre
 */
const htmlPattern = /<(\w+)>.*?<\/\1>/gs;

const html = '<div>contenido</div> <span>texto</span> <p>párrafo</div>';
console.log(html.match(htmlPattern));
// ['<div>contenido</div>', '<span>texto</span>']
// Nota: <p>párrafo</div> NO coincide porque p ≠ div
```

### 2. Detectar Palíndromos Simples

```javascript
/**
 * Patrón: Palabras de 3 letras palíndromas
 *
 * ¿Por qué? Primera y última letra deben ser iguales
 * ¿Para qué? Encontrar patrones simétricos
 */
const palindromo3 = /\b(\w)\w\1\b/gi;

const texto = 'ojo ala oso perro gato pop';
console.log(texto.match(palindromo3));
// ['ojo', 'ala', 'oso', 'pop']
```

### 3. Validar Comillas Consistentes

```javascript
/**
 * Patrón: Texto entre comillas (simples o dobles)
 *
 * ¿Por qué? Las comillas de cierre deben coincidir con las de apertura
 * ¿Para qué? Extraer strings correctamente formados
 *
 * Desglose:
 * (['"])    → Grupo 1: comilla de apertura (' o ")
 * [^'"]*    → Contenido (sin comillas)
 * \1        → Backreference: misma comilla de cierre
 */
const stringPattern = /(['"])[^'"]*\1/g;

const codigo = `nombre = 'Juan', apellido = "Pérez", error = 'mixto"`;
console.log(codigo.match(stringPattern));
// ["'Juan'", '"Pérez"']
// 'mixto" NO coincide porque ' ≠ "
```

### 4. Números de Tarjeta

```javascript
/**
 * Patrón: Tarjeta con grupos de 4 dígitos separados por mismo carácter
 *
 * ¿Por qué? El separador debe ser consistente
 * ¿Para qué? Aceptar "1234-5678-9012-3456" o "1234 5678 9012 3456"
 */
const tarjetaPattern = /\d{4}([-\s])\d{4}\1\d{4}\1\d{4}/;

console.log(tarjetaPattern.test('1234-5678-9012-3456')); // true
console.log(tarjetaPattern.test('1234 5678 9012 3456')); // true
console.log(tarjetaPattern.test('1234-5678 9012-3456')); // false (separadores mixtos)
```

## Múltiples Backreferences

Puedes usar varias backreferences en el mismo patrón:

```javascript
/**
 * Patrón: Fecha con mismo separador
 *
 * ¿Por qué? El separador debe ser consistente (. o / o -)
 * ¿Para qué? Validar formatos de fecha uniformes
 */
const fechaPattern = /(\d{2})([.\/-])(\d{2})\2(\d{4})/;

console.log(fechaPattern.test('15/01/2024')); // true
console.log(fechaPattern.test('15.01.2024')); // true
console.log(fechaPattern.test('15-01-2024')); // true
console.log(fechaPattern.test('15/01-2024')); // false (separadores mixtos)
```

## Named Backreferences: `\k<nombre>`

Con named groups, usa `\k<nombre>`:

```javascript
/**
 * Patrón: Etiqueta HTML con named groups
 *
 * ¿Por qué? Más legible que \1
 * ¿Para qué? Código mantenible
 */
const htmlPattern = /<(?<tag>\w+)>.*?<\/\k<tag>>/gs;

const html = '<div>contenido</div>';
console.log(htmlPattern.test(html)); // true
```

## Backreferences en Reemplazos

Las backreferences también funcionan en `replace()`:

### Con `$n`

```javascript
/**
 * Convertir "Apellido, Nombre" a "Nombre Apellido"
 *
 * ¿Por qué? El formato de entrada es diferente al deseado
 * ¿Para qué? Normalizar nombres
 */
const nombre = 'García, Juan';
const resultado = nombre.replace(/(\w+),\s*(\w+)/, '$2 $1');
console.log(resultado); // "Juan García"
```

### Con Named Groups

```javascript
/**
 * Formatear fecha de DD/MM/YYYY a YYYY-MM-DD
 *
 * ¿Por qué? Convertir a formato ISO
 * ¿Para qué? Almacenar en base de datos
 */
const fecha = '15/01/2024';
const pattern = /(?<dia>\d{2})\/(?<mes>\d{2})\/(?<anio>\d{4})/;
const resultado = fecha.replace(pattern, '$<anio>-$<mes>-$<dia>');
console.log(resultado); // "2024-01-15"
```

### Con Función

```javascript
/**
 * Reemplazo dinámico con función
 *
 * ¿Por qué? Necesitamos lógica en el reemplazo
 * ¿Para qué? Transformaciones complejas
 */
const texto = 'temperatura: 20C, humedad: 65%';

const resultado = texto.replace(/(\d+)C/g, (match, grados) => {
  const fahrenheit = (grados * 9) / 5 + 32;
  return `${fahrenheit}F`;
});

console.log(resultado); // "temperatura: 68F, humedad: 65%"
```

## Limitaciones

### 1. JavaScript no soporta referencias hacia adelante

```javascript
// ❌ No funciona en JavaScript
/(\1b|a)+/; // No puedes referenciar grupo 1 antes de definirlo
```

### 2. Grupos no participantes

Si un grupo no coincide (es opcional y no se usó), la backreference falla:

```javascript
const pattern = /(a)?b\1/;

console.log(pattern.test('aba')); // true
console.log(pattern.test('b')); // false (grupo 1 no coincidió)
```

## Ejemplos Avanzados

### Detectar Secuencias Repetidas

```javascript
/**
 * Patrón: Encontrar cualquier carácter repetido consecutivamente
 *
 * ¿Por qué? Detectar errores tipográficos o patrones
 * ¿Para qué? Limpieza de texto
 */
const repetidoPattern = /(.)\1+/g;

console.log('Holaaa, ¿cóooomo estás???'.match(repetidoPattern));
// ['aaa', 'oooo', '???']
```

### Validar Rimas

```javascript
/**
 * Patrón: Palabras que terminan igual
 *
 * ¿Por qué? Las rimas comparten terminación
 * ¿Para qué? Análisis de poesía
 */
const rimaPattern = /\b\w*(\w{3})\b.*\b\w*\1\b/i;

console.log(rimaPattern.test('corazón y canción')); // true (ón)
console.log(rimaPattern.test('amor y dolor')); // true (lor)
console.log(rimaPattern.test('gato y perro')); // false
```

### Invertir Palabras Compuestas

```javascript
/**
 * Invertir orden en palabras guionadas
 *
 * ¿Por qué? Cambiar "agua-fuego" a "fuego-agua"
 * ¿Para qué? Transformación de texto
 */
const texto = 'norte-sur, este-oeste, arriba-abajo';
const resultado = texto.replace(/(\w+)-(\w+)/g, '$2-$1');
console.log(resultado);
// "sur-norte, oeste-este, abajo-arriba"
```

## Resumen

| Sintaxis     | Descripción                | Ejemplo                        |
| ------------ | -------------------------- | ------------------------------ |
| `\1`         | Backreference al grupo 1   | `(\w+)\s+\1`                   |
| `\n`         | Backreference al grupo n   | `(a)(b)\2\1` → "abba"          |
| `\k<nombre>` | Backreference por nombre   | `(?<x>a)\k<x>`                 |
| `$1`         | En replace: grupo 1        | `.replace(/(a)/, "$1b")`       |
| `$<nombre>`  | En replace: grupo nombrado | `.replace(/(?<x>a)/, "$<x>b")` |

---

**Anterior:** [Grupos de Captura](01-grupos-captura.md)

**Siguiente:** [Ejercicios de Grupos](../2-ejercicios/ejercicio-04-grupos.md)
