# DataWeave type system

Built-in types, the type system, and coercion rules.

## Value Constructs for Types

DataWeave represents data using values, each of which has a data type associated with it. There are many types, such as strings, arrays, Booleans, numbers, objects, dates, times, and others. Each type supports several ways of creating its values. This topic explores many of the ways you can create them.

The types that DataWeave provide are bundled into modules that also contain the related functions.

Types in the `dw::Core` module (Core types) are available without having to import the Core module. Other modules need to be imported for their functions and types to be available.

It is important for you to know the values that are possible for each DataWeave type, how to create those values, and the common patterns used:

- Conditional elements that use `if` expressions for arrays and objects.
- string interpolation
- date decomposition for accessing different parts of a date
- date format
- dynamic keys and dynamic elements, which allow you to access parts of an object dynamically
- Use of dw type regex expressions

### Array (dw::Core Type)

An array can hold elements of any supported type. Here is an example of an array:

**Example: DataWeave Array**

```dataweave
%dw 2.0
output application/json
var x = "words"
---
[ "My", "three", x ]
```

#### Conditional Elements

Arrays can define elements that appear (or not) based on a condition.

Conditional elements take the form `(value) if condition`, for example:

**Example: if Condition**

```dataweave
%dw 2.0
output application/json
---
[(1) if true, (2) if false]
```

**Output**

```json
[1]
```

### Boolean (dw::Core Type)

A `Boolean` is defined by the keywords `true` and `false`.

### CData (dw::Core Type)

XML defines a custom type named `CData`, which inherits from and extends `String`. It is used to identify a CDATA XML block. It can be used to tell the writer to wrap the content inside CDATA or to check if the input string arrives inside a CDATA block.

**Transform**

```dataweave
%dw 2.0
output application/xml encoding="UTF-8"
---
{
  users:
  {
    user : "Mariano" as CData,
    age : 31 as CData
  }
}
```

**Output**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<users>
  <user><![CDATA[Mariano]]></user>
  <age><![CDATA[31]]></age>
</users>
```

### Date and Time (dw::Core Types)

Dates in DataWeave follow the ISO-8601 standard and literals are defined between `|` characters.

The language has the following native date types:

- `Date`
- `DateTime`
- `LocalDateTime`
- `LocalTime`
- `Period`
- `Time`
- `TimeZone`

#### Date

A `Date` represented by `Year`, `Month`, and `Day`, specified as `|uuuu-MM-dd|`. The `Date` type has no time component.

**Example**

```dataweave
|2003-10-01|
```

#### DateTime

A Date and Time within a TimeZone. It is the conjunction of `Date` + `Time` + `TimeZone`.

**Example**

```dataweave
|2003-10-01T23:57:59-03:00|
```

#### LocalDateTime

A `DateTime` in the current `TimeZone`.

**Example**

```dataweave
|2003-10-01T23:57:59|
```

#### LocalTime

A `Time` in the current `TimeZone`.

#### Period

`Period` represents an amount of time. The type takes the following form:

- `P[n]Y[n]M[n]DT[n]H[n]M[n]S`
- `P<date>T<time>``

Where the [n] is replaced by the value for each of the date and time elements that follow the [n].

`Period` has two subcategories:

- `DatePeriod` +
 A date-based amount of time, for example, 1 year, 2 months, 3 days. Because these expressions are date-based, they cannot be converted to milliseconds. For example, a month does not specify whether it is a month of 31 days or not, nor does a year specify whether it is a leap year. The data expresses just an amount of date. In DataWeave, the syntax is `|P1Y|`.

- `Duration` +
A time-based amount of time, for example, 1 second, 2 hours, or 2 days, each of which can be represented in seconds or milliseconds. In DataWeave, the syntax is `|PT1H|`.

`P` is the duration designator placed at the start of the duration representation.

- `Y` is the year designator (e.g. `|P1Y|`)
- `M` is the month designator (e.g. `|P1M|`)
- `D` is the day designator (e.g. `|P1D|`)

`T` is the time designator that precedes the time components of the representation.

- `H` is the hour designator (e.g. `|PT1H|`)
- `M` is the minute designator (e.g. `|PT1M|`)
- `S` is the second designator (e.g. `|PT1S|`)

`DatePeriod` is useful for date manipulation, such as addition or subtraction. +
The following example shows how to subtract one year from a date using `DatePeriod`. The return type is a new `Date` value:

**Source**

```dataweave
output application/dw
---
|2003-10-01| - |P1Y|
```

**Output**

```dataweave
|2002-10-01|
```

`Duration` is useful as a result of a `Date` to `Date` subtraction so the amount of time between those two dates can be inferred. +
The following example shows how subtracting one `Date` value from another returns a `Duration` value:

**Source**

```dataweave
output application/dw
---
|2003-11-01| - |2003-10-01|
```

**Output**

```dataweave
|PT744H|
```

##### Period Coercion

Because a `DatePeriod` value is date-based, it can be coerced to `Number` date-based units, such as `years` or `months`. +
The following example shows how to coerce a `DatePeriod` value to a `Number` value by using different units:

**Source**

```dataweave
output application/json
---
{
 years:  |P1Y12M| as Number {unit: "years"},
 months: |P8Y12M| as Number {unit: "months"}
}
```

**Output**

```json
{
  "years": 2,
  "months": 108
}
```

##### Duration Coercion

Because `Duration` is time-based, this type can be coerced to a `Number` with different time-based units, such as `nanos`, `milliseconds`, `seconds`, `hours`, and `days`.

The following example shows how to coerce a `Duration` to a `Number` by using different units:

**Source**

```dataweave
output application/json
var period = (|2010-12-10T12:10:12| - |2010-09-09T10:02:10|)
---
{
 nanos: period as Number {unit: "nanos"},
 millis: period as Number {unit: "milliseconds"},
 seconds: period as Number {unit: "seconds"},
 hours: period as Number {unit: "hours"},
 days: period as Number {unit: "days"}
}
```

**Output**

```json
{
  "nanos": 7956482000000000,
  "millis": 7956482000,
  "seconds": 7956482,
  "hours": 2210,
  "days": 92
}
```

##### Deconstruct

A `Duration` can be deconstructed into `hours`, `minutes` and `secs`.

The following example shows how to deconstruct a `Duration` value:

**Source**

```dataweave
%dw 2.0
output application/json
var period = (|2010-12-10T12:10:12| - |2010-12-10T10:02:10|)
---
{
   hours:  period.hours,
   minutes:  period.minutes,
   secs:  period.secs,
}
```

**Output**

```json
{
  "hours": 2,
  "minutes": 8,
  "secs": 2
}
```

#### Time

A time in a specific `TimeZone`, specified as `|HH:mm:ss.SSS|`.

**Example**

```dataweave
|23:59:56|
```

#### TimeZone

The `Time` relative to Greenwich Mean Time (GMT). A `TimeZone` must include a `+` or a `-`. For example, `|03:00|` is a time, while `|+03:00|` is a `TimeZone`.

**Example**

```dataweave
|-08:00|
```

#### Date Decomposition

To access the different parts of the date, special selectors must be used.

**Transform**

```dataweave
%dw 2.0
output application/json
var myDate = |2003-10-01T23:57:59.700-03:00|
---
{
  year: myDate.year,
  month: myDate.month,
  day: myDate.day,
  hour: myDate.hour,
  minutes: myDate.minutes,
  seconds: myDate.seconds,
  milliseconds: myDate.milliseconds,
  nanoseconds: myDate.nanoseconds,
  quarter: myDate.quarter,
  dayOfWeek: myDate.dayOfWeek,
  dayOfYear: myDate.dayOfYear,
  offsetSeconds: myDate.offsetSeconds
}
```

**Output**

```json
{
  "year": 2003,
  "month": 10,
  "day": 1,
  "hour": 23,
  "minutes": 57,
  "seconds": 59,
  "milliseconds": 700,
  "nanoseconds": 700000000,
  "quarter": 4,
  "dayOfWeek": 3,
  "dayOfYear": 274,
  "offsetSeconds": -10800
}
```

#### Date and Time Formats

To enable you to format dates and times, DataWeave supports formatting characters, such as the `u` (for the year), `M`, and `d` in the date format `uuuu-MM-dd`. These characters are based on the Java 8 `java.time.format` package.

For examples, see Format Dates and Times.

#### Timezone IDs

In addition to accepting time zone values, such as `-07:00`, DataWeave also accepts IDs such as `America/Buenos_Aires`, `America/Los_Angeles`, `Asia/Tokyo`, and `GMT`.

For examples and a list of supported IDs, see Time Zone IDs and Change a Time Zone.

### Enum (dw::Core Type)

This type is based on the Enum Java class.
It must always be used with the `class` property, specifying the full Java class name of the class, as shown in this example.

**Transform**

```dataweave
%dw 2.0
output application/java
---
"Male" as Enum {class: "com.acme.GenderEnum"}
```

### Iterator (dw::Core Type)

The `Iterator` type is based on the Iterator Java class, that iterates through arrays. `Iterator` contains a collection and includes methods to iterate through and filter it.

Note that like the Java class, the iterator is designed to be consumed only once. For example, if a logger consumes the value, the value is no longer readable by subsequent elements in the flow.

### Null (dw::Core Type)

DataWeave defines a `Null` data type for `null` values. It is important to note that `null`
is the value, while `Null` is the type. DataWeave functions do not recognize `Null` as
a `null` value.

You can determine whether a DataWeave function accepts `null` values by
looking in the DataWeave reference documentation for a function signature
that accepts a Null type. For example, the
flatten function has two function
signatures, one of which is `flatten(Null): Null`. The signature indicates that
`flatten` can accept `null` values. The ++
(concatenate) function, which lacks a signature for handling value so the `Null`
type, does not accept `null`.

- `flatten([[1],2,[null],null])` returns `[1,2,null,null]`
- `"a" ++ null` returns the error
`Unable to call `` with (`String`, `Null`)`.

### Number (dw::Core Type)

There is only one Number type that supports both floating point and integer numbers. There is no loss of precision in any operation, the engine always stores the data in the most performant way that does not compromise precision.

DataWeave provides a mechanism for formatting numeric values and for coercing dates and strings to numbers. The language also provides operators that act on numeric values and includes many functions that take numeric values as arguments.

- Type Coercion with DataWeave shows how to format a number.
- mapObject provides an example that coerces a string to a number and formats the number.
- period coercion and duration coercion include date coercion examples.
- Operators describes operators that act on numeric values.
- avg is one of many DataWeave functions that accepts a numeric value. The `Number` type appears in its function signature, `avg(Array<Number>): Number`, which indicates that the function accepts an array of numeric values and returns a numeric value.
- The Numbers module provides helper functions that work on numbers.

### Object (dw::Core Type)

Represents any object as a collection of `Key:value` pairs, where a `Key` is
composed of a `Name` and `Attributes`.

The `Name` type is composed of a `String` as the local name and the `Namespace`.
`Attributes` is composed of an Array of `Name:value` pairs. Note that the `Key`
is not a `String`, so it is not possible to compare keys. However, you can get
the local name by performing an `as String` type coercion on any value of type
`Key`.

**Example**

```dataweave
%dw 2.0
output application/json
---
{
  name: "Annie"
}
```

#### Single Value Objects

If an object has only one `key:value` pair, the enclosing curly braces `{ }` are not required:

**Example**

```dataweave
%dw 2.0
output application/json
---
name: "Annie"
```

#### Conditional Elements

Objects can define conditional key-value pairs based on a conditional expression. Conditional elements have the form `(key:value) if` condition.

```dataweave
%dw 2.0
output application/xml encoding="UTF-8"
---
file: {
  name: "transform",
  (extension: "zip") if payload.fileSystem?
}
```

This example outputs an additional field called "extension" only when the fileSystem property is present in payload (this field may contain any value, not just `true`).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<file>
  <name>transform</name>
  <extension>zip</extension>
</file>
```

If absent:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<file>
  <name>transform</name>
</file>
```

#### Dynamic Keys

To specify a key through an expression, you need to wrap the expression in parentheses.

**Transform**

```dataweave
%dw 2.0
output application/json
var dynamicKey = "language"
---
{
  (dynamicKey): "Data Weave"
}
```

**Output**

```json
{
  "language": "Data Weave"
}
```

#### Dynamic Elements

Dynamic elements allow you to add the result of an expression as `key:value` pairs of an object. That expression must be either an `object` or an `array of objects`.

**Transform**

```dataweave
%dw 2.0
output application/json
var x = [
  {b: "b"},
  {c: "c", d: "d"}
]
var y = {e: "e"}
---
{
  a: "a",
  (x),
  (y)
}
```

The _evaluation parentheses_ around the variables in the body of the script above (`(x)` and `(y)`) enable the object constructor curly braces (`{ }`) surrounding the body of the script to act on the values of the variables. Specifically, the object constructor curly braces extract the key-value pairs from the values of `x` and `y` and convert them into a collection of key-value pairs within an object. Without the parentheses (for example, if you use `x` instead of `(x)`), the script returns an error.

The object constructor curly braces require a data construct that contains one or more key-value pairs, specifically an object, such as `{ "a":"one", "b":"two"}`, or an array of objects, such as `[{"a":"one"},{"b":"two"}]` so that it can produce a valid object. Because the first element within the object constructor curly braces is the key-value pair `a: "a"`, the object constructor curly braces leave the pair as the first element in the output object, without any modifications. However, the object constructor curly braces extract the outer-level key-value pairs in the evaluated expressions `(x)` and `(y)` and append those key-value pairs to the output object.

**Output**

```json
{
  "a": "a",
  "b": "b",
  "c": "c",
  "d": "d",
  "e": "e"
}
```

#### Conditional XML Attributes

You might want your output to only include certain XML attributes based on a condition. Conditional elements have the form `(key:value) if condition`

**Transform**

```dataweave
%dw 2.0
output application/xml
---
{
  name @(
    (company: "Acme") if false,
    (transform: "Anything") if true
  ): "DataWeave"
}
```

**Output**

```xml
<?xml version='1.0' encoding='US-ASCII'?>
<name transform="Anything">DataWeave</name>
```

#### Dynamic XML Attributes

You might want to include a changing set of key:value pairs in a specific location as XML attributes.

**Input**

```json
{
  "company": "Mule",
  "product": "DataWeave"
}
```

**Transform**

```dataweave
%dw 2.0
output application/xml
---
transformation @((payload)): "Transform from anything to anything"
```

**Output**

```xml
<?xml version='1.0' encoding='US-ASCII'?>
<transformation company="Mule" product="DataWeave">Transform from anything to anything</transformation>
```

### Regex (dw::Core Type)

Regular Expressions are defined between `/`. For example `/\d+/` represents multiple numerical digits from 0-9. These may be used as arguments in certain operations that act upon strings, like Matches or Replace, or on operations that act upon objects and arrays, such as filters.

### String (dw::Core Type)

A string can be defined by the use of double quotes or single quotes.

```dataweave
{
  doubleQuoted: "Hello",
  singleQuoted: 'Hello',
}
```

#### Escaping Special Characters

Use the backslash (`\`) to escape special characters in an input string:

- `$`: You need to escape any use of `$` in a string. Otherwise, DataWeave
treats the `$` as an unnamed parameter for a function and returns the error
`Unable to resolve reference of $.`.
- `"`: For a string that is surrounded by double quotes, you need to escape any
double quote that is part of the string, for example, `"a\"bcdef"`. Here, the
second double-quote is part of the string that starts with an `a` and ends
with `f`.
- `'` For a string that is surrounded by single quotes, you need to escape any
single quote that is part of the string: for example, `'abcd\'e"f'`. In this example, the
second single quote is part of the string that starts with an `a` and ends
with `f`. Notice that you do not need to escape the double quote in this case.
- `\``: For a string that is surrounded by backticks, you must escape any backtick that is part of the string: for example, ``abc\`def``.
- `\`: Because the backslash is the character you use to escape other special
characters, you need to escape it with a separate backslash to use it in
a string, for example,`\\`.
- `\n`: For inserting a new line.
- `\t`: For inserting a tab.
- `\u`: For inserting a unicode character, such as `\u25c4`.

#### String Interpolation

String interpolation allows you to embed variables or expressions directly in a string. The expression need to be enclosed (`$( <expression> )`), and it should always return String type or something that is coercible to String.

```dataweave
%dw 2.0
output application/json
var name = "Shoki"
---
{
    Greeting: "Hi, my name is $name",
    Sum: "1 + 1 = $(1 + 1)"
}
```

**Output**

```json
{
  "Greeting": "Hi, my name is Shoki",
  "Sum": "1 + 1 = 2"
}
```

### TryResult (dw::Runtime Type)

Evaluates the delegate and returns an object with the result or an error message. See the `try` example. A successful `TryResult` contains the `result` field and a `success` value of `true`. An unsuccessful `TryResult` contains the `error` field  and a `success` value of `false`.

**Definition**

```dataweave
{
  success: Boolean,
  result?: T,
  error?: {
    kind: String,
    message: String,
    stack?: Array<String>,
    location?: String
  }
}
```

### URI Types (dw::core::URL)

Functions in the URI function module can return a URI data type.

**Definition:**

```dataweave
{
  isValid: Boolean,
  host?: String,
  authority?: String,
  fragment?: String,
  path?: String,
  port?: Number,
  query?: String,
  scheme?: String,
  user?: String,
  isAbsolute?: Boolean,
  isOpaque?: Boolean
}
```

The URI type consists of the following fields:

- `isValid`: Boolean that indicates whether the URI is valid. Invalid characters
   include `<`, `>`, and blank spaces.
- `host`: String representing the host name (for example,
  `my.company.com` from `http://my.company.com:8080/hello`)
- `authority`: String representing the authority, which includes the host
   and port (for example, `my.company.com:8080` from
  `http://my.company.com:8080/hello`). Returns the port only if it is
  explicitly specified in the URI.
- `fragment`: String representing the subordinate resource after the `#` in
              the URI (for example, `footer` in the URI
              `"https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#footer"`).
- `path`: String representing a path following the host or authority (for example,
          `/hello` in `http://my.company.com:8080/hello`) .
- `port`: Number representing an explicit port in the URI (for example, `8080`
          in `http://my.company.com:8080/hello`). If no port is specified
          (for example, `http://my.company.com/hello`), the value of the
          `port` field is `null`.
- `query`: String identifying a query portion of a URI (for example,
           `field=value` in '+http://my.company.com:1234/hello/?field=value+').
- `scheme`: String identifying the URI scheme, such as `https` or `http`,
            which appears before a colon (`:`).
- `user`: String representing user information in a URI (for example, the
          `myname` in `http://myname@www.mycompany.com`).
- `isAbsolute`: Boolean value of `true` if the URI contains a scheme,
                `false` if the URI does not (for example, a relative URI such as
                `/path/to/somewhere`).
- `isOpaque`: Boolean value of `true` if the URI lacks a scheme followed by
              forward slashes (`/`).
              `mailto:somebody@somewhere.com` returns `true`.

The following DataWeave script uses the `parseURI` function to return and
access values to fields from a URI type. Note that fields with `null`
values (for example, the URI defined by `uriDataTypeEx`) are not returned
unless you explicitly select them.

**DataWeave Script**

```dataweave
%dw 2.0
import * from dw::core::URL
var uriDataTypeEx = "https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#footer"
var queryStringsEx = 'http://my.company.com:1234/hello/?field=value'
output application/json
---
{
    'myUriDataTypeEx': parseURI(uriDataTypeEx),
    // queryStringsEx has a query string:
    'myQueryStringsEx': parseURI(queryStringsEx).query,
    // uriDataTypeEx lacks a query string:
    'myQueryStringNullEx': parseURI(uriDataTypeEx).query,
    // The URI includes the port number:
    'myAuthorityEx': parseURI('http://localhost:8080/test').authority
}
```

**Output**

```json
{
  "myUriDataTypeEx": {
    "isValid": true,
    "raw": "https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#footer",
    "host": "en.wikipedia.org",
    "authority": "en.wikipedia.org",
    "fragment": "footer",
    "path": "/wiki/Uniform_Resource_Identifier",
    "scheme": "https",
    "isAbsolute": true,
    "isOpaque": false
  },
  "myQueryStringsEx": "field=value",
  "myQueryStringNullEx": null,
  "myAuthorityEx": "localhost:8080"
}
```

### DataWeave Type References

You can find more data type documentation in the reference pages for the
DataWeave function modules:

 * Core Types (dw::Core)
 * Coercions Types (dw::util::Coercions)
 * DataFormat Types (dw::extension::DataFormat)
 * Dates Types (dw::core::Dates)
 * Diff Types (dw::core::Diff)
 * Mule Types (Mule)
 * Multipart Types (dw::module::Multipart)
 * Runtime Types (dw::Runtime)
 * Timer Types (dw::core::Timer)
 * Tree Types (dw::util::Tree)
 * Types Types (dw::core::Types)
 * URL Types (dw::core::URL)
 * Values Types (dw::util::Values)

### See Also

- DataWeave Scripts

- Anypoint Exchange (List of Projects that use DataWeave)

---

## Type System

2.x versions of DataWeave support a type system. To take advantage of the type-checking that the type system executes, you need to provide constraint expressions for variables and functions described in this section. For information about how values for these types are defined, refer to Value Constructs for Types.

A type system defines a set of constraints to a set of constructs, such as:

- Variables
- Function parameters

These constraints are used in the type-checking phase, when DataWeave ensures that the values assigned
to variables or the arguments for a function call respect its constraints, for example:

**DataWeave Script:**

```text
%dw 2.0
import * from dw::core::Strings
output application/json

var userName: String = "John"
```

The variable definition for `userName` has the constraint of assigning a value of type `String`.
If some other value type is assigned, a type-checking error is raised.

**DataWeave Script:**

```text
%dw 2.0
import * from dw::core::Strings
output application/json

fun toUser(id: Number, userName: String): String = "you called the function toUser!"
```

The constraints to call the function `toUser` are that the first argument has to be of type `Number`, the second one of type `String` (to be coercible to those types). Another constraint is that the result of the function has to be of type `String`. This constraint isn't used in the call for `toUser`; it's applied to its definition to validate that the function body generates the proper type.

```text
toUser(123, "John")
toUser("123", true)
```

Although you might expect the second call to fail, autocoercion enables the call to be successful, and both calls work. In the case of the second function call, there is autocoercion of the `String` value `"123"` to the `Number` value `123`, and the `Boolean` value `true` to the `String` value `"true"`, which makes it possible to call the function. +
An example of a call that throws a type-checking error is `toUser("a 12", "John")`, because the String value `"a 12"` isn't coercible to a `Number` type. +

DataWeave also uses a global type inference algorithm to validate your code even if no types are specified as
constraints.

Although the use of constraints is optional, they can be useful in big scripts or multiple scripts. The type system helps you to avoid bugs in your DataWeave logic because it causes the type-checking algorithm to run. Additionally, when you write your script in an IDE and define these constraints, the tooling helps you to find type checking errors, instead of when the script is running and fails.

The types supported by the DataWeave type system are divided into three categories:

- Simple Types
- Composite Types
- Complex Types

### Simple Types

Simple types represent values such as strings, Booleans, and so on. These values are atomic; they are not composed of other values. These are the simple types:

- `String`
- `Boolean`
- `Number`
- `Regex`
- `Null`
- Temporal: `Date`, `DateTime`, `LocalDateTime`, `LocalTime`, `Time`, `Period`

#### Null

`Null` is a type of only one value, the value `null`, which means that `null` cannot be assigned to the type `String` or any other type except for the type `Null`.

For example, the `repeat` function in the String module has the signature `repeat(String, Number): String`, which means that the function accepts as a first parameter only a value of type `String`, and as a second parameter only a value of type `Number.` The function returns a value of type `String`.

**DataWeave Script:**

```text
%dw 2.0
import * from dw::core::Strings
output application/json
---
repeat("a", 3)
```

This returns `"aaa"`, but the following example throws an error because the value `null` cannot be assigned to the parameter that expects a value of type `String`:

**DataWeave Script:**

```text
%dw 2.0
import * from dw::core::Strings
output application/json
---
repeat(null, 3)
```

In the following example, the script assigns to the first parameter a value that is the type `Null` (the type of this value is `Type<Null>`). It returns `"NullNullNull"` because autocoercion coerces the value to the type `String` (`"Null"`).

**DataWeave Script:**

```text
%dw 2.0
import * from dw::core::Strings
output application/json
---
repeat(Null, 3)
```

Some functions have an overloaded signature (the function has multiple definitions for different parameter types) that let you call it with `null`.

For example, the `isNumeric` function from `dw::core::Strings` has the signature `isNumeric(String): Boolean`, which receives a string and successfully returns a result if that string is numeric, but the function is also defined as `isNumeric(Null): Boolean`. +

So, if you call the function `isNumeric` with `null` (`isNumeric(null)`), the function does not throw an exception. At runtime, the function that is dispatching algorithm selects the correct function based on the types of the values you use. The function returns `false` because of the definition of `isNumeric` for `null` as the argument.

### Composite Types

A composite type contains other values. The composite types are `Array`, `Object` and `Function`.

#### Array Type

An  array is of the type `Array<T>` in which `T` is a type parameter that defines the type of the elements inside the array. For example, the syntax to define a variable with the type `Array` of `Number` is:

```text
var idsList: Array<Number> = [1, 22, 333, 4444]
```

The variable `idsList` passes the type-checking phase only when the array that is assigned to it only contains values of the `Number` type.

#### Object Type

You can define an `Object` type in two ways: `Object` or `{}`. Both define an open object and don't specify any constraint to their key-value pairs. See also close open objects.

The syntax for defining an `Object` type with a set of constraints for its key-value pairs is very similar to the syntax for defining the value of an `Object` type:

```text
{
    keyName @(attrName: AttrType): valueType,
    ...
}
```

For example, the syntax to define a `User` type with `firstName` `String`, `lastName` `String`, and `age` `Number` is:

**DataWeave Script:**

```text
%dw 2.0
output application/json

type User = {
    firstName: String,
    lastName: String,
    age: Number
}
```

You can apply modifiers to each key-value pair to specify when a field is always present or when a field can be repeated.

For repeated fields use `*`. For example, the following type allows you to have multiple `lastName` fields:

**DataWeave Script:**

```text
%dw 2.0
output application/json

type User = {
    firstName: String,
    lastName*: String,
    age: Number
}
```

For conditional fields, use `?`. For example, the following type allows the `age` field to be present or not:

**DataWeave Script:**

```text
%dw 2.0
output application/json

type User = {
    firstName: String,
    lastName*: String,
    age?: Number
}
```

##### Close and Open Objects

`Object` type can be either closed or open. A _closed_ object accepts an object value only if there are no fields except the key-value pairs specified by the type.

An _open_ object only put constraints on the fields that are declared in the type, and if they are all verified, then the type accepts the value. The type accepts objects that have other fields apart of the ones mentioned in the declaration. All `object` types are open unless specified.

The following example succeeds even if `age` is not in the type declaration because the type of the variable `user` is an open object:

**DataWeave Script:**

```text
%dw 2.0
output application/json

var user: {firstName: String, lastName: String} = {firstName: "John", lastName: "Smith", age: 34}
```

The syntax to specify a closed object is `{| |}`. The following example makes the `User` type support only the keys `firstName` and `lastName`. The script throws an exception because the `age` field is not accepted.

**DataWeave Script:**

```text
%dw 2.0
output application/json

var user: {|firstName: String, lastName: String|} = {firstName: "John", lastName: "Smith", age: 34}
```

#### Function Type

DataWeave is a functional language, and functions are considered first class citizens, which means that functions are values with associated types.

The syntax to define a function type is:

```text
(paramType: ParamType,...) -> ReturnType
```

For example, if you want to define in a constraint a `Function` type that has a parameter of type `String`, a second parameter of type `Number`, and a `Boolean` return value, the correct syntax is:

```text
(paramA: String, paramB: Number) -> Boolean
```

In the following example, you define a function that receives another function as an argument:

**DataWeave Script:**

```text
%dw 2.0
output application/json

fun applyIDsChange(ids: Array<Number>, changeTo: (Number) -> Number): Array<Number> = ???
```

If you call the function `applyIDsChange` with a function that does not match the `changeTo` constraint `(Number) -> Number`, DataWeave throws a type-checking error. +

For example, the following call works because `abs` is a function that takes a value of the `Number` type and returns a `Number`, which matches the `changeTo` parameter:

```text
applyIDsChange([1,-6, 3, -8], abs)
```

But the following call fails because `sum` is a function that takes an `Array` and returns a `Number`, so it does not match the parameter constraint:

```text
applyIDsChange([1,-6, 3, -8], sum)
```

### Complex Types

Complex types include the `Any` and `Nothing` types, the `Union` type, the `Intersection` type, and `Literal` types, each of which is named intuitively.

#### Any and Nothing

In some cases, you cannot enforce a restriction because the type accepts all the value: +

- `Any` type accepts all possible values.
- `Nothing` type accepts no value, but it can be assigned to all the types. This type is not frequently used explicitly, but it is used by the type inference algorithm.

#### Union Type

The `Union` type is used to compose types. The syntax to define a `Union` type is:

```text
TypeA | TypeB | ...
```

The following example defines a variable with a constraint that accepts a value of type `String` or `Number`:

```text
var age: String | Number = if (payload.allStrings) "32" else 32
```

A common pattern is to use `Null` type with a `Union` type to specify that a type accepts `null` as a value. In the following example, the function `parseEmail` allows inputs of type `String` or `Null`. In this case, you can have a object with a payload optional field `email` and you call the function with `payload.email`.

```text
fun parseEmail(email: String | Null) = "Code that handles email being of type String or Null"
```

#### Intersection Type

_Introduced in DataWeave 2.3.0. Supported by Mule 4.3 and later._

The `Intersection` type intersects `Object` types. In this case, the intersection works as the concatenation (``) of object types.

The syntax for the `Intersection` type is:
```text
TypeA & TypeB & ...
```

In the following example, the `Intersection` concatenates the two `Object` types, resulting in the type `{name: String, lastName: String}`. The type is an open object that can accept additional key-value pairs. The variable accepts the value assigned to it:

```text
var a: {name: String} & {lastName: String} = {name: "John", lastName: "Smith", age: 34}
```

In the case of closed objects, it returns the concatenation of the object types but results in a closed object. +
In the following example, the intersection results in the type `{|name: String, lastName: String|}`, which throws
an exception because a closed object does not accept an `Object` value if there are additional fields in the object (field `age`):

```text
var a: {|name: String|} & {|lastName: String|} = {name: "John", lastName: "Smith", age: 34}
```

#### Literal Types

_Introduced in DataWeave 2.3.0. Supported by Mule 4.3 and later._

A literal type represents exactly one value. For example, the `String` value `"foo"` can be represented with the type `"foo"`.

The following literal types are included to the type system:

- `String` literal types
- `Number` literal types
- `Boolean` literal types

You can use literal types with `Union` types to declare a type as a finite set of allowed values. For example, the following type declarations are aliases of `Union` and literal types:

```text
type Weekdays = "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday"
type Days = Weekdays | "Saturday" | "Sunday"
```

In the following example, the variable accepts only a value of the literal types `404` and `500`. The type system ensures before runtime that the variable can be only one of those literal values:

**DataWeave Script:**

```text
%dw 2.0
output application/json

var errorStatusCode: 404 | 500 = payload.statusCode match {
    case "error 404" -> 404
    case "error 500" -> 500
}
```

Function overloading enables you to define different behaviors based on the input argument's value:

**DataWeave Script:**

```text
%dw 2.0
import * from dw::core::Strings
output application/json

fun errorHandling(errorCode: 404 | 405, response): String = "Code for error 4XX handling here!"
fun errorHandling(errorCode: 500 | 501, response): String = "Code for error 5XX handling here!"
---
errorHandling(payload.statusCode, payload)
```

At runtime, the function-dispatching algorithm selects the correct function based on the type of the value of `payload.statusCode`. It is not necessary to check the value of an argument with an `if` statement to change the behavior of the function.

#### Type Parameters

A type parameter enables you to write a function or data type generically so
that you can handle values identically, without depending on the type of the values.

For example, you can define a function that returns the first element of an array without losing its type information. In the example, the variable definitions `firstString:String` and `firstNumber:Number` specify the type of the item in the array that the `head` function takes as input.

```dataweave
%dw 2.0
fun head<ItemType>(elements: Array<ItemType>): ItemType = elements[0]!

var firstString:String = head(["DataWeave", "Java", "Scala", "Haskell"]) ++ " Rules!!!"
var firstNumber:Number = head([1,2,3])
output application/json
---
firstNumber
```

In the body of the script, `firstNumber` returns the number `1`. If you replace `firstNumber` with `firstString`, the script returns the string `"DataWeave Rules!!!"`.

##### Binding Type Parameters

You can bind type parameters to require a value of a specific type. Appending `{name: "DataWeave"}` in the following example is valid because `{name: String}` in the function definition indicates that the value of the `name` key must be a string.

```dataweave
%dw 2.0

fun addName<User <: {} >(user: User): User & {name: String} = user ++ {name: "DataWeave"}

var myUser: {name: String, developers: Number} = addName({developers: 3})
```

##### Parameterizing Type Definitions

You can use type parameters to parameterize type definitions. For example, assume that you define a data structure that models file content, one for text files and the other for binary files. You can use type parameters to construct new types that dispatch the correct implementation.

```dataweave
%dw 2.0

type FileData<Content> = {
    data: Content,
    name: String
}

fun read(file: FileData<String>) =  "This is a text file with data " ++ file.data
fun read(file: FileData<Binary>) =  "This is a binary file with data " ++ (file.data as String {base: "64"})

---
{
  binary: read({data: "Hello World" as Binary, name: "myFile.bin"}),
  text: read({data: "Hello World", name: "myFile.txt"})
}
```

### Reuse Types

You can declare and use types within the same DataWeave script (see type system), or you can reuse types from different sources by loading them with a specific module loader. DataWeave currently supports loading types from:

- type reuse modules
- type reuse json schema
- type reuse xml schema
- type reuse java classes
- type reuse avro schema

Module loaders are used to load files as DataWeave modules, in which different parts of those files are loaded as DataWeave functions, variables, types, and namespace definitions. Using a prefix such as `java!` or `xmlschema!` in the import directive tells DataWeave which module loader to use when loading the Java class or the XML schema as a DataWeave module.

---

## Type Coercion with DataWeave

In DataWeave, types can be coerced from one type to other using the `as` operator. Type coercion takes place at runtime.

Note that when you provide an operator with properties that do not match the expected types, DataWeave automatically attempts to coerce the provided property to the required type.

### Defining DataWeave Types For Type Coercion

The DataWeave example defines the type `Currency` using the `String` type, formats the value with the Java DecimalFormat pattern (`##`), and then uses `as` to coerce the `price` values to the `Currency` type.

**Input**

```xml
<items>
    <item>
        <price>22.30</price>
    </item>
    <item>
        <price>20.31</price>
    </item>
</items>
```

**DataWeave**

```dataweave
%dw 2.0
output application/json
type Currency = String { format: "\$#,###.00"}
---
books: payload.items.*item map
    book:
        price: $.price as Currency
```

**Output**

```json
{
  "books": [
    {
      "book": {
        "price": "22.30"
      }
    },
    {
      "book": {
        "price": "20.31"
      }
    }
  ]
}
```

### Type Coercion Table

This table shows the possible combinations and the properties from the schema that are used in the transformation.

| Source | Target | Property |
|---|---|---|
| `Range` | `Array` |  |
| `Number` | `Binary` |  |
| `String` | `Binary` |  |
| `String` | `Boolean` |  |
| `Number` | `DateTime` | `unit` |
| `LocalDateTime` | `DateTime` |  |
| `String` | `DateTime` | `format` / `locale` |
| `DateTime` | `LocalDate` |  |
| `LocalDateTime` | `LocalDate` |  |
| `String` | `LocalDate` | `format` / `locale` |
| `DateTime` | `LocalDateTime` |  |
| `String` | `LocalDateTime` | `format` / `locale` |
| `DateTime` | `LocalTime` |  |
| `LocalDateTime` | `LocalTime` |  |
| `Time` | `LocalTime` |  |
| `String` | `LocalTime` | `format` / `locale` |
| `DateTime` | `Number` | `unit` |
| `Period` | `Number` | `unit` |
| `String` | `Number` | `format` / `locale` |
| `String` | `Period` |  |
| `String` | `Regex` |  |
| `DateTime` | `String` | `format` / `locale` |
| `LocalDateTime` | `String` | `format` / `locale` |
| `LocalTime` | `String` | `format` / `locale` |
| `LocalDate` | `String` | `format` / `locale` |
| `Time` | `String` | `format` / `locale` |
| `Period` | `String` |  |
| `TimeZone` | `String` |  |
| `Number` | `String` | `format` / `locale` |
| `Boolean` | `String` |  |
| `Range` | `String` | Returns a string with all the values of the range using `,` as the separator |
| `Type` | `String` |  |
| `DateTime` | `Time` |  |
| `LocalDateTime` | `Time` |  |
| `LocalTime` | `Time` |  |
| `String` | `Time` | `format` |
| `DateTime` | `TimeZone` |  |
| `Time` | `TimeZone` |  |
| `String` | `TimeZone` |  |

#### Properties for Type Coercion

| Property | Description |
|---|---|
| `class` | Accepts Java classes for Object types. |
| `format` | Accepts Java `DecimalFormat` patterns to format numbers and dates. |
| `locale` | Accepts Java locales. A Java `Locale` object represents a region  (geographical, political, or cultural). |
| `mode` | Parsing mode for date and time values. Valid values: `SMART`, `STRICT`, `LENIENT` Note that `LENIENT` and `SMART` autocorrect invalid dates in different ways, but `STRICT` returns an error on the date. See examples that use `mode`. |
| `unit` | Value can be `milliseconds` or `seconds`. These are used for Number to DateTime, DateTime to Number, and Period to Number conversions. |

The following examples show uses of the `mode` property. Notice that `LENIENT` and `SMART` return valid dates when they receive an invalid date such as `02/31/2020`, but the resulting dates differ. `STRICT` returns an error on an invalid date. The examples use `uuuu` to represent the year instead of `yyyy`.

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
---
{
  examples : {

    badDateWithLenient: '02/31/2020' as Date {mode: "LENIENT", format: 'MM/dd/uuuu'},
    badDateWithSmart: '02/31/2020' as Date {mode: "SMART", format: 'MM/dd/uuuu'}
  }
}
```

**Output:**

```json
%dw 2.0
output application/json
---
{
  "examples": {
    "badDateWithLenient": "03/02/2020",
    "badDateWithSmart": "02/29/2020"
  }
}
```

Using STRICT on an invalid date returns an error. The following example is an error returned by `badDateWithStrict: '02/31/2020' as Date {mode: "STRICT", format: 'MM/dd/uuuu'}`:

```text
"Cannot coerce String (02/31/2020) to Date, caused by: Text '02/31/2020' could not be parsed: Invalid date 'FEBRUARY 31'

9| 	badDateWithSmart:
    '02/31/2020' as Date {mode: "STRICT", format: 'MM/dd/uuuu'}
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

The following example converts two strings into a date format and concatenates the result. The first string represents the date, and the second string represents the time. The transformation uses `as` to coerce the first string to `LocalDateTime`, and then to a `String` with the specified format. The transformation also uses `` to concatenate the result.

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
var s1= 20201228 // (uuuuMMdd),
var s2= 1608 //(HHMM)
---
(s1 ++ s2)
as LocalDateTime {format:"uuuuMMddHHmm"}
as String {format:"MM-dd-uuuu HH:mm:ss"}
```

**Output:**

```json
"12-28-2020 16:08:00"
```

The following example also converts a string into a date format. First, the transformation uses `as` to coerce the string into a `LocalDateTime` type, and then it coerces the result into a `String` type with the specified output format.

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
---
"8/30/2020 4:00:13 PM"
    as LocalDateTime {format: "M/dd/uuuu h:mm:ss a"}
    as String {format: "MM/dd/uuuu"}
```

**Output:**

```json
"08/30/2020"
```

This example converts a number to a string with a decimal representation:

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
---
{
     data: 22 as String {format: ".00"}
}
```

**Output:**

```json
{
  "data": "22.00"
}
```

To maintain consistency across all formats, starting with DataWeave 2.5, writing number values directly doesn’t preserve formatting and strips trailing zeroes. Format metadata is only used to parse the provided string into the correct number representation. To retain this behavior, you can re-enable it by using the `stripTrailingZeroes` property. See system properties.

The following example uses the `locale` property to format number and date values. First, you coerce a number value into `String` type to the specified output format that uses the Java DecimalFormat pattern (##) and also the `locale` property `en` (English) or `es` (Spanish). The `locale: "en"` property, formats the output number decimal representation using a `.`, while the `locale: "es"` property, formats the output using a `,`. +
Then, you coerce a date value into `Date` type and then to `String` type with the output format `dd-MMM-yy` and the `locale` property `en` (English), or `es` (Spanish). The `locale: "en"` property, formats the month `MMM` in English, while the `locale: "es"` property formats the month in Spanish.

**DataWeave script:**

```dataweave
%dw 2.0
output application/json
---
{
    enNumber: 12.3 as String {format: "##.##", locale: "en"},
    esNumber: 12.3 as String {format: "##.##", locale: "es"},
    esDate: "2020-12-31" as Date as String {format: "dd-MMM-yy", locale: "es"},
    enDate: "2020-12-31" as Date as String {format: "dd-MMM-yy", locale: "en"}
}
```

**Output:**

```json
{
  "enNumber": "12.3",
  "esNumber": "12,3",
  "esDate": "31-dic.-20",
  "enDate": "31-Dec-20"
}
```

### See Also

- Format Dates and Times
- Supported Data Formats
