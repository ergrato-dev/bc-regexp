# Proyecto Semana 01: Validador de Formato Básico

## 🎯 Objetivo

Crear un validador simple que use los conceptos aprendidos:

- Literales
- Metacharacter dot (`.`)
- Anchors (`^`, `$`)
- Escape (`\`)

## 📋 Descripción

Construirás un validador de **códigos de producto** para una tienda ficticia.

### Formato del Código de Producto

```
XX-000
│  │
│  └─ 3 dígitos (cualquier carácter por ahora)
└──── 2 letras (cualquier carácter por ahora)
```

**Ejemplos válidos:**

- `AB-123`
- `XY-999`
- `CD-001`

**Ejemplos inválidos:**

- `ABC-123` (3 letras en vez de 2)
- `AB123` (falta el guión)
- `AB-12` (solo 2 dígitos)
- `ab-123` (válido en formato, pero asumimos mayúsculas)

## 🛠️ Instrucciones

### Paso 1: Crear el Patrón Base

```javascript
/**
 * Validador de código de producto
 *
 * ¿Por qué? Los códigos de producto deben seguir un formato estándar
 * ¿Para qué? Validar input antes de buscar en base de datos
 */

// Tu patrón aquí:
const codigoPattern = /???/;
```

### Paso 2: Crear la Función Validadora

```javascript
/**
 * Valida si un código de producto tiene el formato correcto
 *
 * ¿Por qué? Centralizar la lógica de validación
 * ¿Para qué? Reutilizar en formularios, APIs, imports de datos
 *
 * @param {string} codigo - El código a validar
 * @returns {object} - Resultado de la validación
 */
function validarCodigo(codigo) {
  // Tu implementación aquí
}
```

### Paso 3: Casos de Prueba

Prueba tu validador con estos casos:

```javascript
// Casos válidos
console.log(validarCodigo('AB-123')); // ✅ válido
console.log(validarCodigo('XY-999')); // ✅ válido
console.log(validarCodigo('ZZ-000')); // ✅ válido

// Casos inválidos
console.log(validarCodigo('ABC-123')); // ❌ 3 letras
console.log(validarCodigo('A-123')); // ❌ 1 letra
console.log(validarCodigo('AB123')); // ❌ sin guión
console.log(validarCodigo('AB-12')); // ❌ 2 dígitos
console.log(validarCodigo('AB-1234')); // ❌ 4 dígitos
console.log(validarCodigo('')); // ❌ vacío
```

## 💡 Hints

<details>
<summary>Hint 1: Estructura del patrón</summary>

El patrón tiene esta estructura:

- Inicio: `^`
- 2 caracteres: `..`
- Guión literal: `-`
- 3 caracteres: `...`
- Fin: `$`

</details>

<details>
<summary>Hint 2: El patrón completo</summary>

```javascript
const codigoPattern = /^..-...$/;
```

</details>

<details>
<summary>Hint 3: Función básica</summary>

```javascript
function validarCodigo(codigo) {
  const esValido = codigoPattern.test(codigo);
  return {
    codigo: codigo,
    valido: esValido,
    mensaje: esValido ? 'Formato correcto' : 'Formato inválido',
  };
}
```

</details>

## 🚀 Extensiones (Opcional)

### Extensión 1: Mensajes Específicos

Mejora el validador para dar mensajes más específicos sobre qué está mal.

```javascript
function validarCodigoDetallado(codigo) {
  // Verificar longitud
  // Verificar que tenga guión
  // Verificar posición del guión
  // etc.
}
```

### Extensión 2: Validador de Múltiples Formatos

Crea validadores para otros formatos de la "tienda":

| Tipo      | Formato  | Ejemplo |
| --------- | -------- | ------- |
| Producto  | `XX-000` | AB-123  |
| Categoría | `CAT-00` | CAT-05  |
| Sucursal  | `S-000`  | S-001   |

### Extensión 3: Interfaz de Usuario

Crea un HTML simple con un input y muestra el resultado de la validación en tiempo real.

## 📁 Estructura de Entrega

```
3-proyecto/
├── proyecto-01-validador.md   (este archivo)
├── validador.js               (tu solución)
└── index.html                 (opcional - UI)
```

## ✅ Criterios de Evaluación

| Criterio                                  | Puntos |
| ----------------------------------------- | ------ |
| Patrón regex correcto                     | 30%    |
| Función validadora funcional              | 30%    |
| Casos de prueba pasados                   | 20%    |
| Código documentado (¿por qué? ¿para qué?) | 20%    |

## 📝 Reflexión

Después de completar el proyecto, responde:

1. ¿Qué limitación tiene usar `.` para validar "letras" y "números"?
2. ¿Qué pasaría si alguien ingresa "@@-###"? ¿Sería válido?
3. ¿Cómo crees que podríamos ser más específicos? (spoiler: semana 02)

---

**Solución:** Disponible en `solucion-proyecto-01.js`
