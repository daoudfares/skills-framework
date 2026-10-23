# Performance tuning

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Performance Tuning Guide

To achieve optimal performance from your Mule applications, you must evaluate both the applications themselves and the environment in which they run. Although Mule 4 is designed to tune itself, your applications might exhibit performance issues due to their initial construction or dependencies. +

Similarly, for on-premises installations, you might need to tune the environment itself so that your Mule applications can take full advantage of it. Because many variables influence it, tuning the performance of your application requires some trial and error. +

You can simplify performance tuning by using documented best practices and testing your applications in ideal test environments.  The following recommendations come from the Development and Services Engineering teams and benchmarking efforts by MuleSoft Performance Engineering.

### Performance Tuning Summary

Optimizing the performance of your Mule apps requires the following actions:

- Applying tuning recommendations at the application level +
See Performance Tuning Recommendations for details.
- Considering tuning prerequisites and best practices before testing +
See Performance Test Validations for details.
- Monitoring performance during testing to determine the resources required by the Mule runtime engine (Mule) +
See Performance Monitoring for details.

## Tuning Recommendations

Mule 4 provides self-tuning execution, which adjusts itself for optimal performance according to the underlying operating conditions of the environment where you deploy Mule runtime engine (Mule). +
Self-tuning allows you to focus on the specifics of your application rather than Mule internals, which eases the optimization process. Additionally, Mule comes to you already tuned for optimal performance for most common use cases, and changing any parameter is advised against unless you fully understand the implications of doing so.

There are tuning recommendations that you can apply at the application level and benefit your specific use case.

### Repeatable vs Non-repeatable Streaming

Understand which streaming strategy results in the best flow performance for your use case: +

- A repeatable stream (read payload more than once)
- A non-repeatable stream (read payload only once)

See Repeatable vs Non-repeatable Streaming for details.

### Back-Pressure and MaxConcurrency

Understand back-pressure and learn how to use the `maxConcurrency` parameter to tune the number of concurrent messages sent to your flow.

See Back-Pressure and MaxConcurrency for details.

### Backend Server Response Time

Understand if the average latency and throughput of backend servers is limiting the scalability or performance of your application.

See Backend Server Response Time for details.

### Caching

Understand when to use cache and which cache-strategy to follow, based on key aspects of your data. Mule offers some customizable mechanisms, such as Cache Scope and the HTTP Caching API Gateway policy, to enable cache according to your needs.

See Caching for details.

### Pooling Profiles

Pooling components helps process simultaneous incoming requests. Understand how to add `pooling-profile` to connectors when performance tests show that it is necessary.

See Pooling Profiles for details.

### Domains

Using domains provides a central repository for all the shared resources, facilitating the class-loading process. Domains enhance performance when you deploy multiple services on the same on-premises instance of Mule runtime engine.

See Domains for details.

### Logging

Understand why asynchronous logging performs better than synchronous logging.

See Logging for details.

### Batch Processing

Mule can process messages in batches, but batch processing requires having enough available memory to process the threads in parallel, which means moving the records from persistent storage into RAM in a fixed-size block. Understand how to configure the batch block size property for your application.

See Batch Processing for details.

### Application Design Best Practices

Following certain practices at the design phase helps you to achieve better performance for your Mule apps.

See Application Design for details.

## Repeatable vs. Non-Repeatable Streaming

Choose between non-repeatable and repeatable streaming to optimize flow performance in Mule. Non-repeatable streams let you read the payload once; repeatable streams support multiple or concurrent reads. Maximize flow performance by choosing the streaming strategy that matches how your flow consumes the payload:

- A non-repeatable stream (read payload only once) or
- A repeatable stream (read payload more than once)

### Non-Repeatable Streaming

The non-repeatable strategy disables repeatable streams. If your use case requires reading the payload only once, use the `non-repeatable-stream` parameter in the connector. See this example:

```xml
<file:read path="exampleFile.json">
  <non-repeatable-stream />
</file:read>
```

### Repeatable Streaming

Alternatively, if your use case requires reading the payload multiple times or concurrently, you can choose among these two strategies:

- File-store streaming
- In-memory streaming

#### File-Store Repeatable Stream

When using the file-store repeatable stream strategy, configure these parameters to optimize performance:

- `inMemorySize` +
Defines the buffer size stored in memory before Mule writes to disk.
- `bufferUnit` +
Defines the unit of measurement for the buffer size.
- `eagerRead` +
Determines whether Mule reads the buffer as soon as data is available (`true`) or waits until the buffer fills (`false`). The default value is `false`.

When configuring `inMemorySize`, consider these trade-offs:

- Configure a larger buffer size to reduce disk writes and improve performance. However, larger buffers require more memory and can reduce the number of concurrent requests your application can handle.
- Configure a smaller buffer size to reduce memory usage at the cost of slower response time.

This example configures a file-store repeatable stream with a buffer size of 1 MB:

```xml
<file:read path="bigFile.json">
  <repeatable-file-store-stream
    inMemorySize="1"
    bufferUnit="MB"
    eagerRead="true"/>
</file:read>
```

Always run performance tests to find the optimal buffer size for your specific use case.

#### In-Memory Repeatable Stream

When using the in-memory repeatable stream strategy, to manage larger or smaller files, configure these parameters:

- `initialBufferSize` +
Defines the initial buffer size.
- `bufferSizeIncrement` +
Defines how much the buffer grows each time it expands.
- `maxInMemorySize` +
Defines the maximum amount of content stored in memory.
- `bufferUnit` +
Defines the unit of measurement for buffer values.
- `eagerRead` +
Defines whether Mule reads the buffer as soon as data is available (`true`) or waits until the buffer fills (`false`). The default value is `false`. The default buffer size is 512 KB. Adjust the buffer configuration based on your payload size and expected concurrency.

This example configures an in-memory repeatable stream with an initial size of 512 KB, which grows at a rate of 256 KB and allows up to 2000 KB (2 MB) of content in memory:

```xml
<file:read path="exampleFile.json">
  <repeatable-in-memory-stream
    initialBufferSize="512"
    bufferSizeIncrement="256"
    maxInMemorySize="2000"
    bufferUnit="KB"/>
</file:read>
```

Always run performance tests to find the optimal buffer size for your specific use case.

## Back-Pressure and MaxConcurrency

Under heavy load, Mule runtime engine (Mule) might not immediately have the resources available to process a specific event. This issue might occur because all threads are busy and the current flow’s concurrency is exceeded. When this occurs, Mule logs the following message:
`Flow 'flowName' is unable to accept new events at this time` +
This message is known as back-pressure. Mule back-pressure actions are specific to each connector’s source.

When a producer component outputs information at a higher rate than a consumer component can process it, you can use the `maxConcurrency` parameter to set the maximum number of concurrent messages that a flow can process at any given time, whether the components are internal or external, flows or sources, and so on.

Although Mule applies back-pressure on its own, the `maxConcurrency` parameter helps to control the flow performance, especially when a backend server may affect when having high concurrency. See how to set the parameter in the following example:

```xml
<flow name="perf-test-flow" maxConcurrency="${flow.max.concurrency}">
```

Similarly, you can limit the number of records that can be processed in a batch job by setting the `maxConcurrency` parameter as in the following example:

```xml
<batch:job jobName="test-batch" maxConcurrency="${batch.max.concurrency}">
```

By default, the Flow and Async scopes do not set a `maxConcurrency` limit, but the Batch Job component limits concurrency to twice the number of available cores. The capacity of your system also limits concurrency.

### Components with Max Concurrency Settings

The following components provide a max concurrency setting:

- Flow scope
- Scatter-Gather router
- Async scope
- Batch Job scope
- Parallel For Each scope

### Recommendation

Unless a lower concurrency is required to artificially trigger a back-pressure event, use the default settings, and do not change the max concurrency value.

### See also

- Execution Engine Threads and Concurrency

## Caching

Identifying key aspects of your data such as when to use cache and which cache strategy to follow, helps you to improve processing performance:

- Is the data frequently called, with often repeated results?
- Can you afford eventual consistency between the data source and the cache information? +
At least for a while until cache refreshes.

Mule runtime engine (Mule) offers customizable strategies, such as the Cache scope and the HTTP Caching API Gateway policy, to enable cache according to your needs. Both strategies help applications that constantly request the same data by reducing the processing load, especially network interactions with a remote host.

For Cache scope, consider a production environment in which the default in-memory caching consumes all of your memory resources. To avoid this consumption, use an object-store caching configuration with well-defined storage and expiry policies.

## Pooling Profiles

Unlike singleton components, pooled components configure their component pool which contains multiple instances of the component to process simultaneous incoming requests. Each pooled component has its pooling profile.

Connectors such as Anypoint Connector for FTP (FTP Connector) and Anypoint Connector for SFTP (SFTP Connector) pool connections by default and use a `pooling-profile` to customize the connection pool. +
When performance tests show it necessary, add the `pooling-profile` parameter to connectors.

However, Anypoint Connector for Database (Database Connector) does not perform connection pooling by default, causing every execution of an SQL statement to open a new connection and close it once finished (unless there is a transaction active that uses the same connection for the whole transaction). By using a pooling profile, you enable one-time connection setup and subsequent requests use existing connections, thereby improving request-processing performance:

```xml
<db:mysql-config name="dbConfig" host="localhost" port="3306" user="root"
   password="" database="esb" doc:name="MySQL Configuration">
   <db:pooling-profile maxPoolSize="17" minPoolSize="13" />
</db:mysql-config>
```

The `maxPoolSize` setting specifies the maximum number of connections open to the database, and available to serve incoming requests.

## Batch Job Performance Tuning

Mule runtime engine (Mule) possesses the ability to process messages in batches. Within an application, you can initiate a batch job which is a block of code that splits large messages into individual records, performs actions upon each record, then reports on the results and potentially pushes the processed output to other systems or queues.

Consider having 1 million records processed by a batch application with three steps. Several I/O operations occur as Mule processes each record as it moves through the job’s phases. The disk characteristics, along with the workload size, play a key role in the performance of the batch job, primarily because during the input phase, an in-disk queue is created of the list of records to be processed, which is constantly read and written by the flow, resulting in heavy I/O utilization.

Additionally, batch processing requires having enough memory available to process the threads in parallel, which means moving the records from persistent storage into RAM in a fixed-size block. The larger your records and their quantity, the more available memory you need for batch processing.

### Batch Block Size

By default, the batch block size is set to 100. It is a good balancing point between performance and working memory requirements based on analysis across a set of representative batch use cases with various record sizes. However, the optimal value for each application depends on its use case. +
You can configure this property for the batch job. If you believe that in your particular case, custom size is best suited, make sure to run comparative tests with different values to find the optimum size in your use case. The following example shows the batch block size:

```xml
<batch:job jobName="test-batch" blockSize="${batch.block.size}">
```

### Max Concurrency

The maximum number of threads used for processing within a Batch scope defaults to 2 times the number of cores that the JVM detects. On fractional core deployments, such as CloudHub and Anypoint Runtime Fabric, the JVM detects a _non-fractional_ number of cores. You can manually increase or lower the automated concurrency setting. The Max Concurrency setting enables you to set an upper limit on the number of threads to use for a batch job instance that, for example, has insufficient records to warrant more threads.

The following example overrides the automated `maxConcurrency` default to a setting that is loaded from a property:

```xml
<batch:job jobName="an-example-batch" maxConcurrency="${batch.block.maxConcurrency}">
```

### Batch Aggregators

One million round trips across a network impacts performance, whether on single or multiple threads. Communication with SaaS systems can easily consume the quota of API calls. Instead of processing records one by one, you can improve performance by using the Batch Aggregator scope to perform bulk operations on arrays of records. The scope uses an Aggregator Size setting to limit the number of records in each array.

When determining the number of records to process in an array of records, you must take into account the maximum number of records permitted by operations on the system with which the communication takes place. It is important to conduct performance testing on your Aggregator Size setting _and on lower values_. Your logic must handle any number of records up to and including the value of your setting because the number of records that the system receives can be lower than your specified value. For example, if there are 120 records, and your Aggregator Size setting is 50, the last submission is 20 records.

The following example shows a Batch Step scope with a Batch Aggregator scope that is set to a fixed size of `50`:

```xml
<batch:step name="Batch_Step_PushToXYZ" >
  <batch:aggregator doc:name="Batch Aggregator" size="50">
     <!-- code for an array of 50 (or fewer) records -->
  </batch:aggregator>
</batch:step>
```

If the aggregator contains an operation that streams data, you can activate the scope's Streaming option (`streaming="true"`) instead of using an Aggregator Size setting (`size="50"`).

### Multiple Concurrent Instances of a Batch Job

Many use cases for Batch Job scopes process only one request (batch job instance) at a time, but some cases simultaneously execute two or more batch job instances. To tune the thread pool sharing in such cases, you can set one of these scheduling strategies, each of which is tracked separately by its batch instance ID:

- `ORDERED_SEQUENTIAL`: Default scheduling strategy that limits the impact of concurrent instances by processing the instances in the order they are triggered. This strategy is useful if nonsequential processing of the same batch job can cause issues, such as data inconsistency, or when resource limitations are reached.

- `ROUND_ROBIN`: Scheduling strategy that shares the threads with batch job instances that are "in flight".

## App Design That Maximizes Process Performance

As you design your applications, consider the following best practices for enhancing processing performance. These practices include guidelines on choosing a Mule runtime engine (Mule) version, avoiding certain app design issues, and specific settings for using Mule components and connectors.

### Mule Runtime Engine Version

Before you start tuning your application, review the following Mule version recommendations:

- Use the latest Mule version to create and run the application.
- Update your application dependencies to the latest version so you take advantage of the recent performance improvements and bug fixes.
- Update to the latest version of the Mule patch whenever possible.
- When developing and testing an application, use the same Mule version as used to deploy that application in your environments.

### Tips to Design for Enhanced Processing Performance

As you design your apps, consider the following recommendations to increase performance:

- Instead of repeatedly using the Java module to reuse code such as Java libraries, create an SDK module with operations that wrap Java invocations.
- Use DataWeave to transform or enrich data, and create payloads instead of custom scripting code such as Java and Groovy.
- Avoid sequences of `set-variable/set-payload` components such as in the following example:
```xml
<set-variable value='"Hello"' doc:name="Set Variable" variableName="hello"/>
<set-variable value='"world!"' doc:name="Set Variable" variableName="world"/>
```

Instead, combine them into a single `ee:transform` operation that avoids generating a new event for each component:
```xml
<ee:transform doc:name="Transform Message" >
	<ee:variables >
		<ee:set-variable variableName="hello" ><![CDATA[%dw 2.0
            output application/json
            ---
           "Hello"]]></ee:set-variable>

           <ee:set-variable variableName="world" ><![CDATA[%dw 2.0
            output application/json
            ---
           "world"]]></ee:set-variable>
	</ee:variables>
</ee:transform>
```

- Avoid using store transient values in `set-variable`, as shown in the following example:
```xml
<flow name="FileComponentWithsetVariableFlow" doc:id="daa9e38a-bb8c-4c87-a4c0-ba2dd90316b2" >
       <set-variable value="#['file_path/' ++ attributes.queryParams['filename']]" doc:name="Set Variable" doc:id="cf876447-12a6-4267-9b26-5e849153142c" variableName="fileName"/>
       <file:read doc:name="Read" doc:id="e4ad1ad4-0edb-45c9-ab43-d7f07effa277" path="#[vars.fileName]"/>
</flow>
```

Instead, move these values into components that need them:
```xml
<flow name="FileComponentWithoutsetVariableFlow" doc:id="0d44d155-cabe-4a79-99e4-81de22743edb" >
      <file:read doc:name="Read" doc:id="09dfb229-67fd-4508-862f-489c123527ba" path="#['file_path/' ++ attributes.queryParams['filename']]"/>
</flow>
```

- Avoid creating property resolvers, which require using DataWeave for every event and thereby increase process overhead:
```xml
<flow-ref name="#[p(someProp) default p(otherProp)]"/>
```

Instead, place DataWeave logic in a property placeholder and use a static flow reference:
```xml
<flow-ref name="${propertyContainer.propertyName}"/>
```

### Avoid Recursive Flow References

Using `flow-ref` to create recursive patterns (a flow that calls itself, or mutual recursion between flows) is an antipattern that can lead to resource exhaustion and should be replaced with iterative constructs.

#### Why Recursion Is Problematic

The Mule runtime maintains a flow call stack for each event being processed. Each `flow-ref` invocation adds an entry to this stack. When the stack depth limit is exceeded, the runtime raises a `CRITICAL` error that can't be handled by error handlers.

Additionally, extremely long flows with many processors generate deeply nested internal execution chains. When these flows are combined with recursive patterns or very deep call chains, the accumulated nesting can exhaust the JVM thread stack and produce a `StackOverflowError` or `VirtualMachineError`, which leaves the runtime in an inconsistent state (see What Happens After a FATAL_JVM_ERROR).

#### Antipattern: Recursive Flow-Ref

This example is an antipattern because it creates a recursive pattern by calling the same flow repeatedly.

```xml
<!-- ANTIPATTERN: Do NOT do this -->
<flow name="process-items">
  <choice>
    <when expression="#[sizeOf(payload) > 0]">
      <!-- process first item -->
      <set-payload value="#[payload[1 to -1]]"/>
      <!-- recursive call to self -->
      <flow-ref name="process-items"/>
    </when>
  </choice>
</flow>
```

#### Recommended Alternatives

| Use Case | Recommended Pattern |
|---|---|
| Process each item in a collection | Use `<foreach>` or `<parallel-foreach>` scope. |
| Process items in large datasets | Use `<batch:job>` for batch processing. |
| Retry an operation | Use `<until-successful>` with `maxRetries`. |
| Poll until a condition is met | Use a source-based polling trigger (for example, a Scheduler with a watermark). |
| Paginated API calls | Use connector-native pagination or a `<foreach>` over page numbers. |
| Complex iterative logic that can't be expressed using built-in scopes | Implement a custom router by using the Mule SDK that encapsulates the iteration logic in Java, avoiding deep nesting in the Mule execution chain. |

#### Example: Replace Recursion with For Each

This example shows how to replace recursion with a For Each scope.

```xml
<!-- CORRECT: Iterative processing -->
<flow name="process-items">
  <foreach collection="#[payload]">
    <!-- process each item -->
  </foreach>
</flow>
```

#### Keep Flows Short

Beyond avoiding recursion, keep individual flows at a reasonable length. Flows with hundreds of processors generate deep internal execution chains. If a flow grows too large, split it into smaller flows and invoke the flows with `flow-ref`. Unlike subflows, which are inlined at execution time and don't reduce internal nesting, separate flows introduce independent execution chains and reset internal nesting depth. This helps prevent stack overflow conditions while improving readability and maintainability.

### Components and Connectors Best Practices

When designing your apps using Mule components and connectors, consider the following recommendations to enhance the performance.

#### APIkit

To improve performance, disable APIkit validations. If payload validations are required, APIkit  validates input requests against API specification.

#### DataWeave

When using DataWeave, consider the following ways to improve performance:

- If payloads are large, include `indent=false` to improve client parsing and reduce response size.
- Define `content-type` to avoid verbose messages in the log.
- Use inline DataWeave scripts during development and then move them to an external file to have a clean XML and reusable scripts.
- Do not log complex DataWeave expressions with every request.
- Avoid patterns of iterating over a collection and then transforming each individual item:
```xml
<foreach>
	<ee:transform >
		<ee:message >
			<ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
payload mapObject (value, key) -> {
	(upper(key)): value
}
			]]></ee:set-payload>
		</ee:message>
	</ee:transform>
	...
</foreach>
```

Instead, transform the entire collection and iterate later:
```xml
<ee:transform>
	<ee:message >
		<ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
payload map (item, index) -> {
	book: item mapObject (value, key) -> {
		(upper(key)): value
	}
}
		]]></ee:set-payload>
	</ee:message>
</ee:transform>
<foreach>
	...
</foreach>
```

#### Validator

Use Validator Module instead of throwing exceptions with Groovy Scripts.

#### HTTP and HTTPS

For HTTP and HTTPS, consider the following recommendations:

- Use the authentication mechanisms provided by Anypoint Connector for HTTP (HTTP Connector) instead using manual authentications such as manually generating the Basic auth header with a DataWeave expression.
- If HTTPS is required, use the HTTPS Listener with a TLS Context reference, configuring the keystore with key-pair values generated with Keytool. +
You can avoid HTTPS configuration if the SSL can also be terminated at the Load Balancer level when using a dedicated load balancer in CloudHub or if there is an on-premises load balancer for hybrid scenarios:
```xml
<tls:context name="TLS_Context" doc:name="TLS Context">
      <tls:key-store type="jks" path="company-keystore.jks" alias="${jks.alias}" keyPassword="${jks.key.password}" password="${jks.password}"/>
</tls:context>
```

#### Database

Use parameterized queries. If you must use dynamic queries, remember to validate inputs first. Using dynamic queries could cause SQL-Injection vulnerability.

#### File Connector

Instead of using a transform component for the transformation in the write operation, use a DataWeave expression. This avoids message payload changes that occur after the write operation, as shown in the following example:

```xml
<file:write path="output.csv">
 <file:content>#[%dw 2.0
                 output application/csv
                 ---
                 payload.customers.email
               ]
 </file:content>
</file:write>
```

Use the recursive parameter to list files and folders within subfolders:

```xml
<file:list config-ref="File_Config" directoryPath="relativePath" recursive="true" />
```

#### Web Service Consumer Connector

To import WSDLs including all references (XSDs) in your project, use Anypoint Connector for Web Service Consumer (Web Service Consumer Connector) and point the configuration to the local WSDL.

#### AMQP Connector

Because the server constrains the performance and configuration of Anypoint Connector for AMQP (AMQP Connector), when you investigate performance issues, explore the server-side configuration to determine if consume or publish parameters have an impact on performance.

##### Consume Parameters

Review consume parameters that can have an impact on performance.

###### Number of Consumers

Setting the number of consumers for an AMQP configuration and the Listener source determines how many consumers are spawned by the source and receive AMQP messages concurrently, as each consumer creates and uses a different channel. +
Message throughput depends on the number of consumers, becoming greater as the number of consumers increases. However, throughput is also affected by the performance characteristics of the flow.

###### ACK Mode Parameter

ACK mode determines the acknowledgment mode to use when consuming from the AMQP broker. You set acknowledgment mode (ACK) at the configuration level (using the **Consumer** tab), but Listener and consume operations can override this mode. +
There are three acknowledgment modes: +

- `AUTO` +
Use Automatic to acknowledge a received message automatically only if the flow execution finishes successfully.
- `MANUAL` +
Use Manual if you want the app logic to control message acknowledgment.
- `IMMEDIATE` +
Use Immediate when you want to acknowledge messages as your app consumes them, before processing them.

Note that if a transaction is opened in the channel, the ACK mode parameter is overruled and the commit automatically process the message acknowledgment and the rollback automatically process the recovery.

###### Quality of Service Tab

You set QoS parameters at the configuration level (using the **Quality of Service** tab), with 0 representing an unlimited value. A Listener operation can override this setting. +
These are the parameters:

- Prefetch Size +
Defines a prefetch size window. The broker sends as many messages as possible without exceeding the prefetch size window in octets (bytes).
- Prefetch Count +
Specifies a global prefetch window in terms of the maximum number of whole messages. You can use this parameter in combination with the `prefetch-size` parameter to send a message in advance only it both prefetch windows sizes allow it.

###### ACK Mode and Prefetch

The acknowledgment mode and QoS prefetch value that you choose have a significant effect on consumer throughput. In general, increasing the prefetch value and choosing Immediate acknowledgment mode yield the best possible rate of delivery. However, with both choices the number of delivered but not yet processed messages also increases, thereby increasing consumer RAM consumption

Automatic acknowledgement mode or Manual acknowledgment mode with unlimited prefetch should be used with care. Consumption of a lot of messages without acknowledgement leads to increased memory consumption on the broker node. Finding a suitable prefetch value is a matter of trial and error and can vary from workload to workload.

##### Publish Parameters

Set the following parameters at the configuration level, using the **Publisher** tab. Publish and Publish-consume operations can override these parameters. Depending on your use case, you might need to enable only one of these parameters.

###### Delivery Mode Parameter

Setting this parameter determines the delivery mode used to publish to the AMQP broker. Possible parameters values are:

- `PERSISTENT` +
Delivered messages to durable queues are logged to disk on the broker.
- `TRANSIENT` +
Delivered messages are not logged.

The broker is responsible for the implementation of the recordable storage mechanism for persistent messages. The impact of this feature on performance depends on the AMQP server.

###### Request Broker Confirm Parameter

If the broker provides no confirmation, setting this parameter determines whether the operation fails. Using this parameter adds one extra communication between the broker and the client per message published.

## Logging

Mule runtime engine (Mule) 4 uses Log4j 2 asynchronous logging by default, so the logging operation happens in a separate thread from the message processing, and the latter can continue without having to wait for the log operation to complete.

Asynchronous logging poses a performance-reliability trade-off as explained in Asynchronous Logging Mule, and you may lose some messages if Mule crashes before the logging buffers flush to the disk. In this case, consider that you can have a mixed configuration of asynchronous or synchronous loggers in your app.
Best practice is to use asynchronous logging over synchronous with a minimum logging level of `WARN` for a production application. In some cases, enable  `INFO` logging level when you need to confirm events such as successful policy installation or to perform troubleshooting.

Configure your logging strategy by editing your application's `src/main/resources/log4j2.xml` file, as shown in the following example:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Configuration>
   <Appenders>
       <RollingFile name="file" fileName="${sys:mule.home}${sys:file.separator}logs${sys:file.separator}try-transactional-propagate.log"
                filePattern="${sys:mule.home}${sys:file.separator}logs${sys:file.separator}try-transactional-propagate-%i.log">
           <PatternLayout pattern="%-5p %d [%t] [event: %X{correlationId}] %c: %m%n" />
           <SizeBasedTriggeringPolicy size="10 MB" />
           <DefaultRolloverStrategy max="10"/>
       </RollingFile>
   </Appenders>
   <Loggers>

       <!-- Http Logger shows wire traffic on DEBUG. -->
       <!--AsyncLogger name="org.mule.service.http.impl.service.HttpMessageLogger" level="DEBUG" /-->
       <AsyncLogger name="org.mule.service.http" level="WARN"/>
       <AsyncLogger name="org.mule.extension.http" level="WARN"/>

   <!-- Mule logger -->
       <AsyncLogger name="org.mule.runtime.core.internal.processor.LoggerMessageProcessor" level="WARN"/>
       <AsyncRoot level="WARN">
           <AppenderRef ref="file" />
       </AsyncRoot>
   </Loggers>
</Configuration>
```

- Apply caution when logging parts of messages, especially the payload, because this bypasses streaming and causes significant disk I/O for large payloads

- Avoid using the `<async>` scope to log messages
Because the logging mechanism is already implemented asynchronously by the Log4j2 library in the backend, enclosing a logger into the `<async>` scope does not improve parallelism, it increases the resource usage and duplicates the numbers of threads required. Repeatedly using this pattern in an application can cause thread exhaustion, low performance, and back-pressure.
```xml
		<async doc:name="Async" doc:description="Don't do this">
			<logger level="INFO" doc:name="Logger" message="Don't do this" />
		</async>

		<logger level="INFO" doc:name="Logger" message="Do this"/>
```

## Execution Engine

Mule runtime engine implements a reactive execution engine, tuned for nonblocking and asynchronous execution. +
To see more details about reactive programming, visit https://en.wikipedia.org/wiki/Reactive_programming.

This task-oriented execution model enables you to take advantage of nonblocking I/O at high concurrency levels transparently, meaning you don’t need to account for threading or asynchronicity in your flows. Each operation inside a Mule flow is a task that provides metadata about its execution, and Mule makes tuning decisions based on that metadata.

Mule event processors indicate to Mule whether they are CPU-intensive, CPU-light, or I/O-intensive operations. These workload types help Mule tune for different workloads, so you don’t need to manage thread pools manually to achieve optimum performance. Instead, Mule introspects the available resources (such as memory and CPU cores) in the system to tune thread pools automatically.

### Processing Types

Mule event processors indicate to Mule what kind of work they do, which can be one of:

- CPU-Light +
For quick operations (around 10 ms), or nonblocking I/O, for example, a Logger (`logger`) or HTTP Request operation (`http:request`). These tasks should not perform any blocking I/O activities. The applicable strings in the logs are `CPU_LIGHT` and `CPU_LIGHT_ASYNC`.
- Blocking I/O +
For I/O that blocks the calling thread, for example, a Database Select operation (`db:select`) or a SFTP read (`sftp:read`) . Applicable strings in the logs are `BLOCKING` and `IO`.
- CPU Intensive +
For CPU-bound computations, usually taking more than 10 ms to execute. These tasks should not perform any I/O activities. One example is the Transform Message component (`ee:transform`). The applicable string in the logs is `CPU_INTENSIVE`.

See specific component or module documentation to learn the processing type it supports. If none is specified, the default type is CPU Light.

For connectors created with the Mule SDK, the SDK determines the most
appropriate processing type based on how the connector is implemented. For
details on that mechanism, refer to the Mule SDK documentation.

### Threading

Starting in Mule 4.3, Mule contains one unique thread pool, called the UBER pool. This thread pool is managed by Mule and shared across all apps in the same Mule instance. At startup, Mule introspects the available resources (such as memory and CPU cores) in the system and tunes automatically for the environment where Mule is running. This algorithm was established through performance testing and found optimal values for most scenarios.

This single thread pool allows Mule to be efficient, requiring significantly fewer threads (and their inherent memory footprint) to process a given workload when compared to previous versions.

If you are upgrading from earlier Mule versions, see Threading in Mule 4.2 to understand the differences applied to the threading model in Mule 4.3.

#### Proactor Pattern

Proactor is a design pattern for asynchronous execution. To understand how the Proactor design pattern works, visit https://en.wikipedia.org/wiki/Proactor_pattern

According to this design pattern, tasks are classified in categories that correspond to Mule processing types, and each task is submitted for execution to the UBER pool.

Performance testing shows that applying the Proactor pattern leads to better performance, even with one unique thread pool, because it allows threads to return to the main loop more quickly, allowing the system to continue to accept new work while the I/O tasks are blocked and waiting.

#### Transactions

When there’s an active transaction, all thread switches are suspended. Event processors participating in the transaction are executed in the same thread.

### Configuration

The thread pool is automatically configured by Mule at startup, applying formulas that consider available resources such as CPU and memory.

If you run Mule runtime engine on premises, you can modify these global formulas by editing the `MULE_HOME/conf/schedulers-pools.conf` file in your local Mule instance. This configuration file contains comments that document each of the properties, but depending on your pool strategy, you can configure specific properties.

Configure the `org.mule.runtime.scheduler.SchedulerPoolStrategy` parameter to switch between the two available strategies:

- UBER +
Unified scheduling strategy. Default.
- DEDICATED +
Separated pools strategy. Legacy.

```ini
# The strategy to be used for managing the thread pools that back the 3 types of schedulers in the Mule Runtime
# (cpu_light, cpu_intensive and I/O).
# Possible values are:
#    - UBER: All three scheduler types will be backed by one uber thread pool (default since 4.3.0)
#    - DEDICATED: Each scheduler type is backed by its own Thread pool (legacy mode to Mule 4.1.x and 4.2.x)
org.mule.runtime.scheduler.SchedulerPoolStrategy=UBER
```

#### UBER Scheduling Strategy

When the strategy is set to `UBER`, the following configuration applies:

- `org.mule.runtime.scheduler.uber.threadPool.coreSize=cores`
- `+org.mule.runtime.scheduler.uber.threadPool.maxSize=max(2, cores + ((mem - 245760) / 5120))+`
- `org.mule.runtime.scheduler.uber.workQueue.size=0`
- `org.mule.runtime.scheduler.uber.threadPool.threadKeepAlive=30000`

Example `schedulers-pools.conf` file:

```ini
# The number of threads to keep in the uber pool.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=UBER
org.mule.runtime.scheduler.uber.threadPool.coreSize=cores

# The maximum number of threads to allow in the uber pool.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=UBER
org.mule.runtime.scheduler.uber.threadPool.maxSize=max(2, cores + ((mem - 245760) / 5120))

# The size of the queue to use for holding tasks in the uber pool before they are executed.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=UBER
org.mule.runtime.scheduler.uber.workQueue.size=0

# When the number of threads in the uber pool is greater than SchedulerService.io.coreThreadPoolSize, this is the maximum
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=UBER
# time (in milliseconds) that excess idle threads will wait for new tasks before terminating.
org.mule.runtime.scheduler.uber.threadPool.threadKeepAlive=30000
```

#### DEDICATED Scheduling Strategy

When the strategy is set to `DEDICATED`, the parameters from the default UBER strategy are ignored.

To enable this configuration, uncomment the following parameters in your `schedulers-pools.conf` file:

- `org.mule.runtime.scheduler.cpuLight.threadPool.size=2*cores`
- `org.mule.runtime.scheduler.cpuLight.workQueue.size=0`
- `org.mule.runtime.scheduler.io.threadPool.coreSize=cores`
- `+org.mule.runtime.scheduler.io.threadPool.maxSize=max(2, cores + ((mem - 245760) / 5120))+`
- `org.mule.runtime.scheduler.io.workQueue.size=0`
- `org.mule.runtime.scheduler.io.threadPool.threadKeepAlive=30000`
- `org.mule.runtime.scheduler.cpuIntensive.threadPool.size=2*cores`
- `org.mule.runtime.scheduler.cpuIntensive.workQueue.size=2*cores`

Example `schedulers-pools.conf` file:

```ini
# The number of threads to keep in the cpu_lite pool, even if they are idle.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.cpuLight.threadPool.size=2*cores

# The size of the queue to use for holding cpu_lite tasks before they are executed.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.cpuLight.workQueue.size=0

# The number of threads to keep in the I/O pool.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.io.threadPool.coreSize=cores

# The maximum number of threads to allow in the I/O pool.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.io.threadPool.maxSize=max(2, cores + ((mem - 245760) / 5120))

# The size of the queue to use for holding I/O tasks before they are executed.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.io.workQueue.size=0

# When the number of threads in the I/O pool is greater than SchedulerService.io.coreThreadPoolSize, this is the maximum
# time (in milliseconds) that excess idle threads will wait for new tasks before terminating.
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.io.threadPool.threadKeepAlive=30000

# The number of threads to keep in the cpu_intensive pool, even if they are idle.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.cpuIntensive.threadPool.size=2*cores

# The size of the queue to use for holding cpu_intensive tasks before they are executed.
# Supports Expressions
# Only applies when org.mule.runtime.scheduler.threadPool.strategy=DEDICATED
org.mule.runtime.scheduler.cpuIntensive.workQueue.size=2*cores
```

##### Considerations

MuleSoft doesn’t recommend changing the used pool strategy nor change its configuration values. Note that the configuration is global and affects the entire Mule Runtime instance.

MuleSoft recommends that you perform load and stress testing with all applications involved in real-life scenarios to validate any change in the threading configurations and to understand how the thread pools work in Mule 4.

#### Configuration at the Application Level

You can define the pool strategy to use in an application by adding the following to your application code:

```xml
<ee:scheduler-pools poolStrategy="UBER" gracefulShutdownTimeout="15000">
   <ee:uber
       corePoolSize="1"
       maxPoolSize="9"
       queueSize="5"
       keepAlive="5"/>
</ee:scheduler-pools>
```

The `poolStrategy` parameter exists for backward compatibility, enabling you to revert to the three pools scheme from earlier Mule versions:

```xml
<ee:scheduler-pools gracefulShutdownTimeout="15000">
   <ee:cpu-light
           poolSize="2"
           queueSize="1024"/>
   <ee:io
           corePoolSize="1"
           maxPoolSize="2"
           queueSize="0"
           keepAlive="30000"/>
   <ee:cpu-intensive
           poolSize="4"
           queueSize="2048"/>
</ee:scheduler-pools>
```

The `gracefulShutdownTimeout` parameter specifies the maximum time (in milliseconds) to wait until all tasks in all the artifact thread pools have completed execution when stopping the scheduler service.

The following table describes the configurable properties and includes the XML attribute for each field.

| Property Name | XML | Description |
|---|---|---|
| Pool Size | `poolSize` | The number of threads to keep in the pool, even if they are idle. |
| Queue Size | `queueSize` | The size of the queue to use for holding tasks before they are executed. |
| Core Pool Size | `corePoolSize` | The number of threads to keep in the pool. |
| Max Pool Size | `maxPoolSize` | The maximum number of threads to allow in the pool. |
| Keep Alive | `keepAlive` | When the number of threads in the pool is greater than the indicated core pool size, this value sets the maximum time (in milliseconds) for excess idle threads to wait for new tasks before terminating. |

##### Considerations

Applying pool configurations at the application level causes Mule to create a completely new set of thread pools for the Mule app. This configuration does not change the default settings in `scheduler-conf.properties`, which is particularly important for on-premises deployments in which many Mule apps are deployed to the same Mule instance.

MuleSoft recommends running Mule using default settings.
If you upgrade from Mule 4.1.x or Mule 4.2.x you can use the DEDICATED strategy so that any customizations to `scheduler-conf.properties` are still used. However, MuleSoft recommends to test the new default setting to determine whether the optimizations are still required. Also, try first to customize the new UBER strategy before reverting to the legacy mode.

If you define pool configurations at the application level for Mule apps deployed to CloudHub, be mindful about worker sizes because fractional vCores have less memory. See CloudHub Workers for more details.

### Custom Thread Pools

Besides the unique UBER thread pool, some components might create additional pools for specific purposes:

- NIO Selectors +
Enables nonblocking I/O. Each connector can create as many as required.
- Recurring tasks pools +
Some connectors or components (expiration monitors, queue consumers, and so on) might create specific pools to perform recurring tasks.

### Back-Pressure Management

Back pressure can occur when, under heavy load, Mule does not have resources available to process a specific event. This issue might occur because all threads are busy and cannot perform the handoff of the newly arrived event, or because the current flow’s `maxConcurrency` value has been exceeded already.

If Mule cannot handle an event, it logs the condition with the message `Flow 'flowName' is unable to accept new events at this time`. Mule also notifies the flow source, to perform any required actions.

The actions that Mule performs as a result of back-pressure are specific to each connector’s source. For example, `http:listener` might return a `503` error code, while a message-broker listener might provide the option to either wait for resources to be available or drop the message.
In some cases, a source might disconnect from a remote system to avoid getting more data than it can process and then reconnect after the server state is normalized.

### Upgrading from Mule 4.2 or 4.1

When upgrading from Mule 4.2.x or 4.1.x to Mule 4.3.x or later, take the following actions:

- If no custom threading settings are applied (either through `scheduler-pools.conf` or directly in the Mule app), then no action is required.
- If custom threading configurations are applied, test your Mule applications using the default configuration. +
Because of the UBER pool strategy and other performance updates implemented in Mule 4.3, you might not need custom threading configurations.
- If tests confirm that a custom configuration is still necessary, a problem might exist with resource management in the application, one of the application dependencies, or the Mule instance.
Using a custom configuration can lead to inefficient use of resources and might hide underlying issues.

### Troubleshooting

When troubleshooting a Mule app, consider thread naming conventions.

For example, consider this flow:

```xml
<flow name="echoFlow">
   <http:listener config-ref="HTTP_Listener_config" path="/echo"/>
   <set-payload value="#['Echo ' ++ now()]" mimeType="text/plain"/>
   <logger level="ERROR" message="request at #[now()]" />
</flow>
```

After execution, the flow produces the following log:

```text
ERROR 2020-03-12 19:13:45,292 [[MuleRuntime].uber.07: [echo].echoFlow.CPU_LITE @63e7e52c]
[event: bd56a240-64ae-11ea-8f7d-f01898419bde] org.mule.runtime.core.internal.processor.LoggerMessageProcessor:
request at 2020-03-12T19:13:45.283-03:00[America/Argentina/Buenos_Aires]
```

In this case, the thread name is `uber.07`. Mule also logs the type of the operation, which in this case is `CPU_LITE`.

Thread names also show up on thread dumps or when using a profiler:
