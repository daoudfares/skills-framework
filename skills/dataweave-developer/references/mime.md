# dw::mime — MIME functions

Namespace `dw::module::Mime`.
Requires an explicit import: `import * from dw::module::Mime`.

Functions: `fromString`, `isHandledBy`, `toString`

---

## fromString

```
fromString(mimeType: String): Result<MimeType, MimeTypeError>
```

Transforms a MIME type string value representation to a `MimeType`. _Introduced in DataWeave version 2.7.0._

- `Description` — `mimeType`
- `String` — The MIME type string value to transform to a `MimeType`.

```dataweave
%dw 2.0
import * from dw::module::Mime
output application/json
---
fromString("application/json")
```

```json
{
  "success": true,
  "result": {
      "type": "application",
      "subtype": "json",
      "parameters": {}
  }
}
```

## isHandledBy

```
isHandledBy(base: MimeType, other: MimeType): Boolean
```

Returns `true` if the given `MimeType` value is handled by the base `MimeType` value. _Introduced in DataWeave version 2.7.0._

- `Description` — `base`
- `MimeType` — The MIME type value used as baseline.
- `other` — `MimeType`

```dataweave
%dw 2.0
import * from dw::module::Mime
output application/json

var JSON = {'type': "application", subtype: "json", parameters: {}}
var MULTIPART = {'type': "multipart", subtype: "form-data", parameters: {boundary: "my-boundary"}}
var ALL = {'type': "*", subtype: "*", parameters: {}}
---
{
  a: isHandledBy(JSON, JSON),
  b: isHandledBy({'type': "*", subtype: "json", parameters: {}}, JSON),
  c: isHandledBy({'type': "application", subtype: "*", parameters: {}}, JSON),
  d: isHandledBy(ALL, MULTIPART),
  e: isHandledBy(MULTIPART, ALL),
  f: isHandledBy(JSON, MULTIPART),
  g: isHandledBy(
    {'type': "application", subtype: "*+xml", parameters: {}},
    {'type': "application", subtype: "soap+xml", parameters: {}})
}
```

```json
{
  "a": true,
  "b": true,
  "c": true,
  "d": true,
  "e": false,
  "f": false,
  "g": true
}
```

## toString

```
toString(mimeType: MimeType): String
```

Transforms a `MimeType` value to a string representation. _Introduced in DataWeave version 2.7.0._

- `Description` — `mimeType`
- `MimeType` — The MIME type value to transform to a `String`.

```dataweave
%dw 2.0
import * from dw::module::Mime
output application/json
---
toString({'type': "application", subtype: "json", parameters: {}})
```

```json
"application/json"
```
