# Glosario - Semana 04: Grupos y Capturas

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### B

#### Backreference

**Descripción:** Referencia dentro del patrón a un grupo capturado previamente. Permite encontrar texto repetido.

```javascript
/**
 * ¿Por qué? Necesitamos que dos partes del texto sean idénticas
 * ¿Para qué? Validar consistencia, encontrar duplicados
 */

// Referencia numérica
/(\w+)\s+\1/gi.exec('hola hola'); // Encuentra palabra duplicada

// Referencia por nombre
/(?<palabra>\w+)\s+\k<palabra>/gi.exec('hola hola');
```

**Sintaxis:**

- `\1`, `\2`, ... - Por número de grupo
- `\k<nombre>` - Por nombre de grupo

---

### C

#### Capture Group

**Descripción:** Paréntesis que capturan y almacenan el texto coincidente para uso posterior.

```javascript
/**
 * ¿Por qué? Necesitamos extraer partes específicas del match
 * ¿Para qué? Procesar componentes individualmente
 */
const pattern = /(\d{2})\/(\d{2})\/(\d{4})/;
const match = '15/01/2024'.match(pattern);

console.log(match[0]); // "15/01/2024" - match completo
console.log(match[1]); // "15" - grupo 1
console.log(match[2]); // "01" - grupo 2
console.log(match[3]); // "2024" - grupo 3
```

---

### G

#### Group

**Descripción:** Conjunto de elementos agrupados con paréntesis. Sirve para capturar, agrupar operadores, o crear alternativas.

```javascript
// Para quantifiers
/(ab)+/ / // "ab" repetido
  // Para alternativas
  (http | https | ftp) /
  // Para captura
  /(\d+)/; // Captura dígitos
```

---

### M

#### matchAll

**Descripción:** Método de String que retorna un iterador con todos los matches incluyendo grupos.

```javascript
/**
 * ¿Por qué? match() con flag g pierde los grupos
 * ¿Para qué? Obtener todos los matches CON sus grupos
 */
const texto = 'a@b.com, c@d.org';
const pattern = /(\w+)@(\w+)\.(\w+)/g;

for (const match of texto.matchAll(pattern)) {
  console.log(`${match[1]}@${match[2]}.${match[3]}`);
}
```

---

### N

#### Named Capture Group

**Descripción:** Grupo de captura con nombre en lugar de solo número.

```javascript
/**
 * ¿Por qué? Los índices numéricos son difíciles de mantener
 * ¿Para qué? Código más legible y refactorizable
 */
const pattern = /(?<dia>\d{2})\/(?<mes>\d{2})\/(?<anio>\d{4})/;
const match = '15/01/2024'.match(pattern);

// Acceso por nombre
const { dia, mes, anio } = match.groups;
console.log(`Año: ${anio}, Mes: ${mes}, Día: ${dia}`);
```

**Sintaxis:** `(?<nombre>...)`

---

#### Non-Capturing Group

**Descripción:** Grupo que agrupa elementos sin capturar el contenido.

```javascript
/**
 * ¿Por qué? A veces solo necesitas agrupar, no capturar
 * ¿Para qué? Simplificar la salida, reducir memoria
 */

// Con captura (innecesaria)
const pattern1 = /(https?):\/\/(\w+)/;
'https://google'.match(pattern1);
// ['https://google', 'https', 'google']

// Sin captura del protocolo
const pattern2 = /(?:https?):\/\/(\w+)/;
'https://google'.match(pattern2);
// ['https://google', 'google']
```

**Sintaxis:** `(?:...)`

---

## Tabla Comparativa de Grupos

| Tipo          | Sintaxis    | Captura | Acceso           | Uso Principal        |
| ------------- | ----------- | ------- | ---------------- | -------------------- |
| Capture Group | `(...)`     | Sí      | `match[1]`       | Extraer partes       |
| Non-Capturing | `(?:...)`   | No      | N/A              | Agrupar sin capturar |
| Named Group   | `(?<n>...)` | Sí      | `match.groups.n` | Código legible       |

---

## Backreferences en Diferentes Contextos

### En el Patrón

```javascript
// Por número
/(\w+)\s+\1/        // Palabra duplicada

// Por nombre
/(?<x>\w+)\s+\k<x>/ // Mismo resultado, más legible
```

### En Replace

```javascript
// Por número
'Pérez, Juan'.replace(/(.+),\s*(.+)/, '$2 $1');
// "Juan Pérez"

// Por nombre
'Pérez, Juan'.replace(
  /(?<apellido>.+),\s*(?<nombre>.+)/,
  '$<nombre> $<apellido>'
);
// "Juan Pérez"

// Con función
'20C'.replace(/(\d+)C/, (_, grados) => {
  return `${(grados * 9) / 5 + 32}F`;
});
// "68F"
```

---

## Métodos de JavaScript y Grupos

### match() sin flag g

```javascript
const match = 'abc'.match(/(a)(b)(c)/);
// [
//   'abc',     // match[0]: completo
//   'a',       // match[1]: grupo 1
//   'b',       // match[2]: grupo 2
//   'c',       // match[3]: grupo 3
//   index: 0,
//   input: 'abc',
//   groups: undefined
// ]
```

### match() con flag g (pierde grupos)

```javascript
const matches = 'a1 b2 c3'.match(/(\w)(\d)/g);
// ['a1', 'b2', 'c3'] - Sin grupos
```

### matchAll() (mantiene grupos)

```javascript
const matches = 'a1 b2 c3'.matchAll(/(\w)(\d)/g);
for (const m of matches) {
  console.log(m[1], m[2]); // a 1, b 2, c 3
}
```

### exec() (con estado)

```javascript
const pattern = /(\w)(\d)/g;
const texto = 'a1 b2';

let match;
while ((match = pattern.exec(texto)) !== null) {
  console.log(match[1], match[2], match.index);
}
// a 1 0
// b 2 3
```

---

## Grupos Anidados

Los grupos se numeran por el paréntesis de **apertura**:

```javascript
/((a)(b(c)))/;
//123  4

const match = 'abc'.match(/((a)(b(c)))/);
// match[0]: "abc" - completo
// match[1]: "abc" - grupo 1 (más externo)
// match[2]: "a"   - grupo 2
// match[3]: "bc"  - grupo 3
// match[4]: "c"   - grupo 4 (más interno)
```

---

## Patrones Útiles

### Extraer Componentes de URL

```javascript
const urlPattern =
  /^(?<protocolo>https?):\/\/(?:(?<subdominio>[\w-]+)\.)?(?<dominio>[\w-]+)\.(?<tld>\w+)(?::(?<puerto>\d+))?(?<path>\/[^?]*)?(?:\?(?<query>[^#]*))?(?:#(?<fragment>.*))?$/;
```

### Validar HTML Tags

```javascript
const htmlPattern = /<(?<tag>\w+)(?:\s+[^>]*)?>(?<contenido>.*?)<\/\k<tag>>/gs;
```

### Reformatear Fecha

```javascript
const fecha = '15/01/2024';
const resultado = fecha.replace(
  /(?<d>\d{2})\/(?<m>\d{2})\/(?<y>\d{4})/,
  '$<y>-$<m>-$<d>'
);
// "2024-01-15"
```

---

**Próxima semana:** Lookahead y Lookbehind (`(?=)`, `(?!)`, `(?<=)`, `(?<!)`)
