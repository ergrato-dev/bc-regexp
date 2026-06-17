# Semana 01: Métodos de RegExp en Python

## Introducción

Python proporciona el módulo `re` para trabajar con expresiones regulares. Es el equivalente a los métodos integrados de JavaScript.

## Importar el Módulo

```python
import re
```

## Métodos del Módulo `re`

### `re.search()` - Buscar Coincidencia

```python
"""
¿Por qué? Es el método más común para buscar un patrón en un string
¿Para qué? Validaciones, búsquedas y extracción de información

Retorna: Match object o None
"""
import re

pattern = r'gato'
resultado = re.search(pattern, 'El gato duerme')

print(bool(resultado))  # True
print(resultado.group())  # 'gato'
print(resultado.start())  # 3 (posición)
print(resultado.end())    # 7
print(resultado.span())   # (3, 7)
```

> **Nota:** `re.search()` busca la **primera** coincidencia en cualquier parte del string. Para buscar **todas** las coincidencias, usar `re.findall()` o `re.finditer()`.

### `re.match()` - Coincidencia al Inicio

```python
"""
¿Por qué? Similar a search() pero solo busca al INICIO del string
¿Para qué? Validar que un string empiece con un patrón específico

Retorna: Match object o None
"""
import re

pattern = r'Hola'

# match() - busca al inicio
print(bool(re.match(pattern, 'Hola mundo')))  # True
print(bool(re.match(pattern, 'mundo Hola')))  # False (no está al inicio)

# Equivale a usar ^ seguido del patrón en search()
print(bool(re.search(r'^Hola', 'Hola mundo')))  # True
print(bool(re.search(r'^Hola', 'mundo Hola')))  # False
```

### `re.fullmatch()` - Coincidencia Completa

```python
"""
¿Por qué? El string ENTERO debe coincidir con el patrón
¿Para qué? Validaciones estrictas de formato

Retorna: Match object o None
"""
import re

pattern = r'\d{2}:\d{2}'

print(bool(re.fullmatch(pattern, '09:30')))   # True
print(bool(re.fullmatch(pattern, '09:30:00'))) # False (hay más texto)
print(bool(re.fullmatch(pattern, '9:30')))     # False (falta un dígito)

# Equivale a usar ^ y $ en search()
print(bool(re.search(r'^\d{2}:\d{2}$', '09:30')))  # True
```

### `re.findall()` - Todas las Coincidencias

```python
"""
¿Por qué? A veces necesitamos TODAS las coincidencias, no solo la primera
¿Para qué? Extraer múltiples valores de un texto

Retorna: Lista de strings (o lista de tuplas si hay grupos)
"""
import re

texto = 'El gato y otro gato'

# Sin grupos - retorna lista de strings
print(re.findall(r'gato', texto))  # ['gato', 'gato']

# Con grupos - retorna lista de tuplas
print(re.findall(r'(\d{2}):(\d{2})', '09:30 y 12:45'))
# [('09', '30'), ('12', '45')]
```

> **Nota:** `re.findall()` es el equivalente a `str.match(/pattern/g)` en JavaScript.

### `re.finditer()` - Iterar Coincidencias

```python
"""
¿Por qué? findall() pierde información de posición y grupos nombrados
¿Para qué? Obtener información completa de CADA match (posición, grupos)

Retorna: Iterator de Match objects
"""
import re

texto = 'gato1 gato2 gato3'
pattern = r'gato(\d)'

for match in re.finditer(pattern, texto):
    print(match.group(0), match.group(1), match.start())
# gato1 1 0
# gato2 2 6
# gato3 3 12
```

> **Nota:** `re.finditer()` es el equivalente a `str.matchAll(/pattern/g)` en JavaScript.

### `re.sub()` - Buscar y Reemplazar

```python
"""
¿Por qué? Una de las operaciones más comunes con regex
¿Para qué? Transformar texto basándose en patrones
"""
import re

# Reemplazo simple (todos por defecto, a diferencia de JS)
print(re.sub(r'gato', 'perro', 'gato gato'))  # "perro perro"

# Limitar número de reemplazos
print(re.sub(r'gato', 'perro', 'gato gato', count=1))  # "perro gato"

# Usar grupos en el reemplazo
print(re.sub(r'(\w+) (\w+)', r'\2 \1', 'Hola mundo'))  # "mundo Hola"
```

> **Diferencia con JS:** `re.sub()` reemplaza **todas** las coincidencias por defecto. En JS, `str.replace()` solo reemplaza la primera a menos que se use el flag `g`.

### `re.split()` - Dividir por Patrón

```python
"""
¿Por qué? El separador a veces varía o tiene un patrón
¿Para qué? Dividir strings de forma más flexible que split simple
"""
import re

# Dividir por uno o más espacios
texto = 'uno   dos  tres'
print(re.split(r'\s+', texto))  # ['uno', 'dos', 'tres']

# Dividir por coma y espacios opcionales
print(re.split(r',\s*', 'a, b,c,  d'))  # ['a', 'b', 'c', 'd']
```

## Compilación de Patrones

```python
"""
¿Por qué? Compilar un patrón para reutilizarlo múltiples veces
¿Para qué? Mejor rendimiento y código más limpio
"""
import re

# Compilar patrón con flags
pattern = re.compile(r'gato', re.IGNORECASE)

# Usar el patrón compilado
print(bool(pattern.search('El GATO duerme')))  # True
print(pattern.findall('gato GATO'))  # ['gato', 'GATO']
```

> **Equivalente JS:** `const pattern = /gato/gi;`

## Creación de Patrones

### 1. Raw Strings (recomendado)

```python
"""
¿Por qué? Los backslashes en Python son caracteres de escape en strings normales
¿Para qué? Usar r'' evita tener que duplicar los backslashes
"""

# Con raw string (recomendado)
pattern = r'\d+\.\d+'  # Uno o más dígitos, punto literal, uno o más dígitos

# Sin raw string (hay que escapar los backslashes)
pattern = '\\d+\\.\\d+'
```

> **Equivalente JS:** En JS, las regex literales (`/.../`) no necesitan escapar backslashes extra.

### 2. Compilación Dinámica

```python
"""
¿Por qué? A veces el patrón se construye dinámicamente
¿Para qué? Crear patrones basados en variables o input del usuario
"""
import re

busqueda = 'hola'
pattern = re.compile(re.escape(busqueda), re.IGNORECASE)
# re.escape() escapa caracteres especiales para búsqueda literal
```

## Flags (Modificadores)

| Flag | Constante | Descripción | Equivalente JS |
|------|-----------|-------------|----------------|
| `i` | `re.IGNORECASE` o `re.I` | Ignorar mayúsculas/minúsculas | `i` |
| `m` | `re.MULTILINE` o `re.M` | `^` y `$` aplican por línea | `m` |
| `s` | `re.DOTALL` o `re.S` | `.` incluye saltos de línea | `s` |
| `x` | `re.VERBOSE` o `re.X` | Permite comentarios y espacios | *(sin equivalente)* |
| `a` | `re.ASCII` o `re.A` | Solo ASCII en `\w`, `\d`, etc. | *(sin equivalente)* |

```python
import re

# Flags combinados con | (bitwise OR)
pattern = re.compile(r'gato', re.IGNORECASE | re.MULTILINE)

# Flags inline (dentro del patrón)
pattern = re.compile(r'(?im)gato')
```

## Ejemplo Práctico Integrado

```python
"""
Validador de formato de hora (HH:MM)

¿Por qué? Los usuarios ingresan horas en diferentes formatos
¿Para qué? Asegurar que la hora tenga el formato correcto antes de procesarla
"""
import re

HORA_PATTERN = re.compile(r'^\d{2}:\d{2}$')
#                          │  │   │  │ │
#                          │  │   │  │ └─ Fin del string
#                          │  │   │  └─── Exactamente 2 dígitos (minutos)
#                          │  │   └────── Dos puntos literal
#                          │  └────────── Exactamente 2 dígitos (hora)
#                          └───────────── Inicio del string

def validar_hora(hora):
    if HORA_PATTERN.fullmatch(hora):
        return f'✅ "{hora}" es válida'
    else:
        return f'❌ "{hora}" no tiene formato HH:MM'

print(validar_hora('09:30'))  # ✅ "09:30" es válida
print(validar_hora('9:30'))   # ❌ "9:30" no tiene formato HH:MM
print(validar_hora('12:5'))   # ❌ "12:5" no tiene formato HH:MM
print(validar_hora('25:00'))  # ✅ "25:00" es válida (formato ok, valor no)
```

> **Nota:** Este patrón valida el **formato**, no el **valor**. Validar que la hora sea lógica (0-23, 0-59) requiere lógica adicional o un patrón más complejo.

## Comparación de Métodos

```
┌────────────────┬───────────────────────────────┬──────────────────────────────────┐
│    Método      │      Retorna                  │          Uso                     │
├────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ re.search()    │ Match object | None           │ Buscar patrón en cualquier parte │
│ re.match()     │ Match object | None           │ Buscar patrón al INICIO          │
│ re.fullmatch() │ Match object | None           │ El string ENTERO debe coincidir  │
│ re.findall()   │ Lista de strings              │ Todas las coincidencias          │
│ re.finditer()  │ Iterator de Match objects     │ Iterar coincidencias con detalle │
│ re.sub()       │ string                        │ Buscar y reemplazar              │
│ re.split()     │ Lista de strings              │ Dividir por patrón               │
└────────────────┴───────────────────────────────┴──────────────────────────────────┘
```

## Mapeo Rápido JS → Python

| JavaScript | Python |
|------------|--------|
| `pattern.test(str)` | `bool(re.search(pattern, str))` |
| `pattern.exec(str)` | `re.search(pattern, str)` |
| `str.match(/p/)` | `re.search(pattern, str)` |
| `str.match(/p/g)` | `re.findall(pattern, str)` |
| `str.matchAll(/p/g)` | `re.finditer(pattern, str)` |
| `str.replace(/p/, r)` | `re.sub(pattern, r, str, count=1)` |
| `str.replace(/p/g, r)` | `re.sub(pattern, r, str)` |
| `str.search(/p/)` | `re.search(pattern, str).start()` |
| `str.split(/p/)` | `re.split(pattern, str)` |
| `new RegExp(p, f)` | `re.compile(pattern, flags)` |
| `/p/flags` | `re.compile(r'p', flags)` |

---

**Siguiente:** Ejercicios prácticos para aplicar lo aprendido.
