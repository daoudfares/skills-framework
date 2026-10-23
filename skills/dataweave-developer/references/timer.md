# dw::timer — Timer functions

Namespace `dw::util::Timer`.
Requires an explicit import: `import * from dw::util::Timer`.

Functions: `currentMilliseconds`, `duration`, `time`, `toMilliseconds`

---

## currentMilliseconds

```
currentMilliseconds(): Number
```

Returns the current time in milliseconds.

```dataweave
%dw 2.0
import * from dw::util::Timer
output application/json
---
{ "currentMilliseconds" : currentMilliseconds() }
```

```xml
{ "currentMilliseconds": 1532923168900 }
```

## duration

```
duration<T>(valueToMeasure: () -> T): DurationMeasurement<T>
```

Executes the input function and returns an object with execution time in milliseconds and result of that function.

- `valueToMeasure` — A function to pass to `duration`.

```dataweave
%dw 2.0
output application/json
fun myFunction() = dw::Runtime::wait("My result",100)
---
dw::util::Timer::duration(() -> myFunction())
```

```xml
{
  "time": 101,
  "result": "My result"
}
```

## time

```
time<T>(valueToMeasure: () -> T): TimeMeasurement<T>
```

Executes the input function and returns a `TimeMeasurement` object that contains the start and end time for the execution of that function, as well the result of the function.

- `valueToMeasure` — A function to pass to `time`.

## toMilliseconds

```
toMilliseconds(date: DateTime): Number
```

Returns the representation of a specified date-time in milliseconds.

- `date` — A `DateTime` to evaluate.

```dataweave
%dw 2.0
import * from dw::util::Timer
output application/json
---
{ "toMilliseconds" : toMilliseconds(|2018-07-23T22:03:04.829Z|) }
```

```xml
{ "toMilliseconds": 1532383384829 }
```
