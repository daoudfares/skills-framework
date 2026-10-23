# dw::tree — Tree functions

Namespace `dw::util::Tree`.
Requires an explicit import: `import * from dw::util::Tree`.

Functions: `asExpressionString`, `filterArrayLeafs`, `filterObjectLeafs`, `filterTree`, `isArrayType`, `isAttributeType`, `isObjectType`, `mapLeafValues`, `nodeExists`

---

## asExpressionString

```
asExpressionString(path: Path): String
```

Transforms a `Path` value into a string representation of the path. _Introduced in DataWeave version 2.2.2._

- `path` — The `Path` value to transform into a `String` value.

```dataweave
%dw 2.0
import * from dw::util::Tree
output application/json
---
asExpressionString([
        {kind: OBJECT_TYPE, selector: "user", namespace: null},
        {kind: ATTRIBUTE_TYPE, selector: "name", namespace: null}
    ])
```

```json
".user.@name"
```

## filterArrayLeafs

```
filterArrayLeafs(value: Any, criteria: (value: Any, path: Path) -> Boolean): Any
```

Applies a filtering expression to leaf or `Path` values of an array. The leaf values in the array must be `SimpleType` or `Null` values. See https://docs.mulesoft.com/dataweave/latest/dw-core-types[Core Types] for descriptions of the types. _Introduced in DataWeave version 2.4.0._

- `value` — An input value of `Any` type.
- `criteria` — Boolean expression to apply to `SimpleType` or `Null` leaf values of all arrays in the input `value`. If the result is `true`, the array retains the leaf value. If not, the function removes the leaf value from the output.

```dataweave
%dw 2.0
import * from dw::util::Tree
var myArray = [1, {name: ["", true], test: 213}, "123", null]
output application/json
---
{
   a: myArray filterArrayLeafs ((value, path) ->
        !(value is Null or value is String)),
   b:  myArray filterArrayLeafs ((value, path) ->
        (value is Null or value == 1)),
   c: { a : [1,2] } filterArrayLeafs ((value, path) ->
        (value is Null or value == 1)),
   d: myArray filterArrayLeafs ((value, path) ->
        !isArrayType(path))
}
```

```json
{
  "a": [
    1,
    {
      "name": [
        true
      ],
      "test": 213
    }
  ],
  "b": [
    1,
    {
      "name": [

      ],
      "test": 213
    },
    null
  ],
  "c": {
    "a": [
     1
    ]
  },
  "d": [
    {
      "name": [

      ],
      "test": 213
    }
  ]
}
```

## filterObjectLeafs

```
filterObjectLeafs(value: Any, criteria: (value: Any, path: Path) -> Boolean): Any
```

Applies a filtering expression to leaf or `Path` values of keys in an object. The leaf values in the object must be `SimpleType` or `Null` values. See https://docs.mulesoft.com/dataweave/latest/dw-core-types[Core Types] for descriptions of the types. _Introduced in DataWeave version 2.4.0._

- `value` — An input value of `Any` type.
- `criteria` — Boolean expression to apply to `SimpleType` or `Null` leaf values of all objects in the input `value`. If the result is `true`, the object retains the leaf value and its key. If not, the function removes the leaf value and key from the output.

```dataweave
%dw 2.0
import * from dw::util::Tree
var myArray = [{name @(mail: "me@me.com", test:123 ): "", id:"test"},
               {name: "Me", id:null}]
output application/json
---
{
 a: {
     name: "Mariano",
     lastName: null,
     age: 123,
     friends: myArray
    }  filterObjectLeafs ((value, path) ->
         !(value is Null or value is String)),
 b: { c : null, d : "hello" } filterObjectLeafs ((value, path) ->
         (value is Null and isObjectType(path)))
}
```

```json
{
  "a": {
    "age": 123,
    "friends": [
      {

      },
      {

      }
    ]
  },
  "b": {
    "c": null
  }
}
```

## filterTree

```
filterTree(value: Any, criteria: (value: Any, path: Path) -> Boolean): Any
```

Filters the value or path of nodes in an input based on a specified `criteria`. The function iterates through the nodes in the input. The `criteria` can apply to the value or path in the input. If the `criteria` evaluates to `true`, the node remains in the output. If `false`, the function filters out the node. _Introduced in DataWeave version 2.4.0._

- `value` — The value to filter.
- `criteria` — The expression that determines whether to filter the node.

```dataweave
%dw 2.0
import * from dw::util::Tree
output application/dw
---
{
    a: {
          name : "",
          lastName @(foo: ""): "Achaval",
          friends @(id: 123): [{id: "", test: true}, {age: 123}, ""]
        } filterTree ((value, path) ->
            value match  {
                            case s is String -> !isEmpty(s)
                            else -> true
                          }
    ),
    b: null filterTree ((value, path) -> value is String),
    c: [
            {name: "Mariano", friends: []},
            {test: [1,2,3]},
            {dw: ""}
        ] filterTree ((value, path) ->
            value match  {
                            case a is Array ->  !isEmpty(a as Array)
                            else -> true
                        })
}
```

```dataweave
{
  a: {
    lastName: "Achaval",
    friends @(id: 123): [
      {
        test: true
      },
      {
        age: 123
      }
    ]
  },
  b: null,
  c: [
    {
      name: "Mariano"
    },
    {
      test: [
        1,
        2,
        3
      ]
    },
    {
      dw: ""
    }
  ]
}
```

## isArrayType

```
isArrayType(path: Path): Boolean
```

Returns `true` if the provided `Path` value is an `ARRAY_TYPE` expression. _Introduced in DataWeave version 2.4.0._

- `path` — The `Path` value to validate.

```dataweave
%dw 2.0
import * from dw::util::Tree
output application/json
---
{
  a: isArrayType([{kind: OBJECT_TYPE, selector: "user", namespace: null},
                  {kind: ATTRIBUTE_TYPE, selector: "name", namespace: null}]),
  b: isArrayType([{kind: OBJECT_TYPE, selector: "user", namespace: null},
                  {kind: ARRAY_TYPE, selector: 0, namespace: null}]),
  c: isArrayType([{kind: ARRAY_TYPE, selector: 0, namespace: null}])
}
```

```json
{
  "a": false,
  "b": true,
  "c": true
}
```

## isAttributeType

```
isAttributeType(path: Path): Boolean
```

Returns `true` if the provided `Path` value is an `ATTRIBUTE_TYPE` expression. _Introduced in DataWeave version 2.4.0._

- `path` — The `Path` value to validate.

```dataweave
%dw 2.0
import * from dw::util::Tree
output application/json
---
{
  a: isAttributeType([{kind: OBJECT_TYPE, selector: "user", namespace: null},
                      {kind: ATTRIBUTE_TYPE, selector: "name", namespace: null}]),
  b: isAttributeType([{kind: OBJECT_TYPE, selector: "user", namespace: null},
                      {kind: ARRAY_TYPE, selector: "name", namespace: null}]),
  c: isAttributeType([{kind: ATTRIBUTE_TYPE, selector: "name", namespace: null}])
}
```

```json
{
  "a": true,
  "b": false,
  "c": true
}
```

## isObjectType

```
isObjectType(path: Path): Boolean
```

Returns `true` if the provided `Path` value is an `OBJECT_TYPE` expression. _Introduced in DataWeave version 2.4.0._

- `path` — The `Path` value to validate.

```dataweave
%dw 2.0
import * from dw::util::Tree
output application/json
---
{
  a: isObjectType([{kind: OBJECT_TYPE, selector: "user", namespace: null},
                   {kind: ATTRIBUTE_TYPE, selector: "name", namespace: null}]),
  b: isObjectType([{kind: OBJECT_TYPE, selector: "user", namespace: null},
                   {kind: OBJECT_TYPE, selector: "name", namespace: null}]),
  c: isObjectType([{kind: OBJECT_TYPE, selector: "user", namespace: null}])
}
```

```json
{
  "a": false,
  "b": true,
  "c": true
}
```

## mapLeafValues

```
mapLeafValues(value: Any, callback: (value: Any, path: Path) -> Any): Any
```

Maps the terminal (leaf) nodes in the tree. Leafs nodes cannot have an object or an array as a value. _Introduced in DataWeave version 2.2.2._

- `value` — The value to map.
- `callback` — The mapper function.

```dataweave
%dw 2.0
import * from dw::util::Tree
output application/json
---
 {
     user: [{
         name: "mariano",
         lastName: "achaval"
     }],
     group: "data-weave"
 } mapLeafValues (value, path) -> upper(value)
```

```json
{
   "user": [
     {
       "name": "MARIANO",
       "lastName": "ACHAVAL"
     }
   ],
   "group": "DATA-WEAVE"
 }
```

## nodeExists

```
nodeExists(value: Any, callback: (value: Any, path: Path) -> Boolean): Boolean
```

Returns `true` if any node in a given tree validates against the specified criteria. _Introduced in DataWeave version 2.2.2._

- `value` — The value to search.
- `callback` — The criteria to apply to the input `value`.

```dataweave
%dw 2.0
import * from dw::util::Tree
var myObject =  {
     user: [{
         name: "mariano",
         lastName: "achaval",
         friends: [
             {
                 name: "julian"
             },
             {
                 name: "tom"
             }
         ]
     },
     {
         name: "leandro",
         lastName: "shokida",
         friends: [
             {
                 name: "peter"
             },
             {
                 name: "robert"
             }
         ]

     }
     ]
 }
output application/json
---
{
    mariano : myObject nodeExists ((value, path) -> path[-1].selector == "name" and value == "mariano"),
    julian : myObject nodeExists ((value, path) -> path[-1].selector == "name" and value == "julian"),
    tom : myObject nodeExists ($$[-1].selector == "name" and $ == "tom"),
    leandro : myObject nodeExists ($$[-1].selector == "name" and $ ==  "leandro"),
    peter : myObject nodeExists ($$[-1].selector == "name" and $ == "peter"),
    wrongField: myObject nodeExists ($$[-1].selector == "wrongField"),
    teo: myObject nodeExists ($$[-1].selector == "name" and $ == "teo")
}
```

```json
{
  "mariano": true,
  "julian": true,
  "tom": true,
  "leandro": true,
  "peter": true,
  "wrongField": false,
  "teo": false
}
```
