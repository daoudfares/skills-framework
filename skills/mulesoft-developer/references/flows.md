# Flows, events and the things that travel through them

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Mule Event Structure

A Mule event contains the core information processed by the runtime, including the message payload, attributes, and variables. It travels through components inside your Mule app following the configured application logic. Understanding Mule events helps you design flows that process and transform data effectively.

The Mule event is immutable, so every change to an instance of a Mule event results in the creation of a new instance.

A Mule event is composed of two objects:

- A Mule Message contains a message payload and its associated attributes.
- Variables are Mule event metadata that you use in your flow.

A Mule event source triggers the generation of a Mule event and dispatches that event to the flow. Event sources include triggers such as the Scheduler and listeners such as the HTTP Listener and On New or Updated File components.

This sequence shows how a Mule event flows through your application:

1. A trigger reaches the event source.
1. The event source produces a Mule event.
1. The Mule event travels sequentially through the components of a flow.
1. Each component interacts in a pre-defined manner with the Mule event.

In some cases when an issue occurs in an event source, the component doesn't produce a Mule event. For example, invalid or incorrect paths in an HTTP listener configuration prevent the creation of a Mule event. Connectors log such issues in ERROR, WARN, or INFO messages.

## Mule Message Structure

A Mule message is the part of the Mule event that serves as a container for message content and metadata, typically from external sources, as it is processed within flows of a Mule app.

The Mule message is immutable, so every change to a Mule message results in the creation of a new instance. Each processor in a flow that receives a message returns a new Mule message consisting of these parts:

- A message `payload`, which contains the body of the message. For example: the content of a file, the HTTP body, a record from a database, or the response to a REST or Web Service request.
- Message `attributes`, which are metadata associated with the payload, such as HTTP headers and query parameters.

A Mule event source triggers a process that creates a Mule event with a Mule message and executes the Mule flow that contains the event source. For example, this process begins each time an HTTP Listener source receives a request or the Scheduler executes.

After the flow begins its execution, downstream processors (such as Core components, File read operations, or the HTTP request operation) can then retrieve, set, and process Mule message data (payload and attributes) that reside in the Mule event according to their configurations.

Note that in Anypoint Studio, the DataSense Explorer shows the structure of a Mule message at any given point of the flow.

### Message Payload

The message payload contains the content or body of a message. For example, the payload can contain the results of an HTTP request, the content of records you retrieve through the Select operation of the Database connector, or the content of a file that you retrieve through a Read operation to the File or FTP connector.

The payload content changes as it travels through a flow when message processors in a Mule flow set it, enrich it, transform it into a new format, extract information from it, or even store it in a Mule event variable and produce a new payload.

You can select the payload of a Mule message through a DataWeave expression that uses the Mule Runtime variable, `payload`.

For example, a Logger component configured to display the `payload` of a response to an HTTP request for the JSON content at `https://jsonplaceholder.typicode.com/users` outputs the following example JSON content in the Studio console:

**Example: HTTP Response Payload**

```text
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    }
  },
  {
    "id": 2,
    "name": "Ervin Howell",
    "username": "Antonette",
    "email": "Shanna@melissa.tv",
    "address": {
      "street": "Victor Plains",
      "city": "Wisokyburgh",
      "zipcode": "90566-7771",
      "geo": {
        "lat": "-43.9509",
        "lng": "-34.4618"
      }
    }
  }
]
```

A Logger component set to display the `payload` for the output of a File Read operation for a simple JSON file can output the following example JSON content in the Studio console:

**Example: File Payload**

```text
{ "hello" : "world" }
```

The next message processor in the flow can then act on this payload, for example, by selecting the value of the JSON object in the payload with `payload.'hello'` to replace the preceding JSON payload with the string, `"world"`.

### Attributes

Attributes contain the metadata associated with the body (or payload) of the message. The specific attributes of a message depend on the connector (such as HTTP, FTP, File) associated with the message. Metadata can consist of headers and properties received or returned by a connector, as well as other metadata that is populated by the connector or through a Core component, such as Transform Message.

You can select attributes of a Mule message through a DataWeave expression that uses the Mule Runtime variable, `attributes`.

For example, when using the `attributes` variable to display HTTP response metadata through a Logger component, the Studio console outputs the following example HTTP response attributes:

**Example: HTTP Response Attributes**

```text
{
   Status Code=200
   Reason Phrase=OK
   Headers=[
      date=Sun, 20 Jan 2019 19:13:51 GMT
      content-type=text/html;
      charset=UTF-8
      transfer-encoding=chunked
      connection=keep-alive
      set-cookie=__cfduid=d03462713a0b2c57c8d2ad3bf311287041548011631;
      expires=Mon, 20-Jan-20 19:13:51 GMT;
      path=/;
      domain=.typicode.com;
      HttpOnly
      x-powered-by=Express
      vary=Origin, Accept-Encoding
      access-control-allow-credentials=true
      cache-control=public, max-age=14400
      last-modified=Tue, 15 Jan 2019 18:17:15 GMT
      via=1.1 vegur
      cf-cache-status=HIT
      expires=Sun, 20 Jan 2019 23:13:51 GMT
      expect-ct=max-age=604800,
      report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
      server=cloudflare
      cf-ray=49c3dc570c2f281c-SJC
   ]
}
```

The example is a response from an HTTP Request operation to the web page `https://jsonplaceholder.typicode.com/users`.

Notice that each attribute is a key-value pair separated by an equal sign (`=`). When using a connector or component (such as the Logger) in your flow, you can use the `attribute` variable with specific attributes and their inner attributes to select the attribute values that you require, such as the status code or content type. For example, you can select the values of attributes in an HTTP response using the following syntax:

- `attributes.statusCode` to select an HTTP status code like `200`.
- `attributes.headers.date` to select `Sun, 20 Jan 2019 18:54:54 GMT` from the header of an HTTP response.
- `attributes.headers.'content-type'` to select the HTTP content type `application/json`.
To select the value of inner attributes like `content-type`, you must surround the name `content-type` in quotes. You do not need quotes around values like `date` because DataWeave applies the rules described in valid identifiers to inner values. To understand why you use `statusCode` for the selector instead of `'Status Code'` or `"Status Code"` to select the status code value, see the note in that section.

For file metadata, the attributes are different. For example, when using the `attributes` variable to display file metadata through a Logger component, the Studio console displays the following example content:

**Example: File Attributes**

```text
LocalFileAttributes[
  lastModifiedTime=2019-01-20T08:17:55,
  lastAccessTime=2019-01-20T10:54:55,
  creationTime=2019-01-20T08:17:55,
  size=22,
  regularFile=true,
  directory=false,
  symbolicLink=false,
  path=/Users/me/Desktop/myJson.json,
  fileName=myJson.json
```

Notice that each attribute is a key-value pair (such as `fileName=myJson.json`). You can select the value of an attribute by referencing its key, for example:

- `attributes.'fileName'` to return the file name: `myJson.json`.
- `attributes.size` to return the size of the file: `22`.

#### Valid Identifiers for Attribute Names

You can access and declare attribute names that follow the rules described in Rules for Declaring Valid Identifiers without using any quotation marks.

To use an attribute name that is not a valid identifier, surround the attribute name with any of the following characters:

- Single quotation marks (`'`)
- Double quotation marks (`"`)
- Backticks (```)

For example, consider the following DataWeave variable declaration:

```java
var myVar = {
              id : "1234",
              "123 abc !@#" : "some_value"
            }
```

Because attribute name `123 abc !@#` is not a valid identifier, you must use quotation marks or backticks to declare it.

To access the value from attribute `123 abc !@#`, which is `"some_value"`, use quotation marks or backticks:

```text
myVar.'123 abc !@#'
```

Using quotation marks or backticks to declare an attribute or select a value from an attribute when the attribute name is a valid identifier is optional.

In the previous variable declaration example, attribute `id` is declared without using any quotation marks. To access the value stored in attribute `id`, you can use any of the following methods:

- `myVar.id`
- `myVar.'id'`
- `myVar."id"`
- `myVar.`id``

Note that human-readable names, such as `Status Code`, that you see in console output for top-level attributes can differ from the name to use for selecting the attribute, which is `statusCode`. Putting quotes around the human-readable name `Status Code` returns `null` instead of making that top-level attribute selectable. You can find the syntax to use for selecting the top-level attribute names, such as `Status Code`, `Reason Phrase`, and `Headers`, through autocompletion in Studio or in the connector documentation, for example, in HTTP Request documentation.

## Variables in Mule Apps

Variables are used to store per-event values for use within a flow of a Mule app. The stored data can be any supported data type, such as an object, number, or string. It is also possible to store the current message (using the `message` keyword), the current message payload (using the `payload` keyword) or just the current message attributes (using the `attributes` keyword). You can even use a DataWeave expression as the value. However, the keyword `vars` (for example, `vars.someOtherVar`) is not allowed.

You can create, or update, variables in these ways:

- Using the Set Variable component.
- Using a Target Variable from within an operation, such as the Read operation to the File connector or the Store operation to the Database connector.
- Using the DataWeave Transform Component (EE-Only)
- Using Scripting Component (in scripting module)

You can also delete/remove:

- Using the Remove Variable component.

After creating a variable, you can access and use it within the scope of a Mule flow where you created it, which includes any flows that are joined with it through a Flow Ref component.

- `vars`: Keyword for accessing a variable, for example, through a DataWeave expression in a Mule component, such as the Logger, or from an Input or Output parameter of an operation. If the name of your variable is `myVar`, you can access it like this: `vars.myVar`

Note that a variable in the Mule event is different from variables defined in a DataWeave script, which are local to the script and not accessible outside of it.

## Enrich Data with Target Variables

When creating a flow in a Mule app, you might need to store data in a variable so that any component in the flow can use it. Non-void operations (such as the Read operation to the File connector) can store the message data that they return in a variable. Once defined, variables created with the Target (`target`) parameter are available for use within the flow, and you can access them like you access any other variable.

You often define variables through these parameters:

- Target (`target`): Name of the variable in which you want to store message data. Names can only include numbers, characters, and underscores. For example, hyphens are not allowed in the name.
- Target Value (`targetValue`): Value of the data to store in the target variable. By default, the value is the message payload (`payload`). The field accepts any value that a variable accepts: any supported data type, DataWeave expressions, the keywords `payload`, `attributes`, and `message`, but _not_ the keyword `vars`.

### Considerations

- Setting a target variable changes the typical course of the message through the flow.
Normally, an operation outputs a different message than it receives as input:
However, when you set a variable from an operation, the operation outputs to the _next_ component in the flow the same message that it received as input. For example, assume you have a flow consisting of component A, followed by component B with a target value of `myMessage`, and then component C. In this case, component C receives the same message that B received from A:

- Configuring target variables affects the behavior of existing variables.
Existing variables retain their original values after an operation with a target variable finishes processing. For example, consider a flow where you set variables 1 and 2, and then an operation modifies variables 1 and 2 and also outputs a target variable A. In this case, after the execution of the operation, variables 1 and 2 return to their previous values:
1. Because the component sets a target variable, variable 1 and 2 revert to their previous values after the execution of the component.

- Target variables are not set when an error occurs.
Because the execution of the flow stops and does not end successfully when an error occurs, target variables are not set in this scenario.

### Target Variable Configuration Examples

The following example configures a Read operation that stores the payload of `readme.txt` in `myVar`:

```xml
<file:read path="readme.txt" target="myVar" />
```

Note that the target variable `myVar` stores the complete payload by default. You only need to specify a Target Value (`targetValue`) if you want to store a value different than the payload.

In this example, the entire message is stored in `myVar`:

```xml
<file:read path="readme.txt" target="myVar" targetValue="#[message]" />
```

In this case, the variable `myVar` contains the content of the file and also all the metadata related.

- Expression to access the file content: `#[myVar.payload]`
- Expression to access the file metadata: `#[myVar.attributes]`

In this example, only the file size is stored in `myVar`:

```xml
<file:read path="readme.txt" target="size" targetValue="#[attributes.size]" />
```

The following scenarios describe some cases where you might use target variables.

### Scenario: Setting a Target Variable from within an Operation

Assume that you want to log the entire message (payload and attributes) returned by a Database connector operation, such as Insert. Instead of using a Set Variable component after the operation, you can instead capture the message data by adding a target variable directly to the operation:

```xml
<db:insert config-ref="dbConfig" target="result" targetValue="#[message]">
    <db:sql>INSERT INTO PLANET(POSITION, NAME, DESCRIPTION) VALUES (777, 'Pluto', :description)</db:sql>
    <db:parameter-types>
        <db:parameter-type key="description" type="CLOB"/>
    </db:parameter-types>
    <db:input-parameters>
        #[{'description' : payload}]
    </db:input-parameters>
</db:insert>
```

- Target Variable for the Insert operation: `result`
- Target Value: `message` in Design Center, `#[message]` in Anypoint Studio.

Then you might retrieve the result from the Logger like this:

```xml
<logger level="INFO" doc:name="Logger" doc:id="8dca355c-a85c-44db-8c53-5b9c188a2431" message="Payload is: #[vars.result.payload] and attributes are: #[vars.result.attributes]"/>
```

- Message: `Payload is: #[vars.result.payload] and attributes are: #[vars.result.attributes]`

Assume that you want to log the name of the first entry in a planet database. You can define a target variable like this one through the Select operation of the Database connector:

```xml
<db:select config-ref="dbConfig" target="planetName" targetValue="#[payload[0].name]">
    <db:parameterized-query>select * from PLANET order by ID</db:parameterized-query>
</db:select>
```

- Target Variable for the Select operation: `planetName`
- Target Value: `payload[0].name` in Design Center, `#[payload[0].name]` in Anypoint Studio.

Then you might retrieve the result from the Logger like this:

```xml
<logger level="INFO" doc:name="Logger" doc:id="8dca355c-a85c-44db-8c53-5b9c188a2431" message="#['Planet name is: ' ++ vars.planetName]"/>
```

- Message: `'Planet name is: ' ++ vars.planetName`

### Scenario: Using the Stored Value as Input to an Operation

Assume that you want to access all planets discovered after a given planet was discovered. You might create a target variable called `discoveryDate` within a select operation to capture the a planet's discovery date.

```xml
<db:select config-ref="dbConfig" target="discoveryDate" targetValue="#[payload[0].discoveryDate]">
    <db:sql>select discoveryDate from PLANET where name = :name</db:sql>
    <db:input-parameters>
        #[{'name' : 'pluto'}]
    </db:input-parameters>
</db:select>
```

- Target Variable for the Retrieve operation: `discoveryDate`

Then you can use the Input parameter of another operation in your flow (such as the Select operation to the Database connector) to make the variable available for use in your query, for example:

```xml
<db:select config-ref="dbConfig" target="discoveryDate" targetValue="#[payload[0].discoveryDate]">
    <db:sql>select * from PLANET where discoveryDate > :discoveryDate</db:sql>
    <db:input-parameters>
        #[{'discoveryDate' : vars.discoveryDate}]
    </db:input-parameters>
</db:select>
```

- Input Parameter definition for the Select operation:
 ** Key: `discoveryDate`
 ** Value: `vars.discoveryDate` in Design Center, `#[vars.discoveryDate]` in Anypoint Studio.

### Scenario: Bypassing the Normal Message Flow

Assume that you want to insert a number of records into a database that are located in the messages's payload, then pass those same records on for further processing by the next component in your flow. Though you want to use the Bulk Insert operation to the Database connector to insert the records, the operation returns a success message that replaces the current payload, which makes the records inaccessible. So, to pass on the records to the next component instead of replacing the payload with the Bulk Insert result, you can store the success message in a target variable, for example:

- Target Variable: `bulkInsertResult`

Then the next operation in your flow can process the records located in the payload.

## Flows and Subflows

Mule apps process messages and other parts of Mule events through Mule
components, connectors, and modules that are set up within the scope of
Flow and Subflow components within an app.

An app can consist of a single flow, or it can break up processing into
discrete flows and subflows that you add to the app and connect together. Mule
apps in production environments typically use multiple flows and subflows
to divide the app into functional modules or for
error handling purposes. For example, one flow might
receive a record and transform data into a given format that another
flow processes in some special way.

You can connect and trigger their execution with Flow Reference
components or by using the DataWeave `lookup` function within expressions and
transformations. The function passes the current event to another flow for
further event processing. You can think of a Flow Reference as a function call that accepts an event as input and then returns the modified event.

### Using Flows

Flows can have Mule Sources (such as an HTTP listener receiving a request)
that trigger the execution of a flow. For cases where you do not want
a source to start a flow right away, you can configure your flow as
initially stopped and start it later through
Runtime Manager.

Like functions or methods in other programming languages, it is a best practice
to focus your flows on specific (perhaps reusable) activities, such as receiving
an API request from a web client, processing the event, then returning an
appropriate response. If the event processing gets complicated, or must call
out to other services, you might factor out that behavior into other flows.

### Using Subflows

A _subflow_ is a scope that enables you to group event processors in a manner similar to that of a flow, but with certain differences and limitations:

- Subflows do not have Mule event sources.
- Subflows do not have an error handling scope.
- During design, subflows work as macros that replace the Flow Reference components that call them. +
When you build the application, all Flow Reference components that call a subflow are replaced by the contents of the referenced subflow.
- Referencing subflows results in better performance than referencing a flow.

#### Limitations

Because the contents of a subflow replace each Flow Reference component that references that subflow, several instances of the event processors inside that subflow exist in the application at runtime. This behavior can cause issues with event processors that depend on unique IDs or instances to execute, such as batch processors.

For example, configuring a batch job inside a subflow causes the application to fail during deployment if the subflow is referenced from more than one Flow Reference component. The application fails to deploy because multiple instances of a batch job with the same job instance ID exist, which is not allowed.

### Error Handling

Each flow (but not subflow) can have its own error handling. One reason for
calling a flow through a Flow Reference component is to isolate the error
handling to different contexts. For example, a parent flow that receives web
client requests might define HTTP-related error handling. If the parent flow
then calls a JMS queue for further processing, you can put the JMS event
processors in a separate child flow and call that flow with a Flow Reference
component. This child flow can then define its own JMS-related error handling.
This practice is similar to the way you handle or propagate errors in other
programming languages, like Java.

Like a flow or subflow, a Try scope also groups
together a sequence of event processors with its own error handling. You can
place a Try scope inside a flow or subflow to isolate error handling inside a
flow without the need to create a separate flow or subflow. The trade-off
is that error handling through a Try scope occurs inline inside the flow,
which makes it harder to reuse between other flows or subflows.

In both cases, calling a flow or including a Try scope isolates the error
handling, similar to the use of Try-Catch blocks inside Java code. For
example, placing JMS queue event processing (described above) in its own
flow or within a Try scope results in exactly the same error handling
behavior, but the event processors in a Try scope cannot be called from
another flow.

### Branching Event Processing

Some scopes are available for a flow to branch event processing into separate
threads and to allow asynchronous processing of the event at a specific point
in the flow, for example, the Scatter-Gather and
Async scopes. A Choice
router enables you to change the downstream sequence of event processors based
on some condition.

## Flow and Subflow Scopes

toc::[]

Flow and Subflow scopes are components for grouping together a sequence of other
Core components and operations (provided by connectors and modules) to help
automate integration processes. The Flow component is fundamental to a
Mule app. Because all Mule apps must contain at least one flow, Anypoint
Studio automatically provides the first Flow component in
your Mule app.

A Mule app can contain additional flows and subflows, as this example shows:

**Example: Flow with Subflows**

For a more in-depth discussion of uses, capabilities, and limits of flows and
subflows, see Flows and Subflows.

Note that flows always function synchronously. If you need to achieve
asynchronous patterns, such as Fire-and-Forget, you can use the
Async Scope (`<async/>`).

### Flow Configuration

Flows are configurable. For example, you can set them to start or remained
stopped when the Mule app starts, place limits on the allowed concurrency, or set
up business events. You can also set up error handling for a component
(see error handling).

| Field | Description |
|---|---|
| Name (`name`) | Name for the flow. Flows automatically receive an editable name that matches (or partially matches) the project name. |
| Initial State (`initialState`) | Values: Started, Stopped. These are Mule runtime settings for the flow. The default, Started (`initialState="started"`, also called Empty in Studio), indicates that the flow is active when you start the app. So it can be triggered by an internal or external Mule event source within the flow (such as an HTTP listener or Scheduler), by a Flow Reference from another flow or subflow, or through a call to the lookup function. If you set the initial state to Stopped (`initialState="stopped"`), activate the flow after deployment. For hybrid standalone and Anypoint Platform PCE deployments, use Runtime Manager to activate the flow. For CloudHub and Anypoint Runtime Fabric deployments, flow management through Runtime Manager isn't supported. To activate the flow, redeploy the application or update the flow configuration to Started. When a flow is deployed with the initial state set to Stopped, the console output looks similar to this: `Flow flow_component_ex has not been started (initial state = 'stopped')`. [WARNING] ==== For CloudHub deployments, avoid setting `initialState="stopped"` on flows that contain a Scheduler. The scheduler gets stuck in a permanent "Running" state, and you can't manage it through Runtime Manager. ==== |
| Max Concurrency (`maxConcurrency`) | Optional. Sets the maximum number of concurrent messages that a flow can process. If not set, the container thread pool determines the maximum number of threads the flow can use to optimize the performance when processing messages. While the flow is processing the maximum number of concurrent messages, it cannot receive additional requests. Set `maxConcurrency` to `1` to cause the flow to process requests one at a time. See Back-pressure for details about Mule's behavior after the maximum concurrency value is reached. |
| Business Events | Optional: Defaults to `false`. For Mule apps that you deploy to CloudHub, you can enable business events (XML example: `tracking:enable-default-event="true"`) and add a Transaction ID (XML example: `<tracking:transaction id=12345`/>). See Business Events. |
| Metadata | As with many other components, you can set metadata for this component. For more on this topic, see the Studio document Metadata Editor. |

### Subflow Configuration

Subflow scopes provide a way to edit the name of the subflow and to add metadata. Unlike flows, subflows lack a built-in mechanism for setting up error handling, though you can use error handling provided by the Try Scope within a subflow if you need to perform error handling.

| Field | Description |
|---|---|
| Name (`name`) | Name for the subflow. Subflows automatically receive an editable name that matches (or partially matches) the project name. |
| Metadata | As with many other components, you can set up metadata for this component. For more on this topic, see the Studio document Metadata Editor. |

### XML for Flows and Subflows

This example shows the XML for a simple flow  (`<flow/>`) that uses a Scheduler as a source to trigger execution of
the flow every 10 seconds, and it connects to a subflow (`<sub-flow/>`) through a Flow Ref (`<flow-ref/>`) component. That
subflow then connects to another subflow, also using a Flow Ref component. Note
that when you configure components through the Studio UI, Studio automatically adds the XML to the Configuration XML for your Mule app.

**Example: XML for a Flow and Subflows**

```xml
<flow name="flow_component_ex">
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="10" timeUnit="SECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <ee:transform doc:name="Transform Message">
    <ee:message >
      <ee:set-payload ><![CDATA[
 %dw 2.0
 var myXml =  read('<prices>
    <basic>9.99</basic>
    <premium>53</premium>
    <vip>398.99</vip>
  </prices>', 'application/xml')
 output application/xml
 ---
 myXml
]]></ee:set-payload>
    </ee:message>
  </ee:transform>
  <flow-ref name="subflow_ex1"/>
</flow>
<sub-flow name="subflow_ex1">
  <ee:transform doc:name="Transform Message">
    <ee:message>
      <ee:set-payload><![CDATA[%dw 2.0
import * from dw::util::Timer
output application/json
var conversionRate=13
---
priceList: payload.prices mapObject(value, key, index) -> {
  (key) : {
       dollars: value,
       localCurrency: value * conversionRate,
       index_plus_1: index + 1,
       timer : currentMilliseconds()
   }
}]]>
      </ee:set-payload>
   </ee:message>
 </ee:transform>
 <flow-ref name="subflow_ex2"/>
</sub-flow>
<sub-flow name="subflow_ex2">
  <logger level="INFO" doc:name="Logger" message="#[payload]" />
</sub-flow>
```

The example produces the following output:

**Output**

```json
{
  "priceList": {
    "basic": {
      "dollars": "9.99",
      "localCurrency": 129.87,
      "index_plus_1": 1,
      "timer": 1533024312658
    },
    "premium": {
      "dollars": "53",
      "localCurrency": 689,
      "index_plus_1": 2,
      "timer": 1533024312659
    },
    "vip": {
      "dollars": "398.99",
      "localCurrency": 5186.87,
      "index_plus_1": 3,
      "timer": 1533024312659
    }
  }
}
```

### Error Handling

You can add error handlers to the Flow components (but not to subflows).

In Studio, you can simply expand the Error Handling area at the bottom of the Flow component and drag the error components into the flow. Note that this process automatically places the component into the Error Handler component, so there is no need to add the Error Handler component first.

Near the end of this XML example, the flow shows an On Error Continue configuration (`<on-error-continue/>`):

**Example: XML for Flow with On Error Continue Configuration**

```xml
<flow name="flow_subflowFlow" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="10" timeUnit="SECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <ee:transform doc:name="Transform Message" >
    <ee:message >
      <ee:set-payload ><![CDATA[
 %dw 2.0
 var myXml =  read('<prices></prices>', 'application/xml')
 output application/xml
 ---
 myXml
]]></ee:set-payload>
    </ee:message>
  </ee:transform>
  <logger level="INFO" doc:name="Logger" message='#[payload.prices]'/>
  <error-handler >
    <on-error-continue enableNotifications="true" logException="true" doc:name="On Error Continue" type="EXPRESSION" when="#[isEmpty(payload.prices)]">
      <logger level="ERROR" doc:name="Logger" message='"An Error Occurred"'/>
    </on-error-continue>
  </error-handler>
</flow>
```

The preceding example produces an error. Notice the following:

1. The variable `var myXml` in `<set-payload/>` configures an empty `<prices></prices>` tag as the payload.
1. The Logger beside the `<set-payload/>` component returns `null` because it is set to log the value of the empty tag.
1. The `<on-error-continue/>` component returns an error because the DataWeave condition `isEmpty(payload.prices)` returns `true`.
1. The Logger (`<logger/>`) within `<on-error-continue/>` configures an error message to print to the console when an error occurs. The resulting error message looks something like this:

```text
ERROR 2018-07-30 23:58:45,293 [[MuleRuntime].cpuLight.06:
 [flow_subflow].flow_subflowFlow.CPU_LITE @1b1529b2]
 [event: 0-2aba3280-948f-11e8-82d0-f45c898f2549]
 org.mule.runtime.core.internal.processor.LoggerMessageProcessor:
 "An Error Occurred"
```

For details about these components, see On-Error error handlers.

## Flow Reference Component

Flow Reference routes the Mule event to another flow or subflow, executes all processors in the referenced flow, and then routes the event back within the same Mule application. The following diagram shows the order of processing when one flow references another:

When the main flow is triggered, the Mule event travels through and executes the flow until the event reaches the Flow Reference. The event then travels through and executes the referenced flow from beginning to end, and then returns to the main flow.

This process enables you to treat the entire referenced flow like a single component in your current flow.

Flow Reference breaks the Mule application into discrete and reusable units. For example, a flow that lists files on a regular basis might reference another flow that processes the output of the List operation. Instead of appending all the processing steps to the flow that lists the files, you can append a Flow Reference that points to the processing flow.

### Configure a Flow Reference

To configure a Flow Reference component, follow these steps in Anypoint Studio:

1. Drag the Flow Reference component from **Mule Palette** to the point in your flow where you want to create the call to the referenced flow:

1. Open the Flow Reference properties and specify the flow you want to reference in **Flow name**:

Use actual flow names to define the **Flow name** (`name`) attribute. Using dynamic values (DataWeave expressions, variables) to specify the referenced flow negatively affects performance. Also, MUnit tests and application analyzing tools cannot work on dynamic references.

### Enrich Content with a Flow Reference Target Variable

Sometimes you need to execute a flow that uses the current payload and variables, but you want the Mule message to remain unchanged after such process. In this case, you can use a target variable to store the results of the referenced flow processing without changing the original message.

You can store the result of a Flow Reference call in a target variable by configuring the following fields in your Flow Reference properties:

- **Target**: Name of the variable that the Flow Reference creates to store the result of the processed message.
- **Target Value**: An expression that evaluates against the operation's output. The result of this evaluation is stored in the defined target variable.

#### Considerations when Using a Target Variable

Setting the `target` variable in a Flow Reference component causes the original message to remain unchanged. This means that any modification to the payload or to the variables that occur in the referenced flow revert after the referenced flow finishes executing its processors, returning the payload and variables to their original values.

Alternatively, if you do not define a `target` variable, any modification that occurs to the payload or to the variables in the referenced flow persist after the referenced flow finishes its execution, changing the original value of the payload or variables.

### Error Handling Behavior in Referenced Flows

When an error occurs inside a flow that is referenced by a Flow Reference component, the execution of the referenced flow stops and the process transfers to the referenced flow's error handler. If the referenced flow does not have a configured error handler, the error is propagated to the flow that contains the Flow Reference call so this flow's configured Error Handler component processes the error.

Target variables are not set when an error occurs because the execution of the flow stops and does not end successfully.

### XML Example of Flow Reference

The following XML code represents the project created in Configure a Flow Reference, adding the target variable `flowReferenceVar,` which stores the result of the secondary flow called by the Flow Reference component. This variable is then used in the main flow by logging `vars.flowReferenceVar`:

```xml
<!-- Main flow -->
<flow name="mainFlow" >
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="test"/>
  <set-payload value="Original payload" doc:name="Set Payload"  />
  <set-variable value="1" doc:name="Set myVar=1" variableName="myVar"/>
  <!-- Flow Reference component with target variable flowReferenceVar -->
  <flow-ref doc:name="secondaryFlow" name="secondaryFlow" target="flowReferenceVar"/>
  <logger level="INFO" doc:name="Log payload" message='#["Payload = " ++ payload]'/>
  <logger level="INFO" doc:name="Log myVar" message='#["myVar = " ++ vars.myVar]'/>
  <logger level="INFO" doc:name="Log flowReferenceVar" message='#["flowReferenceVar = " ++ vars.flowReferenceVar]'/>
</flow>
<!-- Secondary flow that is referenced from Main flow-->
<flow name="secondaryFlow" doc:id="044ece19-aa71-4fc9-ad34-8df655dd59a8" >
  <set-payload value="Modified payload" doc:name="Update Payload" />
  <set-variable value="2" doc:name="Update myVar=2" variableName="myVar"/>
</flow>
```

The following log represents the output of the example application after its execution:

```text
INFO  LoggerMessageProcessor: Payload = Original payload
INFO  LoggerMessageProcessor: myVar =  1
INFO  LoggerMessageProcessor: flowReferenceVar =  Modified payload
```

If you remove `target="flowReferenceVar"` from the Flow Reference component, the application returns the following output:

```text
INFO  LoggerMessageProcessor: Payload = Modified payload
INFO  LoggerMessageProcessor: myVar = 2
INFO  LoggerMessageProcessor: flowReferenceVar = null
```

The logs are shortened to improve readability.

## Mule Components

The main building blocks of Mule applications are components. Components execute
business logic on the messages that flow through your Mule applications. There
are a couple types of component: Core components and the components that
belong to connectors and modules.

### Core Components

These are individual components that are part of the core of the functionality of Mule Runtime. Here is a sampling of the features that core components let you add to your apps:

- Asynchronous processing of parts of a flow or subflow
- Batch processing of messages
- Initiating subflows
- Logging
- Setting payloads
- Transforming messages with the DataWeave language
- Creating Try scopes in your flows so that you can catch and respond to errors

For example, the Choice router is a component that dynamically routes messages through a flow according to a set of DataWeave expressions that evaluate message content. Each expression is associated with a different routing option. The effect is to add conditional processing to a flow, similar to an `if`/`then`/`else` code block in most programming languages.

**A List of the Core Components in Anypoint Studio**

For component documentation, see Core Components.

### Connectors

Connectors group together components that were created to facilitate the integration of MuleSoft applications with any external resources, such as third-party APIs or standard integration protocols. They enable connectivity to SaaS and on-premises applications, systems, and services.

For example, the Salesforce Connector provides components that let you use the Salesforce platform APIs to perform a large number of different operations.

**The Salesforce connector and its operations listed in Anypoint Studio**

### Modules

Modules group together components that were created to add flexibility to your applications by allowing you to aggregate values compress data, use Java features, use extra features for processing JSON, and more. The features that modules offer are more at the level of traditional application coding.

For example, the XML module provides components that can process and extract data from an XML document.

**The XML module and its components listed in Anypoint Studio**

## Scheduler Endpoint (Trigger)

Automate recurring tasks by executing flows at specific times or intervals. Use fixed frequencies to run flows every few seconds, minutes, or hours, or create complex schedules with cron expressions for specific days and times. Configure time zones to ensure flows execute at the correct local time for your use case.

Consider this when adding a Scheduler to your Mule application:

- Schedulers use the same time zone as the machine on which Mule is running. However, if an application is running in CloudHub, the Scheduler conforms to the UTC time zone, regardless of the geographic region in which the application is running.
To set a different time zone for the Scheduler, see `timeZone` in props cron expressions.
- The `disallowConcurrentExecution` property prevents the Scheduler from triggering the execution of the flow while a previously-triggered execution is running.
- If back-pressure occurs because no resources are available at the time of the scheduled trigger, Mule skips that execution.
- In a Mule runtime engine cluster or multi-worker CloudHub deployment, the Scheduler executes only on the primary node (that is, only in one Mule instance).

### Architecture

Like other Mule event source components, a Scheduler is the first component in a Mule flow.

The XML for the Scheduler consists of these elements:

- `<scheduler />`: Top-level element of the Scheduler.
- `<scheduling-strategy />`: Second-level element that accepts one of these children:
  - `<fixed-frequency />`: For common scheduling frequencies, such as every second.
  - `<cron />`: For cron expressions and time zone settings.

The Scheduler sets a scheduling strategy at a fixed frequency or an interval based on a cron expression. For example:

- The fixed frequency setting in this Scheduler executes every fifteen seconds:
```xml
<flow name="ex-fixed-frequency-flow" >
  <scheduler doc:name="Scheduler">
    <scheduling-strategy>
      <fixed-frequency frequency="15" timeUnit="SECONDS" />
    </scheduling-strategy>
  </scheduler>
  <!-- One or more processors here. -->
</flow>
```

- The cron expression in this Scheduler triggers the generation of a Mule message in a new execution of the flow every fifteen seconds:
```xml
<flow name="ex-cron-expression-flow" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <cron expression='0/15 * * * * ? '/>
    </scheduling-strategy>
  </scheduler>
  <!-- One or more processors here. -->
</flow>
```

At least one processor must follow the Scheduler. Processors include Mule components and connector operations, such as an HTTP Request operation or Transform Message component. Failure to provide a processor produces a `MuleRuntimeException` and causes the deployment of the Mule application to fail with this ERROR message in the logs (edited for readability):

```text
ERROR ...MuleRuntimeException ...
The content of element 'flow' is not complete.
One of '{"http://www.mulesoft.org/schema/mule/core":abstract-message-processor,
"http://www.mulesoft.org/schema/mule/core":abstract-mixed-content-message-processor}'
is expected.
```

For Scheduler attributes, see reference.

### Reference

The Scheduler elements accept attributes for configuring the execution interval and concurrency.

#### Scheduler (`<scheduler/>`)

By default, the Scheduler does not wait for one execution of a given flow to complete before executing another instance of the flow at the configured cadence. You can change this behavior by setting the `disallowConcurrentExecution="true"` attribute directly in the configuration XML.

| Attribute XML | Description |
|---|---|
| `disallowConcurrentExecution` | When this attribute is set to `true`, the Scheduler skips its scheduled execution if a previous execution is still running. Once the flow finishes, the Scheduler executes at the next configured interval. The default value is `false`. |

In this example, the Scheduler skips its execution if the flow takes longer to complete than the fixed frequency of 10 milliseconds:

```xml
<flow name="scheduler-disallowConcurrentExecution-ex" >
  <scheduler doc:name="Scheduler" disallowConcurrentExecution="true" >
    <scheduling-strategy>
      <fixed-frequency frequency="10" timeUnit="MILLISECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <!-- processors here -->
</flow>
```

Each time a Scheduler skips its execution, Mule logs an `Execution skipped` message, for example (edited for readability):

```text
INFO  2022-11-09 15:15:43,082 ...
...scheduler.DefaultSchedulerMessageSource:
Flow 'scheduler-disallowConcurrentExecution-ex' is already running and
'disallowConcurrentExecution' is set to 'true'. Execution skipped.

INFO  2022-11-09 15:15:43,083 ...
...scheduler.DefaultSchedulerMessageSource:
Flow 'scheduler-disallowConcurrentExecution-ex' is already running and
'disallowConcurrentExecution' is set to 'true'. Execution skipped.
```

#### Fixed Frequency (`<fixed-frequency/>`)

The fixed frequency scheduling strategy accepts these attributes:

| Attribute | XML | Default | Description |
|---|---|---|---|
| **Frequency** | `frequency` | `1000` | The frequency at which the Scheduler triggers the flow given the `timeUnit` setting. |
| **Start Delay** | `startDelay` | `0` | The amount of time to delay execution of the Scheduler for the first time after the application starts. This property uses the same `timeUnit` as the frequency. |
| **Time Unit** | `timeUnit` | `MILLISECONDS` | One of these time units for the values of `frequency` and `startDelay`: `MILLISECONDS`, `SECONDS`, `MINUTES`, `HOURS`, or `DAYS` |

This strategy delays executes the Scheduler every 10 seconds after an initial 10 second delay:

```xml
<scheduler doc:name="Scheduler" >
  <scheduling-strategy >
    <fixed-frequency frequency="10" timeUnit="SECONDS" startDelay="10"/>
  </scheduling-strategy>
</scheduler>
```

#### Cron (`<cron/>`)

For more complex scheduling strategies, you can use a cron expression.

| Attribute | XML | Description |
|---|---|---|
| **Expression** | `expression` | A cron expression for triggering the Scheduler. There is no default cron expression. For guidance with expressions, see cron expressions. Example: `expression="1 1 1 1,7 * ?"` |
| **Time Zone** | `timeZone` | Time zone passed as a system property, or in a machine's operating system. Java time zone^ values are supported. Avoid Java abbreviations, such as `PST` and `AGT`, and instead use the full-name Java equivalents, such as `America/Los_Angeles`. Example: `timeZone="America/Argentina/Buenos_Aires"` |

This example uses a cron expression to trigger the flow at 12:00 every day in the `America/Los_Angeles` time zone.

```xml
<flow name="componentsFlow">
  <scheduler>
    <scheduling-strategy>
      <cron expression="0 0 12 * * ?" timeZone="America/Los_Angeles"/>
    </scheduling-strategy>
  </scheduler>
  <logger message="my message"/>
</flow>
```

### Cron Expressions

Cron is a widely used standard for describing time and date information. The Cron Expression (`<cron expression />` scheduling strategy (`<scheduling-strategy >`) is useful for triggering a flow at intervals not available through the Fixed Frequency scheduling strategy.

The Scheduler keeps track of every second and creates a Mule event when the
Quartz Cron expression matches your time-date setting. You can trigger the event
just once or at regular intervals.

A date-time expression consists of six required settings and can include the
optional year setting. Specify the settings in this order:

1. Seconds (`0`-`59`)
1. Minutes (`0`-`59`)
1. Hours (`0`-`23`)
1. Day of month (`1`-`31`)
1. Month (`1`-`12` or `JAN`-`DEC`)
1. Day of the week (`1`-`7` or `SUN`-`SAT`)
1. Year (empty or a 4-digit year between `1970`-`2199`, for example, `2019`)

The Scheduler supports Quartz Cron expressions. Here are a few examples:

| Expression | Behavior |
|---|---|
| `1/2 ** ** ** ** ?` | Run every 2 seconds of the day, every day. |
| `0 15 10 ? ** **` | Run at 10:15 a.m., every day. `0 15 10 ** ** ? **` and `0 15 10 ** * ?` produce the same effect. |
| `0 15 10 ** ** ? 2019` | Run at 10:15 a.m., every day during the year 2019. |
| `0 ** 14 ** * ?` | Run every minute starting at 2pm and ending at 2:59pm, every day. |
| `0 0/5 14 ** ** ?` | Run every 5 minutes starting at 2pm and ending at 2:55pm, every day |
| `1 1 1 1,7 * ?` | Run the first second of the first minute of the first hour, on the first and seventh day, every month. |

The Scheduler component also supports Quartz Scheduler special characters:

- `*`: All values.
- `?`: No specific value.
- `-`: Range of values, for example, `1-3`.
- `,`: Additional values, for example, `1,7`.
- `/`: Incremental values, for example, `1/7`.
- `L`: Last day of the week or month, or last specific day of the month
  (such as `7L` for the last Saturday of the month).
- `W`: Weekday, which is valid in the day-of-month field and must follow a specific day. For example, `15W` for the weekday nearest to the 15th of the month.
- `#`: "nth" day of the month. For example, `#3` is the third day of the month.

See CronExpression for more information.

This example logs the message "hello" every second:

```xml
<flow name="cronFlow" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <cron expression="* * * * * ?" />
    </scheduling-strategy>
  </scheduler>
  <logger level="INFO" doc:name="Logger" message='"hello"'/>
</flow>
```

Note that there are several free online tools that can help you build Cron expressions.

### Examples in Anypoint Exchange

The examples in Anypoint Exchange^ show use cases for a Scheduler component:

- _Data Sync Using Watermarking and Batch_
- _Import Contacts into Microsoft Dynamics CRM_
- _Import Leads into Salesforce_
- _Importing a CSV File into mongoDB_
- _Importing an Email Attachment Using the IMAP Connector_
- _Salesforce to MySQL Database Using Batch Processing_
- _Sending a CSV File Through Email Using SMTP_

To download and open the project from Anypoint Studio, see studio::import project exchange.

### Debugging in Anypoint Studio

In Anypoint Studio debug mode, the Mule application disables the triggering of events. You can manually execute the Scheduler component when debugging by clicking the green arrow icon in Studio that appears at the bottom of the component, for example:

## Correlation ID

When Mule creates a new event, it generates a unique identifier string called a **correlation ID** before sending the event to the next processor in the flow. This ID enables you to correlate different log entries with a particular execution.

Use the correlation ID to understand the entire history of an event that resulted in an issue or an unhandled error (all errors include the correlation ID of the event that triggered it). Also, knowing the correlation ID helps you perform a memory analysis of heap dumps.

To obtain a correlation ID, Mule first checks for one in the source message (for example, a JMS message or an HTTP listener with the X-CORRELATION-ID header). If the source does not set a correlation ID, Mule generates one using the correlation ID generator.

### Modify the Correlation ID Generator

Although it is best to avoid making changes to the correlation ID generator, you might need to format the correlation ID for the events if:

- Your company has its own standard or format for correlation IDs.
- Your external system correlation IDs are a different length than those in Mule, causing an incompatibility that makes them untraceable.

In CloudHub 2.0, even if you enable the correlation ID generator, the correlation-id configured in a private space overrides the correlation ID generator.

To change how Mule generates the correlation ID:

1. Add the `<configuration>` component to your application XML.
1. Set the `correlationIdGeneratorExpression` attribute to specify the expression that generates the correlation ID:
```xml
<configuration correlationIdGeneratorExpression="#[<custom_generator_expression>]"/>
```

Ensure that the algorithm you use cannot generate the same correlation ID for two different events.

#### Correlation ID Generator Configuration Example

In the following example, Mule generates the correlation ID by calling the Java `uuid()` method, and then replaces the dashes (`-`) with dots (`.`):

```xml
<configuration correlationIdGeneratorExpression="#[uuid() replace /-/ with('.')]"/>

<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<flow name="example">
  <http:listener config-ref="HTTP_Listener_config" path="/test"/>
  <set-payload value="some"/>
  <logger level="WARN" message="#[payload]"/>
</flow>
```

After executing the flow, the logger shows the following:

```text
WARN  2021-03-30 16:46:11,269 [[MuleRuntime].uber.06: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/1; event: b5a95a63.f190.4c91.880a.5b54512fa6b1] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
```

In this case, the value `b5a95a63.f190.4c91.880a.5b54512fa6b1` is the correlation ID.

### Change the Correlation ID During the Flow Execution

You might want to change the correlation ID of the event for a given scope or a set of operations if:

- You are processing the results of a database query inside a `foreach` scope and you want to correlate
the event with the register you are processing.
- You are consuming a JMS message queue and you want to proceed using the JMS correlation ID for traceability purposes.

For these scenarios, installing the Mule Tracing module enables you to use the `with-correlation-id` scope to modify the correlation ID during the execution of said scope.

#### Install the Mule Tracing Module

To install the Mule Tracing module in your application:

1. Open your Mule project in Anypoint Studio.
1. Go to the Mule Palette.
1. Select **Search in Exchange**, and search for the Mule Tracing module.
1. Select the module and click **Add**.
1. Click **Finish**.

#### Configuration Example

Consider the following Mule application:

Application XML configuration:

```xml
<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<flow name="example">
  <http:listener config-ref="HTTP_Listener_config" path="/test"/>
  <set-payload value="some"/>
  <logger level="WARN" message="#[payload]"/>
  <tracing:with-correlation-id correlationId="#[correlationId ++ '-EXAMPLE']">
    <logger level="WARN" message="#[payload]"/>
  </tracing:with-correlation-id>
  <logger level="WARN" message="#[payload]"/>
</flow>
```

In this case, after the application executes the flow, the output logs are:
```text
WARN  2021-03-30 16:46:11,269 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/1; event: bad0e5b0-9191-11eb-a0b3-36548d51aeee] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
WARN  2021-03-30 16:46:11,271 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/2/processors/0; event: bad0e5b0-9191-11eb-a0b3-36548d51aeee-EXAMPLE] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
WARN  2021-03-30 16:46:11,274 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/3; event: bad0e5b0-9191-11eb-a0b3-36548d51aeee] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
```

### Use the DEBUG Log Level to View Additional Correlation ID Logs

If you want to see additional logs related to the correlation ID, set the log level to `DEBUG` by adding the following code to your application XML:

```text
<AsyncLogger name="org.mule.runtime.module.extension.internal.runtime.operation" level="DEBUG"/>
```

The updated logs display as follows:

```text
WARN  2021-03-30 16:58:29,545 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/1; event: bad0e5b0-9191-11eb-a0b3-36548d51aeee] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
DEBUG 2021-03-30 16:58:29,548 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] org.mule.runtime.module.extension.internal.runtime.operation.ImmutableProcessorChildContextChainExecutor: Changing event correlationId from '4c355b30-9192-11eb-b79f-36548d51aeee' to '4c355b30-9192-11eb-b79f-36548d51aeee-EXAMPLE' in location example/processors/2
WARN  2021-03-30 16:58:29,555 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/2/processors/0; event: bad0e5b0-9191-11eb-a0b3-36548d51aeee-EXAMPLE] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
DEBUG 2021-03-30 16:58:29,566 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] org.mule.runtime.module.extension.internal.runtime.operation.ImmutableProcessorChildContextChainExecutor: Event with correlationId '4c355b30-9192-11eb-b79f-36548d51aeee-EXAMPLE' going back to '4c355b30-9192-11eb-b79f-36548d51aeee' (successful execution) in location example/processors/2
WARN  2021-03-30 16:58:29,568 [[MuleRuntime].uber.05: [test-project-app].example.CPU_LITE @6d3b5ad] [processor: example/processors/3; event: bad0e5b0-9191-11eb-a0b3-36548d51aeee] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
```

### Error Handling

If an error occurs, the error handler logs the correlation ID that corresponds to the flow or Try scope that contains the error handler, for example:

```xml
<flow name="example">
  <tracing:with-correlation-id correlationId="#[correlationId ++ '-EXAMPLE']">
    <raise-error type="APP:SOME"/>
  </tracing:with-correlation-id>
  <error-handler>
    <on-error-continue>
      <logger message="#[correlationId]"/>
    </on-error-continue>
  </error-handler>
</flow>
```

In this scenario, Mule logs the correlation ID set at the beginning of the execution, because the error stops the execution of the correlation ID scope, preventing it from setting the new correlation ID (`#[correlationId ++ '-EXAMPLE']`).

However, consider the following example:

```xml
<flow name="example">
  <tracing:with-correlation-id correlationId="#[correlationId ++ '-EXAMPLE']">
    <try>
      <raise-error type="APP:SOME"/>
      <error-handler>
        <on-error-continue>
          <logger message="#[correlationId]"/>
        </on-error-continue>
      </error-handler>
    </try>
  </tracing:with-correlation-id>
</flow>
```

In this scenario, because the error handler executes within the correlation ID scope, the correlation ID logged after the flow execution is the one configured in the correlation ID scope (`#[correlationId ++ '-EXAMPLE']`).

### Example of Identifying the Correlation ID in Logs

Consider the following flow:

```xml
<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<flow name="example">
  <http:listener config-ref="HTTP_Listener_config" path="/test"/>
  <set-payload value="some"/>
  <logger level="WARN" message="#[payload]"/>
</flow>
```

After receiving a request, the flow produces the following log:

```text
WARN  2021-03-30 14:19:52,862 [[MuleRuntime].uber.04: [test-project-app].example.CPU_LITE @7a3620f2] [processor: example/processors/1; event: 23d22940-917c-11eb-9209-3c22fb13cde7] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
```

In this case, the value `23d22940-917c-11eb-9209-3c22fb13cde7` is the correlation ID. This ID is unique for the corresponding event, so any other log that includes this correlation ID is referring to the same event.

### Example of Logging the Same Correlation ID from Different Operations

Consider the following flow, which is the same as in the previous example but including a `raise-error` component:

```xml
<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<flow name="example">
  <http:listener config-ref="HTTP_Listener_config" path="/test"/>
  <set-payload value="some"/>
  <logger level="WARN" message="#[payload]"/>
  <raise-error type="APP:SOME"/>
</flow>
```

After its execution, the flow generates the following log:

```text
WARN  2021-03-30 14:27:36,045 [[MuleRuntime].uber.08: [test-project-app].example.CPU_LITE @19afa17] [processor: example/processors/1; event: 37f0f591-917d-11eb-9209-3c22fb13cde7] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: some
ERROR 2021-03-30 14:27:36,052 [[MuleRuntime].uber.08: [test-project-app].example.CPU_LITE @19afa17] [processor: example/processors/2; event: 37f0f591-917d-11eb-9209-3c22fb13cde7] org.mule.runtime.core.internal.exception.OnErrorPropagateHandler:
********************************************************************************
Message               : An error occurred.
Element               : example/processors/2 @ test-project-app:test-project-app.xml:16
Element DSL           : <raise-error type="APP:SOME"></raise-error>
Error type            : APP:SOME
FlowStack             : at example(example/processors/2 @ test-project-app:test-project-app.xml:16)

  (set debug level logging or '-Dmule.verbose.exceptions=true' for everything)
********************************************************************************
```

When the Logger and the Raise Error components execute, both components log the correlation ID `37f0f591-917d-11eb-9209-3c22fb13cde7`. Note that this correlation ID is different from the one logged in the previous example.

### Example of Setting the Correlation ID for a Database Query

The following example shows a scenario in which you can modify the correlation ID while processing the results of a database query:

Application XML configuration:

```xml
<flow name="correlation-id-flow">
  <db:select config-ref="Database_Config">
    <db:sql ><![CDATA[SELECT orderId, customerId, total from Orders  ]]></db:sql>
  </db:select>
  <foreach >
    <tracing:with-correlation-id correlationId="#[payload.orderId]">
      <logger level="INFO" message="#[correlationId]"/>
      <http:request method="GET" url="http://a-service.com" sendCorrelationId="ALWAYS"/>
    </tracing:with-correlation-id>
  </foreach>
</flow>
```

In this case, each record obtained from the database is processed within the `foreach` scope, and the correlation ID for each iteration corresponds to the `orderId` of said record. In this scenario, if there is a problem during the HTTP request operation, the correlation ID enables you to track which record caused the error.
