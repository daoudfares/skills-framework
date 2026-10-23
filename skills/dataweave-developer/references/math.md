# dw::math — Math functions

Namespace `dw::util::Math`.
Requires an explicit import: `import * from dw::util::Math`.

Functions: `acos`, `asin`, `atan`, `cos`, `decimalAdd`, `decimalDivide`, `decimalMultiply`, `decimalPow`, `decimalRound`, `decimalSqrt`, `decimalSubtract`, `log10`, `logn`, `sin`, `tan`, `toDegrees`, `toRadians`

---

## acos

```
acos(angle: Number): Number | NaN
```

Returns an arc cosine value that can range from `0.0` through pi. If the absolute value of the input is greater than `1`, the result is `null`. _Introduced in DataWeave version 2.4.0._

- `angle` — Number to convert into it arc cosine value.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "acos0": acos(0),
  "acos13": acos(0.13),
  "acos-1": acos(-1),
  "acos1": acos(1),
  "acos1.1": acos(1.1)
}
```

```json
{
   "acos0": 1.5707963267948966,
   "acos13": 1.440427347091751,
   "acos-1": 3.141592653589793,
   "acos1": 0.0,
   "acos1.1": null
 }
```

## asin

```
asin(angle: Number): Number | NaN
```

Returns an arc sine value that can range from `-pi/2` through `pi/2`. If the absolute value of the input is greater than 1, the result is `null`. _Introduced in DataWeave version 2.4.0._

- `angle` — Number to convert into its arc sine value.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "asin0": asin(0),
  "asin13": asin(0.13),
  "asin-1": asin(-1),
  "asin1.1": asin(1.1)
}
```

```json
{
   "asin0": 0.0,
   "asin13": 0.1303689797031455,
   "asin-1": -1.5707963267948966,
   "asin1.1": null
 }
```

## atan

```
atan(angle: Number): Number
```

Returns an arc tangent value that can range from `-pi/2` through `pi/2`. _Introduced in DataWeave version 2.4.0._

- `angle` — Number to convert into its arc tangent value.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "atan0":  atan(0),
  "atan13": atan(0.13),
  "atan-1": atan(-1)
}
```

```json
{
   "atan0": 0.0,
   "atan13": 0.12927500404814307,
   "atan-1": -0.7853981633974483
}
```

## cos

```
cos(angle: Number): Number
```

Returns the trigonometric cosine of an angle from a given number of radians. _Introduced in DataWeave version 2.4.0._

- `angle` — Number of radians in an angle.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "cos0": cos(0),
  "cos13": cos(0.13),
  "cos-1": cos(-1)
}
```

```json
{
  "cos0": 1.0,
  "cos13": 0.9915618937147881,
  "cos-1": 0.5403023058681398
}
```

## decimalAdd

```
decimalAdd(lhs: Number, rhs: Number, ctx: OperationContext = DECIMAL_128_CONTEXT): Number
```

Performs number addition with rounding specified by the operation context.

## decimalDivide

```
decimalDivide(dividend: Number, divisor: Number, ctx: OperationContext = DECIMAL_128_CONTEXT): Number
```

Performs number division with rounding specified by the operation context. If precision is set to 0 (unlimited precision) and the result has an infinite decimal expansion, the function returns an error.

## decimalMultiply

```
decimalMultiply(leftFactor: Number, rightFactor: Number, ctx: OperationContext = DECIMAL_128_CONTEXT): Number
```

Performs number multiplication with rounding specified by the operation context.

## decimalPow

```
decimalPow(base: Number, exponent: Number, ctx: OperationContext = DECIMAL_128_CONTEXT): Number
```

Returns a number with value base^exponent with rounding specified by the operation context. The maximum value for exponent is 99999999.

## decimalRound

```
decimalRound(n: Number, ctx: OperationContext = DECIMAL_128_CONTEXT)
```

Returns the argument number with rounding specified by the operation context.

## decimalSqrt

```
decimalSqrt(n: Number, ctx: OperationContext = DECIMAL_128_CONTEXT): Number
```

Returns a number that approximates the square root of the argument with rounding specified by the operation context.

## decimalSubtract

```
decimalSubtract(lhs: Number, rhs: Number, ctx: OperationContext = DECIMAL_128_CONTEXT): Number
```

Performs number subtraction with rounding specified by the operation context.

## log10

```
log10(a: Number): Number | NaN
```

Returns the logarithm base 10 of a number. _Introduced in DataWeave version 2.4.0._

- `a` — A `Number` value that serves as input to the function.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "log1010": log10(10),
  "log1013": log10(0.13),
  "log10-20": log10(-20)
}
```

```json
{
   "log1010": 1.0,
   "log1013": -0.8860566476931632,
   "log10-20": null
}
```

## logn

```
logn(a: Number): Number | NaN
```

Returns the natural logarithm (base `e`) of a number. If the input value is less than or equal to zero, the result is `NaN` (or `null`). _Introduced in DataWeave version 2.4.0._

- `a` — Number to convert into its natural logarithm.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
   "logn10":  logn(10),
   "logn13": logn(0.13),
   "logn-20": logn(-20)
}
```

```json
{
   "logn10": 2.302585092994046,
   "logn13": -2.0402208285265546,
   "logn-20": null
}
```

## sin

```
sin(angle: Number): Number
```

Returns the trigonometric sine of an angle from a given number of radians. _Introduced in DataWeave version 2.4.0._

- `angle` — Number of radians in an angle.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "sin0": sin(0),
  "sin13": sin(0.13),
  "sin-1": sin(-1)
}
```

```json
{
  "sin0": 0.0,
  "sin13": 0.12963414261969486,
  "sin-1": -0.8414709848078965
}
```

## tan

```
tan(angle: Number): Number
```

Returns the trigonometric tangent of an angle from a given number of radians. _Introduced in DataWeave version 2.4.0._

- `angle` — Number of radians in an angle.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
   "tan0": tan(0),
   "tan13": tan(0.13),
   "tan-1": tan(-1)
}
```

```json
{
   "tan0": 0.0,
   "tan13": 0.13073731800446006,
   "tan-1": -1.5574077246549023
 }
```

## toDegrees

```
toDegrees(angrad: Number): Number
```

Converts an angle measured in radians to an approximately equivalent number of degrees. _Introduced in DataWeave version 2.4.0._

- `angrad` — Number of radians to convert to degrees.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "toDegrees0.17":  toDegrees(0.174),
  "toDegrees0": toDegrees(0),
  "toDegrees-20": toDegrees(-0.20)
}
```

```json
{
   "toDegrees0.17": 9.969465635276323832571267395889251,
   "toDegrees0": 0E+19,
   "toDegrees-20": -11.45915590261646417536927286883822
 }
```

## toRadians

```
toRadians(angdeg: Number): Number
```

Converts a given number of degrees in an angle to an approximately equivalent number of radians. _Introduced in DataWeave version 2.4.0._

- `angdeg` — Number of degrees to convert into radians.

```dataweave
%dw 2.0
import * from dw::util::Math
output application/json
---
{
  "toRadians10":  toRadians(10),
  "toRadians013": toRadians(0.13),
  "toRadians-20": toRadians(-20)
}
```

```json
{
   "toRadians10": 0.1745329251994329576922222222222222,
   "toRadians013": 0.002268928027592628449998888888888889,
   "toRadians-20": -0.3490658503988659153844444444444444
 }
```
