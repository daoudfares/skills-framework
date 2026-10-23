# Routers and scopes

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Choice Router

The Choice router dynamically routes messages through a flow according to a set of DataWeave expressions that evaluate message content. Each expression is associated with a different routing option. The effect is to add conditional processing to a flow, similar to an `if`/`then`/`else` code block in most programming languages.

Only one of the routes in the Choice router executes, meaning that the first expression that evaluates to `true` triggers that route's execution and the others are not checked. If none of the expressions are `true`, then the default route executes.

**Schematic diagram of a Choice router with three options, one being the default option**

### Configuration

To configure the Choice router, specify one or more conditions to evaluate, and the message processors that execute when any condition evaluates to `true`. Additionally, configure a default route that executes when none of the defined conditions are `true`.

#### Anypoint Studio Configuration

To configure the Choice router in Studio, follow these steps:

1. Drag the **Choice** component to any point of the flow.
1. Click **When**, inside the Choice router, and configure the **Expression** value in the properties window to specify the condition to evaluate.
1. Drag message processors inside **When** to specify the processors to execute when the condition is met.
1. Drag message processors inside **Default** to specify the processors to execute when none of the defined conditions are met.

#### XML Configuration

Following is the basic XML structure for a Choice router:

```xml
<choice doc:name="Choice">
  <when expression=${expressionToEvaluate}> <1>
  	<!-- Message processors --> <2>
  </when>
  <otherwise>
    <!-- Message processors--> <3>
  </otherwise>
</choice>
```

<1> The `expression` attribute has the condition to evaluate.
<2> Add any number of message processors to execute if `expression` evaluates to `true`.
<3> Add any number of message processors to execute if none of the conditions evaluates to `true`.

### Adding Routes to the Choice Router

By default, the Choice router has one route option that executes when the configured DataWeave expression evaluates to `true`, and a default route that executes when none of the expressions in the existing routes are `true`. Add more routes when you need to evaluate more than one condition and then execute different operations depending on which condition is met.

#### Add Routes by Dragging Components in Studio

From **Mule Palette** in Anypoint Studio, click any component and drag it into the Choice router, where you see a vertical black line:

#### Add Routes by Editing the XML

You can also add additional route options to a Choice router by modifying the XML configuration file:

1. In Studio, right-click the Choice router and select **Go to XML...**.
1. Inside the `<choice>` element, add a `<when>` element:
```xml
<!--Content based routing example flow -->
<flow name="content-based-routingFlow">
  <http:listener config-ref="HTTP_Listener_config" path="/" doc:name="Listener"/>
  <set-variable variableName="language" value="#[attributes.queryParams.language]" doc:name="Set Variable" />
  <!-- Choice router block-->
  <choice doc:name="Choice" >
    <when expression="#[vars.language == 'Spanish']" >
      <set-payload value="Hola!" doc:name="Reply in Spanish" />
    </when>
    <when expression="#[vars.language == 'French']" >
      <set-payload value="Bonjour!" doc:name="Reply in French" />
    </when>
    <!-- This is the new route option added in this step -->
    <when>
    </when>
    <otherwise>
      <flow-ref name="reply-in-default-languageSub_Flow" doc:name="reply-in-default-languageSub_Flow" />
    </otherwise>
  </choice>
  <logger level="INFO" doc:name="Log the reply" message='#["The reply $(payload) means hello in $(vars.language)" ]'/>
</flow>
```

After adding a new `<when>` element, the new route option shows in the Message Flow view:

### Example Project

You can use Anypoint Studio to download the example project _Content-Based Routing_ from Anypoint Exchange. This project presents a working example of a flow that uses the Choice router.

**Flow with a Choice router with three options, one being the default option**

To download and open this example project:

1. Click the Exchange icon () in Anypoint Studio.
1. In the left panel, click **All assets**.
1. In the window that opens, log in to Anypoint Exchange and search for the example project Content-Based Routing.
1. Click the Open icon ().

#### Behavior of the Example Project

When you run the project as a Mule application, the application performs the following actions:

1. Listens for messages.
1. Passes messages to a Set Variable component that sets the variable `language` to the language that is passed in the message by the parameter `language`.
1. Uses a  Choice router to find out whether each message contains a `language` attribute. The presence and value of this attribute determine how the Choice router routes the message:

  - If the value is `French`, the router routes the message to a Set Payload component that is named _Reply in French_. This latter component returns the message `Bonjour!` to the requester.
  - If the value is `Spanish`, the router routes the message to a Set Payload component that is named _Reply in Spanish_. This latter component returns the message `Hola!` to the requester.
  - If the message contains no `language` attribute, the router routes the message to the default path, which is a subflow that:

1. Logs the message "No language specified. Using English as a default." to the console
1. Sets the value of `language` to `English`.
1. Returns the message `Hello!`.

The example project demonstrates that, when you are planning to route messages in a flow by using a Choice router, there are four aspects to planning that you need to consider:

- The content that the Choice router evaluates to determine how it routes messages
- The number of routes
- The default routing option
- The processing that the flow performs for each routing option

### Example XML

Following is the XML code for the Choice router example:

```xml
<mule xmlns:http="http://www.mulesoft.org/schema/mule/http" xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
	xmlns:spring="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-current.xsd
http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/http http://www.mulesoft.org/schema/mule/http/current/mule-http.xsd">
	<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
		<http:listener-connection host="0.0.0.0" port="8081" />
	</http:listener-config>
	<flow name="content-based-routingFlow" >
		<http:listener config-ref="HTTP_Listener_config" path="/" doc:name="Listener" />
		<set-variable variableName="language" value="#[attributes.queryParams.language]" doc:name="Set Variable" />
    <!-- START OF CHOICE BLOCK-->
		<choice doc:name="Choice" >
			<when expression="#[vars.language == 'Spanish']" >
				<set-payload value="Hola!" doc:name="Reply in Spanish" />
			</when>
			<when expression="#[vars.language == 'French']" >
				<set-payload value="Bonjour!" doc:name="Reply in French" />
			</when>
			<otherwise>
				<flow-ref name="reply-in-default-languageSub_Flow" doc:name="reply-in-default-languageSub_Flow" />
			</otherwise>
		</choice>
    <!-- END OF CHOICE BLOCK-->
		<logger level="INFO" doc:name="Log the reply" message='#["The reply $(payload) means hello in $(vars.language)" ]'/>
	</flow>
  <sub-flow name="reply-in-default-languageSub_Flow" >
		<logger level="INFO" doc:name="Logger" message="No language specified. Using English as a default. "/>
		<set-variable variableName="language" value="English" doc:name="Set Language to English" />
		<set-payload value="Hello!" doc:name="Reply in English" />
	</sub-flow>
</mule>
```

### Choice Router XML Reference

A Choice flow control component contains these elements:

- A single root element `<choice>`
- A `<when>` child element for each routing option, each with an expression to match
- Optionally, an `<otherwise>` child element of Choice that handles all cases where none of the expressions on the `<when>` elements evaluate to `true`
- Components that are conditionally executed under each of the choices are defined as child elements of the `when` and `otherwise` elements

#### Properties of <choice>

| Property | Description |
|---|---|
| Business Events | For activating the Business Events feature: + [source,xml,linenums] ---- <choice doc:name="Choice" tracking:enable-default-events="true" > ---- |

#### Properties of <when>

| Property | Description |
|---|---|
| Expression (`expression`) | Expression in DataWeave language to evaluate input. + If the expression evaluates to `true`, this routing option is used: + [source,xml,linenums] ---- <when expression="#[vars.language == 'Spanish']" > ---- |

## Scatter-Gather Router

The Scatter-Gather component is a routing event processor that processes a Mule event through different parallel processing routes that contain different event processors. Each route receives a reference to the Mule event and executes a sequence of one or more event processors. Each of these routes uses a separate thread to execute the event processors, and the resulting Mule event can be either the same Mule event without modifications or a new Mule event with its own payload, attributes, and variables. The Scatter-Gather component then combines the Mule events returned by each processing route into a new Mule event that is passed to the next event processor only after every route completes successfully.

The Scatter-Gather component executes each route in parallel, not sequentially. Parallel execution of routes can greatly increase the efficiency of your Mule application and may provide more information than sequential processing.

The Scatter-Gather component works with repeatable streams. It does not process nonrepeatable streams, which can be read only once before they are lost. By default, all streams are repeatable in Mule unless a component's streaming strategy is configured to be nonrepeatable.

The following diagram details the behavior of the Scatter-Gather component:

1. The Scatter-Gather component receives a Mule event and sends a reference of this Mule event to each processing route.
1. Each of the processing routes starts executing in parallel. After all processors inside a route finish processing, the route returns a Mule event, which can be either the same Mule event without modifications or a new Mule event created by the processors in the route as a result of the modifications applied.
1. After all processing routes have finished execution, the Scatter-Gather component creates a new Mule event that combines all resulting Mule events from each route, and then passes the new Mule event to the next component in the flow.

> **Warning:** Configure your Scatter-Gather component to have at least two routes; otherwise, your Mule application throws an exception and does not start.

### Result

After all routes complete, the component outputs the results in the following format:
`{0: messageFromRoute0, 1: messageFromRoute1, ...}`

To extract all resulting payloads to an array, use a DataWeave script, such as the following:

```text
flatten(valuesOf(payload) map ((item, index) -> item.*payload))
```

### Variable Propagation

Every route starts with the same initial variable values. Modifications to a variable within a specific route do not affect other routes. So, if a variable is added or modified in one route, then, after aggregation, the value is defined by that route. If a variable is added or modified by more than one route, the value is added to a list of all the values defined for that variable within all the routes, for example:

```xml
<set-variable variableName="var1" value="var1"/>
<set-variable variableName="var2" value="var2"/>
<scatter-gather doc:name="Scatter-Gather" doc:id="abc665e0-6119-4ecb-9f8b-52dbcbb1d488" >
	<route >
		<set-variable variableName="var2" value="newValue"/>
        <set-variable variableName="var3" value="appleVal"/>
	</route>
	<route >
		<set-variable variableName="var3" value="bananaVal"/>
	</route>
	<route >
		<set-variable variableName="var3" value="otherVal"/>
        <set-variable variableName="var4" value="val4"/>
	</route>
</scatter-gather>
```

After aggregation, the variables are:

`{var1: "var1", var2: "newValue", var3: ["appleVal, bananaVal, otherVal"], var4: "val4"}`

### Error Handling Inside Scatter-Gather Routes

You can use a Try scope in each route of a Scatter-Gather component to handle any errors that might be generated by a route’s event processors. After every route executes, if any has failed with an error, then the Scatter-Gather component throws an error of type `MULE:COMPOSITE_ROUTING`, and event processing does not proceed past the Scatter-Gather component in the flow. Instead, the flow branches to your error-handling event processors.

Because the `MULE:COMPOSITE_ROUTING` error object gathers not only errors from routes that failed but also Mule events from successfully completed routes, your application can use the error-handling event processors to process Mule events from the routes that completed

To illustrate how this works, consider the following two cases:

- The routes in a Scatter-Gather component each contain a Try scope. +
One of the routes generates an error that is successfully handled by that route’s Try scope through an `on-error-continue` error handler, so the route is completed successfully. The Scatter-Gather component consolidates the Mule events from all routes into a new Mule event and passes the consolidated event to the next event processor.

- One of the routes in a Scatter-Gather component does not contain a Try scope or contains a Try scope with an error handler that cannot handle the error type, or the error handler is an `on-error-propagate` type. +
An error occurs in this route, causing the route to fail, which in turn causes the Scatter-Gather component to throw a `MULE:COMPOSITE_ROUTING` error. The flow branches to your error-handling event processors, which are able to process the Mule events from the completed routes.

Example of handling these errors:
```xml
<flow name="errorHandler">
    <scatter-gather>
        <route>
            <raise-error type="APP:MYERROR"/>
        </route>
        <route>
            <set-payload value="apple"/>
        </route>
    </scatter-gather>
    <error-handler>
        <on-error-continue type="MULE:COMPOSITE_ROUTING">
            <!-- This will have the error thrown by the first route -->
            <logger level="WARN" message="#[error.errorMessage.payload.failures['0']]"/>
            <!-- This will be a null value -->
            <logger level="WARN" message="#[error.errorMessage.payload.failures['1']]"/>

            <!-- This will be a null value -->
            <logger level="WARN" message="#[error.errorMessage.payload.results['0']]"/>
            <!-- This will have the result of the second (correctly executed) route -->
            <logger level="WARN" message="#[error.errorMessage.payload.results['1']]"/>
        </on-error-continue>
    </error-handler>
</flow>
```

### Handle Timeout Errors in a Scatter-Gather

If you configure a timeout for a Scatter-Gather component and a route does not complete processing before the timeout expires, the route throws a `MULE:TIMEOUT` error. This error is then handled the same way as any other error generated from a route: after each route completes (either by processing success or by throwing a `MULE:TIMEOUT` error), the successful results and errors are collected together in the Scatter-Gather component `MULE:COMPOSITE_ROUTING` error, which is then processed in your configured error handler.

### Example Project

In Anypoint Studio, you can download and open the example project _Scatter-Gather Flow Control_ from Anypoint Exchange to learn more about how to use the Scatter-Gather component. This example shows the usage of the scatter-gather control flow to aggregate data in parallel and return the result in JSON.

The example uses prepared data as input for two resources that should be aggregated. The data represents information about two contacts and has the following structure:

| Resource | `firstname` | `surname` | `phone` | `email` |
|---|---|---|---|---|
| contacts-1.csv |  |  |  |  |
| John |  |  |  |  |
| Doe |  |  |  |  |
| 096548763 |  |  |  |  |
| john.doe@texasComp.com |  |  |  |  |
| contacts-2.csv |  |  |  |  |
| Jane |  |  |  |  |
| Doe |  |  |  |  |
| 091558780 |  |  |  |  |
| jane.doe@texasComp.com |  |  |  |  |

DataWeave is used to aggregate the data. The information about the contacts is aggregated to a JSON structure that represents data from both resources.

To download and open this example project while you are in Anypoint Studio, click the Exchange icon in the upper-left corner. Then, in the window that opens, log into Anypoint Exchange and search on the name of the project.

### Scatter-Gather XML Reference

| Element | Description |
|---|---|
| `scatter-gather` | Sends a request message to multiple targets concurrently. It collects the responses from all routes, and aggregates them into a single message. 2+\| **Attributes** |
| `timeout` | Sets the timeout for responses from sent messages, in milliseconds. A value of 0 or lower than 0 means no timeout. |
| `maxConcurrency` | Determines the maximum amount of concurrent routes to process. + By default all routes run in parallel. By setting this value to 1, scatter-gather processes the routes sequentially. |
| `target` | The name of the target variable. |
| `targetValue` | Value of the data to store in the target variable. + If not set, the default value is `#[payload]`. + This field accepts any value that a variable accepts: · Any supported data type. · DataWeave expressions. · The keywords `payload`, `attributes`, and `message`, but _not_ the keyword `vars`. |

| Child Element | Description |
|---|---|
| `route` | One of the routes in a the scatter-gather router. |

#### Throws

- `MULE:ROUTING`
- `MULE:COMPOSITE_ROUTING`

## Round Robin Router

Round Robin is a Mule component that contains two or more processing routes and executes only _one_ of the routes each time the flow executes the component. Each route within Round Robin is a scope that can contain one or more processors. Starting with the first route, Round Robin initiates execution of processors within the route over a Mule event and sends the results to the next processor in the flow. Round Robin keeps track of the previously selected route and never selects the same route consecutively. For example, the first time Round Robin executes, the component selects the first route. The next time, it selects the second route. If the previously selected route is the last route, Round Robin executes the first route.

The payload, variables, and attributes from the Mule event that reaches Round Robin are accessible for processing within the route. Any changes to the Mule event within a route propagate to the processor after Round Robin.

The following examples illustrates the functionality of Round Robin:

```xml
<flow name="round-robin-ex" >
  <scheduler doc:name="Scheduler" > <!-- 1 -->
    <scheduling-strategy >
      <fixed-frequency frequency="10" timeUnit="SECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <set-payload value="#[[1,2,3,4]]" doc:name="Set Payload" /> <!-- 2 -->
  <logger level="INFO" doc:name="Logger" 
          category="PAYLOAD BEFORE ROUND ROBIN" 
  	message="#[payload]"/>
  <round-robin doc:name="Round Robin" >
    <route > <!-- 3 -->
      <set-payload value="#[payload - 4]" doc:name="Set Payload" /> 
      <logger level="INFO" doc:name="Logger" 
              message="#[%dw 2.0
output application/json
---
{ 'r1' : payload}]" 
	      category="ROUTE 1 PAYLOAD"/>
    </route>
    <route > <!-- 4 -->
      <set-payload value="#[payload + 5]" doc:name="Set Payload" />
        <logger level="INFO" doc:name="Logger" 
                message="#[%dw 2.0
output application/json
---
{'r2' : payload}]" 
                category="ROUTE 2 PAYLOAD"/>
    </route>
  </round-robin>
  <logger level="INFO" doc:name="Logger" 
           message="#[payload]" 
	   category="PAYLOAD OUTSIDE ROUND ROBIN"/> <!-- 5 -->
</flow>
```

1. Scheduler (`<scheduler/>`) executes the flow every 10 seconds.
1. Set Payload (`<set-payload/>`) provides the array `[1,2,3,4]`.
1. The Logger component _before_ Round Robin prints the initial payload, `[1,2,3,4]`.
1. In the _first_ route (`<route/>`) of Round Robin, a Set Payload component uses the DataWeave expression `payload - 4` to remove the last element of the initial payload, and the Logger in that route prints the resulting payload as the value of key `"r1"`, `{ "r1": [1,2,3] }`.
1. In the _second_ route (`<route/>`) of Round Robin, a Set Payload component uses the DataWeave expression `payload + 5` to append a new element to the initial payload, and the Logger in that route prints the resulting payload as the value of key `"r2"`, `{ "r2": [1,2,3,4,5] }`.
1. The Logger component _after_ Round Robin prints the payload of the route processed by an execution of Round Robin. The first execution prints `[1, 2, 3]`. The next execution prints `[1, 2, 3, 4, 5]`. The next prints `[1, 2, 3]`, and so on.

In the following excerpt, the logs show three executions of the Round Robin router. In this example, the flow processes Mule events with IDs that begin `4df56260`, `53eb1c50`, and `59e12460`. (The example is edited for readability.)

```text
...

INFO  2022-12-19 10:02:30,233 ...event: 4df56260-7fc7-11ed-957f-147ddaaf4f97] 
      PAYLOAD BEFORE ROUND ROBIN: [1, 2, 3, 4]
INFO  2022-12-19 10:02:30,290 ...event: 4df56260-7fc7-11ed-957f-147ddaaf4f97] 
      ROUTE 1 PAYLOAD: { "r1": [1,2,3] }
INFO  2022-12-19 10:02:30,291 ...event: 4df56260-7fc7-11ed-957f-147ddaaf4f97] 
      PAYLOAD OUTSIDE ROUND ROBIN: [1, 2, 3]

INFO  2022-12-19 10:02:40,154 ...event: 53eb1c50-7fc7-11ed-957f-147ddaaf4f97] 
      PAYLOAD BEFORE ROUND ROBIN: [1, 2, 3, 4]
INFO  2022-12-19 10:02:40,167 ...event: 53eb1c50-7fc7-11ed-957f-147ddaaf4f97] 
      ROUTE 2 PAYLOAD: { "r2": [1, 2, 3, 4, 5] }
INFO  2022-12-19 10:02:40,168 ...event: 53eb1c50-7fc7-11ed-957f-147ddaaf4f97] 
      PAYLOAD OUTSIDE ROUND ROBIN: [1, 2, 3, 4, 5]

INFO  2022-12-19 10:02:50,151 ...event: 59e12460-7fc7-11ed-957f-147ddaaf4f97] 
      PAYLOAD BEFORE ROUND ROBIN: [1, 2, 3, 4]
INFO  2022-12-19 10:02:50,154 ...event: 59e12460-7fc7-11ed-957f-147ddaaf4f97] 
      ROUTE 1 PAYLOAD: { "r1": [1, 2, 3] }
INFO  2022-12-19 10:02:50,154 ...event: 59e12460-7fc7-11ed-957f-147ddaaf4f97] 
      PAYLOAD OUTSIDE ROUND ROBIN: [1, 2, 3]

...
```

### Reference

Round Robin provides a configurable attribute to the `<round-robin />` element.

| Name | XML | Description |
|---|---|---|
| Business Events | `tracking:enable-default-events="true"` | Defaults to `false`. Enables tracking of business events. See business events. |

### Throws

- `MULE:ROUTING`

## First Successful Router

The First Successful router iterates through a list of configured processing routes until one of the routes executes successfully. If any processing route fails execution (throws an error), the router executes the next configured route.

If none of the configured routes execute successfully, the First Successful router throws an error.

### First Successful Router Configuration Example

The following example shows a First Successful router configured with four processing routes:

```xml
<mule xmlns:file="http://www.mulesoft.org/schema/mule/file" xmlns:sockets="http://www.mulesoft.org/schema/mule/sockets"
  xmlns:http="http://www.mulesoft.org/schema/mule/http" xmlns="http://www.mulesoft.org/schema/mule/core"
  xmlns:db="http://www.mulesoft.org/schema/mule/db"  xmlns:doc="http://www.mulesoft.org/schema/mule/documentation" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
                            http://www.mulesoft.org/schema/mule/db http://www.mulesoft.org/schema/mule/db/current/mule-db.xsd
                            http://www.mulesoft.org/schema/mule/http http://www.mulesoft.org/schema/mule/http/current/mule-http.xsd
                            http://www.mulesoft.org/schema/mule/sockets http://www.mulesoft.org/schema/mule/sockets/current/mule-sockets.xsd
                            http://www.mulesoft.org/schema/mule/file http://www.mulesoft.org/schema/mule/file/current/mule-file.xsd">
  <http:request-config name="HTTP_Request_configuration" doc:name="HTTP Request configuration" doc:id="b026579b-5a59-444f-8f91-ff209bed8342" >
    <http:request-connection >
      <http:client-socket-properties >
        <sockets:tcp-client-socket-properties connectionTimeout="500" clientTimeout="500" />
      </http:client-socket-properties>
    </http:request-connection>
  </http:request-config>
  <http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" doc:id="4631e4fd-571f-41c8-831d-d908b1763ef2" >
    <http:listener-connection host="localhost" port="8081" />
  </http:listener-config>
  <flow name="testFlow" doc:id="79cd7fcd-d355-418b-898b-5d7e3a1cbcab" >
    <scheduler doc:name="Scheduler" doc:id="6dc5dcc7-ce33-4d18-9de9-2c665f713508" >
      <scheduling-strategy >
        <fixed-frequency />
      </scheduling-strategy>
    </scheduler>
    <first-successful doc:name="First Successful" doc:id="6ae009e7-ebe5-47cf-b860-db6d51a31251" >
      <route>
        <file:read doc:name="Read non existent file" doc:id="199cdb01-cb43-404e-acfd-211fe5a9167e" path="nonExistentFile"/>
        <set-variable value="1" doc:name="Set successfulRoute var to route 1" doc:id="c740b39e-a1c4-41d6-8a28-0766ca815ec6" variableName="successfulRoute"/>
      </route>
      <route>
        <set-payload value="#[vars.nonExistentVar!]" doc:name="Set Payload with non existent variable" doc:id="0cc9ac4d-5622-4e10-971c-99073cb58df0" />
        <set-variable value="2" doc:name="Set successfulRoute var to route 2" doc:id="88f15c26-d242-4b11-af49-492c35625b84" variableName="successfulRoute" />
      </route>
      <route>
        <set-variable value="3" doc:name="Set successfulRoute var to route 3" doc:id="446afb25-0181-45e5-b04a-68ecb98b57b7" variableName="successfulRoute" />
      </route>
      <route >
        <logger level="INFO" doc:name="Logger" doc:id="b94b905a-3a68-4c88-b753-464bc3d0cfeb" message="This route is never going to be executed"/>
      </route>
    </first-successful>
    <logger level="ERROR" doc:name="Logger" doc:id="9ffe328d-2595-4f28-81e8-ae731fc6cb89" message="#['Successful route was $(vars.successfulRoute)']"/>
  </flow>
</mule>
```

Execution behavior for the previous example is as follows:

1. The first route executes and fails because it tries to read a file that does not exist.
1. The second route fails because it tries to access a variable that does not exist.
1. The third route executes successfully and sets variable `successfulRoute` with value `3`.
1. The fourth route is not executed because the First Successful router stops executing routes after one of them completes successfully.

## For Each Scope

The For Each scope splits a payload into elements and processes them one by one through the components that you place in the scope.
It is similar to a `for-each`/`for` loop code block in most programming languages and can process any collection, including lists and arrays.
The collection can be any supported content type, such as `application/json`, `application/java`, or `application/xml`.

TODO? Splitter not in Studio 7 as of GA. Not clear when it will be in.
### Differences With a Splitter

The For Each scope performs a similar task to using a Splitter and then an Aggregator. The main difference is that the For Each scope outputs a collection just like the one it receives, the Aggregator outputs a message where the payload is a list of mule messages (each with its own payload and attributes).
General considerations about the For Each scope:

- By default, For Each tries to split the payload. If the payload is a simple Java collection, the For Each scope can split it without any configuration. The payload inside the For Each scope is each of the split elements. Attributes within the original message are ignored because they are related to the entire message.
- For Each does not modify the current payload. The output payload is the same as the input.
- For non-Java collections, such as XML or JSON, use a DataWeave expression to split data. Use the **Collection** field for this purpose.
In the following example, the **Collection** field in For Each is set to iterate over an array stored in `payload.topics`:

The For Each scope stores each item of the collection in `payload` during each iteration.
Note that if the input contains information outside the collection you tell it to split, this information is lost.

You can also split an array into batches to enable quicker processing. Each batch is treated as a separate Mule message. For example, if a collection has 200 elements and you set **Batch Size** to `50`, the For Each scope iteratively processes 4 batches of 50 elements, each as a separate Mule message.

### Example XML

This is an example XML based on the For Each scope configuration detailed above:
```xml
...
  <foreach doc:name="For Each" collection="#[payload.topics]" batchSize="1" rootMessageVariableName="rootMessage" counterVariableName="counter">
      <file:write ... >
      <!--Any other module that you want to include in the For Each scope -->
  </foreach>
...
```

### Variable Propagation

Every execution of the For Each scope starts with the variables and values
from the previous execution of the block. New variables or modifications
to existing variables that take place when processing one element are visible
during the processing of another element. These changes to variables continue
to be available outside the For Each scope.

```xml
<set-variable variableName="var1" value="var1"/>
<set-variable variableName="var2" value="var2"/>
<foreach collection="#[['apple', 'banana', 'orange']]">
    <choice>
        <when expression="#[payload == 'apple']">
            <set-variable variableName="var2" value="newValue"/>
            <set-variable variableName="var3" value="appleVal"/>
        </when>
        <when expression="#[payload == 'banana']">
            <set-variable variableName="var3" value="#[vars.var3 ++ ' bananaVal']"/>
            <!-- var3 will now have value 'appleVal bananaVal'-->
        </when>
        <otherwise>
            <set-variable variableName="var3" value="otherVal"/>
            <set-variable variableName="var4" value="val4"/>
        </otherwise>
    </choice>
</foreach>
```

After aggregation, the variables are:

```json
{var1: "var1", var2: "newValue", var3: "otherVal", var4: "val4"}
```

### Error Handling

If one of the elements in a collection throws an exception, the For Each scope stops processing that collection and invokes the error handler.

### Example Projects

There are several example projects in Anypoint Exchange that you can open in Anypoint Studio to learn more about how to use the For Each scope:

- _Authenticating Salesforce using OAuth2_
- _Import contacts into Microsoft Dynamics CRM_
- _Importing a CSV file into mongoDB_
- _Importing an Email Attachment using the IMAP Connector_
- _Importing Email Attachments using the POP3 Connector_
- _Querying a Database and Attaching Results to an Email_

To download and open an example project while you are in Anypoint Studio, click the Exchange icon in the upper-left corner. Then, in the window that opens, log into Anypoint Exchange and search on the name of the project.

### XML Reference

For Each scopes open and close with a `<foreach>` tag. Components that are affected by this scope are defined as child elements of the `<foreach>` tag.

#### Configurable Variables

| Variable | Default | Description |
|---|---|---|
| `collection` | `payload` | An expression that returns a Java collection, object array, map, or DOM nodes. |
| `counterVariableName` | `counter` | Name of the variable that stores the number of messages over which it iterates. |
| `batchSize` | `1` | Partitions the collection into sub-collections of the specified size. For example, if a collection has 200 elements and you set the batch size to 50, it processes 4 batches of 50 elements each. |
| `rootMessageVariableName` | `rootMessage` | Name of the variable that stores the parent message. The parent is the complete, non-split message. |

#### Iterate a JSON Array

```xml
[source,xml]
```

<?xml version="1.0" encoding="UTF-8"?>

<mule xmlns:ee="http://www.mulesoft.org/schema/mule/ee/core" xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/ee/core http://www.mulesoft.org/schema/mule/ee/core/current/mule-ee.xsd">
	<flow name="foreach-test-casesFlow" doc:id="df0421a0-4ec5-482e-8b44-44effb6d4c9d" >
		<scheduler doc:name="Scheduler" doc:id="b833c81f-2e6f-4520-bd5b-fa692786a395" >
			<scheduling-strategy >
				<fixed-frequency />
			</scheduling-strategy>
		</scheduler>
		<ee:transform doc:name="Transform Message" doc:id="ed8669cc-e5a3-4ca4-8040-9c18cd355442" >
			<ee:message >
				<ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
[
	{
		name: 'Mark',
		lastname: 'Panoti'
	},
	{
		name: 'Alyssa',
		lastname: 'Milano'
	}
]
	]]></ee:set-payload>
			</ee:message>
		</ee:transform>
		<foreach doc:name="For Each" doc:id="c3fcdac5-c13a-4de6-bf97-dd7619daa2a3" >
			<logger level="ERROR" doc:name="Logger" doc:id="c62ea746-65bc-425f-bb59-d515b39fb9b8" message="#['Name is $(payload.name) and lastname is $(payload.lastname)']"/>
		</foreach>
	</flow>
</mule>
```text
```

In this case, the payload contains a JSON array. For Each iterates over the payload because the `collection` attribute has not been defined. The payload within For Each is each of the users in the JSON array.

#### Iterate over a Java Map that is Placed in a Variable

```xml
[source,xml]
```

<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns:ee="http://www.mulesoft.org/schema/mule/ee/core" xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/ee/core http://www.mulesoft.org/schema/mule/ee/core/current/mule-ee.xsd">
	<flow name="map-keys-iterateFlow" doc:id="323f6bfd-baec-47c5-b65e-e890958fb537" >
		<scheduler doc:name="Scheduler" doc:id="d79f9550-5da8-4c3d-abec-3b2f508431e7" >
			<scheduling-strategy >
				<fixed-frequency />
			</scheduling-strategy>
		</scheduler>
		<ee:transform doc:name="Transform Message" doc:id="4ce789e8-eeca-4cf6-928d-97e1cfd00825" >
			<ee:message >
			</ee:message>
			<ee:variables >
				<ee:set-variable variableName="users" ><![CDATA[%dw 2.0
output application/java
---
{
	mark: 'Panoti',
	alyssa: 'Milano'
}
]]></ee:set-variable>
			</ee:variables>
		</ee:transform>
		<foreach doc:name="For Each" doc:id="d25efadf-782c-4904-ac06-1ed259749d0e" collection="#[dw::core::Objects::entrySet(vars.users)]">
			<logger level="ERROR" doc:name="Logger" doc:id="d6d56214-4b79-45c9-964f-6c4db1a34bc4" message="#['Name is $(payload.key.name) and lastname is $(payload.value)']"/>
		</foreach>
	</flow>
</mule>
```text
```

The example uses the `ee:transform` to set a variable named `users` with a Java map that is created with DataWeave. Then it uses a built-in DataWeave function to get the entries of a map as a collection in order to iterate over it.

#### Split a Collection into Batches

```xml
[source,xml]
```

<?xml version="1.0" encoding="UTF-8"?>

<mule xmlns:ee="http://www.mulesoft.org/schema/mule/ee/core" xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/ee/core http://www.mulesoft.org/schema/mule/ee/core/current/mule-ee.xsd">
	<flow name="foreach-test-casesFlow" doc:id="df0421a0-4ec5-482e-8b44-44effb6d4c9d" >
		<scheduler doc:name="Scheduler" doc:id="b833c81f-2e6f-4520-bd5b-fa692786a395" >
			<scheduling-strategy >
				<fixed-frequency />
			</scheduling-strategy>
		</scheduler>
		<ee:transform doc:name="Transform Message" doc:id="ed8669cc-e5a3-4ca4-8040-9c18cd355442" >
			<ee:message >
				<ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
[
	{
		name: 'Mark',
		lastname: 'Panoti'
	},
	{
		name: 'Alyssa',
		lastname: 'Milano'
	},
	{
		name: 'Kevin',
		lastname: 'Bacon'
	},
	{
		name: 'Fiona',
		lastname: 'Apple'
	}
]
	]]></ee:set-payload>
			</ee:message>
		</ee:transform>
		<foreach doc:name="For Each" doc:id="c3fcdac5-c13a-4de6-bf97-dd7619daa2a3" batchSize="2" >
			<logger level="ERROR" doc:name="Logger" doc:id="c62ea746-65bc-425f-bb59-d515b39fb9b8" message="#['First user name is $(payload[0].name) and lastname is $(payload[0].lastname)']"/>
			<logger level="ERROR" doc:name="Logger" doc:id="c62ea746-65bc-425f-bb59-d515b39fb9b8" message="#['Second user name is $(payload[1].name) and lastname is $(payload[1].lastname)']"/>
		</foreach>
	</flow>
</mule>
```text
```

The `batchSize` attribute creates sub-arrays of two elements. So inside `foreach`, the payload will have an array of two elements.

#### Aggregate the Process of Each Element into a Variable

```xml
[source,xml]
```

<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns:ee="http://www.mulesoft.org/schema/mule/ee/core" xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/ee/core http://www.mulesoft.org/schema/mule/ee/core/current/mule-ee.xsd">
	<flow name="foreach-test-aggregate" doc:id="df0421a0-4ec5-482e-8b44-44effb6d4c9d" >
		<scheduler doc:name="Scheduler" doc:id="b833c81f-2e6f-4520-bd5b-fa692786a395" >
			<scheduling-strategy >
				<fixed-frequency />
			</scheduling-strategy>
		</scheduler>
		<ee:transform doc:name="Transform Message" doc:id="ed8669cc-e5a3-4ca4-8040-9c18cd355442" >
			<ee:message >
				<ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
[
	{
		name: 'Mark',
		lastname: 'Panoti'
	},
	{
		name: 'Alyssa',
		lastname: 'Milano'
	}
]
	]]></ee:set-payload>
			</ee:message>
		</ee:transform>
		<foreach doc:name="For Each" doc:id="c3fcdac5-c13a-4de6-bf97-dd7619daa2a3" >
			<set-variable variableName="aggregation" value="#[output application/java --- vars.aggregation default '' ++ payload.name[-1 to 0]]" />
		</foreach>
		<logger level="ERROR" message="#[vars.aggregation]"/>
	</flow>
</mule>
```text
```

Within the For Each, the example creates an `aggregation` variable that concatenates the name in reverse. Then that variable can be accessed outside the For Each scope.

EDGE CASE? OUT IN 4.0, PER DAN F. IF THERE'S A REQUEST TO RESTORE IT, WE MIGHT RESTORE IT
### Persisting Data

In case the message inside the For Each scope is persisted, not only the item in the collection is serialized but also all the variables associated with it. The rootMessage variable, associated with the message, contains a reference to the complete, unsplit collection. Therefore, serialization/deserialization of the rootMessage variable could impact memory consumption considerably when this collection is large enough.

To avoid this issue you must first remove the rootMessage variable from the message before persisting it.

### Differences between For Each and Parallel For Each Scopes

Both For Each and Parallel For Each split the defined collection, and the
components within the scope process each element in the collection. Also, in
both cases, each route runs with the same initial context. The difference
between these two scopes are:

- For Each works sequentially, while the Parallel For Each processes in parallel.
This difference affects _error handling_:
Because of the processing differences, the execution of For Each execution is
interrupted when an error is raised (and the Error Handler is invoked), while
Parallel For Each processes every route before invoking the Error Handler with a
`MULE:COMPOSITE_ROUTE` error type.
- For Each does not modify the payload, while the Parallel For Each outputs a
collection of the output messages from each iteration.

See Parallel For Each Scope.

## Parallel For Each Scope

The Parallel For Each scope enables you to process a collection of messages by splitting the collection into parts that are simultaneously processed in separate routes within the scope of any limitation configured for concurrent-processing. After all messages are processed, the results are aggregated following the same order they were in before the split, and then the flow continues.

### Considerations

- Parallel For Each buffers all processing routes' results in a list to return it after the scope finishes processing, which can cause out-of-memory errors when processing a high number of entries. To process large payloads, use Batch Processing instead.
- Anypoint Studio versions prior to 7.6 do not provide this feature in the Mule Palette view. To use Parallel for Each in those versions, you must manually configure Parallel For Each scope in the XML.

### Configuration

The Parallel For Each scope can be configured through the following fields:

| Child element | Description |
|---|---|
| Collection (`collection`) | Specifies the expression that defines the collection of parts to be processed in parallel. By default, it uses the incoming payload. |

| Attribute | Description |
|---|---|
| Collection Expression (`collection`) | An expression that returns a collection. By default, the payload is taken as the collection to split. |
| Timeout (`timeout`) | Specifies the timeout in milliseconds for each parallel route. By default, there is no timeout. |
| Max Concurrency (`maxConcurrency`) | Specifies the maximum level of parallelism for the router to use. By default, all routes run in parallel. |
| Target Variable (`target`) | Specifies a variable to use for storing the processed payload. By default, the output is saved in the flow's payload. |
| Target Value (`targetValue`) | Specifies an expression to evaluate against the operation's output value. The outcome of this expression is stored in the target variable. By default, this is the same as the operation's output value. |

### Example

This XML example adds to every element in the collection the string `"-result"`:

```xml
<flow name="myFlow">

  <parallel-foreach collection="#[['apple', 'banana', 'orange']]">
      <set-payload value="#[payload ++ '-result']"/>
  </parallel-foreach>

</flow>
```

Every execution of the Parallel For Each scope starts with the same variables and values as before the execution of the block.

New variables or modifications of already existing variables while processing one element are not visible while processing another element. All of those variable changes are not available outside the Parallel For Each scope, the set of variables (and their values) after the execution of the Parallel For Each Scope remains the same as before the execution.

Consider the following example:

```xml
<flow name="myFlow">

  <set-variable variableName="var1" value="var1"/>
  <set-variable variableName="var2" value="var2"/>
  <parallel-foreach collection="#[['apple', 'banana', 'orange']]">
      <choice>
          <when expression="#[payload == 'apple']">
              <set-variable variableName="var2" value="newValue"/>
              <set-variable variableName="var3" value="appleVal"/>
          </when>
          <when expression="#[payload == 'banana']">
              <set-variable variableName="var3" value="bananaVal"/>
          </when>
          <otherwise>
              <set-variable variableName="var3" value="otherVal"/>
              <set-variable variableName="var4" value="val4"/>
          </otherwise>
      </choice>
  </parallel-foreach>

</flow>
```

After aggregation, the variables are:

`{var1: "var1", var2: "var2"}`

None of the modifications done inside the Parallel For Each scope are registered, including the creation of new variables.

### Error Handling

Because every route is processed in parallel, if an error is thrown in one route, processing continues in all of the other routes until all finish processing. After that, all results (and any errors) are aggregated and then processed by the Error Handler, as shown here:

```xml
<flow name="myFlow">

  <parallel-foreach collection="#[['banana', 'apple']]">
      <choice>
          <when expression="#[payload == 'banana']">
              <!-- Processor that throws error -->
          </when>
          <otherwise>
              <set-payload value="#[payload ++ '-result']"/>
          </otherwise>
      </choice>
  </parallel-foreach>
  <error-handler>
      <on-error-continue type="COMPOSITE_ROUTING">
          <!-- This will have the error thrown by the above processor -->
          <logger message="#[error.errorMessage.payload.failures['0']]"/>
          <!-- This will be a null value -->
          <logger message="#[error.errorMessage.payload.failures['1']]"/>
          <!-- This will be a null value -->
          <logger message="#[error.errorMessage.payload.results['0']]"/>
          <!-- This will have the result of this (correctly executed) route -->
          <logger message="#[error.errorMessage.payload.results['1']]"/>
      </on-error-continue>
  </error-handler>

</flow>
```

#### Throws

- `MULE:COMPOSITE_ROUTING`

### Differences between For Each and Parallel For Each Scopes

Both For Each and Parallel For Each split the defined collection, and the
components within the scope process each element in the collection. Also, in
both cases, each route runs with the same initial context. The difference
between these two scopes are:

- For Each works sequentially, while the Parallel For Each processes in parallel.
This difference affects _error handling_:
Because of the processing differences, the execution of For Each execution is
interrupted when an error is raised (and the Error Handler is invoked), while
Parallel For Each processes every route before invoking the Error Handler with a
`MULE:COMPOSITE_ROUTE` error type.
- For Each does not modify the payload, while the Parallel For Each outputs a
collection of the output messages from each iteration.

## Until Successful Scope

The Until Successful scope executes processors within it, in order, until they
all succeed or the scope exhausts the maximum number of retries.
Until Successful runs synchronously. If any processor
within the scope fails to connect or to produce a successful result,
Until Successful retries all the processors within it, including the one that failed, until all configured retries
are exhausted. If a retry succeeds, the scope proceeds to the next
component. If the final retry doesn't succeed, Until Successful produces an error.

Routing is successful if no exception is raised
or if the response matches an expression.

Common processes that use Until Successful include:

- Dispatching to outbound endpoints, for example, when calling a remote web service that might have availability issues.
- Executing a component method, for example, when executing on a Spring bean that may depend on unreliable resources.
- Using a sub-flow to re-execute several actions until they all succeed.

### Until Successful Scope Configuration

To configure an Until Successful scope, add the `<until-successful>` XML element inside an application flow.

You can configure the following attributes in the Until Successful scope:

| Field | XML | Description |
|---|---|---|
| Max Retries | `maxRetries` | Specifies the maximum number of retries that are allowed. This attribute can be either a number or an expression that resolves to a number. An error message looks like this: `Message: 'until-successful' retries exhausted.` The Mule error type is `MULE:RETRY_EXHAUSTED`. |
| Milliseconds Between Retries | `millisBetweenRetries` | Specifies the minimum interval, in milliseconds, between retries. The actual interval depends on the duration of the previous attempt, but it shouldn't exceed twice this value. The default is `60000` (one minute). This attribute can be either a number or an expression that resolves to a number. |

### Example Configuration of the Until Successful Scope

The following XML example configures a flow triggered by a Scheduler component and an Until Successful scope that executes an FTP Write operation:

```xml
<!-- FTP Connector config-->
<ftp:config name="FTP_Config" doc:name="FTP Config" >
  <ftp:connection workingDir="${ftp.dir}" host="${ftp.host}" />
</ftp:config>

<flow name="untilSuccessfulFlow" >
  <!-- Scheduler component to trigger the flow-->
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="15" timeUnit="SECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <!-- Until Successful scope-->
  <until-successful maxRetries="5" doc:name="Until Successful" millisBetweenRetries="3000">
    <!-- FTP Write operation that executes as part of the Until Successful Scope -->
    <ftp:write doc:name="Write" config-ref="FTP_Config" path="/"/>
  </until-successful>
  <logger level="INFO" doc:name="File upload success" message="File upload success"/>
  <!-- Error Handler at flow level-->
  <error-handler>
    <on-error-continue enableNotifications="true" logException="true" doc:name="On Error Continue" type="RETRY_EXHAUSTED">
      <logger level="INFO" doc:name="File upload failed" message="File upload failed"/>
    </on-error-continue>
  </error-handler>
</flow>
```

Behavior of the example application:

- If the FTP Write operation fails
The Until Successful scope retries the operation every `3000` milliseconds until the operation succeeds, with a limit of `5` retries. If the last execution fails, the scope throws a `MULE:RETRY_EXHAUSTED` error. Then, the `<on-error-continue>` handles the error and executes the Logger with the message: `File upload failed`.
Before throwing `MULE:RETRY_EXHAUSTED`, Mule also logs each unsuccessful attempt to retry execution of the processors on the Mule event, for example:
```text
ERROR 2022-12-09 17:41:44,910 ... event: cdad31c0-782b-11ed-af21-147ddaaf4f97] 
...UntilSuccessfulRouter: Retrying execution of event, attempt 1 of 5.
...
ERROR 2022-12-09 17:41:55,079 ... event: cdad31c0-782b-11ed-af21-147ddaaf4f97] 
...UntilSuccessfulRouter: Retrying execution of event, attempt 5 of 5.
```

- If the FTP Write operation executes successfully in any of the attempts
The next processor after the Until Successful scope executes, in this case, the Logger showing the message: `File upload success`.

### Variable Propagation

Every execution of the Until Successful scope starts with the same variables and values present before the execution of the block. New variables or modifications to already-existing variables while processing one element aren't visible in the next execution (in case there is an error). If the execution finishes correctly, the variables (and payload) are propagated to the rest of the flow.

### See also

- How Transactions Affect Scopes and Routers

## Async Scope

The Async scope is a branch processing block that executes simultaneously with the main flow. The main flow continues to execute while it initiates and processes the Async scope. The flow does not have to pause until the last message processor embedded in the asynchronous flow has completed its task.

Async can be useful for executing time-consuming operations that do not require you to send a response back to the initiating flow (such as printing a file or connecting to a mail server).

To facilitate simultaneous branch processing, the Async scope sends one copy of the message it has received to the first embedded message processor in its own processing block. At the same time, it sends another copy of the message to the next message processor in the main flow.

Because the Async scope is executed in a "fire and forget" manner, the result of the processing within the scope is not available in the main flow.

### Async Configuration

Async scopes are configurable.

| Field | Description |
|---|---|
| Display Name (`name`) | Name for the Async scope. |
| Max Concurrency (`maxConcurrency`) | Optional. Sets the maximum number of concurrent messages that the scope can process. By default, the container thread pool determines the maximum number of threads to use to optimize the performance when processing messages. When the scope is processing the maximum number of concurrent messages, it cannot receive additional requests. Set `maxConcurrency` to `1` to cause the scope to process requests one at a time. See Back-Pressure Management for details about Mule behavior after reaching the maximum concurrency value. |

### Async Scopes versus Subflows

Unlike a subflow, an Async scope:

- Does not inherit the exception strategy of the main flow.
To handle errors in an Async scope, use the Try scope.
- Processes messages asynchronously.
- Does not pass data back to the main flow.
- Exists inline with the main flow thread.
- Is not called by a Flow Reference component.
- Is not reusable

Note that even though the Async scope receives a copy of the Mule message, the payload is not copied. The same payload objects are referenced by both Mule messages: One that continues down the original flow, and the one processed by the Async scope.

In other words, if the payload of your message is a mutable object (for example, a bean with different fields in it) and a message processor in your Async scope changes the value of one of the fields, the message processors outside of the Async scope see the changed values.

### Example Async Scope Configuration

The following XML fragment shows an example configuration of an Async scope inside an application flow. The Async scope contains a `file:read` operation that executes asynchronously once triggered, while the application continues processing the next operation in the flow, `http:request`:

```xml
<!-- Main application flow -->
<flow name="myMainFlow" >
  <!-- HTTP Listener as event source -->
  <http:listener doc:name="Listener" />
  <!-- A Transform operation that executes as part of the main flow -->
  <ee:transform doc:name="Transform Message" >
    <ee:message >
      <ee:set-payload >
        <![CDATA[%dw 2.0
        output application/json
        ---
        payload]]>
      </ee:set-payload>
    </ee:message>
  </ee:transform>
    <!-- The Async scope executes its message processors in a different thread, while the main flow continues its execution -->
    <async doc:name="Async" >
      <!-- A Try scope to handle errors, because the async scope does not inherit the error strategy from the flow -->
      <try doc:name="Try" >
        <!-- A Write operation -->
        <file:write doc:name="Write" path="/" />
        <!-- Error handling strategy defined in the Try scope, to handle errors during the Async scope execution -->
        <error-handler >
          <on-error-continue enableNotifications="true" logException="true" doc:name="On Error Continue" type="ANY">
            <!-- Some error handling logic for this strategy -->
            ...
          </on-error-continue>
        </error-handler>
      </try>
    </async>
  <!-- This HTTP Request operation starts executing without waiting for the Async scope to finish its execution -->
  <http:request method="GET" doc:name="Request" />
  ...
</flow>
```

## Try Scope

The Try scope enables you to handle errors that may occur when attempting to execute any of the components inside the Try scope. It also supports transactions. A Try scope wraps one or more operations, then catches and handles any exceptions that might be thrown by any of these enclosed operations. The behavior is as if you extracted those enclosed event components into a separate flow with its own error handling strategy, but inline, without having to actually define a new flow.

### Error Handling with the Try Scope

When designing your flow, try to group those operations that are likely to experience errors inside a Try scope. The Try scope enables you to isolate potentially troublesome operations in your flow and assign them an error-handling method. You can also configure the operations inside the Try scope to be processed as a transaction.

The Try scope has an error handling strategy that you configure in the same way you configure error handling for a flow.

The Try scope can distinguish among various error type conditions and apply different behaviors. If an error is raised by a component inside a Try scope, then the Try scope's error handler is executed. At this point, the error is available for inspection, so the handlers can execute and act accordingly:

- On Error Continue
Executes and sends the result of the execution to its container Try scope, which uses that result to complete the execution successfully. Any transactions at this point are also committed.
- On Error Propagate
Rolls back any transactions, then executes and uses that result to re-throw the existing error, causing its container Try scope's execution to fail.

Example Try Scope Configuration

In the previous example, any database connection errors (`DB:CONNECTIVITY`) are propagated because of the On Error Propagate (`on-error-propagate`) error handler. Propagation of this error causes the Try scope's execution to fail and the flow’s error handler to execute. Other errors are handled through the On Error Continue (`on-error-continue`) error handler, so the Try scope's execution is treated as successful when they occur, meaning that the next operation, an HTTP request, continues its execution.

If the Try scope has several components, then after a component raises an exception, subsequent components in the Try scope are not executed, regardless of the type of error handler that catches the exception. In the case of On Error Propagate, the error is propagated to the flow's error handler, as if the Try scope did not exist. In the case of On Error Continue, processing continues outside the Try scope at the next flow component, as if the Try scope never threw an exception.

### Handling Transactions

A transaction is a series of actions that should never be partially executed. Configure a Try scope so that it is a set of operations that are considered one unit that either succeeds or fails, depending on whether errors are propagated and the transaction rolled back, or handled and the transaction committed. In either case, the process flow in which the Try scope resides continues.

The Try scope treats child operations as a transaction when the Transactional Action (`transactionalAction`) is set to `ALWAYS_BEGIN` or `BEGIN_OR_JOIN`. It can be configured in the following ways:

- Ignore (`INDIFFERENT`)
Default. If a transaction is active, the scope joins it. If not, the scope does not create a transaction.

- Always Begin (`ALWAYS_BEGIN`)
A new transaction is started every time the scope is executed.

- Begin or Join (`BEGIN_OR_JOIN`)
Relevant only when execution order might vary (for example, due to asynchronous actions occurring outside the flow).
If current flow processing has already started a transaction, the scope joins it. If not, the scope initiates a new transaction.

#### Analyzing Different Transactional Actions in Try Scope

The following example shows a `jms:listener` operation configured to initiate a transaction at flow level, a Try scope that tries to initiate or join the transaction (depending on its configuration), and a `jms:publish` operation configured to run outside of the transaction:

```xml
<flow name="someFlow">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<!-- Processors -->
	<try transactionalAction="${action}">
		<!-- Processors -->
		<!-- Join if possible is the default value for jms:publish operation -->
		<jms:publish config-ref="JMS_Config" destination="test.out" transactionalAction="NOT_SUPPORTED"/>
		<raise-error type="APP:SOME"/>
		<!-- More Processors -->
	</try>
	<!-- Processors -->
</flow>
```

If the operations within the Try scope do not produce an error, the scope finishes the execution and commits the transaction, independently of the configured `transactionalAction` value.

The transaction and the messages are handled differently when a `<raise-error/>` component is added, depending on the `transactionalAction` of the Try scope:

- Ignore (`INDIFFERENT`)
In this case, the transaction continues while executing the operations inside the Try scope. When the error is raised, it is propagated to the source (which does not handle it with an `<on-error-continue>` error handler). The transaction is rolled back, and the message is available again in the JMS queue. This rollback does not affect the completed `jms:publish` operation, which was outside of the transaction scope because `transactionAction` was set to its default, `NOT_SUPPORTED`.
Had `transactionAction` been set to `JOIN_IF_POSSIBLE`, the `jms:publish` operation would have been rolled back.
- Always Begin (`ALWAYS_BEGIN`)
This raises an error because an active transaction already exists.
- Begin or Join (`BEGIN_OR_JOIN`)
In this case, a transaction was already initiated so the scope joins the active transaction. The result is the same as in `INDIFFERENT`.

##### Error Handler at Flow Level

In the following example, an error handler is added at flow level:

```xml
<flow name="someFlow">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<!-- Processors -->
	<try transactionalAction="${action}">
		<!-- Processors -->
		<!-- Join if possible is the default value for jms:publish operation -->
		<jms:publish config-ref="JMS_Config" destination="test.out"/>
		<raise-error type="APP:SOME"/>
		<!-- More Processors -->
	</try>
	<!-- Processors -->
	<error-handler>
		<on-error-continue/>
	</error-handler>
</flow>
```

The behavior in this example is:

- Ignore (`INDIFFERENT`)
The transaction continues. Because the error is handled by an `on-error-continue` error handler, the transaction is committed. The message read from the `jms:listener` source is consumed, and the message processed by the `jms:publish` operation is actually sent.
- Always Begin (`ALWAYS_BEGIN`)
Raises an error because an active transaction already exists.
- Begin or Join (`BEGIN_OR_JOIN`)
Displays the same behavior as `INDIFFERENT`.

##### Error Handler Inside the Try Scope

In this case, the error handler is inside the Try scope and the error occurs after the execution of the scope:

```xml
<flow name="someFlow">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<!-- Processors -->
	<try transactionalAction="${action}">
		<!-- Processors -->
		<!-- Join if possible is the default value for jms:publish operation -->
		<jms:publish config-ref="JMS_Config" destination="test.out"/>
		<!-- More Processors -->
		<!-- There could be a component that raises an error, it will be handled by the error handler -->
		<error-handler>
			<on-error-continue/>
		</error-handler>
	</try>
	<!-- Processors -->
	<raise-error type="APP:SOME"/>
</flow>
```

Depending on the configured `transactionalAction`, the behavior in the Try scope is one of the following:

- Ignore (`INDIFFERENT`)
The transaction continues but the error is not handled by an `on-error-continue` at the flow level, causing the transaction to be rolled back, and the message to not be sent.
- Always Begin (`ALWAYS_BEGIN`)
Raises an error because an active transaction already exists.
- Begin or Join (`BEGIN_OR_JOIN`)
Displays the same behavior as `INDIFFERENT`.

#### Configuring Local or XA Transactions

In addition to configuring the Transactional Action, you can also configure the Transaction Type to be Local (single Resource) or XA Transaction.

The Try scope uses the Transaction Type configuration only when a new transaction is created. The type cannot change while a transaction executes.

For each Transactional Action, the behavior changes:

- Ignore (`INDIFFERENT`)
The Transaction used is the one already created (if there is one). This means that setting the Transactional Type makes no difference for this Transactional Action.
- Always Begin (`ALWAYS_BEGIN`)
The Transaction created is of the type set in the Transaction Type configuration. Remember that `ALWAYS_BEGIN` is an invalid configuration when already running within a Single Resource transaction.
- Begin or Join (`BEGIN_OR_JOIN`)
If there is a Transaction already created, then the Transactional Type makes no difference, as in the case of `INDIFFERENT`. If there is no Transaction, it creates one of the Type configured in Transaction Type, as in the case of `ALWAYS_BEGIN`.

### Variable and Payload Propagation

Every payload modification or variable addition, modification, or removal is propagated through the rest of the execution. This propagation includes modifications that take place inside the error handlers.

## Cache Scope

The Cache scope is for storing and reusing frequently called data. You can use a Cache scope to reduce the processing load on the Mule instance and to increase the speed of message processing within a flow. It is particularly effective for these tasks:

- Processing repeated requests for the same information.
- Processing requests for information that involve large repeatable streams.

When a message processor in a Mule app sends a message to the Cache scope, the parent flow expects an output. The Cache scope processes the message payload, delivers the output to the parent flow, and saves the output (that is, caches the response). The next time the Cache scope receives the same kind of message payload, the scope can offer a cached response rather than invoking a potentially time-consuming process again.

For instance, you can use a Cache scope to manage customer requests for flight information. Many customers might request the same pricing information about flights from San Francisco to Buenos Aires. Rather than using a lot of processing power to send separate requests to several airline databases with each customer query, you can use a Cache scope to arrange to send a request to the databases fewer times – say, once every ten minutes – and present users with the cached flight pricing information. Where timeliness of data is not critical, Cache scope can save time and processing power.

Note that you can put any number of message processors (such as connectors or components) into a Cache scope and configure the caching strategy to store the responses (which contain the payload of the response message) produced by the processing that occurs within the scope.

The cache scope also works in clustered environments because the object store configured in the caching strategy is shared across all nodes in the cluster.

### Caching Process

The Cache scope caches repeatable streams. It does not cache nonrepeatable streams, which can be read only once before they are lost. By default, all streams are repeatable in Mule unless a component's streaming strategy is configured to be nonrepeatable.

In general, the caching process follows this sequence:

1. A message enters the Cache scope.
1. The Cache scope determines whether the message payload is nonrepeatable.
1. The Cache scope generates a key to identify the message’s payload.
By default, Mule uses an SHA256KeyGenerator and a SHA256 digest to generate a unique key for the message payload. However, you can set up your own key through a custom caching strategy.
1. The Cache scope compares the newly generated key to cached responses that it has previously processed and saves it in the ObjectStore you set up (recommended) or in the default `InMemoryObjectStore`.
- If there is no cached response event (a _cache miss_), the Cache scope processes the new message and produces a response.
It also saves the resulting response in the object store (if the response is repeatable).
- If there is a cached response event (a _cache hit_), the caching strategy generates a response that combines data from both the new request and the cached response.
Note that if the generated response is a nonrepeatable stream, the scope does not cache the response.
1. The Cache scope pushes the response out into the parent flow for continued processing.

### Caching Strategy

A caching strategy defines the actions a Cache scope takes when a message enters its sub-flow. By default, the Cache scope uses a caching strategy that stores data in an in-memory object store. You can create a custom caching strategy that references an existing object store, or you can create a new custom object store to use in this caching strategy.

You can configure the cache size, expiration time, and maximum allowed entries by setting these values in the object store that you define or reference from the caching strategy. You can also configure a caching strategy to synchronize access to the cache, to avoid different message processors from using the cache at the same time.

Your caching strategy can also reference these customizations:

- Event Key for the ObjectStore, which is a DataWeave expression or Java object used to create the key to use for storing the payload in the ObjectStore.
- Response Generator for your strategy, which is a reference to a Java object that is used to create the responses returned by the caching strategy.
- Event Copy Strategy for mutable or immutable data.
REMOVED:
- Consumable Message Filter, which is a reference to a Java object that is used to determine whether a message contains a consumable payload.

### Filters

Instead of processing all message payloads that it receives, the Cache scope can exclude specific payloads from the Cache scope flow based on an DataWeave expression.

### Example

In Anypoint Studio, you can download and open the example project _Cache Scope with Salesforce Contacts_ from Anypoint Exchange to learn more about how to use the Cache scope. This example caches fetched data from Salesforce. When a query is issued to request the data again, results are returned from cache and a new call to Salesforce is not made.

To download and open this example project while you are in Anypoint Studio, click the Exchange icon in the upper-left corner. Then, in the window that opens, log into Anypoint Exchange and search on the name of the project.

## Set Up a Caching Strategy

You can create a caching strategy from a Cache scope properties panel or a Global Elements configuration in Anypoint Studio. After you create a strategy, a Cache component in your flow can reference it.

You can configure the cache size, expiration time, and maximum allowed entries by setting these values in the object store that you define or reference from the caching strategy.

Follow these steps to configure a caching strategy:

1. Open the caching strategy configuration window.
You can open it from the Cache scope properties panel or the **Caching Strategies** option in the Global Elements tab within Studio:

1. Define the **Name** of the caching strategy.
1. Define the **ObjectStore** to use by selecting any of the following options:
  - **Edit Inline** +
Use this option to create an Object Store configuration specific for this caching strategy.
  - **Global Reference** +
Use this option either to select an existing Object Store, or to create a new global Object Store that can be referenced by this caching strategy and any other component in your application.
1. Select a mechanism for generating a key used for storing events within the caching strategy:
- **Default**
- **Key Expression**
A DataWeave expression (for example, `keyGenerationExpression="#[vars.requestId]"`).
Note that for two requests that are the same ("equal"), you need to generate the same key. Otherwise, you can get wrong results.
- **Key Generator**
Requires you to implement the `com.mulesoft.mule.runtime.cache.api.key.MuleEventKeyGenerator` interface.
1. (Optional) Open the **Advanced** tab in the properties window to configure advanced settings:

- Select or create a **Response Generator**.
Note that this step requires that you implement the
`com.mulesoft.mule.runtime.cache.api.response.ResponseGenerator` interface.
- Select the **Event Copy Strategy**:
  - **Simple event copy strategy**
Data is immutable. This is the default value.
  - **Serializable event copy strategy**
Data is mutable.

### Synchronized Access to a Cache

By default, Mule synchronizes access to a cache to avoid unexpected results if multiple message processors (on the same or different Mule instances) use the cache at the same time.

Consider a scenario where two message processors attempt to retrieve a value from a cache but do not find the value in the cache. So each message processor calculates the value independently and inserts it into the cache. If access to the cache is not synchronized, the value inserted by the second message processor overwrites the value inserted by the first message processor. If the values are different, then two different results are obtained for the same input, with only the last one stored in the cache.

In some scenarios this outcome is valid, but it can be a problem if the application requires cache coherence. Synchronizing the caching strategy ensures this coherence. A synchronized cache is locked when it is being modified by a message processor. In the previous scenario, a locked cache forces the second message processor to wait until the first message processor has calculated the value, and then it retrieves the value from the cache.

You can disable cache synchronization by defining the `synchronized` property in the `<ee:object-store-caching-strategy>` element and setting it to `false`.

Synchronization affects performance, and the impact is most severe in cluster mode.

### Example Caching Strategy

The following XML snippet shows the configuration of a caching strategy that synchronizes access to the cache, and defines a persistent Object Store to store the cached responses. The caching strategy is then referenced by a Cache scope:

```xml
<!-- Caching strategy definition -->
<ee:object-store-caching-strategy name="Caching_Strategy" doc:name="Caching Strategy">
  <!-- Object Store defined for the caching strategy-->
  <os:private-object-store
    alias="CachingStrategy_ObjectStore"
    maxEntries="100"
    entryTtl="10"
    expirationInterval="5"
    config-ref="ObjectStore_Config" />
</ee:object-store-caching-strategy>

<!-- Cache scope referencing the strategy-->
<ee:cache doc:name="Cache" cachingStrategy-ref="Caching_Strategy">
      <!-- Some processing logic to cache-->
</ee:cache>
```

## Idempotent Message Validator

The Idempotent Message Validator ensures that only unique messages continue through a flow's execution by checking the unique ID of the incoming message. You can use any incoming attribute of the Mule message as an ID, or you can compute the ID by configuring a DataWeave expression. You can also use the DataWeave `Crypto` functions to compute hashes (SHA, MD5) from the data.

### Message Hashing

DataWeave enables you to import the `Crypto` library to execute hashing functions. Calculating a hash can be useful when you want to compute a unique ID for the Mule message. For example, if you want to get an MD5 hash from the payload and use it as the ID, open the Idempotent Message Validator properties in Anypoint Studio and set **ID Expression** (`idExpression` in XML) to the following DataWeave expression:

```text
#[
    %dw 2.0
    output text/plain
    import dw::Crypto
    ---
    Crypto::hashWith(payload,'MD5')
]
```

### Examples

- The following example shows an Idempotent Message Validator configured to extract the query parameter `id` from the HTTP request and use that value as a unique identifier to filter the message:
```xml
<flow name="myFlow">
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/"/>
  ...
  <idempotent-message-validator doc:name="Idempotent Message Validator" idExpression="#[attributes.queryParams.id]"/>
  ...
</flow>
```

- The next example shows an Idempotent Message Validator configured to hash the payload using a DataWeave expression, store the result in a persistent object store, and then use the processed message IDs as the unique identifier to filter the message:
```xml
<flow name="myFlow">
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/"/>
  ...
  <idempotent-message-validator doc:name="Idempotent Message Validator" idExpression="
    #[%dw 2.0
      import dw::Crypto
      output application/octet-stream
      ---
      Crypto::hashWith(payload,'MD5')]">
    <os:private-object-store alias="privateObjectStore"
       entryTtl="1"
       entryTtlUnit="MINUTES"
       maxEntries="10" />
  </idempotent-message-validator>
  ...
</flow>
```

### Parameter Reference

| Name | Type | Description | Default Value | Required |
|---|---|---|---|---|
| ID Expression | Expression | The expression Mule uses to generate the ID. You can use a DataWeave function to calculate the ID, or you can extract the ID from any existing value of the Mule message. | `#[correlationId]` | No |
| Value Expression | Expression | This parameter is not used. Setting a value has no effect. | `#[correlationId]` | No |
| Object Store | Object Store | Either a name to reference a global object store or a definition of a private object store where the component stores the processed message IDs. | Object Store created by the Object Store Manager. Not persistent, with an entry TTL of 5 MINUTES and an expiration interval of 6 SECONDS. | No |
| Store Prefix | String | Defines the prefix of the object store names. This value is used only for the internally built object store. | _configFileName_._flowName_.IdempotentMessageValidator | No |

#### Throws

- `MULE:DUPLICATE_MESSAGE`
