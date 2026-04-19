/**
 * ============================================
 * Solución: Proyecto Semana 01
 * Validador de Código de Producto
 * ============================================
 */

/**
 * Patrón para validar código de producto
 * Formato: XX-000 (2 caracteres, guión, 3 caracteres)
 *
 * ¿Por qué? Los códigos de producto siguen un formato estándar
 *           que debemos validar antes de procesarlos
 * ¿Para qué? Evitar errores en búsquedas, imports y registro de productos
 *
 * Desglose del patrón:
 * ^     → Inicio del string (anchor)
 * ..    → Exactamente 2 caracteres (cualquiera)
 * -     → Guión literal
 * ...   → Exactamente 3 caracteres (cualquiera)
 * $     → Fin del string (anchor)
 */
const codigoPattern = /^..-...$/;

/**
 * Valida si un código de producto tiene el formato correcto
 *
 * ¿Por qué? Centralizar la lógica de validación en una función
 * ¿Para qué? Reutilizar en múltiples partes de la aplicación
 *
 * @param {string} codigo - El código a validar
 * @returns {object} Objeto con resultado de validación
 */
function validarCodigo(codigo) {
  const esValido = codigoPattern.test(codigo);

  return {
    codigo: codigo,
    valido: esValido,
    mensaje: esValido ? '✅ Formato correcto' : '❌ Formato inválido',
  };
}

/**
 * Versión mejorada con mensajes específicos
 *
 * ¿Por qué? El usuario necesita saber QUÉ está mal, no solo que está mal
 * ¿Para qué? Mejor UX y debugging más fácil
 *
 * @param {string} codigo - El código a validar
 * @returns {object} Objeto con resultado detallado
 */
function validarCodigoDetallado(codigo) {
  // Validar que no esté vacío
  if (!codigo || codigo.length === 0) {
    return {
      codigo: codigo,
      valido: false,
      mensaje: '❌ El código no puede estar vacío',
    };
  }

  // Validar longitud total (XX-000 = 6 caracteres)
  if (codigo.length !== 6) {
    return {
      codigo: codigo,
      valido: false,
      mensaje: `❌ Longitud incorrecta: ${codigo.length} (esperado: 6)`,
    };
  }

  // Validar que tenga guión en posición correcta
  if (codigo[2] !== '-') {
    return {
      codigo: codigo,
      valido: false,
      mensaje: '❌ Falta el guión en la posición 3',
    };
  }

  // Si pasa todas las validaciones
  return {
    codigo: codigo,
    valido: true,
    mensaje: '✅ Formato correcto',
    partes: {
      prefijo: codigo.substring(0, 2),
      numero: codigo.substring(3),
    },
  };
}

// ============================================
// CASOS DE PRUEBA
// ============================================

console.log('=== Validación Básica ===\n');

// Casos válidos
console.log(validarCodigo('AB-123')); // ✅
console.log(validarCodigo('XY-999')); // ✅
console.log(validarCodigo('ZZ-000')); // ✅

console.log('\n--- Casos inválidos ---\n');

// Casos inválidos
console.log(validarCodigo('ABC-123')); // ❌ 3 letras
console.log(validarCodigo('A-123')); // ❌ 1 letra
console.log(validarCodigo('AB123')); // ❌ sin guión
console.log(validarCodigo('AB-12')); // ❌ 2 dígitos
console.log(validarCodigo('AB-1234')); // ❌ 4 dígitos
console.log(validarCodigo('')); // ❌ vacío

console.log('\n=== Validación Detallada ===\n');

// Pruebas con versión detallada
console.log(validarCodigoDetallado('AB-123'));
console.log(validarCodigoDetallado(''));
console.log(validarCodigoDetallado('ABC-123'));
console.log(validarCodigoDetallado('AB123'));

// ============================================
// EXTENSIÓN: Validadores adicionales
// ============================================

/**
 * Validador de código de categoría
 * Formato: CAT-00
 *
 * ¿Por qué? Las categorías tienen su propio formato
 * ¿Para qué? Diferenciar categorías de productos
 */
const categoriaPattern = /^CAT-..$/;

/**
 * Validador de código de sucursal
 * Formato: S-000
 *
 * ¿Por qué? Las sucursales usan un formato más corto
 * ¿Para qué? Identificar ubicaciones de inventario
 */
const sucursalPattern = /^S-...$/;

/**
 * Validador universal que detecta el tipo
 *
 * ¿Por qué? A veces recibimos códigos mixtos
 * ¿Para qué? Clasificar y validar en un solo paso
 */
function validarCodigoUniversal(codigo) {
  if (codigoPattern.test(codigo)) {
    return { tipo: 'producto', valido: true, codigo };
  }
  if (categoriaPattern.test(codigo)) {
    return { tipo: 'categoria', valido: true, codigo };
  }
  if (sucursalPattern.test(codigo)) {
    return { tipo: 'sucursal', valido: true, codigo };
  }
  return { tipo: 'desconocido', valido: false, codigo };
}

console.log('\n=== Validador Universal ===\n');
console.log(validarCodigoUniversal('AB-123')); // producto
console.log(validarCodigoUniversal('CAT-05')); // categoria
console.log(validarCodigoUniversal('S-001')); // sucursal
console.log(validarCodigoUniversal('XYZ')); // desconocido
