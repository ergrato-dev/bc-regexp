# Ejercicios Semana 02: Character Classes

## Instrucciones Generales

- Usa [regex101.com](https://regex101.com) para probar (flavor: JavaScript)
- Intenta resolver sin ver las soluciones
- Usa los conceptos: `[abc]`, `[^abc]`, `[a-z]`, `\d`, `\w`, `\s`, `\b`

---

## Ejercicio 01: Character Classes Básicas

### Objetivo

Practicar la creación de character classes personalizadas.

### Texto de Prueba

```
casa cosa cesa cisa cusa
cAsa cOsa cEsa
c1sa c@sa c-sa
```

### Tareas

1. Crea un patrón que coincida solo con las vocales minúsculas entre 'c' y 'sa'
2. Crea un patrón que coincida con vocales mayúsculas O minúsculas
3. Crea un patrón que coincida con cualquier cosa EXCEPTO vocales

### Resultado Esperado

| Tarea | Patrón | Matches                      |
| ----- | ------ | ---------------------------- |
| 1     | `???`  | casa, cosa, cesa, cisa, cusa |
| 2     | `???`  | + cAsa, cOsa, cEsa           |
| 3     | `???`  | c1sa, c@sa, c-sa             |

### Hints

<details>
<summary>Hint 1</summary>
Tarea 1: `c[aeiou]sa`
</details>

<details>
<summary>Hint 2</summary>
Tarea 2: Combina rangos `[aeiouAEIOU]`
</details>

---

## Ejercicio 02: Rangos

### Objetivo

Dominar la sintaxis de rangos en character classes.

### Texto de Prueba

```
A1 B2 C3 a1 b2 c3
Z9 z9 M5 m5
1A 2B 3C
@# $% ^&
```

### Tareas

1. Encuentra pares de "letra mayúscula + dígito" (A1, B2, Z9, etc.)
2. Encuentra pares de "dígito + letra mayúscula" (1A, 2B, etc.)
3. Encuentra cualquier carácter que NO sea letra ni dígito
4. Encuentra letras minúsculas seguidas de dígito

### Hints

<details>
<summary>Hint 1</summary>
Mayúscula + dígito: `[A-Z][0-9]` o `[A-Z]\d`
</details>

<details>
<summary>Hint 2</summary>
No letra ni dígito: `[^a-zA-Z0-9]` o `[^\w]` (casi, `\w` incluye `_`)
</details>

---

## Ejercicio 03: Shorthand Classes

### Objetivo

Usar `\d`, `\w`, `\s` y sus negaciones.

### Texto de Prueba

```
usuario123
user_name
user-name
user name
user@name
12345
   espacios
```

### Tareas

1. Encuentra strings que contengan SOLO word characters
2. Encuentra strings que contengan algún whitespace
3. Encuentra strings que contengan SOLO dígitos
4. Encuentra strings que contengan caracteres NO word

### Resultado Esperado

| Tarea | Matches                                       |
| ----- | --------------------------------------------- |
| 1     | usuario123, user_name, 12345                  |
| 2     | user name, " espacios "                       |
| 3     | 12345                                         |
| 4     | user-name, user name, user@name, " espacios " |

### Hints

<details>
<summary>Hint 1</summary>
Solo word chars de inicio a fin: `^\w+$` (necesitas `+` de semana 03, o muchos `\w`)
</details>

<details>
<summary>Hint 2</summary>
Por ahora puedes usar `/\s/` para detectar SI tiene espacio
</details>

---

## Ejercicio 04: Word Boundaries

### Objetivo

Dominar `\b` para encontrar palabras completas.

### Texto de Prueba

```
The cat sat on the mat.
Concatenate the categories.
There is the theater.
Cat category caterpillar.
```

### Tareas

1. Encuentra la palabra "cat" como palabra completa (no dentro de otras)
2. Encuentra "the" solo como palabra completa
3. Encuentra "cat" SOLO cuando está dentro de otra palabra
4. Encuentra palabras que EMPIECEN con "cat"

### Resultado Esperado

| Tarea | Patrón | Matches                                                   |
| ----- | ------ | --------------------------------------------------------- |
| 1     | `???`  | "cat" (línea 1), "Cat" (necesita flag i)                  |
| 2     | `???`  | "The", "the" x3                                           |
| 3     | `???`  | En "Concatenate", "categories", "category", "caterpillar" |
| 4     | `???`  | "cat", "Cat", "category", "caterpillar", "categories"     |

### Hints

<details>
<summary>Hint 1</summary>
Palabra completa: `\bcat\b`
</details>

<details>
<summary>Hint 2</summary>
Dentro de palabra: `\Bcat\B`
</details>

<details>
<summary>Hint 3</summary>
Empieza con: `\bcat` (boundary al inicio, no al final)
</details>

---

## Ejercicio 05: Validaciones Prácticas

### Objetivo

Aplicar character classes a casos reales.

### Tareas

Crea patrones para validar:

1. **Código postal español** (5 dígitos)

   - Válido: `28001`, `08080`, `41001`
   - Inválido: `2800`, `280011`, `2800A`

2. **Inicial + número de 2 dígitos** (formato: A-99)

   - Válido: `A-01`, `Z-99`, `M-50`
   - Inválido: `AB-01`, `A-1`, `a-01`

3. **Código hexadecimal de 3 caracteres**

   - Válido: `F00`, `ABC`, `1a2`
   - Inválido: `GGG`, `FFFF`, `XYZ`

4. **Nombre simple** (solo letras, primera mayúscula)
   - Válido: `Juan`, `Ana`, `Pedro`
   - Inválido: `juan`, `JUAN`, `Juan1`, `J`

### Hints

<details>
<summary>Hint para código postal</summary>
5 dígitos: `^\d\d\d\d\d$`
</details>

<details>
<summary>Hint para inicial</summary>
`^[A-Z]-\d\d$`
</details>

<details>
<summary>Hint para hex</summary>
`^[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]$`
</details>

<details>
<summary>Hint para nombre</summary>
`^[A-Z][a-z][a-z]+$` (mínimo 3 letras)
O más flexible: `^[A-Z][a-z]+$`
</details>

---

## Ejercicio 06: Caracteres Especiales en Classes

### Objetivo

Entender qué caracteres necesitan escape dentro de `[]`.

### Texto de Prueba

```
precio: $100
rango: 1-10
array[0]
resultado: 50%
path: C:\Users
opción: a^b
```

### Tareas

1. Encuentra el símbolo `$`
2. Encuentra el guión `-`
3. Encuentra los corchetes `[` o `]`
4. Encuentra el circunflejo `^`
5. Encuentra el backslash `\`

### Hint General

<details>
<summary>Ver hint</summary>

Dentro de `[]`:

- `$` no necesita escape
- `-` necesita escape O ir al inicio/final: `[-...]` o `[...-]`
- `]` necesita escape: `[\]]`
- `^` necesita escape si está al inicio: `[\^]` o `[a^]`
- `\` siempre necesita escape: `[\\]`

</details>

---

## Desafío Extra 🔥

### El Reto

Crea un patrón que valide un **número de teléfono español** con estos formatos:

```
Válidos:
612345678     (móvil sin espacios)
612 345 678   (móvil con espacios)
91 234 56 78  (fijo con espacios)
912345678     (fijo sin espacios)

Inválidos:
12345678      (no empieza con 6, 7, 8 o 9)
6123456789    (demasiados dígitos)
612-345-678   (guiones no válidos)
```

### Restricciones

- Solo usa character classes (sin cuantificadores `+`, `*`, `{n}`)
- Acepta espacios opcionales (difícil sin `?`, intenta una aproximación)

### Hint

<details>
<summary>Ver hint</summary>

Para móvil sin espacios:
`^[6789]\d\d\d\d\d\d\d\d$`

Para aceptar espacios, necesitarías cuantificadores (semana 03).
Por ahora, crea patrones separados para cada formato.

</details>

---

**Siguiente:** Revisa las soluciones en `solucion-02-character-classes.md`
