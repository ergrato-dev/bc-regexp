# Soluciones - Semana 04: Grupos y Capturas

## Ejercicio 1: Extraer Partes de Email

```javascript
/**
 * Patrón: Email con usuario y dominio
 *
 * ¿Por qué? Los emails tienen estructura usuario@dominio
 * ¿Para qué? Extraer ambas partes para procesamiento
 *
 * Desglose:
 * ([\w.-]+)   → Grupo 1: usuario (letras, números, ., -)
 * @           → Arroba literal
 * ([\w.-]+)   → Grupo 2: dominio completo
 */
const emailPattern = /([\w.-]+)@([\w.-]+)/g;

const texto = `Lista de contactos:
ana@gmail.com
carlos.perez@empresa.es
soporte@mi-tienda.com`;

for (const match of texto.matchAll(emailPattern)) {
  console.log(`Usuario: ${match[1]}, Dominio: ${match[2]}`);
}
// Usuario: ana, Dominio: gmail.com
// Usuario: carlos.perez, Dominio: empresa.es
// Usuario: soporte, Dominio: mi-tienda.com
```

---

## Ejercicio 2: Parser de Fecha

```javascript
/**
 * Patrón: Fecha con separador consistente
 *
 * ¿Por qué? El separador debe ser el mismo en toda la fecha
 * ¿Para qué? Validar y extraer componentes de fecha
 *
 * Desglose:
 * (?<dia>\d{2})    → Named group: día
 * ([\/.-])         → Grupo anónimo: separador
 * (?<mes>\d{2})    → Named group: mes
 * \2               → Backreference: mismo separador
 * (?<anio>\d{4})   → Named group: año
 */
const fechaPattern = /(?<dia>\d{2})([\/.-])(?<mes>\d{2})\2(?<anio>\d{4})/g;

const texto = `Fechas importantes:
15/01/2024
28-12-2023
01.06.2025
15/06-2024`; // Esta no coincide por separadores mixtos

for (const match of texto.matchAll(fechaPattern)) {
  console.log(match.groups);
}
// { dia: '15', mes: '01', anio: '2024' }
// { dia: '28', mes: '12', anio: '2023' }
// { dia: '01', mes: '06', anio: '2025' }
```

---

## Ejercicio 3: Encontrar Palabras Duplicadas

```javascript
/**
 * Patrón: Palabra seguida de sí misma
 *
 * ¿Por qué? Los errores tipográficos incluyen repeticiones
 * ¿Para qué? Detectar y corregir duplicados
 *
 * Desglose:
 * \b         → Word boundary
 * (\w+)      → Grupo 1: una palabra
 * \s+        → Uno o más espacios
 * \1         → Backreference: la misma palabra
 * \b         → Word boundary
 */
const duplicadaPattern = /\b(\w+)\s+\1\b/gi;

const texto = 'El el gato saltó sobre la la cerca y y corrió muy muy rápido.';

console.log(texto.match(duplicadaPattern));
// ["El el", "la la", "y y", "muy muy"]

// Para corregir:
const corregido = texto.replace(duplicadaPattern, '$1');
console.log(corregido);
// "El gato saltó sobre la cerca y corrió muy rápido."
```

---

## Ejercicio 4: Validar Etiquetas HTML

```javascript
/**
 * Patrón: Etiqueta HTML con apertura y cierre correcto
 *
 * ¿Por qué? La etiqueta de cierre debe coincidir con la de apertura
 * ¿Para qué? Validar estructura HTML
 *
 * Desglose:
 * <(?<tag>\w+)>     → Apertura con nombre capturado
 * (?<contenido>.*?) → Contenido (lazy)
 * <\/\k<tag>>       → Cierre con backreference al nombre
 */
const htmlPattern = /<(?<tag>\w+)>(?<contenido>.*?)<\/\k<tag>>/gs;

const texto = `<div>contenido</div>
<span>texto</span>
<p>párrafo</div>
<h1>título</h1>
<a>enlace</b>`;

const resultados = [];
for (const match of texto.matchAll(htmlPattern)) {
  resultados.push({
    tag: match.groups.tag,
    contenido: match.groups.contenido,
  });
}

console.log(resultados);
// [
//   { tag: 'div', contenido: 'contenido' },
//   { tag: 'span', contenido: 'texto' },
//   { tag: 'h1', contenido: 'título' }
// ]
```

---

## Ejercicio 5: Reformatear Nombres

```javascript
/**
 * Patrón: "Apellido, Nombre" → "Nombre Apellido"
 *
 * ¿Por qué? El formato de entrada es diferente al deseado
 * ¿Para qué? Normalizar formato de nombres
 *
 * Desglose:
 * (.+?)      → Grupo 1: apellido (lazy para manejar compuestos)
 * ,\s*       → Coma y espacios opcionales
 * (.+)       → Grupo 2: nombre completo
 */
const nombrePattern = /(.+?),\s*(.+)/gm;

const texto = `García, Juan
López, María Elena
Martínez de la Cruz, Carlos`;

const resultado = texto.replace(nombrePattern, '$2 $1');
console.log(resultado);
// Juan García
// María Elena López
// Carlos Martínez de la Cruz

// Con named groups (más legible):
const nombrePatternNamed = /(?<apellido>.+?),\s*(?<nombre>.+)/gm;
const resultado2 = texto.replace(nombrePatternNamed, '$<nombre> $<apellido>');
console.log(resultado2);
```

---

## Ejercicio 6: Números de Teléfono

```javascript
/**
 * Patrón: Teléfono internacional
 *
 * ¿Por qué? Los formatos internacionales varían
 * ¿Para qué? Extraer código y número normalizado
 *
 * Desglose:
 * (?<codigo>\+\d{1,3})  → Código de país
 * [\s(]*                → Espacios o paréntesis opcionales
 * (?<numero>[\d\s()-]+) → Resto del número
 */
const telefonoPattern = /(?<codigo>\+\d{1,3})[\s(]*(?<numero>[\d\s()-]+)/g;

const texto = `+34 612 345 678
+1 (555) 123-4567
+44 20 7946 0958`;

for (const match of texto.matchAll(telefonoPattern)) {
  const { codigo, numero } = match.groups;
  // Limpiar el número (quitar espacios, paréntesis, guiones)
  const numeroLimpio = numero.replace(/[\s()-]/g, '').trim();
  console.log({ codigo, numero: numeroLimpio });
}
// { codigo: '+34', numero: '612345678' }
// { codigo: '+1', numero: '5551234567' }
// { codigo: '+44', numero: '2079460958' }
```

---

## Ejercicio 7: Non-Capturing Groups

```javascript
/**
 * Patrón: Extraer solo dominio de URL
 *
 * ¿Por qué? No necesitamos capturar protocolo ni www
 * ¿Para qué? Simplificar la salida
 *
 * Desglose:
 * (?:https?|ftp):\/\/  → Non-capturing: protocolo
 * (?:www\.)?           → Non-capturing: www (opcional)
 * ([\w.-]+)            → Capturing: dominio
 */
const dominioPattern = /(?:https?|ftp):\/\/(?:www\.)?([\w.-]+)/g;

const texto = `https://www.google.com
http://example.org
https://api.github.com`;

const dominios = [];
for (const match of texto.matchAll(dominioPattern)) {
  dominios.push(match[1]);
}

console.log(dominios);
// ["google.com", "example.org", "api.github.com"]
```

---

## Desafío: Parser de URL Completo

```javascript
/**
 * Patrón: URL completa con todas sus partes
 *
 * ¿Por qué? Las URLs tienen múltiples componentes opcionales
 * ¿Para qué? Parser completo para análisis de URLs
 *
 * Estructura:
 * protocolo://[subdominio.]dominio.tld[:puerto][/path][?query][#fragment]
 */
const urlPattern =
  /^(?<protocolo>https?|ftp):\/\/(?:(?<subdominio>[\w-]+)\.)?(?<dominio>[\w-]+)\.(?<tld>\w+)(?::(?<puerto>\d+))?(?<path>\/[^?#]*)?(?:\?(?<query>[^#]*))?(?:#(?<fragment>.*))?$/;

const urls = [
  'https://www.ejemplo.com:8080/ruta/pagina.html?id=123&lang=es#seccion',
  'http://api.servicio.io/v1/users',
  'ftp://files.servidor.net/descargas/archivo.zip',
];

urls.forEach((url) => {
  const match = url.match(urlPattern);
  if (match) {
    console.log(`\n${url}`);
    console.log(match.groups);
  }
});

// https://www.ejemplo.com:8080/ruta/pagina.html?id=123&lang=es#seccion
// {
//   protocolo: 'https',
//   subdominio: 'www',
//   dominio: 'ejemplo',
//   tld: 'com',
//   puerto: '8080',
//   path: '/ruta/pagina.html',
//   query: 'id=123&lang=es',
//   fragment: 'seccion'
// }

// http://api.servicio.io/v1/users
// {
//   protocolo: 'http',
//   subdominio: 'api',
//   dominio: 'servicio',
//   tld: 'io',
//   puerto: undefined,
//   path: '/v1/users',
//   query: undefined,
//   fragment: undefined
// }

// ftp://files.servidor.net/descargas/archivo.zip
// {
//   protocolo: 'ftp',
//   subdominio: 'files',
//   dominio: 'servidor',
//   tld: 'net',
//   puerto: undefined,
//   path: '/descargas/archivo.zip',
//   query: undefined,
//   fragment: undefined
// }

/**
 * Función utilitaria para parsear URLs
 */
function parseURL(url) {
  const match = url.match(urlPattern);
  if (!match) return null;

  // Limpiar undefined
  const result = {};
  for (const [key, value] of Object.entries(match.groups)) {
    if (value !== undefined) {
      result[key] = value;
    }
  }
  return result;
}

console.log(parseURL('https://www.google.com'));
// { protocolo: 'https', subdominio: 'www', dominio: 'google', tld: 'com' }
```

---

## Explicación del Patrón del Parser de URL

```javascript
/^
  (?<protocolo>https?|ftp)       // Protocolo: http, https, o ftp
  :\/\/                          // :// literal
  (?:                            // Non-capturing group para subdominio
    (?<subdominio>[\w-]+)        // Subdominio capturado
    \.                           // Punto
  )?                             // Todo el grupo es opcional
  (?<dominio>[\w-]+)             // Dominio principal
  \.                             // Punto
  (?<tld>\w+)                    // TLD (com, org, etc.)
  (?:                            // Non-capturing para puerto
    :(?<puerto>\d+)              // Puerto capturado
  )?                             // Opcional
  (?<path>\/[^?#]*)?             // Path: / seguido de cualquier cosa excepto ? o #
  (?:                            // Non-capturing para query
    \?(?<query>[^#]*)            // Query sin el #
  )?                             // Opcional
  (?:                            // Non-capturing para fragment
    \#(?<fragment>.*)            // Fragment hasta el final
  )?                             // Opcional
$/
```

---

**Siguiente:** [Proyecto Semana 04](../3-proyecto/proyecto-04-parser.md)
