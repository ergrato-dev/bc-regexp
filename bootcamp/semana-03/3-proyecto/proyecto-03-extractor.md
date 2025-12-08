# Proyecto Semana 03: Extractor de Datos de Texto

## 🎯 Objetivo

Crear un sistema de extracción de datos que use quantifiers para:

- Extraer precios, fechas, emails y teléfonos
- Validar formatos con longitud variable
- Parsear logs y documentos estructurados

## 📋 Descripción

Construirás un **extractor de datos** para un sistema de facturación que procesa texto no estructurado.

### Datos a Extraer

| Tipo       | Formato                           | Ejemplo                    |
| ---------- | --------------------------------- | -------------------------- |
| Precio     | $XXX.XX o $XXX                    | `$99.99`, `$1000`          |
| Fecha      | DD/MM/YYYY                        | `15/01/2024`               |
| Email      | usuario@dominio.ext               | `cliente@empresa.com`      |
| Teléfono   | 9 dígitos (con o sin separadores) | `612345678`, `612 345 678` |
| Referencia | REF-XXXXX (5+ dígitos)            | `REF-12345`, `REF-999999`  |

## 🛠️ Instrucciones

### Paso 1: Documento de Prueba

```javascript
const documento = `
FACTURA #2024-0042
Fecha: 15/01/2024
Cliente: Juan Pérez (cliente@empresa.com)
Teléfono: 612 345 678

PRODUCTOS:
- Laptop Dell XPS 15        $1299.99
- Mouse Logitech MX         $79.50
- Teclado mecánico          $149
- Monitor 27" 4K            $450.00

SUBTOTAL: $1978.49
IVA (21%): $415.48
TOTAL: $2393.97

Referencia de pago: REF-20240115001
Contacto alternativo: soporte@tienda.es, 91 234 56 78

Gracias por su compra.
`;
```

### Paso 2: Definir Patrones

```javascript
/**
 * Patrón para precios
 * Formato: $X.XX o $X (decimales opcionales)
 *
 * ¿Por qué? Los precios pueden tener o no centavos
 * ¿Para qué? Extraer todos los valores monetarios
 */
const precioPattern = /???/g;

/**
 * Patrón para fechas
 * Formato: DD/MM/YYYY
 *
 * ¿Por qué? Formato europeo estándar
 * ¿Para qué? Identificar fechas en documentos
 */
const fechaPattern = /???/g;

/**
 * Patrón para emails
 * Formato: usuario@dominio.ext
 *
 * ¿Por qué? Los emails tienen estructura predecible
 * ¿Para qué? Extraer contactos
 */
const emailPattern = /???/g;

/**
 * Patrón para teléfonos
 * Formato: 9 dígitos con espacios opcionales
 *
 * ¿Por qué? Los teléfonos vienen en diferentes formatos
 * ¿Para qué? Normalizar números de contacto
 */
const telefonoPattern = /???/g;

/**
 * Patrón para referencias
 * Formato: REF-XXXXX (5+ dígitos)
 *
 * ¿Por qué? Las referencias identifican transacciones
 * ¿Para qué? Tracking de pagos
 */
const referenciaPattern = /???/g;
```

### Paso 3: Crear Extractor

```javascript
/**
 * Extrae todos los datos de un documento
 *
 * ¿Por qué? Centralizar la lógica de extracción
 * ¿Para qué? Procesar múltiples documentos uniformemente
 *
 * @param {string} texto - El documento a procesar
 * @returns {object} Datos extraídos
 */
function extraerDatos(texto) {
  return {
    precios: texto.match(precioPattern) || [],
    fechas: texto.match(fechaPattern) || [],
    emails: texto.match(emailPattern) || [],
    telefonos: texto.match(telefonoPattern) || [],
    referencias: texto.match(referenciaPattern) || [],
  };
}

// Uso
const datos = extraerDatos(documento);
console.log(datos);
```

### Paso 4: Funciones de Utilidad

```javascript
/**
 * Suma todos los precios extraídos
 *
 * @param {string[]} precios - Array de strings de precios
 * @returns {number} Total
 */
function sumarPrecios(precios) {
  // Convertir "$99.99" a 99.99 y sumar
}

/**
 * Normaliza teléfonos (quita espacios y guiones)
 *
 * @param {string[]} telefonos - Array de teléfonos
 * @returns {string[]} Teléfonos normalizados
 */
function normalizarTelefonos(telefonos) {
  // Quitar espacios y guiones
}

/**
 * Valida formato de email más estrictamente
 *
 * @param {string} email - Email a validar
 * @returns {boolean}
 */
function validarEmail(email) {
  // Validación más estricta
}
```

## 💡 Hints

<details>
<summary>Hint para precios</summary>

```javascript
// Precio con decimales opcionales
const precioPattern = /\$\d+(\.\d{2})?/g;

// O más flexible:
const precioPattern2 = /\$[\d,]+(\.\d{2})?/g;
```

</details>

<details>
<summary>Hint para fechas</summary>

```javascript
const fechaPattern = /\d{2}\/\d{2}\/\d{4}/g;
```

</details>

<details>
<summary>Hint para emails</summary>

```javascript
const emailPattern = /[\w.-]+@[\w.-]+\.\w{2,}/g;
```

</details>

<details>
<summary>Hint para teléfonos</summary>

```javascript
// Teléfono con espacios opcionales
const telefonoPattern = /\d{2,3}[\s-]?\d{3}[\s-]?\d{2,3}[\s-]?\d{2,3}/g;

// O más simple:
const telefonoPattern2 = /[6-9][\d\s]{8,11}/g;
```

</details>

<details>
<summary>Hint para referencias</summary>

```javascript
const referenciaPattern = /REF-\d{5,}/g;
```

</details>

## 🚀 Extensiones (Opcional)

### Extensión 1: Parser de Facturas

Crea un parser más completo que extraiga:

- Número de factura
- Nombre del cliente
- Lista de productos con precio individual
- Subtotal, IVA y total

### Extensión 2: Validador de Formato

Además de extraer, valida que los datos tengan sentido:

- Fechas válidas (no 99/99/9999)
- Precios positivos
- Emails con dominios conocidos

### Extensión 3: Generador de Reporte

```javascript
function generarReporte(datos) {
  return `
    === REPORTE DE EXTRACCIÓN ===
    Precios encontrados: ${datos.precios.length}
    Total: $${sumarPrecios(datos.precios)}
    Emails: ${datos.emails.join(', ')}
    Teléfonos: ${normalizarTelefonos(datos.telefonos).join(', ')}
    Referencias: ${datos.referencias.join(', ')}
    `;
}
```

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-03-extractor.md      (este archivo)
├── extractor.js                   (tu solución)
└── test-extractor.js              (tests)
```

## ✅ Criterios de Evaluación

| Criterio                 | Puntos |
| ------------------------ | ------ |
| Patrones regex correctos | 30%    |
| Extractor funcional      | 25%    |
| Funciones de utilidad    | 20%    |
| Manejo de casos edge     | 15%    |
| Documentación            | 10%    |

## 📝 Reflexión

Después de completar el proyecto, responde:

1. ¿Por qué usamos `(\.\d{2})?` para decimales en lugar de `\.?\d*`?
2. ¿Qué problemas podrían surgir con el patrón de email simplificado?
3. ¿Cómo manejarías teléfonos internacionales (+34 612...)?
4. ¿Qué diferencia hay entre usar `+` vs `{1,}` en términos de legibilidad?

---

**Solución:** Disponible en `solucion-proyecto-03.js`
