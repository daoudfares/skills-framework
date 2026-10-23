# dw::dtd — DTD functions

Namespace `dw::xml::Dtd`.
Requires an explicit import: `import * from dw::xml::Dtd`.

Functions: `docTypeAsString`

---

## docTypeAsString

```
docTypeAsString(docType: DocType): String
```

Transforms a `DocType` value to a string representation. _Introduced in DataWeave version 2.5.0._

- `Description` — `docType`
- `DocType` — The `DocType` value to transform to a string.

```dataweave
%dw 2.0
import * from dw::xml::Dtd
output application/json
---
docTypeAsString({rootName: "cXML", systemId: "http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd"})
```

```json
"cXML SYSTEM http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd"
```
