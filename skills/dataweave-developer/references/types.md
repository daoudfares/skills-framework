# dw::types — Types functions

Namespace `dw::core::Types`.
Requires an explicit import: `import * from dw::core::Types`.

Functions: `arrayItem`, `baseTypeOf`, `functionParamTypes`, `functionReturnType`, `intersectionItems`, `isAnyType`, `isArrayType`, `isBinaryType`, `isBooleanType`, `isDateTimeType`, `isDateType`, `isFunctionType`, `isIntersectionType`, `isKeyType`, `isLiteralType`, `isLocalDateTimeType`, `isLocalTimeType`, `isNamespaceType`, `isNothingType`, `isNullType`, `isNumberType`, `isObjectType`, `isPeriodType`, `isRangeType`, `isReferenceType`, `isRegexType`, `isStringType`, `isTimeType`, `isTimeZoneType`, `isTypeType`, `isUnionType`, `isUriType`, `literalValueOf`, `metadataOf`, `nameOf`, `objectFields`, `unionItems`

---

## arrayItem

```
arrayItem(t: Type): Type
```

Returns the type of the given array. This function fails if the input is not an Array type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ArrayOfString = Array<String>
type ArrayOfNumber = Array<Number>
type ArrayOfAny = Array<Any>
type ArrayOfAnyDefault = Array
output application/json
---
{
   a: arrayItem(ArrayOfString),
   b: arrayItem(ArrayOfNumber),
   c: arrayItem(ArrayOfAny),
   d: arrayItem(ArrayOfAnyDefault)
}
```

```json
{
  "a": "String",
  "b": "Number",
  "c": "Any",
  "d": "Any"
}
```

## baseTypeOf

```
baseTypeOf(t: Type): Type
```

Returns an the base type of the given type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = String {format: "YYYY-MM-dd"}
output application/json
---
{
   a: baseTypeOf(AType)
}
```

```json
{
  "a": "String"
}
```

## functionParamTypes

```
functionParamTypes(t: Type): Array<FunctionParam>
```

Returns the list of parameters from the given function type. This function fails if the provided type is not a Function type. _Introduced in DataWeave version 2.3.0._

- `t` — The function type.

```dataweave
%dw 2.0
output application/json
import * from dw::core::Types
type AFunction = (String, Number) -> Number
type AFunction2 = () -> Number
---
{
    a: functionParamTypes(AFunction),
    b: functionParamTypes(AFunction2)
}
```

```json
{
   "a": [
     {
       "paramType": "String",
       "optional": false
     },
     {
       "paramType": "Number",
       "optional": false
     }
   ],
   "b": [

   ]
 }
```

## functionReturnType

```
functionReturnType(t: Type): Type | Null
```

Returns the type of a function's return type. This function fails if the input type is not a Function type. _Introduced in DataWeave version 2.3.0._

- `t` — The function type.

```dataweave
%dw 2.0
output application/json
import * from dw::core::Types
type AFunction = (String, Number) -> Number
type AFunction2 = () -> Number
---
{
    a: functionReturnType(AFunction),
    b: functionReturnType(AFunction2)
}
```

```json
{
  "a": "Number",
  "b": "Number"
}
```

## intersectionItems

```
intersectionItems(t: Type): Array<Type>
```

Returns an array of all the types that define a given Intersection type. This function fails if the input is not an Intersection type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = {name: String} & {age: Number}
output application/json
---
{
   a: intersectionItems(AType)
}
```

```json
{
  "a": ["Object","Object"]
}
```

## isAnyType

```
isAnyType(t: Type): Boolean
```

Returns `true` if the input is the Any type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AAny = Any
output application/json
---
{
   a: isAnyType(AAny),
   b: isAnyType(Any),
   c: isAnyType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isArrayType

```
isArrayType(t: Type): Boolean
```

Returns `true` if the input type is the Array type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = Array<String>
output application/json
---
{
   a: isArrayType(AType),
   b: isArrayType(Boolean),
}
```

```json
{
  "a": true,
  "b": false
}
```

## isBinaryType

```
isBinaryType(t: Type): Boolean
```

Returns `true` if the input is the Binary type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ABinary = Binary
output application/json
---
{
   a: isBinaryType(ABinary),
   b: isBinaryType(Binary),
   c: isBinaryType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isBooleanType

```
isBooleanType(t: Type): Boolean
```

Returns `true` if the input is the Boolean type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ABoolean = Boolean
output application/json
---
{
   a: isBooleanType(ABoolean),
   b: isBooleanType(Boolean),
   c: isBooleanType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isDateTimeType

```
isDateTimeType(t: Type): Boolean
```

Returns `true` if the input is the DateTime type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ADateTime = DateTime
output application/json
---
{
   a: isDateTimeType(ADateTime),
   b: isDateTimeType(DateTime),
   c: isDateTimeType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isDateType

```
isDateType(t: Type): Boolean
```

Returns `true` if the input is the Date type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ADate = Date
output application/json
---
{
   a: isDateType(ADate),
   b: isDateType(Date),
   c: isDateType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isFunctionType

```
isFunctionType(t: Type): Boolean
```

Returns `true` if the input is the Function type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AFunction = (String) -> String
output application/json
---
{
   a: isFunctionType(AFunction),
   b: isFunctionType(Boolean)
}
```

```json
{
  "a": true,
  "b": false
}
```

## isIntersectionType

```
isIntersectionType(t: Type): Boolean
```

Returns `true` if the input type is the Intersection type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = {name: String} & {age: Number}
output application/json
---
{
   a: isIntersectionType(AType),
   b: isIntersectionType(Boolean),
}
```

```json
{
  "a": true,
  "b": false
}
```

## isKeyType

```
isKeyType(t: Type): Boolean
```

Returns `true` if the input is the Key type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AKey = Key
output application/json
---
{
   a: isKeyType(AKey),
   b: isKeyType(Key),
   c: isKeyType(Boolean),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isLiteralType

```
isLiteralType(t: Type): Boolean
```

Returns `true` if the input is the Literal type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ALiteralType = "Mariano"
output application/json
---
{
   a: isLiteralType(ALiteralType),
   b: isLiteralType(Boolean)
}
```

```json
{
  "a": true,
  "b": false
}
```

## isLocalDateTimeType

```
isLocalDateTimeType(t: Type): Boolean
```

Returns `true` if the input is the LocalDateTime type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ALocalDateTime = LocalDateTime
output application/json
---
{
   a: isLocalDateTimeType(ALocalDateTime),
   b: isLocalDateTimeType(LocalDateTime),
   c: isLocalDateTimeType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isLocalTimeType

```
isLocalTimeType(t: Type): Boolean
```

Returns `true` if the input is the LocalTime type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ALocalTime = LocalTime
output application/json
---
{
   a: isLocalTimeType(ALocalTime),
   b: isLocalTimeType(LocalTime),
   c: isLocalTimeType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isNamespaceType

```
isNamespaceType(t: Type): Boolean
```

Returns `true` if the input is the Namespace type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ANamespace = Namespace
output application/json
---
{
   a: isNamespaceType(ANamespace),
   b: isNamespaceType(Namespace),
   c: isNamespaceType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isNothingType

```
isNothingType(t: Type): Boolean
```

Returns `true` if the input is the Nothing type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ANothing = Nothing
output application/json
---
{
   a: isNothingType(ANothing),
   b: isNothingType(Nothing),
   c: isNothingType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isNullType

```
isNullType(t: Type): Boolean
```

Returns `true` if the input is the Null type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ANull = Null
output application/json
---
{
   a: isNullType(ANull),
   b: isNullType(Null),
   c: isNullType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isNumberType

```
isNumberType(t: Type): Boolean
```

Returns `true` if the input is the Number type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ANumber = Number
output application/json
---
{
   a: isNumberType(ANumber),
   b: isNumberType(Number),
   c: isNumberType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isObjectType

```
isObjectType(t: Type): Boolean
```

Returns `true` if the input is the Object type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = {name: String}
output application/json
---
{
   a: isObjectType(AType),
   b: isObjectType(Boolean),
}
```

```json
{
  "a": true,
  "b": false
}
```

## isPeriodType

```
isPeriodType(t: Type): Boolean
```

Returns `true` if the input is the Period type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type APeriod = Period
output application/json
---
{
   a: isPeriodType(APeriod),
   b: isPeriodType(Period),
   c: isPeriodType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isRangeType

```
isRangeType(t: Type): Boolean
```

Returns `true` if the input is the Range type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ARange = Range
output application/json
---
{
   a: isRangeType(ARange),
   b: isRangeType(Range),
   c: isRangeType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isReferenceType

```
isReferenceType(t: Type): Boolean
```

Returns `true` if the input type is a Reference type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
output application/json
import * from dw::core::Types
 type AArray = Array<String> {n: 1}
 type AArray2 = Array<AArray>
 ---
 {
     a: isReferenceType( AArray),
     b: isReferenceType(arrayItem(AArray2)),
     c: isReferenceType(String)
 }
```

```json
{
  "a": false,
  "b": true,
  "c": false
}
```

## isRegexType

```
isRegexType(t: Type): Boolean
```

Returns `true` if the input is the Regex type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ARegex = Regex
output application/json
---
{
   a: isRegexType(ARegex),
   b: isRegexType(Regex),
   c: isRegexType(Boolean),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isStringType

```
isStringType(t: Type): Boolean
```

Returns `true` if the input is the String type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AString = String
output application/json
---
{
   a: isStringType(AString),
   b: isStringType(String),
   c: isStringType(Boolean),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isTimeType

```
isTimeType(t: Type): Boolean
```

Returns `true` if the input is the Time type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ATime = Time
output application/json
---
{
   a: isTimeType(ATime),
   b: isTimeType(Time),
   c: isTimeType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isTimeZoneType

```
isTimeZoneType(t: Type): Boolean
```

Returns `true` if the input is the TimeZone type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type ATimeZone = TimeZone
output application/json
---
{
   a: isTimeZoneType(ATimeZone),
   b: isTimeZoneType(TimeZone),
   c: isTimeZoneType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isTypeType

```
isTypeType(t: Type): Boolean
```

Returns `true` if the input is the Type type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = Type
output application/json
---
{
   a: isTypeType(AType),
   b: isTypeType(Type),
   c: isTypeType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## isUnionType

```
isUnionType(t: Type): Boolean
```

Returns `true` if the input type is the Union type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = String | Number
output application/json
---
{
   a: isUnionType(AType),
   b: isUnionType(Boolean),
}
```

```json
{
  "a": true,
  "b": false
}
```

## isUriType

```
isUriType(t: Type): Boolean
```

Returns `true` if the input is the Uri type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AUri = Uri
output application/json
---
{
   a: isUriType(AUri),
   b: isUriType(Uri),
   c: isUriType(String),
}
```

```json
{
  "a": true,
  "b": true,
  "c": false
}
```

## literalValueOf

```
literalValueOf(t: Type): String | Number | Boolean
```

Returns the value of an input belongs to the Literal type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = "Mariano"
output application/json
---
{
   a: literalValueOf(AType)
}
```

```json
{
  "a": "Mariano"
}
```

## metadataOf

```
metadataOf(t: Type): Object
```

Returns metadata that is attached to the given type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = String {format: "YYYY-MM-dd"}
output application/json
---
{
   a: metadataOf(AType)
}
```

```json
{
  "a": {"format": "YYYY-MM-dd"}
}
```

## nameOf

```
nameOf(t: Type): String
```

Returns the name of the input type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to query

```dataweave
%dw 2.0
output application/json
import * from dw::core::Types
type AArray = Array<String> {n: 1}
type AArray2 = Array<String>
---
 {
     a: nameOf(AArray),
     b: nameOf(AArray2),
     c: nameOf(String)
 }
```

```json
{
   "a": "AArray",
   "b": "AArray2",
   "c": "String"
 }
```

## objectFields

```
objectFields(t: Type): Array<Field>
```

Returns the array of fields from the given Object type. This function fails if the type is not an Object type. _Introduced in DataWeave version 2.3.0._

- `t` — The function type.

```dataweave
import * from dw::core::Types
ns ns0 http://acme.com
type ADictionary = {_ : String}
type ASchema = {ns0#name @(ns0#foo: String): {}}
type AUser = {name @(foo?: String,l: Number)?: String, lastName*: Number}
---
{
    a: objectFields(ADictionary),
    b: objectFields(ASchema),
    c: objectFields(Object),
    d: objectFields(AUser)
}
```

```json
{
  "a": [
    {
      "key": {
        "name": {
          "localName": "_",
          "namespace": null
        },
        "attributes": [

        ]
      },
      "required": true,
      "repeated": false,
      "value": "String"
    }
  ],
  "b": [
    {
      "key": {
        "name": {
          "localName": "name",
          "namespace": "http://acme.com"
        },
        "attributes": [
          {
            "name": {
              "localName": "foo",
              "namespace": "http://acme.com"
            },
            "value": "String",
            "required": true
          }
        ]
      },
      "required": true,
      "repeated": false,
      "value": "Object"
    }
  ],
  "c": [

  ],
  "d": [
    {
      "key": {
        "name": {
          "localName": "name",
          "namespace": null
        },
        "attributes": [
          {
            "name": {
              "localName": "foo",
              "namespace": null
            },
            "value": "String",
            "required": false
          },
          {
            "name": {
              "localName": "l",
              "namespace": null
            },
            "value": "Number",
            "required": true
          }
        ]
      },
      "required": false,
      "repeated": false,
      "value": "String"
    },
    {
      "key": {
        "name": {
          "localName": "lastName",
          "namespace": null
        },
        "attributes": [

        ]
      },
      "required": true,
      "repeated": true,
      "value": "Number"
    }
  ]
}
```

## unionItems

```
unionItems(t: Type): Array<Type>
```

Returns an array of all the types that define a given Union type. This function fails if the input is not a Union type. _Introduced in DataWeave version 2.3.0._

- `t` — The type to check.

```dataweave
%dw 2.0
import * from dw::core::Types
type AType = String | Number
output application/json
---
{
   a: unionItems(AType)
}
```

```json
{
  "a": ["String","Number"]
}
```
