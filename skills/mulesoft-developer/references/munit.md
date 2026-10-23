# MUnit: suites, tests and lifecycle

> Derived from mulesoft/docs-munit (Apache 2.0).

## MUnit Overview

Build automated tests for your integrations and APIs with MUnit. MUnit is a Mule application testing framework that provides a full suite of integration and unit test capabilities, and is fully integrated with Maven and Surefire for integration with your continuous deployment environment.

MUnit version 3.0 and later works with all Mule versions since 4.3.

With MUnit you can:

- Create your test by writing Mule code
- Mock processors
- Spy any processor
- Verify processor calls
- Enable or ignore particular tests
- Tag tests
- Generate coverage reports

You can create, design, and run MUnit tests in Anypoint Studio and Anypoint Code Builder.

MUnit has two main sub modules:

- MUnit
- MUnit Tools

Each module has its dependency:

### MUnit Dependencies

```xml
<dependency>
	<groupId>com.mulesoft.munit</groupId>
	<artifactId>munit-runner</artifactId>
	<version>LATEST_VERSION</version> //<!--1-->
	<classifier>mule-plugin</classifier>
	<scope>test</scope>
</dependency>
```

  1. Check the release notes to get the **LATEST_VERSION**.

### MUnit Tools Dependencies

```xml
<dependency>
	<groupId>com.mulesoft.munit</groupId>
	<artifactId>munit-tools</artifactId>
	<version>LATEST_VERSION</version> //<!--1-->
	<classifier>mule-plugin</classifier>
	<scope>test</scope>
</dependency>
```

  1. Check the release notes to get the **LATEST_VERSION**.

## MUnit Test Structure Fundamentals

### MUnit Test Suite

The base file in MUnit is the test suite file, an XML file located in the `src/test/munit` directory of your Mule application project. You can use multiple MUnit test suite files. Each MUnit test suite file is a collection of MUnit tests and runs independently from other MUnit test suites.

An MUnit test suite can contain any combination of the following components:

- Before/After Suites
- Before/After Tests
- MUnit tests

Each MUnit test suite is similar to a Mule configuration file. You can use several of the Mule top-level elements such as flow, sub-flow, and scripts.

#### MUnit Configuration

The MUnit configuration element (`munit:config`) identifies a Mule configuration file as an MUnit suite file:

```xml

<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:munit="http://www.mulesoft.org/schema/mule/munit" xmlns:munit-tools="http://www.mulesoft.org/schema/mule/munit-tools"
	xmlns="http://www.mulesoft.org/schema/mule/core"
	xsi:schemaLocation="
		http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
		http://www.mulesoft.org/schema/mule/munit http://www.mulesoft.org/schema/mule/munit/current/mule-munit.xsd
		http://www.mulesoft.org/schema/mule/munit-tools  http://www.mulesoft.org/schema/mule/munit-tools/current/mule-munit-tools.xsd">

	<munit:config name="An MUnit Suite" />

	<!-- Tests -->

</mule>
```

##### Ignore a Suite

To ignore a whole suite from running, you can use the `ignore` attribute of the configuration:

```xml
<munit:config name="A MUnit Suite" ignore="true"/>
```

##### Minimum Mule Version

Specify the minimum required Mule version to run a test suite by defining the `minMuleVersion` attribute of the configuration:

```xml
<munit:config name="A MUnit Suite" minMuleVersion="4.1.4"/>
```

### MUnit Test

An MUnit test is the basic processor of an MUnit test suite and it represents the scenario to test.

Three optional scopes divide MUnit tests:

| Scope | Description |
|---|---|
| Behavior | The behavior scope sets all the preconditions before executing the test logic. |
| Execution | The execution scope contains the testing logic which waits for all processes to finish before executing the next scope. |
| Validation | The validation scope contains all the validations for the results of the execution scope. |

```xml

<munit:test name="exampleTest" description="Test to verify scenario 1">>

     <munit:behavior>
         <!-- Processors to set preconditions for the test -->
     </munit:behavior>

     <munit:execution>
         <flow-ref name="exampleFlow"/>
     </munit:execution>

     <munit:validation>
         <!-- Processors to validate result -->
     </munit:validation>
 </munit:test>
```

**A Studio representation of the MUnit Test**

#### MUnit Test Reference

| Name | Description |
|---|---|
| `name` | Defines the name of the test. The name must be unique in the test suite. + This attribute is mandatory. |
| `description` | Describes the scenario to test. |
| `ignore` | Defines if the test must be ignored. If not present, the test isn't ignored. |
| `tags` | Comma-separated list of tags to assign to the test. |
| `expectedErrorType` | Defines the error Type to receive after executing the test. |
| `expectedException` | Defines the exception to receive after executing the test. |
| `expectedErrorDescription` | Defines the error description to receive after executing the test. |
| `timeOut` | Defines the maximum time in milliseconds that the test can run before failing. |

##### MUnit Test Description Attribute

MUnit tests require a description. The description must be useful and representative of the tested scenario. This description shows in the test console before running the test, and also in the reports. The more representative the description, the easier it is to read and troubleshoot failures.

##### Ignore a Test

When a test fails or has inconvenient side effects, you can shut it down without commenting out the code.

To ignore a test, add the `ignore` boolean to its definition:

```xml
<munit:test name="my-flow-Test"
      ignore="true"
      description="Test to verify scenario 1">
</munit:test>
```

The default value for the ignore attribute is `false`.

You can also use expressions to ignore a test based on your current Mule version or on your current operating system:

**Ignore a Test Based on the Operating System**

```xml
<munit:test name="linux-ignore-test" ignore="#[Munit::osEqualTo('Mac OS X')]">
```

**Ignore a Test Based on Mule Runtime Engine Version**

```xml
<munit:test name="mule-version-ignore-test" ignore="#[Munit::muleVersionPriorTo('4.1.4')]">
```

MUnit ignores this test if the Mule version is earlier than `4.1.4`. Other possible functions are `muleVersionEqualTo` and `muleVersionNewerThan`.

##### Test TimeOut Attribute

An MUnit test automatically fails if it takes more than 2 minutes to complete. Use the `timeOut` attribute to set a custom maximum time --in milliseconds-- that the test can run before failing:

```xml
<munit:test
  name="custom-timeout-test"
  description="This test has a timeout of 10 seconds"
  timeOut="10000" >
  ....
</munit:test>
```

##### Test Tag Attribute

You can tag your tests and choose to run tests under a specific tag. For example:

```xml
<munit:test
  name="exampleTest"
  description="A test that works as an example"
  ignore="true"
  tags="integration,http" >
		…
</munit:test>
```

**In Anypoint Studio, you can define tags in the **Tags** field.**

##### MUnit Test Expected Error and Exception Attributes

To validate that a flow or sub-flow you're testing fails and throws a specific error, add the `expectedErrorType`, `expectException`, and `expectedErrorDescription` attributes as follows:

```xml
<munit:test name="MUnit-test-suite"
  description="A test that works as an example"
  expectedErrorType="RETRY_EXHAUSTED"
  expectedException="java.lang.RuntimeException"
  expectedErrorDescription="retries exhausted">
  ...
</munit:test>
```

**A visual representation on Anypoint Studio**

- The `expectedErrorType` attribute expects an error ID defined in the tested application. +
This attribute validates that your application throws a defined error type. If you define an `errorType` that does not exist in your application, the test doesn't run.
```xml
<munit:test name="MUnit-test-suite"
  description="Test Error Type"
  expectedErrorType="FTP:ILLEGAL_PATH">
  ...
</munit:test>
```

This Error Type test expects that an FTP operation throws an `FTP:ILLEGAL_PATH` error. +
If none of your flows are using an FTP connector, then the error type isn't defined within your application and the test doesn't run.
You mustn't typify `ErrorTypes` that belong to the Mule Runtime. For example, you can define `MULE:RETRY_EXHAUSTED` as `RETRY_EXHAUSTED`.

- The attribute `expectException` expects a literal exception class name. +
You must provide the canonical class name of the exception that you expect. MUnit then validates that the underlying cause for the exception thrown is of the same type of the class name you're expecting.
```xml
<munit:test name="testExceptions"
  description="Test Exceptions"
  expectedException="java.lang.RuntimeException">
  ...
</munit:test>
```

If you define that your test expects an exception and none is thrown, the test fails immediately.

- The attribute `expectedErrorDescription` expects an error description. +
This attribute validates that your application throws an error and the error has a description that is equal to or contains the expected error description. If you define that your test expects an error and none is thrown or the error description doesn't match, the test fails immediately.
```xml
<munit:test name="testExpectedErrorDescription"
  description="Test Expected Error Description Attribute"
  expectedErrorDescription="An error has occurred">
  ...
</munit:test>
```

### Before and After Scopes

As with other testing frameworks, MUnit provides a set of scopes so you can add processing or actions to run before and after the entire MUnit test or MUnit test suite executes:

- Before and After Suite Scopes.
- Before and After Test Scopes.

The ID field for each component must be unique across all your applications. The before and after scopes can't share the same name, nor have the same name as any flow in your application.

See before after scopes reference reference for additional information.

## Before and After Scopes

### Before Suite Scope

The MUnit Before Suite contains code that is meant to be executed before the whole suite.
The Before Suite has one execution rule: Run before all the tests, just once.

For example, suppose you have an MUnit Test Suite file with four tests. The code inside an MUnit Before Suite runs just once, before your four tests.

You can only use one Before Suite scope per MUnit test suite.

Use a Before Suite scope to set up state that every test in the suite shares, such as seeding an in-memory database, starting a server utility, or storing values that the tests read. In the example, the `jobtitlelookup.csv` file creates the table and its initial contents when the database server starts, and the Before Suite adds one shared row that all tests in the suite query:

**Before Suite example**

```xml
<dbserver:config name="MUnit_DB_Server_Config">
  <dbserver:connection csv="jobtitlelookup.csv" database="DATABASE_NAME"
    connectionStringParameters="MODE=MySQL" />
</dbserver:config>

<munit:before-suite name="before-suite" description="Adds a shared row for the whole suite">
  <dbserver:execute config-ref="MUnit_DB_Server_Config"
    sql="INSERT INTO jobtitlelookup VALUES ('Support Engineer','10','SUP');" />
</munit:before-suite>

<munit:test name="munit.test" description="Test">
  <!-- Every test in this suite can query the row added by the before-suite -->
</munit:test>
```

The `before-suite` scope is located outside the MUnit test, so the insert runs once before the first test instead of once per test.

When you place a before-suite in the Anypoint Studio canvas, the scope locates outside the MUnit test.

### After Suite Scope

The MUnit After Suite is a scope. It can contain code that is meant to be executed after the whole suite. The After suite has one execution rule: Run after all the tests, just once.

For instance, let's suppose you have an MUnit Test Suite File with four tests. The code inside an MUnit After Suite, runs just once, after all your tests.

You can only use one After Suite scope per MUnit test suite.

Use an After Suite scope to tear down whatever the Before Suite created, so the next suite run starts from a clean state. The example removes only the row that the Before Suite added, leaving the contents loaded from the CSV file untouched:

**After Suite example**

```xml
<munit:before-suite name="before.suite" description="Adds a shared row for the whole suite">
  <dbserver:execute config-ref="MUnit_DB_Server_Config"
    sql="INSERT INTO jobtitlelookup VALUES ('Support Engineer','10','SUP');" />
</munit:before-suite>

<munit:test name="munit.test" description="Test">
  <!-- some more mule code here -->
</munit:test>

<munit:after-suite name="after.suite" description="Removes the data created for the suite">
  <dbserver:execute config-ref="MUnit_DB_Server_Config"
    sql="DELETE FROM jobtitlelookup WHERE JOBTITLEID='SUP';" />
</munit:after-suite>
```

The `after-suite` scope is located outside the MUnit test, so the cleanup runs once after the last test completes.

When you place an after-suite in the Anypoint Studio canvas, the scope locates outside the MUnit test.

### Before Test Scope

The MUnit Before Test Scope contains code that is meant to be executed before each test. Each Before Test scope follows the same execution rule: Run before each test.

For instance, let's suppose you have an MUnit Test Suite file with four tests. The code inside an MUnit Before test runs before each of your four tests; it runs four times.

You can only use one Before Test scope per MUnit test suite.

Use a Before Test scope to set up state that each test needs individually, such as inserting a record, creating a file, or setting a variable that the test consumes. The following example inserts a record and sets the variable that the flow under test reads:

**Before Test example**

```xml
<munit:before-test name="before.test" description="Creates the record each test needs">
  <dbserver:execute config-ref="MUnit_DB_Server_Config"
    sql="INSERT INTO jobtitlelookup VALUES ('Culinary Team Member','10','HIR');" />
  <set-variable variableName="jobid" value="HIR" />
</munit:before-test>

<munit:test name="munit.test" description="Test">
  <munit:execution>
    <flow-ref name="selectFlow" />
  </munit:execution>
  <munit:validation>
    <munit-tools:assert-equals actual="#[vars.job]" expected="Culinary Team Member" />
  </munit:validation>
</munit:test>
```

The `before.test` scope is located outside the MUnit test, so each test starts from the same record and variable value without repeating the setup in every test.

When you place a before-test in the Anypoint Studio canvas, the scope locates outside the MUnit test.

### After Test Scope

The MUnit After Test Scope contains code that is meant to be executed after each test. Each After Test scope follows the same execution rule: Run after each test.

For instance, let's suppose you have an MUnit Test Suite file with four tests. The code inside an MUnit After Test runs after each of your four tests; it runs four times.

You can only use one After Test scope per MUnit test suite.

Use an After Test scope to undo what the Before Test created, so one test doesn't leave data behind that affects the next one. The following example deletes the record that the Before Test inserted:

**After Test example**

```xml
<munit:before-test name="before.test" description="Creates the record each test needs">
  <dbserver:execute config-ref="MUnit_DB_Server_Config"
    sql="INSERT INTO jobtitlelookup VALUES ('Culinary Team Member','10','HIR');" />
</munit:before-test>

<munit:test name="munit.test" description="Test">
  <!-- some more mule code here -->
</munit:test>

<munit:after-test name="after.test" description="Removes the record created for the test">
  <dbserver:execute config-ref="MUnit_DB_Server_Config"
    sql="DELETE FROM jobtitlelookup WHERE JOBTITLEID='HIR';" />
</munit:after-test>
```

The `after.test` scope is located outside the MUnit test, so the cleanup runs after each test rather than once after the suite.

When you place an after-test in the Anypoint Studio canvas, the scope locates outside the MUnit test.

### Before Suite Reference

| Attribute Name | Description |
|---|---|
| `name` | Defines the name of the Before suite. The name must be unique inside the suite. |
| `description` | Describes the actions performed. |

### After Suite Reference

| Attribute Name | Description |
|---|---|
| `name` | Defines the name of the After suite. The name must be unique inside the suite. |
| `description` | Describes the actions performed. |

### Before Test Reference

| Attribute Name | Description |
|---|---|
| `name` | Defines the name of the Before test. The name must be unique inside the suite. |
| `description` | Describes the actions performed. |

### After Test Reference

| Attribute Name | Description |
|---|---|
| `name` | Defines the name of the After test. The name must be unique inside the suite. |
| `description` | Describes the actions performed. |

## Enable Flow Sources

The `Enable Flow Sources` element within the MUnit test instructs MUnit which flow sources to load and execute for the test.

By default, MUnit doesn't start any of the event sources (flow sources such as triggers and listeners). You must configure which flow sources must start for your tests.

Assume that your application has a flow with an HTTP listener that returns a specific payload:

```xml
<http:listener-config name="HTTP_Listener_config">
    <http:listener-connection host="localhost" port="1234"/>
</http:listener-config>

<flow name="http-example-flow">
    <http:listener path="/" config-ref="HTTP_Listener_config"/>
    <set-payload value="#['Hello World!']" mimeType="text/plain"/>
</flow>
```

For MUnit to invoke that listener, enable the `http-example-flow` in your `enable-flow-source` property within your MUnit test:

```xml
<http:request-config name="HTTP_Request_config">
    <http:request-connection host="localhost" port="1234"/>
</http:request-config>

<munit:test name="http-example-test">
    <munit:enable-flow-sources>
        <munit:enable-flow-source value="http-example-flow"/>
    </munit:enable-flow-sources>

    <munit:execution>
        <http:request method="GET" path="/" config-ref="HTTP_Request_config"/>
    </munit:execution>

    <munit:validation>
        <munit-tools:assert-that expression="#[payload]"
                                 is="#[MunitTools::equalTo('Hello World!')]"/>
    </munit:validation>
</munit:test>
```

If the `http-example-flow` value isn't listed as an enabled flow source, your MUnit test fails because it can't initialize the HTTP listener configuration.

MUnit starts flow sources at the beginning of the test and stops them at the end of the test. Flow sources aren't executed during the before-suite/before-test, nor during the after-test/after-suite. +
See Before/After scopes for additional information.

## Parameterized

A parameterized test suite runs the same tests but with different inputs.

The test suite parameterization is defined at a configuration level as follows:

```xml
<munit:config>
    <munit:parameterizations>
        <munit:parameterization name="firstParameterization">
            <munit:parameters>
                <munit:parameter propertyName="name" value="Robert"/>
                <munit:parameter propertyName="lastname" value="Plant"/>
            </munit:parameters>
        </munit:parameterization>
        <munit:parameterization name="secondParameterization">
            <munit:parameters>
                <munit:parameter propertyName="name" value="Jimmy"/>
                <munit:parameter propertyName="lastname" value="Page"/>
            </munit:parameters>
        </munit:parameterization>
    </munit:parameterizations>
</munit:config>
```

The Test Suite runs twice: Firstly, with the `firstParameterization` parameters. Secondly, with the `secondParameterization` parameters.

For example, if you have a test that sets a payload for a flow and expects a result:

**Parameterization Example**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns="http://www.mulesoft.org/schema/mule/core"
      xmlns:munit="http://www.mulesoft.org/schema/mule/munit"
      xmlns:munit-tools="http://www.mulesoft.org/schema/mule/munit-tools"
      xsi:schemaLocation="
        http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
        http://www.mulesoft.org/schema/mule/munit http://www.mulesoft.org/schema/mule/munit/current/mule-munit.xsd
        http://www.mulesoft.org/schema/mule/munit-tools http://www.mulesoft.org/schema/mule/munit-tools/current/mule-munit-tools.xsd">

    <munit:config name="parameterized-test.xml">
        <munit:parameterizations>
            <munit:parameterization name="sumThree">
                <munit:parameters>
                    <munit:parameter propertyName="input" value="#[1]"/>
                    <munit:parameter propertyName="output" value="#[2]"/>
                </munit:parameters>
            </munit:parameterization>
            <munit:parameterization name="sumFive">
                <munit:parameters>
                    <munit:parameter propertyName="input" value="#[2]"/>
                    <munit:parameter propertyName="output" value="#[4]"/>
                </munit:parameters>
            </munit:parameterization>
        </munit:parameterizations>
    </munit:config>

    <munit:test name="expectFlowResult">
        <munit:behavior>
            <set-payload value="${input}"/>
        </munit:behavior>
        <munit:execution >
            <flow-ref name="myFlow"/>
        </munit:execution>
        <munit:validation>
            <munit-tools:assert-equals actual="#[payload]" expected="${output}" />
        </munit:validation>
    </munit:test>

</mule>
```

### Access Parameters from DataWeave

Use the DataWeave `p()` function to access parameter values inside DataWeave expressions, concatenate parameter values with other strings, perform comparisons or calculations, and use parameters in complex DataWeave transformations.

Using the parameterization from the first example, the following test uses `p()` to build a greeting message and validate that the payload contains the expected name:

**Accessing Parameters with the p() Function**

```xml
<munit:test name="validateGreeting">
    <munit:behavior>
        <set-payload value="#['Hello, ' ++ p('name') ++ ' ' ++ p('lastname')]"/>
    </munit:behavior>
    <munit:validation>
        <munit-tools:assert-that 
          expression="#[payload contains p('name')]" 
          is="#[MunitTools::equalTo(true)]"/>
    </munit:validation>
</munit:test>
```

### Parameterization from File

To use the same parameterized values on different test suites, you must save your parameterizations values in a YAML file in the `/test/resources` directory of your Mule application project:

**parameterizations.yaml Example**

```yaml
firstParameterization:
    name: "Robert"
    lastname: "Plant"

secondParameterization:
    name: "Jimmy"
    lastname: "Page"
```

And reference it from your test suite configuration:

**Example Parameterization From File**

```xml
<munit:config>
    <munit:parameterizations file="parameterizations.yaml" />
</munit:config>
```

You can combine both methods to add parameterized values to a test suite:

**Example Parameterization From File and in the Test Suite Configuration**

```xml
<munit:config name="parameterization-from-file-test.xml">
    <munit:parameterizations file="parameterizations.yaml" >
        <munit:parameterization name="thirdParameterization">
            <munit:parameters>
                <munit:parameter propertyName="name" value="John"/>
                <munit:parameter propertyName="lastname" value="Bonham"/>
            </munit:parameters>
        </munit:parameterization>
    </munit:parameterizations>
</munit:config>
```

If you define the same parameterization key in a YAML file and your test suite configuration, the test suite parameterization overrides your YAML parameterization.

## Reading MUnit Results

This section briefly explains how to read the MUnit console logs.

**Successful Build**

```text
============================================================
============  Running  new-test-suite.xml suite ============
============================================================
++++++++++++++++++++++++++++++++++++++++++++
+ Running test: test-suite - Test          +
++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ SUCCESS - Test test-suite finished successfully - Time elapsed: 2227ms +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

==================================================================================
Number of tests run: 1 - Failed: 0 - Errors: 0 - Skipped: 0 - Time elapsed: 2241ms
==================================================================================

[INFO] ====================================================================================
[INFO] MUnit Run Summary
[INFO] ====================================================================================
[INFO]  >> new-test-suite.xml test result: Tests: 1, Errors: 0, Failures: 0, Skipped: 0
[NOTE]
[INFO] ====================================================================================
[INFO]  > Tests:   	1
[INFO]  > Errors:  	0
[INFO]  > Failures:	0
[INFO]  > Skipped: 	0
[INFO] ====================================================================================
```

**Failed Build**

```text
============================================================
============  Running  new-test-suite.xml suite ============
============================================================
++++++++++++++++++++++++++++++++++++++++++++
+ Running test: test-suite - Test          +
++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ FAILURE - The test test-suite finished with a failure - Time elapsed: 2399ms +
java.lang.AssertionError:
Expected: "Bye World!"
     but: was "Hello World"
	at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:20)
	at org.mule.munit.assertion.internal.AssertModule.assertThat(AssertModule.java:34)
	at org.mule.munit.tools.assertion.AssertOperations.assertThat(AssertOperations.java:45)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

==================================================================================
Number of tests run: 1 - Failed: 1 - Errors: 0 - Skipped: 0 - Time elapsed: 2416ms
==================================================================================

[INFO] ====================================================================================
[INFO] MUnit Run Summary
[INFO] ====================================================================================
[INFO]  >> new-test-suite.xml test result: Tests: 1, Errors: 0, Failures: 1, Skipped: 0
[INFO] 	 --- test-suite <<< FAILED
[NOTE]
[INFO] ====================================================================================
[INFO]  > Tests:   	1
[INFO]  > Errors:  	0
[INFO]  > Failures:	1
[INFO]  > Skipped: 	0
[INFO] ====================================================================================
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 22.400 s
[INFO] Finished at: 2017-11-16T14:37:32-03:00
[INFO] Final Memory: 19M/302M
[INFO] ------------------------------------------------------------------------
```

**Build Error**

```text
============================================================
============  Running  new-test-suite.xml suite ============
============================================================
++++++++++++++++++++++++++++++++++++++++++++
+ Running test: test-suite - Test          +
++++++++++++++++++++++++++++++++++++++++++++
ERROR 2017-11-16 14:40:20,239 [[coverage].http.requester.HTTP_Request_configuration.01: [coverage].http.requester.HTTP_Request_configuration @55ccbf06 SelectorRunner] org.mule.extension.http.internal.request.HttpRequester: Error sending HTTP request to http://0.0.0.0:8081/
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ ERROR - The test test-suite finished with an error - Time elapsed: 218ms +
java.util.concurrent.ExecutionException: org.mule.runtime.api.component.execution.ComponentExecutionException: org.mule.extension.http.api.error.HttpRequestFailedException: HTTP GET on resource 'http://0.0.0.0:8081/' failed: Connection refused.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

[INFO] ====================================================================================
[INFO] MUnit Run Summary
[INFO] ====================================================================================
[INFO]  >> new-test-suite.xml test result: Tests: 1, Errors: 1, Failures: 0, Skipped: 0
[INFO] 	 --- test-suite <<< ERROR
[NOTE]
[INFO] ====================================================================================
[INFO]  > Tests:   	1
[INFO]  > Errors:  	1
[INFO]  > Failures:	0
[INFO]  > Skipped: 	0
[INFO] ====================================================================================
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 20.167 s
[INFO] Finished at: 2017-11-16T14:40:27-03:00
[INFO] Final Memory: 25M/315M
[INFO] ------------------------------------------------------------------------
```

## Coverage

The MUnit Coverage feature provides a measurement of how much of a Mule application has been executed by a set of MUnit tests by counting the amount of event processors executed. This allows you to obtain a quality standard for your application, and provides metrics for:

- Application overall coverage: An average of the items below.
- Resource coverage: Refers to each Mule configuration file under src/main/mule.
- Flow coverage: Refers to any of the following components: Flows, Sub-flows, and Batch jobs.

Coverage report runs only for EE edition runtimes. If your application has a `requiredProduct` of a Mule CE runtime you will see the following message: **Coverage is a EE only feature and you've selected to run over CE**. To run against an EE runtime see Specifying the Runtime Product.

The following is a coverage report sample in JSON format. +
Use the code callouts below to understand each field in the report:

**MUnit Coverage - sample JSON report**

```json
{
  "coverage": 75.0, <1>
  "requiredApplicationCoverage": 40.0, <2>
  "requiredResourceCoverage": 30.0,    <2>
  "requiredFlowCoverage": 25.0,        <2>
  "flowCount": 3,             <3>
  "processorCount": 4,        <4>
  "coveredProcessorCount": 3, <5>
  "files": [ {
    "name": "file1.xml", <6>
    "flowCount": 1,      <7>
    "coverage": 100.0,   <8>
    "processorCount": 2, <9>
    "weight": 50.0,     <10>
    "flows": [ {
      "name": "file1Flow1", <11>
      "type": "FLOW",       <12>
      "coverage": 100.0,    <13>
      "messageProcessorCount": 2, <14>
      "coveredProcessorCount": 2, <15>
      "lines": [ { <16>
        "lineNumber": 11,
        "covered": true
      }, {
        "lineNumber": 12,
        "covered": true
      } ]
    } ]
  }, {
    "name": "file2.xml",
    "flowCount": 2,
    "coverage": 50.0,
    "processorCount": 2,
    "weight": 50.0,
    "flows": [ {
      "name": "file2Flow2",
      "type": "SCOPE",
      "coverage": 100.0,
      "messageProcessorCount": 1,
      "coveredProcessorCount": 1,
      "lines": [ {
        "lineNumber": 10,
        "covered": true
      } ]
    }, {
      "name": "file2Flow1",
      "type": "SCOPE",
      "coverage": 0.0,
      "messageProcessorCount": 1,
      "coveredProcessorCount": 0,
      "lines": [  {
        "lineNumber": 7,
        "covered": false
      } ]
    } ]
  } ]
}
```

<1>  Coverage percentage of the whole application.
<2>  Required coverages for application, resources, and flows. If not configured, they default to -1.
<3>  Amount of flows in the application.
<4>  Amount of event processors in the application.
<5>  Amount of covered event processors.
<6>  Name of that file.
<7>  Amount of flows in that file.
<8>  Coverage percentage of that file.
<9>  Amount of event processors in that file.
<10> Contribution of that file to the coverage percentage of the whole application.
<11> Name of the flow.
<12> Type of the top level element. +
     Other type of top level element in coverage is error-handler.
<13> Coverage percentage of that flow.
<14> Amount of event processors in that flow.
<15> Amount of event processors covered in that flow.
<16> XML line numbers containing event processors in that file, and whether they were covered or not.

## Maven Configuration for Coverage

From MUnit 2.x and later, the coverage report goal is integrated with the Maven reporting section. MUnit generates coverage reports during the Maven `site` lifecycle, during the `coverage-report` goal.

The following configurations apply if you execute your MUnit tests using the Maven plugin. They don't apply when running tests from Anypoint Code Builder or Anypoint Studio.

**MUnit Coverage - Sample Maven configuration**

```xml
<plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <version>${munit.version}</version>

    <executions>
        <execution>
            <id>test</id>
            <phase>test</phase>
            <goals>
                <goal>test</goal>
                <goal>coverage-report</goal>
            </goals>
        </execution>
    </executions>

    <configuration>
        <coverage>
            <runCoverage>true</runCoverage>
            <failBuild>false</failBuild>

            <requiredApplicationCoverage>75</requiredApplicationCoverage>
            <requiredResourceCoverage>50</requiredResourceCoverage>
            <requiredFlowCoverage>50</requiredFlowCoverage>

            <formats>
                <format>console</format>
                <format>html</format>
            </formats>
        </coverage>
    </configuration>
</plugin>
```

### Coverage Report Types

When you enable MUnit Coverage, the console displays a summary report.

```text
===============================================================================
MUnit Coverage Summary
===============================================================================
 * Resources: 2 - Flows: 3 - Processors: 4
 * Application Coverage: 75.00%
====================================================================================
```

MUnit Coverage offers four types of reports:

- Console report +
The console report prints in the console. It works with the summary report and shows an overview of the MUnit run, with a count of all resources, flows, and processors, as well as the overall application coverage level, and warnings and errors if any.

- HTML report +
The HTML report shows the same information as the console report but is formatted to fit any web browser. It's available in the `${application.path}/target/site/munit/coverage/` path.

- JSON report +
The JSON report provides the same information as the HTML report but in a JSON format. It's available at `${application.path}/target/site/munit/coverage/munit-coverage.json`.

- SONAR report +
The SONAR report shows the same information as the HTML report, in a SonarQube format.

To enable the report generation, add the following configuration:

**MUnit Coverage - Report Configuration**

```xml
<coverage>
    <runCoverage>true</runCoverage>

    <formats>
        <format>console</format> <1>
        <format>html</format>    <2>
        <format>json</format>    <3>
        <format>sonar</format>   <4>
    </formats>
</coverage>
```

<1> Console report
<2> HTML report
<3> JSON report
<4> SONAR report

You can choose to have either none, one, or all the report types added to your configuration.

To configure, for example, the JSON report generation, add the following configuration to your `pom.xml` file:

```xml
<coverage>
    <runCoverage>true</runCoverage>

    <formats>
        <format>json</format>
    </formats>
</coverage>
```

### Set up a Minimum Coverage Level

One of the features of MUnit Coverage is to fail the build if a certain coverage level isn't reached.

MUnit Coverage handles three different levels:

- **Application**: The overall coverage of all your application.
- **Resource**: The coverage level of each Mule configuration file.
- **Flow**: The coverage of event processors in each flow.

To define the required coverage levels:

**MUnit Coverage - Require Coverage**

```xml
<coverage>
    <runCoverage>true</runCoverage>
    <failBuild>true</failBuild>

    <requiredApplicationCoverage>75</requiredApplicationCoverage> //<1>
    <requiredResourceCoverage>50</requiredResourceCoverage>
    <requiredFlowCoverage>50</requiredFlowCoverage>
</coverage>
```

<1> Each value represents a percentage. +
If a percentage isn't defined, it defaults to **-1**, which sets no requirements for said level so the build doesn't fail due to low coverage.

If you define coverage levels but set the property `failBuild` to `false`, and then the levels aren't reached, a warning shows up in the MUnit Coverage summary:

```text
===============================================================================
MUnit Coverage Summary
===============================================================================
 * Resources: 2 - Flows: 3 - Processors: 4
 * Application Coverage: 75.00%
```

 * Flow: file2.xml -> file2Flow1 coverage is below defined limit. Required: 50.0% - Current: 00.00% <1>
====================================================================================
```text
<1> Warning detailing which coverage level isn't met, and where it happens.

== Ignore a Flow or a File

You can also ignore a flow or a file. This way, the ignored resource:

* Does not count as coverage data.
* Does not affect the overall number of message processors.
* Does not cause a build to fail if the flow isn't tested or if the flow doesn't reach coverage metrics.

To ignore flows and files:

.MUnit Coverage - Ignore flows and files
[source,xml,linenums]
```

<coverage>
    <runCoverage>true</runCoverage>
    <failBuild>true</failBuild>

    <requiredApplicationCoverage>100</requiredApplicationCoverage>
    <requiredResourceCoverage>100</requiredResourceCoverage>
    <requiredFlowCoverage>100</requiredFlowCoverage>

    <ignoreFlows>
        <ignoreFlow>flow-1</ignoreFlow>
        <ignoreFlow>flow-2</ignoreFlow>
        ...
        <ignoreFlow>flow-n</ignoreFlow>
    </ignoreFlows>

    <ignoreFiles>
        <ignoreFile>mule-config-1.xml</ignoreFile>
        <ignoreFile>mule-config-2.xml</ignoreFile>
        ...
        <ignoreFile>mule-config-n.xml</ignoreFile>
    </ignoreFiles>
</coverage>
```text

// end::coverage-report[]

== See Also

* xref:munit-coverage-report.adoc[Coverage Report]
* xref:coverage-studio-concept.adoc[].

```

## MUnit Maven Plugin

MUnit provides a Maven plugin that enables you to run your MUnit tests as part of your continuous integration environment.

The following configurations to the `pom.xml` or `settings.xml` files of your Maven installation apply only when running MUnit through Maven.

### Set Up MUnit Maven Plugin

You must have the `<munit.version>` property in your pom.xml to set up MUnit Maven Plugin.

- Enable MUnit Maven Plugin in your `pom.xml` file:
**MUnit Maven Plugin**

```xml
<build>
  <plugins>
  ...

    <plugin>
      <groupId>com.mulesoft.munit.tools</groupId>
      <artifactId>munit-maven-plugin</artifactId>
      <version>${munit.version}</version>
      <executions>
        <execution>
          <id>test</id>
          <phase>test</phase>
          <goals>
            <goal>test</goal>
          </goals>
        </execution>
      </executions>
    </plugin>

  ...
  </plugins>
</build>
```

- Add MUnit dependencies to your `pom.xml` file:
**Dependencies**

```xml
<dependencies>
  ...
  <dependency>
    <groupId>com.mulesoft.munit</groupId>
    <artifactId>munit-runner</artifactId>
    <version>${munit.version}</version>
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>com.mulesoft.munit</groupId>
    <artifactId>munit-tools</artifactId>
    <version>${munit.version}</version>
    <classifier>mule-plugin</classifier>
    <scope>test</scope>
  </dependency>
  ...
</dependencies>
```

- Configure the repositories for the MUnit dependencies and plugin:
**Repositories**

```xml
<repositories>
  <repository>
    <id>mulesoft-releases</id>
      <name>MuleSoft Releases Repository</name>
      <url>https://repository.mulesoft.org/releases/</url>
      <layout>default</layout>
    </repository>
</repositories>
```

**Plugin Repositories**

```xml
<pluginRepositories>
  <pluginRepository>
    <id>mulesoft-release</id>
    <name>mulesoft release repository</name>
    <layout>default</layout>
    <url>https://repository.mulesoft.org/releases/</url>
    <snapshots>
      <enabled>false</enabled>
    </snapshots>
  </pluginRepository>
</pluginRepositories>
```

MUnit has Surefire support built in. The reports output to `target/surefire-reports`.

#### Handle Parent POM Files

You can declare the MUnit plugin in a parent `pom.xml` file and every child project under this file can reference this definition.

To configure MUnit Maven Plugin in a parent-child POM relationship, include the MUnit plugin declaration in the `<pluginManagement>` section of your parent `pom.xml` file.

In the following example, the `pirate-pom` project declares MUnit Maven Plugin in its plugin management section. This section also defines a global configuration that each child under this parent can reference, override, or ignore.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.1.0</modelVersion>

    <groupId>org.pirate</groupId>
    <artifactId>pirate-pom</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <properties>
        <munit.version>2.3.0</munit.version>
    </properties>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>com.mulesoft.munit.tools</groupId>
                    <artifactId>munit-maven-plugin</artifactId>
                    <version>${munit.version}</version>
                    <executions>
                        <execution>
                            <id>test</id>
                            <phase>test</phase>
                            <goals>
                                <goal>test</goal>
                            </goals>
                        </execution>
                    </executions>
                    <configuration>
                      <coverage>
                          <runCoverage>true</runCoverage>
                          <failBuild>false</failBuild>
                          <requiredApplicationCoverage>0</requiredApplicationCoverage>
                          <requiredResourceCoverage>0</requiredResourceCoverage>
                          <requiredFlowCoverage>0</requiredFlowCoverage>
                          <formats>
                              <format>console</format>
                              <format>html</format>
                          </formats>
                      </coverage>
                    </configuration>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

#### Inherit a Parent Plugin

To inherit the MUnit plugin in your child `pom.xml` files, reference it in the `<plugin>` section of each child POM file individually.

The following sample references the `pirate-pom` file as its parent. It declares the MUnit plugin in a `<plugin>` section without specifying its `<version>` because the MUnit plugin configuration is inherited from the `<pluginManagement>` section in the parent POM file:

**POM child file sample**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">

    <parent>
        <groupId>org.pirate</groupId>
        <artifactId>pirate-pom</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <modelVersion>4.0.0</modelVersion>
    <groupId>com.mycompany</groupId>
    <artifactId>ninja</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>mule</packaging>
    <name>Mule ninja Application</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <app.runtime>4.1.4</app.runtime>
        <munit.version>2.3.0</munit.version>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>com.mulesoft.munit.tools</groupId>
                <artifactId>munit-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Ignore a Parent Plugin

Each child project under a parent `pom.xml` file can ignore the plugin referenced in the parent plugin management section and not implement the plugin configuration declared there.

By not declaring the MUnit Plugin in your `<plugin>` section, you avoid inheriting the plugin declared in **pirate-pom**:

**Child POM file not inheriting the MUnit Maven Plugin**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">

    <parent>
        <groupId>org.pirate</groupId>
        <artifactId>pirate-pom</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <modelVersion>4.0.0</modelVersion>
    <groupId>com.mycompany</groupId>
    <artifactId>ninja</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>mule</packaging>
    <name>Mule ninja Application</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <mule.version>4.1.0</mule.version>
        <munit.version>2.3.0</munit.version>
    </properties>

    <build>
        <plugins>
            <plugin>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Override a Parent Plugin

When inheriting the plugin from a parent POM file, you can also override the parent configuration. Overriding the plugin configuration from your parent POM file suppresses the original configuration requiring you to declare all necessary configurations again.

The following example overrides the console coverage report from its parent POM file, replacing it with the HTML report. Because the values from the other elements in the parent (`<failBuild>`, `<requiredApplicationCoverage>`, `<requiredResourceCoverage>`, `<requiredFlowCoverage>`) aren't being referenced, this child file won't inherit them and the default values are applied:

**Coverage configuration in parent POM file**

```xml
<coverage>
	<runCoverage>true</runCoverage>
	<failBuild>false</failBuild>
	<requiredApplicationCoverage>0</requiredApplicationCoverage>
	<requiredResourceCoverage>0</requiredResourceCoverage>
	<requiredFlowCoverage>0</requiredFlowCoverage>
	<formats>
		<format>console</format>
		<format>html</format>
	</formats>
</coverage>
```

**POM child file overriding coverage report format**

```xml
<plugin>
	<groupId>com.mulesoft.munit.tools</groupId>
	<artifactId>munit-maven-plugin</artifactId>
	<configuration>
		<coverage>
			<runCoverage>true</runCoverage>
			<formats>
				<format>html</format>
			</formats>
		</coverage>
	</configuration>
</plugin>
```

### Set Up Coverage

The following configurations only apply when you execute your MUnit tests using the Maven plugin. They don't apply when running tests from Studio. See Using Coverage in Maven for additional information.

### Dynamic Ports

MUnit 2.2 and later introduce the `dynamic-port` global element, that allows you to define dynamic ports at the MUnit suite level. Using this element instead of the plugin configuration described as follows allows you to set the dynamic port both from Maven and Studio. +
See Dynamic Ports to learn how to configure this element.

When testing a Mule application in a continuous integration (CI) environment, you might encounter the following scenario:

```text
Your application tries to open a specific port. The port is already in use. The application fails with a port binding exception.
```

The MUnit Maven Plugin comes with a built-in feature to make your application use a free port.

MUnit Dynamic Ports instructs the MUnit Maven Plugin to look for unbound ports and reserve them before running the tests over the Mule application. Each port selected is placed in a system property under the name indicated in the configuration. The application can get the port number through the use of placeholders afterward.

The plugin selects the ports from the range: `[40000,50000]`

Dynamic Ports feature is only available as part of the MUnit Maven Plugin. This feature does not work when running tests in Anypoint Studio.

#### Enable Dynamic Ports

To enable the feature, you must add the following code to the `configuration` section of the MUnit Maven Plugin:

**Dynamic Ports Configuration**

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
    ...
    <dynamicPorts>
      <dynamicPort>a.dynamic.port</dynamicPort>
    </dynamicPorts>
    ...
    </configuration>
  </plugin>
</plugins>
```

If you have the `${http.port}` placeholder in your application, the configuration looks something like:

**Example**

```xml
<dynamicPorts>
  <dynamicPort>http.port</dynamicPort>
</dynamicPorts>
```

#### Prepare Your Application

A placeholder must parameterize the part of the application trying to make use of a port. For example, to have your Mule application listening for HTTP traffic, provide the following configuration:

**HTTP Application**

```xml
<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>

<flow name="httpFlow">
  <http:listener path="/" config-ref="HTTP_Listener_config"/>
</flow>
```

The previous application always listens in port `8081`. To make it dynamic, change it to:

**HTTP Application with dynamic port**

```xml
<http:listener-config name="HTTP_Listener_config">
  <http:listener-connection host="0.0.0.0" port="${http.port}"/> //<1>
</http:listener-config>

<flow name="httpFlow">
  <http:listener path="/" config-ref="HTTP_Listener_config"/>
</flow>
```

<1> Notice the placeholder `${http.port}`.

With the application coded in this way and the configuration of Dynamic Ports in place, your application starts each run listening on a different port.

### Enable Surefire Reports

MUnit has built-in support for Surefire. You mustn't do additional configurations, and you can disable it if not needed:

**Disable Surefire reports**

```text
<enableSurefireReports>false</enableSurefireReports>
```

You can find the reports under `${project.build.directory}/surefire-reports`.

By default, it's set to `true`.

### Enable Sonar Reports

MUnit has built-in support for SonarQube, with a default setting of `true` for `enableSonarReports`. No other configuration is required.

You can find the reports under `${project.build.directory}/sonar-reports`.

You can disable SONAR reports if not needed:

**Disable Sonar reports**

```text
<enableSonarReports>false</enableSonarReports>
```

You can find the reports under `${project.build.directory}/sonar-reports`.

By default, it's set to `true`.

### Run Tests Using the Plugin

#### Run MUnit Tests for a Mule Application

**Run MUnit tests in a Single Resource Mule project.**

```text
mvn clean test
```

#### Run a Specific MUnit Test Suite

By using the property `munit.test`, you can instruct the MUnit Maven plugin to run certain tests that belong to a specific test suite:

```text
mvn clean test -Dmunit.test=<regex-test-suite>
```

This path is relative to `src/test/munit`.

The property `munit.test` accepts regular expressions. The expression is applied to the name of the MUnit Test Suite file. The regular expression language is the Java implementation. +

For example:

```text
mvn clean test -Dmunit.test=.*my-test.*
```

You can leverage this feature by adding naming conventions to your MUnit Test suites.

#### Run Specific MUnit Tests

In the same way that you instruct MUnit to run one test suite, you can also configure it to run a specific test in that test suite. You must use the property `munit.test` with the addition of the special character `#` to append the test name:

```text
mvn clean test -Dmunit.test=<regex-test-suite>#<regex-test-name>
```

It also accepts regular expressions. The expression is applied to the attribute `name` of the MUnit Test. For example:

```text
mvn clean test -Dmunit.test=.*my-test.*#.*test-scenario-1.*
```

MUnit flags the tests in the MUnit Test Suite that don't match the regular expression as **ignored**.

You can also configure this from the `pom.xml` configuration:

```xml
<plugins>
  <plugin>
      <groupId>com.mulesoft.munit.tools</groupId>
      <artifactId>munit-maven-plugin</artifactId>
      <configuration>
      ...
      <munitTest>example-MunitTest-suite.xml</munitTest>
      ...
    </configuration>
  </plugin>
</plugins>
```

#### Run Tests Using a Specific Tag

You can run the tests that you grouped under one specific tag:

```text
mvn clean test -Dmunit.tags=<munit-tag>
```

You can also configure this from the `pom.xml` configuration:

```xml
<plugins>
  <plugin>
      <groupId>com.mulesoft.munit.tools</groupId>
      <artifactId>munit-maven-plugin</artifactId>
      <configuration>
      ...
      <munitTags>exampleMunitTag</munitTags>
      ...
    </configuration>
  </plugin>
</plugins>
```

You can specify more than one tag by separating them with a comma.

#### Skip All Tests

MUnit leverages the same mechanism as Maven. To skip tests, you must use the `skipTests` parameter:

**Skip Tests example**

```text
mvn clean package -DskipTests
```

You can also configure this from the `pom.xml` configuration:

```xml
<plugins>
  <plugin>
      <groupId>com.mulesoft.munit.tools</groupId>
      <artifactId>munit-maven-plugin</artifactId>
      <configuration>
      ...
      <skipMunitTests>true</skipMunitTests>
      ...
    </configuration>
  </plugin>
</plugins>
```

#### Skip Tests After One Suite Fails

MUnit allows you to skip the rest of the tests if one test suite fails:

```xml
<plugins>
  <plugin>
      <groupId>com.mulesoft.munit.tools</groupId>
      <artifactId>munit-maven-plugin</artifactId>
      <configuration>
      ...
      <skipAfterFailure>true</skipAfterFailure>
      ...
    </configuration>
  </plugin>
</plugins>
```

If not specified, it's default value is `false`.

### Specify the Runtime Product

You can specify the type of runtime in which the applications you test run. Accepted values are:

- `MULE` for the Mule Kernel (formerly called Mule Community Edition)
- `MULE_EE` for the Mule Enterprise Edition

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <runtimeProduct>MULE</runtimeProduct>
      ...
    </configuration>
  </plugin>
</plugins>
```

#### Specify the Runtime Product Version

You can specify the runtime version in which the applications you test run.

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <munit.runtimeversion>4.2.2</munit.runtimeversion>
      ...
    </configuration>
  </plugin>
</plugins>
```

The `munit.runtimeversion` property replaces the deprecated `runtimeVersion` property. The `runtimeVersion` property remains supported. If you use `runtimeVersion`, MUnit displays a warning message that indicates the property is deprecated and that you must migrate to `munit.runtimeversion`.

### Specify the JVM

You can specify the JVM (or the Java executable) in which the applications you test run. You must populate the `munit.jvm` parameter with the path to the executable:

**Specify the JVM**

```text
mvn clean package -Dmunit.jvm=/path/to/jdk/bin/java
```

You can also configure this from the `pom.xml` configuration:

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <jvm>/path/to/jdk/bin/java</jvm>
      ...
    </configuration>
  </plugin>
</plugins>
```

#### Additional Argument Lines

You can pass additional argument lines to the JVM. Specify each argument in a separate `argLine`:

**Argument lines**

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <argLines>
          <argLine>-XX:MaxPermSize=512m</argLine>
          <argLine>-Xmx1024m</argLine>
      </argLines>
      ...
    </configuration>
  </plugin>
</plugins>
```

#### Environment Variables

To set additional environment variables during the test run, you can specify them with the respective key and value:

**Additional Environment Variables**

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <environmentVariables>
        <MY_ENV>exampleValue</MY_ENV>
        <MY_OTHER_ENV>val2</MY_OTHER_ENV>
      </environmentVariables>
      ...
    </configuration>
  </plugin>
</plugins>
```

As shown in the previous example, you can use environment variables to replace placeholders such as `$\`.

#### System Properties Variables

If you must define specific system variables to run your MUnit test successfully:

**Setting system property variables**

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <systemPropertyVariables>
        <my.property.key>my.property.value</my.property.key>
      </systemPropertyVariables>
      ...
    </configuration>
  </plugin>
</plugins>
```

Depending on the execution context, the system property values can vary. When referencing these properties, you must override their value to enforce test reproducibility.

You can do so by using the ­`-D` argument when running MUnit with Maven. Variables passed with the `-D` argument take full priority over any other property. For example:

```text
-Dmy.property.key=my.property.another.value
```

### Redirect Test Output to File

When running several tests, the build output can get very complex to read. MUnit allows you to redirect the output of each test suite to a file. This way, the test results remain in the build output and you can check the respective file to check the standard output of each test suite.

You can find these files in the `testOutputDirectory` folder following the naming convention: `munit.$\-output.txt`, where `suiteName` represents the name of the XML file relative to the MUnit test folder.

The test output that doesn't belong to a particular suite isn't printed to keep the build output clean. You can enable it by running Maven in debug mode.

To redirect the output of each test suite to a file:

**Redirect test output to a file**

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <redirectTestOutputToFile>true</redirectTestOutputToFile>
      ...
    </configuration>
  </plugin>
</plugins>
```

By default, it's set to `false`.

#### Test Output Directory

If you want to choose the location where the test creates the output files, the path specified can be absolute or written as a Maven placeholder:

**Test output directory with absolute path**

```xml
<plugins>
  <plugin>
    <groupId>com.mulesoft.munit.tools</groupId>
    <artifactId>munit-maven-plugin</artifactId>
    <configuration>
      ...
      <testOutputDirectory>/my/absolute/path</testOutputDirectory>
      ...
    </configuration>
  </plugin>
</plugins>
```

**Test output directory using Maven placeholders**

```xml
<testOutputDirectory>${project.build.directory}/my/output/folder</testOutputDirectory>
```

By default, the files are created in `${project.build.directory}/munit-reports/output/`.

### MUnit Maven Plugin Configuration Reference

The MUnit Maven Plugin offers a set of optional configurable parameters.

**Maven Plugin Parameters**

| Name | Type | Description |
|---|---|---|
| `argLines` | List | Additional JVM argument lines to set on the test run. |
| `coverage` | Configuration | Coverage configuration to set on the test run. |
| `dynamicPorts` | List | Dynamic ports to set on the test run. |
| `enableSurefireReports` | boolean | Set value to `true` to generate MUnit test results in the Surefire format. + Its default value is `true`. |
| `munitTest` | String | Name of the MUnit tests to run. |
| `munitTags` | String | Name of the MUnit tags. Tests tagged with these names run. |
| `skipMunitTests` | boolean | Setting this parameter to `true` skips all MUnit tests. + Its default value is `false`. |
| `skipAfterFailure` | boolean | Skip all tests if one fails. + Its default value is `false`. |
| `munitTestsDirectory` | File | Directory where the MUnit tests reside. + Its default value is `${project.build.directory}/test-mule/munit`. |
| `munit.runtimeversion` | String | Version of the Mule runtime + When you run your tests from Maven, this value comes from the `minMuleVersion` parameter in the `mule-artifact.json` file. + To modify the Mule runtime version used to run your MUnit tests, see Runtime Patching. |
| `runtimeVersion` (deprecated) | String | Deprecated alias for `munit.runtimeversion`. + This property remains supported for backward compatibility. + When you use this property, MUnit displays a warning message and instructs you to migrate to `munit.runtimeversion`. |
| runtimeProduct | String | Type of runtime. Expected values are: · `MULE` for the Mule Kernel (formerly called Mule Community Edition) · `MULE_EE` for the Mule Enterprise Edition By default, this value comes from the `requiredProduct` parameter in the `mule-artifact.json` file. |
| `jvm` | String | Option to specify the JVM (or path to the Java executable) to use. By default, the JVM is the same VM as the one used to run Maven. |
| `environmentVariables` | Map | Additional environment variables to set on the test run. |
| `redirectTestOutputToFile` | boolean | Setting this value to `true` redirects the MUnit tests standard output to a file. + Its default value is `false`. |
| `systemPropertyVariables` | Map | System properties set on the test run. |
| `testOutputDirectory` | File | Directory where the test outputs are written. + Its default value is `${project.build.directory}/munit-reports/output/`. |
