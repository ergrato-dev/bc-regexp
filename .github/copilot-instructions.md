# Copilot Instructions - Bootcamp RegExp

## Descripción del Proyecto

Este es un **bootcamp de Expresiones Regulares (RegExp)** de zero to hero, diseñado para 8 semanas con dedicación de 4 horas semanales.

## Estructura del Proyecto

```
bc-regexp/
├── .github/           # Configuración de GitHub y Copilot
├── .vscode/           # Configuración del editor
├── assets/            # Recursos globales (imágenes, diagramas)
├── _docs/             # Documentación general del bootcamp
├── _scripts/          # Scripts de utilidad
├── bootcamp/
│   └── week-XX-tema_principal/     # Contenido por semana
│       ├── 0-assets/      # Recursos de la semana
│       ├── 1-teoria/      # Contenido teórico
│       ├── 2-ejercicios/  # Ejercicios prácticos
│       ├── 3-proyecto/    # Mini-proyecto semanal
│       ├── 4-resursos/    # Enlaces y recursos externos
│       └── 5-glosario/    # Términos y definiciones
└── README.md
```

## Convenciones de Código

### Archivos Markdown

- Usar español para todo el contenido
- Títulos en formato: `# Semana XX: Título del Tema`
- Incluir ejemplos de código con syntax highlighting
- Usar bloques de código con lenguaje especificado: ` ```regex `, ` ```javascript `, ` ```python `

### Ejemplos de RegExp

- Siempre incluir:
  - El patrón regex
  - Texto de prueba
  - Resultado esperado
  - Explicación paso a paso

```markdown
**Patrón:** `/\d{3}-\d{4}/`
**Texto:** `Mi número es 555-1234`
**Coincidencia:** `555-1234`
**Explicación:** Busca 3 dígitos, un guión y 4 dígitos
```

### Nomenclatura de Archivos

- Usar kebab-case: `introduccion-metacaracteres.md`
- Prefijos numéricos para orden: `01-conceptos-basicos.md`
- Ejercicios: `ejercicio-01-literales.md`
- Soluciones: `solucion-01-literales.md`

## Temario por Semanas

| Semana | Tema Principal                                                 |
| ------ | -------------------------------------------------------------- |
| 01     | Fundamentos: literales, metacaracteres básicos (`.`, `^`, `$`) |
| 02     | Clases de caracteres: `[abc]`, `[^abc]`, `\d`, `\w`, `\s`      |
| 03     | Cuantificadores: `*`, `+`, `?`, `{n,m}`, greedy vs lazy        |
| 04     | Grupos y capturas: `()`, `(?:)`, backreferences `\1`           |
| 05     | Lookahead y lookbehind: `(?=)`, `(?!)`, `(?<=)`, `(?<!)`       |
| 06     | Flags y modificadores: `g`, `i`, `m`, `s`, `u`                 |
| 07     | Patrones avanzados y optimización                              |
| 08     | Proyecto final + casos reales                                  |

## Instrucciones para Copilot

### Al crear contenido teórico:

1. Explicar conceptos de forma progresiva
2. Incluir analogías para facilitar comprensión
3. Proporcionar múltiples ejemplos por concepto
4. Agregar notas sobre errores comunes

### Al crear ejercicios:

1. Empezar con ejercicios simples y aumentar dificultad
2. Incluir casos edge
3. Proporcionar hints sin revelar la solución
4. Formato estándar:
   - Objetivo
   - Instrucciones
   - Texto de prueba
   - Resultado esperado
   - Hints (opcionales)

### Al crear proyectos:

1. Casos de uso del mundo real
2. Validación de emails, teléfonos, URLs, etc.
3. Extracción de datos de logs
4. Parsing de archivos estructurados

## Herramientas Recomendadas

- [regex101.com](https://regex101.com) - Tester online
- [regexr.com](https://regexr.com) - Visualizador
- [debuggex.com](https://debuggex.com) - Diagramas de flujo

## Idioma y Nomenclatura

- **Contenido explicativo:** en español
- **Nomenclatura técnica:** en inglés (obligatorio)
- Todos los términos técnicos deben usarse en inglés:
  - `lookahead`, `lookbehind`, `backreference`
  - `greedy`, `lazy`, `quantifier`
  - `capture group`, `non-capturing group`
  - `character class`, `metacharacter`
  - `anchor`, `boundary`, `flag`

### Glosario de Referencia

| Término en Inglés | Descripción en Español                      |
| ----------------- | ------------------------------------------- |
| `pattern`         | El patrón o expresión regular               |
| `match`           | Coincidencia encontrada                     |
| `capture group`   | Grupo de captura                            |
| `backreference`   | Retro-referencia a un grupo capturado       |
| `lookahead`       | Aserción que mira hacia adelante            |
| `lookbehind`      | Aserción que mira hacia atrás               |
| `greedy`          | Cuantificador codicioso (captura lo máximo) |
| `lazy`            | Cuantificador perezoso (captura lo mínimo)  |
| `anchor`          | Ancla de posición (`^`, `$`)                |
| `boundary`        | Límite de palabra (`\b`)                    |
| `flag`            | Modificador del patrón (`g`, `i`, `m`)      |

## Documentación de Código

### Regla Principal

**Todo código debe estar explicado con:**

1. **¿Por qué?** - La razón o problema que resuelve
2. **¿Para qué?** - El propósito o resultado esperado

### Formato de Explicación

```javascript
// ¿Por qué? El email tiene un formato específico que debemos validar
// ¿Para qué? Asegurar que el usuario ingrese un email válido antes de enviar el formulario
const emailPattern = /^[\w.-]+@[\w.-]+\.\w{2,}$/;
```

### Ejemplo Completo

```javascript
/**
 * Patrón: Validación de número telefónico
 *
 * ¿Por qué?
 * Los números de teléfono pueden venir en diferentes formatos
 * y necesitamos normalizarlos para almacenarlos consistentemente.
 *
 * ¿Para qué?
 * - Validar el formato antes de guardar en base de datos
 * - Extraer los componentes (código de área, número)
 * - Mostrar feedback al usuario si el formato es incorrecto
 */
const phonePattern = /^(\d{3})-(\d{3})-(\d{4})$/;
//                    │    │   │    │   │    │
//                    │    │   │    │   │    └─ Exactamente 4 dígitos (número local)
//                    │    │   │    │   └────── Fin del grupo 3
//                    │    │   │    └────────── Guión literal (separador)
//                    │    │   └─────────────── Exactamente 3 dígitos (prefijo)
//                    │    └─────────────────── Guión literal (separador)
//                    └──────────────────────── Exactamente 3 dígitos (código de área)
```

### Desglose de Patrones Complejos

Para patrones complejos, usar comentarios alineados:

```javascript
const urlPattern = /^(https?):\/\/([^\/]+)(\/.*)?$/;
//                  │  │     │    │      │ │    │
//                  │  │     │    │      │ │    └─ Fin del string
//                  │  │     │    │      │ └────── Grupo 3: path (opcional)
//                  │  │     │    │      └──────── Cualquier caracter excepto /
//                  │  │     │    └─────────────── Grupo 2: dominio
//                  │  │     └──────────────────── :// literal
//                  │  └────────────────────────── 's' opcional (http o https)
//                  └───────────────────────────── Grupo 1: protocolo
```

## Assets y Recursos Visuales

### Formato y Estilo

- **Formato obligatorio:** SVG (Scalable Vector Graphics)
- **Tema:** Dark mode
- **Colores:** Sólidos, sin degradados ni gradientes
- **Tipografía:** Sans-serif (Inter, Roboto, Arial, o similares)
- **Fondo:** Oscuro (#1a1a2e, #16213e, o similares)
- **Acentos:** Naranja (#FF6B35), Cyan (#00BCD4), Verde (#8BC34A)

### Directrices de Diseño

- Mantener alto contraste para legibilidad
- Usar formas geométricas simples
- Incluir el patrón regex cuando sea relevante
- Optimizar para visualización en GitHub (fondo oscuro)
