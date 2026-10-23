# Errors and error handling

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Mule Errors

Mule execution failures result in an error. When a Mule app is running, both
the Mule runtime engine and the module and connector operations configured in the app can throw errors that are represented by a Mule error object, which
is associated with a Mule event. You can handle error objects with On-Error components and find information about them in the logs.

Mule errors are grouped into error types that follow a hierarchical
order and use a naming convention that helps you identify the source of the error
and handle the error at the level you choose. You can also create custom error
types that you map to these errors. The mappings can help you further
differentiate and group errors that you need to handle in your app.

To inspect and use values of Mule errors in your error handling configurations,
you can also use selector expressions.

Mule errors include expression (`EXPRESSION`) and stream-related errors
(`STREAM_MAXIMUM_SIZE_EXCEEDED`), while the operations can throw many different
types of errors. Examples include `HTTP:NOT_FOUND` (a 404 error) and
`HTTP:CONNECTIVITY` errors from the HTTP listener in the HTTP connector.
`DB:BAD_SYNTAX` and `DB:QUERY_EXPRESSION` are errors that the Select operation in
the Database connector can throw.

The reference documentation for modules and connectors (for example,
the HTTP Connector and
Database Connector
references) lists Mule errors.

### Selector Expressions for Mule Errors

Mule errors are complex data types with several fields, such as a description
and type. When logging and handling Mule errors, can select the values from any
number of the error fields.

| Field | Description | Selector Expression |
|---|---|---|
| Description |  |  |
| A description of the problem. |  |  |
| `#[error.description]` |  |  |
| Detailed Description |  |  |
| A description of the problem, which can be the same or more extensive than the description. |  |  |
| `#[error.detailedDescription]` |  |  |
| Type |  |  |
| A type, used to characterize the problem and allow for routing within an error handler. |  |  |
| `#[error.errorType]` |  |  |
| Cause |  |  |
| The underlying Java `Throwable` that resulted in the failure. |  |  |
| `#[error.cause]` |  |  |
| Message |  |  |
| An optional Mule message about the problem. |  |  |
| `#[error.errorMessage]` |  |  |
| Child Errors |  |  |
| An optional collection of inner errors, used by elements like Scatter-Gather to provide aggregated route errors. |  |  |
| `#[error.childErrors]` |  |  |

In most cases, the `error.cause` selector returns a `Throwable` instance that is part of the Mule API. Do not access the error's internal structure to define error handling logic. The other selectors expose all the necessary information to handle errors. Also, serializing the `error.cause` might result in redundant information.

#### HTTP Request Error Example

For example, when an HTTP request fails with an `HTTP:NOT_FOUND` error (for a 404
status code), the values for each part of the Error Message are:

- `#[error.description]` returns:
```text
HTTP GET on resource 'http://jsonplaceholder.typicode.com:80/mybadrequest' failed: not found (404).
```

- `#[error.detailedDescription]` returns `HTTP GET on resource 'http://jsonplaceholder.typicode.com:80/mybadrequest' failed: not found (404).`
- `#[error.errorType]` returns `HTTP:NOT_FOUND`
- `#[error.cause]` returns `org.mule.extension.http.api.request.validator.ResponseValidatorTypedException`. If you print the return instance of `ResponseValidatorTypedException`, Mule prints the result of `toString`. When the error has an associated known HTTP status code (such as 404), the string representation of the `ResponseValidatorTypedException` instance is a human-readable description of the error.
- `#[error.errorMessage]` returns:
```text
org.mule.runtime.core.internal.message.DefaultMessageBuilder$MessageImplementation
{
  payload=org.mule.runtime.core.internal.streaming.bytes.ManagedCursorStreamProvider@223d8f75
  mediaType=application/json; charset=UTF-8
  attributes=org.mule.extension.http.api.HttpResponseAttributes
{
   Status Code=404
   Reason Phrase=Not Found
   Headers=[
      date=Sat, 03 Aug 2019 04:28:29 GMT
      content-type=application/json; charset=utf-8
      content-length=2
      connection=keep-alive
      set-cookie=__cfduid=de19ed0b495b5b58e74fa0ee31a700d651564806509; expires=Sun, 02-Aug-20 04:28:29 GMT; path=/; domain=.typicode.com; HttpOnly
      x-powered-by=Express
      vary=Origin, Accept-Encoding
      access-control-allow-credentials=true
      cache-control=public, max-age=14400
      pragma=no-cache
      expires=Sat, 03 Aug 2019 08:28:29 GMT
      x-content-type-options=nosniff
      etag=W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
      via=1.1 vegur
      cf-cache-status=HIT
      age=96
      server=cloudflare
      cf-ray=50058b8add0a92fe-SJC
   ]
}
  attributesMediaType=*/*
}
```

The `errorMessage` element becomes available when a connector or component exposes the message that it has interpreted as an error. For example, when an HTTP request receives a status code that Mule treats
as an error, the process fails and also populates the `errorMessage` with
information about the error. You can then gain access to error message
attributes (metadata) and to the payload itself with
`#[error.errorMessage.payload]` for the payload and
`#[error.errorMessage.attributes]` for the metadata. In the case of an HTTP
request that returns an error, you can then use
`#[error.errorMessage.attributes.statusCode]` to select the value of the
status code (such as `404`). To see message attributes in Studio, see
DataSense.
- `#[error.childErrors]` returns: `[]`

### Mule Error Types

Mule errors have a namespace (such as `HTTP:` and `FILE:`) and identifier
(such as `NOT_FOUND`), and they belong to a hierarchy of error types.

The naming convention enables you to
distinguish errors according to their domain. For example, instead of
throwing `NOT_FOUND`, the HTTP connector can throw `HTTP:NOT_FOUND`, and the
File connector can throw `FILE:NOT_FOUND` errors.

Unlike connectors, Mule runtime errors have an implicit `MULE` namespace, so
`MULE:EXPRESSION` and `EXPRESSION` are interpreted the same way.

Error types can have a parent
type. For example, the parent of `HTTP:UNAUTHORIZED` is `MULE:CLIENT_SECURITY`,
and the parent of `MULE:CLIENT_SECURITY` is `MULE:SECURITY`. This hierarchy
implies that each error type is a specification of more global error type.
For example, an `HTTP:UNAUTHORIZED` error type is a type of client security
error (`MULE:CLIENT_SECURITY`), which is a type of a more broad security issue
(`MULE:SECURITY`).

The hierarchies enable you to route errors in a general or more specific way. For
example, an error handler for `MULE:SECURITY` catches `HTTP:UNAUTHORIZED` errors
and OAuth errors. The follow figure shows the core runtime hierarchy:

All errors belong to one of these two main types: `ANY` or `CRITICAL`. Each type
under `ANY` is matched by its parent and can be handled, while error types under
`CRITICAL` are so severe that cannot be handled and are only logged. `CRITICAL`
errors include `FATAL_JVM_ERROR` and `OVERLOAD`.

Whenever there is no clear reason for a failure, a component can use the
`UNKNOWN` type. You handle this error through the `ANY` type to define unclear
errors, without changing the existing behavior of the app.

For connectors, each connector defines its error type hierarchy considering
the core runtime hierarchy, though `CONNECTIVITY` and `RETRY_EXHAUSTED` types
are always present because they are common to all connectors.

Error Types:

- `ANY`: error type that matches all error types that occur in a Flow and can be
handled. This type does not include errors that occur on the source.
  - `TRANSFORMATION`: indicates an error occurred while transforming a value. This involves Mule runtime internal transformations and not DataWeave transformations.
  - `EXPRESSION`: indicates an error occurred while evaluating a DataWeave expression.
  - `VALIDATION`: indicates a validation error occurred.
    - `DUPLICATE_MESSAGE`: indicates a validation error regarding a message being processed twice. For example, using the Idempotent message validator.
  - `REDELIVERY_EXHAUSTED`: indicates that max attempts to reprocess a message from a source have been exhausted.
  - `CONNECTIVITY`: indicates that there was a problem establishing a connection. This could occur while using a connector, for example, an HTTP requester.
    - `RETRY_EXHAUSTED`: indicates that retries of a certain execution block have been exhausted. For example, for a given operation, or using Until Successful Scope.
  - `ROUTING`: indicates an error occurred while routing a message. For example, using the Round Robin router.
    - `COMPOSITE_ROUTING`: indicates that one or more errors occurred while routing a message. For example, using a Scatter Gather Router.
  - `SECURITY`: indicates a security error occurred, like invalid credentials being received or an expired token being used.
    - `CLIENT_SECURITY`: indicates an external entity (e.g., calling an external endpoint) produced a security error.
    - `SERVER_SECURITY`: indicates a security error enforced by the Mule runtime.
      - `NOT_PERMITTED`: indicates a security restriction enforced by a filter. For example, using the Authorization Filter of the Mule Spring Module.
  - `STREAM_MAXIMUM_SIZE_EXCEEDED`: indicates the maximum size allowed for a stream has been exceeded. For more insight, see Streaming in Mule Apps.
  - `TIMEOUT`: indicates timeout occurred while processing a message.
  - `UNKNOWN`: indicates an unknown or unexpected error occurred. This cannot be handled directly, only by handling `ANY`, to ensure backward compatibility in case more error types are added in future runtime versions.
- `SOURCE`: indicates that an error occurred in the source of the flow. These errors cannot be handled.
  - `SOURCE_ERROR_RESPONSE_GENERATE`: indicates that an error occurred in the source of the flow generating the parameters of an error response. This error cannot be handled since the source has already executed the failing path.
  - `SOURCE_ERROR_RESPONSE_SEND`: indicates that an error occurred in the source of the flow sending an error response. This error cannot be handled since the source has already executed the failing path.
- `SOURCE_RESPONSE`: indicates that an error occurred in the source of a flow while processing a successful response. These errors can only be propagated since the source has already executed the successful path. These errors cannot be handled.
  - `SOURCE_RESPONSE_GENERATE`: indicates an error occurred in the source of the flow while generating the parameters of a successful response.
  - `SOURCE_RESPONSE_SEND`: indicates an error occurred in the source of the flow while sending a successful response.
- `CRITICAL`: indicates a severe error occurred. These errors cannot be handled.
  - `OVERLOAD`: indicates a problem of overloading occurred and the execution was rejected.
    - `FLOW_BACK_PRESSURE`: indicates a problem of overloading occurred at the source level. For example, using an HTTP listener as a source.
  - `FATAL_JVM_ERROR`: indicates that a fatal error occurred, such as stack overflow.

#### What Happens After a FATAL_JVM_ERROR

When the JVM throws a `VirtualMachineError` (for example, `OutOfMemoryError` or `StackOverflowError`), Mule runtime wraps it as a `MULE:FATAL` error and raises a `FATAL_ERROR_RAISED` alert. Because these errors are in the `CRITICAL` hierarchy, On-Error components (`on-error-continue`, `on-error-propagate`) can't handle them.

After a `VirtualMachineError` occurs, the Mule runtime instance, its internal components, or the underlying JVM can remain in an invalid state. Memory can be corrupted, threads can enter undefined states, and further message processing is unreliable.

The only safe recovery action after a `VirtualMachineError` occurs is to restart the Mule runtime instance. Don't assume that the application can continue processing correctly after encountering one of these errors.

##### Common Causes

| Error | Common Causes |
|---|---|
| `OutOfMemoryError` | Unbounded in-memory caching, unconsumed streams that accumulate buffers, processing very large payloads without streaming, or memory leaks in custom Java code. |
| `StackOverflowError` | Extremely long flows that create deeply nested Reactor operator stacks, or unbounded recursion in custom Java components or DataWeave expressions. Recursive flow references (a flow calling itself through `flow-ref`) are protected by Mule runtime internal nesting limit, which raises an `EventContextDeepNestingException` before a JVM stack overflow occurs. |

##### Monitoring and Recovery

- Monitor application logs for messages containing `VirtualMachineError`, `OutOfMemoryError`, or `StackOverflowError`.
- In managed deployment targets (CloudHub, Runtime Fabric), configure health checks and automatic restarts so that affected instances are replaced quickly.
- For on-premises deployments, configure your process supervisor (systemd, Tanuki wrapper) to restart the Mule process if it becomes unresponsive.
- After a restart, investigate the root cause by using heap dumps (for `OutOfMemoryError`) or thread dumps (for `StackOverflowError`) captured before the failure occurs.

For design patterns that help prevent these errors, see Avoid Recursive Flow References and Consume Streams Promptly.

### Custom Error Types

To use custom error types, you need to define them either when mapping or when
raising the errors. These errors
require a specific custom namespace to
distinguish them from other existing types within an application. This means
that an app that uses HTTP and Database connector operations cannot use the
HTTP and DB namespaces for custom error types.

You need to define namespaces that are related to the particular Mule app name
or context and avoid using existing connector namespaces. For example, a
customer aggregation API might use the `CUSTOMER` namespace for its custom
error types, and an order-processing API might use the `ORDER` namespace.

### Error Mappings

In each operation of your flow, you can map the possible error types to a
custom error type of your choosing. You can use these custom error types to
differentiate where an error occurred in your flow.
For example, if your flow has two HTTP Request operations that reach out to
different REST services, a connectivity failure on either produces the same
error. By mapping each error to different custom error types, you can
differentiate the error handling of each operation failure and quickly identify
the source of the error in the Mule app logs.

In the following example, you can see how mappings allow granular error handling
by defining two custom error types: `APP:CUSTOMER_API` and `APP:ORDER_API`.

Example XML Configuration for Mappings:
```xml
<flow name="retrieveMatchingOrders">
  <http:request config-ref="customersConfig" path="/customer">
    <error-mapping sourceType="CONNECTIVITY" targetType="APP:CUSTOMER_API"/>
  </http:request>
  <http:request config-ref="ordersConfig" path="/order">
    <error-mapping sourceType="CONNECTIVITY" targetType="APP:ORDER_API"/>
  </http:request>
  <error-handler>
    <on-error-continue type="APP:CUSTOMER_API">
      <logger message="#['Could not retrieve customer data.']"/>
    </on-error-continue>
    <on-error-continue type="APP:ORDER_API">
      <logger message="#['Could not retrieve customer order data.']"/>
    </on-error-continue>
  </error-handler>
</flow>
```

## Error Handlers

Errors that occur in Mule belong to one of two major categories:

- system errors
- messaging errors

### System Errors

Mule throws a system error when an exception occurs at the system level and
no Mule event is involved. A system error handler manages exceptions that occur:

- During application startup.
- When a connection to an external system fails.

When a system error occurs, Mule sends an error notification to registered
listeners, logs the error, and if the error is caused by a connection failure,
executes a reconnection strategy.

System error handlers are not configurable in Mule.

### Messaging Errors

Mule throws a messaging error (a Mule error)
whenever a problem occurs within a flow of a Mule app, where Mule events
and the messages they contain are processed.

You can handle Mule messaging errors in more than one way:

- You can rely on the default error handling mechanism.
- Within a flow, you can set up xref:on-error-scope-concept.adoc[On-Error
components] (On Error Continue and On Error Propagate) inside the flow's
built-in Error Handler component. These components can contain any number of
components to process the error.
The following figure shows what happens when an event processor, such as an
HTTP request or database operation, throws an error:
- Outside a flow, you can set up an Error Handler
component and reference it from other Error Handler configurations. The global
Error Handler can also contain On-Error components and their contents.
- It is also possible to set up error handling from within a
Try scope that resides in a flow. The scope contains
a built-in Error Handler in which you can configure On-Error components and
their contents.

#### Using Default Error Handling for Messages

By default, unhandled messaging errors are logged and propagated. When a flow is
processing a Mule message that raises an error, the normal execution of the flow
stops, and the process transfers to the flow's default error handler, which
propagates the error.

The following example shows a simple Mule app configuration that relies on
default error handling instead of using explicitly configured error handling
components to manage the error.

The XML for the default error handling example looks like this:

```xml
<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<http:request-config name="HTTP_Request_configuration" doc:name="HTTP Request configuration" >
  <http:request-connection host="jsonplaceholder.typicode.com" port="80" />
</http:request-config>
<flow name="error-handlers-example" >
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/users"/>
  <http:request method="GET" doc:name="Request" config-ref="HTTP_Request_configuration" path="/somebadrequest"/>
</flow>
```

After you start a Mule app with this configuration and trigger the HTTP listener
by loading `http://0.0.0.0:8081/users` (for example, into a browser), the flow makes
an HTTP request (`http://jsonplaceholder.typicode.com:80/somebadrequest`) for
a file that does not exist. As a result, the Anypoint Studio console logs and propagates
the error to the web browser.

- Anypoint Studio Console Log
The Studio console prints an error message. The message indicates that
the default handler, `OnErrorPropagateHandler`, propagates a 404 error returned
from the HTTP GET request. Mule identifies this error as HTTP:NOT_FOUND.
```text
ERROR 2021-01-19 18:48:50,392
  [[error-handlers-example].http.requester.HTTP_Request_configuration.11 SelectorRunner]
  [processor: error-handlers-example/processors/0; event: 1d3baf11-5aa0-11eb-b96f-a483e7abe2b5] org.mule.runtime.core.internal.exception.OnErrorPropagateHandler:
********************************************************************************
Message               : HTTP GET on resource 'http://jsonplaceholder.typicode.com:80/somebadrequest' failed: not found (404).
Element               : error-handlers-example/processors/0 @ error-handlers-example:error-handlers-example.xml:15 (Request)
Element DSL           : <http:request method="GET" doc:name="Request" config-ref="HTTP_Request_configuration" path="/somebadrequest"></http:request>
Error type            : HTTP:NOT_FOUND
FlowStack             : at error-handlers-example(error-handlers-example/processors/0 @ error-handlers-example:error-handlers-example.xml:15 (Request))

  (set debug level logging or '-Dmule.verbose.exceptions=true' for everything)
********************************************************************************
```

The error logs in the Studio console present the following information:
  - **Message**: Description of the error
  - **Element**: XML element that failed execution and caused the error
  - **Element DSL**: XML element that failed execution and caused the error, expressed in DSL
  - **Error type**: Type of Mule error raised by the Mule app
  - **Flowstack**: Flowstack trace error log
This field lists an entry for each flow that processed the Mule event and the processor that sent the event to the next flow. The last entry shows the flow and the processor that failed during the processing of the event.
Starting with Mule 4.3.0, the Flowstack entry is enabled by default. You can disable Flowstack logging by setting the `mule.flowTrace` configuration property to `false`.

- Error Propagation to the Web Browser
A description of the HTTP:NOT_FOUND error appears in the browser tab you
use to trigger the listener:
```text
HTTP GET on resource 'http://jsonplaceholder.typicode.com:80/somebadrequest'
failed: not found (404).
```

This Mule error description appears in the browser for two reasons:
  - The default error handler uses an On Error Propagate process (`OnErrorPropagateHandler`).
The On Error Propagate component causes the flow to fail and the HTTP listener to prepare an error response
for the `404` error associated with the file not found.
  - The HTTP listener is using default error (`error.description`) and success (`payload`) responses to
return the message body.
Because no custom responses are configured, the browser shows the description of the error.

#### Using On-Error Components to Handle Messaging Errors

Instead of relying on the default error-handling mechanism, you can use
On-Error components (On Error Continue and
On Error Propagate) inside a built-in or external Error Handler component.

The following example shows a simple flow that is configured in Studio to return
the results of an HTTP request when the HTTP listener is triggered. Unlike the
default error-handling example, this example
configures On Error Continue (`on-error-continue`) inside the flow's built-in
Error Handler (`error-handler`) component, and On Error Continue contains a
Logger that writes a description of the error.

The XML for the example looks like this:
```xml
<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<http:request-config name="HTTP_Request_configuration" doc:name="HTTP Request configuration" >
  <http:request-connection host="jsonplaceholder.typicode.com" port="80" />
</http:request-config>
<flow name="error-handlers-normalFlow" >
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/users"/>
  <http:request method="GET" config-ref="HTTP_Request_configuration" path="/somebadrequest"/>
  <logger level="INFO" doc:name="Logger" />
  <error-handler>
    <on-error-continue enableNotifications="true" logException="true" doc:name="On Error Continue" >
      <logger level="ERROR" doc:name="Logger" message="#[error.description]"/>
    </on-error-continue>
  </error-handler>
</flow>
```

As in the default error-handling example, the requested page is not found, so
the flow returns a 404 error that Mule identifies as an HTTP:NOT_FOUND error.
However, in this case, the tab of the browser used to trigger the HTTP
listener is blank because the error is not propagated. With On Error Continue,
the flow in the example is treated as though it ends successfully with a 200 for
the GET request, even though the page is not found. The HTTP listener executes
the behavior for the default success response (returning `payload` content
as the message body). Because the page was not found, there is no content to
display in the browser, so the browser tab is blank.

The Studio console also prints an error message (the first ERROR message below)
indicating that `OnErrorContinueHandler` is handling the error, and it prints an
ERROR message from the logger (the second ERROR below) that describes the Mule
error (an `error.description`, see
Selector Expressions for Mule Errors).

```text
ERROR 2021-01-19 18:42:04,583
  [[error-handlers-example].http.requester.HTTP_Request_configuration.11 SelectorRunner]
  [processor: error-handlers-normalFlow/processors/0; event: 2a95eaa1-5a9f-11eb-b96f-a483e7abe2b5] org.mule.runtime.core.internal.exception.OnErrorContinueHandler:
********************************************************************************
Message               : HTTP GET on resource 'http://jsonplaceholder.typicode.com:80/somebadrequest' failed: not found (404).
Element               : error-handlers-normalFlow/processors/0 @ error-handlers-example:error-handlers-example.xml:15
Element DSL           : <http:request method="GET" config-ref="HTTP_Request_configuration" path="/somebadrequest"></http:request>
Error type            : HTTP:NOT_FOUND
FlowStack             : at error-handlers-normalFlow(error-handlers-normalFlow/processors/0 @ error-handlers-example:error-handlers-example.xml:15)

  (set debug level logging or '-Dmule.verbose.exceptions=true' for everything)
********************************************************************************

ERROR 2021-01-19 18:42:04,586
  [[error-handlers-example].http.requester.HTTP_Request_configuration.11 SelectorRunner]
  [processor: error-handlers-normalFlow/errorHandler/0/processors/0; event: 2a95eaa1-5a9f-11eb-b96f-a483e7abe2b5] org.mule.runtime.core.internal.processor.LoggerMessageProcessor:
  HTTP GET on resource 'http://jsonplaceholder.typicode.com:80/somebadrequest' failed: not found (404).
```

If you instead create the same Mule app using On Error Propagate
(`on-error-propagate`) instead of On Error Continue (`on-error-continue`), you
receive the same error messages in the Studio console, but you also see the
logged error message in your browser. This behavior is identical to the
default error handling behavior because both use On Error Propagate.

Note that within each On-Error component, the error path you define can
incorporate any number of event processors to handle specific error types as
precisely as you want. You can select specific Mule errors for the On-Error
component to handle. The Error Handler component routes an error to the
first On-Error component that matches the error.

For more information about On Error Continue and On Error Propagate, see
On-Error components.

#### Referencing a Global Error Handler

A global error handler can be useful if you want more than one flow or Try scope
to handle errors in the same way. You can create reuse configurations by
providing a reference to an error handler:

- global error config set
- global error config ref

##### Setting a Global Error-Handling Configuration

The following XML configuration defines a default error-handling configuration
that uses
`<configuration doc:name="Configuration" defaultErrorHandler-ref="allErrorHandler" />`
to reference the `<error-handler name="allErrorHandler"/>` configuration.

```xml
<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<http:request-config name="HTTP_Request_configuration" doc:name="HTTP Request configuration" >
  <http:request-connection host="json.typicode.com/" port="80" />
</http:request-config>
<configuration doc:name="Configuration" defaultErrorHandler-ref="allErrorHandler" />
<flow name="someFlow" >
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/users"/>
  <http:request method="GET" doc:name="Request" config-ref="HTTP_Request_configuration" path="/somebadrequest"/>
</flow>
<error-handler name="allErrorHandler" >
  <on-error-continue enableNotifications="true" logException="true" doc:name="On Error Continue" >
    <set-payload value="#[error.description]" doc:name="Set Payload" />
  </on-error-continue>
</error-handler>
```

In the Studio UI, the global error-handling example looks like this:

The example includes two main components for handling errors, an Error Handler
(`error-handler`) with embedded components that are visible in the Studio canvas
and a global error-handling configuration, which is not visible in the canvas.
The flow (**someFlow**) in the UI example illustrates that the Error Handler
component lies outside any flow in the Mule app.

Because the request produces an HTTP:NOT_FOUND error, the Studio console prints
an error message indicating that `OnErrorContinueHandler` is handling the error.
On Error Continue configurations do not propagate the errors they handle
(see on error continue).

To set up the global error-handling example through the Studio UI instead
of writing the configuration in XML markup:

1. Drag the Error Handler component from the **Mule Palette** to the Studio canvas,
and name it **allErrorHandler**.
Notice that the component is not part of any flow.
1. Drag the On Error Continue component into the Error Handler component.
1. Drag a Set Payload component into the On Error Continue component.
Note that the Set Payload component is an example. You can use other components,
such as a Logger, and you can write your own error message inside that
component. The Set Payload example uses a Mule variable for the error
description (see the `error` variable in
Predefined Variables for details).
1. Create a global error-handling reference in Studio:
  1. Click **Global Elements** to open **Global Configuration Elements**.
**Global Elements** is located below the Studio canvas.
  1. In **Global Configuration Elements**, click **Create** to open the
**Choose Global Type** dialog.
  1. From the dialog, select **Global Configuration** --> **Configuration**, and then
click **OK** to open the **Configuration** dialog.
  1. From the select **Configuration** dialog, select **allErrorHandler** for the
**Default Error Handler** field, and click **OK**.
1. Set up the HTTP listener and HTTP request components using the values
described in the XML.
1. Check that the XML configuration looks correct by clicking **Configuration XML**
(located below the Studio canvas).

#### Referencing an Error-Handling Configuration from a Flow

> **Note:** The configuration of some elements in these examples is XML-only.

A flow can reference a global error handler that resides outside the flow. The
flow logs all its errors through a reference.

**Example: XML Configuration for the App**

```xml
<error-handler name="loggingErrorHandler">
    <on-error-continue>
        <logger message="#['Error: ' ++ error.description]"/>
    </on-error-continue>
</error-handler>

<flow name="withSharedHandler">
    <http:request url="http://example.com"/>
    <error-handler ref="loggingErrorHandler"/>
</flow>
```

In this XML example, the global error handler is configured through an
`<error-handler/>` element named `loggingErrorHandler`. The flow references
the error handler with `<error-handler ref="loggingErrorHandler"/>`.

To reference a global error handler configuration from a flow in Studio:

1. From Studio, drag an **Error Handler** component from the **Mule Palette**
to the canvas, and configure it components through the UI.
1. In the Mule app, click **Configuration XML** (located below the Studio canvas).
1. (XML-only configuration) Within your `<flow/>` element, type the XML for the
reference, for example, `<error-handler ref="loggingErrorHandler"/>`.

The following example references a global On Error Continue element
(`<on-error-continue/>`) using `<on-error ref="loggingErrorHandler"/>`
within an `<error-handler/>` element. Both require manual configuration
through the **Configuration XML**, rather than the UI.

```xml
<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
	<http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<on-error-continue name="loggingErrorHandler">
    <logger message="#['Error: ' ++ error.description]" level="INFO"/>
</on-error-continue>

<flow name="withSharedHandler">
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/"/>
  <http:request url="http://jsonplaceholder.typicode.com/badrequestbad" method="GET"/>
  <error-handler >
    <on-error ref="loggingErrorHandler"/>
  </error-handler>
</flow>
```

## On-Error Components

When an error occurs in a Mule app, an Error Handler component routes the error
to the first On-Error component (On Error Continue or On Error Propagate)
configuration that matches the Mule error, such as `HTTP:NOT_FOUND`,
`DB:CONNECTIVITY`, or `ANY` (the default for all Mule errors). If no error handling
is configured for the error, the app follows a
default error handling process.

**Error Handling Components in Studio**

### On-Error Components Behavior

On-Error components differ in the way they affect their _owner_,
that is, the Flow or Try scope where they are defined. Also, On-Error components can be defined inside a Global Error Handler, affecting the entire Mule application.

#### On Error Propagate

Executes but propagates the error to a higher level, such as a containing
scope (for example, to a Flow that contains a Try scope where the error occurs)
or external flow containing a Flow Reference to the flow in which an error occurs.
The error breaks the owner's execution and propagates to that higher level,
causing a failure at that level. In addition, any transaction the owner handles
is rolled back. However, note that the transaction is not rolled back if another
component (one that does not own On Error Propagate) created the transaction.

#### On Error Continue

Executes and uses the result of the execution as the result of its owner,
as if the owner completed the execution successfully. Any transaction the
owner handles is committed. However, note that the transaction is not committed
if another component (one that does not own On Error Continue) created the
transaction.

### Error Matching

To help you identify and handle potential errors when designing a Mule app,
On-Error components list the errors that the runtime engine and operations
configured in the app can throw. You can select the errors you want to handle.

- Matching based on error type:
On-Error components can perform matching based on
error types you select. The list of
selectable error types depends on the module and connector operations within the
flow or scope to which the On-Error component applies. It also lists `EXPRESSION`
and `STREAM_MAXIMUM_SIZE_EXCEEDED` errors, which the runtime can throw.

- Matching based on a condition (for more advanced use cases):
You can perform error matching based on a `when` condition that you define in the
**When** field of an On-Error component. For example, you might map the component
to fatal errors, which have error messages that contain the word "fatal":
```xml
<on-error-continue
  enableNotifications="true" logException="true"
  type="ANY"
  when='error.cause.message contains "fatal"'/>
```

In the example, every error that matches the `when` expression is handled by `on-error-continue`. You can also add a restrictive type such as `type="HTTP:CONNECTIVITY"` so that the error handler handles only the errors that match the specified type and condition.

Note that matching conditions are evaluated sequentially, in the order in
which the On-Error components reside in the error handler. For example, if
you want to handle `VALIDATION:NOT_NULL` in one way but handle all other
errors a different way, provide an On-Error component configuration
for that error before a component that captures the remaining errors
(identified as `ANY` by the second On-Error component). Remember that
default error handling takes place for errors you do not explicitly match
or use ANY to capture.

### Configuration and Use

In most cases, you configure On-Error components within the scope-like Error
Handler component. Though each flow contains only one built-in Error Handler,
the Error Handler can contain as many On-Error components as you require, and
each On-Error component can contain any number of other components, such as
Loggers and other components that you configure to handle errors captured by
the On-Error component.

Because an Error Handler component is built into Flow and Try components, you
can use On-Error components for errors that occur within the scope of a flow or
within a Try component. For examples, see
Using On-Error Components to Handle Messaging Errors.

You can also use On-Error components in a separate Error Handler configuration
that is referenced from a Flow component or Try scope (see
Referencing a Global Error Handler).

By default, On-Error components also log matching errors and enable error
notifications for occurrences of the errors. You can disable these settings by modifying the component properties in Studio or by editing the configuration XML.
You can also configure notification listeners in your Mule application so that they can react to the notification events.

#### Error Handling within a Flow

Within a flow's built-in Error Handler component, you can set up one or more
On-Error components to match error types and expressions. The following example
outlines the general structure for handling errors that occur within a given
flow. One flow uses On Error Continue (`on-error-continue`) in its Error Handler
component. The other flow uses On Error Propagate (`on-error-propagate`).

```xml
<flow name="catch">
  <!-- flow logic -->
  <error-handler>
    <on-error-continue>
      <!-- error handling logic -->
    </on-error-continue>
  </error-handler>
</flow>

<flow name="rollback">
  <!-- flow logic -->
  <error-handler>
    <on-error-propagate>
      <!-- error handling logic -->
    </on-error-propagate>
  </error-handler>
</flow>
```

For examples, see
Using On-Error Components to Handle Messaging Errors.

#### Reuse of On-Error Scopes

Just as you can share error handlers by exposing them globally and referencing
them in flows and try scopes, you can also reuse On-Error components. You can
define and name an On-Error component globally and then reference from an
Error Handler component.

**Example: XML Configuration for Referenced On-Error**

```xml
<on-error-propagate name="sharedPropagateHandler">
  <logger message="An unhandled error has occurred."/>
</on-error-propagate>

<on-error-continue type="EXPRESSION" name="sharedContinueHandler">
  <logger message="An expression failed to evaluate."/>
</on-error-continue>

<error-handler name="reusingHandlers">
  <on-error ref="sharedContinueHandler"/>
  <on-error-continue type="ROUTING">
    <logger message="An expression failed to evaluate."/>
  </on-error-continue>
  <on-error ref="sharedPropagateHandler"/>
</error-handler>
```

For other reuse examples, see
Referencing a Global Error Handler.

### Error Handling Example

The following error handlers are configured to produce
`{ "MyError": "value was expected to be null" }` for a `VALIDATION:NOT_NULL`
error, rather than `{ "messageANY" : "Some other error" }`. The string
`value was expected to be null` is the description of the
`VALIDATION:NOT_NULL` error. The Is Null component can throw this error.
Is Null belongs to the Validation module.

```xml
<error-handler >
  <on-error-continue
    enableNotifications="true"
    logException="true"
    type="VALIDATION:NOT_NULL">
    <ee:transform >
      <ee:message>
        <ee:set-payload><![CDATA[%dw 2.0
output application/json
---
{
MyError : error.description as String
}]]></ee:set-payload>
      </ee:message>
    </ee:transform>
  </on-error-continue>
  <on-error-continue
    enableNotifications="true"
    logException="true"
    type="ANY">
    <ee:transform>
      <ee:message >
        <ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
{
"messageANY" : "Some other error"
}
]]></ee:set-payload>
      </ee:message>
    </ee:transform>
  </on-error-continue>
</error-handler>
```

### On-Error Components Reference

| Field | Value | Description |
|---|---|---|
| Type (`type`) | Mule error type | A comma-separated list of Mule error types that defines the errors handled by this on-error strategy. |
| When (`when`) | DataWeave Expression | A matching expression that defines the condition to trigger the execution of this on-error strategy. The expression must evaluate to a boolean value (`true` or `false`). |
| Enable Notifications (`enableNotifications`) | Boolean | Specifies if this strategy fires a notification of type `ExceptionNotification` when an error occurs. The default value is `true`. |
| Log Exception (`logException`) | Boolean. | Specifies if the error is logged, at level `ERROR`, before this strategy handles it. The default value is `true`. |

## Raise Error Component

This core component generates a Mule error, as if a failure had occurred, which allows you to customize its description and type.

Use this component to only raise:

- Core runtime errors, such as `MULE:SECURITY`, `MULE:CONNECTIVITY`, etc.
- Custom error types. +

You cannot raise an error from another connector or module like `FILE:FILE_NOT_FOUND`, `JSON:INVALID_SCHEMA`. You cannot use a connector's existing namespace.

### Raise Error Configuration

| Field | Value | Description | Example |
|---|---|---|---|
| Description | String or DataWeave expression | Specifies the error description. |  `description="Error description message."` |
| Type | String | Specifies the type of the error. |  `type="CUSTOM:CUSTOM_ERROR"` |

### Raise Core Runtime Error Types

For core runtime error types, you must use the implicit namespace and identifier, you can only customize the error's description message. For example:

```xml
<raise-error type="MULE:CONNECTIVITY" description="Error description message"/>
```

### Raise Custom Error Types

For custom error types, declare a new namespace. The namespace of an error type should help you identify the origin of an error. For example:

```xml
<raise-error type="ORDER:INVALID_DATA" description="Email is invalid. Cannot complete transaction"/>
```

You cannot use existing namespaces from connectors or modules, since these have their defined namespaces.
Once you declare a custom namespace by using it in a `raise-error`, you can use it in other `raise-error` components and custom types.

### Examples

The following example of a driving lessons platform checks that the user is over 16 years old to drive. The flow raises a `PRECONDITIONS:INCORRECT_AGE` error when the user enters an age lower than 16 years.

- The Choice router components adds conditional processing to the flow.
- If the age parameter sent in the request is lower than 16 `http://localhost:8081/test?age=15`, the Raise Error component raises the error type `PRECONDITIONS:INCORRECT_AGE` and description `Minimum age of 16 required to drive`.
- Then, an On-Error Continue component matches the type of the error `PRECONDITIONS:INCORRECT_AGE` and executes the Logger component inside its scope. The Logger component logs the error message `Minimum age of 16 required to drive`.
- If the age parameter is greater than 16 in the request `http://localhost:8081/test?age=17`, a Logger component returns the default message `User age above 16 years. Allowed to drive`.
- If no age parameter is passed in the request `http://localhost:8081/test` the choice component will automatically raise a `MULE:EXPRESSION` error when trying to evaluate the expression `#[message.attributes.queryParams.age < 16]` because no age parameter was provided in the request, so its value is null.
- Then, an On-Error Continue component matches the type of the error `MULE:EXPRESSION` and executes the Logger component inside its scope. The Logger component returns the message `The parameter age is missing or invalid`.

XML Configuration of the Flow:
```xml
<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<flow name="raise-error-example-flow">
  <http:listener config-ref="HTTP_Listener_config" path="/test"/>
  <choice>
    <when expression="#[message.attributes.queryParams.age < 16]">
      <raise-error type="PRECONDITIONS:INCORRECT_AGE" description="Minimum age of 16 required to drive" />
    </when>
    <otherwise >
      <logger level="INFO" message="User age above 16 years. Allowed to drive"/>
    </otherwise>
  </choice>
  <error-handler >
    <on-error-continue enableNotifications="true" logException="true" type="PRECONDITIONS:INCORRECT_AGE">
      <logger level="INFO" message="Minimum age to drive is 16 years old"/>
    </on-error-continue>
    <on-error-continue enableNotifications="true" logException="true"  type="MULE:EXPRESSION">
      <logger level="INFO" message="The parameter age is missing or invalid"/>
    </on-error-continue>
  </error-handler>
</flow>
```

Consider an API that returns an account balance when making a request to `https://unsecurebank.com/balance`. +
The following example, makes a request to this API and stores the value in the `balance` variable, then it compares it with `payload.amount` to determine if the operation is possible. +
The Choice router produces an `ACCOUNT:INSUFFICIENT_FUNDS` error when a transfer amount surpasses the available balance, preventing the transfer from taking place. Additionally, it generates a dynamic description by providing an expression with failure details.

XML Configuration of the Flow:
```xml
<flow name="raise-error-example-flow">
  <http:request url="https://unsecurebank.com/balance" target="balance"/>
  <choice>
    <when expression="#[payload.amount > vars.balance]">
      <raise-error type="ACCOUNT:INSUFFICIENT_FUNDS" description="#['Cannot transfer $(payload.amount) since only $(vars.balance) are available.']"/>
    </when>
  </choice>
  <http:request url="https://unsecurebank.com/transfer"/>
</flow>
```
