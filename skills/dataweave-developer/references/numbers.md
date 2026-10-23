# dw::numbers — Numbers functions

Namespace `dw::core::Numbers`.
Requires an explicit import: `import * from dw::core::Numbers`.

Functions: `fromBinary`, `fromHex`, `fromRadixNumber`, `toBinary`, `toHex`, `toRadixNumber`

---

## fromBinary

```
fromBinary(binaryText: String): Number
```

Transforms from a binary number into a decimal number. _Introduced in DataWeave version 2.2.0._

- `binaryText` — The binary number represented in a `String`.

```dataweave
%dw 2.0
import fromBinary from dw::core::Numbers
output application/json
---
{
    a: fromBinary("-10"),
    b: fromBinary("11111000111010111010110100101011100001001110000011010101100010111101001011100000100010011000011101100101101001111101111010110010010100110010100100000000000000000000000000000000000000000000000000000000000000"),
    c: fromBinary(0),
    d: fromBinary(null),
    e: fromBinary("100"),
}
```

```json
{
  "a": -2,
  "b": 100000000000000000000000000000000000000000000000000000000000000,
  "c": 0,
  "d": null,
  "e": 4
}
```

```
fromBinary(binaryText: Null): Null
```

Helper function that enables `fromBinary` to work with null value. _Introduced in DataWeave version 2.2.0._

## fromHex

```
fromHex(hexText: String): Number
```

Transforms a hexadecimal number into decimal number. _Introduced in DataWeave version 2.2.0._

- `hexText` — The hexadecimal number represented in a `String`.

```dataweave
%dw 2.0
import fromHex from dw::core::Numbers
output application/json
---
{
    a: fromHex("-1"),
    b: fromHex("3e3aeb4ae1383562f4b82261d969f7ac94ca4000000000000000"),
    c: fromHex(0),
    d: fromHex(null),
    e: fromHex("f"),
}
```

```json
{
  "a": -1,
  "b": 100000000000000000000000000000000000000000000000000000000000000,
  "c": 0,
  "d": null,
  "e": 15
}
```

```
fromHex(hexText: Null): Null
```

Helper function that enables `fromHex` to work with null value. _Introduced in DataWeave version 2.2.0._

## fromRadixNumber

```
fromRadixNumber(numberStr: String, radix: Number): Number
```

Transforms a number in the specified radix into decimal number _Introduced in DataWeave version 2.2.0._

- `numberText` — The number text.
- `radix` — The radix number.

```dataweave
%dw 2.0
import fromRadixNumber from dw::core::Numbers
output application/json
---
{
    a: fromRadixNumber("10", 2),
    b: fromRadixNumber("FF", 16)
}
```

```json
{
  "a": 2,
  "b": 255
}
```

## toBinary

```
toBinary(number: Number): String
```

Transforms a decimal number into a binary number. _Introduced in DataWeave version 2.2.0._

- `number` — The input number.

```dataweave
%dw 2.0
import toBinary from dw::core::Numbers
output application/json
---
{
    a: toBinary(-2),
    b: toBinary(100000000000000000000000000000000000000000000000000000000000000),
    c: toBinary(0),
    d: toBinary(null),
    e: toBinary(2),
}
```

```json
{
  "a": "-10",
  "b": "11111000111010111010110100101011100001001110000011010101100010111101001011100000100010011000011101100101101001111101111010110010010100110010100100000000000000000000000000000000000000000000000000000000000000",
  "c": "0",
  "d": null,
  "e": "10"
}
```

```
toBinary(number: Null): Null
```

Helper function that enables `toBinary` to work with null value. _Introduced in DataWeave version 2.2.0._

## toHex

```
toHex(number: Number): String
```

Transforms a decimal number into a hexadecimal number. _Introduced in DataWeave version 2.2.0._

- `number` — The input number.

```dataweave
%dw 2.0
import toHex from dw::core::Numbers
output application/json
---
{
    a: toHex(-1),
    b: toHex(100000000000000000000000000000000000000000000000000000000000000),
    c: toHex(0),
    d: toHex(null),
    e: toHex(15),
}
```

```json
{
  "a": "-1",
  "b": "3e3aeb4ae1383562f4b82261d969f7ac94ca4000000000000000",
  "c": "0",
  "d": null,
  "e": "f"
}
```

```
toHex(number: Null): Null
```

Helper function that enables `toHex` to work with null value. _Introduced in DataWeave version 2.2.0._

## toRadixNumber

```
toRadixNumber(number: Number, radix: Number): String
```

Transforms a decimal number into a number string in other radix. _Introduced in DataWeave version 2.2.0._

- `number` — The decimal number.
- `radix` — The radix of the result number.

```dataweave
%dw 2.0
import toRadixNumber from dw::core::Numbers
output application/json
---
{
    a: toRadixNumber(2, 2),
    b: toRadixNumber(255, 16)
}
```

```json
{
  "a": "10",
  "b": "ff"
}
```
