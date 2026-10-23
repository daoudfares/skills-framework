---
name: dataweave-developer
description: Write, review, debug and refactor DataWeave 2.0 scripts for MuleSoft integrations. Use when working with .dwl files, Mule transform components, mapping between JSON, XML, CSV, flat file, Excel or Java payloads, when a DataWeave script raises a type or selector error, or when asked about DataWeave functions, selectors, operators, formats or reader/writer properties.
---

# DataWeave Developer

DataWeave 2.0 is MuleSoft's transformation language. This skill covers writing
scripts, choosing the right function, reading the format reader/writer
properties, and diagnosing the errors the runtime actually produces.

## Script anatomy

Every script is a header, a `---` separator, and a body expression.

```dataweave
%dw 2.0
import * from dw::core::Strings
var taxRate = 0.21
fun gross(net: Number) = net * (1 + taxRate)
output application/json
---
payload.items map (item) -> {
  sku:   item.code,
  gross: gross(item.net)
}
```

The header holds the version directive, `output` (and optional `input`),
`import`, `var`, `fun`, `type` and `ns` declarations. The body is a **single
expression** — there are no statements and no mutation. Build results by
composing expressions.

## Finding the right function

Read only the reference you need; they are large.

| Need | Read |
|---|---|
| `map`, `filter`, `reduce`, `groupBy`, `pluck`, `orderBy`, `flatten`, `++`, `default` | `references/core.md` |
| Text: `splitBy`, `substringAfter`, `camelize`, `pluralize`, padding | `references/strings.md` |
| `sumBy`, `countBy`, `partition`, `drop`/`take`, `divideBy` | `references/arrays.md` |
| `mapObject`, `filterObject`, `entrySet`, `nameSet`, `divideBy` | `references/objects.md` |
| `now()`, `\|P1D\|`, formatting, time zones | `references/dates.md`, `references/periods.md` |
| Rounding, `abs`, `sqrt`, `randomInt` | `references/math.md`, `references/numbers.md` |
| Type tests and conversions: `isBlank`, `isDecimal`, `valueOf` | `references/types.md`, `references/coercions.md` |
| The type system itself: type declarations, unions, coercion rules | `references/type-system.md` |
| Reading/writing other formats at runtime, `wait`, `fail`, `try` | `references/runtime.md` |
| Hashing, HMAC | `references/crypto.md` |
| `p()`, `lookup()`, `causedBy()` — Mule-only | `references/mule.md` |
| Deep traversal and masking | `references/tree.md`, `references/values.md` |
| `.key`, `.*key`, `..key`, `[0 to 2]`, `.@attr`, `.^raw` | `references/selectors.md` |
| `if/else`, `match`, `do`, `unless`, operator precedence | `references/language.md` |
| MIME types, reader/writer properties, CSV separators, XML namespaces | `references/formats.md` |
| Binary data, base64, MIME types, multipart bodies | `references/binaries.md`, `references/mime.md`, `references/multipart.md` |
| URL encoding, DTDs, structural diffing, timing, environment variables | `references/url.md`, `references/dtd.md`, `references/diff.md`, `references/timer.md`, `references/system.md` |
| An error message you do not recognise | `references/troubleshooting.md` |

Every module except `dw::core` and `dw::Mule` needs an explicit import. Each
reference file states its namespace at the top.

## Idioms worth reaching for

**Reshape a collection** — `map` over arrays, `mapObject` over objects. Using
`map` on an object silently gives you an array of its values.

**Dynamic keys need parentheses.** `{ (item.name): item.value }` builds a key
from an expression; `{ item.name: ... }` creates the literal key `item.name`.

**Positional lambda params.** `$` is the value, `$$` the index (arrays) or key
(objects). Name them when a lambda gets long enough to be unclear.

**Grouping then reshaping** is the common report pattern:

```dataweave
payload
  groupBy (line) -> line.invoiceId
  pluck (lines, invoiceId) -> {
    invoiceId: invoiceId,
    total: sum(lines.amount)
  }
```

**Concatenate with `++`**, for strings, arrays and objects alike. `+` is
arithmetic and will fail on strings.

**Handle absence with `default`**, and prefer it to nested `if`:
`payload.customer.email default "unknown"`.

**Filter before mapping** rather than mapping and pruning nulls afterwards.

## Where scripts usually go wrong

- **Selector returns `null`, not an error.** `.key` on a missing key yields
  `null` and the failure surfaces much later. Use `key!` to assert presence or
  `key?` to test it explicitly.
- **Multi-value vs single-value selectors.** Repeated XML elements need `.*item`;
  `.item` silently gives you only the first.
- **XML is ordered and repeatable, JSON objects are not.** Converting XML with
  repeated elements to JSON needs an explicit array (`.*`), or you lose data.
- **Numbers coming from CSV and XML are strings.** Coerce (`as Number`) before
  arithmetic; comparison against a number otherwise fails silently.
- **`reduce` needs a seed** when the array can be empty, or it returns `null`.
- **Key order and duplicate keys.** DataWeave objects permit duplicate keys;
  writers may keep them. Use `distinctBy` when the target format cannot.
- **Date arithmetic uses periods**: `now() - |P1D|`, not numeric subtraction.

## Formats

Set `output application/json` and so on in the header; add reader or writer
properties inline. `references/formats.md` has the full property tables per
format — including CSV separators and headers, XML namespaces and indentation,
flat file and fixed width schemas, and Excel sheet selection.

```dataweave
output application/csv separator=";", header=true
```

Reader properties belong on `input`, or on `read()` when parsing a string.

## Working practice

- Prefer named `fun` declarations over deeply nested inline lambdas; DataWeave
  has no debugger and the stack traces are shallow.
- Keep the body a composition of small named functions when a mapping exceeds
  roughly thirty lines.
- Test transformations against a real captured payload, not a hand-written one —
  most defects are absent fields and unexpected repetition, not logic errors.
- The [DataWeave playground](https://dataweave.mulesoft.com/learn/dataweave) is
  the fastest way to check an expression.

## Provenance

The `references/` directory is derived from MuleSoft's official DataWeave
documentation, version 2.12. Function signatures, parameter descriptions and
examples are condensed from that source. See `ATTRIBUTION.md`.

Where this skill and the reference disagree, the reference wins — it is
generated from upstream. Where the runtime and the reference disagree, the
runtime wins: the docs are versioned per release and your Mule runtime may not
be on 2.12.
