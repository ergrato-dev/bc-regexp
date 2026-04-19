/**
 * ============================================
 * Solución: Proyecto Semana 05
 * Validador de Formularios Avanzado
 * ============================================
 */

// ============================================
// REGLAS DE VALIDACIÓN
// ============================================

const REGLAS = {
  password: {
    minLength: 8,
    maxLength: 128,
    requireUppercase: true,
    requireLowercase: true,
    requireDigit: true,
    requireSpecial: true,
    noSpaces: true,
    noConsecutiveRepeats: 3,
  },
  username: {
    minLength: 3,
    maxLength: 20,
    mustStartWithLetter: true,
    noConsecutiveUnderscores: true,
  },
};

const PALABRAS_PROHIBIDAS = [
  'admin',
  'root',
  'system',
  'null',
  'undefined',
  'test',
  'user',
];

// ============================================
// VALIDADOR DE PASSWORD
// ============================================

/**
 * Patrón de password con todos los requisitos
 *
 * ¿Por qué? Múltiples reglas deben cumplirse simultáneamente
 * ¿Para qué? Seguridad de cuentas de usuario
 *
 * Desglose:
 * (?=.*[A-Z])       → Lookahead: al menos una mayúscula
 * (?=.*[a-z])       → Lookahead: al menos una minúscula
 * (?=.*\d)          → Lookahead: al menos un dígito
 * (?=.*[!@#$%^&*]) → Lookahead: al menos un carácter especial
 * (?!.*\s)          → Negative lookahead: sin espacios
 * (?!.*(.)\1{2})    → Negative lookahead: sin 3 caracteres consecutivos iguales
 * .{8,128}          → 8 a 128 caracteres
 */
const passwordPattern =
  /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=])(?!.*\s)(?!.*(.)\1{2}).{8,128}$/;

/**
 * Valida una contraseña y retorna resultado detallado
 *
 * @param {string} password - La contraseña a validar
 * @returns {object} Resultado con validez, errores y fortaleza
 */
function validarPassword(password) {
  const resultado = {
    valido: false,
    errores: [],
    fortaleza: 0,
  };

  // Validaciones individuales para mensajes específicos
  if (password.length < REGLAS.password.minLength) {
    resultado.errores.push(
      `Debe tener al menos ${REGLAS.password.minLength} caracteres`
    );
  }

  if (password.length > REGLAS.password.maxLength) {
    resultado.errores.push(
      `No debe superar ${REGLAS.password.maxLength} caracteres`
    );
  }

  if (!/[A-Z]/.test(password)) {
    resultado.errores.push('Debe contener al menos una mayúscula');
  }

  if (!/[a-z]/.test(password)) {
    resultado.errores.push('Debe contener al menos una minúscula');
  }

  if (!/\d/.test(password)) {
    resultado.errores.push('Debe contener al menos un dígito');
  }

  if (!/[!@#$%^&*()_+\-=]/.test(password)) {
    resultado.errores.push(
      'Debe contener al menos un carácter especial (!@#$%^&*()_+-=)'
    );
  }

  if (/\s/.test(password)) {
    resultado.errores.push('No debe contener espacios');
  }

  // Caracteres consecutivos repetidos
  if (/(.)\1{2}/.test(password)) {
    resultado.errores.push(
      'No debe tener 3 o más caracteres consecutivos iguales'
    );
  }

  // Patrón común (123, abc, qwerty)
  if (/(?:123|abc|qwerty|password)/i.test(password)) {
    resultado.errores.push('No debe contener patrones comunes');
  }

  resultado.valido = resultado.errores.length === 0;
  resultado.fortaleza = calcularFortaleza(password);

  return resultado;
}

/**
 * Calcula la fortaleza de una contraseña (0-100)
 *
 * @param {string} password - La contraseña
 * @returns {number} Fortaleza de 0 a 100
 */
function calcularFortaleza(password) {
  let fortaleza = 0;

  // Longitud base
  fortaleza += Math.min(password.length * 4, 40);

  // Variedad de caracteres
  if (/[a-z]/.test(password)) fortaleza += 10;
  if (/[A-Z]/.test(password)) fortaleza += 10;
  if (/\d/.test(password)) fortaleza += 10;
  if (/[!@#$%^&*()_+\-=]/.test(password)) fortaleza += 15;

  // Penalizaciones
  if (/(.)\1{2}/.test(password)) fortaleza -= 10;
  if (/^[a-zA-Z]+$/.test(password)) fortaleza -= 10;
  if (/^\d+$/.test(password)) fortaleza -= 20;

  return Math.max(0, Math.min(100, fortaleza));
}

// ============================================
// VALIDADOR DE USERNAME
// ============================================

/**
 * Patrón de username
 *
 * ¿Por qué? Los usernames tienen reglas específicas de formato
 * ¿Para qué? Consistencia y seguridad en identificadores
 *
 * Desglose:
 * ^              → Inicio
 * (?!.*__)       → Negative lookahead: sin __ consecutivos
 * [a-zA-Z]       → Primer carácter debe ser letra
 * \w{2,19}       → 2-19 caracteres más (word chars)
 * $              → Fin
 */
const usernamePattern = /^(?!.*__)[a-zA-Z]\w{2,19}$/;

/**
 * Valida un nombre de usuario
 *
 * @param {string} username - El username a validar
 * @returns {object} Resultado con validez, errores y sugerencias
 */
function validarUsername(username) {
  const resultado = {
    valido: false,
    errores: [],
    sugerencias: [],
  };

  // Longitud
  if (username.length < REGLAS.username.minLength) {
    resultado.errores.push(
      `Debe tener al menos ${REGLAS.username.minLength} caracteres`
    );
  }

  if (username.length > REGLAS.username.maxLength) {
    resultado.errores.push(
      `No debe superar ${REGLAS.username.maxLength} caracteres`
    );
  }

  // Caracteres permitidos
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    resultado.errores.push('Solo se permiten letras, números y guión bajo');
  }

  // Empezar con letra
  if (!/^[a-zA-Z]/.test(username)) {
    resultado.errores.push('Debe empezar con una letra');
  }

  // Guiones bajos consecutivos
  if (/__/.test(username)) {
    resultado.errores.push('No debe tener guiones bajos consecutivos');
  }

  // Palabras prohibidas
  const palabraProhibida = PALABRAS_PROHIBIDAS.find((palabra) =>
    username.toLowerCase().includes(palabra)
  );
  if (palabraProhibida) {
    resultado.errores.push(`No puede contener "${palabraProhibida}"`);
  }

  resultado.valido = resultado.errores.length === 0;

  // Generar sugerencias si no es válido
  if (!resultado.valido) {
    resultado.sugerencias = generarSugerencias(username);
  }

  return resultado;
}

/**
 * Genera sugerencias de usernames alternativos
 *
 * @param {string} base - Username base
 * @returns {string[]} Array de sugerencias
 */
function generarSugerencias(base) {
  const sugerencias = [];

  // Limpiar el base
  let limpio = base
    .replace(/[^a-zA-Z0-9_]/g, '')
    .replace(/__+/g, '_')
    .replace(/^[^a-zA-Z]+/, '');

  // Si está vacío, usar genérico
  if (!limpio || limpio.length < 3) {
    limpio = 'user';
  }

  // Generar variantes
  const random = () => Math.floor(Math.random() * 1000);

  sugerencias.push(`${limpio}${random()}`);
  sugerencias.push(`${limpio}_${random()}`);
  sugerencias.push(`the_${limpio}`);
  sugerencias.push(`${limpio.charAt(0)}${limpio.slice(1)}${random()}`);
  sugerencias.push(`real_${limpio}`);

  return sugerencias.slice(0, 5);
}

// ============================================
// VALIDADOR DE TARJETA DE CRÉDITO
// ============================================

/**
 * Patrones de tarjetas
 *
 * ¿Por qué? Cada emisor tiene un formato específico
 * ¿Para qué? Detectar tipo de tarjeta y validar formato
 */
const TARJETAS = {
  visa: {
    pattern: /^4\d{15}$/,
    nombre: 'Visa',
    longitud: 16,
  },
  mastercard: {
    pattern:
      /^(?:5[1-5]\d{14}|2(?:2[2-9]\d{12}|[3-6]\d{13}|7[01]\d{12}|720\d{12}))$/,
    nombre: 'MasterCard',
    longitud: 16,
  },
  amex: {
    pattern: /^3[47]\d{13}$/,
    nombre: 'American Express',
    longitud: 15,
  },
};

/**
 * Valida un número de tarjeta de crédito
 *
 * @param {string} numero - Número de tarjeta (con o sin espacios)
 * @returns {object} Resultado con validez, tipo y errores
 */
function validarTarjeta(numero) {
  const resultado = {
    valido: false,
    tipo: null,
    formateado: null,
    errores: [],
  };

  // Limpiar: solo dígitos
  const limpio = numero.replace(/\D/g, '');

  if (!limpio) {
    resultado.errores.push('El número de tarjeta está vacío');
    return resultado;
  }

  // Detectar tipo
  for (const [tipo, config] of Object.entries(TARJETAS)) {
    if (config.pattern.test(limpio)) {
      resultado.tipo = config.nombre;
      break;
    }
  }

  if (!resultado.tipo) {
    resultado.errores.push('Número de tarjeta no reconocido');
    return resultado;
  }

  // Validar Luhn
  if (!verificarLuhn(limpio)) {
    resultado.errores.push('Número de tarjeta inválido (Luhn)');
    return resultado;
  }

  resultado.valido = true;
  resultado.formateado = formatearTarjeta(limpio, resultado.tipo);

  return resultado;
}

/**
 * Verifica el dígito de control usando algoritmo de Luhn
 *
 * ¿Por qué? Es el estándar de la industria para validar tarjetas
 * ¿Para qué? Detectar errores de tipeo
 *
 * @param {string} numero - Solo dígitos
 * @returns {boolean} Si pasa la validación
 */
function verificarLuhn(numero) {
  const digits = numero.split('').reverse().map(Number);

  const sum = digits.reduce((acc, digit, i) => {
    if (i % 2 === 1) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    return acc + digit;
  }, 0);

  return sum % 10 === 0;
}

/**
 * Formatea el número de tarjeta según su tipo
 *
 * @param {string} numero - Solo dígitos
 * @param {string} tipo - Tipo de tarjeta
 * @returns {string} Número formateado
 */
function formatearTarjeta(numero, tipo) {
  if (tipo === 'American Express') {
    // Formato: 3411 111111 11111
    return numero.replace(/(\d{4})(\d{6})(\d{5})/, '$1 $2 $3');
  }
  // Formato estándar: 4111 1111 1111 1111
  return numero.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/, '$1 $2 $3 $4');
}

// ============================================
// EXTRACTOR DE INFORMACIÓN CONTEXTUAL
// ============================================

/**
 * Extrae información usando lookarounds
 *
 * @param {string} texto - Texto a analizar
 * @returns {object} Información extraída
 */
function extraerInformacion(texto) {
  return {
    // Precios en euros (solo el número)
    precios: (texto.match(/\d+(?:[.,]\d{2})?(?=\s*€)/g) || []).map((p) =>
      parseFloat(p.replace(',', '.'))
    ),

    // Fechas en formato europeo DD/MM/YYYY
    fechas: texto.match(/\b\d{2}\/\d{2}\/\d{4}\b/g) || [],

    // Menciones de usuarios @username
    menciones: (texto.match(/(?<=@)\w+/g) || []).map((m) => m.toLowerCase()),

    // Hashtags #tema
    hashtags: (texto.match(/(?<=#)\w+/g) || []).map((h) => h.toLowerCase()),

    // Emails
    emails: texto.match(/[\w.-]+@[\w.-]+\.\w{2,}/g) || [],

    // URLs
    urls: texto.match(/https?:\/\/[^\s<>"{}|\\^`[\]]+/g) || [],
  };
}

// ============================================
// EJECUCIÓN Y TESTS
// ============================================

console.log('=== Test de Password ===\n');

const passwords = [
  'Abc12345!',
  'abc12345!',
  'ABC12345!',
  'Abcdefgh!',
  'Abc123!',
  'Abc12 345!',
  'Abc111111!',
  'Abcqwerty!',
];

passwords.forEach((pwd) => {
  const result = validarPassword(pwd);
  console.log(
    `${pwd.padEnd(15)} → ${result.valido ? '✅' : '❌'} Fortaleza: ${
      result.fortaleza
    }%`
  );
  if (result.errores.length) {
    console.log(`   Errores: ${result.errores.join(', ')}`);
  }
});

console.log('\n=== Test de Username ===\n');

const usernames = [
  'johnDoe',
  'john_doe',
  '123john',
  'john__doe',
  'jo',
  'admin_user',
  'valid_user_123',
];

usernames.forEach((user) => {
  const result = validarUsername(user);
  console.log(`${user.padEnd(15)} → ${result.valido ? '✅' : '❌'}`);
  if (result.errores.length) {
    console.log(`   Errores: ${result.errores.join(', ')}`);
  }
  if (result.sugerencias.length) {
    console.log(`   Sugerencias: ${result.sugerencias.join(', ')}`);
  }
});

console.log('\n=== Test de Tarjetas ===\n');

const tarjetas = [
  '4111111111111111',
  '4111 1111 1111 1111',
  '5500000000000004',
  '371449635398431',
  '1234567890123456',
  '4111111111111112',
];

tarjetas.forEach((card) => {
  const result = validarTarjeta(card);
  console.log(
    `${card.padEnd(20)} → ${result.valido ? '✅' : '❌'} ${result.tipo || ''}`
  );
  if (result.formateado) {
    console.log(`   Formateado: ${result.formateado}`);
  }
  if (result.errores.length) {
    console.log(`   Errores: ${result.errores.join(', ')}`);
  }
});

console.log('\n=== Test de Extracción ===\n');

const textoEjemplo = `
Hola @juan y @maria! 
El precio es 99,99€ más 21€ de IVA.
Evento el 15/03/2024 y 20/04/2024.
Contacto: info@ejemplo.com
Más info en https://ejemplo.com/info
Usa #oferta #descuento
`;

console.log(extraerInformacion(textoEjemplo));
