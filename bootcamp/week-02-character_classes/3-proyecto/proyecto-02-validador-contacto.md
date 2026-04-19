# Proyecto Semana 02: Validador de Datos de Contacto

## 🎯 Objetivo

Crear un sistema de validación para datos de contacto usando character classes:

- `[abc]`, `[a-z]`, `[^...]`
- `\d`, `\w`, `\s`
- `\b` (word boundary)

## 📋 Descripción

Construirás un validador de formulario de contacto para una empresa.

### Campos a Validar

| Campo           | Formato                         | Ejemplo             |
| --------------- | ------------------------------- | ------------------- |
| Código empleado | 2 letras mayúsculas + 4 dígitos | `AB1234`            |
| Extensión       | 3 o 4 dígitos                   | `123`, `4567`       |
| Departamento    | 3 letras mayúsculas             | `TIC`, `ADM`, `VEN` |
| Inicial nombre  | 1 mayúscula + punto             | `J.`, `M.`          |

## 🛠️ Instrucciones

### Paso 1: Definir los Patrones

```javascript
/**
 * Patrones de validación para formulario de contacto
 */

// Código de empleado: 2 mayúsculas + 4 dígitos
// Ejemplo: AB1234, XY9999
const codigoEmpleado = /???/;

// Extensión telefónica: 3 o 4 dígitos
// Ejemplo: 123, 4567
// Nota: Sin cuantificadores {3,4}, crea dos patrones o uno largo
const extension3 = /???/;
const extension4 = /???/;

// Departamento: 3 letras mayúsculas
// Ejemplo: TIC, ADM, VEN
const departamento = /???/;

// Inicial: 1 mayúscula + punto
// Ejemplo: J., M.
const inicial = /???/;
```

### Paso 2: Crear Funciones de Validación

```javascript
/**
 * Valida código de empleado
 *
 * ¿Por qué? El código identifica únicamente a cada empleado
 * ¿Para qué? Verificar formato antes de buscar en BD
 *
 * @param {string} codigo
 * @returns {object}
 */
function validarCodigoEmpleado(codigo) {
  // Tu implementación
}

/**
 * Valida extensión telefónica
 *
 * ¿Por qué? Las extensiones tienen longitud fija
 * ¿Para qué? Routing de llamadas interno
 *
 * @param {string} ext
 * @returns {object}
 */
function validarExtension(ext) {
  // Tu implementación
}

// ... más funciones
```

### Paso 3: Validador Integrado

```javascript
/**
 * Valida un registro completo de contacto
 *
 * @param {object} contacto
 * @returns {object}
 */
function validarContacto(contacto) {
  const errores = [];

  // Validar cada campo
  // Acumular errores
  // Retornar resultado

  return {
    valido: errores.length === 0,
    errores: errores,
    datos: contacto,
  };
}

// Ejemplo de uso:
const contacto = {
  codigo: 'AB1234',
  extension: '456',
  departamento: 'TIC',
  inicial: 'J.',
};

console.log(validarContacto(contacto));
```

### Paso 4: Casos de Prueba

```javascript
// Casos válidos
const validos = [
  { codigo: 'AB1234', extension: '123', departamento: 'TIC', inicial: 'J.' },
  { codigo: 'XY9999', extension: '4567', departamento: 'ADM', inicial: 'M.' },
  { codigo: 'ZZ0000', extension: '999', departamento: 'VEN', inicial: 'A.' },
];

// Casos inválidos
const invalidos = [
  { codigo: 'A1234', extension: '123', departamento: 'TIC', inicial: 'J.' },
  // ↑ Solo 1 letra en código

  { codigo: 'AB1234', extension: '12', departamento: 'TIC', inicial: 'J.' },
  // ↑ Extensión muy corta

  { codigo: 'AB1234', extension: '123', departamento: 'IT', inicial: 'J.' },
  // ↑ Departamento muy corto

  { codigo: 'AB1234', extension: '123', departamento: 'TIC', inicial: 'JJ.' },
  // ↑ Inicial con 2 letras
];
```

## 💡 Hints

<details>
<summary>Hint 1: Código de empleado</summary>

```javascript
const codigoEmpleado = /^[A-Z][A-Z]\d\d\d\d$/;
// 2 mayúsculas + 4 dígitos
```

</details>

<details>
<summary>Hint 2: Extensión (3 o 4 dígitos)</summary>

```javascript
// Opción 1: Dos patrones
const ext3 = /^\d\d\d$/;
const ext4 = /^\d\d\d\d$/;

// Opción 2: Combinado (menos elegante sin cuantificadores)
function validarExtension(ext) {
  return /^\d\d\d$/.test(ext) || /^\d\d\d\d$/.test(ext);
}
```

</details>

<details>
<summary>Hint 3: Departamento</summary>

```javascript
const departamento = /^[A-Z][A-Z][A-Z]$/;
```

</details>

<details>
<summary>Hint 4: Inicial</summary>

```javascript
const inicial = /^[A-Z]\.$/;
// Recuerda escapar el punto
```

</details>

## 🚀 Extensiones (Opcional)

### Extensión 1: Detectar Caracteres Inválidos

Además de validar el formato, identifica qué caracteres específicos son inválidos.

```javascript
function detectarInvalidos(codigo) {
  const invalidos = codigo.match(/[^A-Z0-9]/g);
  return invalidos || [];
}

detectarInvalidos('AB@123#'); // ['@', '#']
```

### Extensión 2: Sugerir Correcciones

```javascript
function sugerirCorreccion(codigo) {
  // Convertir minúsculas a mayúsculas
  // Eliminar caracteres inválidos
  // etc.
}

sugerirCorreccion('ab1234'); // "AB1234"
sugerirCorreccion('AB-1234'); // "AB1234"
```

### Extensión 3: Validador con Word Boundary

Busca códigos de empleado válidos dentro de un texto largo:

```javascript
const texto = 'El empleado AB1234 reporta a XY5678 en el depto TIC';

function encontrarCodigos(texto) {
  // Usa \b para encontrar códigos como palabras completas
}
```

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-02-validador-contacto.md   (este archivo)
├── validador-contacto.js               (tu solución)
└── test-validador.js                   (tests opcionales)
```

## ✅ Criterios de Evaluación

| Criterio                             | Puntos |
| ------------------------------------ | ------ |
| Patrones regex correctos             | 30%    |
| Funciones de validación              | 25%    |
| Validador integrado                  | 20%    |
| Casos de prueba                      | 15%    |
| Documentación (¿por qué? ¿para qué?) | 10%    |

## 📝 Reflexión

Después de completar el proyecto, responde:

1. ¿Cuál es la diferencia entre `[A-Z]` y `\w` para validar letras?
2. ¿Por qué usamos `^` y `$` en todos los patrones?
3. ¿Cómo simplificarías `/^\d\d\d\d$/` con cuantificadores? (spoiler: `\d{4}`)
4. ¿Qué pasaría si el código de empleado tuviera longitud variable?

---

**Solución:** Disponible en `solucion-proyecto-02.js`
