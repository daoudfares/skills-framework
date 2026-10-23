# dw::runtime — Runtime functions

Namespace `dw::Runtime`.
Requires an explicit import: `import * from dw::Runtime`.

Functions: `dataFormatsDescriptor`, `eval`, `evalUrl`, `fail`, `failIf`, `findDataFormatDescriptorByMime`, `location`, `locationString`, `orElse`, `orElseTry`, `prop`, `props`, `run`, `runUrl`, `try`, `version`, `wait`

---

## dataFormatsDescriptor

```
dataFormatsDescriptor(): Array<DataFormatDescriptor>
```

Returns an array of all `DataFormatDescriptor` values that are installed in the current instance of DataWeave. _Experimental:_ This function is an experimental feature that is subject to change or removal from future versions of DataWeave.

```dataweave
import * from dw::Runtime
---
dataFormatsDescriptor()
```

```json
[
      {
           "id": "json",
           "binary": false,
           "defaultEncoding": "UTF-8",
           "extensions": [
             ".json"
           ],
           "defaultMimeType": "application/json",
           "acceptedMimeTypes": [
             "application/json"
           ],
           "readerProperties": [
             {
               "name": "streaming",
               "optional": true,
               "defaultValue": false,
               "description": "Used for streaming input (use only if entries are accessed sequentially).",
               "possibleValues": [
                 true,
                 false
               ]
             }
           ],
           "writerProperties": [
             {
               "name": "writeAttributes",
               "optional": true,
               "defaultValue": false,
               "description": "Indicates that if a key has attributes, they are going to be added as children key-value pairs of the key that contains them. The attribute new key name will start with @.",
               "possibleValues": [
                 true,
                 false
               ]
             },
             {
              "name": "skipNullOn",
                 "optional": true,
                 "defaultValue": "None",
                 "description": "Indicates where is should skips null values if any or not. By default it doesn't skip.",
                 "possibleValues": [
                   "arrays",
                   "objects",
                   "everywhere"
                 ]
               }
             ]
           },
           {
             "id": "xml",
             "binary": false,
             "extensions": [
               ".xml"
             ],
             "defaultMimeType": "application/xml",
             "acceptedMimeTypes": [
               "application/xml"
             ],
             "readerProperties": [
               {
               "name": "supportDtd",
               "optional": true,
               "defaultValue": true,
               "description": "Whether DTD handling is enabled or disabled; disabling means both internal and external subsets will just be skipped unprocessed.",
               "possibleValues": [
                 true,
                 false
               ]
             },
             {
               "name": "streaming",
               "optional": true,
               "defaultValue": false,
               "description": "Used for streaming input (use only if entries are accessed sequentially).",
               "possibleValues": [
                 true,
                 false
               ]
             },
             {
               "name": "maxEntityCount",
               "optional": true,
               "defaultValue": 1,
               "description": "The maximum number of entity expansions. The limit is in place to avoid Billion Laughs attacks.",
               "possibleValues": [

               ]
             }
           ],
           "writerProperties": [
             {
               "name": "writeDeclaration",
               "optional": true,
               "defaultValue": true,
               "description": "Indicates whether to write the XML header declaration or not.",
               "possibleValues": [
                 true,
                 false
               ]
             },
             {
               "name": "indent",
               "optional": true,
               "defaultValue": true,
               "description": "Indicates whether to indent the code for better readability or to compress it into a single line.",
               "possibleValues": [
                 true,
                 false
               ]
             }
           ]
         }
]
```

## eval

```
eval(fileToExecute: String, fs: Dictionary<String>, readerInputs: Dictionary<ReaderInput> = {}, inputValues: Dictionary<Any> = {}, configuration: RuntimeExecutionConfiguration = {}): EvalResult
```

Evaluates a script with the specified context and returns the result of that evaluation. _Experimental:_ This function is an experimental feature that is subject to change or removal from future versions of DataWeave.

- `fileToExecute` — Name of the file to execute.
- `fs` — An object that contains the file to evaluate.
- `readerInputs` — Reader inputs to bind.
- `inputValues` — Additional literal values to bind
- `configuration` — The runtime configuration.

```dataweave
%dw 2.0
import * from dw::Runtime

var jsonValue = {
   value: '{"name": "Mariano"}' as Binary {encoding: "UTF-8"},
   encoding: "UTF-8",
   properties: {},
   mimeType: "application/json"
}

var jsonValue2 = {
   value: '{"name": "Mariano", "lastName": "achaval"}' as Binary {encoding: "UTF-8"},
   encoding: "UTF-8",
   properties: {},
   mimeType: "application/json"
}

var invalidJsonValue = {
   value: '{"name": "Mariano' as Binary {encoding: "UTF-8"},
   encoding: "UTF-8",
   properties: {},
   mimeType: "application/json"
}

var Utils = "fun sum(a,b) = a +b"
output application/json
---
{
   "execute_ok" : run("main.dwl", {"main.dwl": "{a: 1}"}, {"payload": jsonValue }),
   "logs" : do {
     var execResult = run("main.dwl", {"main.dwl": "{a: log(1)}"}, {"payload": jsonValue })
     ---
     {
         m: execResult.logs.message,
         l: execResult.logs.level
     }
   },
   "grant" : eval("main.dwl", {"main.dwl": "{a: readUrl(`http://google.com`)}"}, {"payload": jsonValue }, {},{ securityManager: (grant, args) -> false }),
   "library" : eval("main.dwl", {"main.dwl": "Utils::sum(1,2)", "/Utils.dwl": Utils }, {"payload": jsonValue }),
   "timeout" : eval("main.dwl", {"main.dwl": "(1 to 1000000000000) map \$ + 1" }, {"payload": jsonValue }, {},{timeOut: 2}).success,
   "execFail" : eval("main.dwl", {"main.dwl": "dw::Runtime::fail('My Bad')" }, {"payload": jsonValue }),
   "parseFail" : eval("main.dwl", {"main.dwl": "(1 + " }, {"payload": jsonValue }),
   "writerFail" : eval("main.dwl", {"main.dwl": "output application/xml --- 2" }, {"payload": jsonValue }),
   "defaultOutput" : eval("main.dwl", {"main.dwl": "payload" }, {"payload": jsonValue2}, {},{outputMimeType: "application/csv", writerProperties: {"separator": "|"}}),
   "onExceptionFail": do  {
     dw::Runtime::try( () ->
         eval("main.dwl", {"main.dwl": "dw::Runtime::fail('Failing Test')" }, {"payload": jsonValue2}, {},{onException: "FAIL"})
     ).success
   },
   "customLogger":
        eval(
  "main.dwl",
           {"main.dwl": "log(1234)" },
   {"payload": jsonValue2},
    {},
   {
                  loggerService: {
                     initialize: () -> {token: "123"},
                     log: (level, msg, context) -> log("$(level) $(msg)", context)
                  }
                }
           )
}
```

```json
{
  "execute_ok": {
    "success": true,
    "value": "{\n  a: 1\n}",
    "mimeType": "application/dw",
    "encoding": "UTF-8",
    "logs": [

    ]
  },
  "logs": {
    "m": [
      "1"
    ],
    "l": [
      "INFO"
    ]
  },
  "grant": {
    "success": false,
    "message": "The given required permissions: `Resource` are not being granted for this execution.\nTrace:\n  at readUrl (Unknown)\n  at main::main (line: 1, column: 5)",
    "location": {
      "start": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "end": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "content": "Unknown location"
    },
    "stack": [
      "readUrl (anonymous:0:0)",
      "main (main:1:5)"
    ],
    "logs": [

    ]
  },
  "library": {
    "success": true,
    "value": 3,
    "logs": [

    ]
  },
  "timeout": true,
  "execFail": {
    "success": false,
    "message": "My Bad\nTrace:\n  at fail (Unknown)\n  at main::main (line: 1, column: 1)",
    "location": {
      "start": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "end": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "content": "Unknown location"
    },
    "stack": [
      "fail (anonymous:0:0)",
      "main (main:1:1)"
    ],
    "logs": [

    ]
  },
  "parseFail": {
    "success": false,
    "message": "Invalid input \"1 + \", expected parameter or parenEnd (line 1, column 2):\n\n\n1| (1 + \n    ^^^^\nLocation:\nmain (line: 1, column:2)",
    "location": {
      "start": {
        "index": 0,
        "line": 1,
        "column": 2
      },
      "end": {
        "index": 4,
        "line": 1,
        "column": 6
      },
      "content": "\n1| (1 + \n    ^^^^"
    },
    "logs": [

    ]
  },
  "writerFail": {
    "success": true,
    "value": 2,
    "logs": [

    ]
  },
  "defaultOutput": {
    "success": true,
    "value": {
      "name": "Mariano",
      "lastName": "achaval"
    },
    "logs": [

    ]
  },
  "onExceptionFail": false,
  "customLogger": {
    "success": true,
    "value": 1234,
    "logs": [

    ]
  }
}
```

## evalUrl

```
evalUrl(url: String, readerInputs: Dictionary<ReaderInput> = {}, inputValues: Dictionary<Any> = {}, configuration: RuntimeExecutionConfiguration = {}): EvalResult
```

Evaluates the script at the specified URL. _Experimental:_ This function is an experimental feature that is subject to change or removal from future versions of DataWeave.

- `url` — Name of the file execute.
- `readerInputs` — Inputs to read and bind to the execution.
- `inputValues` — Inputs to bind directly to the execution.
- `configuration` — The runtime configuration.

```dataweave
%dw 2.0
import * from dw::Runtime
var jsonValue = {
  value: '{"name": "Mariano"}' as Binary {encoding: "UTF-8"},
  encoding: "UTF-8",
  properties: {},
  mimeType: "application/json"
}

var Utils = "fun sum(a,b) = a +b"
output application/json
---
{
  "execute_ok" : evalUrl("classpath://org/mule/weave/v2/engine/runtime_evalUrl/example.dwl", {"payload": jsonValue }),
  "execute_ok_withValue" : evalUrl("classpath://org/mule/weave/v2/engine/runtime_evalUrl/example.dwl", {}, {"payload": {name: "Mariano"}})
}
```

```json
{
   "execute_ok": {
     "success": true,
     "value": "Mariano",
     "logs": [

     ]
   },
   "execute_ok_withValue": {
     "success": true,
     "value": "Mariano",
     "logs": [

     ]
   }
 }
```

## fail

```
fail(message: String = 'Error'): Nothing
```

Throws an exception with the specified message.

- `message` — An error message (`String`).

```dataweave
%dw 2.0
import * from dw::Runtime
var result = []
output application/json
---
if(sizeOf(result) <= 0) fail('Data was empty') else result
```

```text
ERROR 2018-07-29 11:47:44,983 ...
*********************************
Message               : "Data was empty
...
```

## failIf

```
failIf<T>(value: T, evaluator: (value: T) -> Boolean, message: String = 'Failed'): T
```

Produces an error with the specified message if the expression in the evaluator returns `true`. Otherwise, the function returns the value.

- `value` — The value to return only if the `evaluator` expression is `false`.
- `evaluator` — Expression that returns `true` or `false`.

```dataweave
%dw 2.0
import failIf from dw::Runtime
var result = {"a":"test"}
output application/json
---
{ "result" : result failIf isEmpty($) }
```

```json
{
  "result": {
    "a": "test"
  }
}
```

## findDataFormatDescriptorByMime

```
findDataFormatDescriptorByMime(mime: dw::module::Mime::MimeType): DataFormatDescriptor | Null
```

Returns the `DataFormatDescriptor` based on the `dw::module::Mime::MimeType` specified or `null` if there is no `DataFormatDescriptor` for the given `MimeType`. _Experimental:_ This function is an experimental feature that is subject to change or removal from future versions of DataWeave. _Introduced in DataWeave version 2.7.0._

- `Description` — `mimeType`
- `dw::module::Mime::MimeType` — The MIME type value to search.

```dataweave
%dw 2.0
import * from dw::Runtime
output application/json

var jsonDF = findDataFormatDescriptorByMime({'type': "*", subtype: "json", parameters: {}})
var unknownDF = findDataFormatDescriptorByMime({'type': "*", subtype: "*", parameters: {}})

fun simplify(df: DataFormatDescriptor | Null) = df  match {
  case d is DataFormatDescriptor -> { name: d.name, defaultMimeType: d.defaultMimeType }
  case is Null -> { name: "unknown", defaultMimeType: "unknown" }
}
---
{
  json: simplify(jsonDF),
  unknown: simplify(unknownDF)
}
```

```json
{
  "json": {
    "name": "json",
    "defaultMimeType": "application/json"
  },
  "unknown": {
    "name": "unknown",
    "defaultMimeType": "unknown"
  }
}
```

## location

```
location(value: Any): Location
```

Returns the location of a given value, or `null` if the location can't be traced back to a DataWeave file. _Introduced in DataWeave version 2.4.0._

- `value` — A value of any type.

```dataweave
%dw 2.0
import location from dw::Runtime
output application/json
---
location(sqrt)
```

```json
{
  "uri": "/dw/Core.dwl",
  "nameIdentifier": "dw::Core",
  "startLine": 5797,
  "startColumn": 36,
  "endLine": 5797,
  "endColumn": 77
}
```

## locationString

```
locationString(value: Any): String
```

Returns the location string of a given value.

- `value` — A value of any type.

```dataweave
%dw 2.0
import * from dw::Runtime
var a = 123
output application/json
---
locationString(a)
```

```json
"var a = 123"
```

## orElse

```
orElse<T, E, R>(previous: Result<T, E>, orElse: () -> R): T | R
```

Returns the result of the `orElse` argument if the `previous` argument to `try` fails. Otherwise, the function returns the value of the `previous` argument. _Introduced in DataWeave version 2.2.0._

- `previous` — Result from a previous call to `try`.
- `orElse` — Argument to return if the `previous` argument fails.

```dataweave
%dw 2.0
import * from dw::Runtime
var user = {}
var otherUser = {name: "DW"}
output application/json
---
{
    a: try(() -> user.name!) orElse "No User Name",
    b: try(() -> otherUser.name) orElse "No User Name"
}
```

```json
{
  "a": "No User Name",
  "b": "DW"
}
```

## orElseTry

```
orElseTry<T, R>(previous: TryResult<T>, orElse: () -> R): TryResult<T | R>
```

Function to use with `try` to chain multiple `try` requests. _Introduced in DataWeave version 2.2.0._

- `previous` — Result from a previous call to `try`.
- `orElseTry` — Argument to try if the `previous` argument fails.

```dataweave
%dw 2.0
import * from dw::Runtime
var user = {}
var otherUser = {}
output application/json
---
{
    a: try(() -> user.name!) orElseTry otherUser.name!,
    b: try(() -> user.name!) orElseTry "No User Name"
}
```

```json
{
  "a": {
    "success": false,
    "error": {
      "kind": "KeyNotFoundException",
      "message": "There is no key named 'name'",
      "location": "\n9|     a: try(() -> user.name!) orElseTry otherUser.name!,\n                                          ^^^^^^^^^^^^^^",
      "stack": [
        "main (org::mule::weave::v2::engine::transform:9:40)"
      ]
    }
  },
  "b": {
    "success": true,
    "result": "No User Name"
  }
}
```

## prop

```
prop(propertyName: String): String | Null
```

Returns the value of the property with the specified name or `null` if the property is not defined.

- `propertyName` — The property to retrieve.

```dataweave
%dw 2.0
import * from dw::Runtime
output application/dw
---
{ "props" : prop("user.timezone") }
```

```json
{ props: "America/Los_Angeles" as String {class: "java.lang.String"} }
```

## props

```
props(): Dictionary<String>
```

Returns all the properties configured for the DataWeave runtime, which executes the language.

```dataweave
%dw 2.0
import * from dw::Runtime
output application/dw
---
{ "props" : props() }
```

```json
{
 props: {
   "java.vendor": "Oracle Corporation" as String {class: "java.lang.String"},
   "sun.java.launcher": "SUN_STANDARD" as String {class: "java.lang.String"},
   "sun.management.compiler": "HotSpot 64-Bit Tiered Compilers" as String ..., *    "os.name": "Mac OS X" as String {class: "java.lang.String"},
   "sun.boot.class.path": "/Library/Java/JavaVirtualMachines/ ...,
   "org.glassfish.grizzly.nio.transport.TCPNIOTransport...": "1048576" ...,
   "java.vm.specification.vendor": "Oracle Corporation" as String ...,
   "java.runtime.version": "1.8.0_111-b14" as String {class: "java.lang.String"},
   "wrapper.native_library": "wrapper" as String {class: "java.lang.String"},
   "wrapper.key": "XlIl4YartmfEU3oKu7o81kNQbwhveXi-" as String ...,
   "user.name": "me" as String {class: "java.lang.String"},
   "mvel2.disable.jit": "TRUE" as String {class: "java.lang.String"},
   "user.language": "en" as String {class: "java.lang.String"} ...,
   "sun.boot.library.path": "/Library/Java/JavaVirtualMachines ...
   "xpath.provider": "com.mulesoft.licm.DefaultXPathProvider" ...,
   "wrapper.backend": "pipe" as String {class: "java.lang.String"},
   "java.version": "1.8.0_111" as String {class: "java.lang.String"},
   "user.timezone": "America/Los_Angeles" as String {class: "java.lang.String"},
   "java.net.preferIPv4Stack": "TRUE" as String {class: "java.lang.String"},
   "sun.arch.data.model": "64" as String {class: "java.lang.String"},
   "java.endorsed.dirs": "/Library/Java/JavaVirtualMachines/...,
   "sun.cpu.isalist": "" as String {class: "java.lang.String"},
   "sun.jnu.encoding": "UTF-8" as String {class: "java.lang.String"},
   "mule.testingMode": "" as String {class: "java.lang.String"},
   "file.encoding.pkg": "sun.io" as String {class: "java.lang.String"},
   "file.separator": "/" as String {class: "java.lang.String"},
   "java.specification.name": "Java Platform API Specification" ...,
   "java.class.version": "52.0" as String {class: "java.lang.String"},
   "jetty.git.hash": "82b8fb23f757335bb3329d540ce37a2a2615f0a8" ...,
   "user.country": "US" as String {class: "java.lang.String"},
   "mule.agent.configuration.folder": "/Applications/AnypointStudio.app/ ...,
   "log4j.configurationFactory": "org.apache.logging.log4j.core...",
   "java.home": "/Library/Java/JavaVirtualMachines/...,
   "java.vm.info": "mixed mode" as String {class: "java.lang.String"},
   "wrapper.version": "3.5.34-st" as String {class: "java.lang.String"},
   "os.version": "10.13.4" as String {class: "java.lang.String"},
   "org.eclipse.jetty.LEVEL": "WARN" as String {class: "java.lang.String"},
   "path.separator": ":" as String {class: "java.lang.String"},
   "java.vm.version": "25.111-b14" as String {class: "java.lang.String"},
   "wrapper.pid": "5212" as String {class: "java.lang.String"},
   "java.util.prefs.PreferencesFactory": "com.mulesoft.licm..."},
   "wrapper.java.pid": "5213" as String {class: "java.lang.String"},
   "mule.home": "/Applications/AnypointStudio.app/...,
   "java.awt.printerjob": "sun.lwawt.macosx.CPrinterJob" ...,
   "sun.io.unicode.encoding": "UnicodeBig" as String {class: "java.lang.String"},
   "awt.toolkit": "sun.lwawt.macosx.LWCToolkit" ...,
   "org.glassfish.grizzly.nio.transport...": "1048576" ...,
   "user.home": "/Users/me" as String {class: "java.lang.String"},
   "java.specification.vendor": "Oracle Corporation" ...,
   "java.library.path": "/Applications/AnypointStudio.app/...,
   "java.vendor.url": "http://java.oracle.com/" as String ...,
   "java.vm.vendor": "Oracle Corporation" as String {class: "java.lang.String"},
   gopherProxySet: "false" as String {class: "java.lang.String"},
   "wrapper.jvmid": "1" as String {class: "java.lang.String"},
   "java.runtime.name": "Java(TM) SE Runtime Environment" ...,
   "mule.encoding": "UTF-8" as String {class: "java.lang.String"},
   "sun.java.command": "org.mule.runtime.module.reboot....",
   "java.class.path": "%MULE_LIB%:/Applications/AnypointStudio.app...",
   "log4j2.loggerContextFactory": "org.mule.runtime.module.launcher...,
   "java.vm.specification.name": "Java Virtual Machine Specification" ,
   "java.vm.specification.version": "1.8" as String {class: "java.lang.String"},
   "sun.cpu.endian": "little" as String {class: "java.lang.String"},
   "sun.os.patch.level": "unknown" as String {class: "java.lang.String"},
   "com.ning.http.client.AsyncHttpClientConfig.useProxyProperties": "true" ...,
   "wrapper.cpu.timeout": "10" as String {class: "java.lang.String"},
   "java.io.tmpdir": "/var/folders/42/dd73l3rx7qz0n625hr29kty80000gn/T/" ...,
   "anypoint.platform.analytics_base_uri": ...,
   "java.vendor.url.bug": "http://bugreport.sun.com/bugreport/" ...,
   "os.arch": "x86_64" as String {class: "java.lang.String"},
   "java.awt.graphicsenv": "sun.awt.CGraphicsEnvironment" ...,
   "mule.base": "/Applications/AnypointStudio.app...",
   "java.ext.dirs": "/Users/staceyduke/Library/Java/Extensions: ..."},
   "user.dir": "/Applications/AnypointStudio.app/..."},
   "line.separator": "\n" as String {class: "java.lang.String"},
   "java.vm.name": "Java HotSpot(TM) 64-Bit Server VM" ...,
   "org.quartz.scheduler.skipUpdateCheck": "true" ...,
   "file.encoding": "UTF-8" as String {class: "java.lang.String"},
   "mule.forceConsoleLog": "" as String {class: "java.lang.String"},
   "java.specification.version": "1.8" as String {class: "java.lang.String"},
   "wrapper.arch": "universal" as String {class: "java.lang.String"}
 } as Object {class: "java.util.Properties"}
```

## run

```
run(fileToExecute: String, fs: Dictionary<String>, readerInputs: Dictionary<ReaderInput> = {}, inputValues: Dictionary<Any> = {}, configuration: RuntimeExecutionConfiguration = {}): RunResult
```

Runs the input script under the provided context and executes the script in the current runtime. _Experimental:_ This function is an experimental feature that is subject to change or removal from future versions of DataWeave.

- `fileToExecute` — Name of the file to execute.
- `fs` — File system that contains the file to execute.
- `readerInput` — Inputs to read and bind to the execution.
- `inputValues` — Inputs to bind directly to the execution.
- `configuration` — The runtime configuration.

```dataweave
import * from dw::Runtime
var jsonValue = {
  value: '{"name": "Mariano"}' as Binary {encoding: "UTF-8"},
  encoding: "UTF-8",
  properties: {},
  mimeType: "application/json"
}

var jsonValue2 = {
  value: '{"name": "Mariano", "lastName": "achaval"}' as Binary {encoding: "UTF-8"},
  encoding: "UTF-8",
  properties: {},
  mimeType: "application/json"
}

var invalidJsonValue = {
  value: '{"name": "Mariano' as Binary {encoding: "UTF-8"},
  encoding: "UTF-8",
  properties: {},
  mimeType: "application/json"
}

var Utils = "fun sum(a,b) = a +b"
---
{
  "execute_ok" : run("main.dwl", {"main.dwl": "{a: 1}"}, {"payload": jsonValue }),
  "logs" : do {
    var execResult = run("main.dwl", {"main.dwl": "{a: log(1)}"}, {"payload": jsonValue })
    ---
    {
        m: execResult.logs.message,
        l: execResult.logs.level
    }
  },
  "grant" : run("main.dwl", {"main.dwl": "{a: readUrl(`http://google.com`)}"}, {"payload": jsonValue }, { securityManager: (grant, args) -> false }),
  "library" : run("main.dwl", {"main.dwl": "Utils::sum(1,2)", "/Utils.dwl": Utils }, {"payload": jsonValue }),
  "timeout" : run("main.dwl", {"main.dwl": "(1 to 1000000000000) map \$ + 1" }, {"payload": jsonValue }, {timeOut: 2}).success,
  "execFail" : run("main.dwl", {"main.dwl": "dw::Runtime::fail('My Bad')" }, {"payload": jsonValue }),
  "parseFail" : run("main.dwl", {"main.dwl": "(1 + " }, {"payload": jsonValue }),
  "writerFail" : run("main.dwl", {"main.dwl": "output application/xml --- 2" }, {"payload": jsonValue }),
  "readerFail" : run("main.dwl", {"main.dwl": "output application/xml --- payload" }, {"payload": invalidJsonValue }),
  "defaultOutput" : run("main.dwl", {"main.dwl": "payload" }, {"payload": jsonValue2}, {outputMimeType: "application/csv", writerProperties: {"separator": "|"}}),
}
```

```json
{
  "execute_ok": {
    "success": true,
    "value": "{\n  a: 1\n}",
    "mimeType": "application/dw",
    "encoding": "UTF-8",
    "logs": [

    ]
  },
  "logs": {
    "m": [
      "1"
    ],
    "l": [
      "INFO"
    ]
  },
  "grant": {
    "success": false,
    "message": "The given required permissions: `Resource` are not being granted for this execution.\nTrace:\n  at readUrl (Unknown)\n  at main::main (line: 1, column: 5)",
    "location": {
      "start": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "end": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "content": "Unknown location"
    },
    "stack": [
      "readUrl (anonymous:0:0)",
      "main (main:1:5)"
    ],
    "logs": [

    ]
  },
  "library": {
    "success": true,
    "value": "3",
    "mimeType": "application/dw",
    "encoding": "UTF-8",
    "logs": [

    ]
  },
  "timeout": false,
  "execFail": {
    "success": false,
    "message": "My Bad\nTrace:\n  at fail (Unknown)\n  at main::main (line: 1, column: 1)",
    "location": {
      "start": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "end": {
        "index": 0,
        "line": 0,
        "column": 0
      },
      "content": "Unknown location"
    },
    "stack": [
      "fail (anonymous:0:0)",
      "main (main:1:1)"
    ],
    "logs": [

    ]
  },
  "parseFail": {
    "success": false,
    "message": "Invalid input \"1 + \", expected parameter or parenEnd (line 1, column 2):\n\n\n1| (1 + \n    ^^^^\nLocation:\nmain (line: 1, column:2)",
    "location": {
      "start": {
        "index": 0,
        "line": 1,
        "column": 2
      },
      "end": {
        "index": 4,
        "line": 1,
        "column": 6
      },
      "content": "\n1| (1 + \n    ^^^^"
    },
    "logs": [

    ]
  },
  "writerFail": {
    "success": false,
    "message": "Trying to output non-whitespace characters outside main element tree (in prolog or epilog), while writing Xml at .",
    "location": {
      "content": ""
    },
    "stack": [

    ],
    "logs": [

    ]
  },
  "readerFail": {
    "success": false,
    "message": "Unexpected end-of-input at payload@[1:18] (line:column), expected '\"', while reading `payload` as Json.\n \n1| {\"name\": \"Mariano\n                    ^",
    "location": {
      "content": "\n1| {\"name\": \"Mariano\n                    ^"
    },
    "stack": [

    ],
    "logs": [

    ]
  },
  "defaultOutput": {
    "success": true,
    "value": "name|lastName\nMariano|achaval\n",
    "mimeType": "application/csv",
    "encoding": "UTF-8",
    "logs": [

    ]
  }
}
```

## runUrl

```
runUrl(url: String, readerInputs: Dictionary<ReaderInput> = {}, inputValues: Dictionary<Any> = {}, configuration: RuntimeExecutionConfiguration = {}): RunResult
```

Runs the script at the specified URL. _Experimental:_ This function is an experimental feature that is subject to change or removal from future versions of DataWeave.

- `url` — The name of the file to execute.
- `readerInputs` — Inputs to read and bind to the execution.
- `inputValues` — Inputs to be bind directly to the execution.
- `configuration` — The runtime configuration.

```dataweave
import * from dw::Runtime
var jsonValue = {
  value: '{"name": "Mariano"}' as Binary {encoding: "UTF-8"},
  encoding: "UTF-8",
  properties: {},
  mimeType: "application/json"
}

var Utils = "fun sum(a,b) = a +b"
---
{
  "execute_ok" : runUrl("classpath://org/mule/weave/v2/engine/runtime_runUrl/example.dwl", {"payload": jsonValue })
}
```

```json
{
   "execute_ok": {
     "success": true,
     "value": "\"Mariano\"",
     "mimeType": "application/dw",
     "encoding": "UTF-8",
     "logs": [

     ]
   }
 }
```

## try

```
try<T>(delegate: () -> T): TryResult<T>
```

Evaluates the delegate function and returns an object with `success: true` and `result` if the delegate function succeeds, or an object with `success: false` and `error` if the delegate function throws an exception. The `orElseTry` and `orElse` functions will also continue processing if the `try` function fails. See the `orElseTry` and `orElse` documentation for more complete examples of handling failing `try` function expressions. Note: Instead of using the `orElseTry` and `orElse` functions, based on the output of the `try` function, you can add conditional logic to execute when the result is `success: true` or `success: false`.

- `delegate` — The function to evaluate.

```dataweave
%dw 2.0
import try, fail from dw::Runtime
output application/json
fun randomNumber() =
if(random() > 0.5)
  fail("This function is failing")
 else
  "OK"
---
try(() -> randomNumber())
```

```json
{
  "success": false,
  "error": {
    "kind": "UserException",
    "message": "This function is failing",
    "location": "Unknown location",
    "stack": [
      "fail (anonymous:0:0)",
      "myFunction (anonymous:1:114)",
      "main (anonymous:1:179)"
    ]
  }
}
```

## version

```
version(): String
```

Returns the DataWeave version that is currently running. _Introduced in DataWeave version 2.5.0._

```dataweave
%dw 2.0
import * from dw::Runtime
output application/json
---
version()
```

```json
"2.5"
```

## wait

```
wait<T>(value: T, timeout: Number): T
```

Stops the execution for the specified timeout period (in milliseconds). WARNING: Stopping the execution blocks the thread, potentially causing slowness, low performance and potentially freezing of the entire runtime. This operation is intended for limited functional testing purposes. Do not use this function in a production application, performance testing, or with multiple applications deployed.

- `value` — Input of any type.
- `timeout` — The number of milliseconds to wait.

```dataweave
%dw 2.0
import * from dw::Runtime
output application/json
---
{ "user" : 1 } wait 2000
```

```json
{ "user": 1 }
```
