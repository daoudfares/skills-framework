# DataWeave language reference

Script structure, variables, functions, flow control, pattern matching, scoping and operators.

## DataWeave Language Guide

DataWeave is a functional language used in Mule applications to perform data transformations.
Before you begin to use DataWeave to code your own powerful and complex data transformations, you must understand the basic concepts of programming and the core features of functional programming languages.

DataWeave enables you to take advantage of the benefits of functional programming, including:

- Pure functions that always produce the same output given the same input, making them easier for you to debug.
- Immutable variables that do not change their value during the execution, adding stability to your code.
- Function signatures that provide additional transparency about what affects a function's execution, because pure functions depend on only their input parameters to produce a result.
- Functional languages produce code that’s easier to maintain because the code is concise and clear.
- A call-by-need strategy (also known as _lazy evaluation_) that improves performance, because expressions are evaluated only when they are needed and their result is stored to avoid evaluating an expression multiple times if the input parameters are the same.

### DataWeave Language Basic Concepts

DataWeave incorporates concepts that are common to most programming languages. All DataWeave scripts consist of a _header_ that contains important directives, including the output format of the transformation, and a _body_ that contains the expression to generate a result.

DataWeave supports different _data structures_, including _simple_, _complex_, and _composite_ types. In most of your DataWeave transformations, you use _data selectors_, _data operators_, and _functions_ alongside _arrays_ and _objects_ to perform data mappings or transformations.

You can also import prebuilt DataWeave _modules_ to extend the set of functions available to use in your scripts.

#### Architecture of a DataWeave Script

A DataWeave script consists of a _header_ and a _body_, separated by three dashes (`---`).
The header contains language directives (`import`, for example), defines the output format of the transformation, and can also contain variable and function declarations.
The body contains the expression that produces the resulting output, usually a data mapping or a transformation.

Here is an example of a basic DataWeave transformation:
```dataweave
%dw 2.0
output application/json
---
payload
```

#### Data Types

DataWeave represents data using values, each of which has a data type associated with it.
The type system enables you to apply constraints to variables and function parameters. The supported data types include simple types such as `String`, `Boolean`, `Number`, and `Date`, as well as composite and complex types such as `Array`, `Object`, and `Any`.

For a complete list of all supported data types, see Type System.

#### Data Selectors

Data selectors enable you to access fields within a data structure so that you can retrieve data from the payload or any other variable created during the DataWeave script execution.
Different types of selectors provide you with a variety of options that you can use to extract data from structures.

For example, you can use the _single-value selector_ `payload.userName` to retrieve the single value `userName`, where `userName` represents an actual key in the input message.

See Selectors for a complete list of data selectors and their usage.

#### Functions

A function is a code block that contains a group of operations that are executed when the function is called in your application. Functions can accept different parameters as input that can then be used by the operations defined in the function. Additionally, every function returns a value after it finishes processing, and this value can then be used as input for a different function.

Each DataWeave script that you write in any component (like a Transform Message component or Set Payload component) works as an independent program, meaning that all function definitions and calls are unique to the script defined in the component.

See Define DataWeave Functions for additional function definition details.

##### Function Definition vs. Function Call

DataWeave enables you to define your own functions in the header of the script, creating a blueprint for the process that defines the operations that are executed upon the function call. You can also define them in DataWeave mapping and module files.

When you _call_ a function from a DataWeave expression, you are instructing DataWeave to run all the operations defined in that function at that exact point of the script’s execution.

For example, `upper` is a built-in function defined in the String module. You can call this function to convert a text value to uppercase. Also, you can use a selector to retrieve a value from the payload, and then execute the `upper()` function call with this value as the input parameter `upper(payload.someKey)`.

DataWeave supports both _prefix_ notation (`function (param1, param2)`) and _infix_ notation (`param1 function param2`) for function calls. Note that you can use infix notation only with functions that accept only two parameters.

See also, Function Signatures.

#### Data Operators

Data operators are symbols that enable you to perform operations on data to produce a result. DataWeave supports operators that are common in most programming languages like mathematical (`+`, `-`, `/`, `*`), relational (`<`, `>`, `<=`, `>=`, `==`, `~=`), and logical (`not`, `!`, `and`, `or`) operators.

DataWeave also supports the following operators:

- Append (``+`), Prepend (``), and Remove (`-`), which enable you to manage data in an array.
- Scope and Flow control operators (`do`, `using`, `if`, `else`) that enable you to create a scope where new variables and functions can be declared, or to execute an expression based on a condition.
- Update (`update`), which enables you to update specific fields of a data structure.

See DataWeave Operators for a complete list of supported operators, their usage, and examples.

##### Import Function Modules

By default, DataWeave scripts import the `dw::Core` function module. To use functions from different modules, import the modules to your script by adding the `import` directive.

See DataWeave Reference for instructions on using the `import` directive.

#### Arrays

An array is a data structure that can contain any number of elements of the supported DataWeave types. To declare an array, use brackets (`[` and `]`) to enclose a comma-separated list of elements, for example: `[1,2,3]`.

Arrays also support the application of conditional logic to define conditional elements (`[(value1) if condition]`). For example, the expression `[(1) if true, (2) if false, (3) if payload != null]` defines the array `[1,3]` (assuming that `payload` is not `null`).

#### Objects

An object is a collection of zero or more `Key` and `value` pairs:

- `Key`, which is formed by:
  - `Name`, composed of a `String` value as the local name and an optional `Namespace`.
  - `Attributes`, a collection of zero or more `Name:value` pairs, where `value` can be any possible value.
- `Value`, comprising any supported type, including another object, a function call, or an array.

To declare an object, use braces (`{` and `}`) to enclose a comma-separated list of `Key:value` pairs:
```dataweave
{
  keyName @(keyAttributeName :"keyAttributeValue"): "value",
  User @(role:"admin"): upper("max the mule"),
  myArray: [1,2,3]
}
```

Objects also support the definition of conditional elements:
```dataweave
{
 (userName: name) if !isBlank(name),
 (userRole: role) if !isBlank(role)
}
```

### Functional Programming Principles

The functional programming paradigm enables developers to build applications by using pure function composition and immutable data. Because functional programming is declarative, functions in DataWeave are just expressions that return a value, instead of imperative statements that change program states.

DataWeave follows the core principles of functional programming, including pure functions, first-class functions, high-order functions, function composition, lambda expressions, and immutable data.

#### Pure Functions

Pure functions in programming are similar to pure functions in mathematics in that, given a certain input, they always return the same output. Also, executing a function has no impact on other parts of a program, other than producing a result.
All functions in DataWeave are pure; they are not affected by external values that could change the result of the execution.

#### First-Class Functions

The pure functions in DataWeave are also “first-class citizens” in that they support operations that are available to any other data type, including being stored in variables, passed as parameters, and returned as results.

#### High-Order Functions

High-order functions in programming also have the same concept as in mathematics. These functions take one or more functions as parameters and return a function as a result. The result of a high-order function can then be used as an input parameter in another function, enabling the concept of _function composition_.

#### Function Composition

Function composition is the process by which functions are combined to build complex operations. In this case, the result of executing one function serves as an input parameter for the next function. In DataWeave, all data transformations are a chain of expressions, functions composed to obtain a final result that outputs the data as needed.

##### Example of Function Composition

The following example uses the function `pluck` to map an object into an array. Then the resulting array serves as input for the function `filter`, which selects the elements in the array that have a `Role` equal to `ADMIN`. During the mapping process, the function `upper` transforms the `role` value:

```dataweave
%dw 2.0
output application/json
var collaborators =
{
    Max: {role: "admin", id: "01"},
    Einstein: {role: "dev", id: "02"},
    Astro: {role: "admin", id: "03"},
    Blaze: {role: "user", id: "04"}
}
---
collaborators pluck ((value,key,index)->  {
        "Name": key,
        "Role": upper(value.role),
        "ID": value.id
    })
    filter ((item, index) -> item.Role == "ADMIN")
```

The following example shows the same expression, but it uses prefix notation.
This syntax helps visualize how `filter` takes as the first parameter the result of `pluck`.

```dataweave
%dw 2.0
output application/json
var collaborators =
{
    Max: {role: "admin", id: "01"},
    Einstein: {role: "dev", id: "02"},
    Astro: {role: "admin", id: "03"},
    Blaze: {role: "user", id: "04"}
}
---
filter(
   pluck(
       collaborators, (value,key,index)->
       {
           "Name": key,
           "Role": upper(value.role),
           "ID": value.id
       }),
   (item, index) -> item.Role == "ADMIN")
```

The output of both expressions is:
```dataweave
[
  {
    "Name": "Max",
    "Role": "ADMIN",
    "ID": "01"
  },
  {
    "Name": "Astro",
    "Role": "ADMIN",
    "ID": "03"
  }
]
```

#### Lambda Expressions

Lambda expressions, also known as _anonymous functions_ or _function literals_, are function definitions that do not have an identifier name and can be passed as parameters to high-order functions. Lambda syntax is expressed in the form `(a,b) -> c`, which can be read as “Given a certain input (`a` and `b`), execute the following (`c`).”

For example, the `map` function in DataWeave accepts a lambda expression as one of its parameters: `map(Array<T>, (item: T, index: Number) -> R): Array<R>`.
`map` iterates over the items in an array and executes the lambda expression that is passed as a parameter. This lambda expression consists of two parameters that represent the value (`item`) and index (`index`) of each array element during the execution, and a function definition to execute during the iteration `R`.

The following code example shows a `map` function that receives a lambda expression to concatenate the index and the value of each element in the array it iterates on, and then returns these values as a new array:

Source
```dataweave
%dw 2.0
output application/json
---
["Max", "the", "Mule"] map (item, index) -> index ++ " - " ++ item
```

Output
```dataweave
[
    "0 - Max",
    "1 - the",
    "2 - Mule"
]
```

See Work with Functions and Lambdas in DataWeave for additional information about Lambda expressions.

#### Immutable Data

In DataWeave, variables cannot change their assigned value after they are defined. This ensures that there are no unexpected results from executing functions. If you want to store a new value that is the result of an operation, you must declare a new data structure.

### Differences with Imperative Programming

If you have a development background in working with object-oriented programming languages, it is important to understand that functional programming separates data from functions and does not use loop control statements.

#### Separation of Data and Functions

DataWeave does not use assignment statements, which ensures that data remains immutable. Because there are no getter and setter methods, nor classes containing data structures and behavior, each function works only with the data you provide as input. If you need to modify any existing data structure, you create a new copy and apply functions to modify its values.

#### Control Flow Statements

There are no loop control statements like `for` or `while` in DataWeave. In DataWeave, instead of defining how to execute a procedure using iteration, you focus on your current requirements when you write the expressions.

For example, to make changes to a list, you use the `map` function to apply changes to the elements in the collection. Additionally, you can use the `filter` function to remove specific elements from a list, or the `reduce` function to collapse all values from an array into one single value.

However, you can use `if-else` statements to apply a condition when executing an expression:

```dataweave
%dw 2.0
var myVar = { country : "FRANCE" }
output application/json
---
if (myVar.country == "USA")
  { currency: "USD" }
else { currency: "EUR" }
```

##### DataWeave Examples

For usage examples of `map`, `reduce`, and `filter`, see:

- Map Data with DataWeave
- Conditionally Reduce a List through a Function
- Merge Fields from Separate Objects

### See Also

- Mule Message Structure
- Mule Events
- Core Components
- Connectors and Modules
- Transform Message Component

---

## DataWeave Variables

DataWeave is a functional programming language in which variables behave just like functions. DataWeave uses eager evaluation for variables and function parameters. In addition, DataWeave variables are immutable.
A variable is assigned a value, which is either a constant (such as `var msg = "hello"`) or a lambda expression such as `() -> "hello"`.

### DataWeave Variable Assignment

Here are some examples of DataWeave 2.0 variable assignments:

**Example: Variable Assignment in a DataWeave Script**

```dataweave
%dw 2.0
output application/json
var msg = "Hello"

var msg2 = (x = "ignore") -> "hello"

var toUpper = (aString) -> upper(aString)

var combined = (function, msg="universe") -> function(msg ++ " WORLD")
---
[
   msg: msg,
   msg2: msg2(),
   toUpper: toUpper(msg),
   combined: combined(toUpper, "hello"),
   combined2: combined(((x) -> lower(x) ++ " Today"), msg)
]
```

The previous script results in this output:

**Example: Output**

```json
[
  {
    "msg": "Hello"
  },
  {
    "msg2": "hello"
  },
  {
    "toUpper": "HELLO"
  },
  {
    "combined": "HELLO WORLD"
  },
  {
    "combined2": "hello world Today"
  }
]
```

In these examples:

- The `msg` var is assigned to a constant.
- `msg2` is assigned to an expression that maps to a constant, so `msg2()` behaves the same way as `msg`, without the `()`.
- The `toUpper` variable maps an input parameter to the DataWeave `upper` function. So it is used like a more traditional function in other languages as `toUpper(aString)`.
- The `combined` variable accepts a function as an input parameter, then applies that function name to the second `msg` argument. The second `msg` argument is optional because a default value `universe` is specified.

The result of the expression `combined(toUpper, " world")` is to apply the `toUpper` function defined earlier in the header to the `msg` parameter value `world`. The supplied second argument `world` overrides the `msg="universe"` default value, so the result is `HELLO WORLD`. The expression `combined(toUpper)`, which omits the second argument, uses the default `msg` value to return `"combined": "UNIVERSE WORLD"`.

The `combined2: combined(((x) -> lower(x) ++ " Today")), msg)`  defines the lambda expression that you can reuse in different contexts. In the example, `combined2` key defines the expression “in place” at the time the function is called.

Note that these types of “in place” expressions are called closures in languages like JavaScript.

DataWeave includes syntactic sugar to make it easier to access lambda expressions that are assigned to a variable as functions. To do this, you replace the `var` directive with the `fun` directive, and replace the arrow `->` in the lambda expression with an equal  sign (`=`). You also move the lambda expression arguments next to the function name so the syntax looks like a function declaration in other procedural programming languages. This enables you to use variables as if they were functions. So the previous example can be equivalently written as:

```dataweave
%dw 2.0
output application/json
var msg = "Hello"

var toUpper = (aString) -> upper(aString)
var toLower = (aString) -> lower(aString)

fun msg2(optParm = "ignore") = "hello"

fun toTitle(text: String) = toLower(text[0]) ++ toUpper(text[1 to -1])

fun combined(function, msg="universe") = function(msg ++ " world")
---
[
   msg: msg,
   msg2: msg2(),
   toUpper: toTitle(msg),
   combined: combined(toUpper, msg),
   combined2: combined((x) -> lower(x) ++ " today", msg)
]
```

This example produces the same result:

```json
[
  {
    "msg": "Hello"
  },
  {
    "msg2": "hello"
  },
  {
    "toUpper": "hELLO"
  },
  {
    "combined": "HELLO WORLD"
  },
  {
    "combined2": "hello world today"
  }
]
```

The important distinction in DataWeave is that functions are variables, and every function is just a syntactical renaming of the underlying `var` syntax, which allows you to pass function names or lambda expressions as arguments to other functions. The `fun` syntax allows you to access the powerful functional programming aspects of DataWeave while also being able to write simpler expressions as function calls you might be more familiar with.

Also notice that DataWeave variables (and functions) can specify any number of optional arguments by providing default values, so long as all those optional arguments are last in the argument list.

### Example: Declare an Array Variable and Transform its Elements

Variables are immutable in DataWeave, however you can iterate over an array variable and apply a transformation to its elements, which can then be assigned to new variables. The following example declares two array variables, iterates over them to transform their elements, and then declares an object containing two new arrays with the transformed elements:

DataWeave Source:

```dataweave
include::partial$examples-dw/variables-array-transform/transform.dwl[]
```

Output:
```json
include::partial$examples-dw/variables-array-transform/out.json[]
```

### Naming Rules for Variables

You can declare any variable name that is a valid identifier. See Rules for Declaring Valid Identifiers for more details.

### Variable Scopes

You can initialize and use both global and local variables in DataWeave scripts.

- Global variables are initialized in the header of the DataWeave script and can be referenced by name from anywhere in the body of a DataWeave script.
The header of a DataWeave script accepts a `var` directive that initializes a variable, for example: `var language='Español'`. You can declare multiple global variables on separate lines in the header.
- Local variables are initialized in the body of the DataWeave script and can be referenced by name only from within the scope of the expression where they are initialized.
The syntax for initializing a local variable looks like this:
```dataweave
do {
      [type <name> = <type expression>]*
      [var <name> = <expression>]*
      [fun <name>(<params>*) = <expression>]*
      [ns <name> <nsUri>]*
      ---
      <body>
}
```

Note that DataWeave variables cannot be reassigned. They are also distinct from variables that are part of the Mule message (such as target variables). DataWeave variables do not persist beyond the scope of the script in which they are initialized.

### Example: Global DataWeave Variables

This example defines a `do` operation that initializes a `language` variable with the constant value `Español` and returns that constant value. The body of the DataWeave script calls the
`do` operation using the variable `myVar`, which populates the `<language/>` element in the
XML output with the value `Español`.

**Transform**

```dataweave
%dw 2.0
output application/xml
var myVar = do {
    var language = "Español"
    ---
    language
}
---
{
  document: {
    language: myVar,
    text: "Hola mundo"
  }
}
```

**Output**

```xml
<?xml version='1.0' encoding='UTF-8'?>
<document>
  <language>Español</language>
  <text>Hola mundo</text>
</document>
```

### Example: Local DataWeave Variables

To initialize local variables, you can use either literal expressions, variable reference expressions, or functional expressions. These expressions can reference any other local variables within their scope or any input or global variables.

As a best practice, declare local variables within `do` scopes (see Flow Control in DataWeave). The alternative method of declaring a scope with the `using` keyword is no longer recommended and available only to provide compatibility.

You can only reference a local variable by name from within the scope of the expression that initializes it. The declaration can be prepended to any literal expression. The literal delimits the scope of the variable, so you cannot reference any variable outside of its scope.

The examples that follow show initialization of local variables.

**Example: Scoped to a Simple Value**

The following example sets the local variable `myVar` in a `do` scope. It calls `do` from the body of the DataWeave script:

```dataweave
%dw 2.0
output application/json
---
do {
      var myVar = 2
      ---
      3 + myVar
}
```

The result is `5`.

**Example: Scoped to an Array Literal**

The following example sets the local variable `myVar` in a `do` scope and uses it to set the value of the second element in the array to `2`:

```dataweave
%dw 2.0
output application/json
---
do {
      var myVar = 2
      ---
      [1, myVar, 3]
}
```

The result is `[ 1, 2, 3]`

**Example: Scoped to the Object literal**

In the following example, references to all the variables are valid. `fn` and `ln` are defined and called within the `do` scope. The global `myVar` variable is also accessible from that scope.

```dataweave
%dw 2.0
var myVar = 1234
var myDo =  do {
    var fn = "Annie"
    var ln = "Point"
    ---
    {
      id : myVar,
      firstname : fn,
      lastname : ln
    }
}
output application/xml
---
{ person : myDo }
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
<person>
  <id>1234</id>
  <firstname>Annie</firstname>
  <lastname>Point</lastname>
</person>
```

**Example: **Invalid Reference** That Is Outside the Scope**

The following example produces an error because `fromDoScope` is referenced from outside the scope of `do`. As a consequence, the concatenation operation (``) cannot append the name-value pair to the collection.

```dataweave
%dw 2.0
var myVar = 1234
var myDo =  do {
    var fn = "Annie"
    var ln = "Point"
    var fromDoScope = "Platform"
    ---
    {
      id : myVar,
      firstname : fn,
      lastname : ln
    }
}
output application/xml
---
{
    person : myDo ++ { "outsideDoScope" : fromDoScope }
}
```

The invalid example returns this error:
`Unable to resolve reference of fromDoScope.`

**Example: Reference That Is Inside a Function**

The following example passes the string `HELLO` to the `test` function defined in the header. The `do` scope accepts the string, converts it to lowercase, and then concatenates that string to the `suffix` variable, which is also defined in the header of the scope.

```dataweave
%dw 2.0
fun test(param1: String) = do {
    var suffix = "123"
    fun innerTest(str: String) = lower(str)
   ---
   innerTest(param1 ++ suffix)
}
output application/json
---
test("HELLO")
```

The result is `"hello123"`.

### Variables Assigned as Lambda Expressions

When a variable is assigned a lambda expression, it behaves just like a function. Like a function, the lambda expression for a variable assignment can include parameters that can be used in the right-hand side expression, such as `(string) -> upper(string)`, which will convert any string to uppercase.

Other variables can also be passed as arguments to another variable's lambda expression. This example shows how the `toUpper` variable's lambda expression can be passed by name into the `addSuffix` variable's lambda expression.

```dataweave
%dw 2.0
output application/json
var toUpper = (aString) -> upper(aString)

var addSuffix = (msg, aFunction, suffix) -> aFunction(msg ++ suffix)
---
addSuffix("hello", toUpper, " world") //result is "HELLO WORLD"
```

### @Lazy() Annotation

When you are writing a DataWeave script in Studio, you might see the internal annotation `@Lazy()` in autocompletion suggestions. This annotation is not intended for general use and does not improve the performance of your scripts.

---

## Define DataWeave Functions

You can define your own DataWeave functions using the `fun` declaration in the header of a DataWeave script.

### DataWeave Function Definition Syntax

To define a function in DataWeave use the following syntax:
```text
fun myFunction(param1, param2, ...) = <code to execute>
```

- The `fun` keyword starts the definition of a function.
- `myFunction` is the name you define for the function.
Function names must be valid identifiers. For additional details about valid identifiers, see Rules for Declaring Valid Identifiers.
- `(param1, param2, ... , paramn)` represents the parameters that your function accepts.
You can specify from zero to any number of parameters, separated by commas (`,`) and enclosed in parentheses.
- The `=` sign marks the beginning of the code block to execute when the function is called.
- `<code to execute>` represents the actual code that you define for your function.

### Example Function Definitions

The following example defines a DataWeave function that accepts a single string argument, calls the `upper` function using the received string argument, and then outputs the result:

**Example: Simple Function Definition**

```dataweave
%dw 2.0
output application/json
fun toUpper(aString) = upper(aString)
---
toUpper("hello")
```

**Output**

```text
"HELLO"
```

The next example shows how the argument to a DataWeave function can be any DataWeave expression:

**Example: Using Expressions as Arguments**

```dataweave
%dw 2.0
output application/json
fun toUpper(aString) = upper(aString)
---
toUpper("h" ++ "el" ++ lower("LO") )
```

**Output**

```text
"HELLO"
```

The following example tests the type of the argument passed to the function by performing pattern matching with the built-in `match` operation:

**Example: Function that Uses Pattern Matching**

```dataweave
%dw 2.0
output application/json
fun toUpper(aString)
= aString match {
  case is String -> upper(aString)
  else -> null
}
---
toUpper("h" ++ "el" ++ lower("LO") )
```

**Output**

```text
"HELLO"
```

This example creates a function that reformats a numeric string into a common phone number format:

**Example: toPhoneFormat() Function**

```dataweave
%dw 2.0
output application/json
fun toPhoneFormat(str: String) =
    "(" ++ str[0 to 2] ++ ") " ++ str[3 to 5] ++ "-" ++ str[6 to 9]
---
toPhoneFormat("1234567890")
```

**Output**

```text
"(123) 456-7890"
```

### Type Constraint Definition

You can define type constraint expressions when you declare functions to ensure that the arguments for a function call respect the defined type constraint.

To define type constraints for functions, use the following syntax:
```text
fun myFunction(param1: Type, param2: Type): ResultType = <code to execute>
```

**Example: Function with Type Constraints**

```text
%dw 2.0
output application/json
fun toUser(id: Number, userName: String): String = "you called the function toUser!"
```

In this example, the type constraints define that the function `toUser` accepts only a first argument of type `Number` and a second argument of type `String`.

Also, the function specifies a constraint for the result to be of type `String`. This return type constraint does not affect the function call; rather, this constraint applies to the function code to validate that the function generates a result of the defined type.

You can find more details about the DataWeave type system in https://docs.mulesoft.com/dataweave/latest/dataweave-type-system.

### Optional Parameters Definition

You can define optional parameters by assigning a default value to them. The following example shows a function that defines one parameter that is mandatory (`name`) and a second parameter that is optional (`countryCode`) and has a default value:

**Example: Function with Optional Parameters**

```dataweave
%dw 2.0
output application/json
fun createUserData(name, countryCode = "US") = { "User name" : name, "Location": countryCode}
---
[createUserData("Cristian", "AR"), createUserData("Max The Mule")]
```

**Output**

```text
[
  {
    "User name": "Cristian",
    "Location": "AR"
  },
  {
    "User name": "Max The Mule",
    "Location": "US"
  }
]
```

#### Optional Parameter Order

DataWeave enables you to define optional parameters at the beginning or at the end of the parameter definition:

**Example: Functions with Optional Parameters**

```dataweave
%dw 2.0
output application/json
fun optionalParamsLast(a, b = 2, c = 3)
fun optionalParamsFirst(a = 1, b = 2, c)
```

When you call a function, the arguments are assigned from left to right. However, if you define optional parameters first, then the arguments are assigned from right to left. In addition, if all the parameters in a function are optional, the assignment is also from right to left:

**Example: Optional Parameter Assignment**

```dataweave
%dw 2.0
output application/json
fun optionalParamsLast(param1, param2 = 2, param3 = 3) =
    { "param1": param1, "param2": param2, "param3": param3}
fun optionalParamsFirst(param1 = 1, param2 = 2, param3) =
    { "param1": param1, "param2": param2, "param3": param3}
fun allParametersOptional(param1 = 1, param2 = 2, param3 = 3) =
    { "param1": param1, "param2": param2, "param3": param3}
---
{
  "optionalParamsLast(A)":optionalParamsLast('A'),
  "optionalParamsLast(A, B)":optionalParamsLast('A', 'B'),
  "optionalParamsLast(A, B, C)":optionalParamsLast('A', 'B', 'C'),
  "optionalParamsFirst(A)":optionalParamsFirst('A'),
  "optionalParamsFirst(A, B)":optionalParamsFirst('A', 'B'),
  "optionalParamsFirst(A, B, C)":optionalParamsFirst('A', 'B', 'C'),
  "allParametersOptional(A)":allParametersOptional('A'),
  "allParametersOptional(A, B)":allParametersOptional('A', 'B'),
  "allParametersOptional(A, B, C)":allParametersOptional('A', 'B', 'C')
}
```

**Output**

```text
{
  "optionalParamsLast(A)": {
    "param1": "A",
    "param2": 2,
    "param3": 3
  },
  "optionalParamsLast(A, B)": {
    "param1": "A",
    "param2": "B",
    "param3": 3
  },
  "optionalParamsLast(A, B, C)": {
    "param1": "A",
    "param2": "B",
    "param3": "C"
  },
  "optionalParamsFirst(A)": {
    "param1": 1,
    "param2": 2,
    "param3": "A"
  },
  "optionalParamsFirst(A, B)": {
    "param1": 1,
    "param2": "A",
    "param3": "B"
  },
  "optionalParamsFirst(A, B, C)": {
    "param1": "A",
    "param2": "B",
    "param3": "C"
  },
  "allParametersOptional(A)": {
    "param1": 1,
    "param2": 2,
    "param3": "A"
  },
  "allParametersOptional(A, B)": {
    "param1": 1,
    "param2": "A",
    "param3": "B"
  },
  "allParametersOptional(A, B, C)": {
    "param1": "A",
    "param2": "B",
    "param3": "C"
  }
}
```

### Type Parameters Definition

DataWeave function definitions support the use of type parameters, which are similar to generics in some programming languages.

**Example: Function that Uses Type Parameters**

```text
%dw 2.0
output application/json

fun toArray<T>(x: T): Array<T> = [x]
---
toArray(2)
```

DataWeave also supports adding type parameter constraints, which limit accepted inputs for a function.

**Example Function that Uses Type Parameters with Constraints**

```text
%dw 2.0
output application/json

fun getName<T <: { name: String }>(x: T): String = x.name
---
{
  name: getName({ name: "Andrés" })
  //name: getName({ age: 20 }) invalid call as the parameter does not fullfill the constraint
}
```

### Function Overloading

DataWeave enables you to create multiple functions with the same name but different parameters. This feature is useful for defining different behaviors based on the arguments of a function call.

Parameters in overloaded functions differ in number or type. To understand more about defining type constraints on function parameters, see Type System.

DataWeave uses the first function it finds that accepts the arguments of the function call, based on the order in which the functions are declared in the script.

**Example: Function that Uses Function Overloading**

```dataweave
%dw 2.0
output application/json

fun toUpper(a: String) = upper(a)
fun toUpper(a: Any) = null
fun toUpper(a: String, b: Number) = upper(a) ++ b as String
---
toUpper("hi!")
```

The argument of the function call `toUpper("hi!")` matches the types String and Any, so it is possible to call the function with the first two definitions. However, DataWeave executes the function `fun toUpper(a: String) = upper(a)` because that function is defined before the one that uses the type Any.

**Output of toUpper("hi!")**

```text
"HI!"
```

**Output of toUpper(true)**

```text
null
```

**Output of toUpper("age: ", 26)**

```text
"AGE: 26"
```

### See Also

Create Custom Modules and Mappings

DataWeave Reference

---

## Flow Control and Scope Operations in DataWeave

You can use the following operators within any DataWeave expression:

- `do`
- `if else`
- `else if`

### `do`

A `do` statement creates a scope in which new variables, functions, annotations, or namespaces can be declared and used. The syntax is similar to a mapping in that it is composed of a header and body separated by `---`. Its header is where all the declarations are defined, and its body is the result of the expression.

This example uses `do` to return the string `"DataWeave"` when `myfun()` is called from the main body of the script.

**DataWeave Script:**

```dataweave
%dw 2.0
output application/json
fun myfun() = do {
    var name = "DataWeave"
    ---
    name
}
---
{ result: myfun() }
```

This example uses `do` to return the string `"DataWeave"` when the variable `myVar` is referenced from the main body of the script.

**DataWeave Script:**

```dataweave
%dw 2.0
output application/json
var myVar = do {
    var name = "DataWeave"
    ---
    name
}
---
{ result: myVar }
```

Both scripts produce this output:

**Output:**

```json
{
  "result": "DataWeave"
}
```

The next example uses `do` to prepend the string `"Foo"` to a string (`" Bar"`) that is passed to the `test(p: String)` function.

**DataWeave Script:**

```dataweave
%dw 2.0
output application/json
fun test(p: String) = do {
    var a = "Foo" ++ p
    ---
    a
}
---
{ result: test(" Bar") }
```

**Output:**

```json
{
  "result": "Foo Bar"
}
```

See also, Examples: Local DataWeave Variables.

### `if else`

An `if` statement evaluates a conditional expression and returns the value under the `if` only if the conditional expression returns `true`. Otherwise, it returns the expression under `else`. Every `if` expression must have a matching `else` expression.

The following example uses the input `{ country : "FRANCE" }`, which is defined by the `myVar` variable in the header:

**DataWeave Script:**

```dataweave
%dw 2.0
var myVar = { country : "FRANCE" }
output application/json
---
if (myVar.country == "USA")
  { currency: "USD" }
else { currency: "EUR" }
```

**Output:**

```text
{
  "currency": "EUR"
}
```

You can use the if-else construct on any condition that evaluates to `true` or `false`, including mathematical, logical, equality, and relational
statements. The condition can act on any valid input.

The next DataWeave script applies `if else` statements to the result of the following conditional statements:

- A mathematical operation in `ex1` +
The `if else` statement returns the Boolean value `true` if the operation `1 + 1 == 55` is true and `false` if not.
- An equality operation in `ex2` +
The `if else` statement returns `1` if the value of the specified index is `1` or a string if the value is not `1`.
- An `isEmpty` function in `ex3` +
The `if else` statement returns the string `"ID is empty"` or `"ID is not empty"` depending on whether `aRecord.bookId` contains a value.
- A mapping in `ex4` that iterates over `firstInput` +
The `if else` statement returns the value of the `bookId` as a Number if the value is equal to `101`. It returns the specified string if the value is not equal to `101`.

**DataWeave Script:**

```dataweave
%dw 2.0
var aRecord =
 [
    "bookId":"101",
    "title":"world history",
    "price":"19.99"
 ]
output application/xml
---
{ examples:
	{
	   ex1 : if (1 + 1 == 55) true
	         else false,
	   ex2 : if ([1,2,3,4][1] == 1) 1
	         else "value of index 1 is not 1",
	   ex3 : if (isEmpty(aRecord.bookId)) "ID is empty"
	  	 else "ID is not empty",
	   ex4 : aRecord.bookId map (idValue) ->
	   	 if (idValue as Number == 101) idValue as Number
		 else "not 101"
	}
}
```

**Output:**

```text
<?xml version='1.0' encoding='UTF-8'?>
<examples>
  <ex1>false</ex1>
  <ex2>value of index 1 is not 1</ex2>
  <ex3>ID is not empty</ex3>
  <ex4>101</ex4>
</examples>
```

Additional examples are available in DataWeave Operators.

### `else if`

You can chain several `else` expressions together within an if-else construct by incorporating `else if`.
The following example uses the input `var myVar = { country : "UK" }`, which is defined by the `myVar` variable in the header.

**DataWeave Script:**

```dataweave
%dw 2.0
var myVar = { country : "UK" }
output application/json
---
if (myVar.country =="USA")
	{ currency: "USD" }
else if (myVar.country =="UK")
	{ currency: "GBP" }
else { currency: "EUR" }
```

**Output**

```text
{
  "currency": "GBP"
}
```

The following example is similar but takes an array as input instead of an object. The body of the script uses `if else` and `else if` statements within a `do` operation to populate the value of the `hello` variable.

**DataWeave Script:**

```dataweave
%dw 2.0
output application/json
---
["Argentina", "USA", "Brazil"] map (country) -> do {
  var hello = if(country == "Argentina") "Hola"
   else if(country == "USA") "Hello"
   else if(country == "Brazil") "Ola"
   else "Sorry! We don't know $(country)'s language."
   ---
   "$(hello) DataWeave"
}
```

**Output:**

```text
[
  "Hola DataWeave",
  "Hello DataWeave",
  "Ola DataWeave"
]
```

### See Also

- DataWeave Types
- DataWeave Selectors

---

## Precedence in DataWeave

DataWeave expressions are compiled in a specific order. The result of
a compilation of something at one level can serve as input for expressions
in higher levels, but not at lower levels.

### Order of Compilation

The following table orders operators and functions from first compiled (1) to
last compiled (10):

| Level | Operator or Function |
|---|---|
| 1 |  · `using`: For initializing local variables in a DataWeave script. · Unary DataWeave operators at this level: · `.^`: Schema selector. · `.#`: Namespace selector. · `..`: Descendants selector. · `not`: Logical operator for negation. · `.@`: All attribute selector, for example, in a case that uses the expression `payload.root.a.@` to return the attributes and values of the input payload `<root> <a attr1="foo" attr2="bar" /></root>` within the array of objects `{ "attr1": "foo", "attr2": "bar" }`. |
| 2 |  · `as`: Used for type coercion. |
| 3 |  · `*`: Multiply. · `/`: Divide. |
| 4 |  · `+`: Add. · `-`: Subtract. · `>>`: Prepend data. · `<<`: Append data. |
| 5 |  · `>`: Greater than or equal to. · `=`: Equal to. · `<`: Less than or equal to. · `<`: Less than. · `>`: Greater than. · `is`: Compare type, for example, used in Remove Specified XML Attributes. |
| 6 |  · `!=`: Not equal to. · `~=`: Contains. · `==`: Equality operator that tries to coerce one value to the type of the other when the types are different. |
| 7 |  · `and`: Logical `and` operator. |
| 8 |  · `or`: Logical `or` operator. |
| 9 |  · `default`: For setting a default value. · `case` and `else`: For pattern matching. · DataWeave functions at this level: · `matches` · `match` · `map` · `mapObject` · `groupBy` · `filter` · Binary DataWeave selectors at this level: · `.@keyName` and `.**@`: Binary DataWeave attribute selectors. · `.**`: Multi-value selector. · `.^`: Metadata selector. · `.&`: Key-value pair selector. · `[?()]`: Filter selector. · `.keyName`: Value selector. · `[<index> to <index>]`: Range selector |
| 10 |  · `if else`: Conditional expression used for flow control in DataWeave. |

### Order of Chained Function Calls

When functions are chained together in a series, the functions are processed
in order from the first to the last function specified in the chain.

For example, the following script acts on the input array of objects defined
by the variable `flights`. The script first calls `filter` to return an array
that accepts all `price` values that are less than 500. Then it calls
`orderBy` to return an array that reorders the objects found in the input
from the lowest to the highest `price` value. Finally, it calls `groupBy`
to group the input array of objects alphabetically by `toAirport` value.

**DataWeave Script:**

```dataweave
%dw 2.0
output application/json
var flights = [
  { "toAirport": "SFO", "price": 550, "airline": "American" },
  { "toAirport": "MUA", "price": 200, "airline": "American" },
  { "toAirport": "SFO", "price": 300, "airline": "American" },
  { "toAirport": "CLE", "price": 600, "airline": "American" },
  { "toAirport": "CLE", "price": 190, "airline": "American" },
  { "toAirport": "SFO", "price": 400, "airline": "American" }
]
---
flights filter $.price < 500 orderBy $.price groupBy $.toAirport
```

The result is an object that contains a collection of key-value pairs:

**Output:**

```text
{
  "CLE": [
    {
      "toAirport": "CLE",
      "price": 190,
      "airline": "American"
    }
  ],
  "SFO": [
    {
      "toAirport": "SFO",
      "price": 300,
      "airline": "United"
    },
    {
      "toAirport": "SFO",
      "price": 400,
      "airline": "American"
    }
  ],
  "MUA": [
    {
      "toAirport": "MUA",
      "price": 200,
      "airline": "American"
    }
  ]
}
```

You can force the evaluation order by inserting evaluation parentheses `(` and `)` into the DataWeave expression. This example returns the same output as the previous example:

**DataWeave Script:**

```dataweave
%dw 2.0
output application/json
var flights = [
  { "toAirport": "SFO", "price": 550, "airline": "American" },
  { "toAirport": "MUA", "price": 200, "airline": "American" },
  { "toAirport": "SFO", "price": 300, "airline": "American" },
  { "toAirport": "CLE", "price": 600, "airline": "American" },
  { "toAirport": "CLE", "price": 190, "airline": "American" },
  { "toAirport": "SFO", "price": 400, "airline": "American" }
]
---
( ( ( flights filter $.price < 500 ) orderBy $.price ) groupBy $.toAirport )
```

The result is an object that contains a collection of key-value pairs:

**Output:**

```text
{
  "CLE": [
    {
      "toAirport": "CLE",
      "price": 190,
      "airline": "American"
    }
  ],
  "SFO": [
    {
      "toAirport": "SFO",
      "price": 300,
      "airline": "United"
    },
    {
      "toAirport": "SFO",
      "price": 400,
      "airline": "American"
    }
  ],
  "MUA": [
    {
      "toAirport": "MUA",
      "price": 200,
      "airline": "American"
    }
  ]
}
```

The order of the function calls is important. For example, the rearranged
expression `flights groupBy $.toAirport filter $.price < 500 orderBy $.price`
returns an error because `groupBy` returns an object, and `filter`
expects an array. The resulting error is
`Expecting Type: Array>T<, but got: {String: Array<{|toA... airline: String|}>}`.

### See Also

- Core (dw::Core) functions
- DataWeave Operators
- DataWeave Selectors
- DataWeave Variables
- Flow Control in DataWeave
- Pattern Matching in DataWeave
- Type Coercion with DataWeave

---

## Pattern Matching in DataWeave Through match Statements

The `match` statement behaves like a `match` or `switch` statement in other
languages, like Java or C++, and routes an input expression to a particular
output expression based on some conditions.

**match Statement Syntax:**

```dataweave
inputExpression match {
  case <condition> -> <routing expression>
  case <condition> -> <routing expression>
  else -> <default routing expression>
}
```

As in other languages, the DataWeave `match` statement provides a compact way to
organize multiple, chained `if-else` statements. A `match` expression consists
of a list of `case` statements that optionally end with an `else` statement.
Each `case` statement consists of a conditional selector expression that must
evaluate to `true` or `false`. This conditional expression corresponds to the
condition expressed by an `if` statement, followed by a corresponding DataWeave
routing expression that can include the `match` statement's input expression.

Each `case` statement can be an `if` statement, or the `case` statement can use
other pattern-matching shortcuts to define the `case` statement's condition. If
a `case` statement is `false`, its routing expression is ignored.

DataWeave supports four different types of patterns for a `case` statement's
condition:

- Expressions
- Literal values
- Data types
- Regular expressions

Each case can be named or unnamed. If the case is named, the name stores the
input expression as a local variable that can be used both in that case
statement's conditional expression and in the corresponding routing expression.

**match Statement Structure**

```dataweave
value match {
  case (<name>:) <condition> -> <routing expression>
  case (<name>:) <condition> -> <routing expression>
  else -> <when none of them matched>
}
```

As this example shows, the expression returns the results of the first matching
`case` statement:

**match Statement Example**

```dataweave
%dw 2.0
output application/json
---
"hello world" match {
	case word matches /(hello)\s\w+/ ->  word[1] as String ++ " was matched"
	case literalMatch: "hello world" -> upper(literalMatch)
	case hasOne if( hasOne is Object and hasOne.three? ) -> hasOne.three
	else -> $
}
```

**Output**

```json
"hello was matched"
```

Notice that you can refer to the input expression ("hello world") through each
`case` statement's local variable name (that is, `word` or `literalMatch`),
while the `else` statement can refer to the input expression using the default
parameter name `$`, an unnamed parameter.

To name the input expression in the `else` statement, you can
replace the `else` statement with a `case` statement that is always `true`:

**match Statement Example**

```dataweave
%dw 2.0
output application/json
---
"hello world" match {
	case word matches  /(hello)\s\w+/ ->  word[1] ++ " was matched"
	case literalMatch: "hello world" -> upper(literalMatch)
	case last if(true) -> last
}
```

For use cases in which the input is of type String, you can also use the match _function_ in the `dw::Core` module to test the string against a regex pattern. The function returns an array with the strings that match the entire regex and any capture groups.

For use cases that require a Boolean result based on whether a string matches a regex pattern, you can use the matches _function_ in the `dw::Core` module instead of using pattern matching or the module's `match` function.

### Pattern Matching to Literal Values

Matches when the evaluated value equals a simple literal value.

In this example, the first field matches the value in `myInput.string` and
returns a boolean. The second field performs the same match, but it returns an
object that contains both a boolean and a reference to the validated value.

**DataWeave Script**

```dataweave
%dw 2.0
var myInput = {
  "string": "Emiliano"
}
output application/json
---
{
  a: myInput.string match {
    case "Emiliano" -> true
    case "Mariano" -> false
  },
  b: myInput.string match {
    case str: "Emiliano" -> { "matches": true, value: str }
    case str: "Mariano" -> { "matches": false, value: str }
  }
}
```

**Output**

```json
{
  "a": true,
  "b": {
    "matches": true,
    "value": "Emiliano"
  }
}
```

### Pattern Matching on Expressions

Matches when a given expression returns `true`.

In this example, the first field matches the value of `myInput.string` against
two alternatives and conditionally appends a different string to it. The second
field evaluates if the value in `myInput.number` is greater than (`>`),
less than (`<`), or equal to (`==`) 3 and returns the corresponding string.

**DataWeave Script**

```dataweave
%dw 2.0
var myInput = {
  "string": "Emiliano",
  "number": 3.14
}
output application/json
---
{
  a: myInput.string match {
    case str if str == "Mariano" -> str ++ " de Achaval"
    case str if str == "Emiliano" -> str ++ " Lesende"
  },
  b: myInput.number match {
    case num if num == 3 -> "equal"
    case num if num > 3 -> "greater than"
    case num if num < 3 -> "less than"
  }
}
```

**Output**

```json
{
  "a": "Emiliano Lesende",
  "b": "greater than"
}
```

### Pattern Matching on the Data Type

Matches when the evaluated value is the specified data type.

In this example, the first field evaluates the data type of `myInput.a` and returns
a string with the corresponding type name. The second field is similar but also
returns the value of the `myInput.b`.

**DataWeave Script**

```dataweave
%dw 2.0
var myInput =
{
  "a": "Emiliano",
  "b": 3.14
}
output application/json
---
{
  a: myInput.a match {
    case is Object -> 'OBJECT'
    case is String -> 'STRING'
    case is Number -> 'NUMBER'
    case is Boolean -> 'BOOLEAN'
    case is Array -> 'ARRAY'
    case is Null -> 'NULL'
    else -> 'ANOTHER TYPE'
  },
  b: myInput.b match {
    case y is Object -> { 'Type': { 'OBJECT' : y} }
    case y is String -> { 'Type': { 'STRING' : y} }
    case y is Number -> { 'Type': { 'NUMBER' : y} }
    case y is Boolean -> { 'Type': { 'BOOLEAN' : y} }
    case y is Array -> { 'Type': { 'ARRAY' : y} }
    case y is Null -> { 'Type': { 'NULL' : y} }
    else -> { 'Type': { 'ANOTHER TYPE' : myInput.b} }
  }
}
```

**Output**

```json
{
  "a": "STRING",
  "b": {
    "Type": {
      "NUMBER": 3.14
    }
  }
}
```

### Pattern Matching on Regular Expressions

Matches when the evaluated value fits a given regular expression (regex),
specifically a regex "flavor" supported by Java. In this example, the input
variable (`myInput`) includes an array of strings. The script uses the `map` function
to iterate through the array. It evaluates each element against a Java regex
and outputs an object based on matches to the input.

**DataWeave Script**

```dataweave
%dw 2.0
var myInput = {
  "phones": [
    "+1 (415) 229-2009",
    "(647) 456-7008"
  ]
}
output application/json
---
{
  a: myInput.phones map ($ match {
     case phone matches /\+(\d+)\s\((\d+)\)\s(\d+\-\d+)/ -> { country: phone[1]}
     case phone matches /\((\d+)\)\s(\d+\-\d+)/ -> { area: phone[1], number: phone[2] }
   }),
 b: myInput.phones map ($ match {
   case phone matches /\+(\d+)\s\((\d+)\)\s(\d+\-\d+)/ -> { country: phone[1], area: phone[2], number: phone[3] }
   case phone matches /\((\d+)\)\s(\d+\-\d+)/ -> { area: phone[1], number: phone[2] }
 })
}
```

**Output**

```json
{
  "a": [
    {
      "country": "1"
    },
    {
      "area": "647",
      "number": "456-7008"
    }
  ],
  "b": [
    {
      "country": "1",
      "area": "415",
      "number": "229-2009"
    },
    {
      "area": "647",
      "number": "456-7008"
    }
  ]
}
```

### Deconstructors on Collections in DataWeave

DataWeave supports two types of collections: Arrays and Objects. Arrays are a sequence of values, while Objects are a sequence of key-value pairs.

#### Deconstruction on Arrays

An Array can be seen as a head (the first element of the Array) and a tail (a new Array with the reminder of the elements). For example, in the array `[1,2,3,4]`, `1` is the head and `2,3,4` is the tail.

To match over an array, use the following syntax, where the script gets the first element of an array or returns null if the array is empty:

**DataWeave Script**

```dataweave
[1,2,3,4] match {
	case [head ~ tail] -> head
	case [] -> null
}
```

This kind of deconstruction is useful when used with recursive functions.

##### Example: Build a `joinBy` Function

This example builds a `joinBy` function that takes an array of string and returns a string with all the elements of the Array concatenated with the given separator:

**DataWeave Script**

```dataweave
fun joinBy(elements: Array<String>, separator: String): String = 
	elements match {
		case [head ~ tail] -> head ++ separator ++ joinBy(tail, separator) //When head and tail append and recursively
		case [] -> "" //When the array is empty return empty array
	}
```

##### Example: Build a Filter Function

This example builds a higher-order filter function:

**DataWeave Script**

```dataweave
fun filter<T>(elements: Array<T>, predicate: (item:T) -> Boolean): Array<T> = 
	elements match {
		case [head ~ tail] -> 
			if(predicate(head))
				[head] ++ filter(tail, predicate)
			else
				filter(tail, predicate)	
		case [] -> []
	}
```

#### Deconstruction on Objects

Objects in DataWeave are similar to Arrays but each element consists of a key and a value. An Object can also be seen as a head (the first key-value pair) and a tail (a new Object with the rest of the key-value pairs).

To match over an object, use the following syntax, where the script gets the first value of an object, which in this case is "Word":

**DataWeave Script**

```dataweave
{hello: "world", test: true} match {
    case {headKey: headValue ~ tail} -> headValue
    case {} -> null
}
```

### See Also

- DataWeave Types
- DataWeave Selectors
- DataWeave Quickstart

---

## Scope Visibility in DataWeave

DataWeave 2.12.0 introduces scope visibility so you can control which directives in a DataWeave file are accessible from other files. Visibility rules apply to module-level declarations: `fun`, `var`, `type`, `ns`, and `annotation`.

Scope visibility is primarily for DataWeave library authors. If you write Mule transformation mappings (the `%dw 2.0` script in a Transform Message component), you can ignore this feature because a mapping is a single, self-contained file that doesn't export directives to other files. Visibility becomes relevant when you publish a `.jar` that other DataWeave code imports.

### Visibility Levels

DataWeave 2.12.0 supports three visibility levels:

| Level | Keyword | Accessible From |
|---|---|---|
| Public | _(none)_ | Anywhere. Default and only behavior in versions before 2.12.0. |
| Private | `private` | The same file only. |
| Internal | `internal` | Any file in the same component. Can be widened with `@VisibleTo`. |

Visibility checks run only at compile time. Once a script is compiled, no runtime visibility check is performed. This keeps execution overhead at zero and ensures pre-compiled (`.bdwl`) modules behave the same as source modules.

### Syntax

Place the visibility keyword before the directive keyword (`fun`, `var`, `type`, `ns`, and `annotation`).

```dataweave
%dw 2.0

// Public (default) — accessible from anywhere
fun greet(name: String) = "Hello, $(name)!"

// Private — accessible only inside this file
private fun normalize(name: String) = upper(name)

// Internal — accessible from any file in the same component
internal var defaultGreeting = "Hello"

// Type and namespace declarations also support visibility
private type UserName = String
internal ns http https://schemas.example.org/http
```

The `@VisibleTo` annotation widens an `internal` directive to a fixed list of additional components:

```dataweave
%dw 2.0
import * from dw::Core

@VisibleTo(components = ["analytics", "reporting"])
internal fun computeStats(records: Array) = sizeOf(records)
```

`@VisibleTo` is only valid on `internal` directives. Applying it to a `private` directive or to a directive without a visibility keyword raises a compile-time error: `The @VisibleTo annotation can only be applied to 'internal' directives`.

### What Is a Component?

DataWeave doesn't provide a `module` or `package` keyword to group files. Until 2.12.0, every `.dwl` file lived in one global namespace. To make `internal` meaningful, the language now uses the component concept, which is a named set of DataWeave resources (modules) that are compiled and packaged together.

A component is described by a component descriptor, a `.dwl` resource located at `META-INF/dw-components.dwl` inside a `.jar` file. The descriptor is an array of components, and each component lists the resources it owns:

```dataweave
%dw 2.0
---
[
    {
        name: "wlang",
        resources: {
            "dw::Core": {},
            "dw::Crypto": {},
            "dw::core::Arrays": {},
            "dw::core::Strings": {}
            // ...
        }
    }
]
```

When the compiler resolves a reference to a symbol declared in another module, it consults the descriptors on the classpath to determine the components that own the declaring module and the caller module.

#### Generating the Descriptor

You don't write the descriptor manually. The Maven plugin for DataWeave generates it automatically:

- For a production build (`data-weave:package`), the plugin scans `src/main/dw`, derives the resource names of every `.dwl` file, and writes `target/generated-dataweave-metadata/dw-components.dwl`. The file is added to the produced JAR at `META-INF/dw-components.dwl`.
- For a test build (`data-weave:test`), the plugin scans both `src/main/dw` and `src/test/dw`, so test files belong to the same component as the production sources they exercise. This lets tests call `internal` directives without further configuration.

The component name defaults to the Maven `artifactId` of the project.

#### Component Resolution Algorithm

Given a reference from caller `A` to symbol `s` declared in module `B`, the compiler looks up `componentOf(B)` from the descriptors on the classpath. Access is allowed based on the visibility of `s`:

- If `s` is `private`, access is allowed only when `A == B`.
- If `s` is `internal`, access is allowed when `componentOf(A) == componentOf(B)`, or when `componentOf(A)` appears in the `@VisibleTo` list on `s`.
- If `s` is `public`, access is always allowed.

If a module declares `internal` directives and no descriptor on the classpath claims it, the compiler emits the `Module 'X' declares 'internal' members but has no component descriptor` error. In that case, package the module with the Maven plugin for DataWeave or add a component descriptor that lists it.

### Compile-Time Validation

The compiler reports four new errors:

| Error Kind | Triggered When |
|---|---|
| `PrivateAccessViolation` | A reference targets a `private` directive declared in a different file. |
| `InternalAccessViolation` | A reference targets an `internal` directive declared in a different component, when the caller's component isn't in the directive's `@VisibleTo` list. |
| `VisibleToRequiresInternal` | `@VisibleTo` is applied to a directive that isn't `internal`. |
| `MissingComponentForInternalDirective` | A module declares `internal` directives but no component descriptor on the classpath claims it. |

### Function Overloads and Visibility

Function overloads must use the same visibility. Mixing `internal fun foo(x: String) = ...` and `fun foo(x: Number) = ...` is rejected with an error that indicates the expected visibility (from the first overload). This guarantees that callers see a single, consistent visibility for any given function name.

### Structural Types and Visibility Propagation

DataWeave uses a structural type system. Visibility on a type controls who can reference the type by name and doesn't propagate to functions or variables that use that type in their signature. A caller can invoke a function whose signature mentions a `private` type as long as the caller doesn't name that type.

```dataweave
// In component A
private type Account = { id: String }

@VisibleTo(components = ["bat"])
internal fun createAccount(account: Account) = account

// In component B (bat)
import createAccount from componentA::Accounts

// OK — structural call, no explicit reference to `Account`
createAccount({ id: "abc" })

// Error — explicit reference to private type `Account`
createAccount({ id: "abc" }) as Account
```

The same rule applies to type annotations on variables (`var x: Account = ...`) and pattern matches that name a type.

### Examples

These examples demonstrate common visibility patterns for DataWeave library authors.

#### File-Local Helper

Use `private` to restrict a helper function to a single file.

```dataweave
// dw/core/Core.dwl

%dw 2.0

private fun isLegacyMode(): Boolean =
    evaluateCompatibilityFlag("com.mulesoft.dw.legacyMode")

fun sizeOf(value) =
    if (isLegacyMode()) legacyImpl(value) else newImpl(value)
```

`isLegacyMode` is reachable only inside `Core.dwl`.

#### Component-Internal Helper

Use `internal` to share helper functions across files within the same component while preventing external access.

```dataweave
// dw/core/Internal.dwl   (component: wlang)
%dw 2.0
internal fun dropFrame(): Boolean = ...

// dw/core/Core.dwl   (component: wlang)
%dw 2.0
import dropFrame from dw::core::Internal
fun process() = if (dropFrame()) ... else ...   // OK — same component

// com/acme/App.dwl   (component: acme-app)
%dw 2.0
import dropFrame from dw::core::Internal         // Error: internal to `wlang`
```

#### Sharing Internals With a Specific Component

Use `@VisibleTo` with `internal` to allow specific external components to access a directive.

```dataweave
// dw/native/Native.dwl   (component: wlang)
%dw 2.0

@VisibleTo(components = ["bat", "dataweave-io"])
internal fun nativeImpl() = ...

// bat/core/Runner.dwl   (component: bat)
import nativeImpl from dw::native::Native        // OK — bat is permitted

// com/paypal/Connector.dwl   (component: paypal-connector)
import nativeImpl from dw::native::Native        // Error — not permitted
```

### Migrating From `@Internal(permits=...)`

In versions before 2.12.0, the only way to constrain visibility was the experimental `@Internal(permits = [...])` annotation, which matched callers by `NameIdentifier` prefix. `@Internal` is still accepted in 2.12.0 but is deprecated in favor of the new keywords:

| Old Form | Replacement |
|---|---|
| `@Internal(permits = [])` | `private` |
| `@Internal(permits = ["dw::"])` | `internal` (the consuming component must also be migrated to a 2.12.0 build so a descriptor exists) |
| `@Internal(permits = ["bat::", "dw::"])` | `@VisibleTo(components = ["bat"])` `internal` |

Files that don't use any visibility keyword behave exactly as in earlier versions: every directive is public.

### Setting a Per-Component Language Level

When a host application embeds the DataWeave engine, it can pin a specific language level for each component using the new `componentLanguageLevels` parameter on `DWScriptingEngine.compileDWScript`:

```scala
def compileDWScript(
    script: String,
    languageLevel: String,
    componentLanguageLevels: util.Map[String, String] = new util.HashMap()
): DWScript
```

This is used together with `@Since` on function overloads to dispatch to the correct overload when a library evolves, ensuring backward compatibility for existing scripts.

### See Also

- `dw::meta::Component` Module
- `@VisibleTo` Annotation
- Maven plugin for DataWeave
- DataWeave extension plugin

---

## DataWeave Operators

DataWeave supports several operators, including mathematical operators, equality operators, and operators such as prepend, append, and update.

### Mathematical Operators

DataWeave supports the most common mathematical operators:

| Operator | Description |
|---|---|
| `+` | For addition. |
| `-` | For subtraction. |
| `*` | For multiplication. |
| `/` | For division. |

In addition to operating with numbers, the `(-)` and `(+)` operators can also operate with complex data structures like arrays, objects, and dates.

The following example uses mathematical operators with different data types:

**Source**

```dataweave
%dw 2.0
output application/json
---
{ "mathOperators" : [
    { "2 + 2" : (2 + 2) },
    { "2 - 2" : (2 - 2) },
    { "2 * 2" : (2 * 2) },
    { "2 / 2" : (2 / 2) },
    { "[1,2,3] - 1 + 4" : [1,2,3] - 1 + 4},
    { "{a:1, b:2, c:3} - 'a' " : {a:1, b:2, c:3} - "a"},
    { "|2021-03-02T10:39:59| - |P1D| + |PT3H|" : |2021-03-02T10:39:59| - |P1D| + |PT3H|}
  ]
}
```

**Output**

```json
{
  "mathOperators": [
    { "2 + 2": 4 },
    { "2 - 2": 0 },
    { "2 * 2": 4 },
    { "2 / 2": 1 },
    { "[1,2,3] - 1 + 4": [2,3,4] },
    { "{a:1, b:2, c:3} - 'a' ": {"b": 2, "c": 3} },
    { "|2021-03-02T10:39:59| - |P1D| + |PT3H|": "2021-03-01T13:39:59" }]
}
```

Several DataWeave functions operate on numbers, for example: sum, mod (for modulo), and avg (for average).

### Equality and Relational Operators

DataWeave supports the following equality and relational operators:

| Operator | Description |
|---|---|
| `<` | For less than. |
| `>` | For greater than. |
| `<=` | For less than or equal to. |
| `>=` | For greater than or equal to. |
| `==` | For equal to. |
| `~=` | Equality operator that tries to coerce one value to the type of the other when the types are different. |

Note that you can negate these operators by using the logical operator, `not`.

The following example uses relational operators:

**Source**

```dataweave
%dw 2.0
output application/json
---
{ "relational" : [
    { "1 < 1" : (1 < 1) },
    { "1 > 2" : (1 > 2) },
    { "1 <= 1" : (1 <= 1) },
    { "1 >= 1" : (1 >= 1) }
  ]
}
```

**Output**

```json
{ "relational": [
    { "(1 < 1)": false },
    { "(1 > 2)": false },
    { "(1 <= 1)": true },
    { "(1 >= 1)": true }
  ]
}
```

Note that if the operands of the relational operator belong to different types,
DataWeave coerces the right-side operand to the type of the left-side operand.
For example, in the expression `"123" > 12` DataWeave coerces `12` (a Number type)
to `"12"` (a String type) and compares each String value lexicographically.
In the expression `123 > "12"`, DataWeave coerces the String value `"12"` to the Number value `12`
and compares the numbers.

These examples use equality operators:

**Source**

```dataweave
%dw 2.0
output application/dw
---
{ "equality" :
  [
    (1 == 1),
    (1 == 2),
    ("true" == true),
    ("true" ~= true),
    (['true'] ~= [true]),
    ('1' ~= 1)
  ]
}
```

**Output**

```text
{
  equality: [ true, false, false, true, true, true ]
}
```

### Logical Operators

DataWeave supports the following logical operators:

| Operator | Description |
|---|---|
| `not` | Negates the result of the input. See also, `!`. |
| `!` | Negates the result of the input. See also, `not`. _Introduced in DataWeave 2.2.0. Supported by Mule 4.2 and later._ |
| `and` | Returns `true` if the result of all inputs is true, `false` if not. |
| `or` | Returns `true` if the result of any input is true, `false` if not. |

> **Note:** Though the semantics of `not` and `!` are the same, their precedence

differs. `not true or true` is executed as `not (true or true)`,
so it returns `false`, whereas `!true or true` returns `true` because
the `!` only applies to the first `true`. `!(true or true)` returns
`false`.

The following examples use logical operators:

**Source**

```dataweave
%dw 2.0
var myArray = [1,2,3,4,5]
var myMap = myArray map not (($ mod 2) == 0)
output application/json
---
{
  "not" : [
    "notTrue" : not true,
    "notFalse" : not false,
    "myMapWithNot" : myMap
  ],
  "and" : [
    "andTrueFalse" : true and false,
    "andIsTrue" : (1 + 1 == 2) and (2 + 2 == 4),
    "andIsFalse" : (1 + 1 == 2) and (2 + 2 == 2)
  ],
  "or" : [
    "orTrueFalse" : true or false,
    "orIsTrue" : (1 + 1 == 2) or (2 + 2 == 2),
    "orIsFalse" : (1 + 1 == 1) or (2 + 2 == 2)
  ],
  "!-vs-not" : [
	  "example-!" : (! true or true),
	  "example-not" : (not true or true)
  ]
}
```

Note that `myMap` iterates through the items in a list (`myArray`) and
determines whether the modulo (`mod`) expression _does not_ evaluate to `0` when
applied to each given item.

**Output**

```json
{
  "not": [
    { "notTrue": false },
    { "notFalse": true },
    { "myMapWithNot": [ true, false, true, false, true ] }
  ],
  "and": [
    { "andTrueFalse": false },
    { "andIsTrue": true },
    { "andIsFalse": false }
  ],
  "or": [
    { "orTrueFalse": true },
    { "orIsTrue": true },
    { "orIsFalse": false }
  ],
  "!-vs-not": [
    { "example-!": true },
    { "example-not": false }
  ]
}
```

Note that `not` works in expressions such as `not (true)`, but `not(true)`
(without the space) does not work.

You can use logical operators together. The following example uses:

- `or not` as defined in the `orNot` expression.
- `and not` in `andNot`.
- `not` and `and not` in `notWithAndNot`.

```dataweave
%dw 2.0
var orNot = if (1 + 1 == 4 or not 1 == 2) {"answer": "orNot - Condition met"}
             else {"answer": "nope"}
var andNot = if (1 + 1 == 2 and not 1 == 2) {"answer": "andNot - Condition met"}
             else {"answer": "nope"}
var notWithAndNot = if (not (1 + 1 == 2 and not 1 == 1)) {"answer": "notWithAndNot - Condition met"}
              else {"answer": "nope"}
output application/json
---
{ "answers" :
  [
    orNot,
    andNot,
    notWithAndNot
  ]
}
```

**Output**

```json
{
  "answers": [
    { "answer": "orNot - Condition met" },
    { "answer": "andNot - Condition met" },
    { "answer": "notWithAndNot - Condition met" }
  ]
}
```

DataWeave executes the code inside each `if` block because all conditional expressions in the example evaluate to `true`.

### Prepend, Append, and Remove Operators for Arrays

DataWeave supports operators for appending and prepending items within
an array:

| Operator | Description |
|---|---|
| `>>` | Prepends data on the left-hand side of the operator to items in the array on the right-hand side. For example, `1 >> [2]` results in `[ 1, 2 ]`, prepending `1` to `2` in the array. |
| `<<` | Appends data on the right-hand side of the operator to items in the array on the left-hand side. For example, `[1] << 2` results in `[ 1, 2 ]`, appending `2` to `1` in the array. |
| `+` | Appends data on the right-hand side of the operator to items in the array on the left-hand side. For example, `[1] + 2` results in `[ 1, 2 ]`, appending `2` to `1` in the array. The array is always on the left-hand side of the operator. |
| `-` | Removes a specified element of any supported type from an array. |

The following examples show uses of prepend, append, and remove operators on arrays:

```dataweave
%dw 2.0
output application/json
---
{
  "prepend-append" : [
  	 // Array on right side when prepending.
     { "prepend" : 1 >> [2] },
     { "prepend-number" : 1 >> [1] },
     { "prepend-string" : "a" >> [1] },
     { "prepend-object" : { "a" : "b"} >> [1] },
     { "prepend-array" : [1] >> [2, 3] },
     { "prepend-binary" : (1 as Binary) >> [1] },
     { "prepend-date-time" : |23:57:59Z| >> [ |2017-10-01| ] },
  	 // Array is on left side when appending.
     { "append-number" : [1] << 2 },
     { "append-string" : [1] << "a" },
     { "append-object" : [1] << { "a" : "b"} },
     { "append-array" : [1,2] << [1, 2, 3] },
     { "append-binary" : [1] << (1 as Binary) },
     { "append-date-time" : [ |2017-10-01| ] << |23:57:59Z| },
     { "append-object-to-array" : [1,2] << {"a" : "b"} },
     { "append-array-to-array1" : ["a","b"] << ["c","d"] },
     { "append-array-to-array2" : [["a","b"],["c","d"]] << ["e","f"] },
     // + always appends within the array
     { "append-with-+" : [1] + 2 },
     { "append-with-+" : [2] + 1 },
     { "removeNumberFromArray" : ( [1,2,3] - 2 ) },
     { "removeObjectFromArray" : ( [ {a : "b"}, {c : "d"} , { e : "f"} ] - { c : "d"} ) }
  ]
}
```

**Output**

```json
{
  "prepend-append": [
    { "prepend": [ 1, 2 ] },
    { "prepend-number": [ 1, 1 ] },
    { "prepend-string": [ "a", 1 ] },
    { "prepend-array": [ [ 1 ], 2, 3 ] },
    { "prepend-object": [ { "a": "b" }, 1 ] },
    { "prepend-binary": [ "\u0001", 1 ] },
    { "prepend-date-time": [ "23:57:59Z", "2017-10-01" ] },
    { "append-number": [ 1, 2 ] },
    { "append-string": [ 1, "a" ] },
    { "append-object": [ 1, { "a": "b" } ] },
    { "append-array": [ 1, 2, [ 1, 2, 3 ] ] },
    { "append-binary": [ 1, "\u0001" ] },
    { "append-date-time": [ "2017-10-01", "23:57:59Z" ] },
    { "append-object-to-array": [ 1, 2, { "a": "b" } ] },
    { "append-array-to-array1": [ "a", "b", ["c","d"] ] },
    { "append-array-to-array2": [ ["a","b"], ["c","d"], ["e","f"] ] },
    { "append-with-+": [ 1, 2] },
    { "append-with-+": [ 2, 1] },
    { "removeNumberFromArray": [ 1, 3 ] },
    { "removeObjectFromArray": [ { "a": "b" }, { "e": "f" } ] }
  ]
}
```

### Scope and Flow Control Operators

DataWeave supports operators that control the flow and scope of expressions:

- `do` and `using`
- `if else` and `else if`

**Scope Operators:**

| Operator | Description |
|---|---|
| `do` | Creates a scope in which new variables, functions, annotations, or namespaces can be declared and used. The syntax is similar to a mapping in that it is composed of a header and body separated by `---`. Its header is where all the declarations are defined, and its body is the result of the expression. See do and Examples: Local DataWeave Variables for examples. |
| `using` | Replaced by `do`. Supported for backwards compatibility only. |

**Flow Control Operators:**

| Operator | Description |
|---|---|
| `if else` | An `if` operator evaluates a conditional expression and returns the value under the `if` only if the conditional expression is true. Otherwise, it returns the expression under `else`. Every `if` expression must have a matching `else` expression. See if else for an example. |
| `else if` | An `else` operator chains expressions together within an if-else construct by incorporating `else if`. See else if for an example. |

### Update Operator

DataWeave supports the `update` operator, which enables you to update specified fields of a data structure with new values.

_Introduced in DataWeave 2.3.0. Supported by Mule 4.3 and later._

Versions prior to Mule 4.3 require the following syntax to increase the `age` value in `myInput` by one without recreating the entire object:

```text
%dw 2.0
var myInput = {
    "name": "Ken",
    "lastName":"Shokida",
    "age": 30
}
output application/json
---
myInput mapObject ((value,key) ->
    if(key as String == "age")
       {(key): value as Number + 1}
    else
       {(key): value} )
```

In Mule 4.3, the `update` operator simplifies the syntax:

```text
%dw 2.0
var myInput = {
    "name": "Ken",
    "lastName":"Shokida",
    "age": 30
}
output application/json
---
myInput update {
    case age at .age -> age + 1
}
```

Both DataWeave scripts return the same result:

```json
{
  "name": "Ken",
  "lastName": "Shokida",
  "age": 31
}
```

With `update`, casting or iterating through all the key-value pairs is not necessary.

The `update` syntax is as follows:

```text
<value_to_update> update {
    case <variable_name> at <update_expression>[!]? [if(<conditional_expression>)]? -> <new value>
    ...
}
```

- `value_to_update` represents the original value to update.
- `update_expression` is the selector expression that matches a value in `value_to_update`.
- `variable_name` is the name of the variable to bind to the matched `update_expression` value.
- `new_value` is the expression with the new value.
- `[if(<conditional_expression>)]?` If `conditional_expression` returns `true`, the script updates the value. Use of a conditional expression is optional.
- `[!]` marks the selector as an upsert. If the expression doesn't find a match, the `!` makes the `update` operator create all the required elements and insert the new value.
- `update_expression` supports multiple `case` expressions.

The `update` operator doesn't mutate the existing value. Instead, the operator creates a new value with the updated expressions.

#### Selector Expressions

Use selector expressions with the `update` operator to specify the fields to update.

##### Value Selector

This matching selector can check for matches to any value within an object.

The following example updates a field at the root level and a field in a nested level using the value selector:

**Source**

```text
%dw 2.0
var myInput = {
    "name": "Ken",
    "lastName":"Shokida",
    "age": 30,
    "address": {
        "street": "Amenabar",
        "zipCode": "AB1234"
    }
}
output application/json
---
myInput update {
    case age at .age -> age + 1
    case s at .address.street -> "First Street"
}
```

**Output**

```json
{
  "name": "Ken",
  "lastName": "Shokida",
  "age": 31,
  "address": {
    "street": "First Street",
    "zipCode": "AB1234"
  }
}
```

##### Index Selector

This matching selector enables you to match any array by its index.

The following example updates an element that is at the first location of the array:

**Input**

```json
{
    "name": "Ken",
    "lastName":"Shokida",
    "age": 30,
    "addresses": [{
        "street": "Amenabar",
        "zipCode": "AB1234"
    }]
}
```

**Source**

```text
%dw 2.0
output application/json
---
payload update {
    case s at .addresses[0] -> {
        "street": "Second Street",
        "zipCode": "ZZ123"
    }
}
```

**Output**

```json
{
  "name": "Ken",
  "lastName": "Shokida",
  "age": 30,
  "addresses": [
    {
      "street": "Second Street",
      "zipCode": "ZZ123"
    }
  ]
}
```

##### Attribute Selector

This matching selector enables you to match any attribute value.

The following example updates an attribute value and changes it to upper case:

**Input**

```xml
<user name="leandro"/>
```

**Source**

```text
%dw 2.0
output application/xml
---
payload update {
    case name at .user.@name -> upper(name)
}
```

**Output**

```xml
<?xml version='1.0' encoding='UTF-8'?>
<user name="LEANDRO"/>
```

##### Dynamic Selector

Any selector can incorporate an expression to make the selection dynamic.

The following example dynamically selects and updates the value of a field that is not hardcoded. Such a field can change at runtime. The example uses the variable `theFieldName` to obtain the field with key `name`, and it changes the value of that field to `Shoki`.

**Input**

```json
{
    "name": "Ken",
    "lastName":"Shokida"
}
```

**Source**

```text
%dw 2.0
var theFieldName = "name"
output application/json
---
payload update {
    case s at ."$(theFieldName)" -> "Shoki"
}
```

**Output**

```json
{
  "name": "Shoki",
  "lastName": "Shokida"
}
```

#### Conditional Update

The `update` operator has syntax for writing a conditional update if you want to modify a field under a given condition.

The following example updates the category based on the name of the user:

**Input**

```json
[{"name": "Ken", "age": 30}, {"name": "Tomo", "age": 70}, {"name": "Kajika", "age": 10}]
```

**Source**

```text
%dw 2.0
output application/json
---
payload map ((user) ->
    user update {
        case name at .name if(name == "Ken") -> name ++ " (Leandro)"
        case name at .name if(name == "Tomo") -> name ++ " (Christian)"
    }
)
```

**Output**

```json
[
  {
    "name": "Ken (Leandro)",
    "age": 30
  },
  {
    "name": "Tomo (Christian)",
    "age": 70
  },
  {
    "name": "Kajika",
    "age": 10
  }
]
```

#### Upserting

The `update` operator enables you to insert a field that is not present already by using the `!` symbol at the end of the selector expression. When the field is not present, the operator binds a `null` value to the variable.

The following example updates each object in the array `myInput`. If the field `name` is present in the object, the example applies the `upper` function to the value of `name`. If the field `name` is not present in the object, the example appends the key-value pair `"name": "JOHN"` to the object.

**Source**

```text
%dw 2.0
var myInput = [{"lastName": "Doe"}, {"lastName": "Parker", "name": "Peter" }]
output application/json
---
myInput  map ((value) ->
    value update {
        case name at .name! -> if(name == null) "JOHN" else upper(name)
    }
)
```

**Output**

```json
[
  {
    "lastName": "Doe",
    "name": "JOHN"
  },
  {
    "lastName": "Parker",
    "name": "PETER"
  }
]
```

#### Sugar Syntax

The `update` operator accepts a default variable named `$` in place of the longer  `<variable_name> at` syntax.

The following example binds the value of the expression `.age` to the default variable name `$`, which is used to express the new value. The longer equivalent is shown in comments.

**Input**

```json
{
    "name": "Ken",
    "lastName":"Shokida",
    "age": 30,
    "address": {
        "street": "Amenabar",
        "zipCode": "AB1234"
    }
}
```

**Source**

```text
%dw 2.0
output application/json
---
payload update {
    //equivalent expression:
    //case age at .age -> age + 1
    case .age -> $ + 1
    case .address.street -> "First Street"
}
```

**Output**

```json
{
  "name": "Ken",
  "lastName": "Shokida",
  "age": 31,
  "address": {
    "street": "First Street",
    "zipCode": "AB1234"
  }
}
```

### Metadata Assignment Operator

DataWeave supports the metadata assignment operator `<~`, which enables you to set the metadata of any value without using the `as` operator.
This operator is useful when you want to set the metadata and retain the current value type. If you are coercing the value to a new type, use as.

_Introduced in DataWeave 2.5.0. Supported by Mule 4.5 and later._

The operator syntax is as follows:

```
<valueB> <~ <objectA>
```

The operator assigns `objectA` as metadata to `valueB`. The arrow points to the value to which the metadata is assigned.

Versions prior to Mule 4.5 require the following syntax, for example, to add the `class` metadata field to an object:

```text
%dw 2.0
---
{name: "Ken"} as Object {class: "Person"}
```

In Mule 4.5, the metadata assignment operator `<~` simplifies the syntax:

```text
%dw 2.0
---
{name: "Ken"} <~ {class: "Person"}
```

#### Metadata Assignment Using Metadata Annotations

DataWeave adds support for metadata annotations. These special annotations, marked with `@Metadata`, attach a key-value pair metadata to any value where they are used.

_Introduced in DataWeave 2.8.0._

The following example achieves the same result as the previous one, but by defining an annotation, which is a class that binds the metadata key `class` to the value provided where it is used.

```text
%dw 2.8

@Metadata(key="class")
annotation Class(value: String)
---
@Class(value="Person")
{name: "Ken"}
```

Defining metadata using annotations provides the following benefits:

- You can define annotations once and reuse them as metadata throughout your code.
- Annotations are additive, and using more than one annotation attaches all the key-value pairs together.
- You get type checking, enabling you to force the value of the annotation to be of a certain type, ensuring consistency.

However, there are certain restrictions when defining metadata annotations:

- Annotations marked with `@Metadata` can only have one parameter.
- The parameter must be called `value`.
- The metadata key is the value set to the key argument of the metadata annotation, not the name of the annotation itself (In the previous example, the metadata value is associated to the `class` key).
- Metadata annotations are additive, so if they are used on a reference that already has metadata, the new metadata is appended.

The following is an example of a metadata annotation that marks a value as CData for the XML writter.

**Source**

```text
%dw 2.8
output application/xml

@Metadata(key="cdata")
annotation CData(value: true)
---
root: {
 test: @CData(value = true) "testCData"
}
```

**Output**

```xml
<?xml version='1.0' encoding='UTF-8'?>
<root>
  <test><![CDATA[testCData]]></test>
</root>
```

#### Metadata

Metadata is any additional information attached to a value that doesn't affect its identity. Given any two values
`A` and `B` that are equal, if you attach metadata to `A` and call it `A'`, then `A == A' == B`. So you can define a value that is formed by the value
and the metadata attached to it.
