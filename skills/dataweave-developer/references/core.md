# dw::core — Core functions

Namespace `dw::core`.


Functions: `++`, `--`, `abs`, `avg`, `ceil`, `contains`, `daysBetween`, `distinctBy`, `endsWith`, `entriesOf`, `evaluateCompatibilityFlag`, `filter`, `filterObject`, `find`, `flatMap`, `flatten`, `floor`, `groupBy`, `indexOf`, `isBlank`, `isDecimal`, `isEmpty`, `isEven`, `isInteger`, `isLeapYear`, `isOdd`, `joinBy`, `keysOf`, `lastIndexOf`, `log`, `logDebug`, `logError`, `logInfo`, `logWarn`, `logWith`, `lower`, `map`, `mapObject`, `match`, `matches`, `max`, `maxBy`, `min`, `minBy`, `mod`, `namesOf`, `native`, `now`, `onNull`, `orderBy`, `pluck`, `pow`, `random`, `randomInt`, `read`, `readUrl`, `reduce`, `replace`, `round`, `scan`, `sizeOf`, `splitBy`, `sqrt`, `startsWith`, `sum`, `then`, `to`, `trim`, `typeOf`, `unzip`, `upper`, `uuid`, `valuesOf`, `with`, `write`, `xsiType`, `zip`

---

## ++

```
++<S, T>(source: Array<S>, with: Array<T>): Array<S | T>
```

Concatenates two values. This version of `++` concatenates the elements of two arrays into a new array. Other versions act on strings, objects, and the various date and time formats that DataWeave supports. If the two arrays contain different types of elements, the resulting array is all of `S` type elements of `Array<S>` followed by all the `T` type elements of `Array<T>`. Either of the arrays can also have mixed-type elements. Also note that the arrays can contain any supported data type.

- `source` — The source array.
- `with` — The array to concatenate with the source array.

```dataweave
%dw 2.0
output application/json
---
{ "result" : [0, 1, 2] ++ ["a", "b", "c"] }
```

```json
{ "result": [0, 1, 2, "a", "b", "c"] }
```

```
++(source: String, with: String): String
```

Concatenates the characters of two strings. Strings are treated as arrays of characters, so the `++` operator concatenates the characters of each string as if they were arrays of single-character string.

- `source` — The source string.
- `with` — The string to concatenate with the source string.

```dataweave
%dw 2.0
output application/json
---
{ "name" : "Mule" ++ "Soft" }
```

```json
{ "name": "MuleSoft" }
```

```
++<T <: Object, Q <: Object>(source: T, with: Q): T & Q
```

Concatenates two objects and returns one flattened object. The `++` operator extracts all the key-values pairs from each object, then combines them together into one result object.

- `source` — The source object.
- `with` — The object to concatenate with the source object.

```dataweave
%dw 2.0
output application/xml
---
{ concat : {aa: "a", bb: "b"} ++ {cc: "c"} }
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<concat>
  <aa>a</aa>
  <bb>b</bb>
  <cc>c</cc>
</concat>
```

```
++(date: Date, time: LocalTime): LocalDateTime
```

Appends a `LocalTime` with a `Date` to return a `LocalDateTime` value. `Date` and `LocalTime` instances are written in standard Java notation, surrounded by pipe (`|`) symbols. The result is a `LocalDateTime` object in the standard Java format. Note that the order in which the two objects are concatenated is irrelevant, so logically, `Date ++ LocalTime` produces the same result as `LocalTime ++ Date`.

- `date` — A `Date`.
- `time` — A `LocalTime`, a time format without a time zone.

```dataweave
%dw 2.0
output application/json
---
{ "LocalDateTime" : (|2017-10-01| ++ |23:57:59|) }
```

```json
{ "LocalDateTime": "2017-10-01T23:57:59" }
```

```
++(time: LocalTime, date: Date): LocalDateTime
```

Appends a `LocalTime` with a `Date` to return a `LocalDateTime`. Note that the order in which the two objects are concatenated is irrelevant, so logically, `LocalTime ++ Date` produces the same result as `Date ++ LocalTime`.

- `time` — A `LocalTime`, a time format without a time zone.
- `date` — A `Date`.

```dataweave
%dw 2.0
output application/json
---
{ "LocalDateTime" : (|23:57:59| ++ |2003-10-01|) }
```

```json
{ "LocalDateTime": "2017-10-01T23:57:59" }
```

```
++(date: Date, time: Time): DateTime
```

Appends a `Date` to a `Time` in order to return a `DateTime`. Note that the order in which the two objects are concatenated is irrelevant, so logically, `Date` + `Time`  produces the same result as `Time` + `Date`.

- `date` — A `Date`.
- `time` — A `Time`, a time format that can include a time zone (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
[ |2017-10-01| ++ |23:57:59-03:00|, |2017-10-01| ++ |23:57:59Z| ]
```

```json
[ "2017-10-01T23:57:59-03:00", "2017-10-01T23:57:59Z" ]
```

```
++(time: Time, date: Date): DateTime
```

Appends a `Date` to a `Time` object to return a `DateTime`. Note that the order in which the two objects are concatenated is irrelevant, so logically, `Date` + `Time`  produces the same result as a `Time` + `Date`.

- `time` — A `Time`, a time format that can include a time zone (`Z` or `HH:mm`).
- `date` — A `Date`.

```dataweave
%dw 2.0
output application/json
---
|2018-11-30| ++ |23:57:59+01:00|
```

```json
"2018-11-30T23:57:59+01:00"
```

```
++(date: Date, timezone: TimeZone): DateTime
```

Appends a `TimeZone` to a `Date` type value and returns a `DateTime` result.

- `date` — A `Date`.
- `timezone` — A `TimeZone` (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
{ "DateTime" : (|2017-10-01| ++ |-03:00|) }
```

```json
{ "DateTime": "2017-10-01T00:00:00-03:00" }
```

```
++(timezone: TimeZone, date: Date): DateTime
```

Appends a `Date` to a `TimeZone` in order to return a `DateTime`.

- `date` — A `Date`.
- `timezone` — A `TimeZone` (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
{ "DateTime" : |-03:00| ++ |2017-10-01| }
```

```json
{ "DateTime": "2017-10-01T00:00:00-03:00" }
```

```
++(dateTime: LocalDateTime, timezone: TimeZone): DateTime
```

Appends a `TimeZone` to a `LocalDateTime` in order to return a `DateTime`.

- `dateTime` — A `LocalDateTime`, a date and time without a time zone.
- `timezone` — A `TimeZone` (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
{ "DateTime" : (|2003-10-01T23:57:59| ++ |-03:00|) }
```

```json
{ "DateTime": "2003-10-01T23:57:59-03:00 }
```

```
++(timezone: TimeZone, datetime: LocalDateTime): DateTime
```

Appends a `LocalDateTime` to a `TimeZone` in order to return a `DateTime`.

- `dateTime` — A `LocalDateTime`, a date and time without a time zone.
- `timezone` — A `TimeZone` (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
{ "TimeZone" : (|-03:00| ++ |2003-10-01T23:57:59|) }
```

```json
{ "TimeZone": "2003-10-01T23:57:59-03:00" }
```

```
++(time: LocalTime, timezone: TimeZone): Time
```

Appends a `TimeZone` to a `LocalTime` in order to return a `Time`.

- `time` — A `LocalTime`, time format without a time zone.
- `timezone` — A `TimeZone` (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
{ "Time" : (|23:57| ++ |-03:00|) }
```

```json
{ "Time": "23:57:00-03:00" }
```

```
++(timezone: TimeZone, time: LocalTime): Time
```

Appends a `LocalTime` to a `TimeZone` in order to return a `Time`.

- `time` — A `LocalTime`, a time format without a time zone.
- `timezone` — A `TimeZone` (`Z` or `HH:mm`).

```dataweave
%dw 2.0
output application/json
---
{ "Time" : (|-03:00| ++ |23:57|) }
```

```json
{
  "Time": "23:57:00-03:00"
}
```

## --

```
--<S>(source: Array<S>, toRemove: Array<Any>): Array<S>
```

Removes specified values from an input value. This version of `--` removes all instances of the specified items from an array. Other versions act on objects, strings, and the various date and time formats that are supported by DataWeave.

```dataweave
%dw 2.0
output application/json
---
{ "a" : [0, 1, 1, 2] -- [1,2] }
```

```json
{ "a": [0] }
```

```
--<K, V>(source: { (K)?: V }, toRemove: Object): { (K)?: V }
```

Removes specified key-value pairs from an object.

- `source` — The source object (an `Object` type).
- `toRemove` — Object that contains the key-value pairs to remove from the source object.

```dataweave
%dw 2.0
output application/json
---
{ "hello" : "world", "name" : "DW" } -- { "hello" : "world"}
```

```json
{ "name": "DW" }
```

```
--(source: Object, keys: Array<String>)
```

Removes all key-value pairs from the source object that match the specified search key.

- `source` — The source object (an `Object` type).
- `toRemove` — An array of keys to specify the key-value pairs to remove from the source object.

```dataweave
%dw 2.0
output application/json
---
{ "yes" : "no", "good" : "bad", "old" : "new" } -- ["yes", "old"]
```

```json
{ "good": "bad" }
```

```
--(source: Object, keys: Array<Key>)
```

Removes specified key-value pairs from an object.

- `source` — The source object (an `Object` type).
- `keys` — A keys for the key-value pairs to remove from the source object.

```dataweave
%dw 2.0
output application/json
---
{ "hello" : "world", "name" : "DW" } -- ["hello" as Key]
```

```json
{ "name": "DW" }
```

```
--(source: Null, keys: Any)
```

Helper function that enables `--` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## abs

```
abs(number: Number): Number
```

Returns the absolute value of a number.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ abs(-2), abs(2.5), abs(-3.4), abs(3) ]
```

```json
[ 2, 2.5, 3.4, 3 ]
```

## avg

```
avg(values: Array<Number>): Number
```

Returns the average of numbers listed in an array. An array that is empty or that contains a non-numeric value results in an error.

- `values` — The input array of numbers.

```dataweave
%dw 2.0
output application/json
---
{ a: avg([1, 1000]), b: avg([1, 2, 3]) }
```

```json
{ "a": 500.5, "b": 2 }
```

## ceil

```
ceil(number: Number): Number
```

Rounds a number up to the nearest whole number.

- `number` — The number to round.

```dataweave
%dw 2.0
output application/json
---

[ ceil(1.5), ceil(2.1), ceil(3) ]
```

```json
[ 2, 3, 3 ]
```

## contains

```
contains<T>(@StreamCapable items: Array<T>, element: Any): Boolean
```

Returns `true` if an input contains a given value, `false` if not. This version of `contains` accepts an array as input. Other versions accept a string and can use another string or regular expression to determine whether there is a match.

- `items` — The input array.
- `elements` — Element to find in the array. Can be any supported data type.

```dataweave
%dw 2.0
output application/json
---
[ 1, 2, 3, 4 ] contains(2)
```

```json
true
```

```
contains(text: String, toSearch: String): Boolean
```

Indicates whether a string contains a given substring. Returns `true` or `false`.

- `text` — An input string (a `String`).
- `toSearch` — The substring (a `String`) to find in the input string.

```dataweave
%dw 2.0
output application/json
---
"mulesoft" contains("mule")
```

```json
true
```

```
contains(text: String, matcher: Regex): Boolean
```

Returns `true` if a string contains a match to a regular expression, `false` if not.

- `text` — An input string.
- `matcher` — A Java regular expression for matching characters in the input `text`.

```dataweave
%dw 2.0
output application/json
---
contains("mulesoft", /[e-g]/)
```

```json
true
```

```
contains(text: Null, matcher: Any): false
```

Helper function that enables `contains` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## daysBetween

```
daysBetween(from: Date, to: Date): Number
```

Returns the number of days between two dates.

- `from` — From date (a `Date` type).
- `to` — To date (a `Date` type). Note that if the `to` date is _earlier_ than the `from` date, the function returns a negative number equal to the number of days between the two dates.

```dataweave
%dw 2.0
output application/json
---
{ days : daysBetween('2016-10-01T23:57:59-03:00', '2017-10-01T23:57:59-03:00') }
```

```json
{ "days" : 365 }
```

## distinctBy

```
distinctBy<T>(@StreamCapable items: Array<T>, criteria: (item: T, index: Number) -> Any): Array<T>
```

Iterates over the input and returns the unique elements in it. DataWeave uses the result of the provided lambda as the uniqueness criteria. This version of `distinctBy` finds unique values in an array. Other versions act on an object and handle a `null` value.

- `items` — The array to evaluate.
- `criteria` — The criteria used to select an `item` and/or `index` from the array.

```dataweave
%dw 2.0
output application/json
---
[0, 1, 2, 3, 3, 2, 1, 4] distinctBy (value) -> { "unique" : value }
```

```json
[ 0, 1, 2, 3, 4]
```

```
distinctBy<K, V>(object: { (K)?: V }, criteria: (value: V, key: K) -> Any): Object
```

Removes duplicate key-value pairs from an object.

- `object` — The object from which to remove the key-value pairs.
- `criteria` — The `key` and/or `value` used to identify the key-value pairs to remove.

```dataweave
%dw 2.0
output application/json
---
{a : "b", a : "b", A : "b", a : "B"} distinctBy (value) -> { "unique" : value }
```

```json
{ "a": "b", "a": "B" }
```

```
distinctBy(@StreamCapable items: Null, criteria: (item: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `distinctBy` to work with a `null` value.

## endsWith

```
endsWith(text: String, suffix: String): Boolean
```

Returns `true` if a string ends with a provided substring, `false` if not.

- `text` — The input string (a `String`).
- `suffix` — The suffix string to find at the end of the input string.

```dataweave
%dw 2.0
output application/json
---
[ "Mariano" endsWith "no", "Mariano" endsWith "to" ]
```

```json
[ true, false ]
```

```
endsWith(text: Null, suffix: Any): false
```

Helper function that enables `endsWith` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## entriesOf

```
entriesOf<T <: Object>(obj: T): Array<{| key: Key, value: Any, attributes: Object |}>
```

Returns an array of key-value pairs that describe the key, value, and any attributes in the input object. _Introduced in DataWeave version 2.3.0._

- `obj` — The object to describe.

```dataweave
%dw 2.0
var myVar = read('<xml attr="x"><a>true</a><b>1</b></xml>', 'application/xml')
output application/json
---
{ "entriesOf" : entriesOf(myVar) }
```

```json
{
  "entriesOf": [
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

```
entriesOf(obj: Null): Null
```

Helper function that enables `entriesOf` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## evaluateCompatibilityFlag

```
evaluateCompatibilityFlag(flag: String): Boolean
```

Returns the value of the compatibility flag with the specified name. _Introduced in DataWeave version 2.5.0._

- `Description` — `flag`
- `String` — The name of the compatibility flag to evaluate.

```dataweave
%dw 2.0
output application/json
---
{
  "com.mulesoft.dw.xml_reader.honourMixedContentStructure": evaluateCompatibilityFlag("com.mulesoft.dw.xml_reader.honourMixedContentStructure")
}
```

```json
{
  "com.mulesoft.dw.xml_reader.honourMixedContentStructure": true
}
```

## filter

```
filter<T>(@StreamCapable items: Array<T>, criteria: (item: T, index: Number) -> Boolean): Array<T>
```

Iterates over an array and applies an expression that returns matching values. The expression must return `true` or `false`. If the expression returns `true` for a value or index in the array, the value gets captured in the output array. If it returns `false` for a value or index in the array, that item gets filtered out of the output. If there are no matches, the output array will be empty.

- `items` — The array to filter.
- `criteria` — Boolean expression that selects an `item` and/or `index`.

```dataweave
[9,2,3,4,5] filter (value, index) -> (value > 2)
```

```json
[9,3,4,5]
```

```
filter(@StreamCapable text: String, criteria: (character: String, index: Number) -> Boolean): String
```

Iterates over a string and applies an expression that returns matching values. The expression must return `true` or `false`. If the expression returns `true` for a character or index in the array, the character gets captured in the output string. If it returns `false` for a character or index in the array, that character gets filtered out of the output. If there are no matches, the output string will be empty.

- `text` — The text to filter.
- `criteria` — The criteria to use.

```dataweave
%dw 2.0
output application/json
---
"hello world" filter ($$ mod 2) == 0
```

```json
"hlowrd"
```

```
filter(@StreamCapable value: Null, criteria: (item: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `filter` to work with a `null` value.

## filterObject

```
filterObject<K, V>(@StreamCapable value: { (K)?: V }, criteria: (value: V, key: K, index: Number) -> Boolean): { (K)?: V }
```

Iterates a list of key-value pairs in an object and applies an expression that returns only matching objects, filtering out the rest from the output. The expression must return `true` or `false`. If the expression returns `true` for a key, value, or index of an object, the object gets captured in the output. If it returns `false` for any of them, the object gets filtered out of the output. If there are no matches, the output array will be empty.

- `value` — The source object to evaluate.
- `criteria` — Boolean expression that selects a `value`, `key`, or `index` of the object.

```dataweave
%dw 2.0
output application/json
---
{"a" : "apple", "b" : "banana"} filterObject ((value) -> value == "apple")
```

```json
{ "a": "apple" }
```

```
filterObject(value: Null, criteria: (value: Nothing, key: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `filterObject` to work with a `null` value.

## find

```
find<T>(@StreamCapable() elements: Array<T>, elementToFind: Any): Array<Number>
```

Returns indices of an input that match a specified value. This version of the function returns indices of an array. Others return indices of a string.

- `elements` — An array with elements of any type.
- `elementToFind` — Value to find in the input array.

```dataweave
%dw 2.0
output application/json
---
["Bond", "James", "Bond"] find "Bond"
```

```json
[0,2]
```

```
find(@StreamCapable() text: String, matcher: Regex): Array<Array<Number>>
```

Returns the indices in the text that match the specified regular expression (regex), followed by the capture groups. The first element in each resulting sub-array is the index in the text that matches the regex, and the next ones are the capture groups in the regex (if present). Note: To retrieve parts of the text that match a regex. use the `scan` function.

- `text` — A string.
- `matcher` — A Java regular expression for matching characters in the `text`.

```dataweave
%dw 2.0
output application/json
---
"I heart DataWeave" find /\w*ea\w*(\b)/
```

```json
[ [2,7], [8,17] ]
```

```
find(@StreamCapable() text: String, textToFind: String): Array<Number>
```

Lists indices where the specified characters of a string are present.

- `text` — A source string.
- `textToFind` — The string to find in the source string.

```dataweave
%dw 2.0
output application/json
---
"aabccdbce" find "a"
```

```json
[0,1]
```

```
find(@StreamCapable() text: Null, textToFind: Any): Array<Nothing>
```

Helper function that enables `find` to work with a `null` value.

## flatMap

```
flatMap<T, R>(@StreamCapable items: Array<T>, mapper: (item: T, index: Number) -> Array<R>): Array<R>
```

Iterates over each item in an array and flattens the results. Instead of returning an array of arrays (as `map` does when you iterate over the values within an input like `[ [1,2], [3,4] ]`), `flatMap` returns a flattened array that looks like this: `[1, 2, 3, 4]`. `flatMap` is similar to `flatten`, but `flatten` only acts on the values of the arrays, while `flatMap` can act on values and indices of items in the array.

- `items` — The array to map.
- `mapper` — Expression or selector for an `item` and/or `index` in the array to flatten.

```dataweave
%dw 2.0
output application/json
---
[ [3,5], [0.9,5.5] ] flatMap (value, index) -> value
```

```json
[ 3, 5, 0.9, 5.5]
```

```
flatMap<T, R>(@StreamCapable value: Null, mapper: (item: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `flatMap` to work with a `null` value.

## flatten

```
flatten<T, Q>(@StreamCapable items: Array<Array<T> | Q>): Array<T | Q>
```

Turns a set of subarrays (such as `[ [1,2,3], [4,5,[6]], [], [null] ]`) into a single, flattened array (such as `[ 1, 2, 3, 4, 5, [6], null ]`). Note that it flattens only the first level of subarrays and omits empty subarrays.

- `items` — The input array of arrays made up of any supported types.

```dataweave
%dw 2.0
output application/json
var array1 = [1,2,3]
var array2 = [4,5,6]
var array3 = [7,8,9]
var arrayOfArrays = [array1, array2, array3]
---
flatten(arrayOfArrays)
```

```json
[ 1,2,3,4,5,6,7,8,9 ]
```

```
flatten(@StreamCapable value: Null): Null
```

Helper function that enables `flatten` to work with a `null` value.

## floor

```
floor(number: Number): Number
```

Rounds a number down to the nearest whole number.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ floor(1.5), floor(2.2), floor(3) ]
```

```json
[ 1, 2, 3]
```

## groupBy

```
groupBy<T, R>(items: Array<T>, criteria: (item: T, index: Number) -> R): {| (R): Array<T> |}
```

Returns an object that groups items from an array based on specified criteria, such as an expression or matching selector. This version of `groupBy` groups the elements of an array using the `criteria` function. Other versions act on objects and handle null values.

- `items` — The array to group.
- `criteria` — Expression providing the criteria by which to group the items in the array.

```dataweave
%dw 2.0
output application/json
---
["a","b","c"] groupBy (item, index) -> index
```

```json
{ "2": [ "c" ], "1": [ "b" ], "0": [ "a" ] }
```

```
groupBy<R>(text: String, criteria: (character: String, index: Number) -> R): { (R): String }
```

Returns an object that groups characters from a string based on specified criteria, such as an expression or matching selector. This version of `groupBy` groups the elements of an array using the `criteria` function. Other versions act on objects and handle `null` values.

- `text` — The string to group by.
- `criteria` — The criteria to use.

```dataweave
%dw 2.0
output application/json
---
"hello world!" groupBy (not isEmpty($ find /[aeiou]/))
```

```json
{
  "false": "hll wrld!",
  "true": "eoo"
}
```

```
groupBy<K, V, R>(object: { (K)?: V }, criteria: (value: V, key: K) -> R): { (R): { (K)?: V } }
```

Groups elements of an object based on criteria that the `groupBy` uses to iterate over elements in the input.

- `object` — The object containing objects to group.
- `criteria` — The grouping criteria to apply to elements in the input object, such as a `key` and/or `value` of the object to use for grouping.

```dataweave
%dw 2.0
output application/json
---
{ "a" : "b", "c" : "d"} groupBy upper($)
```

```json
{ "D": { "c": "d" }, "B": { "a": "b" } }
```

```
groupBy(value: Null, criteria: (Nothing, Nothing) -> Any): Null
```

Helper function that enables `groupBy` to work with a `null` value.

## indexOf

```
indexOf(array: Array, value: Any): Number
```

Returns the index of the _first_ occurrence of the specified element in this array, or `-1` if this list does not contain the element. _Introduced in DataWeave version 2.4.0._

- `array` — The array of elements to search.
- `value` — The value to search.

```dataweave
%dw 2.0
output application/json
---
{
  present: ["a","b","c","d"] indexOf "c",
  notPresent: ["x","w","x"] indexOf "c",
  presentMoreThanOnce: ["a","b","c","c"] indexOf "c",
}
```

```json
{
   "present": 2,
   "notPresent": -1,
   "presentMoreThanOnce": 2
 }
```

```
indexOf(theString: String, search: String): Number
```

Returns the index of the *first* occurrence of the specified String in this String. _Introduced in DataWeave version 2.4.0._

- `theString` — The string to search.
- `search` — The string to find within `theString`.

```dataweave
%dw 2.0
output application/json
---
{
  present: "abcd" indexOf "c",
  notPresent: "xyz" indexOf "c",
  presentMoreThanOnce: "abcdc" indexOf "c",
}
```

```json
{
   "present": 2,
   "notPresent": -1,
   "presentMoreThanOnce": 2
 }
```

```
indexOf(array: Null, value: Any): Number
```

Helper method to make indexOf null friendly _Introduced in DataWeave version 2.4.0._

## isBlank

```
isBlank(text: String | Null): Boolean
```

Returns `true` if the given string is empty (`""`), completely composed of whitespaces, or `null`. Otherwise, the function returns `false`.

- `text` — An input string to evaluate.

```dataweave
%dw 2.0
output  application/json
var someString = "something"
var nullString = null
---
{
  // checking if the string is blank
  "emptyString" : isBlank(""),
  "stringWithSpaces" : isBlank("      "),
  "textString" : isBlank(someString),
  "somePayloadValue" : isBlank(payload.nonExistingValue),
  "nullString" : isBlank(nullString),

  // checking if the string is not blank
  "notEmptyTextString" : not isBlank(" 1234"),
  "notEmptyTextStringTwo" : ! isBlank("")
}
```

```json
{
  "emptyString": true,
  "stringWithSpaces": true,
  "textString": false,
  "somePayloadValue": true,
  "nullString": true,
  "notEmptyTextString": true,
  "notEmptyTextStringTwo": false
}
```

## isDecimal

```
isDecimal(number: Number): Boolean
```

Returns `true` if the given number contains a decimal, `false` if not.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ isDecimal(1.1), isDecimal(1), isDecimal("1.1") ]
```

```json
[ true, false, true ]
```

## isEmpty

```
isEmpty(elements: Array<Any>): Boolean
```

Returns `true` if the given input value is empty, `false` if not. This version of `isEmpty` acts on an array. Other versions act on a string or object, and handle null values.

- `elements` — The input array to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ isEmpty([]), isEmpty([1]) ]
```

```json
[ true, false ]
```

```
isEmpty(value: String): Boolean
```

Returns `true` if the input string is empty, `false` if not.

- `value` — A string to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ isEmpty(""), isEmpty("DataWeave") ]
```

```json
[ true, false ]
```

```
isEmpty(value: Object): Boolean
```

Returns `true` if the given object is empty, `false` if not.

- `value` — The object to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ isEmpty({}), isEmpty({name: "DataWeave"}) ]
```

```json
[ true, false ]
```

```
isEmpty(value: Binary): Boolean
```

Returns `true` if the input binary is empty, `false` if not. _Introduced in DataWeave version 2.11.0._

- `Description` — `value`
- `Binary` — The input binary value.

```dataweave
%dw 2.0
output application/json
---
[ isEmpty("" as Binary), isEmpty("DataWeave" as Binary) ]
```

```json
[ true, false ]
```

```
isEmpty(value: Null): true
```

Returns `true` if the input is `null`.

- `value` — `null` is the value in this case.

```dataweave
%dw 2.0
output application/json
---
{ "nullValue" : isEmpty(null) }
```

```json
{ "nullValue": true }
```

## isEven

```
isEven(number: Number): Boolean
```

Returns `true` if the number or numeric result of a mathematical operation is even, `false` if not.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output  application/json
---
{ "isEven" : [ isEven(0), isEven(1), isEven(1+1) ] }
```

```json
{ "isEven" : [ true, false, true ] }
```

## isInteger

```
isInteger(number: Number): Boolean
```

Returns `true` if the given number is an integer (which lacks decimals), `false` if not.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output application/json
---
[isInteger(1), isInteger(2.0), isInteger(2.2), isInteger("1")]
```

```json
[ true, true, false, true ]
```

## isLeapYear

```
isLeapYear(dateTime: DateTime): Boolean
```

Returns `true` if it receives a date for a leap year, `false` if not. This version of `leapYear` acts on a `DateTime` type. Other versions act on the other date and time formats that DataWeave supports.

- `dateTime` — The `DateTime` value to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ isLeapYear(|2016-10-01T23:57:59|), isLeapYear(|2017-10-01T23:57:59|) ]
```

```json
[ true, false ]
```

```
isLeapYear(date: Date): Boolean
```

Returns `true` if the input `Date` is a leap year, 'false' if not.

- `date` — The `Date` value to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ isLeapYear(|2016-10-01|), isLeapYear(|2017-10-01|) ]
```

```json
[ true, false ]
```

```
isLeapYear(datetime: LocalDateTime): Boolean
```

Returns `true` if the input local date-time is a leap year, 'false' if not.

- `datetime` — A `LocalDateTime` value to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ |2016-10-01T23:57:59-03:00|, |2016-10-01T23:57:59Z| ] map isLeapYear($)
```

```json
[ true, true ]
```

## isOdd

```
isOdd(number: Number): Boolean
```

Returns `true` if the number or numeric result of a mathematical operation is odd, `false` if not.

- `number` — A number to evaluate.

```dataweave
%dw 2.0
output  application/json
---
{ "isOdd" : [ isOdd(0), isOdd(1), isOdd(2+2) ] }
```

```json
{ "isOdd": [ false, true, false ] }
```

## joinBy

```
joinBy(@StreamCapable elements: Array<StringCoerceable>, separator: String): String
```

Merges an array into a single string value and uses the provided string as a separator between each item in the list. Note that `joinBy` performs the opposite task of `splitBy`.

- `elements` — The input array.
- `separator` — A `String` used to join elements in the list.

```dataweave
%dw 2.0
output application/json
---
{ "hyphenate" : ["a","b","c"] joinBy "-" }
```

```json
{ "hyphenate": "a-b-c" }
```

```
joinBy(n: Null, separator: Any): Null
```

Helper function that enables `joinBy` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## keysOf

```
keysOf<K, V>(obj: { (K)?: V }): Array<K>
```

Returns an array of keys from key-value pairs within the input object. The returned keys belong to the Key type. To return each key as a string, you can use `namesOf`, instead. _Introduced in DataWeave version 2.3.0._

- `object` — The object to evaluate.

```dataweave
%dw 2.0
output application/json
---
{ "keysOf" : keysOf({ "a" : true, "b" : 1}) }
```

```json
{ "keysOf" : ["a","b"] }
```

```
keysOf(obj: Null): Null
```

Helper function that enables `keysOf` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## lastIndexOf

```
lastIndexOf(array: Array, value: Any): Number
```

Returns the index of the _last_ occurrence of the specified element in a given array or `-1` if the array does not contain the element. _Introduced in DataWeave version 2.4.0._

- `array` — The array of elements to search.
- `value` — The value to search.

```dataweave
%dw 2.0
output application/json
---
{
  present: ["a","b","c","d"] lastIndexOf "c",
  notPresent: ["x","w","x"] lastIndexOf "c",
  presentMoreThanOnce: ["a","b","c","c"] lastIndexOf "c",
}
```

```json
{
  "present": 2,
  "notPresent": -1,
  "presentMoreThanOnce": 3
}
```

```
lastIndexOf(array: String, value: String): Number
```

Takes a string as input and returns the index of the _last_ occurrence of a given search string within the input. The function returns `-1` if the search string is not present in the input. _Introduced in DataWeave version 2.4.0._

- `string` — The string to search.
- `value` — A string value to search for within the input string.

```dataweave
%dw 2.0
output application/json
---
{
  present: "abcd" lastIndexOf "c",
  notPresent: "xyz" lastIndexOf "c",
  presentMoreThanOnce: "abcdc" lastIndexOf "c",
}
```

```json
{
  "present": 2,
  "notPresent": -1,
  "presentMoreThanOnce": 4
}
```

```
lastIndexOf(array: Null, value: Any): Number
```

Helper function that enables `lastIndexOf` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## log

```
log<T>(prefix: String = "", value: T): T
```

Without changing the value of the input, `log` returns the input as a system log. So this makes it very simple to debug your code, because any expression or subexpression can be wrapped with *log* and the result will be printed out without modifying the result of the expression. The output is going to be printed in application/dw format. The prefix parameter is optional and allows to easily find the log output. Use this function to help with debugging DataWeave scripts. A Mule app outputs the results through the `DefaultLoggingService`, which you can see in the Studio console.

- `prefix` — An optional string that typically describes the log.
- `value` — The value to log.

```dataweave
%dw 2.0
output application/json
---
log("WARNING", "Houston, we have a problem")
```

```xml
"WARNING - Houston, we have a problem"
```

## logDebug

```
logDebug<T>(prefix: String = "", value: T): T
```

Helper function that logs messages at `Debug` level. _Introduced in DataWeave version 2.10.0._

- `prefix` — An optional string that typically describes the log.
- `value` — The value to log.

## logError

```
logError<T>(prefix: String = "", value: T): T
```

Helper function that logs messages at `Error` level. _Introduced in DataWeave version 2.10.0._

- `prefix` — An optional string that typically describes the log.
- `value` — The value to log.

## logInfo

```
logInfo<T>(prefix: String = "", value: T): T
```

Helper function that logs messages at `Info` level. _Introduced in DataWeave version 2.10.0._

- `prefix` — An optional string that typically describes the log.
- `value` — The value to log.

## logWarn

```
logWarn<T>(prefix: String = "", value: T): T
```

Helper function that logs messages at `Warn` level. _Introduced in DataWeave version 2.10.0._

- `prefix` — An optional string that typically describes the log.
- `value` — The value to log.

## logWith

```
logWith<T>(level: LogLevel, prefix: String, value: T): T
```

Without changing the value of the input, `logWith` returns the input as a system log at the specified level. This makes it simple to debug your code, because any expression or subexpression can be wrapped with *log* and the result is printed out without modifying the result of the expression. The output is printed in application/dw format. The prefix parameter is optional and allows finding the log output easily. Use the `LogLevel` to categorize log events by severity and control the verbosity of the logs. Use this function to help with debugging DataWeave scripts. A Mule app outputs the results through the `DefaultLoggingService`, which you can see in the Studio console. _Introduced in DataWeave version 2.10.0._

- `level` — Log level that indicates the severity of the event.
- `prefix` — An optional string that typically describes the log.
- `value` — The value to log.

## lower

```
lower(text: String): String
```

Returns the provided string in lowercase characters.

- `text` — The input string.

```dataweave
%dw 2.0
output application/json
---
{ "name" : lower("MULESOFT") }
```

```json
{ "name": "mulesoft" }
```

```
lower(value: Null): Null
```

Helper function that enables `lower` to work with a `null` value.

## map

```
map<T, R>(@StreamCapable items: Array<T>, mapper: (item: T, index: Number) -> R): Array<R>
```

Iterates over items in an array and outputs the results into a new array.

- `items` — The array to map.
- `mapper` — Expression or selector used to act on each `item` and optionally,  each `index` of that item.

```dataweave
%dw 2.0
output application/json
---
["jose", "pedro", "mateo"] map (value, index) -> { (index) : value}
```

```json
[ { "0": "jose" }, { "1": "pedro" }, { "2": "mateo" } ]
```

```
map(@StreamCapable value: Null, mapper: (item: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `map` to work with a `null` value.

## mapObject

```
mapObject<K, V>(@StreamCapable object: { (K)?: V }, mapper: (value: V, key: K, index: Number) -> Object): Object
```

Iterates over an object using a mapper that acts on keys, values, or indices of that object.

- `object` — The object to map.
- `mapper` — Expression or selector that provides the `key`, `value`, or `index` used for mapping the specified object into an output object.

```dataweave
%dw 2.0
output application/json
---
{"a":"b","c":"d"} mapObject (value,key,index) -> { (index) : { (value):key} }
```

```json
{ "0": { "b": "a" }, "1": { "d": "c" } }
```

```
mapObject(value: Null, mapper: (value: Nothing, key: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `mapObject` to work with a `null` value.

## match

```
match(text: String, matcher: Regex): Array<String>
```

Uses a Java regular expression (regex) to match a string and then separates it into capture groups. Returns the results in an array. Note that you can use `match` for pattern matching expressions that include https://docs.mulesoft.com/dataweave/latest/dataweave-pattern-matching[case statements].

- `text` — A string.
- `matcher` — A Java regex for matching characters in the `text`.

```dataweave
%dw 2.0
output application/json
---
"me@mulesoft.com" match(/([a-z]*)@([a-z]*)\.com/)
```

```json
[
  "me@mulesoft.com",
  "me",
  "mulesoft"
]
```

```
match(text: Null, matcher: Any): Null
```

Helper function that enables `match` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## matches

```
matches(text: String, matcher: Regex): Boolean
```

Checks if an expression matches the entire input string. For use cases where you need to output or conditionally process the matched value, see https://docs.mulesoft.com/dataweave/latest/dataweave-pattern-matching[Pattern Matching in DataWeave].

- `text` — The input string.
- `matcher` — A Java regular expression for matching characters in the string.

```dataweave
%dw 2.0
output application/json
---
[ ("admin123" matches /a.*\d+/), ("admin123" matches /^b.+/) ]
```

```json
[ true, false ]
```

```
matches(text: Null, matcher: Any): false
```

Helper function that enables `matches` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## max

```
max<T <: Comparable>(@StreamCapable values: Array<T>): T | Null
```

Returns the highest `Comparable` value in an array. The items must be of the same type, or the function throws an error. The function returns `null` if the array is empty.

- `values` — The input array. The elements in the array can be any supported type.

```dataweave
%dw 2.0
output application/json
---
{ a: max([1, 1000]), b: max([1, 2, 3]), c: max([1.5, 2.5, 3.5]) }
```

```json
{ "a": 1000, "b": 3, "c": 3.5 }
```

## maxBy

```
maxBy<T>(@StreamCapable array: Array<T>, criteria: (item: T) -> Comparable): T | Null
```

Iterates over an array and returns the highest value of `Comparable` elements from it. The items must be of the same type. `maxBy` throws an error if they are not, and the function returns `null` if the array is empty.

- `array` — The input array.
- `criteria` — Expression for selecting an item from the array, where the item is a `Number`, `Boolean`, `DateTime`, `LocalDateTime`, `Date`, `LocalTime`, `Time`, or `TimeZone` data type. Can be referenced with `$`.

```dataweave
%dw 2.0
output  application/json
---
[ { "a" : 1 }, { "a" : 3 }, { "a" : 2 } ] maxBy ((item) -> item.a)
```

```json
{ "a" : 3 }
```

## min

```
min<T <: Comparable>(@StreamCapable values: Array<T>): T | Null
```

Returns the lowest `Comparable` value in an array. The items must be of the same type or `min` throws an error. The function returns `null` if the array is empty.

- `values` — The input array. The elements in the array can be any supported type.

```dataweave
%dw 2.0
output application/json
---
{ a: min([1, 1000]), b: min([1, 2, 3]), c: min([1.5, 2.5, 3.5]) }
```

```json
{ "a": 1, "b": 1, "c": 1.5 }
```

## minBy

```
minBy<T>(@StreamCapable array: Array<T>, criteria: (item: T) -> Comparable): T | Null
```

Iterates over an array to return the lowest value of comparable elements from it. The items need to be of the same type. `minBy` returns an error if they are not, and it returns null when the array is empty.

- `item` — Element in the input array (of type `Number`, `Boolean`, `DateTime`, `LocalDateTime`, `Date`, `LocalTime`, `Time`, or `TimeZone`). Can be referenced with `$`.

```dataweave
%dw 2.0
output  application/json
---
[ { "a" : 1 }, { "a" : 2 }, { "a" : 3 } ] minBy (item) -> item.a
```

```json
{ "a" : 1 }
```

## mod

```
mod(dividend: Number, divisor: Number): Number
```

Returns the modulo (the remainder after dividing the `dividend` by the `divisor`).

- `dividend` — The number that serves as the dividend for the operation.
- `divisor` — The number that serves as the divisor for the operation.

```dataweave
%dw 2.0
output application/json
---
[ (3 mod 2), (4 mod 2), (2.2 mod 2) ]
```

```json
[ 1, 0, 0.2]
```

## namesOf

```
namesOf(obj: Object): Array<String>
```

Returns an array of strings with the names of all the keys within the given object. _Introduced in DataWeave version 2.3.0._

- `obj` — The object to evaluate.

```dataweave
%dw 2.0
output application/json
---
{ "namesOf" : namesOf({ "a" : true, "b" : 1}) }
```

```json
{ "namesOf" : ["a","b"] }
```

```
namesOf(obj: Null): Null
```

Helper function that enables `namesOf` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## native

```
native(String): Nothing
```

Internal method used to indicate that a function implementation is not written in DataWeave but in Scala.

## now

```
now(): DateTime
```

Returns a `DateTime` value for the current date and time. DataWeave delegates to Java `ZonedDateTime.now()`, so the precision of the returned value depends on the underlying JVM and operating system.

```dataweave
%dw 2.0
output application/json
---
{
   nowCalled: now(),
   nowCalledSpecificTimeZone: now() >> "America/New_York"
}
```

```json
{
  "nowCalled": "2019-08-26T13:32:10.64-07:00",
  "nowCalledSpecificTimeZone": "2019-08-26T16:32:10.643-04:00"
}
```

## onNull

```
onNull<R>(previous: Null, callback: () -> R): R
```

Executes a callback function if the preceding expression returns a `null` value and then replaces the `null` value with the result of the callback. _Introduced in DataWeave version 2.4.0._

- `previous` — The value of the preceding expression.
- `callback` — Callback that generates a new value if `previous` returns `null`.

```dataweave
%dw 2.0
output application/json
---
{
     "onNull": []
             reduce ((item, accumulator) -> item ++ accumulator)
             then ((result) -> sizeOf(result))
             onNull "Empty Text"
 }
```

```json
{
  "onNull": "Empty Text"
}
```

```
onNull<T>(previous: T, callback: () -> Any): T
```

Helper function that enables `onNull` to work with a _non-null_ value. _Introduced in DataWeave version 2.4.0._

## orderBy

```
orderBy<K, V, R, O <: { (K)?: V }>(object: O, criteria: (value: V, key: K) -> R): O
```

Reorders the elements of an input using criteria that acts on selected elements of that input. This version of `orderBy` takes an object as input. Other versions act on an input array or handle a `null` value. Note that you can reference the index with the anonymous parameter `$$` and the value with `$`.

- `object` — The object to reorder.
- `criteria` — The result of the function is used as the criteria to reorder the object.

```dataweave
%dw 2.0
output application/json
---
[{ letter: "e" }, { letter: "d" }] orderBy($.letter)
```

```json
[
  {
    "letter": "d"
  },
  {
    "letter": "e"
  }
]
```

```
orderBy<T, R>(array: Array<T>, criteria: (item: T, index: Number) -> R): Array<T>
```

Sorts an array using the specified criteria.

- `array` — The array to sort.
- `criteria` — The result of the function serves as criteria for sorting the array. It should return a simple value (`String`, `Number`, and so on).

```dataweave
%dw 2.0
output application/json
---
[3,2,3] orderBy $
```

```json
[ 2, 3, 3 ]
```

```
orderBy(value: Null, criteria: (item: Nothing, index: Nothing) -> Null): Null
```

Helper function that enables `orderBy` to work with a `null` value.

## pluck

```
pluck<K, V, R>(@StreamCapable object: { (K)?: V }, mapper: (value: V, key: K, index: Number) -> R): Array<R>
```

Useful for mapping an object into an array, `pluck` iterates over an object and returns an array of keys, values, or indices from the object. It is an alternative to `mapObject`, which is similar but returns an object, instead of an array.

- `object` — The object to map.
- `mapper` — Expression or selector that provides the `key`, `value`, and/or `index` (optional) used for mapping the specified object into an array.

```dataweave
%dw 2.0
output application/json
---
{"a":"b","c":"d"} pluck (value,key,index) -> { (index) : { (value):key} }
```

```json
[ { "0": { "b": "a" } }, { "1": { "d": "c" } } ]
```

```
pluck(value: Null, mapper: (value: Nothing, key: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `pluck` to work with a `null` value.

## pow

```
pow(base: Number, power: Number): Number
```

Raises the value of a `base` number to the specified `power`.

- `base` — A number (`Number` type) that serves as the base.
- `power` — A number (`Number` type) that serves as the power.

```dataweave
%dw 2.0
output application/json
---
[ (2 pow 3), (3 pow 2), (7 pow 3) ]
```

```json
[ 8, 9, 343 ]
```

## random

```
random(): Number
```

Returns a pseudo-random number greater than or equal to `0.0` and less than `1.0`.

```dataweave
%dw 2.0
output application/json
---
{ price: random() * 1000 }
```

```json
{ "price": 65.02770292248383 }
```

## randomInt

```
randomInt(upperBound: Number): Number
```

Returns a pseudo-random whole number from `0` to the specified number (exclusive).

- `upperBound` — A number that sets the upper bound of the random number.

```dataweave
%dw 2.0
output application/json
---
{ price: randomInt(1000) }
```

```json
{ "price": 442.0 }
```

## read

```
read(stringToParse: String | Binary, contentType: String = "application/dw", readerProperties: Object = {}): Any
```

Reads a string or binary and returns parsed content. This function can be useful if the reader cannot determine the content type by default.

- `stringToParse` — The string or binary to read.
- `contentType` — A supported format (or content type). Default: `application/dw`.
- `readerProperties` — Optional: Sets reader configuration properties. For other formats and reader configuration properties, see https://docs.mulesoft.com/dataweave/latest/dataweave-formats[Supported Data Formats].

```dataweave
%dw 2.0
output application/xml
---
read('{ "hello" : "world" }','application/json')
```

```json
<?xml version='1.0' encoding='UTF-8'?><hello>world</hello>
```

## readUrl

```
readUrl(url: String, contentType: String = "application/dw", readerProperties: Object = {}): Any
```

Reads a URL, including a classpath-based URL, and returns parsed content. This function works similar to the `read` function. The classpath-based URL uses the `classpath:` protocol prefix, for example: `classpath://myfolder/myFile.txt` where `myFolder` is located under `src/main/resources` in a Mule project. Other than the URL, `readURL` accepts the same arguments as `read`.

- `url` — The URL string to read. It also accepts a classpath-based URL.
- `contentType` — A supported format (or MIME type). Default: `application/dw`.
- `readerProperties` — Optional: Sets reader configuration properties. For other formats and reader configuration properties, see https://docs.mulesoft.com/dataweave/latest/dataweave-formats[Supported Data Formats].

```dataweave
%dw 2.0
output application/json
---
readUrl("https://jsonplaceholder.typicode.com/posts/1", "application/json")
```

```json
{ "userId": 1, "id": 1, "title": "sunt aut ...", "body": "quia et ..." }
```

## reduce

```
reduce<T>(@StreamCapable items: Array<T>, callback: (item: T, accumulator: T) -> T): T | Null
```

Applies a reduction expression to the elements in an array. For each element of the input array, in order, `reduce` applies the reduction lambda expression (function), then replaces the accumulator with the new result. The lambda expression can use both the current input array element and the current accumulator value. Note that if the array is empty and no default value is set on the accumulator parameter, a null value is returned.

- `item` — Item in the input array. It provides the value to reduce. Can also be referenced as `$`.
- `acc` — The accumulator. Can also be referenced as `$$`. Used to store the result of the lambda expression after each iteration of the `reduce` operation. The accumulator parameter can be set to an initial value using the syntax `acc = initValue`. In this case, the lambda expression is called with the first element of the input array. Then the result is set as the new accumulator value. If an initial value for the accumulator is not set, the accumulator is set to the first element of the input array. Then the lambda expression is called with the second element of the input array. The initial value of the accumulator and the lambda expression dictate the type of result produced by the `reduce` function. If the accumulator is set to `acc = {}`, the result is usually of type `Object`. If the accumulator is set to `acc = []`, the result is usually of type `Array`. If the accumulator is set to `acc = ""`, the result is usually a `String`.

```dataweave
%dw 2.0
output application/json
---
[2, 3] reduce ($ + $$)
```

```json
5
```

```
reduce<T, A>(@StreamCapable items: Array<T>, callback: (item: T, accumulator: A) -> A): A
```

```
reduce(@StreamCapable text: String, callback: (item: String, accumulator: String) -> String): String
```

Applies a reduction expression to the characters in a string. For each character of the input string, in order, `reduce` applies the reduction lambda expression (function), then replaces the accumulator with the new result. The lambda expression can use both the current character and the current accumulator value. Note that if the string is empty and no default value is set on the accumulator parameter, an empty string is returned.

- `text` — The string to reduce.
- `callback` — The function to apply.

```dataweave
%dw 2.0
output application/json
---
"hello world" reduce (item, acc = "") -> item ++ acc
```

```json
"dlrow olleh"
```

```
reduce<A>(@StreamCapable text: String, callback: (item: String, accumulator: A) -> A): A
```

```
reduce<T, A>(@StreamCapable items: Null, callback: (item: T, accumulator: A) -> A): Null
```

Helper function that enables `reduce` to work with a `null` value.

## replace

```
replace(text: String, matcher: Regex): ((Array<String>, Number) -> String) -> String
```

Performs string replacement. This version  of `replace` accepts a Java regular expression for matching part of a string. It requires the use of the `with` helper function to specify a replacement string for the matching part of the input string.

- `text` — A string to match.
- `matcher` — A Java regular expression for matching characters in the input `text` string.

```dataweave
%dw 2.0
output application/json
---
["123-456-7890" replace /.*-/ with(""), "abc123def" replace /[b13e]/ with("-")]
```

```json
[ 7890, "a-c-2-d-f" ]
```

```
replace(text: String, matcher: String): ((Array<String>, Number) -> String) -> String
```

Performs string replacement. This version of `replace` accepts a string that matches part of a specified string. It requires the use of the `with` helper function to pass in a replacement string for the matching part of the input string.

- `text` — The string to match.
- `matcher` — The string for matching characters in the input `text` string.

```dataweave
%dw 2.0
output application/json
---
{ "replace": "admin123" replace "123" with("ID") }
```

```json
{ "replace": "adminID" }
```

```
replace(text: Null, matcher: Any): ((Nothing, Nothing) -> Any) -> Null
```

Helper function that enables `replace` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## round

```
round(number: Number): Number
```

Rounds a number up or down to the nearest whole number.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ round(1.2), round(4.6), round(3.5) ]
```

```json
[ 1, 5, 4 ]
```

## scan

```
scan(text: String, matcher: Regex): Array<Array<String>>
```

Returns an array with all of the matches found in an input string. Each match is returned as an array that contains the complete match followed by any capture groups in your regular expression (if present).

- `text` — The input string to scan.
- `regex` — A Java regular expression that describes the pattern match in the `text`.

```dataweave
%dw 2.0
output application/json
---
flatten("www.mulesoft.com" scan(/([w]*)\.([a-z]*)\.([a-z]*)/))
```

```json
[ "www.mulesoft.com", "www", "mulesoft", "com" ]
```

```
scan(text: Null, matcher: Any): Null
```

Helper function that enables `scan` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## sizeOf

```
sizeOf(array: Array<Any>): Number
```

Returns the number of elements in an array. It returns `0` if the array is empty. This version of `sizeOf` takes an array or an array of arrays as input. Other versions act on arrays of objects, strings, or binary values.

- `array` — The input array. The elements in the array can be any supported type.

```dataweave
%dw 2.0
output application/json
---
sizeOf([ "a", "b", "c"])
```

```json
3
```

```
sizeOf(object: Object): Number
```

Returns the number of key-value pairs in an object. This function accepts an array of objects. Returns `0` if the input object is empty.

- `object` — The input object that contains one or more key-value pairs.

```dataweave
%dw 2.0
output application/json
---
sizeOf({a: 1, b: 2})
```

```json
2
```

```
sizeOf(binary: Binary): Number
```

Returns the size of a binary payload in bytes. Returns 0 if the payload is empty.

- `binary` — The input array of binary values.

```dataweave
%dw 2.0
output application/json
---
{

BinarySizeOf: sizeOf("'my word'" as Binary) ++ " " ++ sizeOf("'my word'" as Binary),

StringSizeOf: sizeOf("'my word'") ++ " " ++ sizeOf("'my word'")

}
```

```json
{

"BinarySizeOf": "9 9",

"StringSizeOf": "9 9"

}
```

```
sizeOf(text: String): Number
```

Returns the number of characters (including white space) in an string. Returns `0` if the string is empty.

- `text` — The input text.

```dataweave
%dw 2.0
output application/json
---
sizeOf("abc")
```

```json
3
```

```
sizeOf(value: Period): Number
```

Returns the number of characters in a `Period` value. _Introduced in DataWeave version 2.6.0._

- `value` — The input `Period`.

```dataweave
%dw 2.0
output application/json
---
{
  a: sizeOf(|P3D|)
}
```

```json
{ "a": 3 }
```

```
sizeOf(value: DateTime): Number
```

Returns the number of characters in a `DateTime` value. _Introduced in DataWeave version 2.6.0._

- `value` — The input `DateTime`.

```dataweave
%dw 2.0
output application/json
---
{
  a: sizeOf(|2025-07-13T18:06:59.314033Z|)
}
```

```json
{ "a": 27 }
```

```
sizeOf(value: LocalDateTime): Number
```

Returns the number of characters in a `LocalDateTime` value. _Introduced in DataWeave version 2.6.0._

- `value` — The input `LocalDateTime`.

```dataweave
%dw 2.0
output application/json
---
{
  a: sizeOf(|2025-07-13T18:06:59.314033|)
}
```

```json
{ "a": 26 }
```

```
sizeOf(number: Number): Number
```

Returns the number of characters in a `Number` value. To keep backward compatibility with 2.4, this function returns `1` for any `Number` value when the flag `com.mulesoft.dw.legacySizeOfNumber` is enabled. _Introduced in DataWeave version 2.6.0._

- `number` — The input number.

```dataweave
%dw 2.0
output application/json
---
{
  a: sizeOf(123),
  b: sizeOf(123.45)
}
```

```json
{ "a": 3, "b": 6 }
```

```
sizeOf(n: Null): Null
```

Helper function that enables `sizeOf` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## splitBy

```
splitBy(text: String, regex: Regex): Array<String>
```

Splits a string into a string array based on a value that matches part of that string. It filters out the matching part from the returned array. This version of `splitBy` accepts a Java regular expression (regex) to match the input string. The regex can match any character in the input string. Note that `splitBy` performs the opposite operation of `joinBy`.

- `text` — The input string to split.
- `regex` — A Java regular expression used to split the string. If it does not match some part of the string, the function will return the original, unsplit string in the array.

```dataweave
%dw 2.0
output application/json
---
"192.88.99.0/24" splitBy(/[.\/]/)
```

```json
["192", "88", "99", "0", "24"]
```

```
splitBy(text: String, separator: String): Array<String>
```

Splits a string into a string array based on a separating string that matches part of the input string. It also filters out the matching string from the returned array. The separator can match any character in the input. Note that `splitBy` performs the opposite operation of `joinBy`.

- `text` — The string to split.
- `separator` — A string used to separate the input string. If it does not match some part of the string, the function will return the original, unsplit string in the array.

```dataweave
%dw 2.0
output application/json
---
"192.88.99.0" splitBy(".")
```

```json
["192", "88", "99", "0"]
```

```
splitBy(text: Null, separator: Any)
```

Helper function that enables `splitBy` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## sqrt

```
sqrt(number: Number): Number
```

Returns the square root of a number.

- `number` — The number to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ sqrt(4), sqrt(25), sqrt(100) ]
```

```json
[ 2, 5, 10 ]
```

## startsWith

```
startsWith(text: String, prefix: String): Boolean
```

Returns `true` or `false` depending on whether the input string starts with a matching prefix.

- `text` — The input string.
- `prefix` — A string that identifies the prefix.

```dataweave
%dw 2.0
output application/json
---
[ "Mari" startsWith("Mar"), "Mari" startsWith("Em") ]
```

```json
[ true, false ]
```

```
startsWith(text: Null, prefix: Any): false
```

Helper function that enables `startsWith` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## sum

```
sum(@StreamCapable values: Array<Number>): Number
```

Returns the sum of numeric values in an array. Returns `0` if the array is empty and produces an error when non-numeric values are in the array.

- `values` — The input array of numbers.

```dataweave
%dw 2.0
output application/json
---
sum([1, 2, 3])
```

```json
6
```

## then

```
then(value: Null, callback: (previousResult: Nothing) -> Any): Null
```

Helper function that enables `then` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

```
then<T, R>(previous: T, callback: (result: T) -> R): R
```

This function works as a pipe that passes the value returned from the preceding expression to the next (a callback) only if the value returned by the preceding expression is not `null`. _Introduced in DataWeave version 2.4.0._

- `previous` — The value of the preceding expression.
- `callback` — Callback that processes the result of `previous` if the result is not `null`.

```dataweave
%dw 2.0
output application/json
---
{
    "chainResult": ["mariano", "de Achaval"]
            reduce ((item, accumulator) -> item ++ accumulator)
            then ((result) -> sizeOf(result)),
    "referenceResult" : ["mariano", "de Achaval"]
                         map ((item, index) -> upper(item))
                         then {
                            name: $[0],
                            lastName: $[1],
                            length: sizeOf($)
                        },
    "onNullReturnNull": []
                reduce ((item, accumulator) -> item ++ accumulator)
                then ((result) -> sizeOf(result))
}
```

```json
{
   "chainResult": 17,
   "referenceResult": {
     "name": "MARIANO",
     "lastName": "DE ACHAVAL",
     "length": 2
   },
   "onNullReturnNull": null
 }
```

## to

```
to(from: Number, to: Number): Range
```

Returns a range with the specified boundaries. The upper boundary is inclusive.

- `from` — `Number` value that starts the range. The output includes the `from` value.
- `to` — `Number` value that ends the range. The output includes the `from` value.

```dataweave
%dw 2.0
output application/json
---
{ "myRange": 1 to 10 }
```

```json
{ "myRange": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] }
```

## trim

```
trim(text: String): String
```

Removes any blank spaces from the beginning and end of a string.

- `text` — The string from which to remove any blank spaces.

```dataweave
%dw 2.0
output application/json
---
{ "trim": trim("   my really long  text     ") }
```

```json
{ "trim": "my really long  text" }
```

```
trim(value: Null): Null
```

Helper function that enables `trim` to work with a `null` value.

## typeOf

```
typeOf<T>(value: T): Type<T>
```

Returns the primitive data type of a value, such as `String`. A value's type is taken from its runtime representation and is never one of the arithmetic types (intersection, union, `Any`, or `Nothing`) nor a type alias. If present, metadata of a value is included in the result of `typeOf` (see https://docs.mulesoft.com/dataweave/latest/dw-types-functions-metadataof[metadataOf]).

- `value` — Input value to evaluate.

```dataweave
%dw 2.0
output application/json
---
[ typeOf("A b"), typeOf([1,2]), typeOf(34), typeOf(true), typeOf({ a : 5 }) ]
```

```json
[ "String", "Array", "Number", "Boolean", "Object" ]
```

## unzip

```
unzip<T>(items: Array<Array<T>>): Array<Array<T>>
```

Performs the opposite of `zip`. It takes an array of arrays as input. The function groups the values of the input sub-arrays by matching indices, and it outputs new sub-arrays with the values of those matching indices. No sub-arrays are produced for unmatching indices. For example, if one input sub-array contains four elements (indices 0-3) and another only contains three (indices 0-2), the function will not produce a sub-array for the value at index 3.

- `items` — The input array of arrays.

```dataweave
%dw 2.0
output application/json
---
unzip([ [0,"a"], [1,"b"], [2,"c"],[ 3,"d"] ])
```

```json
[ [ 0, 1, 2, 3 ], [ "a", "b", "c", "d" ] ]
```

## upper

```
upper(text: String): String
```

Returns the provided string in uppercase characters.

- `text` — The string to convert to uppercase.

```dataweave
%dw 2.0
output application/json
---
{ "name" : upper("mulesoft") }
```

```json
{ "name": "MULESOFT" }
```

```
upper(value: Null): Null
```

Helper function that enables `upper` to work with a `null` value.

## uuid

```
uuid(): String
```

Returns a v4 UUID using random numbers as the source.

```dataweave
%dw 2.0
output application/json
---
uuid()
```

```json
"7cc64d24-f2ad-4d43-8893-fa24a0789a99"
```

## valuesOf

```
valuesOf<K, V>(obj: { (K)?: V }): Array<V>
```

Returns an array of the values from key-value pairs in an object. _Introduced in DataWeave version 2.3.0._

- `obj` — The object to evaluate.

```dataweave
%dw 2.0
output application/json
---
{ "valuesOf" : valuesOf({a: true, b: 1}) }
```

```json
{ "valuesOf" : [true,1] }
```

```
valuesOf(obj: Null): Null
```

Helper function that enables `valuesOf` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## with

```
with<V, U, R, X>(toBeReplaced: ((V, U) -> R) -> X, replacer: (V, U) -> R): X
```

Helper function that specifies a replacement element. This function is used with `replace`, `update` or `mask` to perform data substitutions.

- `toBeReplaced` — The value to be replaced.
- `replacer` — The replacement value for the input value.

```dataweave
%dw 2.0
output application/json
---
{ "ssn" : "987-65-4321" replace /[0-9]/ with("x") }
```

```json
{ "ssn": "xxx-xx-xxxx" }
```

## write

```
write(value: Any, contentType: String = "application/dw", writerProperties: Object = {}): String | Binary
```

Writes a value as a string or binary in a supported format. Returns a String or Binary with the serialized representation of the value in the specified format (MIME type). This function can write to a different format than the input. Note that the data must validate in that new format, or an error will occur. For example, `application/xml` content is not valid within an `application/json` format, but `text/plain` can be valid. It returns a `String` value for all text-based data formats (such as XML, JSON , CSV) and a `Binary` value for all the binary formats (such as Excel, MultiPart, OctetStream).

- `value` — The value to write. The value can be of any supported data type.
- `contentType` — A supported format (or MIME type) to write. Default: `application/dw`.
- `writerProperties` — Optional: Sets writer configuration properties. For writer configuration properties (and other supported MIME types), see https://docs.mulesoft.com/dataweave/latest/dataweave-formats[Supported Data Formats].

```dataweave
%dw 2.0
output application/json
---
{ hello : write("world", "text/plain") }
```

```json
{ "hello": "world" }
```

## xsiType

```
xsiType(name: String, namespace: Namespace)
```

Creates a `xsi:type` type attribute. This method returns an object, so it must be used with dynamic attributes. _Introduced in DataWeave version 2.2.2._

- `name` — The name of the schema `type` that is referenced without the prefix.
- `namespace` — The namespace of that type.

```dataweave
%dw 2.0
output application/xml
ns acme http://acme.com
---
  {
      user @((xsiType("user", acme))): {
          name: "Peter",
          lastName: "Parker"
      }
  }
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
 <user xsi:type="acme:user" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:acme="http://acme.com">
     <name>Peter</name>
     <lastName>Parker</lastName>
 </user>
```

## zip

```
zip<T, R>(left: Array<T>, right: Array<R>): Array<Array<T | R>>
```

Merges elements from two arrays into an array of arrays. The first sub-array in the output array contains the first indices of the input sub-arrays. The second index contains the second indices of the inputs, the third contains the third indices, and so on for every case where there are the same number of indices in the arrays.

- `left` — The array on the left-hand side of the function.
- `right` — The array on the right-hand side of the function.

```dataweave
%dw 2.0
output application/json
---
[0,1] zip ["a","b"]
```

```json
[ [0,"a"], [1,"b"] ]
```
