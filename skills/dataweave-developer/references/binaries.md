# dw::binaries — Binaries functions

Namespace `dw::core::Binaries`.
Requires an explicit import: `import * from dw::core::Binaries`.

Functions: `concatWith`, `fromBase64`, `fromHex`, `readLinesWith`, `toBase64`, `toHex`, `writeLinesWith`

---

## concatWith

```
concatWith(source: Binary, with: Binary): Binary
```

Concatenates the content of two binaries. _Introduced in DataWeave version 2.5.0._

- `Description` — `source`
- `Binary` — The source binary content.
- `with` — Binary

```dataweave
%dw 2.0
import * from dw::core::Binaries
output application/dw
---
"CAFE" as Binary {base: "16"} concatWith "ABCD" as Binary {base: "16"}
```

```json
"yv6rzQ==" as Binary {base: "64"}
```

```
concatWith(source: Binary, with: Null): Binary
```

Helper function that enables `concatWith` to work with a `null` value.

```
concatWith(source: Null, with: Binary): Binary
```

Helper function that enables `concatWith` to work with a `null` value.

## fromBase64

```
fromBase64(base64String: String): Binary
```

Transforms a Base64 string into a binary value.

- `base64String` — The Base64 string to transform.

```dataweave
%dw 2.0
import * from dw::core::Binaries
output application/octet-stream
---
fromBase64(payload)
```

## fromHex

```
fromHex(hexString: String): Binary
```

Transforms a hexadecimal string into a binary.

- `hexString` — A hexadecimal string to transform.

```dataweave
%dw 2.0
import * from dw::core::Binaries
output application/dw
---
{ "hexToBinary": fromHex("4D756C65") }
```

```json
{
   hexToBinary: "TXVsZQ==" as Binary {base: "64"}
}
```

## readLinesWith

```
readLinesWith(content: Binary, charset: String): Array<String>
```

Splits the specified binary content into lines and returns the results in an array. _Introduced in DataWeave version 2.2.0._

- `content` — Binary data to read and split.
- `charset` — String representing the encoding to read.

```dataweave
%dw 2.0
import * from dw::core::Binaries
var content = read("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n", "application/octet-stream")
output application/json
---
{
   lines : (content readLinesWith "UTF-8"),
   showType: typeOf(content)
}
```

```json
{
   "lines": [ "Line 1", "Line 2", "Line 3", "Line 4", "Line 5" ],
   "showType": "Binary"
}
```

## toBase64

```
toBase64(content: Binary): String
```

Transforms a binary value into a Base64 string.

- `content` — The binary value to transform.

```dataweave
%dw 2.0

import dw::Crypto
import toBase64 from dw::core::Binaries

var emailChecksum = Crypto::MD5("achaval@gmail.com" as Binary)
var image = readUrl(log("https://www.gravatar.com/avatar/$(emailChecksum)"), "application/octet-stream")

output application/json
---
toBase64(image)
```

```json
"/9j/4AAQSkZJRgABAQEAYABgAAD//..."
```

## toHex

```
toHex(content: Binary): String
```

Transforms a binary value into a hexadecimal string.

- `content` — The `Binary` value to transform.

```dataweave
%dw 2.0
import * from dw::core::Binaries
output application/json
var myBinary = "Mule" as Binary
var testType = typeOf(myBinary)
---
{
   "binaryToHex" : toHex(myBinary)
}
```

```json
{ "binaryToHex": "4D756C65" }
```

## writeLinesWith

```
writeLinesWith(content: Array<String>, charset: String): Binary
```

Writes the specified lines and returns the binary content. _Introduced in DataWeave version 2.2.0._

- `content` — Array of items to write.
- `charset` — String representing the encoding to use when writing.

```dataweave
%dw 2.0
import * from dw::core::Binaries
output application/json
---
{ lines: to(1, 10) map "Line $" writeLinesWith  "UTF-8" }
```

```json
{
  "lines": "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n"
}
```
