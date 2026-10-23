# Logging and debugging

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Configuring Logging

MuleSoft provides application logs and a runtime log to help you monitor and troubleshoot your Mule applications and the Mule instance.

### App Logs

Every app that you build in Studio comes with its own `log4j2.xml` file. The log contains information about any errors raised in the app (unless you have app logic to handle those errors). It also contains anything you want to explicitly log, if you build the logic in the app.

Mule automatically logs multiple messages and specific elements in your app flows to help you debug and keep track of events. You can also include the Logger component anywhere in a flow and set it up to output any message you want.

You can view an app log as follows:

- If you're running an app from Anypoint Studio, the output from the app log is visible in Anypoint Studio's console window.

- If you're using Mule from the command line to run an app, the app log is visible in your OS console.

By default, Mule stores application log files in the following location: `MULE_HOME/logs/<app-name>.log`. You can customize the log file path in the `log4j2.xml` file of the Mule app.

### Runtime Log

The runtime log (`mule_ee.log`) contains information about the apps and lifecycle events. For example, the log records an entry when a Mule service or app starts, deploys, stops, or undeploys.

The runtime log configuration is located in the `log4j2.xml` file, in the `/conf` directory. You can customize this file when running Mule on-premises.

#### View the Runtime Log in Anypoint Studio:

Click **Anypoint Studio > About Anypoint Studio > Installation Details > Configuration > View Error Log**:

#### Change the Log Level

You can change the runtime log level by modifying the `level` value of the following packages in the `log4j2.xml` file:

```xml
  <AsyncLogger name="org.mule" level="INFO"/>
  <AsyncLogger name="com.mulesoft" level="INFO"/>
```

Accepted values are: `DEBUG`, `ERROR`, `INFO`, `TRACE`, and `WARN`.

To change the log level only for specific Connectors, see Enable Verbose Logging.

### Configure Logging

You can create a configuration file to define:

 * What kinds of messages to log
 * How to log the messages (asynchronously or synchronously)
 * Where to log the messages, such as to the console or disk, or to an endpoint or database

Mule uses `slf4j`, which is a logging facade that discovers and uses a logging strategy from the classpath, such as Apache Log4j 2 or the JDK Logger. By default, Mule includes Log4j 2, which is configured with a file called `log4j2.xml`.

### Synchronous Versus Asynchronous Logging

By default, Mule logs messages asynchronously. When logging synchronously, the execution of the thread that is processing your message is interrupted to wait for the log message to be fully handled before it can continue:

When logging asynchronously, the logging operation occurs in a separate thread, so the message can process before the logging completes:

In most situations, MuleSoft recommends that you use **asynchronous logging** because it substantially improves the throughput and lowers the latency of message processing.

When asynchronous logging is used, some actions might not be logged if there is a system crash. This situation occurs because log writing is performed on a separate thread that runs independently of other actions. See Exception Handling with Asynchronous Logging for information on mitigating this issue.

If you use app logs as audit trails, configure your app to always use **synchronous** logging. This prevents the loss of any log messages.

Mule 4 introduced thread-local functionality to optimize the memory usage of log4j. To enhance the use of this feature, you can set the system property `AsyncLoggerConfig.RingBufferSize` (see Configuring Properties). `20000` is the suggested value, but you need to tune it to meet your needs.

#### Performance tests

The chart below shows the performance difference between synchronous and asynchronous logging, and how much latency increased as more concurrent messages were added. In this test, an app logged about one million messages, using an increasingly higher amount of threads on each run. Each transaction resulted in 1000 messages.

As indicated by the chart, the results of logging asynchronously are significantly closer to the results of not logging at all.

### Configuring Custom Logging Settings

By default, logging in Mule is done asynchronously and at a level greater than or equal to INFO. The default log level discards log messages at the DEBUG or TRACE level.

To use synchronous logging, adjust the logging level or define custom categories. You can configure these properties using the `$MULE_HOME/conf/log4j2.xml` file, which specifies how the logger behaves. If you don't edit this file, Mule uses the default properties.

In Anypoint Studio, `log4j2.xml` appears in the `src/main/resources` path of each Mule object.

The default configuration defines all loggers, including the root logger, as asynchronous. You can override this configuration at the domain or app level. To override this configuration at the app level, add a `logConfigFile` entry to the `mule-artifact.json` file. For example:

```json
{
  "minMuleVersion": "4.0.0",

  "logConfigFile": "../../../test-classes/resources/logging/custom-log4j2.xml"
}
```

The following is the default configuration for the `log4j2.xml` file:

```xml
<Configuration>
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%-5p %d [%t] %c: %m%n"/>
        </Console>
    </Appenders>

    <Loggers>

        <!-- CXF is used heavily by Mule for web services -->
        <AsyncLogger name="org.apache.cxf" level="WARN"/>

        <!-- Apache Commons tend to make a lot of noise which can clutter the log-->
        <AsyncLogger name="org.apache" level="WARN"/>

        <!-- Reduce startup noise -->
        <AsyncLogger name="org.springframework.beans.factory" level="WARN"/>

        <!-- Mule classes -->
        <AsyncLogger name="org.mule" level="INFO"/>
        <AsyncLogger name="com.mulesoft" level="INFO"/>

        <AsyncRoot level="INFO">
            <AppenderRef ref="Console"/>
        </AsyncRoot>
    </Loggers>

</Configuration>
```

### Configuring Logs for the Runtime Manager Agent

This configuration is only valid when using the Runtime Manager agent 1.5.2 and later.

To log the Runtime Manager Agent state in a location other than the default `mule_agent.log` file, configure the `$MULE_HOME/conf/log4j2.xml` file to include a new Log4j 2 Appender called `mule-agent-appender`. If included, the Runtime Manager Agent plugin uses this appender to log its state.

The `log4j2.xml` file should include something like the following snippet to enable this functionality:

```xml
<Configuration>
    <Appenders>

      (...)

        <RollingFile name="mule-agent-appender" fileName="${env:MULE_HOME}/logs/custom_mule_agent.log" filePattern="${env:MULE_HOME}/logs/custom_mule_agent.log-%d{MM-dd-yyyy}.log.gz">
            <PatternLayout>
                <Pattern>%d %p %c{1.} [%t] %m%n</Pattern>
            </PatternLayout>
            <Policies>
                <TimeBasedTriggeringPolicy />
                <SizeBasedTriggeringPolicy size="250 MB"/>
            </Policies>
        </RollingFile>
    </Appenders>

    <Loggers>

        (...)

        <AsyncLogger name="com.mulesoft.agent" additivity="TRUE" level="ALL">
          <AppenderRef ref="mule-agent-appender" />
        </AsyncLogger>

        <AsyncRoot level="INFO">
          <AppenderRef ref="Console"/>
        </AsyncRoot>

</Configuration>
```

The above example makes the Runtime Manager agent log its state to a rolling log file in `$MULE_HOME/logs/custom_mule_agent.log`. This file rolls over on a daily interval until it reaches a 250MB size.

For other Log4j 2 appender configurations, see the Apache Log4j 2 documentation.

### Exception Handling with Asynchronous Logging

If you're using asynchronous logging and experience a system crash that might have caused incomplete logs, the LMAX `ExceptionHandler` handler can help. By default, Mule registers this handler to log events to the disk, console, and `logs/mule_ee.log`. To provide your own exception handler, set the system property `AsyncLoggerConfig.ExceptionHandler` to the canonical name of a class that implements the interface.

The default exception handler is shown below:

```java
/*
 * Copyright (c) MuleSoft, Inc.  All rights reserved.  http://www.mulesoft.com
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */
package org.mule.runtime.module.launcher.api.log4j2;

import com.lmax.disruptor.ExceptionHandler;

import org.apache.logging.log4j.status.StatusLogger;

/**
 * Implementation of {@link com.lmax.disruptor.ExceptionHandler} to be used when async loggers fail to log their messages. It will
 * log this event using the {@link org.apache.logging.log4j.status.StatusLogger}
 *
 * @since 3.6.0
 */
public class AsyncLoggerExceptionHandler implements ExceptionHandler {

  private static final StatusLogger LOGGER = StatusLogger.getLogger();

  @Override
  public void handleEventException(Throwable ex, long sequence, Object event) {
    LOGGER.error("Failed to asynchronously log message: " + event, ex);
  }

  @Override
  public void handleOnStartException(Throwable ex) {
    LOGGER.error("Failed to start asynchronous logger", ex);
  }

  @Override
  public void handleOnShutdownException(Throwable ex) {
    LOGGER.error("Failed to stop asynchronous logger", ex);
  }
}
```

There is a performance-reliability trade-off between asynchronous and synchronous logging. If the risk of losing log messages is a serious issue, then configure your loggers to be synchronous. You can have a mix of both synchronous and asynchronous logging.

### Configuration Reloading

Mule runtime uses Log4j 2 as the framework for logging. To add or change the monitoring interval at which Log4j 2 checks for changes, add the `monitorInterval` to the `log4j2.xml` configuration file:

1. In the Mule installation folder, open `conf/log4j2.xml`.
1. Add `<Configuration monitorInterval="15">` after the first line. For example:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration monitorInterval="15">
    <Appenders>
       <Console name="Console" target="SYSTEM_OUT">
           <PatternLayout pattern="%-5p %d [%t] %c: %m%n"/>
       </Console>
    </Appenders>
...
```

In this example, Log4j 2 checks for changes every 15 seconds.
1. Save the file, and restart the Mule server.

For more information, see the Apache documentation on automatically configuring Log4j 2.

### Debugging Projects that Use the HTTP Connector

To debug projects that use the HTTP connector, you might want to make the logging more verbose than usual and track all of the behavior of the HTTP connector's `http-listener` and `http-request` operations in your project. See HTTP Connector Troubleshooting Guide for information.

### Request and Response Logging for SOAP

1. Open the `log4j2.xml` file in `src/main/resources` and add the `HttpMessageLogger` to the config:
```xml
<!-- HTTP is used by Mule for dispatching to web services -->
<AsyncLogger name="org.mule.service.http.impl.service.HttpMessageLogger" level="DEBUG" />
```

1. Save your project.

### Troubleshooting Logging

I don't see any logging output::

Set the `log4j2.xml` at the root of your classpath.
I reconfigured Log4j 2, but nothing happened::

This issue happens because there is another `log4j2.xml` file on your classpath that is getting picked up before your modified one. To find out which configuration file Log4j 2 is using, add the following switch when starting Mule (or add it to the container startup script if you are embedding Mule):
```text
-M-Dlog4j.debug=true
```

This switch writes the Log4j 2 startup information, including the location of the configuration file being used, to `stdout`. You must remove that configuration file before your modified configuration can work.

## Logging and Debugging

MuleSoft provides a variety of logging and debugging options for Mule apps.

Application logs and a runtime log help you monitor and troubleshoot your apps and the Mule server. For details, see Configuring Logging.

You can enable verbose logging for connectors and modules to record debug level information in the logs.

The Logger component can help you monitor or even debug your Mule app by logging important information such as error messages, status notifications, payloads, and so on. You can add a Logger anywhere in a flow, and you can configure it to log a string that you specify, the output of a DataWeave expression you write, or any combination of strings and expressions. For details, see Logger Component in the Core component documentation.

To control the display of Mule stack traces, you can use command-line arguments or set properties in Anypoint Studio. For details, see Configuring Mule Stack Traces.

To troubleshoot a Mule app in Anypoint Studio, you can use the Studio Visual Debugger, which lets you set breakpoints to stop execution and check events. If you are creating your Mule app outside of Studio, you can either use MUnit to test your app, or you can activate remote debugging. For details, see Debugging Outside Studio.

If you are running your Mule application in CloudHub, see View Log Data for additional information about log data and persistence.

## MDC Logging

Mapped Diagnostic Context (MDC) enriches logging and improves tracking by providing more context or information in the logs for the current Mule event.

By default, Mule logs two MDC entries: `processor`, which shows the location of the current event, and `event`, which shows the correlation ID of the event.

Mule Tracing module enables you to enhance your logs by adding, removing, and clearing variables from the logging context for a given Mule event. The logging context exists for the entire execution of the corresponding event.

### Prerequisites

To use the MDC Logging operations, complete the following tasks:

- Install the Mule Tracing module in your application.
- Change the pattern layouts in the `log4j2.xml` file to `MDC`.

You can use MDC Logging with Anypoint Runtime Fabric or CloudHub 2.0. However, if you are using CloudHub 1.0 to deploy your Mule applications, MDC logging isn't supported.

### Install the Mule Tracing Module

Follow the next steps to install the Mule Tracing module in your application.

1. Open your Mule project in Anypoint Studio.
1. Go to the Mule Palette.
1. Select **Search in Exchange**, and search for the Mule Tracing module.
1. Select the module and click **Add**.
1. Click **Finish**.

### Change the Pattern Layouts in the log4j2.xml File

This change instructs Mule to automatically add the MDC context, which includes the correlation ID and the processor path. You can modify the `log4j2.xml` file of your Mule application or the file of your Mule instance, which is located in `/conf/log4j2.xml`.

Follow these steps to change the pattern layouts to MDC:

1. Open the `log4j2.xml` file for editing.
1. Replace `[processor: %X; event: %X]` with `[%MDC]`.

#### Example log4j2.xml File Configurations

**Example: Default log4j2.xml file without MDC logging.**

```text
<PatternLayout pattern="%-5p %d [%t] [processor: %X{processorPath}; event: %X{correlationId}] %c: %m%n"/>
```

**Example: Updated log4j2.xml file with MDC logging.**

```text
<PatternLayout pattern="%-5p %d [%t] [%MDC] %c: %m%n"/>
```

### Available Operations

| XML Element | Description | Accepted Attributes |
|---|---|---|
| `set-logging-variable` | Sets a logging variable and its value. |  [%header%autowidth.spreadcols="a,a"] !=== ! Attribute Name ! Description !`variableName` ! The name of the variable to log. ! `value` ! The value to assign to the variable. Accepts DataWeave expressions. !=== |
| `remove-logging-variable` | Removes a logging variable. |  [%header%autowidth.spreadcols="a,a"] !=== ! Attribute Name ! Description ! `variableName` ! The name of the variable to remove. !=== |
| `clear-logging-variables` | Removes all the logging variables. This option doesn't remove the processor path or the correlation ID. | None |

### Configure MDC Logging in Your Application

To configure MDC logging, add any of the available operations to your Mule application flow and specify the corresponding attributes.

For example, to configure a logging variable, insert the `<tracing:set-logging-variable>` XML element into your application flow:
```text
<flow name="exampleFlow">
    ...
    <tracing:set-logging-variable variableName="testVar" value="testValue" />
    ...
</flow>
```

After executing the flow, the output logs are:
```text
INFO  2021-04-08 16:58:26,882 [[MuleRuntime].uber.15: [test-project-app].exampleFlow.CPU_LITE @18f679] [{correlationId=c85e16c0-98a4-11eb-bc34-cac765a2219b, processorPath=exampleFlow/processors/2, testVar=testValue}] org.mule.runtime.core.internal.processor.LoggerMessageProcessor: Example
```

This logging context affects any output of a Logger component and any internal logging that Mule runtime produces. Therefore, you can add more context to the event that Mule is processing if you need additional information for tracking down any potential issue, for example, when an unexpected error occurs.

### Example

Consider the following application:

```text
<flow name="logging-variables">
    <http:listener config-ref="HTTP_Listener_config" path="/order"/>
    <tracing:set-logging-variable variableName="customerId" value="#[payload.customerId]"/>
    <tracing:set-logging-variable variableName="requestPath" value='#["$(attributes.method):$(attributes.requestPath)"]'/>
    <logger level="INFO" message="#[output application/json --- payload]" />
</flow>
```

After sending the following request:

```text
curl --location --request GET '0.0.0.0:8081/order' \
--header 'Content-Type: application/json' \
--data-raw '{
    "orderId": 548102842,
    "customerId": "ARG-12934",
    "items": [
        "CP-123",
        "CP-452"
    ]
}'
```

The output log is:

```text
INFO  2021-04-09 11:14:38,409 [[MuleRuntime].uber.05: [tracing-module].tracing-moduleFlow.CPU_LITE @34a62707] [processor: tracing-moduleFlow/processors/2; event: eb2b2461-993d-11eb-8a64-4865ee1fd814] {correlationId=eb2b2461-993d-11eb-8a64-4865ee1fd814, customerId=ARG-12934, processorPath=tracing-moduleFlow/processors/2, requestPath=GET:/order} org.mule.runtime.core.internal.processor.LoggerMessageProcessor: {
    "orderId": 548102842,
    "customerId": "ARG-12934",
    "items": [
        "CP-123",
        "CP-452"
    ]
}
```

## Enable Verbose Logging

You can enable verbose logging for different modules and connectors. Because of the high impact to application performance, limit verbose logging to testing and troubleshooting operations.

### Configure Verbose Logging

To configure verbose logging, add an entry to your `log4j2.xml` file, indicating the package names of the connectors or modules you want to log, and set the log level to `DEBUG`.

The following example shows how to find the package names for Anypoint Connector JMS (JMS Connector) and configure verbose logging:

1. In the **Package Explorer** view, open the JMS Connector package library.
1. Inside the `.jar` file, locate all Mule-related packages.

1. Add an entry to your `log4j2.xml` file, indicating the package name and log level = `DEBUG`:
```xml
<Loggers>
    ...
    <AsyncLogger name="org.mule.extensions.jms" level="DEBUG"/>
    ...
</Loggers>
```

### Common Connector Package Names

The following table shows some common Anypoint Connectors and their package names so you don't have to search for them:

| Connector Name | Package Names |
|---|---|
| Anypoint Connector for HTTP | `org.mule.service.http.impl.service.HttpMessageLogger` |
| Anypoint Connector for Salesforce | `org.mule.extension.salesforce` |
| Anypoint Connector for FTP | `org.mule.extension.ftp` |
| Anypoint Connector for SFTP |  · `org.mule.extension.sftp` · `com.jcraft` |
| Anypoint Connector for FTPS | `com.mulesoft.extension.ftps` |
| Anypoint Connector for NetSuite |  · `httpclient.wire.header` · `httpclient.wire.content` · `httpclient.wire` · `org.apache.commons.httpclient` · `org.apache.http` · `org.mule.module.netsuite` · `com.netsuite.webservices` · `org.mule.service.http.impl.service.HttpMessageLogger` · `org.mule.module.netsuite.extension.internal.connection.provider.soap.JavaWSDispatcher` |
| Anypoint Connector for Amazon SQS |  · `org.mule.extension.sqs` · `org.apache.http` |
| Anypoint Connector for Microsoft Dynamics 365 |  · `org.mule.service.http.impl.service.HttpMessageLogger` · `org.apache.http` · `org.mule.extension.microsoftdynamics365` |
| Anypoint Connector for MuleSoft SAP | `org.mule.modules.sap` |
| Anypoint Connector for Anypoint MQ |  · `com.mulesoft.extension.mq` · `com.mulesoft.mq` |
| Anypoint Connector for Database | `org.mule.extension.db` |
| Anypoint Connector for Microsoft SharePoint (version 3.x) |  · `org.apache.http.wire` · `org.apache.http` |

## Configuring Mule Stack Traces

Mule does not display all stack traces by default. When Mule does show stack traces, it filters out some internal class references from to produce a more readable output.

You can control Mule stack trace behavior in two ways:

- Use command-line arguments

- Set properties in Mule Studio

### Use Command-Line Arguments

Use `-M-DpropertyName` with the following command-line arguments to control the behavior of stack traces:

- `mule.verbose.exceptions` - If set to **true**, Mule shows filtered stack traces.

- `mule.stacktrace.filter` - A comma-separated list of packages and/or classes to
 remove from the stack traces, which are matched using `string.startsWith()`.

=====================================================================
These arguments are available for Mule developers and administrators to use while troubleshooting. They are not intended for use by end users.
=====================================================================

### Set Properties in Anypoint Studio

In Studio, you can set the properties specified above to instruct Mule to
provide stack traces and to filter out packages or classes to remove. To adjust these settings:

1. Select **Run** > **Run Configurations...**
1. Define the properties to specify the behavior you want.

In the example below, the `mule.verbose.exceptions` property is set to **true**.

### Obtain the Stack Trace and Thread Dump

Follow these steps to troubleshoot Mule if it stops and you need
more information to find the cause:

1. Identify the Mule process ID (`MULE_PID`).
1. Retrieve the thread dump.
1. Retrieve the heap dump if the Mule server throws
 an Out Of Memory error: `java.lang.OutOfMemoryError: Java heap space`

#### Identify the Mule process ID

To identify the Mule process ID, use the Unix/Linux `ps` command, or execute the `jps`
  command from the terminal. The `jps` tool ships with the JDK used to run Mule.
  For example, a line containing `MuleContainerBootstrap`, `ApplicationDeployer`, or similar identifies the Mule process.

#### Retrieve the Thread Dump

Use the `jstack` tool, which is available in modern JDKs, to retrieve the thread dump:

```text
jstack -l MULE_PID > filename.tdump
```

#### Retrieve the Heap Dump

Retrieve the heap dump if the Mule server throws
 an out of memory error: `java.lang.OutOfMemoryError: Java heap space`

The Oracle JVM provides a JVM modifier
 to gather this information. You must restart the Mule server after
 applying this change and reproduce the out of memory error one more time.

To apply this modifier to the JVM that Mule uses, set the following parameters in Mule's `/conf/wrapper.conf` file to automatically trigger the creation of a heap dump:

```text
wrapper.java.additional.<n>=-XX:+HeapDumpOnOutOfMemoryError
wrapper.java.additional.<n+1>=-XX:HeapDumpPath=path/to/dumps
```

When you set the parameters, change <n> to a number that follows the sequence in `wrapper.conf`.

=====================================================================
By default, Mule includes the `HeapDumpOnOutOfMemoryError` property, but it does not define a path for heap dumps.
=====================================================================

If no path is defined for a heap dump, the file is created in the directory
 where the java process was launched. The heap dump file is then generated as `java_pid<pid>.hprof.<unique number>`.

## Debugging Outside Studio

To troubleshoot a Mule app in Anypoint Studio, you can use the Studio Visual Debugger. This lets you set breakpoints to stop execution and check events.

If you're creating your Mule app outside of Studio, you can either use MUnit to test your app, or you can activate remote debugging.

### Use MUnit to Test an App

MUnit is a Mule application testing framework that allows you to build automated tests for your integrations and APIs. It provides a full suite of integration and unit test capabilities, and is fully integrated with Maven and Surefire for integration with your continuous deployment environment.

For more information, see the MUnit documentation.

### Activate Remote Debugging

You can start Mule with the **-debug** option to activate remote debugging, as shown in this Linux example:

```text
$MULE_HOME/bin/mule -debug
```

With this option, Mule starts normally and logs the following message in the console:

```text
Listening for transport dt_socket at address: 5005
```

Mule is now remotely debuggable on port 5005. Follow these steps to debug Mule:

1. Access Eclipse, and select the **Run > Debug Configurations** menu. From there, create a **Remote Java Application** configuration that uses port 5005.

1. Add the source code of your Mule local instance as an external archive on the second tab of the configuration panel.

1. Click the **Debug** button at the lower right corner of the configuration screen. The local Mule instance resumes its start-up sequence and you can debug the app step-by-step.

If you want to use a port other than 5005, change the JPDA_OPTS property file in the Mule startup script before following the steps for debugging Mule.

## Mule Server Notifications

Mule provides an internal notification mechanism that you can use to access changes that occur on the Mule Server, such as adding a flow component, a request for authorization failing, or Mule starting. You can set up your agents or flow components to react to these notifications.

### Configuring Notifications

Message notifications provide a snapshot of all information sent into and out of the Mule Server. Mule fire these notifications whenever it receives or sends a message. These additional notifications have some impact on performance, so they are disabled by default. To enable message notifications, you set the type of messages you want to enable using the `<notifications>` element in your Mule configuration file. You also register the notification listeners and associate interfaces with specific notifications.

For example, first you create beans for the notification listeners in your spring configuration file, specifying the class of the type of notification you want to receive:

```xml
<bean name="notificationLogger" class="org.myfirm.ProcessorNotificationStore"/>
```

And then, add the reference for your spring configuration:

```xml
<spring:config name="springConfig" files="notification-beans.xml"/>
```

Next, you specify the notifications you want to receive using the `<notification>` element, and then register the listeners using the `<notification-listener>` element:

```xml
<notifications>
    <notification event="MESSAGE-PROCESSOR"/>
    <notification-listener ref="notificationLogger"/>
</notifications>
```

When you specify the MESSAGE-PROCESSOR notification, a notification is sent before and after a message processor is invoked. Because the listeners implement the interface for the type of notification they want to receive, the listeners receive the correct notifications.

For example, the `ProcessorNotificationLogger` class would implement `org.mule.runtime.api.notification.MessageProcessorNotificationListener`:

```java
public class ProcessorNotificationLogger implements MessageProcessorNotificationListener<MessageProcessorNotification> {

    @Override
    public void onNotification(MessageProcessorNotification notification) {
        // write here the logic to process the notification event
    }
}
```

Don't forget to add the mule-api dependency in your pom file with `provided` as scope, so the api classes will be available in your classpath. The dependency will then be provided by mule in runtime.

For a list of notification types, see Notifications Configuration Reference. For a list of notification listener interfaces, see Notification Interfaces below.

#### Specifying a Different Interface

If you want to change the interface associated with a notification, you specify the new interface with the `interface-class` attribute:

```xml
<notifications>
    <notification event="COMPONENT-MESSAGE" interface-class="org.myfirm.MyMessageNotifications"/>
</notifications>
```

#### Configuring a Custom Notification

If you create a custom notification, you also specify the `event-class` attribute:

```xml
<notifications>
  <notification event="CUSTOM" event-class="org.myfirm.MyMessageNotificationsCustomMessage"
  interface-class="org.myfirm.MyMessageNotifications"/>
</notifications>
```

#### Disabling Notifications

If you want to block a specific interface from receiving a notification, you specify it with the `<disable-notification>` element. You can specify the notification type (event), event class, interface, and/or interface class to block.

```xml
<notifications>
    <disable-notification interface="SECURITY"/>
</notifications>
```

#### Using Subscriptions

When registering a listener, you can specify that it only receives notifications from a specific component using the `subscription` attribute. For example, to specify that the listener only receives notifications from a flow component called "MyService1", you would configure the listener as follows:

```xml
<notification-listener ref="endpointNotificationLogger" subscription="MyService1"/>

<object name="endpointNotificationLogger" class="org.myfirm.EndpointNotificationLogger"/>
```

To register interest in notifications from all flow components with "Service" in the name, you would use a wildcard string as follows:

```text
<notification-listener ref="endpointNotificationLogger" subscription="*Service*"/>
```

For more information, see Registering Listeners Programmatically below.

### Firing Custom Notifications

Objects can fire custom notifications in Mule to notify custom listeners. For example, a discovery agent might fire a Client Found notification when a client connects.

You fire a custom notification as follows:

```text
CustomNotification n = new CustomNotification("Hello");

notificationDispatcher.dispatch(n);
```

Any objects implementing `CustomNotificationListener` will receive this notification. It’s a good idea to extend `CustomNotification` and define actions for your custom notification type. For example:

```text
DiscoveryNotification n = new DiscoveryNotification(client, DiscoveryNotification.CLIENT_ADDED);

notificationDispatcher.dispatch(n);
```

### Notification Interfaces

The following table describes the Mule server notifications and the interfaces in the `org.mule.runtime.api.notification` package. An object can implement one of these interfaces to become a listener for the associated notification. All listeners extend the `NotificationListener` interface.

| Notification | Description | Interface |
|---|---|---|
| Connection Notification | Is fired when a connection is made or disconnected. | `ConnectionNotificationListener` |
| Custom Notification | Can be fired by components and other objects such as routers, transformers, agents to communicate a change of state to each other. | `CustomNotificationListener` |
| Exception Notification | An exception was thrown. | `ExceptionNotificationListener` |
| Management Notification | The state of the Mule instance or its resources have changed, such as internal queues reach capacity. | `ManagementNotificationListener` |
| Mule Context Notification | Can be fired when an event such as the mule context start occurs. | `MuleContextNotificationListener` |
| Routing Notification | Async-Reply routers use this when an event is received for an event group that has already been processed. | `RoutingNotificationListener` |
| Security Notification | Is fired when a request for authorization failed. | `SecurityNotificationListener` |
| Transaction Notification | Is fired after a transaction has begun, was committed, or was rolled back. | `TransactionNotificationListener` |
| Async-Message Notification | Can be fired when async work is scheduled and completed for a given flow. | `AsyncMessageNotificationListener` |
| Pipeline-Message Notification | Is fired at key steps in the processing of pipeline. | `PipelineMessageNotificationListener` |
| Message-Processor Notification | A message processor was invoked. | `MessageProcessorNotificationListener` |
| Exception Strategy Notification | An exception strategy was invoked. | `ExceptionStrategyNotificationListener` |
| Extension Notification | Can be fired by extensions, including custom data. | `ExtensionNotificationListener` |
| Connector-Message Notification | Is fired when a message is received or sent through a Connector. | `ConnectorMessageNotificationListener` |

The listener interfaces all have a single method:

```java

public void onNotification(T notification);
```

where T is a notification class (listener class without the 'Listener' at the end).

Depending on the listener implemented, only certain notifications will be received. For example, if the object implements `ManagementNotificationListener`, only notifications of type `ManagementNotification` will be received. Objects can implement more than one listener to receive more types of notifications.

### Registering Listeners Programmatically

You can register listeners as follows:

```text

notificationListenerRegistry.registerListener(listener);

```

or:

```text

notificationListenerRegistry.registerListener(listener, selector);

```

where `listener` is a `NotificationListener<N>` instance and `selector` is a `Predicate<N>` that works as a filter to apply on a fired notification before calling the listener with it.

### Notification Action Codes

Each notification has an action code that determines the notification type. You can query the action code to determine its type. For example:

**MyObject.java**

```java
public class MyObject implements ConnectionNotificationListener<ConnectionNotification> {

    (...)

    public void onNotification(ConnectionNotification notification) {

        if (valueOf(ConnectionNotification.CONNECTION_FAILED).equals(notification.getAction().getIdentifier())) {

            // write here the logic to handle the connection failed notification
        }
     }
}
```

### Notification Payloads

All notifications extend `java.util.EventObject`, and you can use the `getSource()` method to access the payload of the object. The following table describes the payloads for each type of notification.

| Notification | Payload Type | Resource ID | Description |
|---|---|---|---|
| Connection Notification | String | `<connector-name>.receiver(<endpoint-uri>)` | The message receiver or message dispatcher that was connected. |
| Custom Notification | Any object | Any String | The object type is custom to the object firing the notification. |
| Exception Notification | ComponentLocation | Component name | The flow component that triggered this notification. |
| Management Notification | Object | The object ID | The monitored object that triggered this notification. |
| Mule Context Notification | MuleContext | Mule context ID | The Mule context instance. Equivalent to calling getMuleContext(). |
| Routing Notification | Message | Message ID | The message sent or received. |
| Security Notification | SecurityException | The exception message | The security exception that occurred. |
| Transaction Notification | String | Transaction ID | The transaction that have triggered this notification. |
| Async-Message Notification | ComponentLocation | Component name | Component that has scheduled the async work. |
| Pipeline-Message Notification | String | Name | Pipeline name. |
| Message-Processor Notification | ComponentLocation | Component name | The flow component that triggered this notification. |
| Exception Strategy Notification | ComponentLocation | Component name | The flow component that triggered this notification. |
| Extension Notification | Object | Extension name | The payload can change from one extension to another. |
| Connector-Message Notification | ComponentLocation | Component name | The flow component that triggered this notification. |
