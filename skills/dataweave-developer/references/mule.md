# dw::mule — Mule functions

Namespace `dw::Mule`.


Functions: `causedBy`, `lookup`, `p`

---

## causedBy

```
causedBy(@DesignOnlyType error: Error, errorType: String): Boolean
```

This function matches an error by its type, like an error handler does. `causedBy` is useful when you need to match by a super type, but the specific sub-type logic is also needed. It can also useful when handling a COMPOSITE_ROUTING error that contains child errors of different types.

- `error` — Optional. An `Error` type.
- `errorType` — A string that identifies the error, such as HTTP:UNAUTHORIZED.

```xml
<error-handler name="securityHandler">
  <on-error-continue type="SECURITY">
    <!-- general error handling for all SECURITY errors -->
    <choice>
      <when expression="#[Mule::causedBy(error, 'HTTP:UNAUTHORIZED')]">
        <!-- specific error handling only for HTTP:UNAUTHORIZED errors -->
      </when>
      <when expression="#[Mule::causedBy('HTTP:FORBIDDEN')]">
        <!-- specific error handling only for HTTP:FORBIDDEN errors -->
      </when>
    </choice>
  </on-error-continue>
</error-handler>
```

## lookup

```
lookup(flowName: String, payload: Any, timeoutMillis: Number = 2000)
```

This function enables you to execute a flow within a Mule app and retrieve the resulting payload. It works in Mule apps that are running on Mule Runtime version 4.1.4 and later. Similar to the Flow Reference component (recommended), the `lookup` function enables you to execute another flow within your app and to retrieve the resulting payload. It takes the flow's name and an input payload as parameters. For example, `lookup("anotherFlow", payload)` executes a flow named `anotherFlow`. The function executes the specified flow using the current attributes, variables, and any error, but it only passes in the payload without any attributes or variables. Similarly, the called flow will only return its payload. Note that the `lookup` function doesn't support calling subflows.

- `flowName` — A string that identifies the target flow.
- `payload` — The payload to send to the target flow, which can be any (`Any`) type.
- `timeoutMillis` — Optional. Timeout (in milliseconds) for the execution of the target flow. Defaults to `2000` milliseconds (2 seconds) if the thread that is executing is CPU_LIGHT or CPU_INTENSIVE, or 1 minute when executing from other threads. If the lookup takes more time than the specified `timeoutMillis` value, an error is raised.

```xml
<flow name="flow1">
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config"
    path="/source"/>
  <ee:transform doc:name="Transform Message" >
    <ee:message >
      <ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
Mule::lookup('flow2', {test:'hello '})]]></ee:set-payload>
    </ee:message>
  </ee:transform>
</flow>
<flow name="flow2" >
  <set-payload value='#[payload.test ++ "world"]' doc:name="Set Payload" />
  <logger level="INFO" doc:name="Logger" message='#[payload]'/>
</flow>
```

## p

```
p(propertyName: String): String
```

This function returns a string that identifies the value of one of these input properties: Mule property placeholders, System properties, or Environment variables. For more on this topic, see https://docs.mulesoft.com/mule-runtime/latest/configuring-properties[Configure Properties].

- `propertyName` — A string that identifies property.

```xml
<flow name="simple">
 <logger level="INFO" doc:name="Logger"
   message="#[Mule::p('http.port')]"/>
</flow>
```
