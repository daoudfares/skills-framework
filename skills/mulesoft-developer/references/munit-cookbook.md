# MUnit: worked examples

> Derived from mulesoft/docs-munit (Apache 2.0).

## MUnit Cookbook

This section links to examples that demonstrate common MUnit usages.

| Example | Description |
|---|---|
| Mocking Resources for Your Tests | Mocking test code for your MUnit tests. |
| Mocking a Message Before and Inside a Foreach Processor | Mocking a processor that can return different payloads. |
| Testing and Mocking Errors | Mocking expected errors in your code. |
| Testing with Environment Properties | Loading different environment values to your MUnit tests. |
| Using Utility Classes From a Test | Using custom Java classes in your MUnit tests. |
| Configuring FTP Server Utility in an MUnit Test | Configuring an FTP utility to test your FTP server connections. |
| Configuring DB Server Utility in an MUnit Test | Configuring a database utility to test your database connections. |
| Patching the Embedded Mule Runtime Engine Version | Configuring MUnit to run against a patched Mule runtime engine version. |
| Test Domain-Based Applications | Testing Mule applications that inherit a Mule domain. |
| Testing a Flow with a Scheduler Source | Testing a flow that is triggered by a scheduler. |
| Recording a Test from an Exchange Example | Using the MUnit test recorder. |
| Testing a Processor That Stores Data in a Target Variable | Ensuring that the assertions check the content of the stored variable. |

## Testing and Mocking Errors

### Expect an Error in your Test

During the execution of a flow, components may throw errors which might be expected for the use case
being tested. In these cases, you want to specify that your test expects a particular error type or exception.

For example, lets look at the following Mule code:

```xml
<flow name="retrieveKey">
    <os:retrieve key="#[payload.key]"/>
    <set-variable value="#[payload.id]" variableName="userId"/>
</flow>
```

The key is taken from the payload and if the key is `null`, the Object Store connector will throw an error with `OS:INVALID_KEY`
error type.

The test to validate this case would be something like this:

```xml
<munit:test name="retrieveNullKeyTest" description="Expect error when key is null" expectedErrorType="OS:INVALID_KEY">
    <munit:behavior>
        <munit:set-event>
            <munit:payload value="#[ { key: null}]" />
        </munit:set-event>
    </munit:behavior>
    <munit:execution>
        <flow-ref name="retrieveKey"/>
    </munit:execution>
</munit:test>
```

### Error Handlers Testing

In many cases, errors are handled by the user. They may want to perform some actions when an error is thrown, and decide
 to propagate the error or continue with the flow's execution.

We can have different tests for each of the following possibilities:

#### On Error Continue

For example, lets look at the following mule code:

```xml
<flow name="retrieveKey">
    <os:retrieve key="#[payload.key]"/>
    <set-variable value="#[payload.id]" variableName="userId"/>
    <error-handler >
        <on-error-continue type="OS:INVALID_KEY">
            <set-payload value="#[{ message : 'Key is null'}]" />
        </on-error-continue>
    </error-handler>
</flow>
```

The `OS:INVALID_KEY` error is being handled and the execution continues with a specific payload.

Since the error is not propagated, the execution resumes and the event can be verified:

```xml
<munit:test name="retrieveNullKeyTest" description="Expect message when key is null">
    <munit:behavior>
        <munit:set-event>
            <munit:payload value="#[ { key: null}]" />
        </munit:set-event>
    </munit:behavior>
    <munit:execution>
        <flow-ref name="retrieveKey"/>
    </munit:execution>
    <munit:validation >
        <munit-tools:assert-that expression="#[payload.message]" is="#[MunitTools::equalTo('Key is null')]"/>
    </munit:validation>
</munit:test>
```

As you can see, in this case you don't have to expect the `OS:INVALID_KEY` error type.

#### On Error Propagate

For example, if the user's code is the following:

```xml
<flow name="retrieveKey">
    <os:retrieve key="#[payload.key]"/>
    <set-variable value="#[payload.id]" variableName="userId"/>
    <error-handler >
        <on-error-propagate type="OS:INVALID_KEY">
            <raise-error type="APP:NULL_KEY"/>
        </on-error-propagate>
    </error-handler>
</flow>
```

The `OS:INVALID_KEY` error is being handled and the error `APP:NULL_KEY` is raised.

Since the test will fail with the raised custom error type, the test should expect it:

```xml
<munit:test name="retrieveNullKeyTest" description="Expect APP:NULL_KEY is raised" expectedErrorType="APP:NULL_KEY">
    <munit:behavior>
        <munit:set-event>
            <munit:payload value="#[ { key: null}]" />
        </munit:set-event>
    </munit:behavior>
    <munit:execution>
        <flow-ref name="retrieveKey"/>
    </munit:execution>
</munit:test>
```

### Mock Errors

When you don't want to trigger manually an error on a component (like the examples above), but you only want to
make the processor fail with a specific error, you can use the `error` parameter of the mock-when processor.

For example, if the user's code is the following:

```xml
<flow name="requestFlow">
    <http:request method="GET" config-ref="HTTP_Request_configuration"/>
    <set-variable value="#[payload.id]" variableName="userId"/>
    <error-handler >
        <on-error-continue type="HTTP:CONNECTIVITY">
            <logger level="ERROR" message="AN ERROR OCCURRED"/>
        </on-error-continue>
    </error-handler>
</flow>
```

and you want to make the `http:request` fail with an `HTTP:CONNECTIVITY` error and also check that the logger was actually
executed, the test may look something like this:

**Mock Error with On Error Continue**

```xml
<munit:test name="requestFlowTest" description="Mock CONNECTIVITY error" >
    <munit:behavior >
        <munit-tools:mock-when processor="http:request">
            <munit-tools:then-return >
                <munit-tools:error typeId="HTTP:CONNECTIVITY" />
            </munit-tools:then-return>
        </munit-tools:mock-when>
    </munit:behavior>
    <munit:execution >
        <flow-ref name="requestFlow"/>
    </munit:execution>
    <munit:validation >
        <munit-tools:verify-call processor="mule:logger"/>
    </munit:validation>
</munit:test>
```

If the On Error scope is an `on-error-propagate`, the verifications won't be executed since the flow will propagate the
error and fail, then the `validation` section of the test will be skipped.

In this case the error could be caught with a try scope and then the verifications can be performed:

**Mock Error with On Error Propagate**

```xml
<munit:test name="requestFlowTest" description="Mock CONNECTIVITY error" >
    <munit:behavior >
        <munit-tools:mock-when processor="http:request">
            <munit-tools:then-return >
                <munit-tools:error typeId="HTTP:CONNECTIVITY" />
            </munit-tools:then-return>
        </munit-tools:mock-when>
    </munit:behavior>
    <munit:execution >
        <try>
            <flow-ref name="requestFlow"/>
            <error-handler >
                <on-error-continue type="HTTP:CONNECTIVITY"/>
            </error-handler>
        </try>
    </munit:execution>
    <munit:validation >
        <munit-tools:verify-call processor="mule:logger"/>
    </munit:validation>
</munit:test>
```

### Set an Event with an Error

When extracting error handling logic into a separated flow or sub flow, the input event must have an error that can be
used in the error handling logic.

For example, lets look at the following mule code:

```xml
<flow name="retrieveFlow">
    <os:retrieve key="#[payload.key]"/>
    <error-handler >
        <on-error-continue>
            <flow-ref name="error-handlingSub_Flow"/>
        </on-error-continue>
    </error-handler>
</flow>

<sub-flow name="error-handlingSub_Flow">
    <logger level="INFO" message="#['Execution failed with: $(error.description)']"/>
</sub-flow>
```

If you wish to test the subFlow independently, you will need to set an error in the event.

The test may look something like this:

**Set Error in the Event**

```xml
<munit:test name="error_handlingSub_FlowTest" description="Test subFlow" >
    <munit:behavior >
        <munit:set-event>
            <munit:error id="OS:INVALID_KEY" exception="#[java!java::lang::Exception::new('Invalid Key')]"/>
        </munit:set-event>
    </munit:behavior>
    <munit:execution >
        <flow-ref name="error-handlingSub_Flow"/>
    </munit:execution>
    <munit:validation >
        <munit-tools:verify-call processor="mule:logger">
            <munit-tools:with-attributes >
                <munit-tools:with-attribute attributeName="message" whereValue="#['Execution failed with: Invalid Key']" />
            </munit-tools:with-attributes>
        </munit-tools:verify-call>
    </munit:validation>
</munit:test>
```

## Mocking a Message Before and Inside a Foreach Processor

Suppose you have a processor inside a `foreach` scope and you want to provide different values on each iteration:

```xml
<flow name="foreachFlow">
	<foreach doc:name="For Each">
		<flow-ref doc:name="Flow Reference" name="FlowToMock"/>
	</foreach>
</flow>
```

Use an `munit-tools:mock-when` processor to mock the processor in your flow and use the `then-call` operation to call a new flow that set payloads depending on the `foreach` status:

```xml
<munit-tools:mock-when doc:name="Mock when" processor="flow-ref">
	<munit-tools:with-attributes >
		<munit-tools:with-attribute attributeName="name" whereValue="FlowToMock" />
	</munit-tools:with-attributes>
	<munit-tools:then-call flow="MockedFlow" />
</munit-tools:mock-when>
```

Inside the flow that is called by the `then-call` you can use a `Choice` processor to evaluate a value and set a mocked payload. In this case, the `foreach` counter is evaluated to decide which payload to set:

```xml
<flow name="MockedFlow" >
	<choice doc:name="Choice">
		<when expression="#[vars.counter == 1]">
			<set-payload value='#["MOCKED1"]' doc:name="Set Payload" />
		</when>
		<when expression="#[vars.counter == 2]">
			<set-payload value='#["MOCKED2"]' doc:name="Set Payload" />
		</when>
		<otherwise >
			<set-payload value='#["DEFAULT"]' doc:name="Set Payload" />
		</otherwise>
	</choice>
</flow>
```

### Mock a Mule Message

To mock processors like `file:list` or `ftp:list`, you must return a Mule message collection as payload. `MunitTools` provides a function to mock these payloads:

```text
fun createMessage(payload: Any, attributes: Any = null)

fun createMessage(payload: Any, mimeType: String|Null , attributes: Any, attributeMimeType: String|Null)
```

```xml
<flow doc:name="Flow" >
	<file:list doc:name="List" config-ref="File_Config" directoryPath="/tmp/"/>
</flow>

<munit-tools:mock-when processor="file:list">
   <munit-tools:with-attributes>
       <munit-tools:with-attribute attributeName="doc:name" whereValue="List"/>
   </munit-tools:with-attributes>
   <munit-tools:then-return>
       <munit-tools:payload value="#[[MunitTools::createMessage( "ITEM-1",  "text/plain", { property : 'ATTRIBUTE-1'}, null) , MunitTools::createMessage( "ITEM-2",  "text/plain", { property : 'ATTRIBUTE-2'}, null)]]" />
   </munit-tools:then-return>
</munit-tools:mock-when>
```

## Mocking Resources for Your Tests

As your tests suites start to get bigger and more complex, it’s a good practice to externalize some parts of the test code, not only so that you can keep the code clean and organized but also to reuse the files that you need to mock for your tests.

You can leverage DataWeave to mock your test code, either by creating DataWeave scripts or by using variables in a DataWeave module.

### Mock Files Using DataWeave File

You can write a DataWeave file that returns the data that you want to mock, save the file under a folder in `src/test/resources` and then use a DataWeave function from your test to read this file.

For example, imagine that you have defined a `mockPost.dwl` file in the `src/test/resources/sample_data` folder with the following content:

```text
%dw 2.0
output application/json
---
{
	"foo" : "var"
}
```

This DataWeave file (`mockPost.dwl`) is a sample that creates a mock payload that you want to return in an `http:request` request.

When configuring the `then-return` section in the `mock-when`, use the `readUrl` function to read the mapping file:

```xml
<munit-tools:then-return>
  <munit-tools:payload value="#[readUrl('classpath://sample_data/mockPost.dwl')]" mediaType="application/json" encoding="UTF-8" />
</munit-tools:then-return>
```

The `classpath-based` URL uses the `classpath:` protocol prefix to find the file defined in `src/test/resources`.

### Mock Files Using Variables in a DataWeave Module

You can create a DataWeave module to centralize all your mocked data in a single file by declaring it using DataWeave variables.

For example, imagine that you create a custom DataWeave module by creating a `TestData.dwl` file in `src/test/resources`, and you add variables with references to different mocked data, either from files or inline:

```text
import getResourceAsString from MunitTools

var mockPost = readUrl('classpath://sample_data/mockPost.dwl')
var foo = "N123"
var jsonFromFile = read(getResourceAsString('sample_data/mydata.json'), 'application/json')
var jsonObject = { paymentID: "1B56925769601335TLQMIWVY" }
```

You can then access any of the defined variables in the DataWeave module by importing the variables from your module:

```xml
<munit-tools:then-return >
    <munit-tools:variables>
        <munit-tools:variable key="ticket" value="#[import TestData output application/json --- TestData::mockPost]" mediaType="application/json" />
    </munit-tools:variables>
</munit-tools:then-return>
```

## Testing with Environment Properties

Assume that you have the following flow that obtains data from an external API and you need to consume it from a test environment when executing your MUnit tests:

```xml
<http:request-config name="HTTP_Request_configuration">
	<http:request-connection host="sampleapi.com/api/v1/" port="80"/>
</http:request-config>
<flow name="requestApiFlow">
	<http:request method="GET" config-ref="HTTP_Request_configuration" path="/employee"/>
</flow>
```

To consume data from a QA API endpoint when running your MUnit tests:

1. Extract the HTTP Configuration values into a properties file for each environment where you will execute the validations. Those properties files must go under `src/main/resources`:
**prod.properties**

```xml
http.host=dummy.restapiexample.com/api/v1/
http.port=80
```

**qa.properties**

```xml
http.host=dummy.qax.restapiexample.com/api/v1/
http.port=8081
```

You can set a properties file for each one of your environments.
1. Use a `configuration-properties` global configuration in your configuration file to load environment properties from the previously created file:
```xml
 <configuration-properties file="${mule-env}.properties"/>
```

1. Replace the HTTP configuration with placeholders matching the variables defined in the properties file:
```xml
<http:request-config name="HTTP_Request_configuration">
	<http:request-connection host="${http.host}" port="${http.port}"/>
</http:request-config>
<flow name="requestApiFlow">
	<http:request method="GET" config-ref="HTTP_Request_configuration" path="/employee"/>
</flow>
```

1. Define an environment variable in the MUnit Maven plugin:
```xml
 <configuration>
     ...
     <environmentVariables>
         <mule-env>qa</mule-env>
     </environmentVariables>
     ...
 </configuration>
```

During the execution of the MUnit tests, MUnit loads the properties from the `qa` properties file and connects to your test environment.

## Using Utility Classes From a Test

When developing test cases, you might want to use custom Java classes located in `src/test/java`. You can use Java classes through DataWeave or through Java Module.

When using custom classes, the package of the class must be exported in the `mule-artifact.json` file:

```json
{
  "minMuleVersion": "4.x.x",
  "classLoaderModelLoaderDescriptor": {
    "id": "mule",
    "attributes": {
      "exportedPackages": [
        "com.example.test"
      ]
    }
  }
}
```

For example, assume that you want to use in an MUnit test a `MyUtilClass.java` class located in `src/test/java/com/example/`:

**MyUtilClass**

```java
package com.example.test;

public class Helper {

  public static long getCurrentMillis() {
    return System.currentTimeMillis();
  }

}
```

### Invoke Your Java Class Using DataWeave

To invoke static methods using DataWeave you must add the `java!` prefix to the package name of the class:

**Use a class in DataWeave**

```xml
<munit:test name="usingJavaInDW">
    <munit:behavior>
        <set-variable variableName="number" value="#[java!com::example::test::Helper::currentMillis()]" />
    </munit:behavior>
    <munit:execution>
        <flow-ref name="myFlow"/>
    </munit:execution>
</munit:test>
```

### Invoke Your Java Class Using Java Module

To invoke a custom Java class using Java Module:

1. Ensure that Java Module is in your project:
**Java Module dependency**

```xml
<dependency>
    <groupId>org.mule.module</groupId>
    <artifactId>mule-java-module</artifactId>
    <version>${javaModule.version}</version>
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
</dependency>
```

1. Use any of the Java Module's operations. +
For this example, invoke a static method of a class:
**Use a class with the Java Module**

```xml
<munit:test name="usingJavaInDW">
    <munit:behavior>
        <set-variable variableName="number" value="#[java!com::example::test::Helper::currentMillis()]" />
    </munit:behavior>
    <munit:execution>
        <flow-ref name="myFlow"/>
    </munit:execution>
</munit:test>
```

## Testing a Flow with a Scheduler Source

Assume that you want to both test the following flow triggered by a Scheduler component and validate that your flow is being triggered correctly:

```xml
<flow name="schedulerFlow">
    <scheduler>
        <scheduling-strategy >
            <fixed-frequency frequency="10" timeUnit="SECONDS"/>
        </scheduling-strategy>
    </scheduler>
    <set-payload value="#['test poll']"/>
</flow>
```

1. Enable flow sources. +
Because MUnit does not start any of the flow sources (such as triggers or listeners), you must configure which flow sources start for your tests.
In this example, you enable the flow that contains the Scheduler:
```xml
<munit:test name="test-schedulerFlowTest">
    <munit:enable-flow-sources>
        <munit:enable-flow-source value="schedulerFlow"/>
    </munit:enable-flow-sources>
</munit:test>
```

1. Verify that flow execution is triggered by the Scheduler. +
To verify that the processors inside your flow are being triggered, use the `munit-tools:verify-call` processor.
Wrap `munit-tools:verify-call` inside an `until-successful` to shorten processing time when the Scheduler is not operating when you want to test.
The following example validates three times that the payload was executed at least once during the test.
```xml
<munit:execution>
    <until-successful maxRetries="3" millisBetweenRetries="100">
        <munit-tools:verify-call processor="set-payload" atLeast="1">
            <munit-tools:with-attributes >
                <munit-tools:with-attribute whereValue="#['test poll']" attributeName="value" />
            </munit-tools:with-attributes>
        </munit-tools:verify-call>
    </until-successful>
</munit:execution>
```

## Testing a Processor That Stores Data in a Target Variable

When you test a processor that stores its result in a target variable, ensure that the assertions check the content of the stored variable. If you mock the processor, define a value for the target variable.

### Example Test of a Target Variable from an HTTP Request Operation

Consider a Mule application with the following XML configuration:

```xml
<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<http:request-config name="HTTP_Request_configuration" doc:name="HTTP Request configuration" />

<flow name="targetVariableTestFlow" >
  <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/test"/>
  <http:request
    method="GET"
    doc:name="Request"
    config-ref="HTTP_Request_configuration"
    target="httpResponse"
    targetValue="#[message]"
    url="http://www.mulesoft.com"/>
  <logger level="INFO" doc:name="Logger" message="#[vars.httpResponse]"/>
</flow>
```

When the HTTP listener receives a request, the app makes an HTTP request and the processor stores the received HTTP response in a target variable called `httpResponse`.

You can create an MUnit test to assert that the stored variable contains, for example, a `200` HTTP status code:

```xml
<munit:test name="test-target-variable-targetVariableTestFlowTest" description="Test">
  <munit:execution >
    <flow-ref doc:name="Flow-ref to targetVariableTestFlow" name="targetVariableTestFlow"/>
  </munit:execution>
  <munit:validation >
    <munit-tools:assert-that doc:name="Assert that" expression="#[vars.httpResponse.attributes.statusCode]" is="#[MunitTools::equalTo(200)]"/>
  </munit:validation>
</munit:test>
```

If you want to test the behavior of this app without making the HTTP request, you can mock the processor and the stored target variable.

#### Mock a Processor that Stores Data in a Target Variable

The following test mocks the HTTP request and the resulting target variable from the previous Mule app example, and then asserts that the stored HTTP status code is `200`:

```xml
<munit:test name="test-target-variable-targetVariableTestFlowTest" description="Test">
  <munit:behavior >
    <munit-tools:mock-when doc:name="Mock when HTTP response" processor="http:request">
      <munit-tools:with-attributes >
        <munit-tools:with-attribute attributeName='#["doc:name"]' whereValue='#["Request"]' />
      </munit-tools:with-attributes>
      <munit-tools:then-return >
        <munit-tools:variables >
          <munit-tools:variable key="#['httpResponse']" value='#[{"attributes":{"statusCode":200}}]' />
        </munit-tools:variables>
      </munit-tools:then-return>
    </munit-tools:mock-when>
  </munit:behavior>
  <munit:execution >
    <flow-ref doc:name="Flow-ref to targetVariableTestFlow" name="targetVariableTestFlow"/>
  </munit:execution>
  <munit:validation >
    <munit-tools:assert-that doc:name="Assert that" expression="#[vars.httpResponse.attributes.statusCode]" is="#[MunitTools::equalTo(200)]"/>
  </munit:validation>
</munit:test>
```

## Configuring the Database Server Utility in an MUnit Test

If you want to test the following Mule application:

```xml
<!-- Local Database Configuration -->
<db:config name="Database_Config">
    <db:my-sql-connection host="localhost" port="1234" />
</db:config>
<!-- Properties according to the environment -->
<configuration-properties file="db.properties" />

<flow name="selectFlow" >
    <!-- Perform a query based on a value passed by a variable -->
    <db:select config-ref="${db.config}">
        <db:sql >SELECT * FROM jobtitlelookup WHERE jobtitleid = :id</db:sql>
        <db:input-parameters ><![CDATA[#[id : vars.jobid]]]></db:input-parameters>
    </db:select>
    <!-- Set two conditions depending on the query result -->
    <choice>
        <!-- If there is one or more values resulting from the query set those values as the payload -->
        <when expression="#[sizeOf(payload) > 0]">
            <set-payload value="#[payload[0].jobtitle]"/>
        </when>
        <!-- If the query throws no results, inform it in the payload  -->
        <otherwise>
            <set-payload value="#['No job title for $(vars.jobid) was found']" />
        </otherwise>
    </choice>

    <!-- Finally, pass the payload content as a Flow variable  -->
    <set-variable value="#[payload]" variableName="job" />
</flow>
```

The file `db.properties` in `src/main/resources` has the following content:

```text
db.config=Database_Config
```

You must create a test that:

- Contains a database server with a `jobtitlelookup` table.
- Provides a valid database structure for the database connector to perform its query.
- Passes a value for the `jobid` variable that Database Connector uses.

### Install the MUnit DB Server Module

1. Look for the **MUnit Utils Database Server** module.
1. Add the module to your project:
```xml
<!-- dbserver Dependency -->
<dependency>
    <groupId>com.mulesoft.munit.utils</groupId>
    <artifactId>munit-dbserver-module</artifactId>
    <version>2.0.2</version>
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
</dependency>
```

The MUnit DB server artifact in your POM file must have the `test` scope.
1. Add the `h2` dependency to your POM file and list it as `sharedLibrary` in `mule-maven-plugin`:
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

The **h2** dependency enhances MUnit tests by allowing the simulation of database interactions using an in-memory, lightweight, and fast database. This setup ensures tests are both isolated and repeatable.

The **MUnit DB Server** module is located at MuleSoft Nexus repository. The **MUnit DB Server** module version 3 and later is compatible with Java 17. Previous versions of this module available at Anypoint Exchange are deprecated.

### Define the MUnit DB Server

Define the database server by creating the **global-configs.xml** file and defining the MUnit DB Server Config element.

Define the MUnit DB Server Config element as follows:

1. Go to the `src/test/resources` directory in your project.
1. Create a file named `jobtitlelookup.csv` containing the following values:
```text
JOBTITLE,EECSALARYORHOURLY,JOBTITLEID
Developer,10,DEV
```

1. Create the **global-configs.xml** file and define the **MUnit DB Server Config** element as follows:
```xml
<dbserver:config name="MUnit_DB_Server_Config" >
    <dbserver:connection csv="jobtitlelookup.csv" database="DATABASE_NAME" connectionStringParameters="MODE=MySQL" />
</dbserver:config>
```

1. Define the DB configuration to connect to your DB server:
```xml
<db:config name="Test_Database_Config">
    <db:generic-connection url="jdbc:h2:tcp://localhost/mem:DATABASE_NAME" driverClassName="org.h2.Driver" />
</db:config>
```

1. Define the `db.properties` file in your `src/test/resources` folder that picks up your test database configuration:
```text
db.config=Test_Database_Config
```

### Run the Test

After installing and configuring the DB server you can run the test:

```xml
<munit:test name="selectFlowTest" description="Test selectFlow"  >
    <munit:behavior>
        <!-- Passes a variable to value to run in the main flow. -->
        <set-variable variableName="jobid" value="DEV" />
    </munit:behavior>
    <munit:execution>
        <!-- Run the production code. -->
        <flow-ref name="db-server-docsFlow"/>
    </munit:execution>
    <munit:validation>
        <munit-tools:assert-equals actual="#[vars.job]" expected="Developer" />
    </munit:validation>
</munit:test>
```

This test validates that the query run in your production code is correct and that the DB server returns the payload as expected.

## Configuring the FTP Server Utility in an MUnit Test

If you want to test the following Mule application:

```xml
<sftp:config name="SFTP_Config">
    <sftp:connection host="${ftp.host}" port="${ftp.port}" username="${ftp.user}" password="${ftp.password}"/>
</sftp:config>

<configuration-properties file="ftp.properties" />

<flow name="listFlow">
    <sftp:list config-ref="SFTP_Config" directoryPath="."/>
    <foreach>
        <logger level="INFO" message="#[attributes.fileName]"/>
    </foreach>
</flow>
```

The `ftp.properties` in `src/main/resources` has the following content:

```text
ftp.host=localhost
ftp.port=22
ftp.user=max
ftp.password=munittest
```

The username field can't be empty. If you don't have a username-password pair, set the username to `anonymous` and don't set any password. By default, the `anonymous` attribute is set to `true`.

### Install the FTP Server

To install the FTP server:

1. Look for the **MUnit Utils FTP Server** module.
1. Add the module to your project:
```xml
<!-- Ftp Server Dependency -->
<dependency>
    <groupId>com.mulesoft.munit.utils</groupId>
    <artifactId>munit-ftpserver-module</artifactId>
    <version>2.0.1</version>
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
</dependency>
```

The MUnit FTP server artifact in your POM file must have the `test` scope.

The **MUnit FTP Server** module is located at MuleSoft Nexus repository. The **MUnit FTP Server** module version 3 and later is compatible with Java 17. Previous versions of this module available at Anypoint Exchange are deprecated.

### Define the FTP Server

To define the FTP server, change the FTP server attributes as follows:

```xml
<ftpserver:config name="MUnit_FTP_Server_Config">
    <ftpserver:connection port="${ftp.port}" username="${ftp.user}" password="${ftp.password}" secure="true" homeDir="${app.home}"/>
```

</ftpserver:config>
```text

== Run the Test

After configuring the FTP server, you can run the test:

[source,xml,linenums]
```

<munit:test name="listFlowTest" description="Test listFlow" >
    <munit:execution>
        <flow-ref name="listFlow"/>
    </munit:execution>
    <munit:validation>
        <munit-tools:assert-that expression="#[sizeOf(payload)]" is="#[MunitTools::greaterThan(0)]"/>
    </munit:validation>
</munit:test>
```text

This FTP accepts any user, so you must not set up a user database or list.

== See Also

* xref:ftp-util.adoc[FTP Util]

```
