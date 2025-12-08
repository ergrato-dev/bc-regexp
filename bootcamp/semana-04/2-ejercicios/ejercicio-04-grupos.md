# Ejercicios - Semana 04: Grupos y Capturas

## Ejercicio 1: Extraer Partes de Email

**Objetivo:** Capturar usuario y dominio de emails.

**Texto de prueba:**

```
Lista de contactos:
ana@gmail.com
carlos.perez@empresa.es
soporte@mi-tienda.com
```

**Requisitos:**

1. Capturar el usuario (antes del @)
2. Capturar el dominio completo (después del @)

**Resultado esperado:**

```javascript
// Para cada email:
// Grupo 1: usuario
// Grupo 2: dominio
```

<details>
<summary>💡 Hint</summary>

```javascript
// El @ separa usuario de dominio
// Usuario: caracteres de palabra, puntos, guiones
// Dominio: igual, incluyendo el TLD
```

</details>

---

## Ejercicio 2: Parser de Fecha

**Objetivo:** Extraer día, mes y año de fechas.

**Texto de prueba:**

```
Fechas importantes:
15/01/2024
28-12-2023
01.06.2025
```

**Requisitos:**

1. Aceptar separadores: `/`, `-`, `.`
2. Usar grupos nombrados: `dia`, `mes`, `anio`
3. El separador debe ser consistente en toda la fecha

**Resultado esperado:**

```javascript
{ dia: "15", mes: "01", anio: "2024" }
{ dia: "28", mes: "12", anio: "2023" }
{ dia: "01", mes: "06", anio: "2025" }
```

<details>
<summary>💡 Hint</summary>

```javascript
// Captura el primer separador y usa backreference
// (?<dia>\d{2})...separador...mes...mismoSeparador...año
```

</details>

---

## Ejercicio 3: Encontrar Palabras Duplicadas

**Objetivo:** Detectar palabras repetidas consecutivamente.

**Texto de prueba:**

```
El el gato saltó sobre la la cerca y y corrió muy muy rápido.
```

**Requisitos:**

1. Capturar palabras duplicadas (case insensitive)
2. Retornar la palabra y su posición

**Resultado esperado:**

```javascript
['El el', 'la la', 'y y', 'muy muy'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// Captura una palabra, espacio, backreference
// Usa flag 'i' para case insensitive
```

</details>

---

## Ejercicio 4: Validar Etiquetas HTML

**Objetivo:** Encontrar etiquetas HTML con cierre correcto.

**Texto de prueba:**

```html
<div>contenido</div>
<span>texto</span>
<p>párrafo</div>
<h1>título</h1>
<a>enlace</b>
```

**Requisitos:**

1. Solo devolver etiquetas con apertura y cierre correcto
2. Capturar el nombre de la etiqueta y su contenido

**Resultado esperado:**

```javascript
[
  { tag: 'div', contenido: 'contenido' },
  { tag: 'span', contenido: 'texto' },
  { tag: 'h1', contenido: 'título' },
];
```

<details>
<summary>💡 Hint</summary>

```javascript
// <(tag)>contenido</\1>
// Usa named groups para mayor claridad
```

</details>

---

## Ejercicio 5: Reformatear Nombres

**Objetivo:** Convertir "Apellido, Nombre" a "Nombre Apellido".

**Texto de prueba:**

```
García, Juan
López, María Elena
Martínez de la Cruz, Carlos
```

**Requisitos:**

1. Usar `replace()` con grupos
2. Manejar apellidos compuestos

**Resultado esperado:**

```
Juan García
María Elena López
Carlos Martínez de la Cruz
```

<details>
<summary>💡 Hint</summary>

```javascript
// El apellido viene antes de la coma
// El nombre viene después
// Usa (.+),\s*(.+) y $2 $1
```

</details>

---

## Ejercicio 6: Números de Teléfono

**Objetivo:** Extraer partes de números de teléfono.

**Texto de prueba:**

```
+34 612 345 678
+1 (555) 123-4567
+44 20 7946 0958
```

**Requisitos:**

1. Capturar código de país
2. Capturar el resto del número (sin espacios)
3. Usar named groups

**Resultado esperado:**

```javascript
{ codigo: "+34", numero: "612345678" }
{ codigo: "+1", numero: "5551234567" }
{ codigo: "+44", numero: "2079460958" }
```

<details>
<summary>💡 Hint</summary>

```javascript
// Código: \+\d{1,3}
// Resto: múltiples grupos de dígitos
// Usa replace para limpiar espacios/paréntesis
```

</details>

---

## Ejercicio 7: Non-Capturing Groups

**Objetivo:** Simplificar la salida eliminando grupos innecesarios.

**Texto de prueba:**

```
https://www.google.com
http://example.org
https://api.github.com
```

**Requisitos:**

1. Extraer solo el dominio (sin www.)
2. No capturar el protocolo ni el www.
3. Solo debe haber 1 grupo de captura

**Resultado esperado:**

```javascript
['google.com', 'example.org', 'api.github.com'];
```

<details>
<summary>💡 Hint</summary>

```javascript
// (?:https?):\/\/(?:www\.)?(\S+)
// Solo el dominio es capture group
```

</details>

---

## Desafío: Parser de URL Completo

**Objetivo:** Crear un parser completo de URLs.

**URLs de prueba:**

```
https://www.ejemplo.com:8080/ruta/pagina.html?id=123&lang=es#seccion
http://api.servicio.io/v1/users
ftp://files.servidor.net/descargas/archivo.zip
```

**Requisitos:**

1. Extraer con named groups:
   - `protocolo`: http, https, ftp
   - `subdominio`: www, api, files (opcional)
   - `dominio`: ejemplo, servicio, servidor
   - `tld`: com, io, net
   - `puerto`: 8080 (opcional)
   - `path`: /ruta/pagina.html (opcional)
   - `query`: id=123&lang=es (opcional)
   - `fragment`: seccion (opcional)

**Resultado esperado:**

```javascript
{
  protocolo: "https",
  subdominio: "www",
  dominio: "ejemplo",
  tld: "com",
  puerto: "8080",
  path: "/ruta/pagina.html",
  query: "id=123&lang=es",
  fragment: "seccion"
}
```

<details>
<summary>💡 Hint 1: Estructura general</summary>

```javascript
// protocolo://[subdominio.]dominio.tld[:puerto][/path][?query][#fragment]
```

</details>

<details>
<summary>💡 Hint 2: Patrón parcial</summary>

```javascript
// Empieza con las partes obligatorias:
// (?<protocolo>https?|ftp):\/\/
// (?<dominio>[\w-]+)
// \.(?<tld>\w+)
```

</details>

---

## Recursos

- [MDN: Groups and Backreferences](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Groups_and_Backreferences)
- [regex101.com](https://regex101.com) - Visualiza grupos

---

**Soluciones:** [solucion-04-grupos.md](solucion-04-grupos.md)
