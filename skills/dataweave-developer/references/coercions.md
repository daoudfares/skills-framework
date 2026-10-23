# dw::coercions — Coercions functions

Namespace `dw::util::Coercions`.
Requires an explicit import: `import * from dw::util::Coercions`.

Functions: `toArray`, `toBinary`, `toBoolean`, `toDate`, `toDateOrNull`, `toDateTime`, `toDateTimeOrNull`, `toLocalDateTime`, `toLocalDateTimeOrNull`, `toLocalTime`, `toLocalTimeOrNull`, `toNumber`, `toNumberOrNull`, `toPeriod`, `toRegex`, `toString`, `toTime`, `toTimeOrNull`, `toTimeZone`, `toUri`

---

## toArray

```
toArray(@StreamCapable text: String): Array<String>
```

Splits a `String` value into an `Array` of characters. _Introduced in DataWeave version 2.4.0._

- `text` — The `String` value to transform into an `Array` of characters (a `Array<String>` type).

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json indent=false
---
{
  a: toArray(""),
  b: toArray("hola")
}
```

```json
{"a": [],"b": ["h","o","l","a"]}
```

## toBinary

```
toBinary(str: String, encoding: String): Binary
```

Transform a `String` value into a `Binary` value using the specified encoding. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Binary` value.
- `encoding` — The encoding to apply to the `String` value. Accepts encodings that are supported by your JDK. For example, `encoding` accepts Java canonical names and aliases for the basic and extended encoding sets in Oracle JDK 8 and JDK 11.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  'UTF-16Ex': toBinary("DW", "UTF-16"),
  'utf16Ex': toBinary("DW", "utf16"),
  'UnicodeBigEx': toBinary("DW", "UnicodeBig"),
  'UTF-32Ex': toBinary("DW", "UTF-32"),
  'UTF_32Ex': toBinary("DW", "UTF_32")
}
```

```json
{
  "UTF-16Ex": "/v8ARABX" as Binary {base: "64"},
  utf16Ex: "/v8ARABX" as Binary {base: "64"},
  UnicodeBigEx: "/v8ARABX" as Binary {base: "64"},
  "UTF-32Ex": "AAAARAAAAFc=" as Binary {base: "64"},
  UTF_32Ex: "AAAARAAAAFc=" as Binary {base: "64"}
}
```

## toBoolean

```
toBoolean(str: String): Boolean
```

Transform a `String` value into a `Boolean` value. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Boolean` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
  a: toBoolean("true"),
  b: toBoolean("false"),
  c: toBoolean("FALSE"),
  d: toBoolean("TrUe")
}
```

```json
{
  "a": true,
  "b": false,
  "c": false,
  "d": true
}
```

## toDate

```
toDate(str: String, formatters: Array<Formatter>): Date
```

Transforms a `String` value into a `Date` value using the first `Formatter` that matches with the given value to transform. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `Date` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
import * from dw::Runtime
output application/dw
---
{
  a: toDate("2023-28-03", [{format: "yyyy/MM/dd"}, {format: "yyyy-dd-MM", locale: "en_US"}]),
  b: try(() -> toDate("2023-28-03", [{format: "yyyy/MM/dd"}])).error.message
}
```

```dataweave
{
  a: |2023-03-28| as Date {format: "yyyy-dd-MM", locale: "en_US"},
  b: "Could not find a valid formatter for '2023-28-03'"
}
```

```
toDate(str: String, format: String | Null = null, locale: String | Null = null): Date
```

Transforms a `String` value into a `Date` value and accepts a format and locale. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Date` value.
- `format` — The formatting to use on the `Date` value. A `null` value has no effect on the `Date` value. This parameter accepts Java character patterns based on ISO-8601. A `Date` value, such as `2011-12-03`, has the format `uuuu-MM-dd`.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toDate("2015-10-01"),
  b: toDate("2003/10/01","uuuu/MM/dd")
}
```

```dataweave
{
  a: |2015-10-01|,
  b: |2003-10-01| as Date {format: "uuuu/MM/dd"}
}
```

## toDateOrNull

```
toDateOrNull(str: String, formatters: Array<Formatter>): Date | Null
```

Transforms a `String` value into a `Date` value using the first `Formatter` that matches with the given value to transform. If none of the `Formatter` matches with the given value, the function returns a `null` value. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `Date` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toDateOrNull("2023-28-03", [{format: "yyyy/MM/dd"}, {format: "yyyy-dd-MM", locale: "en_US"}]),
  b: toDateOrNull("2023-28-03", [{format: "yyyy/MM/dd"}])
}
```

```dataweave
{
  a: |2023-03-28| as Date {format: "yyyy-dd-MM", locale: "en_US"},
  b: null
}
```

## toDateTime

```
toDateTime(str: String, formatters: Array<Formatter>): DateTime
```

Transforms a `String` value into a `DateTime` value using the first `Formatter` that matches with the given value to transform. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `DateTime` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
import * from dw::Runtime
output application/dw
---
{
  a: toDateTime("2003-10-01 23:57:59Z", [{format: "uuuu/MM/dd HH:mm:ssz"}, {format: "uuuu-MM-dd HH:mm:ssz"}]),
  b: try(() -> toDateTime("2003-10-01 23:57:59Z", [{format: "uuuu/MM/dd HH:mm:ssz"}])).error.message
}
```

```dataweave
{
  a: |2003-10-01T23:57:59Z| as DateTime {format: "uuuu-MM-dd HH:mm:ssz"},
  b: "Could not find a valid formatter for '2003-10-01 23:57:59Z'"
}
```

```
toDateTime(number: Number, unit: MillisOrSecs | Null = null): DateTime
```

Transforms a `Number` value into a `DateTime` value using `milliseconds` or `seconds` as the unit. _Introduced in DataWeave version 2.4.0._

- `number` — The `Number` value to transform into a `DateTime` value.
- `unit` — The unit to use for the conversion: `"milliseconds"` or `"seconds"`. A `null` value for the `unit` field defaults to `"seconds"`.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
    fromEpoch: toDateTime(1443743879),
    fromMillis: toDateTime(1443743879000, "milliseconds")
}
```

```dataweave
{
  fromEpoch: |2015-10-01T23:57:59Z|,
  fromMillis: |2015-10-01T23:57:59Z| as DateTime {unit: "milliseconds"}
}
```

```
toDateTime(str: String, format: String | Null = null, locale: String | Null = null): DateTime
```

Transforms a `String` value into a `DateTime` value and accepts a format and locale. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `DateTime` value.
- `format` — The formatting to use on the `DateTime` value. A `null` value has no effect on the `DateTime` value. This parameter accepts Java character patterns based on ISO-8601. A `DateTime` value, such as `2011-12-03T10:15:30.000000+01:00`, has the format `uuuu-MM-dd HH:mm:ssz`.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
   a: toDateTime("2015-10-01T23:57:59Z"),
   b: toDateTime("2003-10-01 23:57:59Z","uuuu-MM-dd HH:mm:ssz")
}
```

```dataweave
{
  a: |2015-10-01T23:57:59Z|,
  b: |2003-10-01T23:57:59Z| as DateTime {format: "uuuu-MM-dd HH:mm:ssz"}
}
```

## toDateTimeOrNull

```
toDateTimeOrNull(str: String, formatters: Array<Formatter>): DateTime | Null
```

Transforms a `String` value into a `DateTime` value using the first `Formatter` that matches with the given value to transform. If none of the `Formatter` matches with the given value, the function returns a `null` value. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `DateTime` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toDateTimeOrNull("2003-10-01 23:57:59Z", [{format: "uuuu/MM/dd HH:mm:ssz"}, {format: "uuuu-MM-dd HH:mm:ssz"}]),
  b: toDateTimeOrNull("2003-10-01 23:57:59Z", [{format: "uuuu/MM/dd HH:mm:ssz"}])
}
```

```dataweave
{
  a: |2003-10-01T23:57:59Z| as DateTime {format: "uuuu-MM-dd HH:mm:ssz"},
  b: null
}
```

## toLocalDateTime

```
toLocalDateTime(str: String, formatters: Array<Formatter>): LocalDateTime
```

Transforms a `String` value into a `LocalDateTime` value using the first `Formatter` that matches with the given value to transform. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `LocalDateTime` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
import * from dw::Runtime
output application/dw
---
{
  a: toLocalDateTime("2003-10-01 23:57:59", [{format: "uuuu/MM/dd HH:mm:ss"}, {format: "uuuu-MM-dd HH:mm:ss"}]),
  b: try(() -> toLocalDateTime("2003-10-01 23:57:59", [{format: "uuuu/MM/dd HH:mm:ss"}])).error.message
}
```

```dataweave
{
  a: |2003-10-01T23:57:59| as LocalDateTime {format: "uuuu-MM-dd HH:mm:ss"},
  b: "Could not find a valid formatter for '2003-10-01 23:57:59'"
}
```

```
toLocalDateTime(str: String, format: String | Null = null, locale: String | Null = null): LocalDateTime
```

Transforms a `String` value into a `LocalDateTime` value and accepts a format and locale. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `LocalDateTime` value.
- `format` — The formatting to use on the `LocalDateTime` value. A `null` value has no effect on the `LocalDateTime` value. This parameter accepts Java character patterns based on ISO-8601. A `LocalDateTime` value, such as `2011-12-03T10:15:30.000000` has the format `uuuu-MM-dd HH:mm:ss`.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toLocalDateTime("2015-10-01T23:57:59"),
  b: toLocalDateTime("2003-10-01 23:57:59","uuuu-MM-dd HH:mm:ss")
}
```

```dataweave
{
  a: |2015-10-01T23:57:59|,
  b: |2003-10-01T23:57:59| as LocalDateTime {format: "uuuu-MM-dd HH:mm:ss"}
}
```

## toLocalDateTimeOrNull

```
toLocalDateTimeOrNull(str: String, formatters: Array<Formatter>): LocalDateTime | Null
```

Transforms a `String` value into a `LocalDateTime` value using the first `Formatter` that matches with the given value to transform. If none of the `Formatter` matches with the given value, the function returns a `null` value. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `LocalDateTime` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toLocalDateTimeOrNull("2003-10-01 23:57:59", [{format: "uuuu/MM/dd HH:mm:ss"}, {format: "uuuu-MM-dd HH:mm:ss"}]),
  b: toLocalDateTimeOrNull("2003-10-01 23:57:59", [{format: "uuuu/MM/dd HH:mm:ss"}])
}
```

```dataweave
{
  a: |2003-10-01T23:57:59| as LocalDateTime {format: "uuuu-MM-dd HH:mm:ss"},
  b: null
}
```

## toLocalTime

```
toLocalTime(str: String, formatters: Array<Formatter>): LocalTime
```

Transforms a `String` value into a `LocalTime` value using the first `Formatter` that matches with the given value to transform. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `LocalTime` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
import * from dw::Runtime
output application/dw
---
{
  a: toLocalTime("23:57:59", [{format: "HH:mm:ss.n"}, {format: "HH:mm:ss"}]),
  b: try(() -> toLocalTime("23:57:59", [{format: "HH:mm:ss.n"}])).error.message
}
```

```dataweave
{
  a: |23:57:59| as LocalTime {format: "HH:mm:ss"},
  b: "Could not find a valid formatter for '23:57:59'"
}
```

```
toLocalTime(str: String, format: String | Null = null, locale: String | Null = null): LocalTime
```

Transforms a `String` value into a `LocalTime` value and accepts a format and locale. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `LocalTime` value.
- `format` — The formatting to use on the `LocalTime` value. A `null` value has no effect on the `LocalTime` value. This parameter accepts Java character patterns based on ISO-8601. A `LocalTime` value, such as `22:15:30.000000`, has the format `HH:mm:ss.n`.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
   toLocalTimeEx: toLocalTime("23:57:59"),
   toLocalTimeEx2: toLocalTime("13:44:12.283","HH:mm:ss.n")
}
```

```dataweave
{
  "toLocalTimeEx": "23:57:59",
  "toLocalTimeEx2": "13:44:12.283"
}
```

## toLocalTimeOrNull

```
toLocalTimeOrNull(str: String, formatters: Array<Formatter>): LocalTime | Null
```

Transforms a `String` value into a `LocalTime` value using the first `Formatter` that matches with the given value to transform. If none of the `Formatter` matches with the given value, the function returns a `null` value. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `LocalTime` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toLocalTimeOrNull("23:57:59", [{format: "HH:mm:ss.n"}, {format: "HH:mm:ss"}]),
  b: toLocalTimeOrNull("23:57:59", [{format: "HH:mm:ss.n"}])
}
```

```dataweave
{
  a: |23:57:59| as LocalTime {format: "HH:mm:ss"},
  b: null
}
```

## toNumber

```
toNumber(str: String, formatters: Array<Formatter>): Number
```

Transforms a `String` value into a `Number` value using the first `Formatter` that matches with the given value to transform. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `Number` value.
- `formatters` — Array<DatesFormatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
import * from dw::Runtime
output application/dw
---
{
  a: toNumber("0.005", [{format: "seconds"}, {format: ".00"}]),
  b: try(() -> toNumber("0.005", [{format: "seconds"}])).error.message
}
```

```dataweave
{
  a: 0.005 as Number {format: ".00"},
  b: "Could not find a valid formatter for '0.005'"
}
```

```
toNumber(dateTime: DateTime, unit: MillisOrSecs | Null = null): Number
```

A variant of `toNumber` that transforms a `DateTime` value into a number of seconds or milliseconds, depending on the selected unit. _Introduced in DataWeave version 2.4.0._

- `dateTime` — The `DateTime` value to transform into a `Number` value.
- `unit` — The unit of time (`"milliseconds"` or `"seconds"`) to use Given a `null` value, the function uses `"seconds"`.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
    epoch: toNumber(|2015-10-01T23:57:59Z|),
    millis: toNumber(|2015-10-01T23:57:59Z|, "milliseconds")
}
```

```dataweave
{
  "epoch": 1443743879,
  "millis": 1443743879000
}
```

```
toNumber(period: Period, unit: PeriodUnits | Null = null): Number
```

A variant of `toNumber` that transforms a `Period` value into a number of hours, minutes, seconds, milliseconds or nanoseconds (`nanos`). _Introduced in DataWeave version 2.4.0._

- `period` — The `Period` value to transform into a `Number` value.
- `unit` — The unit to apply to the specified `period`: `hours`, `minutes`, `seconds`, `milliseconds`, or `nanos`.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
    toSecondsEx1: toNumber(|PT1H10M|, "seconds"),
    toSecondsEx2: toNumber(|PT1M7S|, "milliseconds")
}
```

```json
{
  "toSecondsEx1": 4200,
  "toSecondsEx2": 67000
}
```

```
toNumber(value: String | Key, format: String | Null = null, locale: String | Null = null): Number
```

A variant of `toNumber` that transforms a `String` or `Key` value into a `Number` value and that accepts a format and locale. _Introduced in DataWeave version 2.4.0._

- `value` — The `String` or `Key` value to transform into a `Number` value.
- `format` — Optional formatting to apply to the `value`. A `format` accepts `#` or `0` (but not both) as placeholders for _decimal_ values and a single whole number that is less than `10`. Only one decimal point is permitted. A `null` or empty `String` value has no effect on the `Number` value. Other characters produce an error.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default.

```dataweave
%dw 2.0
import * from dw::util::Coercions
var myKey = keysOf({"123" : "myValue"})
output application/json
---
 {
     "default": toNumber("1.0"),
     "withFormat": toNumber("0.005",".00"),
     "withLocal": toNumber("1,25","#.##","ES"),
     "withExtraPlaceholders": toNumber("5.55","####.####"),
     "keyToNumber": toNumber(myKey[0])
 }
```

```json
{
  "default": 1.0,
  "withFormat": 0.005,
  "withLocal": 1.25,
  "withExtraPlaceholders": 5.55,
  "keyToNumber": 123
}
```

## toNumberOrNull

```
toNumberOrNull(str: String, formatters: Array<Formatter>): Number | Null
```

Transforms a `String` value into a `Number` value using the first `Formatter` that matches with the given value to transform. If none of the `Formatter` matches with the given value, the function returns a `null` value. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `Number` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toNumberOrNull("0.005", [{format: "seconds"}, {format: ".00"}]),
  b: toNumberOrNull("0.005", [{format: "seconds"}])
}
```

```dataweave
{
  a: 0.005 as Number {format: ".00"},
  b: null
}
```

## toPeriod

```
toPeriod(str: String): Period
```

Transform a `String` value into a `Period` value. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Period` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  toPeriodEx1: toPeriod("P1D"),
  toPeriodEx2: toPeriod("PT1H1M")
}
```

```json
{
  toPeriodEx1: |P1D|,
  toPeriodEx2: |PT1H1M|
}
```

## toRegex

```
toRegex(str: String): Regex
```

Transforms a `String` value into a `Regex` value. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Regex` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  toRegexEx1: toRegex("a-Z"),
  toRegexEx2: toRegex("0-9+")
}
```

```dataweave
{
  toRegexEx1: /a-Z/,
  toRegexEx2: /0-9+/
}
```

## toString

```
toString(number: Number, format: String | Null = null, locale: String | Null = null, roundMode: RoundingMode | Null = null): String
```

A variant of `toString` that transforms a `Number` value (whole or decimal) into a `String` value and accepts a format, locale, and rounding mode value. _Introduced in DataWeave version 2.4.0._

- `number` — The `Number` value to format.
- `format` — The formatting to apply to the `Number` value. A `format` accepts `#` or `0` (but not both) as placeholders for _decimal_ values, and only one decimal point is permitted. A `null` or empty `String` value has no effect on the `Number` value. Most other values are treated as literals, but you must escape special characters, such as a dollar sign (for example, `\$`). Inner quotations must be closed and differ from the surrounding quotations.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default. When you pass a translatable format, such as `eeee` and `MMMM`, a `locale` (such as `ES`) transforms the corresponding numeric values to a localized string.
- `roundMode` — Optional parameter for rounding decimal values when the formatting presents a rounding choice, such as a format of `0.#` for the decimal `0.15`. The default is `HALF_UP`, and a `null` value behaves like `HALF_UP`. Only one of the following values is permitted: * `UP`: Always rounds away from zero (for example, `0.01` to `"0.1"` and `-0.01` to `"-0.1"`). Increments the preceding digit to a non-zero fraction and never decreases the magnitude of the calculated value. * `DOWN`: Always rounds towards zero (for example, `0.19` to `"0.1"` and `-0.19` to `"-0.1"`). Never increments the digit before a discarded fraction (which truncates to the preceding digit) and never increases the magnitude of the calculated value. * `CEILING`: Rounds towards positive infinity and behaves like `UP` if the result is positive (for example, `0.35` to `"0.4"`). If the result is negative, this mode behaves like `DOWN` (for example, `-0.35` to `"-0.3"`). This mode never decreases the calculated value. * `FLOOR`: Rounds towards negative infinity and behaves like DOWN if the result is positive (for example, `0.35` to `"0.3"`). If the result is negative, this mode behaves like `UP` (for example, `-0.35` to `"-0.4"`). The mode never increases the calculated value. * `HALF_UP`: Default mode, which rounds towards the nearest "neighbor" unless both neighbors are equidistant, in which case, this mode rounds up. For example, `0.35` rounds to `"0.4"`, `0.34` rounds to `"0.3"`, and `0.36` rounds to `"0.4"`. Negative decimals numbers round similarly. For example, `-0.35` rounds to `"-0.4`". * `HALF_DOWN`: Rounds towards the nearest numeric "neighbor" unless both neighbors are equidistant, in which case, this mode rounds down. For example, `0.35` rounds to `"0.3"`, `0.34` rounds to `"0.3"`, and `0.36` rounds to `"0.4"`. Negative decimals numbers round similarly. For example, `-0.35` rounds to `"-0.3"`. * `HALF_EVEN`: For decimals that end in a `5` (such as, `1.125` and `1.135`), the behavior depends on the number that precedes the `5`. `HALF_EVEN` rounds up when the next-to-last digit before the `5` is an odd number but rounds down when the next-to-last digit is even. For example, `0.225` rounds to `"0.22"`, `0.235` _and_ `0.245` round to `"0.24"`, and `0.255` rounds to `"0.26"`. Negative decimals round similarly, for example, `-0.225` to `"-0.22"`. When the last digit is not `5`, the setting behaves like `HALF_UP`. Rounding of monetary values sometimes follows the `HALF_EVEN` pattern.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
    a: toString(1.0),
    b: toString(0.005,".00"),
    c: toString(0.035,"#.##","ES"),
    d: toString(0.005,"#.##","ES","HALF_EVEN"),
    e: toString(0.035,"#.00",null,"HALF_EVEN"),
    f: toString(1.1234,"\$.## 'in my account'")
}
```

```json
{
  "a": "1",
  "b": ".01",
  "c": "0,04",
  "d": "0",
  "e": ".04",
  "f": "$1.12 in my account"
}
```

```
toString(date: Date | DateTime | LocalDateTime | LocalTime | Time, format: String | Null = null, locale: String | Null = null): String
```

A variant of `toString` that transforms a `Date`, `DateTime`, `LocalTime`, `LocalDateTime`, or `Time` value into a `String` value. _Introduced in DataWeave version 2.4.0._

- `date` — The `Date`, `DateTime`, `LocalTime`, `LocalDateTime`, or `Time` value to coerce to a `String` type.
- `format` — The ISO-8601 formatting to use on the date or time. For example, this parameter accepts character patterns based on the Java 8 `java.time.format`. A `null` value has no effect on the value. Defaults: * `Date` example: `2011-12-03` (equivalent format: `uuuu-MM-dd`) * `DateTime` example: `2011-12-03T10:15:30.000000+01:00` (equivalent format: `uuuu-MM-dd HH:mm:ssz`) * `LocalDateTime` example: `2011-12-03T10:15:30.000000` (equivalent format: `uuuu-MM-dd HH:mm:ss`) * `LocalTime` example: `10:15:30.000000` (equivalent format: `HH:mm:ss.n`) * `Time` example: `10:15:30.000000Z` (equivalent format: `HH:mm:ss.nxxxz`)
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default. When you pass a translatable format, such as `eeee` and `MMMM`, a `locale` (such as `ES`) transforms the corresponding numeric values to a localized string.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
   aDate: toString(|2003-10-01|, "uuuu/MM/dd"),
   aDateTime: toString(|2018-09-17T22:13:00-03:00|),
   aLocalTime: toString(|23:57:59|, "HH-mm-ss"),
   aLocalDateTime : toString(|2015-10-01T23:57:59|),
   aLocalDateTimeFormatted: toString(|2003-10-01T23:57:59|, "uuuu-MM-dd HH:mm:ss a"),
   aLocalDateTimeFormattedAndLocalizedSpain: toString(|2003-01-01T23:57:59|, "eeee, dd MMMM, uuuu HH:mm:ss a", "ES"),
   aTime: typeOf(|22:10:18Z|),
   aTimeZone: toString(|-03:00|)
}
```

```json
{
  "aDate": "2003/10/01",
  "aDateTime": "2018-09-17T22:13:00-03:00",
  "aLocalTime": "23-57-59",
  "aLocalDateTime": "2015-10-01T23:57:59",
  "aLocalDateTimeFormatted": "2003-10-01 23:57:59 PM",
  "aLocalDateTimeFormattedAndLocalizedSpain": "miércoles, 01 enero, 2003 23:57:59 p. m.",
  "aTime": "Time",
  "aTimeZone": "-03:00"
}
```

```
toString(binary: Binary, encoding: String): String
```

A variant of `toString` that transforms a `Binary` value into a `String` value with the specified encoding. _Introduced in DataWeave version 2.4.0._

- `binary` — The `Binary` value to coerce to a `String` value.
- `encoding` — The encoding to apply to the `String` value. Accepts encodings that are supported by your JDK. For example, `encoding` accepts Java canonical names and aliases for the basic and extended encoding sets in Oracle JDK 8 and JDK 11.

```dataweave
%dw 2.0
import * from dw::util::Coercions
var binaryData= "DW Test" as Binary {encoding: "UTF-32"}
output application/json
---
{
  a: toString(binaryData, "UTF-32"),
}
```

```json
{
  "a": "DW Test"
}
```

```
toString(data: TimeZone | Uri | Boolean | Period | Regex | Key): String
```

A variant of `toString` that transforms a `TimeZone`, `Uri`, `Boolean`, `Period`, `Regex`, or `Key` value into a string. _Introduced in DataWeave version 2.4.0._

- `data` — The `TimeZone`, `Uri`, `Boolean`, `Period`, `Regex`, or `Key` value to coerce to a `String` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
  transformTimeZone: toString(|Z|),
  transformBoolean: toString(true),
  transformPeriod: toString(|P1D|),
  transformRegex: toString(/a-Z/),
  transformPeriod: toString(|PT8M10S|),
  transformUri: toString("https://docs.mulesoft.com/" as Uri)
}  ++
{ transformKey : toString((keysOf({ "aKeyToString" : "aValue"})[0])) }
```

```json
{
  "transformTimeZone": "Z",
  "transformBoolean": "true",
  "transformPeriod": "P1D",
  "transformRegex": "a-Z",
  "transformPeriod": "PT8M10S",
  "transformUri": "https://docs.mulesoft.com/",
  "transformKey": "aKeyToString"
}
```

```
toString(arr: Array<String>): String
```

A variant of `toString` that joins an `Array` of characters into a single `String` value. _Introduced in DataWeave version 2.4.0._

- `arr` — The `Array` of characters to transform into a `String` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
  a: toString([]),
  b: toString(["h", "o", "l", "a"])
}
```

```json
{
  "a": "",
  "b": "hola"
}
```

## toTime

```
toTime(str: String, formatters: Array<Formatter>): Time
```

Transforms a `String` value into a `Time` value using the first `Formatter` that matches with the given value to transform. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `Time` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
import * from dw::Runtime
output application/dw
---
{
  a: toTime("13:44:12.283-08:00", [{format: "HH:mm:ss.xxx"}, {format: "HH:mm:ss.nxxx"}]),
  b: try(() -> toTime("13:44:12.283-08:00", [{format: "HH:mm:ss.xxx"}]).error.message
}
```

```dataweave
{
  a: |13:44:12.000000283-08:00| as Time {format: "HH:mm:ss.nxxx"},
  b: "Could not find a valid formatter for '13:44:12.283-08:00'"
}
```

```
toTime(str: String, format: String | Null = null, locale: String | Null = null): Time
```

Transforms a `String` value into a `Time` value and accepts a format and locale. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Time` value.
- `format` — The formatting to use on the `Time` value. A `null` value has no effect on the `Time` value. This parameter accepts Java character patterns based on ISO-8601. A `Time` value, such as `10:15:30.000000`, has the format `HH:mm:ss.nxxx`.
- `locale` — Optional ISO 3166 country code to use, such as `US`, `AR`, or `ES`. A `null` or absent value uses your JVM default.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
   a: toTime("23:57:59Z"),
   b: toTime("13:44:12.283-08:00","HH:mm:ss.nxxx")
}
```

```dataweave
{
  a: |23:57:59Z|,
  b: |13:44:12.000000283-08:00| as Time {format: "HH:mm:ss.nxxx"}
}
```

## toTimeOrNull

```
toTimeOrNull(str: String, formatters: Array<Formatter>): Time | Null
```

Transforms a `String` value into a `Time` value using the first `Formatter` that matches with the given value to transform. If none of the `Formatter` matches with the given value, the function returns a `null` value. _Introduced in DataWeave version 2.5.0._

- `Description` — `str`
- `String` — The `String` value to transform into a `Time` value.
- `formatters` — Array<Formatter>

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
  a: toTimeOrNull("13:44:12.283-08:00", [{format: "HH:mm:ss.xxx"}, {format: "HH:mm:ss.nxxx"}]),
  b: toTimeOrNull("13:44:12.283-08:00", [{format: "HH:mm:ss.xxx"}])
}
```

```dataweave
{
  a: |13:44:12.000000283-08:00| as Time {format: "HH:mm:ss.nxxx"},
  b: null
}
```

## toTimeZone

```
toTimeZone(str: String): TimeZone
```

Transform a `String` value into a `TimeZone` value. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `TimeZone` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/dw
---
{
   toTimeZoneOffset: toTimeZone("-03:00"),
   toTimeZoneAbbreviation: toTimeZone("Z"),
   toTimeZoneName: toTimeZone("America/Argentina/Buenos_Aires")
}
```

```dataweave
{
  toTimeZoneOffset: |-03:00|,
  toTimeZoneAbbreviation: |Z|,
  toTimeZoneName: |America/Argentina/Buenos_Aires|
}
```

## toUri

```
toUri(str: String): Uri
```

Transforms a `String` value into a `Uri` value. _Introduced in DataWeave version 2.4.0._

- `str` — The `String` value to transform into a `Uri` value.

```dataweave
%dw 2.0
import * from dw::util::Coercions
output application/json
---
{
  toUriExample: toUri("https://www.google.com/")
}
```

```dataweave
{
  "toUriExample": "https://www.google.com/"
}
```
