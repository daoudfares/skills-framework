# DataWeave selectors

Traversing objects and arrays: single-value, multi-value, descendants, index, range, attribute, namespace, filter and metadata selectors.

## DataWeave Selectors

DataWeave selectors traverse the structures of objects and arrays and
return matching values.

A selector always operates within a context, which can be a reference to
a variable, an object literal, an array literal, or the invocation of a
DataWeave function.

| Selector Type | Syntax | Return Type |
|---|---|---|
| Single-value | `.keyName` | Any type of value that belongs to a matching key |
| Multi-value | `.*keyName` | Array of values of any matching keys |
| Descendants | `..keyName` | Array of values of any matching descendant keys |
| Dynamic | See dynamic selector. |  |
| Key-value pair | `.&keyName` | Object with the matching key |
| Index | `[<index>]` | Value of any type at selected array index. Use negative numbers to index from the end of an array, for example, `-1` for the last element in the array. Use of numbers beyond the array size returns `null`. |
| Range | `[<index> to <index>]` | Array with values from selected indexes |
| XML attribute | `@`, `.@keyName` | String value of the selected attribute |
| Namespace | `keyName.#` | String value of the namespace for the selected key |
| Key present | `keyName?`, `keyName.@type?` | Boolean (`true` if the selected key of an object or XML attribute is present, `false` if not) |
| Assert present | `keyName!` | String: Exception message if the key is not present |
| Filter | `[?(boolean_expression)]` | Array or object containing key-value pairs _if_ the DataWeave expression returns `true`. Otherwise, returns the value `null`. |
| Metadata | `.^someMetadata` |  Returns the value of specified metadata for a Mule payload, variable, or attribute. The selector can return the value of class (`.^class`), content length (`.^contentLength`), encoding (`.^encoding`), mime type (`.^mimeType`), media type (`.^mediaType`), raw  (`.^raw`), and custom (`.^myCustomMetadata`) metadata. For details, see Extract Data. |

The following examples use these selectors. For additional examples of selectors, see
Extract Data.

### Rules for Matching

In DataWeave, a name that matches the key of an object (such as the key
`"someName"` in the JSON object `{ "someName" : "Data Weave" }`) can select
data from that object. For a simple example, see single value selector.

### Single-Value Selector

This selector matches the value of the first key-value pair in which the key
matches the given selector name. The selector can be applied to an Object or
to an array. On an array, the selector applies to all Object values inside the
array and ignores all values that are not Object values. If no key matches,
the value `null` is returned.

For information about the dot selector (`.`) and how to use it on DataWeave types, refer to selecting types.

#### Example: Using a Single-Value Selector on an Object

This example shows how the selector works on a simple JSON object.

##### Input Payload

The input payload is an object with the key `"name"` and the
value `"DataWeave"`:

```json
{ "name": "Data Weave" }
```

##### DataWeave Source

The DataWeave script uses `payload.name` to select the
value of the object that has the key `"name"`.
Note that `payload.name` and `payload."name"` are both valid
ways to perform the selection.

```dataweave
%dw 2.0
output application/json
---
payload.name
```

##### Output

The script outputs the String value of the input object, "Data Weave":

```json
"Data Weave"
```

#### Example: Using a Single-Value Selector on an Array

On an array, the selector applies to every element.

##### Input Payload

The input payload is an array that contains two objects with the same
key, "name":

```json
[
  {
    "name": "Arg"
  },
  {
    "name": "Japan"
  }
]
```

##### DataWeave Source

The DataWeave script uses `payload.name` to select the
value of any objects in input payload that have the key "name":

```dataweave
%dw 2.0
output application/json
---
payload.name
```

##### Output

The script outputs an array that contains the values of the input objects
with the key `"name"`: `"Arg"` and `"Japan"`:

```json
["Arg", "Japan"]
```

### Namespace Selector

The DataWeave namespace selector supports the use of a name that matches a
namespace or a local part. To match a namespace, the name must match the
namespace and the local part. If the name only matches the local part, the
selector matches all namespaces with that local part, regardless of the
namespace.

Note that XML namespaces and their prefixes are defined in the `xmlns` attribute
of an XML element. For example, the element
`<h:table xmlns:h="http://www.w3.org/TR/html4/"/>` defines a namespace that
assigns the prefix `h` to the namespace  `http://www.w3.org/TR/html4/`.
All elements in that namespace contain the `h` prefix. For example, in the
element `<h:table/>`, `h` is the prefix for the namespace, and `table` is the
local part.

#### Example: Using a Namespace Selector

This example selects values from XML elements using the namespace and local part.

##### Input Payload

The input payload contains XML elements, `h:table` and `f:table`, that have
different namespaces but the same local names (`table`):

```xml
<root>

  <h:table xmlns:h="http://www.w3.org/TR/html4/">
    <h:tr>
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
    </h:tr>
  </h:table>

  <f:table xmlns:f="https://www.w3schools.com/furniture">
    <f:tr>
      <f:name>African Coffee Table</f:name>
      <f:width>80</f:width>
      <f:length>120</f:length>
    </f:tr>
  </f:table>

</root>
```

##### DataWeave Source

The DataWeave script selects XML content from specified namespaces. The
script's header creates namespace (`ns`) variables `html` and `furniture`
to store namespaces from the input payload. To select the children of `h:table`
into element `a` and the children of `f:table` elements into element `b`, the
script uses the `html` and `furniture` namespace variables with a
namespace selector (`#`) and local part (`table`):

```dataweave
%dw 2.0
output application/xml
ns html http://www.w3.org/TR/html4/
ns furniture https://www.w3schools.com/furniture
---
root: {
     a: payload.root.html#table,
     b: payload.root.furniture#table
 }
```

##### Output

The script outputs children of the `h:table` element under element `a` and
the children of the `f:table` under element `b`:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<root>
  <a>
    <h:tr xmlns:h="http://www.w3.org/TR/html4/">
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
    </h:tr>
  </a>
  <b>
    <f:tr xmlns:f="https://www.w3schools.com/furniture">
      <f:name>African Coffee Table</f:name>
      <f:width>80</f:width>
      <f:length>120</f:length>
    </f:tr>
  </b>
</root>
```

#### Example: Using a Local Name to Select XML Values

This example selects XML values using a local name `table` from the `h:table`
element.

##### Input Payload

The input payload contains XML with a `table` element that contains
the namespace `"http://www.w3.org/TR/html4/"`:

```xml
<root>
  <h:table xmlns:h="http://www.w3.org/TR/html4/">
    <h:tr>
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
    </h:tr>
  </h:table>
</root>
```

##### DataWeave Source

The DataWeave script selects values of children in the `table` element
by using a local name of the XML element `table` instead of its namespace:

```dataweave
%dw 2.0
output application/xml
---
root: { a: payload.root.table }
```

##### Output

The script outputs XML that contains the values of children in the
`table` element:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<root>
  <a>
    <h:tr xmlns:h="http://www.w3.org/TR/html4/">
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
    </h:tr>
  </a>
</root>
```

### Attribute Selector

The attribute selector returns the first attribute value that matches the
selected name expression. If no key matches, the selection returns the value
`null`.

The following example selects the value of an XML attribute.

#### Input Payload

The input payload is an XML `user` element that contains the attribute
`name="Weave"`:

```xml
<user name="Weave"/>
```

#### DataWeave Source

The DataWeave script selects the value of the `name` attribute
from the input payload (`<user name="Weave"/>`). Notice that the `@`
indicates an attribute selection.

```dataweave
%dw 2.0
output application/json
---
payload.user.@name
```

#### Output

The DataWeave script outputs the value of `name` attribute.

```json
"Weave"
```

### Multi-Value Selector

Instead of returning the value of the first matching key in an array
of objects, the multi-value selector (`*`) returns an array containing
values to the matching key (for example, `*user` where `user` is
the key). The selector does not return the values of descendants,
only those at the specified level. If no key matches, the selection
returns the value `null`.

#### Input Payload

The input payload contains an XML array of `user` elements.

```xml
<users>
  <user>Weave</user>
  <user>BAT</user>
  <user>TF</user>
</users>
```

#### DataWeave Source

The DataWeave script uses `*user` to select the values of
all `user` elements from the input payload.

```dataweave
%dw 2.0
output application/json
---
payload.users.*user
```

#### Output

The script outputs an array of `user` values.

```json
[
  "Weave",
  "BAT",
  "TF"
]
```

### Descendant Selector

The descendant selector returns a list of all children and their descendants.
You can directly chain
this selector to any other selector without using a single `.`. For example,
`payload..` recursively returns an array of all the child values, the values
of _their_ children, and so on. You can also chain the selector to another element
(for example, with `payload..user`) to select the values of each `user` key and
its descendants, or you can use `payload..*name` to select the values
of all `name` descendants.

#### Example: Selecting Each Descendant

This example selects each descendant of the input payload.

##### Input Payload

The input payload contains a set of elements that are nested
at different levels.

```xml
<users>
  <user>
    <name>Weave</name>
    <user>
      <name>BAT</name>
      <user>
        <name>BDD</name>
      </user>
    </user>
  </user>
</users>
```

##### DataWeave Source

The DataWeave script uses `..` to recursively select all elements in
the input payload and return them in a JSON array.

```dataweave
%dw 2.0
output application/json
---
payload..
```

##### Output

```json
[
  {
    "user": {
      "name": "Weave",
      "user": {
        "name": "BAT",
        "user": {
          "name": "BDD"
        }
      }
    }
  },
  {
    "name": "Weave",
    "user": {
      "name": "BAT",
      "user": {
        "name": "BDD"
      }
    }
  },
  "Weave",
  {
    "name": "BAT",
    "user": {
      "name": "BDD"
    }
  },
  "BAT",
  {
    "name": "BDD"
  },
  "BDD"
]
```

#### Example: Selecting Descending Values

This example selects the descending `name` values.

##### Input Payload

The input payload contains a set of `name` elements that are nested
at different levels.

```xml
<users>
  <user>
    <name>Weave</name>
    <user>
      <name>BAT</name>
      <name>Munit</name>
      <user>
        <name>BDD</name>
      </user>
    </user>
  </user>
</users>
```

##### DataWeave Source

The DataWeave script uses `..` to select the values of all first `name` elements
from the input payload and output those values into a JSON array.

```dataweave
%dw 2.0
output application/json
---
payload..name
```

##### Output

The script outputs a JSON array with all `name` values.

```json
[
  "Weave",
  "BAT",
  "BDD"
]
```

#### Example

This example selects the descending `name` values.

##### Input Payload

The input payload contains a set of `name` elements that are nested
at different levels.

```xml
<users>
  <user>
    <name>Weave</name>
    <user>
      <name>BAT</name>
      <name>Munit</name>
      <user>
        <name>BDD</name>
      </user>
    </user>
  </user>
</users>
```

##### DataWeave Source

The DataWeave script uses `..*` to select the values of all `name` elements
from the input payload and output those values into a JSON array, including
the `BAT` and `Munit` values of the repeated `name` keys that are at the same level in the XML hierarchy.

```dataweave
%dw 2.0
output application/json
---
payload..*name
```

##### Output

The script outputs a JSON array with all `name` values.

```json
[
  "Weave",
  "BAT",
  "Munit",
  "BDD"
]
```

#### Example: Selecting Descending Values

This example selects the descending `Name` values of the `Item` elements.

##### Input Payload

The input payload contains a set of `Name` elements that are nested
at different levels.

```xml
<Example>
    <Brand>
        <Id>32345</Id>
        <logo>circle</logo>
        <Item>
            <Name>Perfume</Name>
            <Item>
                <Name>Bosque</Name>
            </Item>
        </Item>
        <Item>
            <Name>t-Shirt</Name>
        </Item>
    </Brand>
    <Brand>
        <Id>435678C</Id>
        <logo>circle</logo>
        <Item>
            <Name>t-Shirt2</Name>
            <Item>
                <Name>t-Shirt red</Name>
                <Item>
                    <Name>t-Shirt red with logo</Name>
                </Item>
            </Item>
        </Item>
    </Brand>
</Example>
```

##### DataWeave Source

The DataWeave script uses `..*` to select the values of all `Name` elements nested in the `Item` elements from the input payload and output those values into a XML array.

```dataweave
%dw 2.0
output application/xml
---
{
    Supermarket: {
        Item: {
            Value: payload..*Item.Name
        }
    }
}
```

##### Output

The script outputs a XML array with all `name` values.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<Supermarket>
  <Item>
    <Value>Perfume</Value>
    <Value>t-Shirt</Value>
    <Value>Bosque</Value>
    <Value>t-Shirt2</Value>
    <Value>t-Shirt red</Value>
    <Value>t-Shirt red with logo</Value>
  </Item>
</Supermarket>
```

### Dynamic Selector

The syntax for dynamic selection depends on what you are selecting:

- Single Value: `payload[(nameExpression)]`
- Multi Value: `payload[*(nameExpression)]`
- Attribute: `payload[@(nameExpression)]`
- Key Value: `payload[&(nameExpression)]`
- Single Value with a Namespace: `payload.ns0#"$(nameExpression)"`

#### Example: Dynamically Selecting a Single Value

This example shows how to dynamically select a single value.

##### Input Payload

The input payload is an array of objects. The first object has the key `"ref"`
and the value `"name"`. The second has the key `"name"` and the value
`"Data Weave"`:

```json
{ "ref": "name", "name": "Data Weave" }
```

##### DataWeave Source

The DataWeave script dynamically selects the value of the `"name"` key:

```dataweave
%dw 2.0
output application/json
---
payload[(payload.ref)]
```

Notice that it passes `payload.ref` within the parentheses of dynamic selector
`[()]`. The script works because the value of `"ref"` is `"name"`, which matches
the key `"name"`.

##### Output

The script outputs the value of the object that has the `"name"` key:

```json
"Data Weave"
```

#### Example: Dynamically Selecting a Single Value with a Namespace

This example shows how to dynamically select a single value that contains
a namespace.

##### Input Payload

The input payload contains a `<root/>` element with two child elements, one of
which has the namespace `http://www.w3.org/TR/html4/`. Both child elements
(`<f:table/>` and `<h:table>`) have the local name `table`:

```xml
<root ref="table">
    <f:table xmlns:f="https://www.w3schools.com/furniture">Manzana</f:table>
    <h:table xmlns:h="http://www.w3.org/TR/html4/">Banana</h:table>
</root>
```

##### DataWeave Source

The DataWeave script dynamically selects the value of the element that has
the namespace `http://www.w3.org/TR/html4/`:

```dataweave
%dw 2.0
output application/json
ns h http://www.w3.org/TR/html4/
---
payload.root.h#"$(payload.root.@ref)"
```

Notice that the expression `payload.root.@ref` uses the attribute selector (`@`)
on the `ref` attribute of the `root` element to select the value `table`,
which matches local name `table` in the element
`<h:table xmlns:h="http://www.w3.org/TR/html4/">Banana</h:table>`.

##### Output

The script outputs the value of the element that has
the namespace `http://www.w3.org/TR/html4/`:

```json
"Banana"
```

### Use of Selectors on Content Stored in Variables

All selectors work with the
predefined Mule Runtime variables and with
DataWeave variables.

To select Mule event data,
such as the payload, an attribute, or variable data within the Mule event,
use predefined Mule Runtime variables, such as `payload`, `attributes`, and `vars`.

Extracted values are handled as literal values of one of the supported DataWeave value types.

| Data to extract | Syntax |
|---|---|
| **Payload** | `payload`, for example: `payload.name` If the `payload` is `{"name" : "somebody"}`, `payload.name` returns `"somebody"`. For more on the Mule payload, see Message Payload. |
| **Attribute** | `attributes.<myAttributeName>` For examples, see Attributes. |
| **Variable** |  `<myVariableName>` To avoid name collisions, you must prepend `vars` to the variable name: `vars.<myVariableName>` For more on Mule variables, see Variables in Mule Apps. |
| **Error object** | `error` For information on errors in the flow, you can use `#[error.cause]`. |
| **Flow** | `flow` For the flow name in the Logger: `#[flow.name]` Note that `flow.name` does not work in some Core components, such as Set Payload and Transform Message. For more on flows, see Flows and Subflows. |

---

## Selecting Types

Using the dot selector (`.`) over DataWeave types enables you to declare new types from existing ones. Combined with the module loader, DataWeave can also load and translate declarations from a custom module file into DataWeave type directives that can be accessed in the same way as types from any other DataWeave module.

### Declare a New Type from an Existing Type

The following example declares the `NameType` from the `User` type. Using the dot selector in `User.name` to declare the `name` variable as `NameType` enables the `typeOf()` function to return the primitive type, `"String"`. The DataWeave variable `name` is declared as a `NameType` value "Seba":

**DataWeave script:**

```dataweave
%dw 2.0
type User = {name: String}
type NameType = User.name
var name: NameType = "Seba"
---
typeOf(name)
```

**Output:**

```text
"String"
```

### Compose a Type from an Existing Type's Field

The following example uses the dot selector (`.`) to declare a new type `Address` from one key in the complex type `User`:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
type User = {
 address : {country: String, city: String, street: String, number: Number},
 userName : String
}
type Address = User.address

var userAddress: Address = {country: "Argentina", city: "Rosario", street: "Calle Falsa", number: 123}
---
userAddress
```

**Output:**

```json
{
 "country": "Argentina",
 "city": "Rosario",
 "street": "Calle Falsa",
 "number": 123
}
```

### Select Types from Union Types

The following example shows how you can use type selection with `Union` types that consist of `Object` types:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
type ID = {id: String, firstName: String, age: Number} | {id: Number, firstName: String, secondName: String}

var nameAge: ID = {firstName: "Seba", id: "123", age: 28}
var fullName: ID = {id: 38123, firstName: "Seba", secondName: "Elizalde"}

var nameString: ID.firstName = "Seba"
var idNumber: ID.id = 38123
---
[nameAge, fullName, nameString ++ " is of type " ++ typeOf(nameString), idNumber ++ " is of type " ++ typeOf(idNumber)]
```

**Output:**

```json
[
  {
    "firstName": "Seba",
    "id": "123",
    "age": 28
  },
  {
    "id": 38123,
    "firstName": "Seba",
    "secondName": "Elizalde"
  },
  "Seba is of type String",
  "38123 is of type Number"
]
```

The following script fails because the second type is not an `Object` type and there is no way to reference it with the selector:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
type UnionType = {name: String} | Number
type Fail = UnionType.name
---
{}
```

**Output:**

```json
Cannot do selection on Type: Number

4| type Fail = UnionType.name
```

### Select Types from Namespaces

The following example shows type selection of a namespace:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
ns ns1 http://acme.com
type User = {
 ns1#name : String,
 name : Number,
}
var nameString: User.ns1#name = "Seba"
var nameNumber: User.name = 123
---
{
   "NameString" : typeOf(nameString),
   "NameNumber" : typeOf(nameNumber)
}
```

**Output:**

```json
{
 "NameString": "String",
 "NameNumber": "Number"
}
```

### Select Types with Type Parameters

This example shows how type selection works with type parameters, which are similar to generics in other programming languages:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
type WithParameters<A, B> = {first: A, second: B, nestedObject: {message: A}}
---
{
 a: true is WithParameters<Boolean, Number>.first,
 b: 4592 is WithParameters<String, Number>.second,
 c: "sdf" is WithParameters<String, Number>.nestedObject.message,
}
```

**Output:**

```json
{
  "a": true,
  "b": true,
  "c": true
}
```

### Preserve Metadata of a Type

This example shows that type selection preserves metadata associated with the type:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
type User = {
 birthDate: Date {format: "dd-MMM-yy"},
 userName : String {schema: "value"}
}
type FormattedDate = User.birthDate
type UserName = User.userName
var formattedDate: FormattedDate = "10-SEP-15" as Date {format: "dd-MMM-yy"}
var otherFormatDate = "23-10-2022" as Date {format: "dd-MM-yyyy"}
var userName = "Messi" as String {schema: "value"}
var otherUserName = "Di María" as String {schema: "otherValue"}
---
{
formattedDate: formattedDate is FormattedDate,
userName: userName is UserName,
otherFormatDate: otherFormatDate is FormattedDate,
otherUserName: otherUserName is UserName
}
```

**Output:**

```json
{
 "formattedDate": true,
 "userName": true,
 "otherFormatDate": false,
 "otherUserName": false
}
```
