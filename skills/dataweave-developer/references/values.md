# dw::values — Values functions

Namespace `dw::util::Values`.
Requires an explicit import: `import * from dw::util::Values`.

Functions: `attr`, `field`, `index`, `mask`, `update`

---

## attr

```
attr(namespace: Namespace | Null = null, name: String): PathElement
```

This function creates a `PathElement` to use for selecting an XML attribute and populates the type's `selector` field with the given string. Some versions of the `update` and `mask` functions accept a `PathElement` as an argument. _Introduced in DataWeave version 2.2.2._

- `namespace` — The namespace of the attribute to select. If not specified, a null value is set.
- `name` — The string that names the attribute to select.

```dataweave
%dw 2.0
output application/json
import * from dw::util::Values
ns ns0 http://acme.com/fo
---
attr(ns0 , "myAttr")
```

```json
{
   "kind": "Attribute",
   "namespace": "http://acme.com/foo",
   "selector": "myAttr"
 }
```

## field

```
field(namespace: Namespace | Null = null, name: String): PathElement
```

This function creates a `PathElement` data type to use for selecting an _object field_ and populates the type's `selector` field with the given string. Some versions of the `update` and `mask` functions accept a `PathElement` as an argument. _Introduced in DataWeave version 2.2.2._

- `namespace` — The namespace of the field to select. If not specified, a null value is set.
- `name` — A string that names the attribute to select.

```dataweave
%dw 2.0
output application/json
import * from dw::util::Values
ns ns0 http://acme.com/foo
---
field(ns0 , "myFieldName")
```

```json
{
   "kind": "Object",
   "namespace": "http://acme.com/foo",
   "selector": "myFieldName"
 }
```

## index

```
index(index: Number): PathElement
```

This function creates a `PathElement` data type to use for selecting an _array element_ and populates the type's `selector` field with the specified index. Some versions of the `update` and `mask` functions accept a `PathElement` as an argument. _Introduced in DataWeave version 2.2.2._

- `index` — The index.

```dataweave
%dw 2.0
output application/json
import * from dw::util::Values
ns ns0 http://acme.com/foo
---
index(0)
```

```json
{
   "kind": "Array",
   "namespace": null,
   "selector": 0
 }
```

## mask

```
mask(value: Null, fieldName: String | Number | PathElement): (newValueProvider: (oldValue: Any, path: Path) -> Any) -> Null
```

Helper function that enables `mask` to work with a `null` value. _Introduced in DataWeave version 2.2.2._

```
mask(value: Any, selector: PathElement): (newValueProvider: (oldValue: Any, path: Path) -> Any) -> Any
```

This `mask` function replaces all _simple_ elements that match the specified criteria. Simple elements do not have child elements and cannot be objects or arrays. _Introduced in DataWeave version 2.2.2._

- `value` — A value to use for masking. The value can be any DataWeave type.
- `selector` — The `PathElement` selector.

```dataweave
%dw 2.0
output application/json
import * from dw::util::Values
---
[{name: "Peter Parker", password: "spiderman"}, {name: "Bruce Wayne", password: "batman"}] mask field("password") with "*****"
```

```json
[
   {
     "name": "Peter Parker",
     "password": "*****"
   },
   {
     "name": "Bruce Wayne",
     "password": "*****"
   }
 ]
```

```
mask(value: Any, fieldName: String): (newValueProvider: (oldValue: Any, path: Path) -> Any) -> Any
```

This `mask` function selects a field by its name. _Introduced in DataWeave version 2.2.2._

- `value` — The value to use for masking. The value can be any DataWeave type.
- `fieldName` — A string that specifies the name of the field to mask.

```dataweave
%dw 2.0
output application/json
import * from dw::util::Values
---
[{name: "Peter Parker", password: "spiderman"}, {name: "Bruce Wayne", password: "batman"}] mask "password" with "*****"
```

```json
[
   {
     "name": "Peter Parker",
     "password": "*****"
   },
   {
     "name": "Bruce Wayne",
     "password": "*****"
   }
 ]
```

```
mask(value: Any, i: Number): (newValueProvider: (oldValue: Any, path: Path) -> Any) -> Any
```

This `mask` function selects an element from array by its index. _Introduced in DataWeave version 2.2.2._

- `value` — The value to mask. The value can be any DataWeave type.
- `index` — The index to mask. The index must be a number.

```dataweave
%dw 2.0
output application/json
import * from dw::util::Values
---
[[123, true], [456, true]] mask 1 with false
```

```json
[
   [
     123,
     false
   ],
   [
     456,
     false
   ]
 ]
```

## update

```
update(objectValue: Object, fieldName: String): UpdaterValueProvider<Object>
```

This `update` function updates a field in an object with the specified string value. The function returns a new object with the specified field and value. _Introduced in DataWeave version 2.2.2._

- `objectValue` — The object to update.
- `fieldName` — A string that provides the name of the field.

```dataweave
%dw 2.0
import * from dw::util::Values
output application/json
---
{name: "Mariano"} update "name" with "Data Weave"
```

```json
{
  "name": "Data Weave"
}
```

```
update(objectValue: Object, fieldName: PathElement): UpdaterValueProvider<Object>
```

This `update` function updates an object field with the specified `PathElement` value. The function returns a new object with the specified field and value. _Introduced in DataWeave version 2.2.2._

- `objectValue` — The object to update.
- `fieldName` — A `PathElement` that specifies the field name.

```dataweave
%dw 2.0
import * from dw::util::Values
output application/json
---
{name: "Mariano"} update field("name") with "Data Weave"
```

```json
{
  "name": "Data Weave"
}
```

```
update(arrayValue: Array, indexToUpdate: Number): UpdaterValueProvider<Array>
```

Updates an array index with the specified value. This `update` function returns a new array that changes the value of the specified index. _Introduced in DataWeave version 2.2.2._

- `objectValue` — The array to update.
- `indexToUpdate` — The index of the array to update. The index must be a number.

```dataweave
%dw 2.0
import * from dw::util::Values
output application/json
---
[1,2,3] update 1 with 5
```

```json
[
   1,
   5,
   3
 ]
```

```
update(arrayValue: Array, indexToUpdate: String): UpdaterValueProvider<Array>
```

This `update` function updates all objects within the specified array with the given string value. _Introduced in DataWeave version 2.2.2._

- `objectValue` — The array of objects to update.
- `indexToUpdate` — A string providing the name of the field to update.

```dataweave
%dw 2.0
import * from dw::util::Values
output application/json
---
[{role: "a", name: "spiderman"}, {role: "b", name: "batman"}] update "role" with "Super Hero"
```

```json
[{
   "role": "Super Hero",
   "name": "spiderman"
 },
 {
   "role": "Super Hero",
   "name": "batman"
}]
```

```
update(arrayValue: Array, indexToUpdate: PathElement): UpdaterValueProvider<Array>
```

This `update` function updates the specified index of an array with the given `PathElement` value. The function returns a new array that contains given value at the specified index. _Introduced in DataWeave version 2.2.2._

- `objectValue` — The array to update.
- `indexToUpdate` — The index of the array to update. The index must be specified as a `PathElement`.

```dataweave
%dw 2.0
import * from dw::util::Values
output application/json
---
[1,2,3] update index(1) with 5
```

```json
[
   1,
   5,
   3
 ]
```

```
update(value: Array | Object | Null, path: Array<String | Number | PathElement>): UpdaterValueProvider<Array | Object | Null>
```

Updates the value at the specified path with the given value. _Introduced in DataWeave version 2.2.2._

- `objectValue` — The value to update. Accepts an array, object, or null value.
- `path` — The path to update. The path must be an array of strings, numbers, or `PathElement`s.

```dataweave
%dw 2.0
import * from dw::util::Values
output application/json
---
{user: {name: "Mariano"}} update ["user", field("name")] with "Data Weave"
```

```json
{
   "user": {
     "name": "Data Weave"
   }
 }
```

```
update(value: Null, toUpdate: Number | String | PathElement): UpdaterValueProvider<Null>
```

Helper function that enables `update` to work with a `null` value. _Introduced in DataWeave version 2.2.2._
