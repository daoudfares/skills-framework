# dw::strings — Strings functions

Namespace `dw::core::Strings`.
Requires an explicit import: `import * from dw::core::Strings`.

Functions: `appendIfMissing`, `camelize`, `capitalize`, `charCode`, `charCodeAt`, `collapse`, `countCharactersBy`, `countMatches`, `dasherize`, `everyCharacter`, `first`, `fromCharCode`, `hammingDistance`, `isAlpha`, `isAlphanumeric`, `isLowerCase`, `isNumeric`, `isUpperCase`, `isWhitespace`, `last`, `leftPad`, `levenshteinDistance`, `lines`, `mapString`, `ordinalize`, `pluralize`, `prependIfMissing`, `remove`, `repeat`, `replaceAll`, `reverse`, `rightPad`, `singularize`, `someCharacter`, `substring`, `substringAfter`, `substringAfterLast`, `substringBefore`, `substringBeforeLast`, `substringBy`, `substringEvery`, `underscore`, `unwrap`, `withMaxSize`, `words`, `wrapIfMissing`, `wrapWith`

---

## appendIfMissing

```
appendIfMissing(text: String, suffix: String): String
```

Appends the `suffix` to the end of the `text` if the `text` does not already ends with the `suffix`. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `suffix` — The text used as the suffix.

```dataweave
%dw 2.0
import appendIfMissing from dw::core::Strings
output application/json
---
{
  "a": appendIfMissing(null, ""),
  "b": appendIfMissing("abc", ""),
  "c": appendIfMissing("", "xyz") ,
  "d": appendIfMissing("abc", "xyz") ,
  "e": appendIfMissing("abcxyz", "xyz")
}
```

```json
{
  "a": null,
  "b": "abc",
  "c": "xyz",
  "d": "abcxyz",
  "e": "abcxyz"
}
```

```
appendIfMissing(text: Null, suffix: String): Null
```

Helper function that enables `appendIfMissing` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## camelize

```
camelize(text: String): String
```

Returns a string in camel case based on underscores in the string. All underscores are deleted, including any underscores at the beginning of the string.

- `text` — The string to convert to camel case.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a" : camelize("customer_first_name"),
  "b" : camelize("_name_starts_with_underscore")
}
```

```json
{
   "a": "customerFirstName",
   "b": "nameStartsWithUnderscore"
 }
```

```
camelize(text: Null): Null
```

Helper function that enables `camelize` to work with a `null` value.

## capitalize

```
capitalize(text: String): String
```

Capitalizes the first letter of each word in a string. The function treats every non-alphabetic character as a separator and replaces underscores with spaces. For example, `capitalize("a*s_b’s")` results in `"A*S B’S"`.

- `text` — The string to capitalize.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a" : capitalize("customer"),
  "b" : capitalize("customer_first_name"),
  "c" : capitalize("customer NAME"),
  "d" : capitalize("customerName"),
  "e" : capitalize("a*s_b’s")
}
```

```json
{
  "a": "Customer",
  "b": "Customer First Name",
  "c": "Customer Name",
  "d": "Customer Name",
  "e": "A*S B’S"
}
```

```
capitalize(text: Null): Null
```

Helper function that enables `capitalize` to work with a `null` value.

## charCode

```
charCode(text: String): Number
```

Returns the Unicode for the first character in an input string. For an empty string, the function fails and returns `Unexpected empty string`.

- `text` — The input string.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "charCode" : charCode("Mule")
}
```

```xml
{ "charCode" : 77 }
```

```
charCode(text: Null): Null
```

Helper function that enables `charCode` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## charCodeAt

```
charCodeAt(content: String, position: Number): Number
```

Returns the Unicode for a character at the specified index. This function fails if the index is invalid.

- `content` — The input string.
- `position` — The index (a `Number` type) of a character in the string (as a string array). Note that the index of the first character is `0`.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "charCodeAt" : charCodeAt("MuleSoft", 1)
}
```

```json
{ "charCodeAt": 117 }
```

```
charCodeAt(content: Null, position: Any): Null
```

Helper function that enables `charCodeAt` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## collapse

```
collapse(text: String): Array<String>
```

Collapses the string into substrings of equal characters. Each substring contains a single character or identical characters that are adjacent to one another in the input string. Empty spaces are treated as characters. _Introduced in DataWeave version 2.4.0._

- `text` — The string to collapse.

```dataweave
%dw 2.0
import collapse from dw::core::Strings
output application/json
---
collapse("a  b babb a")
```

```json
["a", "  ", "b", " ", "b", "a", "bb", " ", "a"]
```

```
collapse(text: Null): Null
```

Helper function that enables `collapse` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## countCharactersBy

```
countCharactersBy(text: String, predicate: (character: String) -> Boolean): Number
```

Counts the number of times an expression that iterates through each character in a string returns `true`. _Introduced in DataWeave version 2.4.0._

- `text` — The string to which the `predicate` applies.
- `predicate` — Expression to apply to each character in the `text` string. The expression must return a Boolean value.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
"42 = 11 * 2 + 20" countCharactersBy isNumeric($)
```

```json
7
```

```
countCharactersBy(text: Null, predicate: (character: Nothing) -> Any): Null
```

Helper function to make `countCharactersBy` work with a `null` value. _Introduced in DataWeave version 2.4.0._

## countMatches

```
countMatches(text: String, pattern: String): Number
```

Counts the number of matches in a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to search for matches.
- `pattern` — A substring to find in the text.

```dataweave
%dw 2.0
import countMatches from dw::core::Strings
output application/json
---
"hello worlo!" countMatches "lo"
```

```json
2
```

```
countMatches(text: String, pattern: Regex): Number
```

Counts the number of times a regular expression matches text in a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to search for matches.
- `pattern` — The regex pattern to use in the search.

```dataweave
%dw 2.0
import countMatches from dw::core::Strings
output application/json
---
"hello, ciao!" countMatches /[aeiou]/
```

```json
5
```

```
countMatches(text: Null, pattern: Any): Null
```

Helper function that enables `countMatches` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## dasherize

```
dasherize(text: String): String
```

Replaces spaces, underscores, and camel-casing in a string with dashes (hyphens). If no spaces, underscores, and camel-casing are present, the output will match the input.

- `text` — The input string.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a" : dasherize("customer"),
  "b" : dasherize("customer_first_name"),
  "c" : dasherize("customer NAME"),
  "d" : dasherize("customerName")
}
```

```json
{
  "a": "customer",
  "b": "customer-first-name",
  "c": "customer-name",
  "d": "customer-name"
}
```

```
dasherize(text: Null): Null
```

Helper function that enables `dasherize` to work with a `null` value.

## everyCharacter

```
everyCharacter(text: String, condition: (character: String) -> Boolean): Boolean
```

Checks whether a condition is valid for _every_ character in a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to check.
- `condition` — Expression that iterates through the characters in the string that it checks and returns a Boolean value.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
"12 34  56" everyCharacter $ == " " or isNumeric($)
```

```json
true
```

```
everyCharacter(text: Null, condition: (character: Nothing) -> Any): true
```

Helper function that enables `everyCharacter` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## first

```
first(text: String, amount: Number): String
```

Returns characters from the beginning of a string to the specified number of characters in the string, for example, the first two characters of a string. If the number is equal to or greater than the number of characters in the string, the function returns the entire string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to process.
- `amount` — The number of characters to return. Negative numbers and `0` return an empty string. Decimals are rounded down to the nearest whole number.

```dataweave
%dw 2.0
import first from dw::core::Strings
output application/json
---
"hello world!" first 5
```

```json
"hello"
```

```
first(text: Null, amount: Any): Null
```

Helper function that enables `first` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## fromCharCode

```
fromCharCode(charCode: Number): String
```

Returns a character that matches the specified Unicode.

- `charCode` — The input Unicode (a `Number`).

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "fromCharCode" : fromCharCode(117)
}
```

```json
{ "fromCharCode": "u" }
```

```
fromCharCode(charCode: Null): Null
```

Helper function that enables `fromCharCode` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## hammingDistance

```
hammingDistance(a: String, b: String): Number | Null
```

Returns the Hamming distance between two strings. _Introduced in DataWeave version 2.4.0._

- `a` — The first string.
- `b` — The second string.

```dataweave
%dw 2.0
import hammingDistance from dw::core::Strings
output application/json
---
"holu" hammingDistance "chau"
```

```json
3
```

## isAlpha

```
isAlpha(text: String): Boolean
```

Checks if the `text` contains only Unicode digits. This excludes digits, punctuation, and other nonletter characters. Note that the method does not allow for a leading sign, either positive or negative. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.

```dataweave
%dw 2.0
import isAlpha from dw::core::Strings
output application/json
---
{
  "a": isAlpha(null),
  "b": isAlpha(""),
  "c": isAlpha("  "),
  "d": isAlpha("abc"),
  "e": isAlpha("ab2c"),
  "f": isAlpha("ab-c")
}
```

```json
{
  "a": false,
  "b": false,
  "c": false,
  "d": true,
  "e": false,
  "f": false
}
```

```
isAlpha(text: Null): Boolean
```

Helper function that enables `isAlpha` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## isAlphanumeric

```
isAlphanumeric(text: String): Boolean
```

Checks if the `text` contains only Unicode letters or digits. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.

```dataweave
%dw 2.0
import isAlphanumeric from dw::core::Strings
output application/json
---
{
  "a": isAlphanumeric(null),
  "b": isAlphanumeric(""),
  "c": isAlphanumeric("  "),
  "d": isAlphanumeric("abc"),
  "e": isAlphanumeric("ab c"),
  "f": isAlphanumeric("ab2c"),
  "g": isAlphanumeric("ab-c")
}
```

```json
{
  "a": false,
  "b": false,
  "c": false,
  "d": true,
  "e": false,
  "f": true,
  "g": false
}
```

```
isAlphanumeric(text: Null): Boolean
```

Helper function that enables `isAlphanumeric` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## isLowerCase

```
isLowerCase(text: String): Boolean
```

Checks if the `text` contains only lowercase Unicode characters. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.

```dataweave
%dw 2.0
import isLowerCase from dw::core::Strings
output application/json
---
{
  "a": isLowerCase(null),
  "b": isLowerCase(""),
  "c": isLowerCase("  "),
  "d": isLowerCase("abc"),
  "e": isLowerCase("aBC"),
  "f": isLowerCase("a c"),
  "g": isLowerCase("a1c"),
  "h": isLowerCase("a/c"),
  "i": isLowerCase("mulesöft"),
  "j": isLowerCase("mulesÖft")
}
```

```json
{
  "a": false,
  "b": false,
  "c": false,
  "d": false,
  "e": false,
  "f": false,
  "g": false,
  "h": false,
  "i": true,
  "j": false
}
```

```
isLowerCase(text: Null): Boolean
```

Helper function that enables `isLowerCase` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## isNumeric

```
isNumeric(text: String): Boolean
```

Checks if the `text` contains only Unicode digits. A decimal point is not a Unicode digit and returns false. Note that the method does not allow for a leading sign, either positive or negative. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.

```dataweave
%dw 2.0
import isNumeric from dw::core::Strings
output application/json
---
{
  "a": isNumeric(null),
  "b": isNumeric(""),
  "c": isNumeric("  "),
  "d": isNumeric("123"),
  "e": isNumeric("१२३"),
  "f": isNumeric("12 3"),
  "g": isNumeric("ab2c"),
  "h": isNumeric("12-3"),
  "i": isNumeric("12.3"),
  "j": isNumeric("-123"),
  "k": isNumeric("+123")
}
```

```json
{
  "a": false,
  "b": false,
  "c": false,
  "d": true,
  "e": true,
  "f": false,
  "g": false,
  "h": false,
  "i": false,
  "j": false,
  "k": false
}
```

```
isNumeric(text: Null): Boolean
```

Helper function that enables `isNumeric` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## isUpperCase

```
isUpperCase(text: String): Boolean
```

Checks if the `text` contains only uppercase characters. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.

```dataweave
%dw 2.0
import isUpperCase from dw::core::Strings
output application/json
---
{
  "a": isUpperCase(null),
  "b": isUpperCase(""),
  "c": isUpperCase("  "),
  "d": isUpperCase("ABC"),
  "e": isUpperCase("aBC"),
  "f": isUpperCase("A C"),
  "g": isUpperCase("A1C"),
  "h": isUpperCase("A/C")
}
```

```json
{
  "a": false,
  "b": false,
  "c": false,
  "d": true,
  "e": false,
  "f": false,
  "g": false,
  "h": false
}
```

```
isUpperCase(text: Null): Boolean
```

Helper function that enables `isUpperCase` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## isWhitespace

```
isWhitespace(text: String): Boolean
```

Checks if the `text` contains only whitespace. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.

```dataweave
%dw 2.0
import isWhitespace from dw::core::Strings
output application/json
---
{
  "a": isWhitespace(null),
  "b": isWhitespace(""),
  "c": isWhitespace("  "),
  "d": isWhitespace("abc"),
  "e": isWhitespace("ab2c"),
  "f": isWhitespace("ab-c")
}
```

```json
{
  "a": false,
  "b": true,
  "c": true,
  "d": false,
  "e": false,
  "f": false
}
```

```
isWhitespace(text: Null): Boolean
```

Helper function that enables `isWhitespace` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## last

```
last(text: String, amount: Number): String
```

Returns characters from the end of string to a specified number of characters, for example, the last two characters of a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to process.
- `amount` — The number of characters to return. Negative numbers and `0` return an empty string. Decimals are rounded up to the nearest whole number.

```dataweave
%dw 2.0
import last from dw::core::Strings
output application/json
---
"hello world!" last 6
```

```json
"world!"
```

```
last(text: Null, amount: Any): Null
```

Helper function that enables `last` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## leftPad

```
leftPad(text: String, size: Number, padText: String = " "): String
```

The specified `text` is _left_-padded to the `size` using the `padText`. By default `padText` is `" "`. Returns left-padded `String` or original `String` if no padding is necessary. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `size` — The size to pad to.
- `padText` — The text to pad with. It defaults to one space if not specified.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
   "a": leftPad(null, 3),
   "b": leftPad("", 3),
   "c": leftPad("bat", 5),
   "d": leftPad("bat", 3),
   "e": leftPad("bat", -1)
}
```

```json
{
  "a": null,
  "b": "   ",
  "c": "  bat",
  "d": "bat",
  "e": "bat"
}
```

```
leftPad(text: Null, size: Any, padText: Any = " "): Null
```

Helper function that enables `leftPad` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## levenshteinDistance

```
levenshteinDistance(a: String, b: String): Number
```

Returns the Levenshtein distance (or edit distance) between two strings. _Introduced in DataWeave version 2.4.0._

- `a` — The first string.
- `b` — The second string.

```dataweave
%dw 2.0
import levenshteinDistance from dw::core::Strings
output application/json
---
"kitten" levenshteinDistance "sitting"
```

```json
3
```

## lines

```
lines(text: String): Array<String>
```

Returns an array of lines from a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to split into lines.

```dataweave
%dw 2.0
import lines from dw::core::Strings
output application/json
---
lines("hello world\n\nhere   data-weave")
```

```json
["hello world", "", "here   data-weave"]
```

```
lines(text: Null): Null
```

Helper function that enables `lines` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## mapString

```
mapString(@StreamCapable text: String, mapper: (character: String, index: Number) -> String): String
```

Applies an expression to every character of a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to map.
- `mapper` — Expression that applies to each character (`$`) or index (`$$`) of the `text` string and returns a string.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{ balance: ("\$234" mapString if (isNumeric($)) "~" else $) }
```

```json
{
  "balance": "$~~~"
}
```

```
mapString(@StreamCapable text: Null, mapper: (character: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `mapString` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## ordinalize

```
ordinalize(num: Number): String
```

Returns a number as an ordinal, such as `1st` or `2nd`.

- `num` — An input number to return as an ordinal.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a" : ordinalize(1),
  "b": ordinalize(2),
  "c": ordinalize(5),
  "d": ordinalize(103)
}
```

```json
{
   "a": "1st",
   "b": "2nd",
   "c": "5th",
   "d": "103rd"
}
```

```
ordinalize(num: Null): Null
```

Helper function that enables `ordinalize` to work with a `null` value.

## pluralize

```
pluralize(text: String): String
```

Pluralizes a singular string. If the input is already plural (for example, "boxes"), the output will match the input.

- `text` — The string to pluralize.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
 { "pluralize" : pluralize("box") }
```

```json
{ "pluralize" : "boxes" }
```

```
pluralize(text: Null): Null
```

Helper function that enables `pluralize` to work with a `null` value.

## prependIfMissing

```
prependIfMissing(text: String, prefix: String): String
```

Prepends the `prefix` to the beginning of the string if the `text` does not already start with that prefix. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `prefix` — The text to use as prefix.

```dataweave
%dw 2.0
import prependIfMissing from dw::core::Strings
output application/json
---
{
  "a": prependIfMissing(null, ""),
  "b": prependIfMissing("abc", ""),
  "c": prependIfMissing("", "xyz"),
  "d": prependIfMissing("abc", "xyz"),
  "e": prependIfMissing("xyzabc", "xyz")
}
```

```json
{
  "a": null,
  "b": "abc",
  "c": "xyz",
  "d": "xyzabc",
  "e": "xyzabc"
}
```

```
prependIfMissing(text: Null, prefix: String): Null
```

Helper function that enables `prependIfMissing` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## remove

```
remove(text: String, toRemove: String): String
```

Removes all occurrences of a specified pattern from a string. _Introduced in DataWeave version 2.4.0._

- `text` — The text to remove from.
- `toRemove` — The pattern to remove.

```dataweave
%dw 2.0
import remove from dw::core::Strings
output application/json
---
"lazyness purity state higher-order stateful" remove "state"
```

```json
"lazyness purity  higher-order ful"
```

```
remove(text: Null, toRemove: Any): Null
```

Helper function that enables `remove` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## repeat

```
repeat(text: String, times: Number): String
```

Repeats a `text` the number of specified `times`. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `times` — Number of times to repeat char. Negative is treated as zero.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": repeat("e", 0),
  "b": repeat("e", 3),
  "c": repeat("e", -2)
}
```

```json
{
  "a": "",
  "b": "eee",
  "c": ""
}
```

```
repeat(text: Null, times: Any): Null
```

Helper function that enables `repeat` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## replaceAll

```
replaceAll(text: String, target: String, replacement: String): String
```

Replaces all substrings that match a literal search string with a specified replacement string. Replacement proceeds from the beginning of the string to the end. For example, the result of replacing `"aa"` with `"b"` in the string` `"aaa"` is `"ba"`, rather than `"ab"`. _Introduced in DataWeave version 2.4.0._

- `text` — The string to search.
- `target` — The string to find and replace in `text`.
- `replacement` — The replacement string.

```dataweave
import * from dw::core::Strings
output application/json
---
{
    a: replaceAll("Mariano", "a" , "A"),
    b: replaceAll("AAAA", "AAA" , "B"),
    c: replaceAll(null, "aria" , "A"),
    d: replaceAll("Mariano", "j" , "Test"),
}
```

```json
{
   "a": "MAriAno",
   "b": "BA",
   "c": null,
   "d": "Mariano"
 }
```

```
replaceAll(text: Null, oldValue: String, newValue: String): Null
```

Helper function that enables `replaceAll` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## reverse

```
reverse(text: String): String
```

Reverses sequence of characters in a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to reverse.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
 {
     a: reverse("Mariano"),
     b: reverse(null),
     c: reverse("")
 }
```

```json
{
  "a": "onairaM",
  "b": null,
  "c": ""
}
```

```
reverse(text: Null): Null
```

Helper function that enables `reverse` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## rightPad

```
rightPad(text: String, size: Number, padChar: String = " "): String
```

The specified `text` is _right_-padded to the `size` using the `padText`. By default `padText` is `" "`. Returns right padded `String` or original `String` if no padding is necessary. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `size` — The size to pad to.
- `padText` — The text to pad with. It defaults to one space if not specified.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": rightPad(null, 3),
  "b": rightPad("", 3),
  "c": rightPad("bat", 5),
  "d": rightPad("bat", 3),
  "e": rightPad("bat", -1)
}
```

```json
{
  "a": null,
  "b": "   ",
  "c": "bat  ",
  "d": "bat",
  "e": "bat"
}
```

```
rightPad(text: Null, size: Any, padText: Any = " "): Null
```

Helper function that enables `rightPad` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## singularize

```
singularize(text: String): String
```

Converts a plural string to its singular form. If the input is already singular (for example, "box"), the output will match the input.

- `text` — The string to convert to singular form.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{ "singularize" : singularize("boxes") }
```

```json
{ "singularize" : "box" }
```

```
singularize(text: Null): Null
```

Helper function that enables `singularize` to work with a `null` value.

## someCharacter

```
someCharacter(text: String, condition: (character: String) -> Boolean): Boolean
```

Checks whether a condition is valid for at least one of the characters or blank spaces in a string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to check.
- `condition` — Expression that iterates through the characters and spaces in the string and returns a Boolean value.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
"someCharacter" someCharacter isUpperCase($)
```

```json
true
```

```
someCharacter(text: Null, condition: (character: Nothing) -> Any): false
```

Helper function that enables `someCharacter` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## substring

```
substring(text: String, from: Number, until: Number): String
```

Returns a substring that spans from the character at the specified `from` index to the last character before the `until` index. The characters in the substring satisfy the condition `from <= indexOf(string) < until`. _Introduced in DataWeave version 2.4.0._

- `text` — The string, treated as an array of characters.
- `from` — The lowest index to include from the character array.
- `until` — The lowest index to exclude from the character array.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
var text = "hello world!"
---
substring(text, 1, 5)
```

```json
"ello"
```

```
substring(text: Null, from: Any, until: Any): Null
```

Helper function that enables `substring` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## substringAfter

```
substringAfter(text: String, separator: String): String
```

Gets the substring after the first occurrence of a separator. The separator is not returned. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `separator` — String to search for.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": substringAfter(null, "'"),
  "b": substringAfter("", "-"),
  "c": substringAfter("abc", "b"),
  "d": substringAfter("abcba", "b"),
  "e": substringAfter("abc", "d"),
  "f": substringAfter("abc", "")
}
```

```json
{

  "a": null,
  "b": "",
  "c": "c",
  "d": "cba",
  "e": "",
  "f": "abc"
}
```

```
substringAfter(text: Null, separator: String): Null
```

Helper function that enables `substringAfter` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## substringAfterLast

```
substringAfterLast(text: String, separator: String): String
```

Gets the substring after the last occurrence of a separator. The separator is not returned. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `separator` — String to search for.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": substringAfterLast(null, "'"),
  "b": substringAfterLast("", "-"),
  "c": substringAfterLast("abc", "b"),
  "d": substringAfterLast("abcba", "b"),
  "e": substringAfterLast("abc", "d"),
  "f": substringAfterLast("abc", "")
}
```

```json
{
 "a": null,
 "b": "",
 "c": "c",
 "d": "a",
 "e": "",
 "f": null
}
```

```
substringAfterLast(text: Null, separator: String): Null
```

Helper function that enables `substringAfterLast` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## substringBefore

```
substringBefore(text: String, separator: String): String
```

Gets the substring before the first occurrence of a separator. The separator is not returned. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `separator` — String to search for.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": substringBefore(null, "'"),
  "b": substringBefore("", "-"),
  "c": substringBefore("abc", "b"),
  "d": substringBefore("abc", "c"),
  "e": substringBefore("abc", "d"),
  "f": substringBefore("abc", "")
}
```

```json
{
  "a": null,
  "b": "",
  "c": "a",
  "d": "ab",
  "e": "",
  "f": ""
}
```

```
substringBefore(text: Null, separator: String): Null
```

Helper function that enables `substringBefore` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## substringBeforeLast

```
substringBeforeLast(text: String, separator: String): String
```

Gets the substring before the last occurrence of a separator. The separator is not returned. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `separator` — String to search for.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": substringBeforeLast(null, "'"),
  "b": substringBeforeLast("", "-"),
  "c": substringBeforeLast("abc", "b"),
  "d": substringBeforeLast("abcba", "b"),
  "e": substringBeforeLast("abc", "d"),
  "f": substringBeforeLast("abc", "")
}
```

```json
{
  "a": null,
  "b": "",
  "c": "a",
  "d": "abc",
  "e": "",
  "f": "ab"
}
```

```
substringBeforeLast(text: Null, separator: String): Null
```

Helper function that enables `substringBeforeLast` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## substringBy

```
substringBy(text: String, predicate: (character: String, index: Number) -> Boolean): Array<String>
```

Splits a string at each character where the `predicate` expression returns `true`. _Introduced in DataWeave version 2.4.0._

- `text` — The string to split. The string is treated as an array of characters.
- `predicate` — Expression that tests each character and returns a Boolean value. The expression can iterate over each character and index of the string.

```dataweave
%dw 2.0
import substringBy from dw::core::Strings
output application/json
---
"hello~world=here_data-weave" substringBy $ == "~" or $ == "=" or $ == "_"
```

```json
["hello", "world", "here", "data-weave"]
```

```
substringBy(text: Null, predicate: (character: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `substringBy` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## substringEvery

```
substringEvery(text: String, amount: Number): Array<String>
```

Splits a string into an array of substrings equal to a specified length. The last substring can be shorter than that length. If the length is greater than or equal to the length of the string to split, the function returns the entire string. _Introduced in DataWeave version 2.4.0._

- `text` — The string to split.
- `amount` — The desired length of each substring.

```dataweave
%dw 2.0
import substringEvery from dw::core::Strings
output application/json
---
substringEvery("substringEvery", 3)
```

```json
["sub", "str", "ing", "Eve", "ry"]
```

```
substringEvery(text: Null, amount: Any): Null
```

Helper function that enables `substringEvery` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## underscore

```
underscore(text: String): String
```

Replaces hyphens, spaces, and camel-casing in a string with underscores. If no hyphens, spaces, and camel-casing are present, the output will match the input.

- `text` — The input string.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
   "a" : underscore("customer"),
   "b" : underscore("customer-first-name"),
   "c" : underscore("customer NAME"),
   "d" : underscore("customerName")
}
```

```json
{
   "a": "customer",
   "b": "customer_first_name",
   "c": "customer_name",
   "d": "customer_name"
}
```

```
underscore(text: Null): Null
```

Helper function that enables `underscore` to work with a `null` value.

## unwrap

```
unwrap(text: String, wrapper: String): String
```

Unwraps a given `text` from a `wrapper` text. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `wrapper` — The text used to unwrap.

```dataweave
%dw 2.0
import unwrap from dw::core::Strings
output application/json
---
{
  "a": unwrap(null, ""),
  "b": unwrap(null, '\0'),
  "c": unwrap("'abc'", "'"),
  "d": unwrap("AABabcBAA", 'A'),
  "e": unwrap("A", '#'),
  "f": unwrap("#A", '#'),
  "g": unwrap("A#", '#')
}
```

```json
{
   "a": null,
   "b": null,
   "c": "abc",
   "d": "ABabcBA",
   "e": "A",
   "f": "#A",
   "g": "A#"
 }
```

```
unwrap(text: Null, wrapper: String): Null
```

Helper function that enables `unwrap` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## withMaxSize

```
withMaxSize(text: String, maxLength: Number): String
```

Checks that the string length isn't greater than the specified `maxLength`. If the string is longer, the function returns a substring that starts at the beginning of the string and is `maxLength` characters long. _Introduced in DataWeave version 2.3.0._

- `text` — The input string.
- `maxLength` — The maximum length of the string.

```dataweave
%dw 2.0
import withMaxSize from dw::core::Strings
output application/json
---
{
   a: "123" withMaxSize 10,
   b: "123" withMaxSize 3,
   c: "123" withMaxSize 2,
   d: "123" withMaxSize 0,
   e: null withMaxSize 23,
}
```

```json
{
  "a": "123",
  "b": "123",
  "c": "12",
  "d": "123",
  "e": null
}
```

```
withMaxSize(text: Null, maxLength: Number): Null
```

Helper function that enables `withMaxSize` to work with a `null` value. _Introduced in DataWeave version 2.3.0._

## words

```
words(text: String): Array<String>
```

Returns an array of words from a string. Separators between words include blank spaces, new lines, and tabs. _Introduced in DataWeave version 2.4.0._

- `text` — The string to split into words.

```dataweave
%dw 2.0
import words from dw::core::Strings
output application/json
---
words("hello world\nhere\t\t\tdata-weave")
```

```json
["hello", "world", "here", "data-weave"]
```

```
words(text: Null): Null
```

Helper function that enables `words` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## wrapIfMissing

```
wrapIfMissing(text: String, wrapper: String): String
```

Wraps `text` with `wrapper` if that `wrapper` is missing from the start or end of the given string. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `wrapper` — The content used to wrap.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
 {
   "a": wrapIfMissing(null, "'"),
   "b": wrapIfMissing("", "'"),
   "c": wrapIfMissing("ab", "x"),
   "d": wrapIfMissing("'ab'", "'"),
   "e": wrapIfMissing("/", '/'),
   "f": wrapIfMissing("a/b/c", '/'),
   "g": wrapIfMissing("/a/b/c", '/'),
   "h": wrapIfMissing("a/b/c/", '/')
 }
```

```json
{
   "a": null,
   "b": "'",
   "c": "xabx",
   "d": "'ab'",
   "e": "/",
   "f": "/a/b/c/",
   "g": "/a/b/c/",
   "h": "/a/b/c/"
 }
```

```
wrapIfMissing(text: Null, wrapper: String): Null
```

Helper function that enables `wrapIfMissing` to work with a `null` value. _Introduced in DataWeave version 2.2.0._

## wrapWith

```
wrapWith(text: String, wrapper: String): String
```

Wraps the specified `text` with the given `wrapper`. _Introduced in DataWeave version 2.2.0._

- `text` — The input string.
- `wrapper` — The content used to wrap.

```dataweave
%dw 2.0
import * from dw::core::Strings
output application/json
---
{
  "a": wrapWith(null, "'"),
  "b": wrapWith("", "'"),
  "c": wrapWith("ab", "x"),
  "d": wrapWith("'ab'", "'"),
  "e": wrapWith("ab", "'")
}
```

```json
{
  "a": null,
  "b": "''",
  "c": "xabx",
  "d": "''ab''",
  "e": "'ab'"
}
```

```
wrapWith(text: Null, wrapper: Any): Null
```

Helper function that enables `wrapWith` to work with a `null` value. _Introduced in DataWeave version 2.2.0._
