# dw::multipart — Multipart functions

Namespace `dw::module::Multipart`.
Requires an explicit import: `import * from dw::module::Multipart`.

Functions: `field`, `file`, `form`, `generateBoundary`

---

## field

```
field(opts: {| name: String, value: Any, mime?: String, fileName?: String |}): MultipartPart
```

Creates a `MultipartPart` data structure using the specified part name, input content for the part, format (or mime type), and optionally, file name. This version of the `field` function accepts arguments as an array of objects that use the parameter names as keys, for example: `Multipart::field({name:"order",value: myOrder, mime: "application/json", fileName: "order.json"})`

- `opts` — Array of objects that specifies: * A unique `name` (required) for the `Content-Disposition` header of the part. * A `value` (required) for the content of the part. * `mime` (optional for strings) for the mime type (for example, `application/json`) to apply to content within the part. This setting can be used to transform the input type, for example, from JSON to XML. * An optional `fileName` value that you can supply to the `filename` parameter in the part's `Content-Disposition` header.

```dataweave
%dw 2.0
import dw::module::Multipart
output multipart/form-data
var firstPart = "content for my first part"
var secondPart = "content for my second part"
---
{
  parts: {
    part1: Multipart::field({name:"myFirstPart",value: firstPart}),
    part2: Multipart::field("mySecondPart", secondPart)
  }
}
```

```
field(name: String, value: Any, mime: String = "", fileName: String = ""): MultipartPart
```

Creates a `MultipartPart` data structure using the specified part name, input content for the part, format (or mime type), and optionally, file name. This version of the `field` function accepts arguments in a comma-separated list, for example: Multipart::field("order", myOrder,"application/json", "order.json")`

- `opts` — A set of parameters that specify: * A unique `name` (required) for the `Content-Disposition` header of the part. * A `value` (required) for the content of the part. * `mime` (optional for strings) for the mime type (for example, `application/json`) to apply to content within the part. This type can be used to transform the input type. * An optional `fileName` value that you can supply to the `filename` parameter in the part's `Content-Disposition` header.

```dataweave
%dw 2.0
import dw::module::Multipart
output multipart/form-data
var myOrder = [
  {
    order: 1,
    amount: 2
  },
  {
    order: 32,
    amount: 1
  }
]
var myClients = {
  clients: {
    client: {
      id: 1,
      name: "Mariano"
    },
    client: {
      id: 2,
      name: "Shoki"
    }
  }
}
---
{
  parts: {
    order: Multipart::field("order", myOrder, "application/json", "order.json"),
    clients: Multipart::field("clients", myClients, "application/xml")
  }
}
```

## file

```
file(opts: {| name: String, path: String, mime?: String, fileName?: String |})
```

Creates a `MultipartPart` data structure from a resource file. This version of the `file` function accepts as argument an object containing key/value pairs, enabling you to enter the key/value pairs in any order, for example: Multipart::file({ name: "myFile", path: "myClients.json", mime: "application/json", fileName: "partMyClients.json"})

- `opts` — An object that specifies the following key/value pairs: * A unique `name` (required) for the `Content-Disposition` header of the part. * A `path` (required) relative to the `src/main/resources` project path for the Mule app. * `mime` (optional for strings) for the mime type (for example, `application/json`) to apply to content within the part. This setting _cannot_ be used to transform the input mime type. * An optional `fileName` value for the `filename` parameter in the part's `Content-Disposition` header. Defaults to the string `"filename"` if not supplied. This value does not need to match the input file name.

```dataweave
%dw 2.0
import dw::module::Multipart
output application/dw
var ordersFilePath = "./orders.xml"
---
Multipart::file{ name: "file", path: ordersFilePath, mime: "application/xml", fileName: "orders.xml" }
```

```json
{
headers: {
    "Content-Type": "application/xml",
    "Content-Disposition": {
      name: "file",
      filename: "orders.xml"
    }
  },
  content: "<?xml version='1.0' encoding='UTF-8'?>\n<orders>\n  <order>\n    <item>\n      <id>1001</id>\n      <qty>1</qty>\n      <price>\$100</price>\n    </item>\n    <item>\n      <id>2001</id>\n      <qty>2</qty>\n      <price>\$50</price>\n    </item>\n  </order>\n</orders>"
}
```

```
file(fieldName: String, path: String, mime: String = 'application/octet-stream', sentFileName: String = 'filename')
```

Creates a `MultipartPart` data structure from a resource file. This version of the `file` function accepts String arguments in a comma-separated list, for example: Multipart::field("myFile", myClients, 'application/json', "partMyClients.json")

- `fieldName` — A unique name (required) for the `Content-Disposition` header of the part.
- `path` — A path (required) relative to the `src/main/resources` project path for the Mule app.
- `mime` — The mime type (optional for strings), for example, `application/json`, to apply to content within the part. This setting _cannot_ be used to transform the input mime type.
- `sentFileName` — An optional file name value for the `filename` parameter in the part's `Content-Disposition` header. Defaults to the string `"filename"` if not specified. This value does not need to match the input file name.

```dataweave
%dw 2.0
import dw::module::Multipart
var myClients = "myClients.json"
output multipart/form-data
---
Multipart::form([
 Multipart::file("myFile", myClients, 'application/json', "partMyClients.json")
])
```

## form

```
form(parts: Array<MultipartPart>): Multipart
```

Creates a `Multipart` data structure using a specified array of parts.

- `parts` — An array of parts (`MultipartPart` data structures).

```dataweave
%dw 2.0
import dw::module::Multipart
output multipart/form-data
var myOrders = "./orders.xml"
var fileArgs = { name: "file", path: myOrders, mime: "application/xml", fileName: "myorders.xml"}
var fieldArgs = {name:"userName",value: "Annie Point", mime: "text/plain"}
---
Multipart::form([
  Multipart::file(fileArgs),
  Multipart::field(fieldArgs),
  Multipart::field("myJson", {"user": "Annie Point"}, "application/json", "userInfo.json")
])
```

## generateBoundary

```
generateBoundary(len: Number = 70): String
```

Helper function for generating boundaries in `Multipart` data structures.
