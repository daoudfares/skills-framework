# dw::system — System functions

Namespace `dw::System`.
Requires an explicit import: `import * from dw::System`.

Functions: `envVar`, `envVars`

---

## envVar

```
envVar(variableName: String): String | Null
```

Returns an environment variable with the specified name or `null` if the environment variable is not defined.

- `variableName` — String that provides the name of the environment variable.

```dataweave
%dw 2.0
import * from dw::System
output application/json
---
{
    "envVars" : [
       "real" : envVar("SHELL"),
       "fake" : envVar("FAKE_ENV_VAR")
    ]
}
```

```json
"envVars": [
  {
    "real": "/bin/bash"
  },
  {
    "fake": null
  }
]
```

## envVars

```
envVars(): Dictionary<String>
```

Returns all the environment variables defined in the host system as an array of strings.

```dataweave
%dw 2.0
import dw::System
output application/json
---
{ "envVars" : dw::System::envVars().SHELL }
```

```json
{ "envVars": "/bin/bash" }
```
