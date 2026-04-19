# Ejercicios Semana 01: Fundamentos de RegExp

## Instrucciones Generales

- Usa [regex101.com](https://regex101.com) para probar tus patrones
- Selecciona "JavaScript" como flavor
- Intenta resolver sin ver las soluciones
- Cada ejercicio incluye hints si te atascas

---

## Ejercicio 01: Literales Básicos

### Objetivo

Practicar búsqueda de texto exacto (literales).

### Instrucciones

Crea patrones que encuentren las siguientes palabras en el texto de prueba.

### Texto de Prueba

```
JavaScript es un lenguaje de programación.
Java es otro lenguaje diferente.
TypeScript extiende JavaScript.
```

### Tareas

1. Encuentra "JavaScript" (debería haber 2 matches)
2. Encuentra "Java" (¿cuántos matches hay? ¿por qué?)
3. Encuentra "Script" (¿cuántos matches hay?)

### Resultado Esperado

| Tarea | Patrón | Matches |
| ----- | ------ | ------- |
| 1     | `???`  | 2       |
| 2     | `???`  | ?       |
| 3     | `???`  | ?       |

### Hints

<details>
<summary>Hint 1</summary>
Los literales buscan exactamente lo que escribes.
</details>

<details>
<summary>Hint 2</summary>
"Java" aparece dentro de "JavaScript" también.
</details>

---

## Ejercicio 02: El Metacharacter Dot

### Objetivo

Entender cómo funciona el dot (`.`) como comodín.

### Instrucciones

Usa el dot para crear patrones flexibles.

### Texto de Prueba

```
casa cosa cesa cisa cusa c@sa c1sa cssa
```

### Tareas

1. Crea un patrón que coincida con todas las palabras que empiecen con "c", tengan cualquier carácter en medio, y terminen con "sa"
2. ¿Coincide con "cssa"? ¿Por qué?
3. ¿Coincide con "ca"? ¿Por qué?

### Resultado Esperado

El patrón debería encontrar: `casa`, `cosa`, `cesa`, `cisa`, `cusa`, `c@sa`, `c1sa`, `cssa`

### Hints

<details>
<summary>Hint 1</summary>
El patrón es: c + (cualquier carácter) + sa
</details>

<details>
<summary>Hint 2</summary>
El dot coincide con UN solo carácter, incluyendo 's'.
</details>

---

## Ejercicio 03: Anchors de Inicio y Fin

### Objetivo

Dominar los anchors `^` y `$`.

### Instrucciones

Crea patrones que validen posiciones específicas.

### Texto de Prueba (probar cada línea por separado)

```
Hola mundo
mundo Hola
Hola
mundo
```

### Tareas

1. Patrón que coincida SOLO si el texto empieza con "Hola"
2. Patrón que coincida SOLO si el texto termina con "mundo"
3. Patrón que coincida SOLO si el texto es exactamente "Hola"
4. Patrón que coincida SOLO si el texto es exactamente "Hola mundo"

### Resultado Esperado

| Tarea | Patrón | "Hola mundo" | "mundo Hola" | "Hola" | "mundo" |
| ----- | ------ | ------------ | ------------ | ------ | ------- |
| 1     | `???`  | ✅           | ❌           | ✅     | ❌      |
| 2     | `???`  | ✅           | ❌           | ❌     | ✅      |
| 3     | `???`  | ❌           | ❌           | ✅     | ❌      |
| 4     | `???`  | ✅           | ❌           | ❌     | ❌      |

### Hints

<details>
<summary>Hint 1</summary>
`^` indica inicio, `$` indica fin.
</details>

<details>
<summary>Hint 2</summary>
Para match exacto, usa ambos: `^texto$`
</details>

---

## Ejercicio 04: Escapando Metacaracteres

### Objetivo

Aprender a buscar caracteres que tienen significado especial.

### Instrucciones

Busca caracteres literales que normalmente son metacaracteres.

### Texto de Prueba

```
El precio es $9.99 dólares.
archivo.txt
config.json
$variable
100%
```

### Tareas

1. Encuentra "$9.99" (el precio completo)
2. Encuentra todas las extensiones de archivo (`.txt`, `.json`)
3. Encuentra el símbolo "$" solo cuando está al inicio
4. Encuentra el símbolo "%"

### Resultado Esperado

| Tarea | Patrón | Match(es)        |
| ----- | ------ | ---------------- |
| 1     | `???`  | $9.99            |
| 2     | `???`  | .txt, .json      |
| 3     | `???`  | $ (de $variable) |
| 4     | `???`  | %                |

### Hints

<details>
<summary>Hint 1</summary>
Usa `\` para escapar: `\.`, `\$`, `\%`
</details>

<details>
<summary>Hint 2</summary>
Para "$" al inicio: `^\$`
</details>

---

## Ejercicio 05: Combinando Todo

### Objetivo

Aplicar todos los conceptos de la semana en patrones más complejos.

### Instrucciones

Crea patrones que combinen literales, dot, anchors y escapes.

### Texto de Prueba

```
index.html
style.css
app.js
main.py
README.md
test.spec.js
.gitignore
```

### Tareas

1. Encuentra archivos que terminen en `.js`
2. Encuentra archivos que empiecen con cualquier letra y terminen en `.md`
3. Encuentra archivos con exactamente un punto (excluye `test.spec.js`)
4. Encuentra archivos ocultos (empiezan con `.`)

### Hints

<details>
<summary>Hint 1</summary>
Para terminar en .js: `\.js$`
</details>

<details>
<summary>Hint 2</summary>
Para archivos ocultos: `^\.`
</details>

<details>
<summary>Hint 3</summary>
Un solo punto es más complejo. Por ahora, intenta con lo que sabes. La solución óptima vendrá en semanas posteriores.
</details>

---

## Desafío Extra 🔥

### El Reto

Sin usar conocimientos de semanas futuras, ¿puedes crear un patrón que valide este formato de fecha simple?

```
Formato: DD.MM.AAAA
Ejemplo válido: 25.12.2024
```

### Restricciones

- Solo usa: literales, `.` (dot), `^`, `$`, `\`
- El dot debe representar "cualquier dígito" (no es perfecto, pero funciona por ahora)

### Hint

<details>
<summary>Ver hint</summary>
Necesitarás 8 dots (para los dígitos) y 2 puntos escapados (para los separadores).
Formato: `^........\...\.....$` pero más legible.
</details>

---

**Siguiente paso:** Revisa las soluciones en `solucion-01-fundamentos.md` después de intentar todos los ejercicios.
