# Glosario - Semana 07: Patrones Avanzados y Optimización

## Términos Técnicos

> **Nota:** La nomenclatura técnica se mantiene en inglés según las convenciones del bootcamp.

---

### A

#### Atomic Group

**Descripción:** Grupo que no permite backtracking una vez que ha hecho match. JavaScript no lo soporta nativamente.

```javascript
/**
 * ¿Por qué? Prevenir backtracking costoso
 * ¿Para qué? Mejorar rendimiento en patrones complejos
 */

// En otros lenguajes: (?>patrón)
// En JavaScript: Simulación con lookahead + backreference
const atomicSim = /(?=(\d+))\1X/;
//                 │   │    │
//                 │   │    └─ Referencia al grupo
//                 │   └────── Captura
//                 └────────── Lookahead "bloquea"
```

---

### B

#### Backtracking

**Descripción:** Mecanismo del motor regex que retrocede e intenta alternativas cuando un match falla.

```javascript
/**
 * ¿Por qué? Permite encontrar matches en patrones complejos
 * ¿Para qué? Flexibilidad del motor regex
 */

// Ejemplo: /a.*b/ en "aXXXb"
// 1. .* consume todo: "aXXXb"
// 2. Falla en 'b' (ya no hay caracteres)
// 3. Backtrack: .* devuelve 'b' → "aXXX" + "b"
// 4. Ahora 'b' coincide → Match!
```

---

#### Backtracking Catastrophic

**Descripción:** Situación donde el backtracking crece exponencialmente, causando tiempo de ejecución extremo.

```javascript
/**
 * ¿Por qué? Patrones mal diseñados pueden causar DoS
 * ¿Para qué? Evitar vulnerabilidades de seguridad
 */

// ❌ Patrón peligroso
/(a+)+$/.test('aaaaaaaaaaaaaaaaaX');
// Prueba millones de combinaciones

// ✅ Alternativa segura
/a+$/.test('aaaaaaaaaaaaaaaaaX');
// Tiempo lineal
```

---

### N

#### Named Capture Group

**Descripción:** Grupo de captura con nombre en lugar de solo número.

```javascript
/**
 * ¿Por qué? Los números de grupo son difíciles de recordar
 * ¿Para qué? Código más legible y mantenible
 */

// Sintaxis: (?<nombre>patrón)
const pattern = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;

const match = '2024-03-15'.match(pattern);

// Acceso por nombre
match.groups.year; // "2024"
match.groups.month; // "03"
match.groups.day; // "15"

// Backreference con nombre
/(?<word>\w+)\s+\k<word>/; // Detecta palabras duplicadas
```

**Nota:** Disponible desde ES2018.

---

### P

#### Possessive Quantifier

**Descripción:** Cuantificador que no permite backtracking. JavaScript no lo soporta nativamente.

```javascript
/**
 * En otros lenguajes:
 * *+ (possessive star)
 * ++ (possessive plus)
 * ?+ (possessive optional)
 *
 * En JavaScript: Simular con atomic groups
 */

// Perl/PCRE: /a++b/
// JavaScript: /(?=(a+))\1b/
```

---

### R

#### ReDoS

**Descripción:** Regular Expression Denial of Service. Ataque que explota catastrophic backtracking.

```javascript
/**
 * ¿Por qué? Atacantes envían inputs maliciosos
 * ¿Para qué? Proteger aplicaciones web
 */

// Patrón vulnerable
const emailBad = /^(\w+\.)*\w+@(\w+\.)*\w+\.\w+$/;

// Input malicioso
const malicious = 'a'.repeat(50) + '@';
// Puede colgar el navegador/servidor

// Protección: Limitar longitud de input
// Protección: Timeout en regex
// Protección: Usar patrones seguros
```

---

### T

#### Tokenizer / Lexer

**Descripción:** Programa que divide texto en tokens (unidades mínimas con significado).

```javascript
/**
 * ¿Por qué? Primer paso en compilación/interpretación
 * ¿Para qué? Convertir texto en estructura procesable
 */

const tokenize = (code) => {
  const patterns = [
    { type: 'NUMBER', regex: /\d+/ },
    { type: 'IDENT', regex: /[a-z]+/i },
    { type: 'OP', regex: /[+\-*/]/ },
  ];
  // ...
};

tokenize('x + 42');
// [
//   { type: 'IDENT', value: 'x' },
//   { type: 'OP', value: '+' },
//   { type: 'NUMBER', value: '42' }
// ]
```

---

## Tabla de Compatibilidad

| Feature              | ES Version | Chrome | Firefox | Safari |
| -------------------- | ---------- | ------ | ------- | ------ |
| Named Groups         | ES2018     | 64+    | 78+     | 11.1+  |
| Named Backreference  | ES2018     | 64+    | 78+     | 11.1+  |
| `\k<name>`           | ES2018     | 64+    | 78+     | 11.1+  |
| `$<name>` in replace | ES2018     | 64+    | 78+     | 11.1+  |

---

## Técnicas de Optimización

### Tabla de Referencia

| Técnica       | Antes      | Después     | Mejora                 |
| ------------- | ---------- | ----------- | ---------------------- |
| Negación      | `.*X`      | `[^X]*X`    | Menos backtracking     |
| Límites       | `\w+`      | `\w{1,50}`  | Previene inputs largos |
| Anclas        | `pattern`  | `^pattern$` | Falla rápido           |
| Non-capturing | `(abc)+`   | `(?:abc)+`  | Menos memoria          |
| Específico    | `(a\|ab)+` | `a+b?`      | Menos alternativas     |

---

## Patrones de Seguridad

### Checklist

```
┌────────────────────────────────────────────────────────────────┐
│                     CHECKLIST DE SEGURIDAD                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ ¿Hay cuantificadores anidados? (a+)+                        │
│  □ ¿Hay alternativas que se solapan? (a|ab)                    │
│  □ ¿Hay .* o .+ sin límites?                                   │
│  □ ¿Falta validación de longitud del input?                    │
│  □ ¿Se usa timeout para regex complejos?                       │
│  □ ¿Los patrones tienen anclas cuando es posible?              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Terminología del Motor Regex

| Término    | Descripción                                                                     |
| ---------- | ------------------------------------------------------------------------------- |
| NFA        | Non-deterministic Finite Automaton - cómo funcionan la mayoría de motores regex |
| DFA        | Deterministic Finite Automaton - más rápido pero menos features                 |
| Greedy     | Consume lo máximo posible primero                                               |
| Lazy       | Consume lo mínimo posible primero                                               |
| Possessive | Como greedy pero sin backtracking                                               |
| Atomic     | Grupo que no permite backtracking                                               |

---

**Próxima semana:** Proyecto Final + Casos Reales
