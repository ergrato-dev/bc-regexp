# Soluciones - Ejercicios Semana 03

> ⚠️ **Importante:** Intenta resolver los ejercicios antes de ver las soluciones.

---

## Ejercicio 01: Quantifiers Básicos

### Soluciones

```javascript
/**
 * Tarea 1: "color" y "colour" (u opcional)
 *
 * ¿Por qué? La palabra tiene dos variantes válidas
 * ¿Para qué? Aceptar ambas ortografías
 */
const pattern1 = /colou?r/g;
// Matches: color, colour
// NO matchea: colouur (dos u's)

/**
 * Tarea 2: "http" y "https" (s opcional)
 *
 * ¿Por qué? Protocolos web pueden ser seguros o no
 * ¿Para qué? Validar URLs con ambos protocolos
 */
const pattern2 = /https?/g;
// Matches: http, https
// NO matchea: httttps

/**
 * Tarea 3: "file" + uno o más dígitos
 *
 * ¿Por qué? Archivos numerados deben tener al menos un número
 * ¿Para qué? Encontrar archivos con índice
 */
const pattern3 = /file\d+/g;
// Matches: file1, file12, file123
// NO matchea: file (sin dígitos)

/**
 * Tarea 4: "file" + cero o más dígitos
 *
 * ¿Por qué? Incluir archivos sin numeración
 * ¿Para qué? Capturar todos los archivos del patrón
 */
const pattern4 = /file\d*/g;
// Matches: file, file1, file12, file123
```

---

## Ejercicio 02: Quantifiers con Llaves

### Soluciones

```javascript
/**
 * Tarea 1: Exactamente 5 dígitos
 *
 * ¿Por qué? Códigos postales tienen exactamente 5 dígitos
 * ¿Para qué? Validar sin capturar números más largos
 */
const pattern1 = /\b\d{5}\b/g;
// Matches: 12345
// NO matchea: 1234, 123456 (gracias a \b)

/**
 * Tarea 2: 3 a 5 dígitos
 *
 * ¿Por qué? Algunos códigos tienen longitud variable
 * ¿Para qué? Flexibilidad en validación
 */
const pattern2 = /\b\d{3,5}\b/g;
// Matches: 123, 1234, 12345
// NO matchea: 12, 123456

/**
 * Tarea 3: Al menos 4 dígitos
 *
 * ¿Por qué? Mínimo requerido sin máximo
 * ¿Para qué? IDs que crecen con el tiempo
 */
const pattern3 = /\b\d{4,}\b/g;
// Matches: 1234, 12345, 123456, 1234567

/**
 * Tarea 4: 2 letras + 3 dígitos
 *
 * ¿Por qué? Códigos con prefijo fijo
 * ¿Para qué? Validar códigos de producto
 */
const pattern4 = /\b[A-Z]{2}\d{3}\b/g;
// Matches: AB123
// NO matchea: AB1, AB12, AB1234
```

---

## Ejercicio 03: Greedy vs Lazy

### Soluciones

```javascript
const html = '<p>Párrafo 1</p><p>Párrafo 2</p><p>Párrafo 3</p>';

/**
 * Tarea 1: Captura TODO (greedy)
 *
 * ¿Por qué? .* captura todo hasta el último </p>
 * ¿Para qué? Cuando queremos el bloque completo
 */
const greedy = /<p>.*<\/p>/;
html.match(greedy);
// ['<p>Párrafo 1</p><p>Párrafo 2</p><p>Párrafo 3</p>']

/**
 * Tarea 2: Captura CADA párrafo (lazy)
 *
 * ¿Por qué? .*? captura lo mínimo hasta el primer </p>
 * ¿Para qué? Extraer elementos individuales
 */
const lazy = /<p>.*?<\/p>/g;
html.match(lazy);
// ['<p>Párrafo 1</p>', '<p>Párrafo 2</p>', '<p>Párrafo 3</p>']

/**
 * Tarea 3: Solo el texto (sin tags)
 *
 * ¿Por qué? El grupo (.*?) captura solo el contenido
 * ¿Para qué? Extraer el texto limpio
 */
const textoSolo = /<p>(.*?)<\/p>/g;
const matches = [...html.matchAll(textoSolo)];
const textos = matches.map((m) => m[1]);
// ['Párrafo 1', 'Párrafo 2', 'Párrafo 3']
```

---

## Ejercicio 04: Validaciones con Quantifiers

### Soluciones

```javascript
/**
 * 1. Código postal español (5 dígitos)
 *
 * ¿Por qué? Los CP españoles tienen exactamente 5 dígitos
 * ¿Para qué? Validar direcciones
 */
const codigoPostal = /^\d{5}$/;
codigoPostal.test('28001'); // true
codigoPostal.test('2800'); // false
codigoPostal.test('280011'); // false

/**
 * 2. Teléfono español (9 dígitos, empieza con 6-9)
 *
 * ¿Por qué? Móviles 6/7, fijos 9, servicios 8
 * ¿Para qué? Validar números de contacto
 */
const telefono = /^[6-9]\d{8}$/;
telefono.test('612345678'); // true
telefono.test('912345678'); // true
telefono.test('12345678'); // false (no empieza con 6-9)
telefono.test('6123456789'); // false (10 dígitos)

/**
 * 3. DNI español (8 dígitos + 1 letra)
 *
 * ¿Por qué? Formato estándar de identificación
 * ¿Para qué? Validar documentos de identidad
 */
const dni = /^\d{8}[A-Z]$/;
dni.test('12345678A'); // true
dni.test('00000000Z'); // true
dni.test('1234567A'); // false (7 dígitos)
dni.test('123456789A'); // false (9 dígitos)

/**
 * 4. Contraseña (8-16 caracteres alfanuméricos)
 *
 * ¿Por qué? Seguridad básica por longitud
 * ¿Para qué? Validar registro de usuarios
 */
const password = /^[a-zA-Z0-9]{8,16}$/;
password.test('Pass1234'); // true (8)
password.test('MiClave123456'); // true (13)
password.test('Pass1'); // false (5)
password.test('EstaContraseñaEsDemasiadoLarga123'); // false (35)

/**
 * 5. Username (3-15 caracteres: letras, números, _)
 *
 * ¿Por qué? Identificadores de usuario estándar
 * ¿Para qué? Validar nombres de cuenta
 */
const username = /^\w{3,15}$/;
username.test('user'); // true
username.test('user_123'); // true
username.test('ab'); // false (2)
username.test('este_username_es_muy_largo'); // false (27)
```

---

## Ejercicio 05: Extracción de Datos

### Soluciones

```javascript
const texto = `Productos:
- Laptop: $999.99
- Mouse: $29.50
- Teclado: $149
- Monitor: $399.00

Contacto: email@example.com, otro.email@dominio.es
Teléfono: 612-345-678 o 91 234 56 78`;

/**
 * Tarea 1: Extraer precios
 *
 * ¿Por qué? Los precios pueden tener o no decimales
 * ¿Para qué? Calcular totales, mostrar en UI
 */
const precios = texto.match(/\$\d+(\.\d{2})?/g);
// ['$999.99', '$29.50', '$149', '$399.00']

// Alternativa más flexible:
const precios2 = texto.match(/\$[\d.]+/g);

/**
 * Tarea 2: Extraer emails
 *
 * ¿Por qué? Emails tienen formato usuario@dominio.ext
 * ¿Para qué? Validar/extraer contactos
 */
const emails = texto.match(/[\w.-]+@[\w.-]+\.\w+/g);
// ['email@example.com', 'otro.email@dominio.es']

/**
 * Tarea 3: Extraer teléfonos
 *
 * ¿Por qué? Los teléfonos pueden tener diferentes formatos
 * ¿Para qué? Normalizar números de contacto
 */
const telefonos = texto.match(/\d[\d\s-]{7,}\d/g);
// ['612-345-678', '91 234 56 78']

// Alternativa más específica:
const telefonos2 = texto.match(/\d{2,3}[\s-]?\d{3}[\s-]?\d{2,3}[\s-]?\d{2,3}/g);

/**
 * Tarea 4: Extraer nombres de productos
 *
 * ¿Por qué? Los productos están después de "- "
 * ¿Para qué? Listar inventario
 */
const productos = texto.match(/(?<=- )\w+/g);
// ['Laptop', 'Mouse', 'Teclado', 'Monitor']

// Sin lookbehind (más compatible):
const lineas = texto.match(/- \w+/g);
const productos2 = lineas.map((l) => l.replace('- ', ''));
```

---

## Ejercicio 06: Alternativa a Lazy

### Soluciones

```javascript
const texto = '"primera" y "segunda" y "tercera"';

/**
 * Opción 1: Lazy quantifier
 *
 * ¿Por qué? .*? captura lo mínimo
 * ¿Para qué? Solución rápida y común
 */
const lazy = /".*?"/g;
texto.match(lazy); // ['"primera"', '"segunda"', '"tercera"']

/**
 * Opción 2: Negación
 *
 * ¿Por qué? [^"]* captura todo excepto comillas
 * ¿Para qué? Más explícito y eficiente
 */
const negacion = /"[^"]*"/g;
texto.match(negacion); // ['"primera"', '"segunda"', '"tercera"']

/**
 * Comparación:
 *
 * Lazy (.*?):
 * - Más corto de escribir
 * - Usa backtracking
 * - Puede ser más lento en textos muy largos
 *
 * Negación ([^"]*):
 * - Más explícito sobre qué caracteres acepta
 * - Sin backtracking (más eficiente)
 * - Más fácil de depurar
 */
```

---

## Desafío Extra 🔥

### Solución: Parser de Logs

```javascript
const logs = `[2024-01-15 10:30:45] INFO: Usuario admin conectado
[2024-01-15 10:31:02] ERROR: Fallo en conexión a BD
[2024-01-15 10:31:15] WARN: Memoria al 85%
[2024-01-15 10:32:00] INFO: Backup completado`;

/**
 * Parser completo de logs
 *
 * ¿Por qué? Los logs tienen estructura predecible
 * ¿Para qué? Analizar eventos del sistema
 *
 * Desglose del patrón:
 * \[                           → Corchete de apertura literal
 * (\d{4}-\d{2}-\d{2})          → Grupo 1: Fecha (YYYY-MM-DD)
 * (\d{2}:\d{2}:\d{2})          → Grupo 2: Hora (HH:MM:SS)
 * \]                           → Corchete de cierre literal
 * \s+                          → Espacios
 * (\w+)                        → Grupo 3: Nivel (INFO, ERROR, WARN)
 * :\s+                         → Dos puntos y espacios
 * (.+)                         → Grupo 4: Mensaje
 */
const logPattern = /\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\] (\w+): (.+)/g;

// Versión simplificada (fecha y hora juntas)
const logPatternSimple = /\[([\d-]+ [\d:]+)\] (\w+): (.+)/g;

// Extraer todos los logs
const matches = [...logs.matchAll(logPattern)];

const logsParseados = matches.map((match) => ({
  fecha: match[1],
  hora: match[2],
  nivel: match[3],
  mensaje: match[4],
}));

console.log(logsParseados);
/*
[
  { fecha: '2024-01-15', hora: '10:30:45', nivel: 'INFO', mensaje: 'Usuario admin conectado' },
  { fecha: '2024-01-15', hora: '10:31:02', nivel: 'ERROR', mensaje: 'Fallo en conexión a BD' },
  { fecha: '2024-01-15', hora: '10:31:15', nivel: 'WARN', mensaje: 'Memoria al 85%' },
  { fecha: '2024-01-15', hora: '10:32:00', nivel: 'INFO', mensaje: 'Backup completado' }
]
*/

// Filtrar solo errores
const errores = logsParseados.filter((log) => log.nivel === 'ERROR');
console.log('Errores encontrados:', errores.length);

// Contar por nivel
const conteo = logsParseados.reduce((acc, log) => {
  acc[log.nivel] = (acc[log.nivel] || 0) + 1;
  return acc;
}, {});
console.log('Conteo por nivel:', conteo);
// { INFO: 2, ERROR: 1, WARN: 1 }
```

---

## Resumen de Quantifiers

| Quantifier | Significado    | Ejemplo   | Match            |
| ---------- | -------------- | --------- | ---------------- |
| `*`        | 0 o más        | `ab*c`    | ac, abc, abbc... |
| `+`        | 1 o más        | `ab+c`    | abc, abbc...     |
| `?`        | 0 o 1          | `colou?r` | color, colour    |
| `{n}`      | Exactamente n  | `\d{5}`   | 12345            |
| `{n,m}`    | Entre n y m    | `\d{3,5}` | 123, 1234, 12345 |
| `{n,}`     | Al menos n     | `\d{3,}`  | 123, 1234...     |
| `*?`       | 0 o más (lazy) | `".*?"`   | Mínimo match     |
| `+?`       | 1 o más (lazy) | `.+?`     | Un carácter      |

---

**Siguiente:** Proyecto de la semana en `3-proyecto/`
