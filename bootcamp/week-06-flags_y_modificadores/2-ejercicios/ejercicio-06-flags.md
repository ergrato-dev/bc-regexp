# Ejercicios - Semana 06: Flags y Modificadores

## Ejercicio 1: Contador de Palabras

**Objetivo:** Contar todas las ocurrencias de una palabra, sin importar mayúsculas.

**Texto de prueba:**

```
JavaScript is a programming language. javascript is used for web development.
Many developers love JavaScript. JAVASCRIPT powers many websites.
```

**Requisitos:**

1. Usar flags `g` e `i`
2. Contar ocurrencias de "javascript"
3. Retornar el conteo

**Resultado esperado:**

```javascript
4; // JavaScript, javascript, JavaScript, JAVASCRIPT
```

<details>
<summary>💡 Hint</summary>

```javascript
const pattern = /javascript/gi;
const matches = texto.match(pattern);
return matches ? matches.length : 0;
```

</details>

---

## Ejercicio 2: Extraer Comentarios Multilínea

**Objetivo:** Extraer comentarios `/* ... */` que pueden ocupar múltiples líneas.

**Texto de prueba:**

```javascript
const x = 1;
/* Este es un
   comentario
   multilínea */
const y = 2;
/* Otro comentario */
const z = 3;
```

**Requisitos:**

1. Usar flag `s` (dotall) o alternativa
2. Capturar todo el contenido del comentario
3. Encontrar todos los comentarios

**Resultado esperado:**

```javascript
['/* Este es un\n   comentario\n   multilínea */', '/* Otro comentario */'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// Con flag s (ES2018+)
/\/\*.*?\*\//gs

// Alternativa sin flag s
/\/\*[\s\S]*?\*\//g
```

</details>

---

## Ejercicio 3: Procesar Archivo de Configuración

**Objetivo:** Extraer pares clave=valor, ignorando líneas de comentario.

**Texto de prueba:**

```
# Configuración de la app
nombre=MiApp
version=1.0.0
# Puerto del servidor
puerto=3000
debug=true
```

**Requisitos:**

1. Usar flag `m` (multiline)
2. Ignorar líneas que empiezan con `#`
3. Extraer clave y valor por separado

**Resultado esperado:**

```javascript
{
  nombre: 'MiApp',
  version: '1.0.0',
  puerto: '3000',
  debug: 'true'
}
```

<details>
<summary>💡 Hint</summary>

```javascript
// Capturar líneas que NO empiezan con #
/^(?!#)(\w+)=(.+)$/gm;
```

</details>

---

## Ejercicio 4: Validar Texto Internacional

**Objetivo:** Validar nombres que pueden contener caracteres de cualquier idioma.

**Textos de prueba:**

```
José García
北京市
Москва
محمد أحمد
João
```

**Requisitos:**

1. Usar flag `u` (unicode)
2. Usar `\p{Letter}` para letras
3. Permitir espacios entre palabras

**Resultado esperado:**

```javascript
// Todos deben ser válidos
true, true, true, true, true;
```

<details>
<summary>💡 Hint</summary>

```javascript
const pattern = /^[\p{Letter}\s]+$/u;
```

</details>

---

## Ejercicio 5: Tokenizer con Sticky

**Objetivo:** Crear un tokenizer simple usando el flag `y`.

**Texto de prueba:**

```
123 + 456 * 789
```

**Requisitos:**

1. Usar flag `y` (sticky)
2. Identificar tokens: números, operadores, espacios
3. Extraer tokens en orden

**Resultado esperado:**

```javascript
[
  { type: 'number', value: '123' },
  { type: 'space', value: ' ' },
  { type: 'operator', value: '+' },
  { type: 'space', value: ' ' },
  { type: 'number', value: '456' },
  { type: 'space', value: ' ' },
  { type: 'operator', value: '*' },
  { type: 'space', value: ' ' },
  { type: 'number', value: '789' },
];
```

<details>
<summary>💡 Hint</summary>

```javascript
const patterns = [
  { type: 'number', regex: /\d+/y },
  { type: 'operator', regex: /[+\-*/]/y },
  { type: 'space', regex: /\s+/y },
];
```

</details>

---

## Ejercicio 6: Índices de Grupos

**Objetivo:** Usar el flag `d` para obtener las posiciones exactas de cada parte.

**Texto de prueba:**

```
Email: usuario@dominio.com
```

**Requisitos:**

1. Usar flag `d` (hasIndices)
2. Capturar usuario, dominio, extensión
3. Retornar las posiciones de cada parte

**Resultado esperado:**

```javascript
{
  usuario: { start: 7, end: 14 },    // "usuario"
  dominio: { start: 15, end: 22 },   // "dominio"
  extension: { start: 23, end: 26 }  // "com"
}
```

<details>
<summary>💡 Hint</summary>

```javascript
const pattern = /(\w+)@(\w+)\.(\w+)/d;
const match = texto.match(pattern);
// match.indices contiene [matchCompleto, grupo1, grupo2, grupo3]
```

</details>

---

## Ejercicio 7: Búsqueda con Emojis

**Objetivo:** Encontrar y contar emojis en un texto.

**Texto de prueba:**

```
Hola 👋 amigo! Cómo estás? 😀 Espero que bien 🎉 Nos vemos 👍
```

**Requisitos:**

1. Usar flag `u` (unicode)
2. Usar `\p{Emoji}` o equivalente
3. Contar emojis únicos

**Resultado esperado:**

```javascript
{
  total: 4,
  emojis: ['👋', '😀', '🎉', '👍'],
  unicos: 4
}
```

<details>
<summary>💡 Hint</summary>

```javascript
const pattern = /\p{Emoji}/gu;
// O para Extended_Pictographic (más completo)
const pattern = /\p{Extended_Pictographic}/gu;
```

</details>

---

## Desafío: Log Parser Avanzado

**Objetivo:** Crear un parser de logs que maneje múltiples formatos y características.

**Logs de prueba:**

```
2024-01-15 10:30:45 [INFO] Server started on port 3000
2024-01-15 10:30:46 [DEBUG] Loading config file...
/* Multi-line
   debug info */
2024-01-15 10:30:47 [ERROR] Connection failed:
  Host: localhost
  Port: 5432
2024-01-15 10:30:48 [warning] Low memory
2024-01-15 10:30:49 [INFO] Retrying connection...
```

**Requisitos:**

1. Extraer fecha, hora, nivel y mensaje
2. Manejar niveles case-insensitive
3. Manejar mensajes multilínea
4. Filtrar por nivel
5. Usar flags apropiados

**Resultado esperado:**

```javascript
const logs = parseLogs(texto);
// [
//   { date: '2024-01-15', time: '10:30:45', level: 'INFO', message: 'Server started on port 3000' },
//   { date: '2024-01-15', time: '10:30:46', level: 'DEBUG', message: 'Loading config file...' },
//   // ... etc
// ]

const errores = logs.filter((l) => l.level === 'ERROR');
```

<details>
<summary>💡 Hint</summary>

```javascript
// Patrón base con flags gim
const pattern =
  /^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.+?)(?=^\d{4}|\Z)/gims;
```

</details>

---

## Recursos

- [MDN: Regular expression flags](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#advanced_searching_with_flags)
- [Unicode property escapes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Unicode_character_class_escape)

---

**Soluciones:** [solucion-06-flags.md](solucion-06-flags.md)
