# Semana 01: Métodos de RegExp en JavaScript

## Introducción

JavaScript proporciona varios métodos para trabajar con expresiones regulares. Es fundamental conocerlos para aplicar lo aprendido.

## Métodos del Objeto RegExp

### `test()` - Verificar Existencia

```javascript
/**
 * ¿Por qué? Es el método más simple para verificar si hay match
 * ¿Para qué? Validaciones booleanas (sí/no existe el patrón)
 *
 * Retorna: boolean (true/false)
 */
const pattern = /gato/;

pattern.test('El gato duerme'); // true
pattern.test('El perro ladra'); // false
```

### `exec()` - Extraer Información

```javascript
/**
 * ¿Por qué? A veces necesitamos más que un simple true/false
 * ¿Para qué? Obtener detalles del match: texto, posición, grupos
 *
 * Retorna: Array con información o null
 */
const pattern = /gato/;
const resultado = pattern.exec('El gato negro');

console.log(resultado);
// [
//   'gato',        // El match encontrado
//   index: 3,      // Posición donde empieza
//   input: 'El gato negro',  // String original
//   groups: undefined  // Grupos nombrados (si hay)
// ]
```

## Métodos del Objeto String

### `match()` - Encontrar Coincidencias

```javascript
/**
 * ¿Por qué? Es más natural llamar el método desde el string
 * ¿Para qué? Obtener todas las coincidencias de un patrón
 */

// Sin flag 'g' - retorna igual que exec()
const texto = 'El gato y otro gato';
texto.match(/gato/); // ['gato', index: 3, ...]

// Con flag 'g' - retorna TODOS los matches
texto.match(/gato/g); // ['gato', 'gato']
```

### `search()` - Encontrar Posición

```javascript
/**
 * ¿Por qué? A veces solo necesitamos saber DÓNDE está el match
 * ¿Para qué? Obtener el índice de la primera coincidencia
 *
 * Retorna: índice (number) o -1 si no encuentra
 */
const texto = 'Hola mundo';

texto.search(/mundo/); // 5
texto.search(/xyz/); // -1
```

### `replace()` - Buscar y Reemplazar

```javascript
/**
 * ¿Por qué? Una de las operaciones más comunes con regex
 * ¿Para qué? Transformar texto basándose en patrones
 */

// Reemplazo simple (solo el primero)
'gato gato'.replace(/gato/, 'perro'); // "perro gato"

// Reemplazo global (todos)
'gato gato'.replace(/gato/g, 'perro'); // "perro perro"
```

### `split()` - Dividir por Patrón

```javascript
/**
 * ¿Por qué? El separador a veces varía o tiene un patrón
 * ¿Para qué? Dividir strings de forma más flexible que split simple
 */

// Dividir por uno o más espacios
const texto = 'uno   dos  tres';
texto.split(/\s+/); // ['uno', 'dos', 'tres']

// Dividir por coma y espacios opcionales
'a, b,c,  d'.split(/,\s*/); // ['a', 'b', 'c', 'd']
```

### `matchAll()` - Iterar Coincidencias (ES2020+)

```javascript
/**
 * ¿Por qué? match() con flag 'g' pierde información de grupos
 * ¿Para qué? Obtener información completa de CADA match
 *
 * Requiere: flag 'g' obligatorio
 * Retorna: Iterator
 */
const texto = 'gato1 gato2 gato3';
const pattern = /gato(\d)/g;

for (const match of texto.matchAll(pattern)) {
  console.log(match[0], match[1], match.index);
}
// gato1 1 0
// gato2 2 6
// gato3 3 12
```

## Comparación de Métodos

```
┌──────────────┬─────────────────────┬────────────────────────────┐
│    Método    │      Retorna        │          Uso               │
├──────────────┼─────────────────────┼────────────────────────────┤
│ test()       │ boolean             │ ¿Existe el patrón?         │
│ exec()       │ Array | null        │ Info detallada del match   │
│ match()      │ Array | null        │ Encontrar coincidencias    │
│ matchAll()   │ Iterator            │ Iterar todos los matches   │
│ search()     │ number              │ Posición del primer match  │
│ replace()    │ string              │ Buscar y reemplazar        │
│ split()      │ Array               │ Dividir por patrón         │
└──────────────┴─────────────────────┴────────────────────────────┘
```

## Creación de RegExp

Hay dos formas de crear una expresión regular:

### 1. Notación Literal

```javascript
/**
 * ¿Por qué? Es la forma más común y legible
 * ¿Para qué? Cuando el patrón es conocido en tiempo de escritura
 */
const pattern = /hola/gi;
```

### 2. Constructor RegExp

```javascript
/**
 * ¿Por qué? A veces el patrón se construye dinámicamente
 * ¿Para qué? Crear patrones basados en variables o input del usuario
 */
const busqueda = 'hola';
const pattern = new RegExp(busqueda, 'gi');

// ⚠️ Cuidado: hay que escapar backslashes
const digitos = new RegExp('\\d+'); // Equivale a /\d+/
```

## Ejemplo Práctico Integrado

```javascript
/**
 * Validador de formato de hora (HH:MM)
 *
 * ¿Por qué? Los usuarios ingresan horas en diferentes formatos
 * ¿Para qué? Asegurar que la hora tenga el formato correcto antes de procesarla
 */

const horaPattern = /^\d{2}:\d{2}$/;
//                   │  │   │  │ │
//                   │  │   │  │ └─ Fin del string
//                   │  │   │  └─── Exactamente 2 dígitos (minutos)
//                   │  │   └────── Dos puntos literal
//                   │  └────────── Exactamente 2 dígitos (hora)
//                   └─────────────  Inicio del string

function validarHora(hora) {
  if (horaPattern.test(hora)) {
    return `✅ "${hora}" es válida`;
  } else {
    return `❌ "${hora}" no tiene formato HH:MM`;
  }
}

console.log(validarHora('09:30')); // ✅ "09:30" es válida
console.log(validarHora('9:30')); // ❌ "9:30" no tiene formato HH:MM
console.log(validarHora('12:5')); // ❌ "12:5" no tiene formato HH:MM
console.log(validarHora('25:00')); // ✅ "25:00" es válida (formato ok, valor no)
```

> **Nota:** Este patrón valida el **formato**, no el **valor**. Validar que la hora sea lógica (0-23, 0-59) requiere lógica adicional o un patrón más complejo.

---

**Siguiente:** Ejercicios prácticos para aplicar lo aprendido.
