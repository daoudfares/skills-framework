# dw::arrays — Arrays functions

Namespace `dw::core::Arrays`.
Requires an explicit import: `import * from dw::core::Arrays`.

Functions: `countBy`, `divideBy`, `drop`, `dropWhile`, `every`, `firstWith`, `indexOf`, `indexWhere`, `join`, `leftJoin`, `outerJoin`, `partition`, `slice`, `some`, `splitAt`, `splitWhere`, `sumBy`, `take`, `takeWhile`

---

## countBy

```
countBy<T>(@StreamCapable array: Array<T>, matchingFunction: (T) -> Boolean): Number
```

Counts the elements in an array that return `true` when the matching function is applied to the value of each element.

- `array` — The input array that contains elements to match.
- `matchingFunction` — A function to apply to elements in the input array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
---
{ "countBy" : [1, 2, 3, 4] countBy (($ mod 2) == 0) }
```

```json
{ "countBy": 2 }
```

```
countBy(array: Null, matchingFunction: (Nothing) -> Any): Null
```

Helper function that enables `countBy` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## divideBy

```
divideBy<T>(items: Array<T>, amount: Number): Array<Array<T>>
```

Breaks up an array into sub-arrays that contain the specified number of elements. When there are fewer elements in the input array than the specified number, the function fills the sub-array with those elements. When there are more elements, the function fills as many sub-arrays needed with the extra elements.

- `items` — Items in the input array.
- `amount` — The number of elements allowed per sub-array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
---
{
  "divideBy" : [
      { "divideBy2" : [1, 2, 3, 4, 5] divideBy 2 },
      { "divideBy2" : [1, 2, 3, 4, 5, 6] divideBy 2 },
      { "divideBy3" : [1, 2, 3, 4, 5] divideBy 3 }
  ]
}
```

```json
{
 "divideBy": [
  {
    "divideBy2": [
      [ 1, 2 ],
      [ 3, 4 ],
      [ 5 ]
    ]
  },
  {
    "divideBy2": [
      [ 1, 2 ],
      [ 3, 4 ],
      [ 5, 6 ]
    ]
  },
    {
      "divideBy3": [
        [ 1, 2, 3 ],
        [ 4, 5 ]
      ]
    }
 ]
}
```

```
divideBy(items: Null, amount: Any): Null
```

Helper function that enables `divideBy` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## drop

```
drop<T>(array: Array<T>, n: Number): Array<T>
```

Drops the first `n` elements. It returns the original array when `n <= 0` and an empty array when `n > sizeOf(array)`. _Introduced in DataWeave version 2.2.0._

- `array` — The left array of elements.
- `n` — The number of elements to take.

```dataweave
%dw 2.0
import * from dw::core::Arrays
var users = ["Mariano", "Leandro", "Julian"]
output application/json
---
drop(users, 2)
```

```json
[
  "Julian"
]
```

```
drop(array: Null, n: Any): Null
```

Helper function that enables `drop` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## dropWhile

```
dropWhile<T>(array: Array<T>, condition: (item: T) -> Boolean): Array<T>
```

Drops elements from the array while the condition is met but stops the selection process when it reaches an element that fails to satisfy the condition. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `condition` — The condition (or expression) used to match an element in the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var arr = [0,1,3,2,1]
---
arr dropWhile $ < 3
```

```json
[
  3,
  2,
  1
]
```

```
dropWhile(array: Null, condition: (item: Nothing) -> Any): Null
```

Helper function that enables `dropWhile` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## every

```
every<T>(list: Array<T>, condition: (T) -> Boolean): Boolean
```

Returns `true` if every element in the array matches the condition. The function stops iterating after the first negative evaluation of an element in the array.

- `list` — The input array.
- `condition` — A condition (or expression) to apply to elements in the input array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
var arr0 = [] as Array<Number>
output application/json
---
{ "results" : [
     "ok" : [
        [1,1,1] every ($ == 1),
        [1] every ($ == 1)
     ],
     "err" : [
        [1,2,3] every ((log('should stop at 2 ==', $) mod 2) == 1),
        [1,1,0] every ($ == 1),
        [0,1,1,0] every (log('should stop at 0 ==', $) == 1),
        [1,2,3] every ($ == 1),
        arr0 every true,
     ]
   ]
 }
```

```json
{
   "results": [
     {
       "ok": [ true, true ]
     },
     {
       "err": [ false, false, false, false, false ]
     }
   ]
 }
```

```
every(value: Null, condition: (Nothing) -> Any): Boolean
```

Helper function that enables `every` to work with a `null` value. _Introduced in DataWeave version 2.3.0._

## firstWith

```
firstWith<T>(array: Array<T>, condition: (item: T, index: Number) -> Boolean): T | Null
```

Returns the first element that satisfies the condition, or returns `null` if no element meets the condition. _Introduced in DataWeave version 2.3.0._

- `array` — The array of elements to search.
- `condition` — The condition to satisfy.

```dataweave
%dw 2.0
output application/json
import firstWith from dw::core::Arrays
var users = [{name: "Mariano", lastName: "Achaval"}, {name: "Ana", lastName: "Felisatti"}, {name: "Mariano", lastName: "de Sousa"}]
---
{
  a: users firstWith ((user, index) -> user.name == "Mariano"),
  b: users firstWith ((user, index) -> user.name == "Peter")
}
```

```json
{
  "a": {
    "name": "Mariano",
    "lastName": "Achaval"
  },
  "b": null
}
```

```
firstWith(array: Null, condition: (item: Nothing, index: Nothing) -> Any): Null
```

Helper function that enables `firstWith` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## indexOf

```
indexOf<T>(array: Array<T>, toFind: T): Number
```

Returns the index of the first occurrence of an element within the array. If the value is not found, the function returns `-1`. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `toFind` — The element to find.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var users = ["Mariano", "Leandro", "Julian"]
---
indexOf(users, "Julian")
```

```json
2
```

## indexWhere

```
indexWhere<T>(array: Array<T>, condition: (item: T) -> Boolean): Number
```

Returns the index of the first occurrence of an element that matches a condition within the array. If no element matches the condition, the function returns `-1`. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `condition` — The condition (or expression) used to match an element in the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var users = ["Mariano", "Leandro", "Julian"]
---
users indexWhere (item) -> item startsWith "Jul"
```

```json
2
```

```
indexWhere(array: Null, condition: (item: Nothing) -> Any): Null
```

Helper function that enables `indexWhere` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## join

```
join<L <: Object, R <: Object>(left: Array<L>, right: Array<R>, leftCriteria: (leftValue: L) -> String, rightCriteria: (rightValue: R) -> String): Array<Pair<L, R>>
```

Joins two arrays of objects by a given ID criteria. `join` returns an array all the `left` items, merged by ID with any right items that exist. _Introduced in DataWeave version 2.2.0._

- `left` — The left-side array of objects.
- `right` — The right-side array of objects.
- `leftCriteria` — The criteria used to extract the ID for the left collection.
- `rightCriteria` — The criteria used to extract the ID for the right collection.

```dataweave
%dw 2.0
import * from dw::core::Arrays
var users = [{id: "1", name:"Mariano"},{id: "2", name:"Leandro"},{id: "3", name:"Julian"},{id: "5", name:"Julian"}]
var products = [{ownerId: "1", name:"DataWeave"},{ownerId: "1", name:"BAT"}, {ownerId: "3", name:"DataSense"}, {ownerId: "4", name:"SmartConnectors"}]
output application/json
---
join(users, products, (user) -> user.id, (product) -> product.ownerId)
```

```json
[
  {
    "l": {
      "id": "1",
      "name": "Mariano"
    },
    "r": {
      "ownerId": "1",
      "name": "DataWeave"
    }
  },
  {
    "l": {
      "id": "1",
      "name": "Mariano"
    },
    "r": {
      "ownerId": "1",
      "name": "BAT"
    }
  },
  {
    "l": {
      "id": "3",
      "name": "Julian"
    },
    "r": {
      "ownerId": "3",
      "name": "DataSense"
    }
  }
]
```

## leftJoin

```
leftJoin<L <: Object, R <: Object>(left: Array<L>, right: Array<R>, leftCriteria: (leftValue: L) -> String, rightCriteria: (rightValue: R) -> String): Array<{ l: L, r?: R }>
```

Joins two arrays of objects by a given ID criteria. `leftJoin` returns an array all the `left` items, merged by ID with any right items that meet the joining criteria. _Introduced in DataWeave version 2.2.0._

- `left` — The left-side array of objects.
- `right` — The right-side array of objects.
- `leftCriteria` — The criteria used to extract the ID for the left collection.
- `rightCriteria` — The criteria used to extract the ID for the right collection.

```dataweave
%dw 2.0
import * from dw::core::Arrays
var users = [{id: "1", name:"Mariano"},{id: "2", name:"Leandro"},{id: "3", name:"Julian"},{id: "5", name:"Julian"}]
var products = [{ownerId: "1", name:"DataWeave"},{ownerId: "1", name:"BAT"}, {ownerId: "3", name:"DataSense"}, {ownerId: "4", name:"SmartConnectors"}]
output application/json
---
leftJoin(users, products, (user) -> user.id, (product) -> product.ownerId)
```

```json
[
  {
    "l": {
      "id": "1",
      "name": "Mariano"
    },
    "r": {
      "ownerId": "1",
      "name": "DataWeave"
    }
  },
  {
    "l": {
      "id": "1",
      "name": "Mariano"
    },
    "r": {
      "ownerId": "1",
      "name": "BAT"
    }
  },
  {
    "l": {
      "id": "2",
      "name": "Leandro"
    }
  },
  {
    "l": {
      "id": "3",
      "name": "Julian"
    },
    "r": {
      "ownerId": "3",
      "name": "DataSense"
    }
  },
  {
    "l": {
      "id": "5",
      "name": "Julian"
    }
  }
]
```

## outerJoin

```
outerJoin<L <: Object, R <: Object>(left: Array<L>, right: Array<R>, leftCriteria: (leftValue: L) -> String, rightCriteria: (rightValue: R) -> String): Array<{ l?: L, r?: R }>
```

Joins two array of objects by a given `ID` criteria. `outerJoin` returns an array with all the `left` items, merged by ID with the `right` items in cases where any exist, and it returns `right` items that are not present in the `left`. _Introduced in DataWeave version 2.2.0._

- `left` — The left-side array of objects.
- `right` — The right-side array of objects.
- `leftCriteria` — The criteria used to extract the ID for the left collection.
- `rightCriteria` — The criteria used to extract the ID for the right collection.

```dataweave
%dw 2.0
import * from dw::core::Arrays
var users = [{id: "1", name:"Mariano"},{id: "2", name:"Leandro"},{id: "3", name:"Julian"},{id: "5", name:"Julian"}]
var products = [{ownerId: "1", name:"DataWeave"},{ownerId: "1", name:"BAT"}, {ownerId: "3", name:"DataSense"}, {ownerId: "4", name:"SmartConnectors"}]
output application/json
---
outerJoin(users, products, (user) -> user.id, (product) -> product.ownerId)
```

```json
[
  {
    "l": {
      "id": "1",
      "name": "Mariano"
    },
    "r": {
      "ownerId": "1",
      "name": "DataWeave"
    }
  },
  {
    "l": {
      "id": "1",
      "name": "Mariano"
    },
    "r": {
      "ownerId": "1",
      "name": "BAT"
    }
  },
  {
    "l": {
      "id": "2",
      "name": "Leandro"
    }
  },
  {
    "l": {
      "id": "3",
      "name": "Julian"
    },
    "r": {
      "ownerId": "3",
      "name": "DataSense"
    }
  },
  {
    "l": {
      "id": "5",
      "name": "Julian"
    }
  },
  {
    "r": {
      "ownerId": "4",
      "name": "SmartConnectors"
    }
  }
]
```

## partition

```
partition<T>(array: Array<T>, condition: (item: T) -> Boolean): { success: Array<T>, failure: Array<T> }
```

Separates the array into the elements that satisfy the condition from those that do not. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements to split.
- `condition` — The condition (or expression) used to match an element in the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var arr = [0,1,2,3,4,5]
---
arr partition (item) -> isEven(item)
```

```json
{
  "success": [
    0,
    2,
    4
  ],
  "failure": [
    1,
    3,
    5
  ]
}
```

```
partition(array: Null, condition: (item: Nothing) -> Any): Null
```

Helper function that enables `partition` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## slice

```
slice<T>(array: Array<T>, from: Number, until: Number): Array<T>
```

Selects the interval of elements that satisfy the condition: `from <= indexOf(array) < until` _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `from` — The starting index of the interval of elements to include from the array. + If this value is negative, the function starts including from the first element of the array. If this value is higher than the last index of the array, the function returns an empty array (`[]`).
- `until` — The ending index of the interval of elements to include from the array. + If this value is higher than the last index of the array, the function includes up to the last element of the array. If this value is lower than the first index of the array, the function returns an empty array (`[]`).

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var arr = [0,1,2,3,4,5]
---
slice(arr, 1, 4)
```

```json
[
  1,
  2,
  3
]
```

```
slice(array: Null, from: Any, until: Any): Null
```

Helper function that enables `slice` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## some

```
some<T>(list: Array<T>, condition: (T) -> Boolean): Boolean
```

Returns `true` if at least one element in the array matches the specified condition. The function stops iterating after the first element that matches the condition is found.

- `list` — The input array.
- `condition` — A condition (or expression) used to match elements in the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
---
{ "results" : [
    "ok" : [
      [1,2,3] some (($ mod 2) == 0),
      [1,2,3] some ((nextNum) -> (nextNum mod 2) == 0),
      [1,2,3] some (($ mod 2) == 1),
      [1,2,3,4,5,6,7,8] some (log('should stop at 2 ==', $) == 2),
      [1,2,3] some ($ == 1),
      [1,1,1] some ($ == 1),
      [1] some ($ == 1)
    ],
    "err" : [
      [1,2,3] some ($ == 100),
      [1] some ($ == 2)
    ]
  ]
}
```

```json
{
   "results": [
     {
       "ok": [ true, true, true, true, true, true, true ]
     },
     {
       "err": [ false, false ]
     }
   ]
 }
```

```
some(list: Null, condition: (Nothing) -> Any): Boolean
```

Helper function that enables `some` to work with a `null` value. _Introduced in DataWeave version 2.3.0._

## splitAt

```
splitAt<T>(array: Array<T>, n: Number): Pair<Array<T>, Array<T>>
```

Splits an array into two at a given position. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `n` — The index at which to split the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var users = ["Mariano", "Leandro", "Julian"]
---
users splitAt 1
```

```json
{
  "l": [
    "Mariano"
  ],
  "r": [
    "Leandro",
    "Julian"
  ]
}
```

```
splitAt(array: Null, n: Any): Null
```

Helper function that enables `splitAt` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## splitWhere

```
splitWhere<T>(array: Array<T>, condition: (item: T) -> Boolean): Pair<Array<T>, Array<T>>
```

Splits an array into two at the first position where the condition is met. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements to split.
- `condition` — The condition (or expression) used to match an element in the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var users = ["Mariano", "Leandro", "Julian", "Tomo"]
---
users splitWhere (item) -> item startsWith "Jul"
```

```json
{
  "l": [
    "Mariano",
    "Leandro"
  ],
  "r": [
    "Julian",
    "Tomo"
  ]
}
```

```
splitWhere(array: Null, condition: (item: Nothing) -> Any): Null
```

Helper function that enables `splitWhere` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## sumBy

```
sumBy<T>(@StreamCapable array: Array<T>, numberSelector: (T) -> Number): Number
```

Returns the sum of the values of the elements in an array.

- `array` — The input array.
- `numberSelector` — A DataWeave selector that selects the values of the numbers in the input array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
---
{
  "sumBy" : [
    [ { a: 1 }, { a: 2 }, { a: 3 } ] sumBy $.a,
    sumBy([ { a: 1 }, { a: 2 }, { a: 3 } ], (item) -> item.a)
  ]
}
```

```json
{ "sumBy" : [ 6, 6 ] }
```

```
sumBy(array: Null, numberSelector: (Nothing) -> Any): Null
```

Helper function that enables `sumBy` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## take

```
take<T>(array: Array<T>, n: Number): Array<T>
```

Selects the first `n` elements. It returns an empty array when `n <= 0` and the original array when `n > sizeOf(array)`. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `n` — The number of elements to select.

```dataweave
%dw 2.0
import * from dw::core::Arrays
var users = ["Mariano", "Leandro", "Julian"]
output application/json
---
take(users, 2)
```

```json
[
  "Mariano",
  "Leandro"
]
```

```
take(array: Null, n: Any): Null
```

Helper function that enables `take` to work with a `null` value. _Introduced in DataWeave version 2.4.0._

## takeWhile

```
takeWhile<T>(array: Array<T>, condition: (item: T) -> Boolean): Array<T>
```

Selects elements from the array while the condition is met but stops the selection process when it reaches an element that fails to satisfy the condition. To select all elements that meet the condition, use the `filter` function. _Introduced in DataWeave version 2.2.0._

- `array` — The array of elements.
- `condition` — The condition (or expression) used to match an element in the array.

```dataweave
%dw 2.0
import * from dw::core::Arrays
output application/json
var arr = [0,1,2,1]
---
arr takeWhile $ <= 1
```

```json
[
  0,
  1
]
```

```
takeWhile(array: Null, condition: (item: Nothing) -> Any): Null
```

Helper function that enables `takeWhile` to work with a `null` value. _Introduced in DataWeave version 2.4.0._
