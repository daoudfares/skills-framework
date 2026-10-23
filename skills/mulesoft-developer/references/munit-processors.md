# MUnit: processors

> Derived from mulesoft/docs-munit (Apache 2.0).

## MUnit Event Processors

MUnit has a set of dedicated event processors to validate, assert, and mock the content and status of the Mule event so you can run automatic tests against your Mule applications.

## Set Event Processor

The Set Event Processor allows you to define a Mule Event. +
This message processor is normally used at the beginning of an MUnit test, to define the first message to send to the flow being tested.

The example below shows how to define a simple payload of a Mule Message:

```xml
<munit:set-event cloneOriginalEvent="false">
  <munit:payload value="#['payload_value']" mediaType="text/plain" encoding="UTF-8"/>
</munit:set-event>
```

The set-event has the cloneOriginalEvent property. If set to true, it clones the event produced by your code. +
By default, the value of this property is false.

The payload element in the Set Event processor has the following attributes:

| Attribute Name | Description |
|---|---|
| `value` |  |
| Defines the value of the payload's message. |  |
| `encoding` |  |
| Defines the encoding of the message. This attribute is optional. |  |
| `mediaType` |  |
| Defines the mime type of the message. This attribute is optional. |  |

You can also use the Set Event processor to define message attributes and event variables:

```xml
<munit:set-event cloneOriginalEvent="false">
  <munit:payload value="#['Example Body']" mediaType="text/plain" encoding="UTF-8"/>

  <munit:attributes value="#[{ method : 'GET', queryParams : { page : '1'}}]" />

  <munit:variables>
    <munit:variable key="variable_key" value="#['example']" mediaType="text/plain" encoding="UTF-8"/>
  </munit:variables>
</munit:set-event>
```

All the properties have the same set of attributes:

**Property Message Processor's Attributes**

| Attribute Name | Description |
|---|---|
| `key` |  |
| The key of the property being set. |  |
| `value` |  |
| The content of the property. |  |
| `encoding` |  |
| Defines the encoding of the message. This attribute is optional. |  |
| `mediaType` |  |
| Defines the mime type of the message. This attribute is optional. |  |

You can define as many properties per each scope as you need for your test.

If you define two properties in the same scope with the _same_ key, be aware that one would end up overwriting the other.

## Mock When Event Processor

The **Mock When** processor enables you to mock an event processor when it matches the defined name and attributes.

For example, you can use the **Mock Event** processor to mock a POST request with a mocked payload:

```xml
<munit-tools:mock-when processor="http:request">
   <munit-tools:with-attributes>
       <munit-tools:with-attribute attributeName="method" whereValue="#['POST']"/>
   </munit-tools:with-attributes>
   <munit-tools:then-return>
       <munit-tools:payload value="#['mockPayload']"/>
   </munit-tools:then-return>
</munit-tools:mock-when>
```

You can set the **processor** attribute to define the processor to mock and set the **with-attribute** element to define the attribute name and value. In the previous example, you define a POST method.

You can also use DataWeave functions and mappings to set the `value` attribute in the **then-return** element. For example, create a **mockPost.dwl** in the **src/test/resources/sample_data** file:

```text
%dw 2.0
output application/json
---
{
	"foo" : "var"
}
```

This DataWeave file creates the payload to send in a POST request. You can then use the **readUrl** DataWeave function to read the mapping file:

```xml
<munit-tools:then-return>
  <munit-tools:payload value="#[readUrl('classpath://sample_data/mockPost.dwl')]" mediaType="application/json" encoding="UTF-8" />
</munit-tools:then-return>
```

Finally, you can configure a **then-return** element to define the type of response the mocked processor returns. It can be a payload, a variable, a list of attributes, or an error.

You can use either a **then-return** to return a static, constant value, or you can use a **then-call** to invoke a flow for cases where the returned value can change over time, or to have different responses according to certain inputs.

> **Note:** The mocking of the processors is executed after the initialization of the Mule app, and some connectors can require credentials or configurations to start the app, even when its processors are mocked.

> **Note:** Logger processor and Transform Message processor (DataWeave) cannot be mocked.

### Mock Using Then-Return

For example, you can mock a web service consumer such as this one:

```xml
<wsc:config name="Web_Service_Consumer_Config">
  <wsc:connection wsdlLocation="tshirt.wsdl" service="TshirtService" port="TshirtServicePort" address="http://tshirt-service.cloudhub.io"/>
</wsc:config>

<wsc:consume config-ref="Web_Service_Consumer_Config" operation="OrderTshirt"/>
```

By configuring the **mock-when** processor as shown in the following example:

```xml
<munit-tools:mock-when processor="wsc:consume">
    <munit-tools:with-attributes>
        <munit-tools:with-attribute attributeName="operation" whereValue="#['OrderTshirt']"/>
    </munit-tools:with-attributes>
</munit-tools:mock-when>
```

This **mock-when** processor mocks a call to the **OrderTshirt** operation in the WSDL definition.

You can also mock specific variables:

```xml
<munit-tools:mock-when processor="http:request">
	<munit-tools:with-attributes>
	    <munit-tools:with-attribute attributeName="config-ref" whereValue="#['HTTP_Request_configuration']"/>
	</munit-tools:with-attributes>
	<munit-tools:then-return>
	  <munit-tools:variables>
	  	<munit-tools:variable key="aVariable" value="#['aValue']"/>
	  </munit-tools:variables>
	</munit-tools:then-return>
</munit-tools:mock-when>
```

#### Mock Errors

The **Mock When** processor also enables you to mock errors in your operations. Assume that you have an HTTP requester in your flow with an On-Error scope that catches any connectivity errors and returns a custom payload if the connection fails:

```xml
<http:request-config name="HTTP_Request_Config">
    <http:request-connection host="localhost" port="8888"/>
</http:request-config>

<http:listener-config name="HTTP_Listener_Config">
    <http:listener-connection host="0.0.0.0" port="8081"/>
</http:listener-config>

<flow name="api-request">
    <http:listener config-ref="HTTP_Listener_Config" path="/"/>
    <http:request method="GET" config-ref="HTTP_Request_Config" path="/api"/>
    <error-handler>
        <on-error-continue enableNotifications="true" logException="true" type="HTTP:CONNECTIVITY">
            <set-payload value="#['Connection Error']"/>
        </on-error-continue>
    </error-handler>
</flow>
```

You can assert that every time the HTTP request fails, your application returns your custom payload:

```xml
<munit:test name="HTTP-fail-test" description="Asserts Custom Payload in HTTP Connectivity errors.">
    <munit:behavior>
        <munit-tools:mock-when processor="http:request">
            <munit-tools:with-attributes>
                <munit-tools:with-attribute attributeName="config-ref"
                                            whereValue="#['HTTP_Request_Config']"/> // <1>
            </munit-tools:with-attributes>

            <munit-tools:then-return>
                <munit-tools:error typeId="#['HTTP:CONNECTIVITY']"/> // <2>
            </munit-tools:then-return>
        </munit-tools:mock-when>
    </munit:behavior>

    <munit:execution>
        <flow-ref name="api-request"/> // <3>
    </munit:execution>

    <munit:validation>
      <munit-tools:assert-that expression="#[payload]" is="#[MunitTools::equalToIgnoringCase('connection error')]"/> // <4>
    </munit:validation>
</munit:test>
```

<1> Mock an HTTP Requester with the configuration of the requester in your flow.
<2> Configure a then-return element to throw an **HTTP:CONNECTIVITY** error. +
    This triggers the On-error scope in your application.
<3> Execute the flow containing the requester.
<4> Assert that the returned payload is the one you set in the On-error scope.

You cannot return all known error types of a Mule application. You can return the type of errors defined in the modules the current flow uses. If you try to return an error type that is out of the scope of the flow you're testing, you get a **MULE:UNKNOWN** error instead of the configured one.

#### Parameters

If you create a mock error, choose one of the following parameters to provide the trigger for the error in the **Then-return** tab:

- **TypeId**: Follows a Mule Error type definition. For example, the HTTP:CONNECTIVITY error explained before.
- **Cause**: Expects the instance of the exception with a message for the error. For example, using Java, write the expression:

```java
#[java!java::lang::Exception::new("Exception Message")]
```

### Mock Using Then-Call

To dynamically mock a variable, use **then-call** as follows:

```xml
<flow name="flow-to-be-mocked">
    <set-variable variableName="count" value="#[0]"/>
</flow>

<flow name="flow-to-test">
    <flow-ref name="flow-to-be-mocked"/> // <1>
</flow>

<flow name="count-to-3"> // <2>
    <choice>
        <when expression="#[vars.count == null]">
            <set-variable variableName="count" value="#[1]" doc:name="Create counter"/>
        </when>

        <when expression="#[vars.count < 3]">
            <set-variable variableName="count" value="#[vars.count + 1]"
                          doc:name="Increase count by 1, up to 3"/>
        </when>
    </choice>
</flow>

<munit:test name="variable-mock-test">
    <munit:behavior>
        <munit-tools:mock-when processor="mule:flow-ref">
            <munit-tools:with-attributes>
                <munit-tools:with-attribute attributeName="name" whereValue="#['flow-to-be-mocked']"/>
            </munit-tools:with-attributes>

            <munit-tools:then-call flow="count-to-3"/> // <3>
        </munit-tools:mock-when>
    </munit:behavior>

    <munit:execution>
        <flow-ref name="flow-to-test"/> <!-- 1 -->
        <flow-ref name="flow-to-test"/> <!-- 2 -->
        <flow-ref name="flow-to-test"/> <!-- 3 -->
        <flow-ref name="flow-to-test"/> <!-- 3 -->
    </munit:execution>

    <munit:validation>
        <munit-tools:assert-that expression="#[vars.count]" is="#[MunitTools::equalTo(3)]"/>
    </munit:validation>
</munit:test>
```

<1> This is the processor you mock.
<2> The mock calls this flow. The mock sets a variable that changes depending on the incoming event.
<3> Configure the mock to call the desired flow.

## Verify Event Processor

The Verify Event processor allows you to verify if a processor was called.

For example, you can validate if a specific processor has been called with a particular set of attributes a specific number of times.

When defining a verification, you are telling MUnit to fail a test if the verification is not successful.

You can define verifications over any processor, even if you haven't created a mock for it.

```xml
<munit-tools:verify-call processor="http:request" atLeast="1">
   <munit-tools:with-attributes>
       <munit-tools:with-attribute attributeName="method" whereValue="#['GET']" />
   </munit-tools:with-attributes>
</munit-tools:verify-call>
```

| Attribute Name | Description |
|---|---|
| `eventProcessor` |  |
| Describes which event processor you want to mock. The description takes the form `\:\`. It supports regular expressions. |  |
| `times` |  |
| **(Default = 1.)** Defines the verification as successful if the event processor was called _N_ and only _N_ number of times. |  |
| `atLeast` |  |
| Defines the verification as successful if the event processor was called a minimum of _N_ number of times. |  |
| `atMost` |  |
| Defines the verification as successful if the event processor was called maximum of _N_ number of times. |  |

The attributes `times`, `atLeast`, `atMost`, are mutually exclusive.

The `eventProcessor` attribute accepts regular expressions. For example, you can create the same verification as `.*:request` to verify for an event processor named request, disregarding which namespace the event processor belongs to. The regular expression language is the same as Java.

## Spy Event Processor

The **Spy Processor** enables you to spy on what happens before and after an event processor is called. +
This enables you to validate, for example that a selected Mule Event reaches a specific event processor containing a specific payload or variable.

Setting a spy processor tells MUnit to run a set of instructions (usually assertions or verifications) before and/or after the execution of the spied event processor.

Assume that you have this configuration:

```xml
<flow name="testFlow">
  <http:request path="/my/api" />
</flow>
```

You can configure the spy processor to spy on any Http Request and assert that the payload is null before reaching the component, and not null after it's been processed:

```xml
<munit:test name="suiteTest" >

  <munit:behavior >

    <munit-tools:spy processor="http:request">
      <munit-tools:before-call >
        <munit-tools:assert-that expression="#[payload]" is="#[MunitTools::nullValue()]"/>
      </munit-tools:before-call>
      <munit-tools:after-call >
        <munit-tools:assert-that expression="#[payload]" is="#[MunitTools::notNullValue()]"/>
      </munit-tools:after-call>
    </munit-tools:spy>

  </munit:behavior>

</munit:test>
```

Or even to spy on any Http Request, whose path is '/my/api'.

```xml
<munit:test name="suiteTest" >

  <munit:enable-flow-sources >
    <munit:enable-flow-source value="testFlow" />
  </munit:enable-flow-sources>

  <munit:behavior >

    <munit-tools:spy processor="http:request">
      <munit-tools:with-attributes >
        <munit-tools:with-attribute attributeName="path" whereValue="#['/my/api']" />
      </munit-tools:with-attributes>

      <munit-tools:before-call >
        <munit-tools:assert-that expression="#[payload]" is="#[MunitTools::nullValue()]"/>
      </munit-tools:before-call>

      <munit-tools:after-call >
        <munit-tools:assert-that expression="#[payload]" is="#[MunitTools::notNullValue()]"/>
      </munit-tools:after-call>

    </munit-tools:spy>

  </munit:behavior>

</munit:test>
```

As shown above, this processor enables you to define actions for before and after calling the spied processor.
However, keep in mind that the spy processor does not modify the original Mule Event. +
If you set variables, attributes, or modify the payload inside a Spy, these changes won't persist outside the processor. +
Overall, you should use the Spy processor to verify or assert.

## Assert That Event Processor

The Assert That event processor allows you to run assertions to validate the state of a Mule event's content. You can use the Assert That processor to validate the Mule event after the production code runs.

The Assert That processor uses a set of DataWeave functions called `MUnit matchers` to define the assertion conditions for any value in an expression.

For example, to assert that a payload is equal to a certain value, configure the Assert That processor using the `equalTo()` matcher.

```xml
<munit-tools:assert-that
  expression="#[payload]"
  is="#[MunitTools::equalTo('example')]"
  message="The payload should be ‘example’"/>
```

Or you can also check if the payload is null using the `nullValue()` matcher.

```xml
<munit-tools:assert-that
  expression="#[payload]"
  is="#[MunitTools::nullValue()]"
  message="The payload should be null"/>
```

See MUnit Matchers for more information.

If these assertion fails, the processor throws a `MUNIT-TOOLS:ASSERTION_ERROR`.

## Assert Equals

The Assert Equals processor allows you to run assertions in order to validate the state of a Mule Event's content. This processor can be used to validate the Mule Event after the production code runs.

For example, to assert that a payload is equal to a certain value, you can configure the Assert-Equals processor the following way:

```xml
<munit-tools:assert-equals
  actual="#[payload]"
  expected="#[2]"
  message="The payload should be 2"/>
```

If the `expected` attribute is a String, you can specify the literal value without requiring an expression.

```xml
<munit-tools:assert-equals
  actual="#[payload]"
  expected="Example"
  message="The payload should be 'Example'"/>
```

If this assertion fails, the processor throws a `MUNIT-TOOLS:ASSERTION_ERROR`.

## Assert Expression

The Assert Expression processor allows you evaluate a Dataweave expression that asserts the state of a Mule Event's content. This processor can be used to validate the Mule Event after the production code runs, using the DataWeave Assertions Library.

For example, to assert that a payload is equal to a certain value, you can configure the Assert-Expression processor using the equalTo() matcher.

```xml
<munit-tools:assert>
    <munit-tools:that>#[ import * from dw::test::Asserts ---
        payload must equalTo('example') ]
    </munit-tools:that>
</munit-tools:assert>
```

### Perform Complex Assertions

The DW assertions library allows you to assert the state of the Mule Event's content in a deeper way.

```xml
<munit-tools:assert>
    <munit-tools:that>#[ import * from dw::test::Asserts ---
        vars.attributes must [beObject(), $.statusCode must equalTo(200), $.method must equalTo('GET')] ]
    </munit-tools:that>
</munit-tools:assert>
```

### Create your own Matcher

To create your own matcher, you can add DW files to your `src/test/resources` folder. For example, a file called
`MyMatcher.dwl` with the following content:

```dataweave
import * from dw::test::Asserts

fun beEven(): Matcher<Number> =
     (actual:Number) -> do {
         var matchesEven = (actual mod 2) == 0
         ---
         {
             matches: matchesEven,
             description: {expected: " to be an even number.", actual: write(actual) as String}
         }
     }
```

And then use it in your Assert-Expression processor:
```xml
<munit-tools:assert>
    <munit-tools:that>#[ import * from dw::test::Asserts ---
        payload must MyMatcher::beEven() ]
    </munit-tools:that>
</munit-tools:assert>
```

If this assertion fails, the processor throws a `MUNIT-TOOLS:ASSERTION_ERROR`.

Matchers from the `dw::test::Asserts` library are not compatible with the `MunitTools` matchers. You can't use `dw::test::Asserts` with the Assert-That processor, and you can't use `MunitTools` matchers with the Assert-Expression processor.

## Fail Event Processor

The Fail Event Processor allows you to fail your test on purpose. This is useful to validate that a test should fail
if that point is reached.

```xml
<munit-tools:fail
  message="This should fail"/>
```

The message field is optional and defines the error message to print when the assertion fails.
The processor throws a `MUNIT-TOOLS:ASSERTION_ERROR`.

## Run Custom Event Processor

The **Run Custom event processor** enables you to assert the Mule event content against a custom assertion.

To add the **Run Custom processor** to your project, add the following dependency to your `pom.xml` file:

```xml
<dependency>
    <groupId>com.mulesoft.munit</groupId>
    <artifactId>munit-assert</artifactId>
    <version>${munit.version}</version>
    <scope>test</scope>
</dependency>
```

You also have to add your custom assertion class to the `mule-artifact.json` file as an exported resource.

For example, you can define the following assertion in Java:

```java
package org.mule.custom;
import org.mule.munit.assertion.api.MunitAssertion;
import org.mule.munit.assertion.api.TypedValue;

public class CustomAssertion implements MunitAssertion {

    @Override
    public void execute(TypedValue expression, Object params) throws AssertionError { // <1>
        if (!"Hello World".equals(expression.getValue())) { // <2>
            throw new AssertionError("Error the payload is incorrect");
        }
     }

}
```

<1> Implement the only method in the interface `public void execute(TypedValue expression, Object params) throws AssertionError`.
<2> Run your custom logic, which in this case validates that the message payload is `Hello World`.

The `CustomAssertion` class must be located in the scr/test/java directory.

And use the **Run Custom Event Processor** to run it:

```xml
<munit-tools:run-custom
  assertion="org.mule.custom.CustomAssertion" // <1>
  expression="#[payload]"/>
```

<1> The assertion field needs to have the canonical class name of your custom assertion and the class needs to be exported.

To export it when packaging your application, add the `org.mule.custom` package to your `mule-artifact.json`

```json
{
    "name": "mule-application",
    "minMuleVersion": "4.2.0",
    "classLoaderModelLoaderDescriptor": {
        "id": "mule",
        "attributes": {
            "exportedPackages": [
                "org.mule.custom" 
            ]
        }
    }
}
```

> **Note:** You only need to configure the package name in the `exportedPackages` collection.

## Storage Event Processors

The Storage processors allows you to manage temporary storage during  your tests.

All storage is cleared as soon as the test ends.

### Store operation

Stores the given data associated with the given key. If `value` not set, it defaults to the `payload`.

```xml
<munit-tools:store key="myKey">
    <munit-tools:value>#[person : { name: 'John', lastName: 'Smith' }]</munit-tools:value>
</munit-tools:store>
```

### Retrieve operation

Retrieves the data associated with the given key

```xml
<munit-tools:retrieve key="myKey"/>
```

### Remove operation

Removes and returns the data associated with the given key

```xml
<munit-tools:remove key="myKey"/>
```

### Clear stored data operation

Clears all stored data

```xml
<munit-tools:clear-stored-data/>
```

## Queue Event Processors

The Queue event processors allow you to manage temporary queues during your test runs.

All queues are emptied as soon as the test ends.

### Queue

Adds the value to the queue. If not specified, the value is taken from the `payload`.

```xml
<munit-tools:queue>
    <munit-tools:value>#[1]</munit-tools:value>
</munit-tools:queue>
```

You can specify the queue's name to which the value should be added. If not specified, the default queue will be used.

```xml
<munit-tools:queue queueName="CUSTOM_QUEUE_1">
    <munit-tools:value>#[1]</munit-tools:value>
</munit-tools:queue>
```

### Dequeue

Removes the last element of the queue, if the queue is empty, it waits until an element is queued.

```xml
<munit-tools:dequeue/>
```

You can specify a timeout when waiting for an element to be queued:

```xml
<munit-tools:dequeue timeout="1000" timeoutUnit="SECONDS"/>
```

Like the queue operation, you can specify the queue's name from which to dequeue. If not specified, the default queue will be used.

```xml
<munit-tools:dequeue queueName="CUSTOM_QUEUE_1"/>
```

### Queue Size

Function that obtains the queue size.

```xml
<munit-tools:assert-that expression="#[MunitTools::queueSize()]" is="#[MunitTools::equalTo(2)]" />
```

Like the other operations, you can specify the queue from which to the get the size.
If not specified, the default queue will be used.

```xml
<munit-tools:assert-that expression="#[MunitTools::queueSize('CUSTOM_QUEUE_1')]" is="#[MunitTools::equalTo(2)]" />
```

## Sleep Processor

The Sleep processor allows you to pause your test for a specific time. You can use this processor to simulate a delay in the processing of the flow:

```xml
<munit-tools:sleep time="100" timeUnit="MILLISECONDS"/>
```

`time` ::
 Numerical value for the unit of time that your test waits before going to sleep.

`timeUnit` ::
The unit in which the `time` value is measured.
Possible values are:
- `MILLISECONDS` (default)
- `MICROSECONDS`
- `MINUTES`
- `NANOSECONDS`
- `SECONDS`
- `HOURS`

## Dynamic Ports

The Dynamic Ports global element allows you to bind a free port to a property. It searches for a free port available and can be narrowed to a specific range.

For example, a dynamic port would look something like this:

```xml
<munit:dynamic-port propertyName="a.dynamic.port"/>
```

And it can be used in the http configuration:

```xml
<http:request-config name="httpRequestConfig">
    <http:request-connection host="localhost" port="${a.dynamic.port}"/>
</http:request-config>
```

Additionally you can set min and max values from where to get the port:

```xml
<munit:dynamic-port propertyName="a.dynamic.port" min="6000" max="7000"/>
```

## Dynamic Directories

When managing files and folders during a test, MUnit provides the `munit.temporary.directory` property to reference a temporary directory. You can create files and folders inside this directory to use in your tests.

The temporary directory is deleted at the end of each test.

For example, using the file connector, you could configure the working directory as follows:

```xml
<file:config name="tmpDir">
    <file:connection workingDir="${munit.temporary.directory}"/>
</file:config>
```

And then use it to create files/folders inside it:

```xml
<file:create-directory config-ref="tmpDir" directoryPath="example"/>
```

## MUnit Utils

One of the main problems of testing production code are external system connections.

MUnit provides a set of utilities for you to write your tests in a portable way and mock external system connections from your tests.

| Utility | Description |
|---|---|
| Database | Implement a DB server in your local environment to test connections. |
| FTP | Implement an FTP server in your local environment to test connections. |
| Queue Event Processors | Manage temporary queues during your test runs. |

## Installing a Database Server

To test a piece of code that connects with a database server, install a database server in your local environment to run the tests. You can also use a dedicated external database server for testing, but your Maven project can't be portable. If so, a third party must install the testing database server to compile your project.

To make it easier for you to test database connections, MUnit allows you to implement a database server in your local environment.

### Install the MUnit DB Server Module

To install the MUnit DB Server Module:

1. Look for the **MUnit Utils Database Server** module.
1. Add the module to your project in the `pom.xml` file:
```xml
<!-- dbserver Dependency -->
<dependency>
    <groupId>com.mulesoft.munit.utils</groupId>
    <artifactId>munit-dbserver-module</artifactId>
    <version>LATEST_VERSION</version> //<!--1-->
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
</dependency>
```

  1. Check the MuleSoft Nexus repository to get the **LATEST_VERSION**.
The MUnit DB server artifact in your `pom.xml` file must have the `test` scope.
1. The `h2` dependency used for the database is a shared library. +
Add the dependency to your `pom.xml` file and list it as a `sharedLibrary` in `mule-maven-plugin`.
```xml
<!--Third party libs-->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <version>1.3.166</version>
</dependency>
```

```xml
<plugin>
    <groupId>org.mule.tools.maven</groupId>
    <artifactId>mule-maven-plugin</artifactId>
    <version>${mule.maven.plugin.version}</version>
    <extensions>true</extensions>
    <configuration>
    <sharedLibraries>
            ...
            <sharedLibrary>
                <groupId>com.h2database</groupId>
                <artifactId>h2</artifactId>
            </sharedLibrary>
        </sharedLibraries>
    </configuration>
</plugin>
```

The **MUnit DB Server** module is located at MuleSoft Nexus repository. The **MUnit DB Server** module version 3 and later is compatible with Java 17. Previous versions of this module available at Anypoint Exchange are deprecated.

### Attributes Reference

| Attribute Name | Description |
|---|---|
| `name` |  |
| Defines the configuration name of this DB server. This value must be unique. |  |
| `database` |  |
| Defines the name of the in-memory DB. |  |
| `sqlFile` |  |
| Specifies the path of the SQL file that defines the DB structure/contents. Use this parameter to create the DB at startup. See the Defining the DB Structure from an SQL File section for additional information. |  |
| `csv` |  |
| Specifies the path of the comma-separated file used to define the DB structure/contents. Use this parameter to create the DB at startup. See Defining the DB Structure from a CSV File section for additional information. |  |
| `connectionStringParameters` |  |
| Defines the connection string for your database. You can concatenate the parameters with a semicolon. |  |

### Define the DB Structure

You can define the structure and content of your database in two different ways:

- SQL
- CSV

The MUnit DB server is based on H2. Complex structures, index and join commands can present issues.

#### Defining the DB Structure from an SQL File

To define the DB structure and content from an SQL file, you must provide a valid set of ANSI SQL DDL (Data Definition Language) instructions in your MUnit suite file. For example, `my-munit-suite.xml`.

```xml
<dbserver:config name="MUnit_DB_Server_Config" >
    <dbserver:connection sqlFile="FILE_NAME.sql" database="DATABASE_NAME" connectionStringParameters="MODE=MySQL" />
</dbserver:config>
```

#### Define the DB Structure From a CSV File

To define your DB structure in your MUnit suite file based on a CSV file:

- The name of the table is the name of the file (in the following example, `customers`).
- The names of the columns are the headers of your CSV file.

```xml
<dbserver:config name="MUnit_DB_Server_Config" >
    <dbserver:connection csv="FILE_NAME.csv" database="DATABASE_NAME" connectionStringParameters="MODE=MySQL" />
</dbserver:config>
```

You can also split your DB structure among several CSV files. In your MUnit suite file, include the file names in a list, with the names separated by semicolons:

```xml
<dbserver:config name="MUnit_DB_Server_Config" >
    <dbserver:connection csv="FILE_NAME.csv;FILE_NAME_1.csv" database="DATABASE_NAME" connectionStringParameters="MODE=MySQL" />
</dbserver:config>
```

This creates two tables: `FILE_NAME` and `FILE_NAME_1`.

### MUnit DB Server Processors

The DB server utility has two processors to interact with your DB server:

#### Validate-That

To validate that the results of a query are as expected, use the `validate-that` operation in your MUnit suite file. Set the `results` property to CSV with rows separated by a newline character (`\n`), as follows:

```xml
<dbserver:validate-that config-ref="DB_Server"
query="SELECT * FROM jobtitlelookup WHERE JOBTITLE='Developer';" returns=""JOBTITLE","EECSALARYORHOURLY","JOBTITLEID"\n"Developer","10","DEV"" />
```

#### Execute

Execute instructions for the in-memory databases to add or remove registries before a test and verify that your data is correctly stored using MUnit DB Server.

In your MUnit suite file, use a DB Server connector with the `execute` operation to insert the new values to the table (`Culinary Team Member,10,HIR`). Then use another DB Server connector with an `execute query` operation to retrieve all values from the table (including the newly added ones). Finally, check the payload using a logger component to store the payload:

```xml
<!-- Execute a SQL instruction using the execute operation -->
<dbserver:execute config-ref="MUnit_DB_Server_Config" sql="INSERT INTO jobtitlelookup VALUES ('Culinary Team Member','10','HIR');"/>

<!-- Check the update using execute-query operation -->
<dbserver:execute-query config-ref="MUnit_DB_Server_Config" sql="SELECT * FROM jobtitlelookup"/>

<!-- log the resulting payload -->
<logger level="INFO" message="#[payload]"/>
```

The logger in your console reads:

```text
org.mule.runtime.core.internal.processor.LoggerMessageProcessor: [{JOBTITLEID=DEV, EECSALARYORHOURLY=10, JOBTITLE=Developer}, {JOBTITLEID=HIR, EECSALARYORHOURLY=10, JOBTITLE=Culinary Team Member}]
```

## FTP Utils

To test a piece of code that connects with an FTP server, install an FTP server in your local environment to run the tests. You can also use a dedicated external FTP server for testing, but your Maven project can't be portable. A third party must install the testing FTP server to compile your project.

To test the FTP connections, you can implement an FTP server in your local environment with MUnit.

### Install the MUnit FTP Server Module

To install the MUnit FTP server module:

1. Look for the **MUnit Utils FTP Server** module.
1. Add the module to your project:
```xml
<!-- Ftp Server Dependency -->
<dependency>
    <groupId>com.mulesoft.munit.utils</groupId>
    <artifactId>munit-ftpserver-module</artifactId>
    <version>LATEST_VERSION</version> //<!--1-->
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
</dependency>
```

  1. Check the MuleSoft Nexus repository to get the **LATEST_VERSION**.

The MUnit FTP server artifact in your POM file must have the `test` scope.

The **MUnit FTP Server** module is located at MuleSoft Nexus repository. The **MUnit FTP Server** module version 3 and later is compatible with Java 17. Previous versions of this module available at Anypoint Exchange are deprecated.

### Attributes Reference

The FTP server module takes the following parameters:

| Attribute Name | Description |
|---|---|
| `name` | Defines the configuration name of the FTP server. + This value must be unique. |
| `port` | Defines the port on which the FTP server listens. |
| `anonymous` | (Boolean) Sets anonymous access to the FTP server. If you set `anonymous` to `true`, don't set a password to access the FTP server when using the `anonymous` username. + The default value is `true`. |
| `secure` | (Boolean) Defines the FTP protocol. If you set the `secure` parameter to `true`, the server behaves as an SFTP server and connections must be authenticated. If you set the `secure` parameter to `false`, the server behaves as an FTP server and allows either authenticated or anonymous connections. + The default value is `false`. |
| `homeDir` | Defines the user's home directory. The default value is the filesystem root. + You can define the FTP user home directory by using the `~` character to represent the home directory on the file system. |

### MUnit FTP Server Processors

The FTP Utility has two processors to interact with your FTP server:

contains-files::
The `contains-files` processor validates the existence of a file in the FTP server. If there is no file present, the processor fails causing the test to fail.
```xml
<ftpserver:contains-files config-ref="MUnit_FTP_Server_Config" path="/" file="example.txt"/>
```

| Attribute Name | Description |
|---|---|
| `config-ref` |  |
| Defines the FTP server configuration. |  |
| `path` |  |
| Defines in which folder to search based on the user home directory defined. |  |
| `file` |  |
| Defines the name of the file to look for. |  |

remove::
The `remove` processor provides an operation that instructs the FTP server to remove a file from storage.
```xml
<ftpserver:remove config-ref="MUnit_FTP_Server_Config" path="example.txt"/>
```

| Attribute Name | Description |
|---|---|
| `config-ref` |  |
| Defines the FTP server configuration. |  |
| `path` |  |
| Defines the full path of the file to remove. |  |

This feature is useful when creating the same file name several times. You can configure it in `after-test` to ensure that no name collisions cause the test to fail.
