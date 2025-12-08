# Ejercicios Semana 03: Quantifiers

## Instrucciones Generales

- Usa [regex101.com](https://regex101.com) para probar (flavor: JavaScript)
- Practica tanto quantifiers greedy como lazy
- Presta atención a la diferencia entre `*`, `+`, `?` y `{n,m}`

---

## Ejercicio 01: Quantifiers Básicos

### Objetivo

Dominar `*`, `+`, `?` y su comportamiento.

### Texto de Prueba

```
color colour colouur
http https httttps
file file1 file12 file123
```

### Tareas

1. Crea un patrón que coincida con "color" y "colour" (u opcional)
2. Crea un patrón que coincida con "http" y "https" (s opcional)
3. Crea un patrón que coincida con "file" seguido de uno o más dígitos
4. Crea un patrón que coincida con "file" seguido de cero o más dígitos

### Resultado Esperado

| Tarea | Patrón | Matches                      |
| ----- | ------ | ---------------------------- |
| 1     | `???`  | color, colour                |
| 2     | `???`  | http, https                  |
| 3     | `???`  | file1, file12, file123       |
| 4     | `???`  | file, file1, file12, file123 |

### Hints

<details>
<summary>Hint 1</summary>
Opcional = `?` → `colou?r`
</details>

<details>
<summary>Hint 2</summary>
Uno o más = `+` → `file\d+`
</details>

---

## Ejercicio 02: Quantifiers con Llaves

### Objetivo

Practicar `{n}`, `{n,m}`, `{n,}`.

### Texto de Prueba

```
12 123 1234 12345 123456 1234567
AB AB1 AB12 AB123 AB1234
```

### Tareas

1. Encuentra secuencias de exactamente 5 dígitos
2. Encuentra secuencias de 3 a 5 dígitos
3. Encuentra secuencias de al menos 4 dígitos
4. Encuentra códigos: 2 letras seguidas de exactamente 3 dígitos

### Hints

<details>
<summary>Hint 1</summary>
Exactamente 5: `\d{5}` (cuidado con límites `\b`)
</details>

<details>
<summary>Hint 2</summary>
Para evitar que 123456 matchee como 12345, usa word boundaries
</details>

---

## Ejercicio 03: Greedy vs Lazy

### Objetivo

Entender la diferencia entre comportamiento greedy y lazy.

### Texto de Prueba

```html
<p>Párrafo 1</p>
<p>Párrafo 2</p>
<p>Párrafo 3</p>
```

### Tareas

1. Captura TODO el contenido entre el primer `<p>` y el último `</p>` (greedy)
2. Captura CADA párrafo individualmente (lazy + flag g)
3. Captura solo el contenido de texto (sin tags) de cada párrafo

### Resultado Esperado

| Tarea | Resultado                                                      |
| ----- | -------------------------------------------------------------- |
| 1     | `<p>Párrafo 1</p><p>Párrafo 2</p><p>Párrafo 3</p>`             |
| 2     | `['<p>Párrafo 1</p>', '<p>Párrafo 2</p>', '<p>Párrafo 3</p>']` |
| 3     | `['Párrafo 1', 'Párrafo 2', 'Párrafo 3']`                      |

### Hints

<details>
<summary>Hint 1</summary>
Greedy: `<p>.*</p>`
</details>

<details>
<summary>Hint 2</summary>
Lazy: `<p>.*?</p>` con flag `/g`
</details>

<details>
<summary>Hint 3</summary>
Para capturar solo el texto, usa un grupo: `<p>(.*?)</p>` y matchAll
</details>

---

## Ejercicio 04: Validaciones con Quantifiers

### Objetivo

Aplicar quantifiers a validaciones reales.

### Tareas

Crea patrones para validar:

1. **Código postal español** (5 dígitos)

   - ✅ `28001`, `08080`
   - ❌ `2800`, `280011`

2. **Teléfono español** (9 dígitos, empieza con 6, 7, 8 o 9)

   - ✅ `612345678`, `912345678`
   - ❌ `12345678`, `6123456789`

3. **DNI español** (8 dígitos + 1 letra)

   - ✅ `12345678A`, `00000000Z`
   - ❌ `1234567A`, `123456789A`

4. **Contraseña** (8-16 caracteres, letras y números)

   - ✅ `Pass1234`, `MiClave123456`
   - ❌ `Pass1`, `EstaContraseñaEsDemasiadoLarga123`

5. **Nombre de usuario** (3-15 caracteres, letras, números, guión bajo)
   - ✅ `user`, `user_123`, `U`
   - ❌ `ab`, `este_username_es_muy_largo`

### Hints

<details>
<summary>Hint para teléfono</summary>
`^[6-9]\d{8}$`
</details>

<details>
<summary>Hint para DNI</summary>
`^\d{8}[A-Z]$`
</details>

<details>
<summary>Hint para contraseña</summary>
`^[a-zA-Z0-9]{8,16}$`
</details>

---

## Ejercicio 05: Extracción de Datos

### Objetivo

Usar quantifiers para extraer información de texto.

### Texto de Prueba

```
Productos:
- Laptop: $999.99
- Mouse: $29.50
- Teclado: $149
- Monitor: $399.00

Contacto: email@example.com, otro.email@dominio.es
Teléfono: 612-345-678 o 91 234 56 78
```

### Tareas

1. Extrae todos los precios (con o sin decimales)
2. Extrae todos los emails
3. Extrae todos los teléfonos (cualquier formato)
4. Extrae todos los nombres de productos

### Hints

<details>
<summary>Hint para precios</summary>
`\$\d+(\.\d{2})?` o `\$[\d.]+`
</details>

<details>
<summary>Hint para emails</summary>
`[\w.-]+@[\w.-]+\.\w+`
</details>

---

## Ejercicio 06: Alternativa a Lazy

### Objetivo

Usar negación como alternativa a lazy quantifiers.

### Texto de Prueba

```
"primera" y "segunda" y "tercera"
```

### Tareas

1. Extrae cada string entre comillas usando lazy: `".*?"`
2. Extrae cada string entre comillas usando negación: `"[^"]*"`
3. Compara ambos enfoques - ¿cuál es más explícito?

### Reflexión

¿Por qué `[^"]*` podría ser mejor que `.*?` en algunos casos?

<details>
<summary>Ver respuesta</summary>

1. **Más explícito**: `[^"]*` dice exactamente "cualquier carácter excepto comillas"
2. **Sin backtracking**: El motor avanza directamente sin probar y retroceder
3. **Más rápido**: En textos muy largos, puede ser más eficiente
4. **Más predecible**: No hay ambigüedad en qué caracteres captura

</details>

---

## Desafío Extra 🔥

### El Reto: Parser de Logs

Tienes un archivo de log con este formato:

```
[2024-01-15 10:30:45] INFO: Usuario admin conectado
[2024-01-15 10:31:02] ERROR: Fallo en conexión a BD
[2024-01-15 10:31:15] WARN: Memoria al 85%
[2024-01-15 10:32:00] INFO: Backup completado
```

### Tareas

1. Extrae la fecha y hora de cada línea
2. Extrae el nivel de log (INFO, ERROR, WARN)
3. Extrae el mensaje después del nivel
4. Crea un patrón que capture los 3 elementos en grupos

### Formato de Salida Esperado

```javascript
const logs = texto.matchAll(/patrón/g);
for (const log of logs) {
  console.log({
    fecha: log[1], // "2024-01-15 10:30:45"
    nivel: log[2], // "INFO"
    mensaje: log[3], // "Usuario admin conectado"
  });
}
```

### Hint

<details>
<summary>Ver hint</summary>

```javascript
/\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)/g;
```

Desglose:

- `\[...\]` - Corchetes literales
- `(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})` - Grupo 1: fecha/hora
- `(\w+)` - Grupo 2: nivel (INFO, ERROR, etc.)
- `(.+)` - Grupo 3: mensaje

</details>

---

**Siguiente:** Revisa las soluciones en `solucion-03-quantifiers.md`
