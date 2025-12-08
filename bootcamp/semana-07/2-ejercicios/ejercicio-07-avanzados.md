# Ejercicios - Semana 07: Patrones Avanzados

## Instrucciones

- Usa named capture groups cuando sea apropiado
- Optimiza los patrones para evitar backtracking
- Todos los ejercicios incluyen casos edge

---

## Ejercicio 1: Parser de Log con Named Groups

### Objetivo

Parsear entradas de log con named groups.

### Texto de Prueba

```
[2024-03-15 10:30:45] ERROR servidor-web: Connection timeout
[2024-03-15 10:31:02] INFO auth-service: User login successful
[2024-03-15 10:31:15] WARN database: High memory usage (85%)
[2024-03-15 10:32:00] DEBUG api-gateway: Request processed in 45ms
```

### Requisitos

1. Extraer: fecha, hora, nivel, servicio, mensaje
2. Usar named groups para cada componente
3. Nivel debe ser: ERROR, WARN, INFO, DEBUG

### Resultado Esperado

```javascript
match.groups = {
  date: '2024-03-15',
  time: '10:30:45',
  level: 'ERROR',
  service: 'servidor-web',
  message: 'Connection timeout',
};
```

---

## Ejercicio 2: Validador de Contraseña Segura

### Objetivo

Crear un validador de contraseña con múltiples requisitos.

### Requisitos

1. Mínimo 8 caracteres
2. Al menos una mayúscula
3. Al menos una minúscula
4. Al menos un número
5. Al menos un carácter especial (!@#$%^&\*)
6. NO puede contener espacios
7. NO puede tener más de 3 caracteres repetidos consecutivos

### Casos de Prueba

```javascript
// ✅ Válidas
'Passw0rd!';
'MyStr0ng#Pass';
'C0mpl3x!ty';

// ❌ Inválidas
'password'; // Sin mayúscula, número, especial
'PASSWORD1!'; // Sin minúscula
'Passw0rd'; // Sin carácter especial
'Pass 0rd!'; // Contiene espacio
'Passsword1!'; // 4 's' consecutivas
```

### Hints

<details>
<summary>Estructura sugerida</summary>

Usa múltiples lookaheads al inicio:

```javascript
/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])(?!.*\s)(?!.*(.)\1{3,}).{8,}$/;
```

</details>

---

## Ejercicio 3: Extractor de URLs con Componentes

### Objetivo

Extraer y descomponer URLs en sus partes.

### Texto de Prueba

```
https://www.example.com:8080/path/to/page?id=123&name=test#section
http://api.service.io/v2/users
ftp://files.server.net/downloads/file.zip
https://sub.domain.example.org/search?q=regex
```

### Requisitos

Extraer con named groups:

- protocol
- subdomain (si existe)
- domain
- tld
- port (si existe)
- path
- query (si existe)
- fragment (si existe)

---

## Ejercicio 4: Detector de SQL Injection

### Objetivo

Detectar posibles intentos de SQL injection.

### Patrones a Detectar

```
' OR '1'='1
'; DROP TABLE users; --
1; DELETE FROM products
UNION SELECT * FROM users
' AND 1=1 --
```

### Casos Seguros

```
John's Pizza        // Apóstrofe válido
SELECT menu items   // Palabra común
```

### Hints

<details>
<summary>Palabras clave a buscar</summary>

```javascript
// Detectar:
// - Comillas seguidas de OR/AND
// - UNION SELECT
// - DROP/DELETE/INSERT/UPDATE sin contexto válido
// - Comentarios SQL (-- o /*)
// - Punto y coma seguido de comando
```

</details>

---

## Ejercicio 5: Parser de CSV Robusto

### Objetivo

Parsear líneas CSV correctamente, incluyendo:

- Campos con comas entre comillas
- Campos con comillas escapadas
- Campos vacíos

### Texto de Prueba

```
nombre,edad,ciudad
"García, Juan",35,"Madrid, España"
Ana,28,Barcelona
"El ""Maestro"" López",45,Sevilla
,25,Valencia
Pedro,,Bilbao
```

### Resultado Esperado

```javascript
[
  ['nombre', 'edad', 'ciudad'],
  ['García, Juan', '35', 'Madrid, España'],
  ['Ana', '28', 'Barcelona'],
  ['El "Maestro" López', '45', 'Sevilla'],
  ['', '25', 'Valencia'],
  ['Pedro', '', 'Bilbao'],
];
```

---

## Ejercicio 6: Optimizar Patrón Problemático

### Objetivo

Identificar y corregir patrones con backtracking.

### Patrones a Optimizar

```javascript
// 1. Email (problemático)
/^(\w+\.?)+@(\w+\.?)+\.\w+$/

// 2. HTML tag (problemático)
/<(\w+)>.*<\/\1>/

// 3. Número con separadores (problemático)
/^[\d,]+$/
```

### Tareas

1. Identificar por qué son problemáticos
2. Proporcionar input que causa backtracking
3. Reescribir de forma segura

---

## Ejercicio 7: Tokenizer Aritmético

### Objetivo

Crear un tokenizer para expresiones aritméticas.

### Tipos de Tokens

| Token  | Patrón              |
| ------ | ------------------- |
| NUMBER | Enteros y decimales |
| PLUS   | +                   |
| MINUS  | -                   |
| MULT   | \*                  |
| DIV    | /                   |
| POWER  | ^ o \*\*            |
| LPAREN | (                   |
| RPAREN | )                   |
| IDENT  | Variables (letras)  |

### Expresiones de Prueba

```
3 + 4 * 2
(10 - 5) / 2.5
x^2 + 2*x + 1
sin(x) ** 2
```

### Resultado Esperado

```javascript
tokenize('3 + 4 * 2');
// [
//   { type: 'NUMBER', value: '3' },
//   { type: 'PLUS', value: '+' },
//   { type: 'NUMBER', value: '4' },
//   { type: 'MULT', value: '*' },
//   { type: 'NUMBER', value: '2' }
// ]
```

---

## Desafío: Parser de Template Strings

### Objetivo

Parsear template strings con interpolaciones anidadas.

### Sintaxis

```
Hello, ${name}!
Your total is ${price * quantity}.
Welcome, ${user.firstName} ${user.lastName}!
${nested ? ${value} : 'default'}
```

### Requisitos

1. Extraer texto literal y expresiones
2. Manejar anidación básica (1 nivel)
3. Identificar expresiones vs texto

### Resultado

```javascript
parseTemplate('Hello, ${name}! You have ${items.length} items.');
// [
//   { type: 'TEXT', value: 'Hello, ' },
//   { type: 'EXPR', value: 'name' },
//   { type: 'TEXT', value: '! You have ' },
//   { type: 'EXPR', value: 'items.length' },
//   { type: 'TEXT', value: ' items.' }
// ]
```

---

## Formato de Entrega

````markdown
## Ejercicio X

### Patrón

```javascript
const pattern = /tu-regex-aquí/;
```
````

### Explicación

¿Por qué? [razón]
¿Para qué? [propósito]

### Tests

```javascript
// Casos que funcionan
// Casos que fallan correctamente
```

```

---

**Soluciones:** [solucion-07-avanzados.md](solucion-07-avanzados.md)
```
