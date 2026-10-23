# dw::url — URL functions

Namespace `dw::core::URL`.
Requires an explicit import: `import * from dw::core::URL`.

Functions: `compose`, `decodeURI`, `decodeURIComponent`, `encodeURI`, `encodeURIComponent`, `parseURI`

---

## compose

```
compose(parts: Array<String>, interpolation: Array<String>): String
```

Uses a custom string interpolator to replace URL components with a `encodeURIComponent` result. You can call this function using the standard call, or a simplified version.

- `baseStringArray` — A string array that contains the URL parts to interpolate using the strings in the `interpolationStringArray` parameter.
- `interpolationStringArray` — A string array that contains the strings used to interpolate the `baseStringArray`.

```dataweave
%dw 2.0
output application/json
var urlPath = "content folder"
import * from dw::core::URL
---
 { "encodedURL" : compose(["http://examplewebsite.com/", "/page.html"], ["$(urlPath)"]) }
```

```json
{ "encodedURL" : "http://examplewebsite.com/content%20folder/page.html" }
```

## decodeURI

```
decodeURI(text: String): String
```

Decodes the escape sequences (such as `%20`) in a URI. The function replaces each escape sequence in the encoded URI with the character that it represents, but does not decode escape sequences that could not have been introduced by `encodeURI`. The character `#` is not decoded from escape sequences.

- `text` — The URI to decode.

```dataweave
%dw 2.0
import * from dw::core::URL
output application/json
---
{
  "decodeURI" : decodeURI('http://asd/%20text%20to%20decode%20/text')
}
```

```json
{
  "decodeURI": "http://asd/ text to decode /text"
}
```

## decodeURIComponent

```
decodeURIComponent(text: String): String
```

Decodes a Uniform Resource Identifier (URI) component previously created by `encodeURIComponent` or a similar routine. For an example, see `encodeURIComponent`.

- `text` — URI component string.

```dataweave
%dw 2.0
import * from dw::core::URL
output application/json
---
{
  "decodeURIComponent": {
    "decodeURIComponent" : decodeURIComponent("%20PATH/%20TO%20/DECODE%20"),
    "decodeURIComponent" : decodeURIComponent("%3B%2C%2F%3F%3A%40%26%3D"),
    "decodeURIComponent" : decodeURIComponent("%2D%5F%2E%21%7E%2A%27%28%29%24"),
  }
}
```

```json
{
   decodeURIComponent: {
     decodeURIComponent: " PATH/ TO /DECODE ",
     decodeURIComponent: ";,/?:@&=",
    decodeURIComponent: "-_.!~*'()\$"
   }
}
```

## encodeURI

```
encodeURI(text: String): String
```

Encodes a URI with UTF-8 escape sequences. Applies up to four escape sequences for characters composed of two "surrogate" characters. The function assumes that the URI is a complete URI, so it does not encode reserved characters that have special meaning. The function _does not encode these characters_ with UTF-8 escape sequences:

- `text` — The URI to encode.

```dataweave
%dw 2.0
import * from dw::core::URL
output application/json
---
{
    "encodeURI" : encodeURI("http://asd/ text to decode /%/\"\\/text"),
    "not_encoded": encodeURI("http://:;,/?:@&=\$_-_.!~*'()")
}
```

```json
{
    "encodeURI": "http://asd/%20text%20to%20decode%20/%25/%22%5C/text",
    "not_encoded": "http://:;,/?:@&=$_-_.!~*'()"
}
```

## encodeURIComponent

```
encodeURIComponent(text: String): String
```

Escapes certain characters in a URI component using UTF-8 encoding. There can be only four escape sequences for characters composed of two "surrogate" * characters. `encodeURIComponent` escapes all characters _except the following_: alphabetic, decimal digits, `- _ . ! ~ * ' ( )`. Note that `encodeURIComponent` differs from `encodeURI` in that it encodes reserved characters and the Number sign `#` of `encodeURI`:

- `text` — URI component string.

```dataweave
%dw 2.0
import * from dw::core::URL
output application/json
---
{
  "comparing_encode_functions_output" : {
  	"encodeURIComponent" : encodeURI(" PATH/ TO /ENCODE "),
  	"encodeURI" : encodeURI(" PATH/ TO /ENCODE "),
  	"encodeURIComponent_to_hex" : encodeURIComponent(";,/?:@&="),
  	"encodeURI_not_to_hex" : encodeURI(";,/?:@&="),
  	"encodeURIComponent_not_encoded" : encodeURIComponent("-_.!~*'()"),
  	"encodeURI_not_encoded" : encodeURI("-_.!~*'()")
  }
}
```

```json
{
  "comparing_encode_functions_output": {
    "encodeURIComponent": "%20PATH/%20TO%20/ENCODE%20",
    "encodeURI": "%20PATH/%20TO%20/ENCODE%20",
    "encodeURIComponent_to_hex": "%3B%2C%2F%3F%3A%40%26%3D",
    "encodeURI_not_to_hex": ";,/?:@&=",
    "encodeURIComponent_not_encoded": "-_.!~*'()",
    "encodeURI_not_encoded": "-_.!~*'()"
  }
}
```

## parseURI

```
parseURI(uri: String): URI
```

Parses a URL and returns a `URI` object. The `isValid: Boolean` property in the output `URI` object indicates whether the parsing process succeeded. Every field in this object is optional, and a field will appear in the output only if it was present in the URL input.

- `uri` — The URI input.

```dataweave
%dw 2.0
import * from dw::core::URL
output application/json
---
{
  'composition': parseURI('https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#footer')
}
```

```json
{
  "composition": {
    "isValid": true,
    "raw": "https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#footer",
    "host": "en.wikipedia.org",
    "authority": "en.wikipedia.org",
    "fragment": "footer",
    "path": "/wiki/Uniform_Resource_Identifier",
    "scheme": "https",
    "isAbsolute": true,
    "isOpaque": false
  }
}
```
