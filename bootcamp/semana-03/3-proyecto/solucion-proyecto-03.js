/**
 * ============================================
 * Solución: Proyecto Semana 03
 * Extractor de Datos de Texto
 * ============================================
 */

// ============================================
// DOCUMENTO DE PRUEBA
// ============================================

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

// ============================================
// PATRONES DE EXTRACCIÓN
// ============================================

/**
 * Patrón: Precios
 * Formato: $XXX.XX o $XXX (decimales opcionales)
 *
 * ¿Por qué? Los precios pueden o no incluir centavos
 * ¿Para qué? Extraer valores monetarios para cálculos
 *
 * Desglose:
 * \$       → Símbolo de dólar literal
 * \d+      → Uno o más dígitos (parte entera)
 * (\.\d{2})? → Opcional: punto + exactamente 2 dígitos (centavos)
 */
const precioPattern = /\$\d+(\.\d{2})?/g;

/**
 * Patrón: Fechas
 * Formato: DD/MM/YYYY
 *
 * ¿Por qué? Formato europeo estándar en documentos
 * ¿Para qué? Identificar y parsear fechas
 *
 * Desglose:
 * \d{2}  → Día (2 dígitos)
 * \/     → Barra literal
 * \d{2}  → Mes (2 dígitos)
 * \/     → Barra literal
 * \d{4}  → Año (4 dígitos)
 */
const fechaPattern = /\d{2}\/\d{2}\/\d{4}/g;

/**
 * Patrón: Emails
 * Formato: usuario@dominio.extension
 *
 * ¿Por qué? Los emails tienen estructura predecible
 * ¿Para qué? Extraer direcciones de contacto
 *
 * Desglose:
 * [\w.-]+   → Usuario: letras, números, guión bajo, punto, guión
 * @         → Arroba literal
 * [\w.-]+   → Dominio: mismos caracteres
 * \.        → Punto literal
 * \w{2,}    → Extensión: 2 o más letras
 */
const emailPattern = /[\w.-]+@[\w.-]+\.\w{2,}/g;

/**
 * Patrón: Teléfonos españoles
 * Formato: 9 dígitos con espacios/guiones opcionales
 *
 * ¿Por qué? Los teléfonos vienen en varios formatos visuales
 * ¿Para qué? Normalizar y extraer números de contacto
 *
 * Desglose:
 * [6-9]     → Primer dígito (móvil 6-7, fijo 9, servicios 8)
 * \d        → Segundo dígito
 * [\d\s-]{7,9} → 7-9 caracteres más (dígitos, espacios o guiones)
 */
const telefonoPattern = /[6-9]\d[\d\s-]{7,9}/g;

/**
 * Patrón: Referencias de pago
 * Formato: REF-XXXXX (5 o más dígitos)
 *
 * ¿Por qué? Las referencias identifican transacciones
 * ¿Para qué? Tracking y reconciliación de pagos
 *
 * Desglose:
 * REF-   → Prefijo literal
 * \d{5,} → 5 o más dígitos
 */
const referenciaPattern = /REF-\d{5,}/g;

/**
 * Patrón: Número de factura
 * Formato: #YYYY-XXXX
 *
 * ¿Por qué? Las facturas tienen numeración secuencial
 * ¿Para qué? Identificar documentos
 */
const facturaPattern = /#\d{4}-\d{4}/g;

// ============================================
// FUNCIONES DE EXTRACCIÓN
// ============================================

/**
 * Extrae todos los datos de un documento
 *
 * ¿Por qué? Centralizar toda la lógica de extracción
 * ¿Para qué? Procesar documentos de forma consistente
 *
 * @param {string} texto - El documento a procesar
 * @returns {object} Objeto con todos los datos extraídos
 */
function extraerDatos(texto) {
  return {
    facturas: texto.match(facturaPattern) || [],
    precios: texto.match(precioPattern) || [],
    fechas: texto.match(fechaPattern) || [],
    emails: texto.match(emailPattern) || [],
    telefonos: texto.match(telefonoPattern) || [],
    referencias: texto.match(referenciaPattern) || [],
  };
}

// ============================================
// FUNCIONES DE UTILIDAD
// ============================================

/**
 * Convierte string de precio a número
 *
 * ¿Por qué? Los precios vienen como "$99.99"
 * ¿Para qué? Hacer cálculos matemáticos
 *
 * @param {string} precioStr - Precio como string
 * @returns {number} Precio como número
 */
function precioANumero(precioStr) {
  return parseFloat(precioStr.replace('$', ''));
}

/**
 * Suma todos los precios extraídos
 *
 * ¿Por qué? Calcular totales es operación común
 * ¿Para qué? Verificar sumas, generar reportes
 *
 * @param {string[]} precios - Array de strings de precios
 * @returns {number} Suma total
 */
function sumarPrecios(precios) {
  return precios.reduce((total, precio) => total + precioANumero(precio), 0);
}

/**
 * Normaliza teléfonos eliminando espacios y guiones
 *
 * ¿Por qué? Los teléfonos vienen en formatos variados
 * ¿Para qué? Almacenar en formato uniforme
 *
 * @param {string[]} telefonos - Array de teléfonos
 * @returns {string[]} Teléfonos normalizados (solo dígitos)
 */
function normalizarTelefonos(telefonos) {
  return telefonos.map((tel) => tel.replace(/[\s-]/g, ''));
}

/**
 * Parsea fecha en formato DD/MM/YYYY a objeto Date
 *
 * ¿Por qué? Las fechas como string no son útiles para cálculos
 * ¿Para qué? Ordenar, comparar, formatear fechas
 *
 * @param {string} fechaStr - Fecha en formato DD/MM/YYYY
 * @returns {Date} Objeto Date
 */
function parsearFecha(fechaStr) {
  const [dia, mes, anio] = fechaStr.split('/').map(Number);
  return new Date(anio, mes - 1, dia);
}

/**
 * Valida que un email tenga formato correcto
 *
 * ¿Por qué? La extracción puede capturar falsos positivos
 * ¿Para qué? Validar antes de usar/almacenar
 *
 * @param {string} email - Email a validar
 * @returns {boolean} Si es válido
 */
function validarEmail(email) {
  // Patrón más estricto
  const emailEstricto = /^[\w.-]+@[\w-]+\.[\w]{2,}(\.[\w]{2,})?$/;
  return emailEstricto.test(email);
}

/**
 * Valida que una fecha tenga valores lógicos
 *
 * ¿Por qué? El patrón acepta fechas inválidas como 99/99/9999
 * ¿Para qué? Asegurar integridad de datos
 *
 * @param {string} fechaStr - Fecha a validar
 * @returns {boolean} Si es válida
 */
function validarFecha(fechaStr) {
  const [dia, mes, anio] = fechaStr.split('/').map(Number);

  if (mes < 1 || mes > 12) return false;
  if (dia < 1 || dia > 31) return false;
  if (anio < 1900 || anio > 2100) return false;

  // Validación más precisa con Date
  const fecha = new Date(anio, mes - 1, dia);
  return (
    fecha.getDate() === dia &&
    fecha.getMonth() === mes - 1 &&
    fecha.getFullYear() === anio
  );
}

// ============================================
// GENERADOR DE REPORTE
// ============================================

/**
 * Genera un reporte legible de los datos extraídos
 *
 * ¿Por qué? Los datos crudos no son amigables
 * ¿Para qué? Presentar información al usuario
 *
 * @param {object} datos - Datos extraídos
 * @returns {string} Reporte formateado
 */
function generarReporte(datos) {
  const totalPrecios = sumarPrecios(datos.precios);
  const telefonosNorm = normalizarTelefonos(datos.telefonos);

  return `
╔══════════════════════════════════════════════════════════════╗
║              REPORTE DE EXTRACCIÓN DE DATOS                 ║
╠══════════════════════════════════════════════════════════════╣
║ FACTURAS: ${datos.facturas.join(', ') || 'Ninguna'}
║ FECHAS: ${datos.fechas.join(', ') || 'Ninguna'}
╠══════════════════════════════════════════════════════════════╣
║ PRECIOS ENCONTRADOS: ${datos.precios.length}
║   ${datos.precios.join('  ')}
║ TOTAL: $${totalPrecios.toFixed(2)}
╠══════════════════════════════════════════════════════════════╣
║ CONTACTOS:
║   Emails: ${datos.emails.join(', ') || 'Ninguno'}
║   Teléfonos: ${telefonosNorm.join(', ') || 'Ninguno'}
╠══════════════════════════════════════════════════════════════╣
║ REFERENCIAS: ${datos.referencias.join(', ') || 'Ninguna'}
╚══════════════════════════════════════════════════════════════╝
  `.trim();
}

// ============================================
// EJECUCIÓN Y TESTS
// ============================================

console.log('=== Extracción de Datos ===\n');

const datos = extraerDatos(documento);

console.log('Datos extraídos:');
console.log(JSON.stringify(datos, null, 2));

console.log('\n=== Reporte ===\n');
console.log(generarReporte(datos));

console.log('\n=== Validaciones ===\n');

// Validar emails
console.log('Validación de emails:');
datos.emails.forEach((email) => {
  const valido = validarEmail(email);
  console.log(`  ${email}: ${valido ? '✅' : '❌'}`);
});

// Validar fechas
console.log('\nValidación de fechas:');
datos.fechas.forEach((fecha) => {
  const valido = validarFecha(fecha);
  console.log(`  ${fecha}: ${valido ? '✅' : '❌'}`);
});

// Cálculos
console.log('\n=== Cálculos ===\n');
console.log(`Número de precios: ${datos.precios.length}`);
console.log(`Suma total: $${sumarPrecios(datos.precios).toFixed(2)}`);
console.log(`Teléfonos normalizados: ${normalizarTelefonos(datos.telefonos)}`);

// ============================================
// CASOS EDGE
// ============================================

console.log('\n=== Tests de Casos Edge ===\n');

const casosEdge = [
  // Sin decimales
  { texto: 'Precio: $100', esperado: ['$100'] },
  // Con decimales
  { texto: 'Total: $99.99', esperado: ['$99.99'] },
  // Múltiples en línea
  { texto: '$10 + $20 = $30', esperado: ['$10', '$20', '$30'] },
  // Fecha inválida (el patrón la captura, la validación la rechaza)
  { texto: 'Fecha: 99/99/9999', esperado: ['99/99/9999'] },
  // Email con subdominio
  { texto: 'mail@sub.dominio.com', esperado: ['mail@sub.dominio.com'] },
];

casosEdge.forEach(({ texto, esperado }) => {
  const precios = texto.match(precioPattern) || [];
  const fechas = texto.match(fechaPattern) || [];
  const emails = texto.match(emailPattern) || [];
  const resultado = [...precios, ...fechas, ...emails];
  const ok = JSON.stringify(resultado) === JSON.stringify(esperado);
  console.log(`${ok ? '✅' : '❌'} "${texto}" → ${JSON.stringify(resultado)}`);
});
