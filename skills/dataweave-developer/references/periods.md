# dw::periods — Periods functions

Namespace `dw::core::Periods`.
Requires an explicit import: `import * from dw::core::Periods`.

Functions: `between`, `days`, `duration`, `hours`, `minutes`, `months`, `period`, `seconds`, `years`

---

## between

```
between(endDateExclusive: Date, startDateInclusive: Date): Period
```

Returns a Period (P) value consisting of the number of years, months, and days between two Date values. The start date is included, but the end date is not. The result of this method can be a negative period if the end date (`endDateExclusive`) is before the start date (`startDateInclusive`). Note that the first parameter of the function is the `endDateExclusive` and the second one is the `startDateInclusive`. _Introduced in DataWeave version 2.3.0._

- `endDateExclusive` — The end date, exclusive.
- `startDateInclusive` — The start date, inclusive.

```dataweave
import * from dw::core::Periods
output application/json
---
{
   a: between(|2010-12-12|,|2010-12-10|),
   b: between(|2011-12-11|,|2010-11-10|),
   c: between(|2020-02-29|,|2020-03-30|)
}
```

```json
{
   "a": "P2D",
   "b": "P1Y1M1D",
   "c": "P-1M-1D"
 }
```

## days

```
days(nDays: Number): Period
```

Creates a Period value from the provided number of days. The function applies the `period` function to input that is a whole number and the `duration` function to decimal input. _Introduced in DataWeave version 2.4.0._

- `nDays` — The number of hours as a whole or decimal number. A positive or negative number is valid.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
   tomorrow: |2020-10-05T20:22:34.385Z| + days(1),
   yesterday: |2020-10-05T20:22:34.385Z| - days(1),
   decimalDaysPlusQuarter:  |2020-10-05T00:00:00.000Z| + days(0.25),
   decimalDaysPlusHalf:  |2020-10-05T00:00:00.000Z| + days(0.5),
   decimalDaysPlusThreeQuarters:  |2020-10-05T00:00:00.000Z| + days(0.75),
   decimalInputAsPeriod : days(4.555),
   fourDayPeriod: days(4),
   negativeValue: days(-1)
}
```

```json
{
   "tomorrow": "2020-10-06T20:22:34.385Z",
   "yesterday": "2020-10-04T20:22:34.385Z",
   "decimalDaysPlusQuarter": "2020-10-05T06:00:00Z",
   "decimalDaysPlusHalf": "2020-10-05T12:00:00Z",
   "decimalDaysPlusThreeQuarters": "2020-10-05T18:00:00Z",
   "decimalInputAsPeriod": "PT109H19M12S",
   "fourDayPeriod": "P4D",
   "negativeValue": "P-1D"
}
```

## duration

```
duration(period: { days?: Number, hours?: Number, minutes?: Number, seconds?: Number }): Period
```

Creates a Period value that represents a number of days, hours, minutes, or seconds. _Introduced in DataWeave version 2.4.0._

- `period` — An object such as `{days:4, hours:11, minutes:45, seconds: 55}`. The key-value pairs are optional and can be specified in any order. An empty object (`{}`) returns the Period value `"PT0S"` (zero seconds). The default value of each key is `0`. Valid values are whole or decimal numbers, which can be positive or negative. Key names are selectable.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
   dayAfterDateTime: |2020-10-05T20:22:34.385Z| + duration({days: 1}),
   dayAndHourBeforeDateTime: |2020-10-05T20:22:34.385Z| - duration({days: 1, hours: 1}),
   pointInTimeBefore: |2020-10-05T20:22:34.385Z| - duration({days: 1, hours: 1, minutes: 20, seconds: 10}),
   emptyDuration: duration({}),
   constructDuration: duration({days:4, hours:11, minutes:28}),
   selectHoursFromDuration: duration({days:4, hours:11, minutes:28}).hours,
   decimalAsPeriod:  duration({seconds: 30.5}),
   addNegativeValue: duration({ minutes : 1 }) + duration({ seconds : -1 })
}
```

```json
{
   "dayAfterDateTime": "2020-10-06T20:22:34.385Z",
   "dayAndHourBeforeDateTime": "2020-10-04T19:22:34.385Z",
   "pointInTimeBefore": "2020-10-04T19:02:24.385Z",
   "emptyDuration": "PT0S",
   "constructDuration": "PT107H28M",
   "selectHoursFromDuration": 11,
   "decimalAsPeriod": "PT30.5S",
   "addNegativeValue": 59
}
```

## hours

```
hours(nHours: Number): Period
```

Creates a Period value from the provided number of hours. The function applies the `duration` function to the input value. _Introduced in DataWeave version 2.4.0._

- `nHours` — The number of hours as a whole or decimal number. A positive or negative number is valid.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
   nextHour: |2020-10-05T20:22:34.385Z| + hours(1),
   previousHour: |2020-10-05T20:22:34.385Z| - hours(1),
   threeHoursLater: |20:22| + hours(3),
   addDecimalInput: |20:22| + hours(3.5),
   decimalInputAsPeriod : hours(4.555),
   fourHourPeriod : hours(4),
   addNegativeValue: hours(-1) + hours(2)
}
```

```json
{
   "nextHour": "2020-10-05T21:22:34.385Z",
   "previousHour": "2020-10-05T19:22:34.385Z",
   "threeHoursLater": "23:22:00",
   "addDecimalInput": "23:52:00",
   "decimalInputAsPeriod": "PT4H33M18S",
   "fourHourPeriod": "PT4H",
   "addNegativeValue": 3600
}
```

## minutes

```
minutes(nMinutes: Number): Period
```

Creates a Period value from the provided number of minutes. The function applies the `duration` function to the input value. _Introduced in DataWeave version 2.4.0._

- `nMinutes` — The number of minutes as a whole or decimal number. A positive or negative number is valid.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
   nextMinute: |2020-10-05T20:22:34.385Z| + minutes(1),
   previousMinute: |2020-10-05T20:22:34.385Z| - minutes(1),
   decimalInputPeriod: minutes(4.555),
   wholeNumberInputPeriod: minutes(4),
   addNegativeValue: minutes(-1) + minutes(2)
}
```

```json
{
   "nextMinute": "2020-10-05T20:23:34.385Z",
   "previousMinute": "2020-10-05T20:21:34.385Z",
   "decimalInputPeriod": "PT4M33.3S",
   "wholeNumberInputPeriod": "PT4M",
   "addNegativeValue": 60
}
```

## months

```
months(nMonths: Number): Period
```

Creates a Period value from the provided number of months. The function applies the `period` function to the input value. _Introduced in DataWeave version 2.4.0._

- `nMonths` — The number of months as a whole number. A positive or negative number is valid.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
  nextMonth: |2020-10-05T20:22:34.385Z| + months(1),
  fourMonthPeriod : months(4),
  addNegativeValue: months(-1) + months(2)
}
```

```json
{
  "nextMonth": "2020-11-05T20:22:34.385Z",
  "fourMonthPeriod": "P4M",
  "addNegativeValue": 1
}
```

## period

```
period(period: { years?: Number, months?: Number, days?: Number }): Period
```

Creates a Period value as a date-based number of years, months, and days in the ISO-8601 calendar system. _Introduced in DataWeave version 2.4.0._

- `period` — An object such as `{years:4, months:11, days:28}`. The key-value pairs are optional and can be specified in any order. An empty object (`{}`) returns the Period value `"P0D"` (zero days). The default value of each key is `0`. Valid values are whole numbers, which can be positive or negative. Decimal values produce an error message. Key names are selectable.

```dataweave
%dw 2.0
output application/json
import * from dw::core::Periods
---
{
   dayBeforeDateTime: |2020-10-05T20:22:34.385Z| - period({days:1}),
   dayAfterDate: |2020-10-05| + period({days:1}),
   yearMonthDayAfterDate: |2020-10-05| + period({years:1, months:1, days:1}),
   emptyPeriod: period({}),
   constructPeriod: period({years:4, months:11, days:28}),
   selectMonthsFromPeriod: period({years:4, months:11, days:28}).months
}
```

```json
{
    "dayBeforeDateTime": "2020-10-04T20:22:34.385Z",
    "dayAfterDate": "2020-10-06",
    "yearMonthDayAfterDate": "2021-11-06",
    "emptyPeriod": "P0D",
    "constructPeriod": "P4Y11M28D",
    "selectMonthsFromPeriod": 11
}
```

## seconds

```
seconds(nSecs: Number): Period
```

Creates a Period value from the provided number of seconds. _Introduced in DataWeave version 2.4.0._

- `nSecs` — The number of seconds as a whole or decimal number. A positive or negative number is valid.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
  nextSecond: |2020-10-05T20:22:34.385Z| + seconds(1),
  previousSecond: |2020-10-05T20:22:34.385Z| - seconds(1),
  decimalInputPeriod: seconds(4.555),
  wholeNumberInputPeriod: seconds(4),
  addNegativeValue: seconds(-1) + seconds(2)
}
```

```json
{
  "nextSecond": "2020-10-05T20:22:35.385Z",
  "previousSecond": "2020-10-05T20:22:33.385Z",
  "decimalInputPeriod": "PT4.555S",
  "wholeNumberInputPeriod": "PT4S",
  "addNegativeValue": 1
}
```

## years

```
years(nYears: Number): Period
```

Creates a Period value from the provided number of years. The function applies the `period` function to the input value. _Introduced in DataWeave version 2.4.0._

- `nYears` — A whole number for the number of years. A positive or negative number is valid.

```dataweave
%dw 2.0
import * from dw::core::Periods
output application/json
---
{
  nextYear: |2020-10-05T20:22:34.385Z| + years(1),
  fourYearPeriod: years(4),
  addNegativeValue: years(-1) + years(2)
}
```

```json
{
   "nextYear": "2021-10-05T20:22:34.385Z",
   "fourYearPeriod": "P4Y",
   "addNegativeValue": 12
}
```
