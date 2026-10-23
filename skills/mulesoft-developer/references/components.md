# Core component XML reference

> Derived from the Anypoint Code Builder documentation at docs.mulesoft.com.

Every component also accepts `doc:name` (the canvas label) and
`doc:id` (a generated identifier). Both are omitted below.

## Async (<async/>)

Group components in a scope and execute them simultaneously with the main flow in an asynchronous
fashion.

The main flow of the application continues to execute after it initiates and processes the Async
scope. The flow does not have to pause until the last message processor embedded in the asynchronous
flow has completed its task. Async is useful for executing time-consuming operations that do not
require you to send a response back to the initiating flow (such as printing a file or connecting to
a mail server).

To facilitate simultaneous branch processing, the Async scope sends one copy of the message it has
received to the first embedded message processor in its own processing block. At the same time, it
sends another copy of the message to the next message processor in the main flow.

Because the Async scope is executed in a "fire and forget" manner, the result of the processing
within the scope is not available in the main flow.

### Component XML

This component supports the following XML structure:

```xml
<async maxConcurrency="" name="">
    <!-- Components to execute asynchronously -->
</async>
```

Async (`<async/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Name** or **Display Name** | `name` | Editable name for the component that appears in the canvas. |
| **Max concurrency** | `maxConcurrency` | Sets the maximum number of concurrent messages that the scope can process. By default, the container thread pool determines the maximum number of threads to use to optimize the performance when processing messages. When the scope is processing the maximum number of concurrent messages, it cannot receive additional requests. Set `maxConcurrency` to `1` to cause the scope to process requests one at a time. See Back-Pressure Management for details about Mule behavior after reaching the maximum concurrency value. |

### Async Scopes versus Subflows

Unlike a subflow, an Async scope:

- Does not inherit the exception strategy of the main flow.

  To handle errors in an Async scope, use the Try scope.

- Processes messages asynchronously.

- Does not pass data back to the main flow.

- Exists inline with the main flow thread.

- Is not called by a Flow Reference component.

- Is not reusable

Even though the Async scope receives a copy of the Mule message, the payload is not copied. The same
payload objects are referenced by both Mule messages: One that continues down the original flow, and
the one processed by the Async scope.

If the payload of your message is a mutable object (for example, a bean with different fields in it)
and a message processor in your Async scope changes the value of one of the fields, the message
processors outside of the Async scope see the changed values.

## Batch Job (<batch:job/>)

Defines the main batch processing scope. A batch job contains two phases:

- **Process Records**: Executes the record processing logic defined in nus.

- **On Complete**: Executes after all records are processed, for example to log results or perform
  cleanup.

### Configuration Options

| Property | Type | Default | Description |
|---|---|---|---|
| `batchBlockSize` | Integer | 50 | Number of records per block to process concurrently within the Process Records phase |

### Child Elements and Scopes

- One or more Batch Steps inside the job

- One optional **On Complete** scope

### Batch Processing Constraints

- Batch jobs can’t be nested.

- At least one Batch Step must be present.

### Batch Processing Example

<batch:job doc:name="Batch Job Example" doc:id="job-1" batchBlockSize="100"> <batch:step
doc:name="Step 1" doc:id="step-1"> <!-- record processors --> </batch:step> <batch:on-complete
doc:name="On Complete" doc:id="onComplete-1"> <!-- final operations --> </batch:on-complete>
</batch:job>

### Batch Step (batch:step/)

Defines a step inside a batch job. Steps group record-level processors and can optionally include a
batch aggregator.

#### Batch Processing Configuration Options

| Property | Type | Default | Description |
|---|---|---|---|
| doc:name | String | Auto-generated | Display name in the canvas |
| doc:id | String | Auto-generated | Unique identifier for the component |

### Child Elements and Sub-Scopes

**Processors**: A sequence of processors (for example, **Transform**, **Logger**) that act on each
record.

**Batch Aggregator**: Aggregates records into blocks (optional).

### Batch Aggregator Constraints

Only one Batch Aggregator is allowed per step.

### Batch Aggregator (batch:aggregator/)

Aggregates records into blocks within a Batch Step for grouped processing before
records are sent back into the flow.

### Batch Aggregator Configuration Options

| Property | Type | Default | Description |
|---|---|---|---|
| doc:name | String | Auto-generated | Display name in the UI |
| doc:id | String | Auto-generated | Unique identifier for the component |
| aggregatorSize | Integer | 100 | Number of records to group before applying aggregation logic |

### Batch Step Behavior

Groups incoming records into blocks of the specified size.

After processing, the records are sent back to the Process Records phase of the Batch Job.

## Cache Scope (<ee:cache/>)

Store and reuse frequently called data.

Use a Cache scope to reduce the processing load on the Mule instance and to increase the speed of
message processing within a flow. The component is particularly effective for these tasks:

- Processing repeated requests for the same information.

- Processing requests for information that involve large repeatable streams.

When a message processor in a Mule app sends a message to the Cache scope, the parent flow expects
an output. The Cache scope processes the message payload, delivers the output to the parent flow,
and saves the output (that is, caches the response). The next time the Cache scope receives the same
kind of message payload, the scope can produce a cached response rather than invoking a potentially
time-consuming process again.

For instance, you can use a Cache scope to manage customer requests for flight information. Many
customers might request the same pricing information about flights from San Francisco to Buenos
Aires. Rather than using a lot of processing power to send separate requests to several airline
databases with each customer query, you can use a Cache scope to schedule periodic requests to
airline databases and present users with the cached prices. When the timeliness of data is not
critical, Cache scope can save time and processing power.

Put any number of message processors (such as connectors or components) into a Cache scope and
configure the caching strategy to store the responses (which contain the payload of the response
message) produced by the processing that occurs within the scope.

The cache scope also works in clustered environments because the object store configured in the
caching strategy is shared across all nodes in the cluster.

### Caching Process

The Cache scope caches repeatable streams. It does not cache nonrepeatable streams, which can be
read only once before they are lost. By default, all streams are repeatable in Mule unless a
component’s streaming strategy is configured to be nonrepeatable.

In general, the caching process follows this sequence:

1.  A message enters the Cache scope.

2.  The Cache scope determines whether the message payload is nonrepeatable.

3.  The Cache scope generates a key to identify the message’s payload.

    By default, Mule uses an SHA256KeyGenerator and a SHA256 digest to generate a unique key for the
    message payload. However, you can set up your own key through a custom caching strategy.

4.  The Cache scope compares the newly generated key to cached responses that it has previously
    processed and saves it in the object store you set up (recommended) or in the default
    `InMemoryObjectStore`.

    - If there is no cached response event (a _cache miss_), the Cache scope processes the new
      message and produces a response.

      It also saves the resulting response in the object store (if the response is repeatable).

    - If there is a cached response event (a _cache hit_), the caching strategy generates a response
      that combines data from both the new request and the cached response.

      If the generated response is a nonrepeatable stream, the scope does not cache the response.

5.  The Cache scope pushes the response out into the parent flow for continued processing.

### Caching Strategy

A caching strategy defines the actions a Cache scope takes when a message enters it. By default, the
Cache scope uses a caching strategy that stores data in an in-memory object store. You can create a
custom caching strategy that references an existing object store, or you can create a new custom
object store to use in this caching strategy.

You can configure the cache size, expiration time, and maximum allowed entries by setting these
values in the object store that you define or reference from the caching strategy. You can also
configure a caching strategy to sync access to the cache, to avoid different message processors from
using the cache at the same time.

Your caching strategy can also reference these customizations:

- Event Key for the object store, which is a DataWeave expression or Java object used to create the
  key to use for storing the payload in the object store.

- Response Generator for your strategy, which is a reference to a Java object that is used to create
  the responses returned by the caching strategy.

- Event Copy Strategy for mutable or immutable data.

#### Synchronized Access to a Cache

By default, Mule synchronizes access to a cache to avoid unexpected results if multiple message
processors (on the same or different Mule instances) use the cache at the same time.

Consider a scenario in which two message processors attempt to retrieve a value from a cache but do
not find the value in the cache. Each message processor calculates the value independently and
inserts it into the cache. If access to the cache is not synchronized, the value inserted by the
second message processor overwrites the value inserted by the first message processor. If the values
are different, then two different results are obtained for the same input, with only the last one
stored in the cache.

In some scenarios this outcome is valid, but this outcome is an issue if the application requires
cache coherence. Synchronizing the caching strategy ensures coherence. A synchronized cache is
locked when it undergoes modifications by a message processor. In this scenario, a locked cache
forces the second message processor to wait until the first message processor has calculated the
value, and then it retrieves the value from the cache.

You can disable cache synchronization by defining the `synchronized` property in the
`<ee:object-store-caching-strategy/>` element and setting it to `false`.

> [!IMPORTANT] Synchronization affects performance, and the impact is most severe in cluster mode.

### Component XML

This component supports the following XML structure:

```xml
<!-- Caching Strategy definition -->
<ee:object-store-caching-strategy
  name="Caching_Strategy"
  doc:name="Caching Strategy">
    <!-- Object Store to use for the caching strategy -->
</ee:object-store-caching-strategy>

<!-- Cache scope referencing the strategy -->
<ee:cache
  doc:name="Cache"
  doc:id="ahiceg"
  cachingStrategy-ref="Caching_Strategy" >
     <!-- Processing logic to cache -->
</ee:cache>
```

Cache (`<cache/>`) attributes are configurable through the UI and XML:

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Cachingstrategy ref** | `cachingStrategy-ref` | Name of a caching strategy to reference. |
| **Filter expression** | `filterExpression` | DataWeave expression for excluding specific payloads from the Cache scope flow. |

The global configuration element `<object-store-caching-strategy/>` provides the following
attributes:

| Attribute Name | Attribute XML | Description |
|---|---|---|
| N/A | `keyGenerationExpression` | Optional. A DataWeave expression to generate the key, for example, `keyGenerationExpression="#[vars.requestId]"`. |
| N/A | `synchronized` | Indicates whether Mule syncs access to a cache. Accepted values are `true` or `false`. Defaults to `true`. |

## Choice (<choice/>)

Route messages dynamically through a flow according to a set of DataWeave expressions that evaluate
message content.

Each expression is associated with a different routing option. The effect is to add conditional
processing to a flow, similar to an `if`/`then`/`else` code block in most programming languages.

Only one of the routes in the Choice router executes, meaning that the first expression that
evaluates to `true` triggers that route’s execution and the others are not checked. If none of the
expressions are `true`, then the default route executes.

To configure the Choice router, specify one or more conditions to evaluate, and the message
processors that execute when any condition evaluates to `true`. Additionally, configure a default
route that executes when none of the defined conditions are `true`.

### Component XML

This component supports the following XML structure:

```xml
<choice doc:name="Choice" doc:id="qwolaa" tracking:enable-default-events="true" >
  <when expression=${expressionToEvaluate}> (1)
    <!-- Message processors --> (2)
  </when>
  <otherwise>
    <!-- Message processors --> (3)
  </otherwise>
</choice>
```

|  |  |
|---|---|
| 1 | The `expression` attribute has the condition to evaluate. |
| 2 | Add any number of message processors to execute if `expression` evaluates to `true`. |
| 3 | Add any number of message processors to execute if none of the conditions evaluates to `true`. |

Choice (`<choice/>`) attributes are configurable through the UI and XML:

Choice (`<choice/>`) has the following child elements:

| Child Element | Description |
|---|---|
| `<when/>` | Child element for specifying a condition to meet before running embedded components to process the Mule event. One or more `<when/>` elements are allowed. |
| `<otherwise/>` | Child element that runs if no conditions set within any `<when/>` element are met. |

The child element `<when/>` has the following attribute:

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Expression** | `expression` | DataWeave expression used to evaluate input. If the expression evaluates to `true`, this routing option executes. |

## Custom Event (<tracking:custom-event/>)

Add metadata and Key Performance Indicators (KPIs) to your flow through a custom business event.

For your KPIs, use names that are easy to search for in the Anypoint Runtime Manager interface, and
use a representative value, which can be any Mule expression:

| Name | Expression / Value |
|---|---|
| `employee-id` | `#[payload['ID']]` |
| `employee-email` | `#[payload['Email']]` |
| `employee-git-id` | `#[payload['GITHUB_ID']]` |
| `price` | `700` |
| `price-after-discount` | `#[vars.price]` |
| `order-id` | `#[payload.order.header.orderID]` |

### Component XML

This component supports the following XML structure:

```xml
<tracking:custom-event
    event-name=""
    doc:name="Custom event"
    doc:id="akfkag" />
```

Custom Business Event (`<tracking:custom-event/>`) attributes are configurable through the UI and
XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Event name** | `event-name` | Name of the event to track. |
| **Inherits** | `inherits` | N/A |
| **Meta data** | `metaData` | N/A |
| **Target Variable** | `target` | Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name. See Enrich Data with Target Variables in the Mule documentation. |
| **Target Value** | `targetValue` | Value of the data to store in the target variable. By default, the value is the message payload (payload). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but not the keyword `vars`. See Enrich Data with Target Variables in the Mule documentation. |

The child element `<tracking:meta-data/>` attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| N/A | `key` | Name of the KPI. |
| N/A | `value` | Value of the KPI. |

## Dynamic Evaluate (<ee:dynamic-evaluate/>)

Evaluates an expression to select a DataWeave script, and then executes the new script to generate a
result.

The script can use any of the usual
predefined variables, such as `message`,
`payload`,`vars`, or `attributes`, but you can also add custom ones by providing a set of key-value
pairs.

### Component XML

This component supports the following XML structure:

```xml
<ee:dynamic-evaluate
  expression=""
  doc:name="Dynamic evaluate"
  doc:id="ojfqoz">
  <ee:parameters>#[]</ee:parameters>
</ee:dynamic-evaluate>
```

Dynamic Evaluate (`<ee:dynamic-evaluate/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Expression** | `expression` | Expression that selects a DataWeave script that Mule executes, for example, `expression="#[vars.generateOrderScript]"`. |
| **Additional Bindings** | `parameters` | N/A |
| **Target Variable** | `target` | Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name. See Enrich Data with Target Variables in the Mule documentation. |
| **Target Value** | `targetValue` | Value of the data to store in the target variable. By default, the value is the message payload (payload). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but not the keyword `vars`. See Enrich Data with Target Variables in the Mule documentation. |

`<ee:parameters/>` is a child element of Dynamic Evaluate.

| Child Element | Description |
|---|---|
| `<ee:parameters/>` | Key-value pairs that serve as parameters that the DataWeave script can evaluate, for example, `<ee:parameters>#[{name: attributes.queryParams.userName}]</ee:parameters>`. |

## Error Handler (<error-handler/>)

Catches an error thrown by the Mule application and routes it to the first On-Error component
configuration that matches the error type.

The Error Handler component has two child elements, On Error Continue and On Error Propagate, which
enable you to configure routes that execute when the error raised in the application matches the
type of error configured in the handler. Each handler has its own behavior and works relative to the
component that contains it (a Flow or a Try scope):

- On Error Continue (`on-error-continue`): executes and uses the result of the execution as the
  result of its container element (as if the container completed the execution successfully). Any
  transactions at this point commit successfully.

- On Error Propagate (`on-error-propagate`): rolls back any transactions, executes, and uses that
  result to rethrow the existing error. In this case, the container element "fails" its execution.

If there’s no error handling configuration that matches the error, the app follows a default error
handling process. See
Using Default Error Handling for Messages
for more information.

### Component XML

This component supports the following XML structure:

```xml
<flow name="myFlow">

    <error-handler>
      <on-error-propagate name="onErrorPropagate" >
        <!-- error handling logic -->
      </on-error-propagate>
      <on-error-continue name="onErrorContinue" >
        <!-- error handling logic -->
      </on-error-continue>
    </error-handler>

</flow>
```

Error Handler (`<error-handler/>`) attributes are configurable through the UI and XML.

The `<on-error-continue/>` and `<on-error-propagate/>` child elements share the following
attributes:

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **When** | `when` | A matching expression that defines the condition to trigger the execution of this on-error strategy. The expression must evaluate to a Boolean value (`true` or `false`). |
| **Type** | `type` | A comma-separated list of Mule error types that defines the errors this on-error strategy handles. |
| **Log exception** | `logException` | Specifies whether to log the error at level `ERROR` before this strategy handles it. Defaults to `true`. |
| **Enable notifications** | `enableNotifications` | Specifies if this strategy triggers a notification of type `ExceptionNotification` when an error occurs. Defaults to `true`. |

### Error Handling Example

The following example configures handlers to produce
`{ "MyError": "value was expected to be null" }` for a `VALIDATION:NOT_NULL` error and
`{ "messageANY" : "Some other error" }` for other error types.

```xml
<error-handler >
  <on-error-continue
    enableNotifications="true"
    logException="true"
    type="VALIDATION:NOT_NULL">
    <ee:transform >
      <ee:message>
        <ee:set-payload>
        <![CDATA[%dw 2.0
        output application/json
        ---
        {
        MyError : error.description as String
        }]]>
        </ee:set-payload>
      </ee:message>
    </ee:transform>
  </on-error-continue>
  <on-error-continue
    enableNotifications="true"
    logException="true"
    type="ANY">
    <ee:transform>
      <ee:message >
        <ee:set-payload >
        <![CDATA[%dw 2.0
        output application/json
        ---
        {
        "messageANY" : "Some other error"
        }
        ]]>
        </ee:set-payload>
      </ee:message>
    </ee:transform>
  </on-error-continue>
</error-handler>
```

## First Successful (<first-successful/>)

Iterates through a list of configured processing routes until one of the routes executes
successfully.

If any processing route fails execution (throws an error), the router executes the next configured
route.

If none of the configured routes execute successfully, the First Successful router throws an error.

### Component XML

This component supports the following XML structure:

```xml
<first-successful
  doc:name="First successful"
  doc:id="vyaedo" >
  <!-- First Route -->
  <route>
    <!-- Processors -->
  </route>
  <!-- Second Route -->
  <route>
    <!-- Processors -->
  </route>
</first-successful>
```

First Successful (`<first-successful/>`) attributes are configurable through the UI and XML.

`<route/>` is a child element of First Successful.

| Child Element | Description |
|---|---|
| `<route/>` | Accepts one or more components as child elements. Multiple `<route/>` configurations are allowed. |

## Flow (<flow/>)

Group together a sequence of Core components and operations (provided by connectors and modules)
inside a scope to help automate integration processes.

Within a Mule application, a flow is a block of executable components, including any connector
operations, that Mule runtime executes sequentially on a Mule event. A flow can also contain an
event source, which triggers the creation of the event and the execution of the flow. You can create
more than one flow in your Mule app.

For a more in-depth discussion of uses, capabilities, and limits of flows and subflows, see
Flows and Subflows.

Flows always function synchronously. To achieve asynchronous patterns, such as Fire-and-Forget, use
the Async Scope.

### Component XML

This component supports the following XML structure:

```xml
<flow name="myFlow">

</flow>
```

Flow (`<flow/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **name1** (default) | `name` | Editable name for the component to display in the canvas. |
| **Initial state** | `initialState` | Indicates whether the flow is active when you start the application. Accepted values are `started` and `stopped`. You can trigger flows in state `started` from an internal or external Mule event source within the flow (such as an HTTP listener or Scheduler), by a Flow Reference from another flow or subflow, or through a call to the lookup DataWeave function. If you set the initial state to `stopped`, use Runtime Manager to activate the flow or reset the Flow configuration to `Started`. The console output for this state is: `Flow flow_component_ex has not been started (initial state = 'stopped')` Defaults to `started`. |
| **Max concurrency** | `maxConcurrency` | Sets the maximum number of concurrent messages that the flow can process. If not set, the container thread pool determines the maximum number of threads the flow can use to optimize the performance when processing messages. While the flow is processing the maximum number of concurrent messages, it cannot receive additional requests. Set `maxConcurrency` to `1` to cause the flow to process requests one at a time. See Back-pressure for details about the behavior of Mule runtime after it reaches the maximum concurrency value. |
| N/A | `tracking:enable-default-event` | When set to `true`, enables business events for Mule apps that you deploy to CloudHub. |
| N/A | `tracking:transaction-id` | Specifies the transaction ID for the business event. Requires `tracking:enable-default-event` set to `true`. |

## Flow Reference (<flow-ref/>)

Routes the Mule event to another flow or subflow, executes all processors in the referenced flow,
and then routes the event back within the same Mule application.

This process enables you to treat the entire referenced flow like a single component in your current
flow.

Flow Reference breaks the Mule application into discrete and reusable units. For example, a flow
that lists files on a regular basis might reference another flow that processes the output of the
List operation. Instead of appending all the processing steps to the flow that lists the files, you
can append a Flow Reference that points to the processing flow.

> [!WARNING] Use actual flow names to define the **Flow name** (`name`) attribute. Using dynamic
> values (DataWeave expressions, variables) to specify the referenced flow negatively affects
> performance. Also, MUnit tests and application analysis tools cannot work on dynamic references.

### Component XML

This component supports the following XML structure:

```xml
<flow-ref name="anotherflow" />
```

Flow Reference (<flow-ref/>) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Name** | `name` | The name of the flow that this component references. |
| **Target Variable** | `target` | Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name. See Enrich Data with Target Variables in the Mule documentation. |
| **Target Value** | `targetValue` | Value of the data to store in the target variable. By default, the value is the message payload (payload). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but not the keyword `vars`. See Enrich Data with Target Variables in the Mule documentation. |

### Considerations when Using a Target Variable

Setting the `target` variable in a Flow Reference component causes the original message to remain
unchanged. This means that any modification to the payload or to the variables that occur in the
referenced flow revert after the referenced flow finishes executing its processors, returning the
payload and variables to their original values.

Alternatively, if you do not define a `target` variable, any modification that occurs to the payload
or to the variables in the referenced flow persist after the referenced flow finishes its execution,
changing the original value of the payload or variables.

### Navigate to the Referenced Flow

You can open the flow that a Flow Reference component points to directly from the canvas, without
switching views manually. To open the referenced flow, right-click the Flow Reference component and
select **Go to Flow**. You can also press Ctrl+Alt+g (Windows) or Cmd+Option+g (macOS).

Anypoint Code Builder opens the target flow in the appropriate canvas:

- In application flows, the referenced flow opens in the flow canvas.

- In MUnit test flows, the referenced flow opens in the MUnit canvas if applicable.

If the referenced flow is in an imported Mule project dependency, you can open it in a read-only
canvas and view its read-only XML. You can inspect the flow and go to other flows in the dependency,
but you can’t modify the dependency flow or its XML.

This helps you trace and manage flow logic across modular designs, whether you’re building or
testing your application.

## For Each (<foreach/>)

Process input in a pattern similar to `for-each` or `for` loop in other programming languages.

### Component XML

This component supports the following XML structure:

```xml
<foreach doc:name="For Each"
  doc:id="119e4859"
  collection="#[payload]"
  counterVariableName="counter"
  batchSize="1"
  rootMessageVariableName="rootMessage" />
```

For Each (`<foreach/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Collection** | `collection` | A DataWeave expression that returns a Java collection, object, array, map, or DOM nodes. For Each automatically splits the collection into elements, such as the highest-level objects in a JSON array of objects. Each element becomes the `payload` on which a processor within For Each acts. For Each accepts collections of any supported content type, such as `application/json`, `application/java`, or `application/xml`. Defaults to `payload`. |
| **Batch size** | `batchSize` | Number that the scope uses to partition the collected elements from the input into sub-collections of a specified size. For example, if input to For Each is an array of 199 elements and you set the batch size to 50, the scope produces three arrays of 50 elements each and one array of 49 elements. Defaults to `1`. |
| **Root message variable name** | `rootMessageVariableName` | Configurable name of the variable that stores the complete, un-split Mule message from the original input to For Each. The message contains the payload and any attributes but does not contain any variables (`vars`), which are part of the Mule event that contains the Mule message. Within For Each, you can gain access to the value of the payload of the message with `vars.rootMessage.payload` and to attributes of the message with `vars.rootMessage.attributes`. For Each consumes this variable, so you can access it only from within the scope. Outside For Each, the variable returns `null`. Defaults to `rootMessage`. |
| **Counter variable name** | `counterVariableName` | Name of the variable that assigns a number to each iteration over a given element. The sequence starts with `1` and proceeds sequentially. Using the default name of this property (`counter`), you can access this number with `vars.counter`. For Each consumes this variable, so it is not available and returns `null` when used outside of the scope. Defaults to `counter`. |

## Idempotent Message Validator (<idempotent-message-validator/>)

Ensure that only unique messages continue through a flow execution by checking the unique ID of the
incoming message.

You can use any incoming attribute of the Mule message as an ID, or you can compute the ID by
configuring a DataWeave expression. You can also use the DataWeave `Crypto` functions to compute
hashes (SHA, MD5) from the data.

### Component XML

This component supports the following XML structure:

```xml
<idempotent-message-validator
  doc:name="Idempotent message validator"
  doc:id="cyuupj"
  idExpression="#[]">
  <!-- Object Store to use for storing the processed message IDs -->
  <os:private-object-store />

</idempotent-message-validator>
```

Idempotent Message Validator (`<idempotent-message-validator/>`) attributes are configurable through
the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Value expression** | `valueExpression` | N/A |
| **Id expression** | `idExpression` | The expression Mule uses to generate the ID. You can use a DataWeave function to calculate the ID, or you can extract the ID from any existing value of the Mule message. |
| **Store prefix** | `storePrefix` | N/A |
| **Object store** | `objectStore` | N/A |

## Invalidate Cache (<ee:invalidate-cache/>)

Invalidate the complete cache in the referenced caching strategy.

Invalidate cache entries when you want the Cache Scope to recalculate the value for those cache
entries. Alternatively, you can configure the caching strategy to invalidate entries automatically
based on time by setting the `entryTtl` parameter in the defined custom object store.

### Component XML

This component supports the following XML structure:

```xml
<ee:invalidate-cache
  cachingStrategy-ref=""
  doc:name="Invalidate cache"
  doc:id="kacopu" />
```

Invalidate Cache (`<ee:invalidate-cache/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Cachingstrategy ref** | `cachingStrategy-ref` | Reference to the caching strategy for the cache to invalidate. |

## Invalidate Key (<ee:invalidate-key/>)

Invalidate a single cache key in the referenced caching strategy.

### Component XML

This component supports the following XML structure:

```xml
<ee:invalidate-key
  cachingStrategy-ref=""
  doc:name="Invalidate key"
  doc:id="ezsaex" />
```

Invalidate Key (`<ee:invalidate-key/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Cachingstrategy ref** | `cachingStrategy-ref` | Reference to the caching strategy for the cache key to invalidate. |
| **Key generation expression** | `keyGenerationExpression` | Optional. A DataWeave expression to generate the key to invalidate. Use the same expression configured in the caching strategy that generated the key. |
| **Keygenerator ref** | `keyGenerator-ref` | N/A |

## Logger Component (<logger/>)

Configure messages for logs anywhere in a Mule flow. Mule applications print the messages when the
Logger executes.

### Component XML

This component supports the following XML structure:

```xml
<logger
  level="ERROR"
  doc:name="Logger"
  doc:id="45653f08"
  message="my logger message"
  category="My OPTIONAL CUSTOM CATEGORY"/>
```

Logger (`<logger/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Message** | `message` | A string in double or single quotation marks, a DataWeave expression, a Mule variable, or a concatenated combination of supported values that serve as the message. When this field is empty, the Logger produces the following message: { payload=<not set> mediaType=*/* attributes=<not set> attributesMediaType=*/* } |
| **Level** | `level` | Options are `DEBUG`, `ERROR`, `INFO` (default), `TRACE`, `WARN`. In the console, the logger message begins with the `level`. |
| **Category** | `category` | Optional string that describes the logger in a way that helps you distinguish it from other loggers in your flow. In the console, the logger replaces the generic processor name with your category. |

## Parallel For Each (<parallel-foreach/>)

Process a collection of messages by splitting the collection into parts that are simultaneously
processed.

After processing all messages, the component aggregates the results following the same order they
were in before the split, and then the flow continues.

Parallel For Each buffers all processing routes' results in a list to return it after the scope
finishes processing, which can cause out-of-memory errors when processing a large number of entries.
To process large payloads, use Batch Processing instead.

### Component XML

This component supports the following XML structure:

```xml
<parallel-foreach
  doc:name="Parallel foreach"
  doc:id="tbfiiz"
  collection="#[payload]"
  timeout=30000
  maxConcurrency=15 />
```

Parallel For Each (`<parallel-foreach/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Collection** | `collection` | An expression that returns a collection. Defaults to `#[payload]`. |
| **Timeout** | `timeout` | Specifies the timeout in milliseconds for each parallel route. |
| **Max concurrency** | `maxConcurrency` | Specifies the maximum level of parallelism for the router to use. + By default, all routes run in parallel. |
| **Target Variable** | `target` | Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name. See Enrich Data with Target Variables in the Mule documentation. |
| **Target Value** | `targetValue` | Value of the data to store in the target variable. By default, the value is the message payload (payload). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but not the keyword `vars`. See Enrich Data with Target Variables in the Mule documentation. |

## Parse Template (<parse-template/>)

Process a template and obtain a result.

A template includes text with embedded DataWeave expressions that Mule evaluates and replaces with
their result.

Configure a template through an external file reference, or embed the template in the component
configuration.

### Component XML

This component supports the following XML structure:

```xml
<parse-template
  doc:name="Parse template"
  doc:id="fppwuw"
  location="template.html" />
```

Parse Template (`<parse-template/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Content** | `content` | String representing the template where embedded expressions are evaluated and replaced by their results. |
| **Location** | `location` | Location of the template file. Mule inserts values extracted from the message properties or variables into this file. |
| **Output encoding** | `outputEncoding` | Encoding of the payload that this component outputs. |
| **Output mime type** | `outputMimeType` | MIME type of the payload that this component outputs. For more information, see Using Reader and Writer Properties. |
| **Parameters** | N/A | Appends a key-value pair for a reader property to the value of the `outputMimeType` attribute. Multiple key-value pairs are allowed. Reader properties are specific to the MIME type. For example, see the JSON reader properties for `application/json`. To find other reader properties, navigate to a supported format from the DataWeave format documentation, and see Using Reader and Writer Properties. |
| **Target Variable** | `target` | Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name. See Enrich Data with Target Variables in the Mule documentation. |
| **Target Value** | `targetValue` | Value of the data to store in the target variable. By default, the value is the message payload (payload). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but not the keyword `vars`. See Enrich Data with Target Variables in the Mule documentation. |

## Raise Error (<raise-error/>)

Generates a Mule error to indicate that a failure occurred.

You can customize the error’s description and type. Use this component to raise:

- Core runtime errors, such as `MULE:SECURITY` and `MULE:CONNECTIVITY`.

- Custom error types.

You cannot raise an error from another connector or module, such as `FILE:FILE_NOT_FOUND` or
`JSON:INVALID_SCHEMA`. You cannot use a connector’s existing namespace.

### Component XML

This component supports the following XML structure:

```xml
<raise-error
  type="MULE:CONNECTIVITY"
  description="Error description message" />
```

Raise Error (`<raise-error/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Type** | `type` | The type of error. |
| **Description** | `description` | The error description. |

## Remove Variable (<remove-variable/>)

Removes a Mule variable from a Mule event.

### Component XML

This component supports the following XML structure:

```xml
<remove-variable
  doc:name="Remove Variable"
  variableName="myMuleVar" />
```

Remove Variable (`<remove-variable/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Variable name** | `variableName` | Name of the Mule variable to remove. |

## Round Robin (<component-xml-root/>)

Provide two or more processing routes, and execute only one of the routes each time the flow
executes the component.

Each route within Round Robin is a scope that can contain one or more processors. Starting with the
first route, Round Robin initiates execution of processors within the route over a Mule event and
sends the results to the next processor in the flow. Round Robin keeps track of the previously
selected route and never selects the same route consecutively. For example, the first time Round
Robin executes, the component selects the first route. The next time, it selects the second route.
If the previously selected route is the last route, Round Robin executes the first route.

The payload, variables, and attributes from the Mule event that reaches Round Robin are accessible
for processing within the route. Any changes to the Mule event within a route propagate to the
processor after Round Robin.

### Component XML

This component supports the following XML structure:

```xml
<round-robin
  doc:name="Round robin"
  doc:id="kaykco" >
  <!-- First processing route -->
  <route>
    <!-- Processors -->
  </route>
  <!-- Second processing route -->
  <route>
    <!-- Processors -->
  </route>

</round-robin>
```

Round Robin (`<round-robin/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| N/A | `tracking:enable-default-events` | When set to `true`, activates the Business Events feature. |

`<route/>` is a child element of Round Robin.

| Child Element | Description |
|---|---|
| `<route/>` | Accepts one or more components as child elements for processing the Mule event. Multiple `<route/>` configurations are allowed. |

## Scatter-Gather (<scatter-gather/>)

Process a Mule event through two or more routes, and combine the results into a single event object.

### Component XML

This component supports the following XML structure:

```xml
<scatter-gather doc:name="Scatter-Gather"
  doc:id="24d159a9"
  timeout="0"
  target="myTarget"
  maxConcurrency="10">
    <route >
      <!-- one or more processors here -->
    </route>
    <route >
      <!-- one or more processors here -->
    </route>
</scatter-gather>
```

Scatter Gather (`<scatter-gather/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Timeout** | `timeout` | Sets the timeout for responses from sent messages, in milliseconds. A value of `0` or less than `0` prevents a timeout. Defaults to `0`. |
| **Max concurrency** | `maxConcurrency` | Sets the maximum number of routes to run concurrently. By default, all routes run in parallel. Setting this value to `1` makes the component process the routes sequentially. |
| **Collect list** | N/A | N/A |
| **Target Variable** | `target` | Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name. See Enrich Data with Target Variables in the Mule documentation. |
| **Target Value** | `targetValue` | Value of the data to store in the target variable. By default, the value is the message payload (payload). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but not the keyword `vars`. The default value is `#[payload]`. See Enrich Data with Target Variables in the Mule documentation. |

`<route/>` is a child element of Scatter Gather.

| Child Element | Description |
|---|---|
| `<route/>` | Accepts one or more components as child elements for processing the Mule event. Multiple `<route/>` configurations are allowed. |

### Error Handling

This component can throw the following errors:

- `MULE:ROUTING`

- `MULE:COMPOSITE_ROUTING`

If you configure a timeout for this component and a route does not complete processing before the
timeout expires, the route throws a `MULE:TIMEOUT` error. Mule handles this error as it handls other
errors generated from a route: After each route completes (either by processing successfully or by
throwing a `MULE:TIMEOUT` error), the successful results and errors are collected into the
`MULE:COMPOSITE_ROUTING` error and then processed within a configured error handler component.

## Scheduler (<scheduler/>)

Trigger execution of a flow based on a time-based condition. For example, a Scheduler might create
and send a message that will trigger the flow processing every 5 seconds or every day at 12:00 in a
given time zone.

The Scheduler sets a scheduling strategy at a fixed frequency or an interval based on a cron
expression.

When adding a Scheduler to your Mule application, consider these points:

- Schedulers use the same timezone as the machine on which Mule is running. However, if an
  application is running in CloudHub, the Scheduler conforms to the UTC timezone, regardless of the
  geographic region in which the application is running.

  To set a different time zone for the Scheduler, see `timeZone` in the
  cron scheduling strategy attributes.

- The `disallowConcurrentExecution` property enables you to prevent the Scheduler from triggering
  the execution of the flow while a previously-triggered execution is running.

- If back-pressure occurs because no
  resources are available at the time of the scheduled trigger, Mule skips that execution.

- In a Mule runtime engine cluster or multi-worker CloudHub deployment, the Scheduler executes only
  on the primary node (that is, only in one Mule instance).

### Component XML

This component supports the following XML structure:

```xml
<scheduler doc:name="Scheduler" doc:id="snswxf" >
  <scheduling-strategy/>
</scheduler>
```

Scheduler (`<scheduler/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Disallow concurrent execution** | `disallowConcurrentExecution` | When this attribute is set to `true`, the Scheduler skips its scheduled execution if a previous execution is still running. Once the flow finishes, the Scheduler executes at the next configured interval. The default value is `false`. |

**Scheduling strategy** (`<scheduling-strategy/>`) is a child element of Scheduler.

| Child Element | Description |
|---|---|
| `<scheduling-strategy/>` | Accepts a `<fixed-frequency/>` or `<cron/>` configuration. |

#### Fixed Frequency Attributes

Scheduler accepts a fixed frequency (`<fixed-frequency/>`) element that accepts these attributes:

| Attribute Name | Attribute XML | Description |
|---|---|---|
| N/A | `frequency` | The frequency at which the Scheduler triggers the flow given the `timeUnit` setting. Defaults to `1000`. |
| N/A | `startDelay` | The amount of time to delay execution of the Scheduler for the first time after the application starts. This property uses the same `timeUnit` as the frequency. Defaults to `0`. |
| N/A | `timeUnit` | One of the following time units for the values of `frequency` and `startDelay`: `MILLISECONDS`, `SECONDS`, `MINUTES`, `HOURS`, or `DAYS`. Defaults to `MILLISECONDS`. |

See the fixed frequency examples.

#### Cron Attributes

For more complex scheduling, configure a cron expression in the `<cron/>` element.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| N/A | `expression` | A cron expression for triggering the Scheduler. There is no default cron expression. For guidance with expressions, see Cron Expressions. Example: `expression="1 1 1 1,7 * ?"`. |
| N/A | `timeZone` | Time zone passed as a system property, or in a machine’s operating system. Java time zone values are supported. Avoid Java abbreviations, such as `PST` and `AGT`, and instead use the full-name Java equivalents, such as `America/Los_Angeles`. Example: `timeZone="America/Argentina/Buenos_Aires"`. |

See the cron examples.

## Set Payload (<set-payload/>)

Sets or updates the payload of the message.

The payload can be a literal string or a DataWeave expression. Use the `set-payload` component only
for simple expressions or transformations. For complex scenarios, use the
Transform Message Component.

### Component XML

This component supports the following XML structure:

```xml
<set-payload
  value=""
  doc:name="Set payload"
  doc:id="vnjpqo" />
```

Set Payload (`<set-payload/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Value** | `value` | A literal string or DataWeave expression that defines how to set the payload, for example, `"some string"` or `#[now()]`. This attribute is required. |
| N/A | `resource` | A `.dwl` file containing a DataWeave transformation script. These values are resolved statically (not dynamically). For example, using `<ee:set-payload resource="myscript-$site.dwl"/>` generates an error. For more information, see dwl File. |
| **Encoding** | `encoding` | Encoding of the payload that this component outputs. |
| **Mime type** | `mimeType` | MIME type of the payload that this component outputs. For more information, see Using Reader and Writer Properties. |
| **Parameters** | N/A | Appends a key-value pair for a reader property to the value of the `outputMimeType` attribute. Multiple key-value pairs are allowed. Reader properties are specific to the MIME type. For example, see the JSON reader properties for `application/json`. To find other reader properties, navigate to a supported format from the DataWeave format documentation, and see Using Reader and Writer Properties. |

> [!WARNING] The `mimeType` and `encoding` attributes do not affect a DataWeave expression used as a
> `value`. These attributes affect the _output_ Mule Message only. If a transformation is required,
> the DataWeave expression must contain an explicit `output` directive.

## Set Variable (<set-variable/>)

Creates or updates a Mule variable to store values
for use within the flow of a Mule app.

A Mule variable is part of the Mule event. You can store
simple literal values such as strings or messages, message payloads, or attribute objects. For
example, you might store the original payload of a message (before it is processed) so you can use
it later in the flow or within an error handler.

Don’t use Set Variable for complex expressions or transformations. Instead, use the component for
simple operations, such as selections, and use the Transform component for complex scenarios.

### Component XML

This component supports the following XML structure:

```xml
<set-variable
  variableName="myVar"
  value="myVarValue"
  doc:name="Set variable"
  doc:id="mrsngz" />
```

Set Variable (`<set-variable/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Value** | `value` | Value for the variable, which can be a string or a DataWeave expression. For an example that uses an expression, see Use Dynamic Writer Properties. This attribute is required. |
| **Variable name** | `variableName` | Name of the variable, which can be a string or a DataWeave expression. Variable names are must include only numbers, characters, and underscores. This attribute is required. |
| **Encoding** | `encoding` | Encoding of the payload that this component outputs. |
| **Mime type** | `mimeType` | MIME type of the payload that this component outputs. For more information, see Using Reader and Writer Properties. |
| **Parameters** | N/A | Appends a key-value pair for a reader property to the value of the `outputMimeType` attribute. Multiple key-value pairs are allowed. Reader properties are specific to the MIME type. For example, see the JSON reader properties for `application/json`. To find other reader properties, navigate to a supported format from the DataWeave format documentation, and see Using Reader and Writer Properties. |

### Accessing Variables in Other Event Processors

Set Variable sets a variable in the current Mule event, and the variables then travel with the Mule
event to downstream event processors. You can access any variable with DataWeave using `vars`. For
example, you can access a variable named _lastMessage_ with `vars.lastMessage`. You can set
variables in a Transform component, and also many connectors and event processors have a Target
variable that you can set.

## Subflow (<sub-flow/>)

Group together a sequence of Core components and operations (provided by connectors and modules)
inside a scope that you invoke from a Flow Reference in your Mule application.

The Subflow component works in a similar way to the Flow component but with
the following differences:

- Subflows do not support Mule event sources.

- Subflows do not have a built-in error handling scope.

- During design, subflows work as macros that replace the Flow Reference components that call them.

  When you build the application, Mule replaces all Flow Reference components that call a subflow
  with the contents of the referenced subflow.

- Referencing subflows results in better performance than referencing a flow.

You can create multiple subflows in your Mule application.

For a more in-depth discussion of uses, capabilities, and limits of flows and subflows, see
Flows and Subflows.

### Limitations

Because the contents of a subflow replace each Flow Reference component that references that
subflow, several instances of the event processors inside that subflow exist in the application at
runtime. This behavior can cause issues with event processors that depend on unique IDs or instances
to execute.

### Component XML

This component supports the following XML structure:

```xml
<sub-flow name="mySubFlow">

</sub-flow>
```

Subflow (`<sub-flow/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **name1** (default) | `name` | Editable name for the subflow. |

## Transaction (<tracking:transaction/>)

Set an identifier for all tracked events.

Use a transaction ID so that meaningful information, such as an order number, is displayed for a
transaction when analyzing tracked events at runtime, whether using Anypoint Runtime Manager or
CloudHub.

The transaction ID supports DataWeave expressions, which enables you to create an ID dynamically and
include information related to the event into the ID.

### Component XML

This component supports the following XML structure:

```xml
<tracking:transaction
    id="#[payload.orderId]"
    doc:name="Transaction"
    doc:id="qjktlq" />
```

Transaction (`<tracking:transaction/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Id** | `id` | Defines the value of the identifier, which can be an expression or a literal. By default, the component assigns a numeric value. |

## Transform (<ee:transform/>)

Write a DataWeave script within this component to set or transform the Mule message payload,
attributes, or variables to the required output format and data structure.

DataWeave is the programming language for all expressions and data transformations in your
integrations and implementations. The language offers function libraries and mechanisms for creating
customizations, including your own functions, libraries, and data types. To learn the basics of
DataWeave and experiment with DataWeave scripts, see
[DataWeave Tutorial and Playground](https://dataweave.mulesoft.com/), and find DataWeave functions
and guidance with the language in the DataWeave documentation.

### Component XML

This component supports the following XML structure:

```xml
<ee:transform doc:name="Transform" doc:id="xnpgke" >
    <ee:message >
        <ee:set-payload ><![CDATA[%dw 2.0
output application/java (1)
---
//DataWeave script (2)
]]></ee:set-payload>
        </ee:message>
    </ee:transform>
```

|  |  |
|---|---|
| 1 | The `output` directive of a DataWeave script that configures the `application/java` format See Supported Data Formats. |
| 2 | Location for the body of the DataWeave script |

Write a DataWeave script within a Transform
component (`<ee:transform/>`) to create or transform content for any parts of the
Mule event:

`<ee:message/>` and `<ee:variables/>` are child elements of Transform (`<ee:transform/>`):

- `<ee:message/>` accepts child elements for creating or transforming a Mule message payload and
  attributes:

| Element Name | Element XML | Description |
|---|---|---|
| **Set payload** | `<ee:set-payload/>` | Sets or transforms the Mule message payload. This child element of `<ee:message/>` accepts a DataWeave script. One `<ee:set-payload/>` element is allowed. |
| **Set attribute** | `<ee:set-attributes/>` | Sets or transforms one or more Mule message attributes. This child element of `<ee:message/>` accepts a DataWeave script. One `<ee:set-attributes/>` element is allowed. |

- `<ee:variables/>` accepts child elements for creating or transforming a Mule variables:

| Element Name | Element XML | Description |
|---|---|---|
| **Set Variables** | `<ee:set-variable/>` | Sets or transforms a Mule variable. This child element of `<ee:variables/>` accepts a DataWeave script. One or more `<ee:set-variable/>` elements are allowed. |

## Try Scope (<try/>)

Handle errors that might occur during the execution of components inside the scope.

The Try scope catches and handles exceptions thrown by the components that you add to the scope.
Error handling within the scope is similar to error handling within a Flow component. Instead of
configuring a separate flow, you can use Try within a Flow component.

Every payload modification or variable addition, modification, or removal is propagated through the
rest of the execution. This propagation includes modifications that take place inside the error
handlers.

The Try scope supports transactions. A transaction is a series of actions that must execute
successfully. Configure components within the Try scope as a single unit that either succeeds or
fails, depending on whether errors are propagated and the transaction rolled back, or handled and
the transaction committed. In either case, the flow that contains the Try scope continues.

### Component XML

This component supports the following XML structure:

```xml
<try
  doc:name="Try"
  doc:id="dieaig"
  transactionalAction="${action}" />
```

Try scope (`<try/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Transaction type** | `transactionType` | Specifies the type of transaction. Accepted values are: `LOCAL` Default. A single or local transaction. `XA` A transaction that groups operations from multiple resources and follows the Extended Architecture (XA) standard. |
| **Transactional action** | `transactionalAction` | Defines how to handle a transaction. Accepted values are: Ignore (`INDIFFERENT`) Default. If a transaction is active, the scope joins it. If not, the scope does not create a transaction. Always Begin (`ALWAYS_BEGIN`) A new transaction is started every time the scope is executed. Begin or Join (`BEGIN_OR_JOIN`) Relevant only when execution order might vary (for example, due to asynchronous actions occurring outside the flow). If current flow processing has already started a transaction, the scope joins it. If not, the scope initiates a new transaction. |

## Until Successful (<until-successful/>)

Executes processors inside its scope, in order, until they all succeed or the scope exhausts the
maximum number of retries.

Until Successful runs synchronously. If any processor within the scope fails to connect or to
produce a successful result, Until Successful retries all the processors within it, including the
one that failed, until all configured retries are exhausted. If a retry succeeds, the scope proceeds
to the next component. If the final retry does not succeed, Until Successful produces an error.

Routing is successful if no exception is raised or if the response matches an expression.

Common processes that use Until Successful include:

- Dispatching to outbound endpoints, for example, when calling a remote web service that might have
  availability issues

- Executing a component method, for example, when executing on a Spring bean that might depend on
  unreliable resources

- Using a Subflow component (`<sub-flow/>`) to re-execute several actions until they all succeed

### Component XML

This component supports the following XML structure:

```xml
<until-successful
  doc:name="Until successful"
  doc:id="mbqhsp" >
  <!-- Components to execute inside the scope -->
</until-successful>
```

Until Successful (`<until-successful/>`) attributes are configurable through the UI and XML.

| Attribute Name | Attribute XML | Description |
|---|---|---|
| **Max retries** | `maxRetries` | Maximum number of retries allowed. This attribute can be either a number or an expression that resolves to a number. Error messages look like this: `Message: 'until-successful' retries exhausted`. The Mule error type is `MULE:RETRY_EXHAUSTED`. |
| **Millis between retries** | `millisBetweenRetries` | Specifies, in milliseconds, the minimum interval between two retries. The length of the interval is affected by a previous execution but typically does not exceed twice the minimum. This attribute can be a number or an expression that resolves to a number. Defaults to `60000` milliseconds (one minute). |

### Variable Propagation

Every execution of the Until Successful scope starts with the same variables and values present
before the execution of the block, even if an error occurs within the scope before the maximum
number of retries is exhausted. New variables or modifications to already-existing variables while
processing one element are not present when the scope executes. If the execution finishes
successfully, the variables (and payload) are propagated to the rest of the flow.
