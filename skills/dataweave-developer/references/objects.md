# dw::objects — Objects functions

Namespace `dw::core::Objects`.
Requires an explicit import: `import * from dw::core::Objects`.

Functions: `divideBy`, `entrySet`, `everyEntry`, `keySet`, `mergeWith`, `nameSet`, `someEntry`, `takeWhile`, `valueSet`

---

## divideBy

```
divideBy(items: Object, amount: Number): Array<Object>
```

Breaks up an object into sub-objects that contain the specified number of key-value pairs. If there are fewer key-value pairs in an object than the specified number, the function will fill the object with those pairs. If there are more pairs, the function will fill another object with the extra pairs.

- `items` — Key-value pairs in the source object.
- `amount` — The number of key-value pairs allowed in an object.

```dataweave
%dw 2.0
import divideBy from dw::core::Objects
output application/json
---
{ "divideBy" : {"a": 1, "b" : true, "a" : 2, "b" : false, "c" : 3} divideBy 2 }
```

```json
{
  "divideBy": [
    {
      "a": 1,
      "b": true
    },
    {
      "a": 2,
      "b": false
    },
    {
      "c": 3
    }
  ]
}
```

## entrySet

```
entrySet<T <: Object>(obj: T): Array<{| key: Key, value: Any, attributes: Object |}>
```

Returns an array of key-value pairs that describe the key, value, and any attributes in the input object. _This function is *Deprecated*. Use dw::Core::entriesOf, instead._

- `obj` — The `Object` to describe.

```dataweave
%dw 2.0
import * from dw::core::Objects
var myVar = read('<xml attr="x"><a>true</a><b>1</b></xml>', 'application/xml')
output application/json
---
{ "entrySet" : entrySet(myVar) }
```

```json
{
  "entrySet": [
    {
       "key": "xml",
       "value": {
         "a": "true",
         "b": "1"
       },
       "attributes": {
         "attr": "x"
       }
    }
  ]
}
```

## everyEntry

```
everyEntry(object: Object, condition: (value: Any, key: Key) -> Boolean): Boolean
```

Returns `true` if every entry in the object matches the condition. The function stops iterating after the first negative evaluation of an element in the object. _Introduced in DataWeave version 2.3.0._

- `object` — The object to evaluate.
- `condition` — The condition to apply to each element.

```dataweave
%dw 2.0
import everyEntry from dw::core::Objects
output application/json
---
{
    a: {} everyEntry (value, key) -> value is String,
    b: {a: "", b: "123"} everyEntry (value, key) -> value is String,
    c: {a: "", b: 123} everyEntry (value, key) -> value is String,
    d: {a: "", b: 123} everyEntry (value, key) -> key as String == "a",
    e: {a: ""} everyEntry (value, key) -> key as String == "a",
    f: null everyEntry ((value, key) -> key as String == "a")
}
```

```json
{
  "a": true,
  "b": true,
  "c": false,
  "d": false,
  "e": true,
  "f": true
}
```

```
everyEntry(list: Null, condition: (Nothing, Nothing) -> Boolean): Boolean
```

Helper function that enables `everyEntry` to work with a `null` value. _Introduced in DataWeave version 2.3.0._

## keySet

```
keySet<K, V>(obj: { (K)?: V }): Array<K>
```

Returns an array of key names from an object. _This function is *Deprecated*. Use dw::Core::keysOf, instead._

- `object` — The object to evaluate.

```dataweave
%dw 2.0
import * from dw::core::Objects
output application/json
---
{ "keySet" : keySet({ "a" : true, "b" : 1}) }
```

```json
{ "keySet" : ["a","b"] }
```

## mergeWith

```
mergeWith<T <: Object, V <: Object>(source: T, target: V): ?
```

Appends any key-value pairs from a source object to a target object. If source and target objects have the same key, the function appends that source object to the target and removes that target object from the output.

- `source` — The object to append to the `target`.
- `target` — The object to which the `source` object is appended.

```dataweave
%dw 2.0
import mergeWith from dw::core::Objects
output application/json
---
{ "mergeWith" : { "a" : true, "b" : 1} mergeWith { "a" : false, "c" : "Test"} }
```

```json
"mergeWith": {
    "b": 1,
    "a": false,
    "c": "Test"
}
```

```
mergeWith<T <: Object>(a: Null, b: T): T
```

Helper function that enables `mergeWith` to work with a `null` value.

```
mergeWith<T <: Object>(a: T, b: Null): T
```

Helper function that enables `mergeWith` to work with a `null` value.

## nameSet

```
nameSet(obj: Object): Array<String>
```

Returns an array of keys from an object. _This function is *Deprecated*. Use dw::Core::namesOf, instead._

- `obj` — The object to evaluate.

```dataweave
%dw 2.0
import * from dw::core::Objects
output application/json
---
{ "nameSet" : nameSet({ "a" : true, "b" : 1}) }
```

```json
{ "nameSet" : ["a","b"] }
```

## someEntry

```
someEntry(obj: Object, condition: (value: Any, key: Key) -> Boolean): Boolean
```

Returns `true` if at least one entry in the object matches the specified condition. The function stops iterating after the first element that matches the condition is found. _Introduced in DataWeave version 2.3.0._

- `obj` — The object to evaluate.
- `condition` — The condition to use when evaluating elements in the object.

```dataweave
%dw 2.0
import someEntry from dw::core::Objects
output application/json
---
{
    a: {} someEntry (value, key) -> value is String,
    b: {a: "", b: "123"} someEntry (value, key) -> value is String,
    c: {a: "", b: 123} someEntry (value, key) -> value is String,
    d: {a: "", b: 123} someEntry (value, key) -> key as String == "a",
    e: {a: ""} someEntry (value, key) -> key as String == "b",
    f: null someEntry (value, key) -> key as String == "a"
}
```

```json
{
  "a": false,
  "b": true,
  "c": true,
  "d": true,
  "e": false,
  "f": false
}
```

```
someEntry(obj: Null, condition: (value: Nothing, key: Nothing) -> Boolean): Boolean
```

Helper function that enables `someEntry` to work with a `null` value. _Introduced in DataWeave version 2.3.0._

## takeWhile

```
takeWhile<T>(obj: Object, condition: (value: Any, key: Key) -> Boolean): Object
```

Selects key-value pairs from the object while the condition is met. _Introduced in DataWeave version 2.3.0._

- `obj` — The object to filter.
- `condition` — The condition (or expression) used to match a key-value pairs in the object.

```dataweave
%dw 2.0
import * from dw::core::Objects
output application/json
var obj = {
  "a": 1,
  "b": 2,
  "c": 5,
  "d": 1
}
---
obj takeWhile ((value, key) ->  value < 3)
```

```json
{
  "a": 1,
  "b": 2
}
```

## valueSet

```
valueSet<K, V>(obj: { (K)?: V }): Array<V>
```

Returns an array of the values from key-value pairs in an object. _This function is *Deprecated*. Use dw::Core::valuesOf, instead._

- `obj` — The object to evaluate.

```dataweave
%dw 2.0
import * from dw::core::Objects
output application/json
---
{ "valueSet" : valueSet({a: true, b: 1}) }
```

```json
{ "valueSet" : [true,1] }
```
