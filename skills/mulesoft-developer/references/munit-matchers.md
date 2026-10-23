# MUnit: matchers

> Derived from mulesoft/docs-munit (Apache 2.0).

## MUnit Matchers

MUnit matchers are a set of DataWeave functions to define assertion conditions for any value in an expression.

When defining matchers, include the prefix `MunitTools::` in the expression, as illustrated in the following examples.

Matchers are grouped according to the type of conditions you want to validate.

### Match Core Values

Core matchers evaluate core values in the expression:

- Is the expression null?
- What is the media type or encoding of the expression?
- Does the expression return false?
- Are two evaluations successful?

Core Matchers:

- nullValue() checks that the expression is null.
Example:
```dataweave
#[MunitTools::nullValue()]
```

- notNullValue() checks that the expression is not null.
Example:
```dataweave
#[MunitTools::notNullValue()]
```

- withMediaType(String) checks that the expression’s media type is the one specified.
Example:
```dataweave
#[MunitTools::withMediaType('text/xml')]
```

- withEncoding(String) checks that the expression’s encoding is the one specified.
Example:
```dataweave
#[MunitTools::withEncoding('UTF-8')]
```

- both(Matcher, Matcher) checks that both provided matchers are successful.
Example:
```dataweave
#[MunitTools::both(MunitTools::notNullValue(), MunitTools::equalTo('example'))]
```

- either(Matcher,Matcher) checks that at least one of the matchers is successful.
Example:
```dataweave
#[MunitTools::either(MunitTools::nullValue(), MunitTools::equalTo(0))]
```

- not(Matcher) checks if the provided matcher is not successful.
Example:
```dataweave
#[MunitTools::not(MunitTools::equalTo(0))]
```

- anyOf(Matchers[\)] checks if any of the matchers are successful.
Example:
```dataweave
#[MunitTools::anyOf([MunitTools::notNullValue(),MunitTools::withMediaType('text/xml'),MunitTools::isEmptyString()])]
```

- allOf(Matchers[\)] checks if all of the matchers are successful.
Example:
```dataweave
#[MunitTools::allOf([MunitTools::notNullValue(),MunitTools::withMediaType('text/xml'),MunitTools::isEmptyString()])]
```

### Match Strings

String Matchers perform assertions on String expressions:

- Does the expression contain a specified string?
- Does the expression start or end with a specified string?
- Does the string in the expression have zero length?
- Does the string in the expression match a specified string?

String Matchers:

- containsString(String) checks that the expression contains the specified String.
Example:
```dataweave
#[MunitTools::containsString('example')]
```

- startsWith(String) checks that the expression starts with the specified String.
Example:
```dataweave
#[MunitTools::startsWith('exam')]
```

- endsWith(String) checks that the expression ends with the specified String.
Example:
```dataweave
#[MunitTools::endsWith('ple')]
```

- isEmptyString() checks that the expression has zero length.
Example:
```dataweave
#[MunitTools::isEmptyString()]
```

- isEmptyOrNullString() checks that the expression is null, or has zero length.
Example:
```dataweave
#[MunitTools::isEmptyOrNullString()]
```

- equalToIgnoringCase(String) checks that the expression is equal to the specified String, ignoring case.
Example:
```dataweave
#[MunitTools::equalToIgnoringCase('example')]
```

- equalToIgnoringWhiteSpace(String) checks that the expression is equal to the string disregarding leading and trailing white spaces, and compressing all inner white spaces to a single space.
Example:
```dataweave
#[MunitTools::equalToIgnoringWhiteSpace('An Example')]
```

- stringContainsInOrder(String, String,...) checks that the expression contains all of the specified substrings, regardless of the order of their appearance.
Example:
```dataweave
is="#[MunitTools::stringContainsInOrder(['an', 'example'])]"/>
```

### Match Comparable Expressions

Comparable matchers compare the expression against a specified value:

- Is the expression's value bigger or smaller than a specified value?
- Is the expression's value closer to a specific number?

Some comparable matchers take a `Comparable` type. `Comparable` is a DataWeave type that represents all the types that can be compared to each other. Allowed primitives are `String`, `Number`, `Boolean`, `DateTime`, `LocalDateTime`, `LocalTime`, `Time`, and `TimeZone`.

Comparable Matchers:

- greaterThan(Comparable) checks that the expression is greater than the specified value.
Examples:
```dataweave
#[MunitTools::greaterThan(20)]
```

```dataweave
#[MunitTools::greaterThan(|2017-08-09|)]
```

- greaterThanOrEqualTo(Comparable) checks that the expression is greater than or equal to the specified value.
Examples:
```dataweave
#[MunitTools::greaterThanOrEqualTo(20)]
```

```dataweave
#[MunitTools::greaterThanOrEqualTo(|2017-08-09|)]
```

- lessThan(Comparable) checks that the expression is less than the specified value.
Examples:
```dataweave
#[MunitTools::lessThan(20)
```

```dataweave
#[MunitTools::lessThan(|2017-08-09|)]
```

- lessThanOrEqualTo(Comparable) checks that the expression is less than or equal to the specified value.
Examples:
```dataweave
#[MunitTools::lessThanOrEqualTo(20)]
```

```dataweave
#[MunitTools::lessThanOrEqualTo(|2017-08-09|)]
```

- closeTo(Number, Number) checks that the expression is in the range defined by the first and second number.
Example:
```dataweave
#[MunitTools::closeTo(1, 0.01)]
```

- equalTo(Object) checks that the expression is equal to a specified value. This matcher also accepts DataWeave objects.
Examples:
```dataweave
#[MunitTools::equalTo('example')]
```

```dataweave
#[MunitTools::equalTo({example1: 1 , example2: 2}]
```

### Match Maps and Iterations

Use iterable matchers and maps matchers when your expression is an array or a map of data:

- Is the map or array in the expression empty?
- Does the map or array in the expression have a specific key?
- Is every item in the array from the expression greater than or less than a specific number?
- Does any item in the array from the expression start or end with a specified string?

Iterable and Map Matchers:

- everyItem(Matcher) checks that every element in the expression matches the specified matcher. This matcher works only for arrays.
Examples:
```dataweave
#[MunitTools::everyItem(MunitTools::notNullValue())]
```

```dataweave
#[MunitTools::everyItem(MunitTools::startsWith('a'))]
```

- hasItem(Matcher) checks that any element in the expression matches the specified matcher. This matcher works only for arrays.
Examples:
```dataweave
#[MunitTools::hasItem(MunitTools::notNullValue())]
```

```dataweave
#[MunitTools::hasItem(MunitTools::startsWith('a'))]
```

- hasSize(Matcher) checks that the size of the expression matches the specified matcher.
Examples:
```dataweave
#[MunitTools::hasSize(MunitTools::equalTo(5))]
```

```dataweave
#[MunitTools::hasSize(MunitTools::greaterThan(5))]
```

- isEmpty() checks that the expression is an empty collection.
Examples:
```dataweave
#[MunitTools::isEmpty()]
```

- hasKey(Matcher) checks that the expression has a key that matches the specified matcher. This matcher works only for maps.
Examples:
```dataweave
#[MunitTools::hasKey(MunitTools::equalTo('myKey'))]
```

```dataweave
#[MunitTools::hasKey(MunitTools::startsWith('a'))]
```

- hasValue(Matcher) checks that the expression has a value that matches the specified matcher. This matcher works only for maps.
Examples:
```dataweave
#[MunitTools::hasValue(MunitTools::equalTo('myValue'))]
```

```dataweave
#[MunitTools::hasValue(MunitTools::startsWith('a'))]
```

## Core Matchers Reference

### nullValue()

Checks that the expression is null.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::nullValue()]"/>
```

### notNullValue()

Checks that the expression is not null.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::notNullValue()]"/>
```

### withMediaType(String)

Checks that the expression's media type is the one specified.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::withMediaType('text/xml')]"/>
```

### withEncoding(String)

Checks that the expression encoding is the one specified.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::withEncoding('UTF-8')]"/>
```

### both(Matcher, Matcher)

Checks that both provided matchers are successful.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::both(MunitTools::notNullValue(),MunitTools::equalTo('example'))]"/>
```

### either(Matcher,Matcher)

Checks that at least one of the matchers is successful.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::either(MunitTools::nullValue(),MunitTools::equalTo(0))]"/>
```

### not(Object)

Checks if the provided matcher is not successful.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::not(0)]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::not(MunitTools::equalTo(0))]"/>
```

### anyOf(Array<Matcher>)

Checks if any of the matchers are successful.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::anyOf([MunitTools::notNullValue(),MunitTools::withMediaType('text/xml'),MunitTools::isEmptyString()])]"/>
```

### allOf(Array<Matcher>)

Checks if all of the matchers are successful.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::allOf([MunitTools::notNullValue(),MunitTools::withMediaType('text/xml'),MunitTools::isEmptyString()])]"/>
```

## String Matchers Reference

### containsString(String)

Checks that the expression contains the specified String.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::containsString('example')]"/>
```

### startsWith(String)

Checks that the expression starts with the specified String.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::startsWith('exam')]"/>
```

### endsWith(String)

Checks that the expression ends with the specified String.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::endsWith('ple')]"/>
```

### isEmptyString()

Checks that the expression has zero length.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::isEmptyString()]"/>
```

### isEmptyOrNullString()

Checks that the expression is null, or has zero length.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::isEmptyOrNullString()]"/>
```

### equalToIgnoringCase(String)

Checks that the expression is equal to the specified String, ignoring case.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::equalToIgnoringCase('example')]"/>
```

### equalToIgnoringWhiteSpace(String)

Checks that the expression is equal to the string disregarding leading and trailing white spaces, and compression all inner white spaces to a single space.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::equalToIgnoringWhiteSpace('An Example')]"/>
```

### stringContainsInOrder(Array<String>)

Checks that the expression contains all of the specified substrings, regardless of the order of their appearance.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::stringContainsInOrder(['an', 'example'])]"/>
```

## Comparable Matchers Reference

`Comparable` is a DataWeave type that represents all the types that can be compared to each other. +
Allowed primitives are String, Number, Boolean, DateTime, LocalDateTime, LocalTime, Time, and TimeZone  that you can pass any primitive value such as an integer or a date.

### greaterThan(Comparable)

Checks that the expression is greater than the specified value.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::greaterThan(|2017-08-09|)]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::greaterThan(20)]"/>
```

### greaterThanOrEqualTo(Comparable)

Checks that the expression is greater than or equal to the specified value.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::greaterThanOrEqualTo(20)]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::greaterThanOrEqualTo(|2017-08-09|)]"/>
```

### lessThan(Comparable)

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::lessThan(20)]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::lessThan(|2017-08-09|)]"/>
```

### lessThanOrEqualTo(Comparable)

Checks that the expression is less than or equal to the specified value.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::lessThanOrEqualTo(20)]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::lessThanOrEqualTo(|2017-08-09|)]"/>
```

### closeTo(Number, Number)

Checks that the expression is close to the first number, using the second number as a delta value. +
In other words, checks that the expression belongs to the range defined by the first number +/- the second number.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::closeTo(1, 0.01)]"/>

<!--
  This evaluates if the expression is between 0.99 (1 - 0.01) and 1.01 (1 + 0.01)
-->
```

### equalTo(Object)

Checks that the expression is equal to a specific value.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::equalTo(0)]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::equalTo('example')]"/>
```

This matcher also accepts Dataweave objects.

**Example**

```xml
<munit-tools:assert-that
expression="#[{example1: 1 , example2: 2}]"
is="#[MunitTools::equalTo({example1: 1 , example2: 2})]"/>
```

The matcher validates that the keys and their respective values are the same. +
The order in the matcher must be the same as the one in the expression or the assertion fails.

**Example**

```xml
<munit-tools:assert-that
expression="#[{example1: 1 , example2: 2}]"
is="#[MunitTools::equalTo({example2: 2 , example1: 1})]"/>

<!-- This assertion fails -->
```

**Example**

```xml
<munit-tools:assert-that
expression="#[[1, 2, 3]]"
is="#[MunitTools::equalTo([3, 2, 1])]"/>

<!-- This assertion fails -->
```

## Iterable and Map Matchers Reference

### everyItem(Matcher)

Checks that every element in the expression matches the specified matcher.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::everyItem(MunitTools::notNullValue())]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::everyItem(MunitTools::startsWith('a'))]"/>
```

### hasItem(Object)

Checks that any element in the expression matches the specified matcher.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasItem('example')]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasItem(MunitTools::startsWith('a'))]"/>
```

### hasSize(Matcher|Integer)

Checks that the size of the expression matches the specified matcher.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasSize(MunitTools::greaterThan(2))]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasSize(5)]"/>
```

### isEmpty()

Checks that the expression is an empty collection.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::isEmpty()]"/>
```

### hasKey(Matcher|String)

Checks that the expression has a key that matches the specified matcher.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasKey(MunitTools::startsWith('a'))]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasKey('mykey')]"/>
```

### hasValue(Object)

Checks that the expression has a value that matches the specified matcher.

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasValue('myvalue')]"/>
```

**Example**

```xml
<munit-tools:assert-that
expression="#[payload]"
is="#[MunitTools::hasValue(MunitTools::startsWith('a'))]"/>
```

## Resource Matchers

### getResourceAsStream(String)

Returns the resource from the path String as a stream.

**Example**

```xml
<set-payload
  value="#[MunitTools::getResourceAsStream('util/files/example.txt')]"/>
```

### getResourceAsReusableStream(String)

Returns the resource from the path String as a reusable stream.

**Example**

```xml
 <set-payload
   value="#[MunitTools::getResourceAsReusableStream('util/files/example.txt')]"/>
```

### getResourceAsString(path:String,encoding:String)

Returns the resource from the path String as a String, where the second parameter (encoding) is optional.

**Example**

```xml
<set-payload
  value="#[MunitTools::getResourceAsString('util/files/example.txt')]"/>
```

You can also specify the encoding:

**Example**

```xml
<set-payload
  value="#[MunitTools::getResourceAsString('util/files/exampleISO.txt', 'ISO-8859-1')]"/>
```

### getResourceAsByteArray(String)

Returns the resource from the path String as a byte array.

**Example**

```xml
 <set-payload
   value="#[MunitTools::getResourceAsByteArray('util/files/example.txt')]"/>
```

### queueSize(String)

Returns the size of the queue specified inside `#[MunitTools::queueSize()]`.

For example, to assert the size of a queue named `QUEUE_SIZE`:

**Example**

```xml

<munit:execution>
  <munit-tools:queue queueName="QUEUE_SIZE">
    <munit-tools:value>#['EXAMPLE']</munit-tools:value>
  </munit-tools:queue>
</munit:execution>

<munit:validation>
  <munit-tools:assert-that expression="#[MunitTools::queueSize('QUEUE_SIZE')]" is="#[MunitTools::equalTo(1)]"/>
</munit:validation>
```

### createMessage(payload: Any, mimeType: String|Null , attributes: Any, attributeMimeType: String|Null)

Creates a Mule message with the specified attributes.

**Example**

```xml
<munit:execution>
     <set-payload value="#[MunitTools::createMessage( 'ITEM-1',  'text/plain', { property : 'ATTRIBUTE-1'}, null )]"/>
 </munit:execution>
```

## DataWeave Assertions Library

### dw::test::Asserts

This module contains the set of core Matchers to use in your tests

**Example**

```dataweave
%dw 2.0
import dw::test::Asserts
---
payload must beObject()
```

Validates if a payload is of type Object

### Functions

#### anyOf

##### anyOf(Array<Matcher<Any>>): Matcher<Any>

Validates that the value satisfies at least one of the given matchers

```dataweave
%dw 2.0
import dw::test::Asserts
---
"A Text" must anyOf([beObject(), beString()])
```

#### beArray

##### beArray(): Matcher

Validates that a given value is of type Array

```dataweave
%dw 2.0
import dw::test::Asserts
---
[1, 4, 7] must beArray()
```

#### beBlank

##### beBlank(): Matcher<String | Null>

Validates that the String value is blank

```dataweave
%dw 2.0
import dw::test::Asserts
---
"  " must beBlank()
```

#### beBoolean

##### beBoolean(): Matcher

Validates that a given value is of type Boolean

```dataweave
%dw 2.0
import dw::test::Asserts
---
true must beBoolean()
```

#### beEmpty

##### beEmpty(): Matcher<String | Object | Array | Null>

Validates that the value (String, Object or Array) is empty

```dataweave
%dw 2.0
import dw::test::Asserts
---
[] must beEmpty()
```

#### beGreaterThan

##### beGreaterThan(Comparable, Boolean): Matcher<Comparable>

Validates that the asserted Comparable value is greater than the given one

Can be equal to when using the _inclusive_ argument

```dataweave
%dw 2.0
import dw::test::Asserts
---
3 must beGreaterThan(2)
```

#### beLowerThan

##### beLowerThan(Comparable, Boolean): Matcher<Comparable>

Validates that the asserted Comparable value is lower than the given one

Can be equal to when using the _inclusive_ argument

```dataweave
%dw 2.0
import dw::test::Asserts
---
1 must beLowerThan(2)
```

#### beNull

##### beNull(): Matcher

Validates that a given value is of type Null

```dataweave
%dw 2.0
import dw::test::Asserts
---
null must beNull()
```

#### beNumber

##### beNumber(): Matcher

Validates that a given value is of type Number

```dataweave
%dw 2.0
import dw::test::Asserts
---
123 must beNumber()
```

#### beObject

##### beObject(): Matcher

Validates that a given value is of type Object

```dataweave
%dw 2.0
import dw::test::Asserts
---
{ name : "Lionel", lastName: "Messi"} must beObject()
```

#### beOneOf

##### beOneOf(Array<Any>): Matcher

Validates that the value is contained in the given Array

```dataweave
%dw 2.0
import dw::test::Asserts
---
1 must beOneOf([1, "A Text", true])
```

#### beString

##### beString(): Matcher

Validates that a given value is of type String

```dataweave
%dw 2.0
import dw::test::Asserts
---
"A Text" must beString()
```

#### contain

##### contain(String): Matcher<String>

Validates that the asserted String contains the given String

```dataweave
%dw 2.0
import dw::test::Asserts
---
"A Text" must contain("ex")
```

##### contain(Any): Matcher<Array<Any>>

Validates that the asserted Array contains the given value

```dataweave
%dw 2.0
import dw::test::Asserts
---
[1, "A Text", true] must contain(1)
```

#### eachItem

##### eachItem(Matcher<Any>): Matcher<Array<Any>>

Validates that each item of the array satisfies the given matcher

```dataweave
%dw 2.0
import dw::test::Asserts
---
[1,2,3] must eachItem(beNumber())
```

#### endWith

##### endWith(String): Matcher<String>

Validates that the asserted String ends with the given String

```dataweave
%dw 2.0
import dw::test::Asserts
---
"A Text" must endWith("xt")
```

#### equalTo

##### equalTo(Any, { unordered?: Boolean }): Matcher<Any>

Validates that a value is equal to another one

```dataweave
%dw 2.0
import dw::test::Asserts
---
(1 + 2) must equalTo(3)
```

#### equalToResource

##### equalToResource(String, String, Object): Matcher<Any>

Validates that the given value is equal to the content of a resource file

The resource file must belong to the classpath

```dataweave
%dw 2.0
import dw::test::Asserts
---
{ name: "Lionel", lastName: "Messi" } must equalToResource("user.json", "application/json")
```

#### haveItem

##### haveItem(Matcher<Any>): Matcher<Array<Any>>

Validates that at least one item of the array satisfies the given matcher

```dataweave
%dw 2.0
import dw::test::Asserts
---
[1, true, "a text"] must haveItem(beNumber())
```

#### haveKey

##### haveKey(String): Matcher<Object>

Validates that the Object has the given key

```dataweave
%dw 2.0
import dw::test::Asserts
---
{ name: "Lionel", lastName: "Messi" } must haveKey("name")
```

#### haveSize

##### haveSize(Number): Matcher<Array | String | Object>

Validates that the array has the given size

```dataweave
%dw 2.0
import dw::test::Asserts
---
[1, 4, 7] must haveSize(3)
```

#### haveValue

##### haveValue(Any): Matcher<Object>

Validates that the Object has the given value

```dataweave
%dw 2.0
import dw::test::Asserts
---
{ name: "Lionel", lastName: "Messi" } must haveValue("Messi")
```

#### must

##### must(T, Array<(value: T) -> Matcher<T> | MatcherResult | Boolean>): MatcherResult

This function allows to assert a value with a list of Matcher of Expressions

**Example**

```dataweave
%dw 2.0
import dw::test::Asserts
---
payload must [
    beObject(),
    $.foo is Null
]
```

##### must(T, (value: T) -> Matcher<T> | Boolean): MatcherResult

This function allows to assert a value with a Matcher of Expressions

**Example**

```dataweave
%dw 2.0
import dw::test::Asserts
---
payload must beObject()
```

#### notBe

##### notBe(Matcher<T>): Matcher<T>

Validates that the value doesn't satisfy the given matcher

```dataweave
%dw 2.0
import dw::test::Asserts
---
1 must notBe(equalTo(2))
```

#### notBeNull

##### notBeNull(): Matcher

Validates that a given value isn't of type Null

```dataweave
%dw 2.0
import dw::test::Asserts
---
"A Text" must notBeNull()
```

#### startWith

##### startWith(String): Matcher<String>

Validates that the asserted String starts with the given String

```dataweave
%dw 2.0
import dw::test::Asserts
---
"A Text" must startWith("A")
```

### Variables

#### MATCHED

Constant that represents a successful match

### Types

#### Matcher

Data Type that represents a Matcher to perform assertions

**Example**

```dataweave
%dw 2.0
import dw::test::Asserts

fun beEqualToOne(): Matcher<Any> =
    (actual) -> do {
        {
            matches: actual == 1,
            description: { expected: "To be 1", actual: write(actual) as String }
        }
    }
```

**Definition**

```dataweave
(value: T) -> MatcherResult
```

#### MatcherResult

Data Type that represents the result of an Assertion

**Example**

```dataweave
{
  "matches": false,
  description : { expected : "Number type", actual: "A Text" }
}
```

**Definition**

```dataweave
{ matches: Boolean, description: { expected: String, actual: String }, reasons?: Array<String> }
```
