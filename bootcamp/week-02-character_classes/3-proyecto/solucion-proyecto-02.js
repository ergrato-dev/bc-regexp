/**
 * ============================================
 * Solución: Proyecto Semana 02
 * Validador de Datos de Contacto
 * ============================================
 */

// ============================================
// PATRONES DE VALIDACIÓN
// ============================================

/**
 * Patrón: Código de empleado
 * Formato: 2 letras mayúsculas + 4 dígitos
 *
 * ¿Por qué? El código identifica únicamente a cada empleado en el sistema
 * ¿Para qué? Validar antes de consultas a BD, evitar errores de formato
 *
 * Desglose:
 * ^        → Inicio del string
 * [A-Z]    → Primera letra mayúscula
 * [A-Z]    → Segunda letra mayúscula
 * \d       → Primer dígito
 * \d       → Segundo dígito
 * \d       → Tercer dígito
 * \d       → Cuarto dígito
 * $        → Fin del string
 */
const patronCodigoEmpleado = /^[A-Z][A-Z]\d\d\d\d$/;

/**
 * Patrón: Extensión telefónica (3 dígitos)
 *
 * ¿Por qué? Las extensiones cortas son para departamentos principales
 * ¿Para qué? Routing de llamadas internas
 */
const patronExtension3 = /^\d\d\d$/;

/**
 * Patrón: Extensión telefónica (4 dígitos)
 *
 * ¿Por qué? Las extensiones largas son para empleados individuales
 * ¿Para qué? Llamadas directas a escritorio
 */
const patronExtension4 = /^\d\d\d\d$/;

/**
 * Patrón: Departamento
 * Formato: 3 letras mayúsculas
 *
 * ¿Por qué? Los códigos de departamento son abreviaturas estándar
 * ¿Para qué? Categorización y reportes
 */
const patronDepartamento = /^[A-Z][A-Z][A-Z]$/;

/**
 * Patrón: Inicial del nombre
 * Formato: 1 letra mayúscula + punto
 *
 * ¿Por qué? Formato estándar para iniciales
 * ¿Para qué? Identificación rápida en listados
 */
const patronInicial = /^[A-Z]\.$/;

// ============================================
// FUNCIONES DE VALIDACIÓN INDIVIDUALES
// ============================================

/**
 * Valida código de empleado
 *
 * ¿Por qué? Centralizar la lógica de validación del código
 * ¿Para qué? Reutilizar en formularios, APIs, imports
 *
 * @param {string} codigo - El código a validar
 * @returns {object} Resultado con valido, mensaje y detalles
 */
function validarCodigoEmpleado(codigo) {
  if (!codigo) {
    return {
      valido: false,
      mensaje: 'El código es requerido',
      campo: 'codigo',
    };
  }

  if (patronCodigoEmpleado.test(codigo)) {
    return {
      valido: true,
      mensaje: 'Código válido',
      campo: 'codigo',
      partes: {
        letras: codigo.substring(0, 2),
        numero: codigo.substring(2),
      },
    };
  }

  // Detectar el error específico
  let detalle = '';
  if (codigo.length !== 6) {
    detalle = `Longitud incorrecta: ${codigo.length} (esperado: 6)`;
  } else if (!/^[A-Z][A-Z]/.test(codigo)) {
    detalle = 'Debe comenzar con 2 letras mayúsculas';
  } else if (!/\d\d\d\d$/.test(codigo)) {
    detalle = 'Debe terminar con 4 dígitos';
  }

  return {
    valido: false,
    mensaje: 'Código inválido',
    campo: 'codigo',
    detalle: detalle,
  };
}

/**
 * Valida extensión telefónica
 *
 * ¿Por qué? Las extensiones deben ser 3 o 4 dígitos exactos
 * ¿Para qué? Asegurar compatibilidad con el sistema telefónico
 *
 * @param {string} extension - La extensión a validar
 * @returns {object} Resultado de validación
 */
function validarExtension(extension) {
  if (!extension) {
    return {
      valido: false,
      mensaje: 'La extensión es requerida',
      campo: 'extension',
    };
  }

  const es3Digitos = patronExtension3.test(extension);
  const es4Digitos = patronExtension4.test(extension);

  if (es3Digitos || es4Digitos) {
    return {
      valido: true,
      mensaje: 'Extensión válida',
      campo: 'extension',
      tipo: es3Digitos ? 'departamento' : 'individual',
    };
  }

  let detalle = '';
  if (extension.length < 3) {
    detalle = 'Muy corta (mínimo 3 dígitos)';
  } else if (extension.length > 4) {
    detalle = 'Muy larga (máximo 4 dígitos)';
  } else if (/[^\d]/.test(extension)) {
    detalle = 'Solo debe contener dígitos';
  }

  return {
    valido: false,
    mensaje: 'Extensión inválida',
    campo: 'extension',
    detalle: detalle,
  };
}

/**
 * Valida código de departamento
 *
 * ¿Por qué? Los departamentos usan códigos estandarizados
 * ¿Para qué? Categorización consistente en reportes
 *
 * @param {string} depto - El código de departamento
 * @returns {object} Resultado de validación
 */
function validarDepartamento(depto) {
  if (!depto) {
    return {
      valido: false,
      mensaje: 'El departamento es requerido',
      campo: 'departamento',
    };
  }

  if (patronDepartamento.test(depto)) {
    return {
      valido: true,
      mensaje: 'Departamento válido',
      campo: 'departamento',
    };
  }

  let detalle = '';
  if (depto.length !== 3) {
    detalle = `Longitud incorrecta: ${depto.length} (esperado: 3)`;
  } else if (/[^A-Z]/.test(depto)) {
    detalle = 'Solo letras mayúsculas permitidas';
  }

  return {
    valido: false,
    mensaje: 'Departamento inválido',
    campo: 'departamento',
    detalle: detalle,
  };
}

/**
 * Valida inicial del nombre
 *
 * ¿Por qué? Las iniciales tienen formato específico
 * ¿Para qué? Consistencia en listados y documentos
 *
 * @param {string} inicial - La inicial a validar
 * @returns {object} Resultado de validación
 */
function validarInicial(inicial) {
  if (!inicial) {
    return {
      valido: false,
      mensaje: 'La inicial es requerida',
      campo: 'inicial',
    };
  }

  if (patronInicial.test(inicial)) {
    return {
      valido: true,
      mensaje: 'Inicial válida',
      campo: 'inicial',
      letra: inicial[0],
    };
  }

  let detalle = '';
  if (inicial.length !== 2) {
    detalle = 'Debe ser 1 letra mayúscula seguida de punto';
  } else if (!/^[A-Z]/.test(inicial)) {
    detalle = 'Debe comenzar con letra mayúscula';
  } else if (!inicial.endsWith('.')) {
    detalle = 'Debe terminar con punto "."';
  }

  return {
    valido: false,
    mensaje: 'Inicial inválida',
    campo: 'inicial',
    detalle: detalle,
  };
}

// ============================================
// VALIDADOR INTEGRADO
// ============================================

/**
 * Valida un registro completo de contacto
 *
 * ¿Por qué? Los formularios envían múltiples campos a la vez
 * ¿Para qué? Validación completa antes de guardar en BD
 *
 * @param {object} contacto - Objeto con los datos del contacto
 * @returns {object} Resultado con todos los errores encontrados
 */
function validarContacto(contacto) {
  const resultados = {
    codigo: validarCodigoEmpleado(contacto.codigo),
    extension: validarExtension(contacto.extension),
    departamento: validarDepartamento(contacto.departamento),
    inicial: validarInicial(contacto.inicial),
  };

  const errores = Object.values(resultados).filter((r) => !r.valido);

  return {
    valido: errores.length === 0,
    errores: errores,
    resultados: resultados,
    datos: contacto,
  };
}

// ============================================
// EXTENSIONES
// ============================================

/**
 * Detecta caracteres inválidos en un código
 *
 * ¿Por qué? Ayuda al usuario a entender qué corregir
 * ¿Para qué? Mejor UX con mensajes específicos
 *
 * @param {string} codigo - El código a analizar
 * @returns {array} Lista de caracteres inválidos
 */
function detectarCaracteresInvalidos(codigo) {
  // Para código de empleado: solo A-Z y 0-9
  const invalidos = codigo.match(/[^A-Z0-9]/gi);
  return invalidos || [];
}

/**
 * Sugiere corrección para un código
 *
 * ¿Por qué? Reducir fricción para el usuario
 * ¿Para qué? Auto-corrección de errores comunes
 *
 * @param {string} codigo - El código a corregir
 * @returns {string} Código sugerido
 */
function sugerirCorreccion(codigo) {
  return codigo
    .toUpperCase() // Convertir a mayúsculas
    .replace(/[^A-Z0-9]/g, '') // Eliminar caracteres inválidos
    .substring(0, 6); // Limitar a 6 caracteres
}

/**
 * Encuentra códigos de empleado en un texto
 *
 * ¿Por qué? Extraer datos de documentos o mensajes
 * ¿Para qué? Parsing automático de información
 *
 * @param {string} texto - Texto a analizar
 * @returns {array} Lista de códigos encontrados
 */
function encontrarCodigosEnTexto(texto) {
  // Usar word boundary para encontrar códigos completos
  const patron = /\b[A-Z][A-Z]\d\d\d\d\b/g;
  return texto.match(patron) || [];
}

// ============================================
// TESTS
// ============================================

console.log('=== Tests de Validación Individual ===\n');

// Código de empleado
console.log('Código de empleado:');
console.log(validarCodigoEmpleado('AB1234')); // ✅ válido
console.log(validarCodigoEmpleado('A1234')); // ❌ solo 1 letra
console.log(validarCodigoEmpleado('ab1234')); // ❌ minúsculas

// Extensión
console.log('\nExtensión:');
console.log(validarExtension('123')); // ✅ válido (3 dígitos)
console.log(validarExtension('4567')); // ✅ válido (4 dígitos)
console.log(validarExtension('12')); // ❌ muy corta

// Departamento
console.log('\nDepartamento:');
console.log(validarDepartamento('TIC')); // ✅ válido
console.log(validarDepartamento('IT')); // ❌ muy corto
console.log(validarDepartamento('tic')); // ❌ minúsculas

// Inicial
console.log('\nInicial:');
console.log(validarInicial('J.')); // ✅ válido
console.log(validarInicial('JJ.')); // ❌ 2 letras
console.log(validarInicial('J')); // ❌ sin punto

console.log('\n=== Test de Validación Integrada ===\n');

// Contacto válido
const contactoValido = {
  codigo: 'AB1234',
  extension: '456',
  departamento: 'TIC',
  inicial: 'J.',
};
console.log('Contacto válido:');
console.log(validarContacto(contactoValido));

// Contacto con errores
const contactoInvalido = {
  codigo: 'A123',
  extension: '12',
  departamento: 'IT',
  inicial: 'JJ.',
};
console.log('\nContacto con errores:');
console.log(validarContacto(contactoInvalido));

console.log('\n=== Tests de Extensiones ===\n');

// Detectar inválidos
console.log("Caracteres inválidos en 'AB@123#':");
console.log(detectarCaracteresInvalidos('AB@123#')); // ['@', '#']

// Sugerir corrección
console.log("\nSugerencia para 'ab-1234':");
console.log(sugerirCorreccion('ab-1234')); // 'AB1234'

// Encontrar en texto
const textoEjemplo =
  'El empleado AB1234 reporta a XY5678 en el depto TIC. El código ZZ no es válido.';
console.log('\nCódigos en texto:');
console.log(encontrarCodigosEnTexto(textoEjemplo)); // ['AB1234', 'XY5678']
