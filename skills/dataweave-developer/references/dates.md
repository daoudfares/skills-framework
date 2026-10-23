# dw::dates — Dates functions

Namespace `dw::core::Dates`.
Requires an explicit import: `import * from dw::core::Dates`.

Functions: `atBeginningOfDay`, `atBeginningOfHour`, `atBeginningOfMonth`, `atBeginningOfWeek`, `atBeginningOfYear`, `date`, `dateTime`, `localDateTime`, `localTime`, `time`, `today`, `tomorrow`, `yesterday`

---

## atBeginningOfDay

```
atBeginningOfDay(dateTime: DateTime): DateTime
```

Returns a  new `DateTime` value that changes the `Time` value in the input to the beginning of the specified _day_. The hours, minutes, and seconds in the input change to `00:00:00`. _Introduced in DataWeave version 2.4.0._

- `dateTime` — The `DateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  "atBeginningOfDayDateTime": atBeginningOfDay(|2020-10-06T18:23:20.351-03:00|)
}
```

```json
{
  "atBeginningOfDayDateTime": "2020-10-06T00:00:00-03:00"
}
```

```
atBeginningOfDay(localDateTime: LocalDateTime): LocalDateTime
```

Returns a new `LocalDateTime` value that changes the `Time` value within the input to the start of the specified _day_. The hours, minutes, and seconds in the input change to `00:00:00`. _Introduced in DataWeave version 2.4.0._

- `localDateTime` — The `LocalDateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  "atBeginningOfDayLocalDateTime": atBeginningOfDay(|2020-10-06T18:23:20.351|)
}
```

```json
{
  "atBeginningOfDayLocalDateTime": "2020-10-06T00:00:00"
}
```

## atBeginningOfHour

```
atBeginningOfHour(dateTime: DateTime): DateTime
```

Returns a  new `DateTime` value that changes the `Time` value in the input to the beginning of the specified _hour_. The minutes and seconds in the input change to `00:00`. _Introduced in DataWeave version 2.4.0._

- `dateTime` — The `DateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
   "atBeginningOfHourDateTime": atBeginningOfHour(|2020-10-06T18:23:20.351-03:00|)
}
```

```json
{
 "atBeginningOfHourDateTime": "2020-10-06T18:00:00-03:00"
}
```

```
atBeginningOfHour(localDateTime: LocalDateTime): LocalDateTime
```

Returns a  new `LocalDateTime` value that changes the `Time` value in the input to the beginning of the specified _hour_. The minutes and seconds in the input change to `00:00`. _Introduced in DataWeave version 2.4.0._

- `localDateTime` — The `LocalDateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
   "atBeginningOfHourLocalDateTime": atBeginningOfHour(|2020-10-06T18:23:20.351|)
}
```

```json
{
 "atBeginningOfHourLocalDateTime": "2020-10-06T18:00:00"
}
```

```
atBeginningOfHour(localTime: LocalTime): LocalTime
```

Returns a  new `LocalTime` value that changes its value in the input to the beginning of the specified _hour_. The minutes and seconds in the input change to `00:00`. _Introduced in DataWeave version 2.4.0._

- `localTime` — The `LocalTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
   "atBeginningOfHourLocalTime": atBeginningOfHour(|18:23:20.351|)
}
```

```json
{
 "atBeginningOfHourLocalTime": "18:00:00"
}
```

```
atBeginningOfHour(time: Time): Time
```

Returns a new `Time` value that changes the input value to the beginning of the specified _hour_. The minutes and seconds in the input change to `00:00`. _Introduced in DataWeave version 2.4.0._

- `time` — The `Time` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
   "atBeginningOfHourTime": atBeginningOfHour(|18:23:20.351-03:00|)
}
```

```json
{
 "atBeginningOfHourTime":  "18:00:00-03:00"
}
```

## atBeginningOfMonth

```
atBeginningOfMonth(dateTime: DateTime): DateTime
```

Returns a new `DateTime` value that changes the `Day` value from the input to the first day of the specified _month_. It also sets the `Time` value to `00:00:00`. The day and time in the input changes to `01T00:00:00`. _Introduced in DataWeave version 2.4.0._

- `dateTime` — The `DateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  "atBeginningOfMonthDateTime": atBeginningOfMonth(|2020-10-06T18:23:20.351-03:00|)
}
```

```json
{
  "atBeginningOfMonthDateTime": "2020-10-01T00:00:00-03:00"
}
```

```
atBeginningOfMonth(localDateTime: LocalDateTime): LocalDateTime
```

Returns a new `LocalDateTime` value that changes the `Day` and `LocalTime` values from the input to the beginning of the specified _month_. The day and time in the input changes to `01T00:00:00`. _Introduced in DataWeave version 2.4.0._

- `localDateTime` — The `LocalDateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
 "atBeginningOfMonthLocalDateTime": atBeginningOfMonth(|2020-10-06T18:23:20.351|)
}
```

```json
{
  "atBeginningOfMonthLocalDateTime": "2020-10-01T00:00:00"
}
```

```
atBeginningOfMonth(date: Date): Date
```

Returns a new `Date` value that changes the `Day` value from the input to the first day of the specified _month_. The day in the input changes to `01`. _Introduced in DataWeave version 2.4.0._

- `date` — The `Date` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfMonthDate: atBeginningOfMonth(|2020-10-06|)
}
```

```json
{
  "atBeginningOfMonthDate": "2020-10-01"
}
```

## atBeginningOfWeek

```
atBeginningOfWeek(dateTime: DateTime): DateTime
```

Returns a new `DateTime` value that changes the `Day` and `Time` values from the input to the beginning of the first day of the specified _week_. The function treats Sunday as the first day of the week. _Introduced in DataWeave version 2.4.0._

- `dateTime` — The `DateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfWeekDateTime: atBeginningOfWeek(|2020-10-06T18:23:20.351-03:00|)
}
```

```json
{
  "atBeginningOfWeekDateTime": "2020-10-04T00:00:00-03:00"
}
```

```
atBeginningOfWeek(localDateTime: LocalDateTime): LocalDateTime
```

Returns a new `LocalDateTime` value that changes the `Day` and `Time` values from the input to the beginning of the first day of the specified _week_. The function treats Sunday as the first day of the week. _Introduced in DataWeave version 2.4.0._

- `localDateTime` — The `LocalDateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfWeekLocalDateTime: atBeginningOfWeek(|2020-10-06T18:23:20.351|)
}
```

```json
{
  "atBeginningOfWeekLocalDateTime": "2020-10-04T00:00:00"
}
```

```
atBeginningOfWeek(date: Date): Date
```

Returns a new `Date` value that changes the `Date` input input to the first day of the specified _week_. The function treats Sunday as the first day of the week. _Introduced in DataWeave version 2.4.0._

- `date` — The `Date` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfWeekDate: atBeginningOfWeek(|2020-10-06|)
}
```

```json
{
  "atBeginningOfWeekDate": "2020-10-04"
}
```

## atBeginningOfYear

```
atBeginningOfYear(dateTime: DateTime): DateTime
```

Takes a `DateTime` value as input and returns a `DateTime` value for the first day of the _year_ specified in the input. It also sets the `Time` value to `00:00:00`. The month, day, and time in the input changes to `01-01T00:00:00`. _Introduced in DataWeave version 2.4.0._

- `dateTime` — The `DateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfYearDateTime: atBeginningOfYear(|2020-10-06T18:23:20.351-03:00|)
}
```

```json
{
  "atBeginningOfYearDateTime": "2020-01-01T00:00:00.000-03:00"
}
```

```
atBeginningOfYear(localDateTime: LocalDateTime): LocalDateTime
```

Takes a `LocalDateTime` value as input and returns a `LocalDateTime` value for the first day of the _year_ specified in the input. It also sets the `Time` value to `00:00:00`. The month, day, and time in the input changes to `01-01T00:00:00`. _Introduced in DataWeave version 2.4.0._

- `localDateTime` — The `LocalDateTime` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfYearLocalDateTime: atBeginningOfYear(|2020-10-06T18:23:20.351|)
}
```

```json
{
  "atBeginningOfYearLocalDateTime": "2020-01-01T00:00:00"
}
```

```
atBeginningOfYear(date: Date): Date
```

Takes a `Date` value as input and returns a `Date` value for the first day of the _year_ specified in the input. The month and day in the input changes to `01-01`. _Introduced in DataWeave version 2.4.0._

- `date` — The `Date` value to reference.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  atBeginningOfYearDate: atBeginningOfYear(|2020-10-06|)
}
```

```json
{
  "atBeginningOfYearDate": "2020-01-01"
}
```

## date

```
date(parts: DateFactory): Date
```

Creates a `Date` value from values specified for `year`, `month`, and `day` fields. _Introduced in DataWeave version 2.4.0._

- `parts` — `Number` values for `year`, `month`, and `day` fields. The `month` must be a value between 1 and 12, and the `day` value must be between 1 and 31. You can specify the name-value pairs in any order, but the output is ordered by default as a Date value, such as `2012-10-11`. The input fields are parts of a `DateFactory` type.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
   newDate: date({year: 2012, month: 10, day: 11})
}
```

```json
{
   "newDate": "2012-10-11"
}
```

## dateTime

```
dateTime(parts: DateTimeFactory): DateTime
```

Creates a `DateTime` value from values specified for `year`, `month`, `day`, `hour`, `minutes`, `seconds`, and `timezone` fields. _Introduced in DataWeave version 2.4.0._

- `parts` — `Number` values for `year`, `month`, `day`, `hour`, `minutes`, and `seconds` fields followed by a `TimeZone` value for the `timezone` field. Valid values are numbers between 1 and 12 for the `month`, 1 through 31 for the `day`, 0 through 23 for the `hour`, 0 through 59 for `minutes`, and 0 through 59 (including decimals, such as 59.99) for seconds. You can specify the name-value pairs in any order, but the output is ordered by default as a `DateTime` value, such as `2012-10-11T10:10:10-03:00`. The input fields are parts of a `DateTimeFactory` type.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
    newDateTime: dateTime({year: 2012, month: 10, day: 11, hour: 12, minutes: 30, seconds: 40 , timeZone: |-03:00|})
}
```

```json
{
   "newDateTime": "2012-10-11T12:30:40-03:00"
}
```

## localDateTime

```
localDateTime(parts: LocalDateTimeFactory): LocalDateTime
```

Creates a `LocalDateTime` value from values specified for `year`, `month`, `day`, `hour`, `minutes`, and `seconds` fields. _Introduced in DataWeave version 2.4.0._

- `parts` — `Number` values for `year`, `month`, `day`, `hour`, `minutes`, and `seconds` fields. Valid values are numbers between 1 and 12 for the `month`, 1 through 31 for the `day`, 0 through 23 for the `hour`, 0 through 59 for `minutes`, and 0 through 59 (including decimals, such as 59.99) for `seconds` fields. You can specify the name-value pairs in any order, but the output is ordered as a default `LocalDateTime` value, such as `2012-10-11T10:10:10`. The input fields are parts of a `LocalDateTimeFactory` type.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
    newLocalDateTime: localDateTime({year: 2012, month: 10, day: 11, hour: 12, minutes: 30, seconds: 40})
}
```

```json
{
   "newLocalDateTime": "2012-10-11T12:30:40"
}
```

## localTime

```
localTime(parts: LocalTimeFactory): LocalTime
```

Creates a `LocalTime` value from values specified for `hour`, `minutes`, and `seconds` fields. _Introduced in DataWeave version 2.4.0._

- `parts` — `Number` values for `hour`, `minutes`, and `seconds` fields. Valid values are 0 through 23 for the `hour`, 0 through 59 for `minutes`, and 0 through 59 (including decimals, such as 59.99) for `seconds` fields. You can specify the name-value pairs in any order, but the output is ordered as a default `LocalTime` value, such as `10:10:10`. The input fields are parts of a `LocalDateTimeFactory` type.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  newLocalTime: localTime({ hour: 12, minutes: 30, seconds: 40})
}
```

```json
{
   "newLocalTime": "12:30:40"
}
```

## time

```
time(parts: TimeFactory): Time
```

Creates a `Time` value from values specified for `hour`, `minutes`, `seconds`, and `timezone` fields. _Introduced in DataWeave version 2.4.0._

- `parts` — `Number` values for `hour`, `minutes`, and `seconds` fields, and a `TimeZone` value for the `timezone` field. Valid values are 0 through 23 for the `hour`, 0 through 59 for `minutes`, and 0 through 59 (including decimals, such as 59.99) for `seconds` fields. The `timezone` must be a valid `TimeZone` value, such as `|-03:00|` You can specify the name-value pairs in any order, but the output is ordered as a default `Time` value, such as `10:10:10-03:00`. The input fields are parts of a `TimeFactory` type.

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
{
  newTime: time({ hour: 12, minutes: 30, seconds: 40 , timeZone: |-03:00| })
}
```

```json
{
   "newTime": "12:30:40-03:00"
}
```

## today

```
today(): Date
```

Returns the date for today as a `Date` type. _Introduced in DataWeave version 2.4.0._

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
today()
```

```json
"2021-05-15"
```

## tomorrow

```
tomorrow(): Date
```

Returns the date for tomorrow as a `Date` type. _Introduced in DataWeave version 2.4.0._

```dataweave
%dw 2.0
import tomorrow from dw::core::Dates
output application/json
---
tomorrow()
```

```json
"2021-05-16"
```

## yesterday

```
yesterday(): Date
```

Returns the date for yesterday as a `Date` type. _Introduced in DataWeave version 2.4.0._

```dataweave
%dw 2.0
import * from dw::core::Dates
output application/json
---
yesterday()
```

```json
"2021-05-14"
```
